from typing import List, Dict, Union

from sqlalchemy.engine import Result
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy import delete

from .models import Base

COL_WIDTH_SPACER = 2
MAX_COL_WIDTH = 30


def db_merge(engine: Engine, entry: Base):
    """
    Merges an ORM object
    """
    with Session(engine) as session:
        session.merge(entry)
        session.commit()


def result_to_cli_string(result: Result) -> str:
    """
    Returns a string that prints out a nice table of sqlalchemy results
    on the cli
    """

    # width of each column
    col_widths = {}

    # list of dicts denoting the table to output
    output = []

    # first we're size our column widths based on the length of the data
    for row in result.scalars():
        # initializing column widths to match the header column + spacer
        if not col_widths:
            for col in row.__table__.columns:
                col_widths[col.name] = len(col.name) + COL_WIDTH_SPACER

        for col_name, col_width in col_widths.items():
            row_col_width = len(str(getattr(row, col_name, "")))
            if row_col_width + COL_WIDTH_SPACER > col_width:
                col_widths[col_name] = row_col_width + COL_WIDTH_SPACER

        # saving row output into our list - you can only iterate over `results.scalars` once!
        output.append({c: str(getattr(row, c, "")) for c in col_widths})

    # now we will turn our output list of lists into a giant string sized
    # on our column widths
    output_str = "".join(
        [c_name.ljust(c_width) for c_name, c_width in col_widths.items()]
    )
    for row in output:
        output_str += "\n" + "".join(
            [row[c_name].ljust(c_width) for c_name, c_width in col_widths.items()]
        )

    return output_str


def delete_and_rebuild_device(
    session: Session, device: str, table: Base, data: Union[Dict, List[Dict]]
):
    """
    Takes in an existing db session, the name of a table, name of the device,
    and a list of rows to update.
    First removes all rows matching the key {col_name, col_data},
    Then inserts ("adds") rows in the data.
    """
    session.execute(delete(table).where(getattr(table, "device") == device))
    session.commit()

    if isinstance(data, dict):
        data = [data]

    for row in data:
        entry = table()
        try:
            setattr(entry, "device", device)
            for k, v in row.items():
                setattr(entry, k, v)
        except AttributeError:
            print(f"Dict to db error for {table}: {row}")
            del entry
            continue

        session.add(entry)
    session.commit()
