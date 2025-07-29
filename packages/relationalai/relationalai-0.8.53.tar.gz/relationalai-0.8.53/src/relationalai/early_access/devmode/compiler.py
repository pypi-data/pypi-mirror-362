from __future__ import annotations

import datetime
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from functools import partial
from itertools import chain
from typing import Tuple, cast, Optional, Union
from decimal import Decimal as PyDecimal

from relationalai.early_access.metamodel.rewrite import Flatten
from relationalai.util.graph import topological_sort
from relationalai.early_access.metamodel import ir, compiler as c, visitor as v, factory as f, builtins, types, \
    helpers
from relationalai.early_access.metamodel.typer import Checker, InferTypes, typer
from relationalai.early_access.metamodel.builtins import from_cdc_annotation, concept_relation_annotation
from relationalai.early_access.metamodel.types import Hash, String, Number, Int, Decimal64, Decimal128, Bool, Date, DateTime, Float
from relationalai.early_access.metamodel.util import FrozenOrderedSet, OrderedSet, frozen, ordered_set, filter_by_type, \
    NameCache
from relationalai.early_access.devmode import sql, rewrite


class Compiler(c.Compiler):
    def __init__(self, skip_denormalization:bool=False):
        rewrites = [
            Checker(),
            InferTypes(),
            Flatten(handle_outputs=False),
            rewrite.RecursiveUnion()
        ]
        if not skip_denormalization:
            # group updates, compute SCCs, use Sequence to denote their order
            rewrites.append(rewrite.Denormalize())
        super().__init__(rewrites)
        self.model_to_sql = ModelToSQL()

    def do_compile(self, model: ir.Model, options:dict={}) -> str:
        return str(self.model_to_sql.to_sql(model))


