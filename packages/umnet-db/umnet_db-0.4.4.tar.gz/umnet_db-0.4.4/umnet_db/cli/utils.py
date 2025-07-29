from typing import List
from decouple import Config, RepositoryEnv, UndefinedValueError
from os import getenv
from texttable import Texttable
from netaddr import IPNetwork, EUI
from netaddr.core import AddrFormatError

from ..errors import UMNetDBError
from ..models import Base

MIN_COL_WIDTH = 5
MAX_COL_WIDTH = 50
MAX_TABLE_WIDTH = 0

COLUMNS_BY_TABLE = {k: [c.name for c in v.c] for k, v in Base.metadata.tables.items()}


def get_db_dsn(env_file: str):
    """
    Generates DSN based on provided environment file. If provided file is none, checks
    for path to file in environment variable UMNETDB_ENV
    """
    env_file = env_file if env_file else getenv("UMNETDB_ENV")
    if not env_file:
        raise UMNetDBError("No config file provided, and no UMNETDB_ENV env set!")

    try:
        env = Config(RepositoryEnv(env_file))
    except FileNotFoundError:
        raise UMNetDBError(f"Cannot locate umnet_db environment file {env_file}")

    e = {}
    for var in ["DB_USER", "DB_PASS", "DB_HOST", "DB_PORT", "DB_NAME"]:
        try:
            e[var] = env.get(var)
        except UndefinedValueError:
            raise UMNetDBError(f"Need to set {var} in {env_file}")

    return f"postgresql+psycopg://{e['DB_USER']}:{e['DB_PASS']}@{e['DB_HOST']}:{e['DB_PORT']}/{e['DB_NAME']}"


def generate_cli_table(header: list, rows: List[list]) -> str:
    """
    Takes in a header and rows and draws a texttable.
    Column widths are dynamically set based on the longest entry in each column,
    limited by MAX_COL_WIDTH
    """

    table = Texttable()
    table.set_deco(Texttable.HEADER)

    # starting with minimum column widths and creating a header
    num_cols = len(header)
    table.set_cols_width([MIN_COL_WIDTH] * num_cols)
    table.add_row(header)
    table.set_max_width(MAX_TABLE_WIDTH)

    table.set_cols_width([len(c) for c in header])
    table.set_cols_dtype(["t" for c in header])

    for row in rows:

        row_widths = [len(str(c)) for c in row]
        for t_col_width, r_col_width, idx in zip(
            table._width, row_widths, range(0, num_cols)
        ):
            if r_col_width > t_col_width and r_col_width <= MAX_COL_WIDTH:
                table._width[idx] = r_col_width

        table.add_row(row)

    return table.draw()


def is_ip_or_prefix(ip: str) -> bool:
    """
    Returns whether a string is an ip (10.233.0.10) or
    IP + prefix (10.233.0.10/24). IPv6 works as well.
    """
    try:
        IPNetwork(ip)
    except AddrFormatError:
        return False
    return True


def is_prefix(ip: str) -> bool:
    """
    Returns whether a string is a prefix or not.
    Host routes don't count!
    """
    try:
        ip_obj = IPNetwork(ip)
    except AddrFormatError:
        return False

    # host routes don't count as prefixes!
    if (ip_obj.prefixlen == 32 and ip_obj.version == 4) or (
        ip_obj.prefixlen == 128 and ip_obj.version == 6
    ):
        return False

    return True


def is_mac(mac: str) -> bool:
    """
    Returns whether this is a valid mac address or not
    """
    try:
        EUI(mac)
    except AddrFormatError:
        return False
    return True
