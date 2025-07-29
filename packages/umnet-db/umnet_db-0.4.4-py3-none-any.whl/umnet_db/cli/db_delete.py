import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import re

from ..models import Base
from .utils import get_db_dsn


def main():

    parser = argparse.ArgumentParser(description="Clear our drop a table or all tables")
    parser.add_argument("table", choices=list(Base.metadata.tables).append("all"))
    parser.add_argument(
        "--env-file",
        help="Path to environment file - you can also set this in your eviroment as UMNETDB_ENV.",
    )
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Actually drop the table instead of just deleting the contents",
    )
    args = parser.parse_args()

    if args.table == "all":
        are_you_sure = input(
            "Are you sure you want to delete ALL tables? Type y or yes to confirm: "
        )
    else:
        are_you_sure = input(
            f"Are you sure you want to delete {args.table}? Type y or yes to confirm: "
        )
    if not (re.match("(y|yes)$", are_you_sure, re.IGNORECASE)):
        print("ok, never mind")
        exit(1)

    engine = create_engine(get_db_dsn(args.env_file))

    with Session(engine) as session:
        if args.table == "all" and args.drop:
            Base.metadata.drop_all(engine)

        elif args.table == "all":
            for table in Base.metadata.tables.values():
                session.execute(table.delete())

        elif args.drop:
            Base.metadata.tables[args.table].drop(engine)
        else:
            session.execute(Base.metadata.tables[args.table].delete())

        session.commit()


if __name__ == "__main__":
    main()