@dataclass
class ModelToSQL:
    """ Generates SQL from an IR Model, assuming the compiler rewrites were done. """

    relation_name_cache: NameCache = field(default_factory=NameCache)
    relation_arg_name_cache: NameCache = field(default_factory=NameCache)

    def to_sql(self, model: ir.Model) -> sql.Program:
        self._register_relation_args(model)
        self._register_external_relations(model)
        return sql.Program(self._sort_dependencies(self._generate_statements(model)))

    def _generate_statements(self, model: ir.Model) -> list[sql.Node]:
        statements: list[sql.Node] = []
        for relation in model.relations:
            if self._is_table_creation_required(relation):
                statements.append(self._create_table(cast(ir.Relation, relation)))
        root = cast(ir.Logical, model.root)
        for child in root.body:
            if isinstance(child, ir.Logical):
                statements.extend(self._create_statement(cast(ir.Logical, child)))
            elif isinstance(child, ir.Union):
                statements.append(self._create_recursive_view(cast(ir.Union, child)))
        return statements

    #--------------------------------------------------
    # SQL Generation
    #--------------------------------------------------
    def _create_table(self, r: ir.Relation) -> sql.Node:
        return sql.CreateTable(
            sql.Table(self._relation_name(r),
                list(map(lambda f: sql.Column(self._var_name(r.id, f), self._convert_type(f.type)), r.fields))
            ))

    def _create_recursive_view(self, union: ir.Union) -> sql.Node:
        assert len(union.tasks) == 2
        assert isinstance(union.tasks[0], ir.Logical)
        assert isinstance(union.tasks[1], ir.Logical)

        def make_case_select(logical: ir.Logical):
            # TODO - improve the typing info to avoid these casts
            lookups = cast(list[ir.Lookup], filter_by_type(logical.body, ir.Lookup))
            # TODO - assuming a single update per case
            update = v.collect_by_type(ir.Update, logical).some()

            # TODO - rewriting references to the view, to use the CTE instead, with _rec
            new_lookups = []
            relation = update.relation
            for lookup in lookups:
                if lookup.relation == relation:
                    new_lookups.append(f.lookup(
                        ir.Relation(f"{lookup.relation.name}_rec", lookup.relation.fields,
                                    frozen(), frozen()), lookup.args, lookup.engine))
                else:
                    new_lookups.append(lookup)

            aliases = []
            for i, arg in enumerate(update.args):
                aliases.append((self._var_name(relation.id, relation.fields[i]), arg))
            return self._make_select(new_lookups, aliases)

        # get a representative update
        update = v.collect_by_type(ir.Update, union).some()

        relation = update.relation
        # TODO - maybe this should be more like INSERT INTO a table than a view?
        return sql.CreateView(self._relation_name(relation),
            sql.CTE(True, f"{self._relation_name(relation)}_rec", [self._var_name(relation.id, f) for f in update.relation.fields], [
                make_case_select(cast(ir.Logical, union.tasks[0])),
                make_case_select(cast(ir.Logical, union.tasks[1]))
            ]))

    def _create_statement(self, task: ir.Logical):

        # TODO - improve the typing info to avoid these casts
        nots = cast(list[ir.Not], filter_by_type(task.body, ir.Not))
        lookups = cast(list[ir.Lookup], filter_by_type(task.body, ir.Lookup))
        updates = cast(list[ir.Update], filter_by_type(task.body, ir.Update))
        outputs = cast(list[ir.Output], filter_by_type(task.body, ir.Output))
        logicals = cast(list[ir.Logical], filter_by_type(task.body, ir.Logical))
        constructs = cast(list[ir.Construct], filter_by_type(task.body, ir.Construct))
        ranks = cast(list[ir.Rank], filter_by_type(task.body, ir.Rank))
        aggs = cast(list[ir.Aggregate], filter_by_type(task.body, ir.Aggregate))
        unions = cast(list[ir.Union], filter_by_type(task.body, ir.Union))
        var_to_rank = {
            r.result: r
            for r in ranks
        } if ranks else {}
        var_to_agg = {
            (a.args[0] if a.aggregation == builtins.count else a.args[1]): a
            for a in aggs
        } if aggs else {}
        var_to_construct = {c.id_var: c for c in constructs} if constructs else {}

        statements = []
        # TODO - this is simplifying soooo much :crying_blood:
        if updates and not lookups and not nots and not aggs and not logicals:
            for u in updates:
                r = u.relation
                if r == builtins.raw_source:
                    lang, src = u.args[0], u.args[1]
                    if not (isinstance(lang, str) and lang.lower() == "sql"):
                        logging.warning(f"Unsupported language for RawSource: {lang}")
                        continue
                    if not isinstance(src, str):
                        raise Exception(f"Expected SQL source to be a string, got: {type(src).__name__}")
                    statements.append(sql.RawSource(src))
                else:
                    # TODO: this is assuming that the updates are all static values
                    # Insert static values: INSERT INTO ... SELECT hash(V1, ...), V2, V3 UNION ALL SELECT hash(V4, ...), V5, V6
                    #   We need to use `SELECT` instead of `VALUES` because Snowflake parses and restricts certain expressions in VALUES(...).
                    #       Built-in functions like HASH() or MD5() are often rejected unless used in SELECT.
                    statements.append(
                        sql.Insert(self._relation_name(r), [self._var_name(r.id, f) for f in r.fields], self._get_tuples(task, u), None)
                    )
        elif lookups or outputs or nots or aggs or updates:
            # Some of the lookup relations we wrap into logical and we need to get them out for the SQL compilation.
            #    For example QB `decimal(0)` in IR will look like this:
            #        Logical ^[res]
            #           Exists(vDecimal128)
            #               Logical
            #                   int_to_decimal128(0, vDecimal128)
            #                   decimal128(vDecimal128, res)
            if logicals:
                unions = self._extract_all_of_type_from_logicals(logicals, ir.Union) + unions
                lookups = self._extract_all_of_type_from_logicals(logicals, ir.Lookup) + lookups
            if updates:
                # insert values that match a query: INSERT INTO ... SELECT ... FROM ... WHERE ...
                for u in updates:
                    r = u.relation
                    aliases = []
                    # We shouldn’t create or populate tables for value types that can be directly sourced from existing Snowflake tables.
                    if not self._is_value_type_population_relation(r):
                        is_rank = False
                        for i, arg in enumerate(u.args):
                            is_rank |= arg in var_to_rank
                            field_name = self._var_name(r.id, r.fields[i])
                            aliases.append(self._get_alias(field_name, arg, var_to_agg, var_to_construct, var_to_rank))

                        statements.append(
                            sql.Insert(self._relation_name(r),
                                       [self._var_name(r.id, f) for f in r.fields], [],
                                       self._make_select(lookups, aliases, nots, aggs, unions, constructs,
                                                         False if is_rank else True)
                            )
                        )
            elif outputs:
                # output a query: SELECT ... FROM ... WHERE ...
                aliases = []
                distinct = False
                for output in outputs:
                    distinct = distinct or output.keys is None
                    for key, arg in output.aliases:
                        aliases.append(self._get_alias(key, arg, var_to_agg, var_to_construct, var_to_rank))

                statements.append(self._make_select(lookups, aliases, nots, aggs, unions, constructs, distinct))
        elif logicals:
            for logical in logicals:
                statements.extend(self._create_statement(logical))
        else:
            raise Exception(f"Cannot create SQL statement for:\n{task}")
        return statements

    def _make_select(self, lookups: list[ir.Lookup], outputs: list[Tuple[str, ir.Value]|Tuple[str, ir.Value, ir.Task]],
                     nots: Optional[list[ir.Not]] = None, aggs: Optional[list[ir.Aggregate]] = None,
                     unions: Optional[list[ir.Union]] = None, constructs: Optional[list[ir.Construct]] = None,
                     distinct: bool = False) -> sql.Select:

        var_to_construct = {c.id_var: c for c in constructs} if constructs else {}

        union_lookups: dict[ir.Union, OrderedSet[ir.Lookup]] = self._extract_all_lookups_per_union(unions)
        all_lookups = lookups + list(chain.from_iterable(union_lookups.values()))

        table_lookups = OrderedSet.from_iterable(t for t in all_lookups if not builtins.is_builtin(t.relation))
        froms, wheres, sql_vars, var_column, var_sql_var, var_lookups = self._extract_lookups_metadata(table_lookups, 0)

        builtin_lookups = OrderedSet.from_iterable(t for t in all_lookups if builtins.is_builtin(t.relation))
        builtin_vars, builtin_wheres = self._resolve_builtins(builtin_lookups, var_lookups, var_column, var_sql_var,
                                                              var_to_construct, outputs)
        wheres.extend(builtin_wheres)

        wheres.extend(self._generate_where_clauses(var_lookups, var_column, sql_vars, var_sql_var, builtin_vars,
                                                   union_lookups, var_to_construct))

        not_null_vars, vars, limit = self._generate_select_output(outputs, builtin_vars, sql_vars, var_column,
                                                                  var_lookups, var_sql_var)

        if not_null_vars:
            wheres.extend(sql.NotNull(var) for var in not_null_vars)

        not_exists, _ = self._generate_select_nots(nots, sql_vars, var_column, len(sql_vars))
        wheres.extend(not_exists)

        where = self._process_wheres_clauses(wheres)

        group_by = self._generate_aggs_group_by(aggs, builtin_vars, sql_vars, var_column, var_lookups)

        return sql.Select(distinct, vars, froms, where, group_by, limit)

    def _extract_lookups_metadata(self, lookups: OrderedSet[ir.Lookup], start_index: int = 0):
        froms: list[sql.From] = []
        wheres: list[sql.Expr] = []
        sql_vars: dict[ir.Lookup, str] = dict()  # one var per table lookup
        var_column: dict[Tuple[ir.Var, ir.Lookup], ir.Field] = dict()
        var_sql_var: dict[ir.Var, str] = dict()
        var_lookups: dict[ir.Var, OrderedSet[ir.Lookup]] = defaultdict(OrderedSet)
        i = start_index

        for lookup in lookups:
            varname = f"v{i}"
            i += 1
            froms.append(sql.From(self._relation_name(lookup.relation), varname))
            sql_vars[lookup] = varname
            relation = lookup.relation
            for j, arg in enumerate(lookup.args):
                rel_field = relation.fields[j]
                if isinstance(arg, ir.Var):
                    var_column[arg, lookup] = rel_field
                    var_sql_var[arg] = varname
                    var_lookups[arg].add(lookup)
                # case when Literal is used as a relation argument: `test(1, x)`
                elif isinstance(arg, (int, str, float, bool, ir.Literal)):
                    ref = f"{sql_vars[lookup]}.{self._var_name(relation.id, rel_field)}"
                    wheres.append(sql.Terminal(f"{ref} = {self._convert_value(arg, False)}"))

        return froms, wheres, sql_vars, var_column, var_sql_var, var_lookups

    def _var_reference(self, var_lookups: dict[ir.Var, OrderedSet[ir.Lookup]], var_sql_var: dict[ir.Var, str],
                       var_column: dict[Tuple[ir.Var, ir.Lookup], ir.Field], v) -> str:
        if isinstance(v, ir.Var):
            # TODO - assuming the built-in reference was grounded elsewhere
            lookup = var_lookups[v].some()
            return f"{var_sql_var[v]}.{self._var_name(lookup.relation.id, var_column[(v, lookup)])}"
        elif isinstance(v, ir.Literal):
            return self._convert_value(v.value)
        elif isinstance(v, datetime.date):
            return f"cast('{v}' as date)"
        return f"'{v}'" if isinstance(v, str) else str(v)

    def _resolve_builtin_var(self, builtin_vars: dict[ir.Var, ir.Value], var):
        # We need recursive lookup because it maybe a case when we need to join more than 2 lookups.
        #    For example QB `a != decimal(0)` in IR will look like this:
        #        Logical ^[res]
        #           Exists(vDecimal128)
        #               Logical
        #                   int_to_decimal128(0, vDecimal128)
        #                   decimal128(vDecimal128, res)
        #        a != res
        #    But we need to convert it to `a != 0` in SQL.
        if isinstance(var, ir.Var) and var in builtin_vars:
            val = builtin_vars[var]
            return self._resolve_builtin_var(builtin_vars, val) if isinstance(val, ir.Var) else val
        return var

    def _resolve_construct_var(self, reference, resolve_builtin_var, construct: ir.Construct):
        # Generate constructions like hash(`x`, `y`, TABLE_ALIAS.COLUMN_NAME)
        elements = []
        for val in construct.values:
            val = resolve_builtin_var(val)
            if isinstance(val, ir.Var):
                elements.append(reference(val))
            else:
                elements.append(self._convert_value(val, True))
        return f"hash({', '.join(elements)})"

    def _resolve_builtins(self, builtin_lookups: OrderedSet[ir.Lookup], var_lookups: dict[ir.Var, OrderedSet[ir.Lookup]],
                          var_column: dict[Tuple[ir.Var, ir.Lookup], ir.Field], var_sql_var: dict[ir.Var, str],
                          var_to_construct: dict[ir.Var, ir.Construct],
                          outputs: Optional[list[Tuple[str, ir.Value]|Tuple[str, ir.Value, ir.Task]]] = None):

        wheres: list[sql.Expr] = []
        builtin_vars: dict[ir.Var, ir.Value] = {}

        output_vars = {
            output[1]
            for output in outputs or []
            if isinstance(output[1], ir.Var)
        }

        intermediate_builtin_vars: set[ir.Var] = {
            arg for lookup in builtin_lookups
            for arg in lookup.args
            if isinstance(arg, ir.Var) and arg not in var_lookups
        }

        reference = partial(self._var_reference, var_lookups, var_sql_var, var_column)
        resolve_builtin_var = partial(self._resolve_builtin_var, builtin_vars)

        for lookup in builtin_lookups:
            args = lookup.args
            relation = lookup.relation
            relation_name = self._relation_name(relation)

            if relation == builtins.substring:
                assert len(args) == 4, f"Expected 4 args for `strings.substring`, got {len(args)}: {args}"

                # Unpack and process arguments
                lhs_raw, from_idx_raw, to_idx_raw, output = args
                assert isinstance(output, ir.Var), "Fourth argument (output) must be a variable"
                from_idx = self._convert_value(from_idx_raw)
                to_idx = self._convert_value(to_idx_raw)

                # Resolve the left-hand side expression
                lhs = lhs_raw if lhs_raw in intermediate_builtin_vars else reference(lhs_raw)
                left = self._var_to_expr(lhs, reference, resolve_builtin_var, var_to_construct) \
                    if isinstance(lhs_raw, ir.Var) else str(lhs)

                # Calculate substring length: SQL is 1-based and end-inclusive
                substring_len = int(to_idx) - int(from_idx) + 2
                assert substring_len >= 0, f"Invalid substring range: from {from_idx} to {to_idx}"

                expr = f"substring({left}, {from_idx}, {substring_len})"
                builtin_vars[output] = expr
            else:
                # Assuming infix binary or ternary operators here
                lhs_raw, rhs_raw = args[0], args[1]
                lhs = lhs_raw if lhs_raw in intermediate_builtin_vars else reference(lhs_raw)
                rhs = rhs_raw if rhs_raw in intermediate_builtin_vars else reference(rhs_raw)
                if relation in builtins.string_binary_builtins:
                    left = self._var_to_expr(lhs_raw, reference, resolve_builtin_var, var_to_construct)
                    if relation == builtins.num_chars and isinstance(rhs_raw, ir.Var):
                        builtin_vars[rhs_raw] = f"length({left})"
                    else:
                        right = self._var_to_expr(rhs_raw, reference, resolve_builtin_var, var_to_construct)
                        if relation == builtins.starts_with:
                            expr = f"concat({right}, '%')" if isinstance(rhs_raw, ir.Var) else f"'{right}%'"
                        elif relation == builtins.ends_with:
                            expr = f"concat('%', {right})" if isinstance(rhs_raw, ir.Var) else f"'%{right}'"
                        elif relation == builtins.like_match:
                            expr = right if isinstance(rhs_raw, ir.Var) else f"'{right}'"
                        elif relation == builtins.contains:
                            expr = f"concat('%', {right}, '%')" if isinstance(rhs_raw, ir.Var) else f"'%{right}%'"
                        else:
                            raise Exception(f"Unsupported string builtin relation: {relation}")
                        wheres.append(sql.Like(left, expr))
                elif relation in builtins.conversion_builtins and isinstance(rhs_raw, ir.Var):
                    if relation == builtins.string and isinstance(lhs_raw, ir.Var) and typer.to_base_primitive(lhs_raw.type) == DateTime:
                        # Convert DateTime to string in the ISO 8601 format.
                        #TODO: This works only in SF and we need to handle it differently for the DuckDB engine.
                        builtin_vars[rhs_raw] = f"""to_varchar({lhs}, 'YYYY-MM-DD"T"HH24:MI:SS.FF3')"""
                    else:
                        # For number conversion relations like `decimal_to_float(x, x_float)`
                        # we need to store mapping to the original value to map it back in the next builtin relation.
                        # example: a = 0.0 in the IR is (decimal_to_float(a, a_float)) and (a_float = 0.0),
                        #   but we will make it back `a = 0.0` in the SQL query.
                        builtin_vars[rhs_raw] = lhs
                elif relation in builtins.date_builtins and isinstance(rhs_raw, ir.Var):
                    expr_map = {
                        builtins.date_year: "year",
                        builtins.date_month: "month",
                        builtins.date_day: "day"
                    }
                    expr = expr_map.get(relation)
                    builtin_vars[rhs_raw] = f"{expr}({lhs})"
                elif helpers.is_type_box(lookup) and isinstance(rhs_raw, ir.Var):
                    # For type box relations we keep the raw var, and we will ground it later.
                    builtin_vars[rhs_raw] = lhs_raw
                elif isinstance(lhs, ir.Var) and lhs in output_vars:
                    builtin_vars[lhs] = self._var_to_expr(rhs, reference, resolve_builtin_var, var_to_construct)
                elif isinstance(rhs, ir.Var) and rhs in output_vars:
                    builtin_vars[rhs] = self._var_to_expr(lhs, reference, resolve_builtin_var, var_to_construct)
                else:
                    left = self._var_to_expr(lhs, reference, resolve_builtin_var, var_to_construct)
                    right = self._var_to_expr(rhs, reference, resolve_builtin_var, var_to_construct)

                    if len(args) == 3:
                        out_var = args[2]
                        if isinstance(out_var, ir.Var):
                            if out_var in builtin_vars:
                                builtin_var = builtin_vars[out_var]
                                if isinstance(builtin_var, ir.Var):
                                    out_var = builtin_var
                            if relation != builtins.concat:
                                expr = f"({left} {relation_name} {right})"

                                # For example, when this is an intermediate result
                                # example: c = a - b in the IR is (a - b = d) and (d = c)
                                builtin_vars[out_var] = expr
                            else:
                                builtin_vars[out_var] = f"{relation_name}({left}, {right})"
                        else:
                            raise Exception(
                                f"Expected `ir.Var` type for the relation `{relation}` output but got `{type(out_var).__name__}`: {out_var}"
                            )
                    else:
                        # Replace intermediate vars with disjoined expressions
                        expr = f"{left} {relation_name} {right}"
                        wheres.append(sql.Terminal(expr))

        return builtin_vars, wheres

    def _generate_where_clauses(self, var_lookups: dict[ir.Var, OrderedSet[ir.Lookup]],
                                var_column: dict[Tuple[ir.Var, ir.Lookup], ir.Field], sql_vars: dict[ir.Lookup, str],
                                var_sql_var: dict[ir.Var, str], builtin_vars: dict[ir.Var, ir.Value],
                                union_lookups: dict[ir.Union, OrderedSet[ir.Lookup]],
                                var_to_construct: dict[ir.Var, ir.Construct]):
        # Reverse mapping: lookup -> union
        lookup_to_union: dict[ir.Lookup, ir.Union] = {}
        for union, lookups in union_lookups.items():
            for lu in lookups:
                lookup_to_union[lu] = union

        reference = partial(self._var_reference, var_lookups, var_sql_var, var_column)
        resolve_builtin_var = partial(self._resolve_builtin_var, builtin_vars)

        wheres: list[sql.Expr] = []
        builtin_clauses: list[sql.Expr] = []
        plain_refs_by_var: dict[ir.Var, list[str]] = defaultdict(list)
        all_union_members: dict[str, dict[ir.Var, str]] = defaultdict(dict)
        for arg, lookup_set in var_lookups.items():
            # if there are 2 lookups for the same variable, we need a join
            if len(lookup_set) > 1:
                # Step 1: Collect all lookups by union member or plain
                for lu in lookup_set:
                    col = var_column[arg, lu]
                    col_name = self._var_name(lu.relation.id, col)

                    matched_union = lookup_to_union.get(lu)
                    if matched_union:
                        for u_lu in union_lookups[matched_union]:
                            u_ref = f"{sql_vars[u_lu]}.{col_name}"
                            all_union_members[sql_vars[u_lu]][arg] = u_ref
                    else:
                        ref = f"{sql_vars[lu]}.{col_name}"
                        plain_refs_by_var[arg].append(ref)

            elif len(lookup_set) == 1:
                lookup = lookup_set[0]
                column = var_column[cast(ir.Var, arg), lookup]
                column_name = self._var_name(lookup.relation.id, column)
                ref = f"{sql_vars[lookup]}.{column_name}"

                # case when we have a builtin operation as a relation argument
                #   example: `test(a - 1, b)` and we are handling here `a - 1` arg.
                if arg in builtin_vars:
                    rhs_ref = self._resolve_builtin_var(builtin_vars, arg)
                    if isinstance(rhs_ref, ir.Var) and rhs_ref in var_lookups:
                        # Case: result of type-boxing variable
                        rhs_lookup = var_lookups[rhs_ref].some()
                        rhs_column = var_column[rhs_ref, rhs_lookup]
                        rhs_column_name = self._var_name(rhs_lookup.relation.id, rhs_column)
                        rhs = f"{sql_vars[rhs_lookup]}.{rhs_column_name}"
                    else:
                        rhs = rhs_ref.name if isinstance(rhs_ref, ir.Var) else str(rhs_ref)
                    builtin_clauses.append(sql.Terminal(f"{ref} = {rhs}"))

                # IR example:
                #   Logical
                #       construct(Manager, "manager_id", "JoeManager", manager_2)
                #       Manager_to_Employee(manager_2, manager_3)
                #       → derive ranking(manager_3, 10)
                elif arg in var_to_construct:
                    rhs = self._resolve_construct_var(reference, resolve_builtin_var, var_to_construct[arg])
                    wheres.append(sql.Terminal(f"{ref} = {rhs}"))

        # Step 2: Build AND chain of plain lookups
        and_clauses = []
        for refs in plain_refs_by_var.values():
            # join variable references pairwise (e.g. "x.id = y.id AND y.id = z.id")
            for lhs, rhs in zip(refs, refs[1:]):
                and_clauses.append(sql.Terminal(f"{lhs} = {rhs}"))

        # Step 3: Build one OR clause across union members
        or_groups: list[sql.Expr] = []
        for member_ref_map in all_union_members.values():
            expressions = []
            for arg_var, rhs in member_ref_map.items():
                plain_refs = plain_refs_by_var.get(arg_var)
                if plain_refs:
                    lhs = plain_refs[-1]  # last plain ref for that var
                    expressions.append(sql.Terminal(f"{lhs} = {rhs}"))
            if expressions:
                or_groups.append(sql.And(expressions) if len(expressions) > 1 else expressions[0])

        wheres.extend(and_clauses)
        wheres.extend(builtin_clauses)
        if or_groups:
            wheres.append(sql.Or(or_groups))

        return wheres

    def _process_wheres_clauses(self, wheres: list[sql.Expr]) -> Optional[sql.Where]:
        # conjunction of not_wheres
        if len(wheres) == 0:
            where = None
        elif len(wheres) == 1:
            where = sql.Where(wheres[0])
        else:
            where = sql.Where(sql.And(wheres))
        return where

    def _generate_aggs_group_by(self, aggs: Optional[list[ir.Aggregate]], builtin_vars: dict[ir.Var, ir.Value],
                                sql_vars: dict[ir.Lookup, str], var_column: dict[Tuple[ir.Var, ir.Lookup], ir.Field],
                                var_lookups: dict[ir.Var, OrderedSet[ir.Lookup]]) -> list[sql.VarRef]:
        group_by: list[sql.VarRef] = []
        if aggs:
            # After flatten it can be only one aggregation per rule.
            agg = aggs[0]
            for var in agg.group:
                resolved_var = var
                # Resolve the variable if it's the result of a builtin
                if var in builtin_vars:
                    # Case: result of type-boxing variable
                    resolved_var = self._resolve_builtin_var(builtin_vars, var)

                if isinstance(resolved_var, ir.Var) and resolved_var in var_lookups:
                    lookup = var_lookups[resolved_var].some()
                    column = var_column[resolved_var, lookup]
                    column_name = self._var_name(lookup.relation.id, column)
                    group_by.append(sql.VarRef(sql_vars[lookup], column_name, None))
                else:
                    # We may group by a result of a builtin operation.
                    # Example: `sum(Person.age).per(strings.len(Person.name))`
                    var_ref = resolved_var.name if isinstance(resolved_var, ir.Var) else str(resolved_var)
                    group_by.append(sql.VarRef(var_ref, None, None))
        return group_by

    def _generate_select_output(self, outputs: list[Tuple[str, ir.Value]|Tuple[str, ir.Value, ir.Task]],
                                builtin_vars: dict[ir.Var, ir.Value], sql_vars: dict[ir.Lookup, str],
                                var_column: dict[Tuple[ir.Var, ir.Lookup], ir.Field],
                                var_lookups: dict[ir.Var, OrderedSet[ir.Lookup]], var_sql_var: dict[ir.Var, str]):
        reference = partial(self._var_reference, var_lookups, var_sql_var, var_column)
        resolve_builtin_var = partial(self._resolve_builtin_var, builtin_vars)
        def handle_lookup_var(var):
            lookup = var_lookups[var].some()
            relation = lookup.relation
            var_name = sql_vars[lookup]
            column_name = self._var_name(relation.id, var_column[var, lookup])
            vars.append(sql.VarRef(var_name, column_name, alias))
            if from_cdc_annotation in lookup.relation.annotations:
                not_null_vars.add(f"{var_name}.{column_name}")
        # finally, compute what the select will return
        vars = []
        # Following flattening, each rule is expected to contain at most one RANK or LIMIT clause.
        limit: Optional[int] = None
        not_null_vars = ordered_set()
        for output in outputs:
            alias, var = output[0], output[1]
            task = output[2] if len(output) > 2 else None
            if isinstance(var, ir.Var):
                if var in var_lookups:
                    handle_lookup_var(var)
                elif var in builtin_vars:
                    var_ref = resolve_builtin_var(var)
                    if var_ref in var_lookups:
                        # Case: result of type-boxing variable
                        handle_lookup_var(var_ref)
                    else:
                        # Example: We may have `decimal(0)` in QB which turns in IR into:
                        #   (int_to_decimal128(0, vDecimal128) and decimal128(vDecimal128, res_3))
                        #   and we need to make it `0` in SQL.
                        var_ref = var_ref.name if isinstance(var_ref, ir.Var) else str(var_ref)
                        vars.append(sql.VarRef(var_ref, None, alias))
                elif task:
                    if isinstance(task, ir.Construct):
                        # Generate constructions like hash(`x`, `y`, TABLE_ALIAS.COLUMN_NAME) as `alias`
                        elements = []
                        for v in task.values:
                            if v in builtin_vars:
                                v = resolve_builtin_var(v)
                            if isinstance(v, ir.Var):
                                lookup = var_lookups[v].some()
                                column_name = self._var_name(lookup.relation.id, var_column[v, lookup])
                                lookup_var = f"{sql_vars[lookup]}.{column_name}"
                                elements.append(lookup_var)
                                if from_cdc_annotation in lookup.relation.annotations:
                                    not_null_vars.add(lookup_var)
                            else:
                                elements.append(self._convert_value(v, True))
                        vars.append(sql.VarRef(f"hash({', '.join(elements)})", None, alias))
                    elif isinstance(task, ir.Rank):
                        limit = task.limit
                        order_by_vars = []
                        for arg, is_ascending in zip(task.args, task.arg_is_ascending):
                            order_by_vars.append(sql.OrderByVar(reference(arg), is_ascending))
                        partition_by_vars = [reference(arg) for arg in task.group] if task.group else []
                        vars.append(sql.RowNumberVar(order_by_vars, partition_by_vars, alias))
                    elif isinstance(task, ir.Aggregate):
                        result_arg = task.projection[0] if task.aggregation == builtins.count else task.args[0]
                        result_arg = resolve_builtin_var(result_arg)
                        ref = reference(result_arg) if isinstance(result_arg, ir.Var) else str(result_arg)
                        vars.append(sql.VarRef(f"{task.aggregation.name}({ref})", None, alias))
            else:
                # TODO - abusing even more here, because var is a value!
                value = self._convert_value(var, False)
                vars.append(sql.VarRef(str(value), None, alias))
        return not_null_vars, vars, limit

    def _generate_select_nots(self, nots: Optional[list[ir.Not]], sql_vars: dict[ir.Lookup, str],
                              var_column:dict[Tuple[ir.Var, ir.Lookup], ir.Field], index: int) -> tuple[list[sql.NotExists], int]:
        not_exists = []
        if nots:
            for not_expr in nots:
                unions = []
                inner_nots = []
                constructs = []
                if isinstance(not_expr.task, ir.Lookup):
                    all_lookups = [not_expr.task]
                else:
                    logical = cast(ir.Logical, not_expr.task)
                    all_lookups = cast(list[ir.Lookup], filter_by_type(logical.body, ir.Lookup))
                    logicals = cast(list[ir.Logical], filter_by_type(logical.body, ir.Logical))
                    inner_nots = cast(list[ir.Not], filter_by_type(logical.body, ir.Not))
                    unions = cast(list[ir.Union], filter_by_type(logical.body, ir.Union))
                    constructs = cast(list[ir.Construct], filter_by_type(logical.body, ir.Construct))

                    # Some of the lookup relations we wrap into logical and we need to get them out for the SQL compilation.
                    #    For example QB `decimal(0)` in IR will look like this:
                    #        Logical ^[res]
                    #           Exists(vDecimal128)
                    #               Logical
                    #                   int_to_decimal128(0, vDecimal128)
                    #                   decimal128(vDecimal128, res)
                    if logicals:
                        unions = self._extract_all_of_type_from_logicals(logicals, ir.Union) + unions
                        all_lookups = self._extract_all_of_type_from_logicals(logicals, ir.Lookup) + all_lookups

                union_lookups: dict[ir.Union, OrderedSet[ir.Lookup]] = self._extract_all_lookups_per_union(unions)
                all_lookups.extend(list(chain.from_iterable(union_lookups.values())))

                lookups = OrderedSet.from_iterable(t for t in all_lookups if not builtins.is_builtin(t.relation))
                froms, wheres, not_sql_vars, not_var_column, not_var_sql_var, not_var_lookups \
                    = self._extract_lookups_metadata(lookups, index)
                index += len(not_sql_vars)

                var_to_construct = {c.id_var: c for c in constructs} if constructs else {}
                builtin_lookups = OrderedSet.from_iterable(t for t in all_lookups if builtins.is_builtin(t.relation))
                builtin_vars, builtin_wheres = self._resolve_builtins(builtin_lookups, not_var_lookups, not_var_column,
                                                                      not_var_sql_var, var_to_construct)
                wheres.extend(builtin_wheres)

                # We need to join the not exists select with the outside select query context
                for arg, lookup_set in not_var_lookups.items():
                    if len(lookup_set) > 0:
                        lu = lookup_set[0]
                        column = not_var_column[cast(ir.Var, arg), lu]
                        column_name = self._var_name(lu.relation.id, column)
                        lhs = f"{not_sql_vars[lu]}.{column_name}"

                        # lookup the same var from the outside context to make the join
                        matching_lookup = next(
                            (lookup for (var, lookup) in var_column if var == arg),
                            None
                        )

                        if matching_lookup is not None:
                            matching_column = var_column[(arg, matching_lookup)]
                            matching_column_name = self._var_name(matching_lookup.relation.id, matching_column)
                            rhs = f"{sql_vars[matching_lookup]}.{matching_column_name}"
                            wheres.append(sql.Terminal(f"{lhs} = {rhs}"))

                wheres.extend(self._generate_where_clauses(not_var_lookups, not_var_column, not_sql_vars,
                                                           not_var_sql_var, builtin_vars, union_lookups, var_to_construct))

                inner_not_exists, index = self._generate_select_nots(inner_nots, not_sql_vars, not_var_column, index)
                wheres.extend(inner_not_exists)

                where = self._process_wheres_clauses(wheres)
                not_exists.append(sql.NotExists(sql.Select(False, [1], froms, where)))

        return not_exists, index

    def _extract_all_of_type_from_logicals(self, logicals: list[ir.Logical], target_type: type) -> list:
        """Recursively extract all instances of `target_type` from a list of Logical tasks."""
        result = ordered_set()

        def visit(logical: ir.Logical):
            for expr in logical.body:
                if isinstance(expr, ir.Logical):
                    visit(expr)
                elif isinstance(expr, target_type):
                    result.add(expr)

        for logical in logicals or []:
            visit(logical)

        return result.list if result.list else []

    def _extract_all_lookups_per_union(self, unions: Optional[list[ir.Union]]) -> dict[ir.Union, OrderedSet[ir.Lookup]]:
        union_lookups: dict[ir.Union, OrderedSet[ir.Lookup]] = defaultdict(OrderedSet)
        for union in unions or []:
            for task in union.tasks:
                if isinstance(task, ir.Logical):
                    union_lookups[union].update(self._extract_all_of_type_from_logicals([task], ir.Lookup))
                elif isinstance(task, ir.Lookup):
                    union_lookups[union].add(cast(ir.Lookup, task))
        return union_lookups

    def _var_to_expr(self, var, reference, resolve_builtin_var, var_to_construct: dict[ir.Var, ir.Construct]):
        """
        Convert a variable to an expression string.
        """
        if isinstance(var, ir.Var) and var in var_to_construct:
            return self._resolve_construct_var(reference, resolve_builtin_var, var_to_construct[var])
        resolved = resolve_builtin_var(var)
        return reference(resolved) if isinstance(resolved, ir.Var) else str(resolved)

    def _get_alias(self, key, arg, var_to_agg, var_to_construct, var_to_rank):
        if not isinstance(arg, ir.Var):
            return key, arg

        var_task = var_to_construct.get(arg) or var_to_rank.get(arg) or var_to_agg.get(arg)
        return (key, arg, var_task) if var_task else (key, arg)

    def _get_tuples(self, logical: ir.Logical, u: ir.Update):
        """
        Get a list of tuples to perform this update.

        This function traverses the update args, assuming they contain only static values or
        variables bound to a construct task, and generates a list of tuples to insert. There
        may be multiple tuples because arguments can be lists of values bound to a field
        whose role is multi.
        """
        # TODO - this only works if the variable is bound to a Construct task, we need a more general approach.

        def find_construct(var):
            for stmt in logical.body:
                if isinstance(stmt, ir.Construct) and stmt.id_var == var:
                    return stmt
            return None

        def resolve_value(arg):
            if isinstance(arg, ir.Var):
                construct = find_construct(arg)
                if not construct:
                    return self._convert_value(arg)

                resolved = []
                for val in construct.values:
                    if isinstance(val, ir.Var):
                        inner_construct = find_construct(val)
                        if inner_construct:
                            nested = [self._convert_value(x, True) for x in inner_construct.values]
                            resolved.append(f"hash({', '.join(nested)})")
                        else:
                            resolved.append(self._convert_value(val, True))
                    else:
                        resolved.append(self._convert_value(val, True))

                return f"hash({', '.join(resolved)})"
            elif isinstance(arg, FrozenOrderedSet):
                return frozen(*[self._convert_value(v) for v in arg])
            else:
                return self._convert_value(arg)

        values = [resolve_value(a) for a in u.args]
        return self._product(values)

    def _product(self, values):
        """ Compute a cartesian product of values when the value is a FrozenOrderedSet. """
        # TODO - some pass needs to check that this is correct, i.e. that we are using a
        # FrozenOrderedSet only if the field is of role multi.
        tuples = [[]]
        for value in values:
            if isinstance(value, FrozenOrderedSet):
                tuples = [prev + [element] for prev in tuples for element in value]
            else:
                tuples = [prev + [value] for prev in tuples]
        return [tuple(t) for t in tuples]

    def _convert_value(self, v, quote_numbers:bool=False) -> str:
        """ Convert the literal value in v to a SQL value."""
        if isinstance(v, str):
            return f"'{v}'"
        if isinstance(v, PyDecimal):
            return str(v)
        if isinstance(v, ir.ScalarType):
            return f"'{v.name}'"
        if isinstance(v, ir.Literal):
            return self._convert_value(v.value, quote_numbers)
        return v if not quote_numbers else f"'{v}'"

    BUILTIN_CONVERSION = {
        Hash: "DECIMAL(38, 0)",
        String: "TEXT",
        Number: "DOUBLE",
        Int: "INT",
        Decimal64: "DECIMAL(19, 6)",
        Decimal128: "DECIMAL(38, 10)",
        Bool: "BOOLEAN",
        Date: "DATE",
        DateTime: "DATETIME",
        Float: "FLOAT(53)",
    }
    def _convert_type(self, t: ir.Type) -> str:
        """ Convert the type t into the equivalent SQL type."""
        # entities become DECIMAL(38, 0)
        if not types.is_builtin(t) and not types.is_value_type(t):
            return "DECIMAL(38, 0)"

        # convert known builtins
        base_type = typer.to_base_primitive(t)
        if isinstance(base_type, ir.ScalarType) and base_type in self.BUILTIN_CONVERSION:
            return self.BUILTIN_CONVERSION[base_type]
        raise Exception(f"Unknown built-in type: {t}")

    def _is_table_creation_required(self, r: ir.Relation) -> bool:
        """
        Determine whether the given relation should result in a SQL table creation.

        Skips creation for:
        - Built-in relations or annotations
        - CDC relations
        - Boxed types or special "rank" name
        - Relations with unresolved field types (types.Any)
        - ValueType population relations
        """
        if (
            builtins.is_builtin(r) or
            builtins.is_annotation(r) or
            from_cdc_annotation in r.annotations or
            helpers.is_type_box(r) or
            r.name == "rank"
        ):
            return False

        if any(relation_field.type == types.Any for relation_field in r.fields):
            if not r.overloads:
                raise ValueError(f"Relation '{r.name}' has unresolved field types (`types.Any`) and no overloads.")
            return False

        return not self._is_value_type_population_relation(r)

    @staticmethod
    def _is_value_type_population_relation(r: ir.Relation) -> bool:
        """
        Check if the relation is a ValueType population relation:
        - Has exactly one field
        - Field type is a value type
        - Annotated with concept_relation_annotation
        """
        if not r.fields or len(r.fields) != 1:
            return False
        return types.is_value_type(r.fields[0].type) and concept_relation_annotation in r.annotations

    def _relation_name(self, relation: ir.Relation):
        if helpers.is_external(relation) or helpers.builtins.is_builtin(relation):
            return relation.name
        return self.relation_name_cache.get_name(relation.id, relation.name, helpers.relation_name_prefix(relation))

    def _register_external_relations(self, model: ir.Model):
        # force all external relations to get a name in the cache, so that internal relations
        # cannot use those names in _relation_name
        for r in model.relations:
            if helpers.is_external(r):
                self.relation_name_cache.get_name(r.id, r.name)

    def _var_name(self, relation_id: int, arg: Union[ir.Var, ir.Field]):
        return self.relation_arg_name_cache.get_name((relation_id, arg.id), arg.name)

    def _register_relation_args(self, model: ir.Model):
        """
        Register all relation arguments in the cache to ensure they have unique names.
        This is necessary for SQL compilation to avoid name collisions.
        """
        self.relation_arg_name_cache = NameCache()
        for r in model.relations:
            if self._is_table_creation_required(r):
                for f in r.fields:
                    self.relation_arg_name_cache.get_name((r.id, f.id), f.name)

    # TODO: need to check if inserts may depend on any view and if so then sort them together.
    def _sort_dependencies(self, statements: list[sql.Node]) -> list[sql.Node]:
        """
            Sorts SQL statements to ensure proper execution order:
            1. CREATE TABLE statements
            2. INSERT statements (topologically sorted by dependencies)
            3. UPDATE statements
            3. Other statements except SELECT queries (e.g., CREATE VIEW, etc.)
            4. SELECT queries
        """
        create_tables = []
        inserts: dict[str, list[sql.Insert]] = defaultdict(list)
        updates = []
        miscellaneous_statements = []
        selects = []

        for statement in statements:
            if isinstance(statement, sql.CreateTable):
                create_tables.append(statement)
            elif isinstance(statement, sql.Insert):
                inserts[statement.table].append(statement)
            elif isinstance(statement, sql.Update):
                updates.append(statement)
            elif isinstance(statement, sql.Select):
                selects.append(statement)
            else:
                miscellaneous_statements.append(statement)

        sorted_inserts = self._sort_inserts_dependency_graph(inserts)

        return create_tables + sorted_inserts + updates + miscellaneous_statements + selects

    @staticmethod
    def _sort_inserts_dependency_graph(insert_statements: dict[str, list[sql.Insert]]) -> list[sql.Insert]:
        """ Topologic sort INSERT statements based on dependencies in their SELECT FROM clauses. """
        nodes = list(insert_statements.keys())
        edges = []

        for target_table, inserts in insert_statements.items():
            for insert in inserts:
                select = insert.select
                if select and select.froms:
                    for from_clause in select.froms:
                        edges.append((from_clause.table, target_table))

        sorted_tables = topological_sort(nodes, edges)

        sorted_inserts = []
        for table in sorted_tables:
            if table in insert_statements:
                sorted_inserts.extend(insert_statements[table])

        return sorted_inserts
