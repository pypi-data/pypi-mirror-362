import argparse

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, configure_mappers
from postgresql_audit import versioning_manager

from ..models import Base
from .utils import get_db_dsn


def main():

    parser = argparse.ArgumentParser(description="Initialize UMnetdb database")
    parser.add_argument(
        "--env-file",
        help="Path to environment file - you can also set this in your eviroment as UMNETDB_ENV.",
    )
    args = parser.parse_args()

    db_url = get_db_dsn(args.env_file)

    engine = create_engine(db_url)
    print(f"connecting to {db_url}")
    engine.connect()
    print("done")
    with Session(engine) as session:

        # extension needed for postresql-audit; https://github.com/kvesteri/postgresql-audit/issues/44
        session.execute(text("CREATE EXTENSION btree_gist;"))
        session.commit()

        configure_mappers()

        # need to create versioning manager tables before creating all other tables
        # if not session.execute(text("select table_name from information_schema.tables where table_name='activity'")):
        versioning_manager.transaction_cls.__table__.create(engine)
        versioning_manager.activity_cls.__table__.create(engine)

        Base.metadata.create_all(engine)
        session.commit()


if __name__ == "__main__":
    main()
