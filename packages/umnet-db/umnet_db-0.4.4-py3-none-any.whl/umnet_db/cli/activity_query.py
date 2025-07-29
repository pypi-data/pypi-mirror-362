import argparse

from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import Session

from postgresql_audit import versioning_manager

from ..models import Base, Versioned
from .utils import get_db_dsn, COLUMNS_BY_TABLE


def main():

    parser = argparse.ArgumentParser(
        description="Query the activity table for changes to the database"
    )
    parser.add_argument(
        "--env-file",
        help="Path to environment file - you can also set this in your eviroment as UMNETDB_ENV.",
    )
    # adding subparsers for each table column
    subparsers = parser.add_subparsers(dest="table")
    for mapper in Base.registry.mappers:

        # skip non-versioned tables
        if not issubclass(mapper.class_, Versioned):
            continue

        t = mapper.local_table

        table_parser = subparsers.add_parser(
            t.name, help=f"Search for activity around the {t.name} table"
        )
        for col in t.c:
            table_parser.add_argument(
                f"--{col.name}", help=f"Search by {col.name} column"
            )
        table_parser.add_argument(
            "--columns",
            nargs="*",
            help="Restrict display to specific columns",
            choices=[c.name for c in t.c],
        )

    args = parser.parse_args()

    engine = create_engine(get_db_dsn(args.env_file))

    activity = versioning_manager.activity_cls

    # querying the activity table
    query = select(activity.issued_at, activity.verb, activity.changed_data).where(
        activity.table_name == args.table
    )

    for col_name in COLUMNS_BY_TABLE[args.table]:
        col_query = getattr(args, col_name)
        if col_query:
            query = query.filter(
                or_(
                    activity.changed_data[col_name].astext == col_query,
                    activity.old_data[col_name].astext == col_query,
                )
            )

    # execute query and print the result
    with Session(engine) as s:
        result = s.execute(query)

        # need to unroll
        for r in result:
            print(f"{r.issued_at}: {r.verb} {r.changed_data}")

        # need to convert to dict and un-nest
        # data = [r[0] for r in list(result)]

        # need to un-nest 'changed data'

        # print(data[0].as_dict())
        # print(generate_cli_table(data[0].keys(), [r.values() for r in data]))


if __name__ == "__main__":
    main()
