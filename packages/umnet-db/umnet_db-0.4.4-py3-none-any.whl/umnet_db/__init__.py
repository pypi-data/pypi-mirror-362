from typing import List, Dict

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from .cli.utils import get_db_dsn


class UMNetdb:
    """
    Class you can initiate with a DSN or path to an env file that
    will do a bunch of queries for you - intended to be imported by
    other libraries.
    """

    def __init__(self, dsn: str = None, env_file: str = None):
        """
        Initiate a umnetdb object. Note that you must provide either a dsn or a path
        to an env file that looks like the 'sample_env' provided in this repo.
        If both are provided, the DSN takes precedence.
        """
        self.session = None
        self.engine = None

        if dsn:
            self.engine = create_engine(dsn)
        elif env_file:
            self.engine = create_engine(get_db_dsn(env_file))
        else:
            raise ValueError("Must provide dsn or env file to instantiate UMNetdb")

    def open(self):
        """
        Create a new session to the database if there isn't one already
        """
        if not self.session:
            self.session = Session(self.engine)

    def close(self):
        """
        Closes db session if there is one
        """
        if self.session:
            self.session.close()
            self.session = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, fexc_type, exc_val, exc_tb):
        self.close()

    def get_device_neighbors(
        self, device: str, known_devices_only: bool = True
    ) -> List[dict]:
        """
        Gets a list of the neighbors of a particular device. If the port
        has a parent in the LAG table that is included as well.
        Neighbor hostname is also looked up in the device table and
        the "source of truth" hostname is returned instead of what shows
        up in lldp neighbor.

        Setting 'known_devices_only' to true only returns neighbors that are found
        in umnet_db's device table. Setting it to false will return all lldp neighbors.

        Returns results as a list of dictionary entries keyed on column names.
        """

        if known_devices_only:
            query = f"""
select n.port,
n_d.name as remote_device,
n.remote_port,
l.parent,
n_l.parent as remote_parent
from neighbor n

join device n_d on n_d.hostname=n.remote_device
left outer join lag l on l.device=n.device and l.member=n.port
left outer join lag n_l on n_l.device=n_d.name and n_l.member=n.remote_port
where n.device='{device}'
        """
        else:
            query = f"""
select n.port,
coalesce(n_d.name, n.remote_device) as remote_device,
n.remote_port,
l.parent,
n_l.parent as remote_parent
from neighbor n

left outer join device n_d on n_d.hostname=n.remote_device
left outer join lag l on l.device=n.device and l.member=n.port
left outer join lag n_l on n_l.device=n_d.name and n_l.member=n.remote_port
    where n.device='{device}'
            """

        result = self.session.execute(text(query))
        return [dict(zip(result.keys(), r)) for r in result]
