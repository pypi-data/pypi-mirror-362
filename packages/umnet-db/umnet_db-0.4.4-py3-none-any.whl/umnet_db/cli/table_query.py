import argparse
from typing import Union

from sqlalchemy import create_engine, select, or_, cast, String, text, Column
from sqlalchemy.orm import Session

from ..models import Base
from .utils import (
    is_ip_or_prefix,
    is_prefix,
    get_db_dsn,
    COLUMNS_BY_TABLE,
    generate_cli_table,
)


inet_ops = {
    "le": "<<=",
    "ge": ">>=",
    "eq": "=",
}


def generate_where_statement(
    col: Column, search: str, arg_inet_op: Union[str, None]
) -> str:
    """
    Generates where statement based on the datatype of the column we're searching
    or if there's a wildcard (%) in the search string
    """

    # if this is an inet type column do an IP based search
    if str(col.type) == "INET" and is_ip_or_prefix(search):

        # setting the inet op. If the user provided what they wanted to use
        # use, that.
        if arg_inet_op:
            inet_op = inet_ops[arg_inet_op]

        # if the search is a prefix-based search, assume we're looking for
        # hosts within a network (find longer-prefix matches)
        elif is_prefix(search):
            inet_op = ">>="

        # if the search is a host-based search, assume we're looking for
        # the network within the host resides (shorter-prefix match)
        else:
            inet_op = "<<="

        where = text(f"'{search}' {inet_op} {col}")

    # if search string has a '%' in it do a 'like' search
    elif "%" in search:
        where = cast(col, String).like(search)

    # default is exact column search
    else:
        where = col == search

    return where


supbarser_epilog = """
Note that a global search cannot be used when also specifying a column to search.
When you do specify columns, the search will 'and' these logically.

Global search looks for your string in all columns and includes substrings.
Column searches are exact but if you use "%" in your query it'll use a 'like' search to capture
wildcard matches
"""


def main():

    parser = argparse.ArgumentParser(description="Query a umnet_db table")
    parser.add_argument(
        "--env-file",
        help="Path to environment file - you can also set this in your eviroment as UMNETDB_ENV.",
    )

    # adding subparsers for each table column
    subparsers = parser.add_subparsers(dest="table")
    for t, cols in COLUMNS_BY_TABLE.items():

        # skip activity/diff tables
        if t in ["transaction", "activity"]:
            continue

        table_parser = subparsers.add_parser(
            t, help=f"Search the {t} table", epilog=supbarser_epilog
        )
        table_parser.add_argument(
            "global_search", nargs="?", help="Global search of the table"
        )
        for col_name in cols:
            table_parser.add_argument(
                f"--{col_name}", help=f"Search by {col_name} column"
            )
        table_parser.add_argument(
            "--columns",
            nargs="*",
            help="Restrict display to specific columns",
            choices=cols,
        )
        table_parser.add_argument(
            "--inet-op",
            choices=inet_ops,
            help="for IP searches, match on 'le' (contains), 'ge' (contained by), or 'eq' exact match",
        )
        table_parser.add_argument(
            "--sort-by", help="Sort by a particular column (ascending)", choices=cols
        )
        table_parser.add_argument(
            "--descending", help="Reverse sort (descending)", action="store_true"
        )

    args = parser.parse_args()

    if not args.table:
        print(
            "Please specify which table to query. Run this command with '-h' for details."
        )
        exit(1)

    # we either want to search for a single term across all columns,
    # or for specific values in specific columns, not both.
    if args.global_search and len(
        [
            a
            for a in args.__dict__
            if a in COLUMNS_BY_TABLE[args.table] and getattr(args, a)
        ]
    ):
        print(
            "ERROR: Global search combined with column-specific searches is not supported"
        )
        exit(1)

    # Sort parameter. If none provided sort by device - for the device table this is
    # the 'name' column, for every other table it's 'device'
    if args.sort_by:
        sort_by = args.sort_by
    elif args.table == "device":
        sort_by = "name"
    else:
        sort_by = "device"

    engine = create_engine(get_db_dsn(args.env_file))

    table = Base.metadata.tables[args.table]

    if args.columns:
        query = select(table.c[tuple(args.columns)])
    else:
        query = select(table)

    # Adding 'where' statements based on columns or global search queries
    if args.global_search:
        query = query.where(
            or_(
                *[
                    generate_where_statement(c, args.global_search, args.inet_op)
                    for c in table._columns
                ]
            )
        )
    # If user inputted columns to query, we want to do do an 'and' query
    else:
        for col_name in COLUMNS_BY_TABLE[args.table]:
            col_search = getattr(args, col_name)
            if col_search:
                query = query.where(
                    generate_where_statement(
                        table._columns[col_name], col_search, args.inet_op
                    )
                )

    # add on our 'sort by'
    if args.descending:
        query = query.order_by(table._columns[sort_by].desc())
    else:
        query = query.order_by(table._columns[sort_by])

    # execute query and print the result
    with Session(engine) as s:
        result = s.execute(query)
        print(generate_cli_table(result.keys(), list(result)))


if __name__ == "__main__":
    main()
