# pylint: disable=too-many-ancestors, missing-class-docstring, too-few-public-methods
from datetime import timedelta, datetime
from typing import Optional
from json import dumps


from netaddr import IPAddress, IPNetwork, EUI

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
import sqlalchemy.types as types
from sqlalchemy.dialects import postgresql
from sqlalchemy import String, ARRAY

from postgresql_audit import versioning_manager

from .errors import UMnetDBModelError

__all__ = (
    "Base",
    "Device",
    "Neighbor",
    "Lag",
    "ARP",
    "IPInterface",
    "Route",
    "VNI",
    "MPLS",
    "Inventory",
)


##########################################
#### SQLalchemy special Network Types ####
# Note that we're using the netaddr library because
# its classes are for both IPv4 and IPv6
class IPAddressType(types.TypeDecorator):
    impl = postgresql.INET
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return str(value) if value else None

    def process_result_value(self, value, dialect):
        return IPAddress(str(value)) if value else None

    @property
    def python_type(self):
        return IPAddress


class IPNetworkType(types.TypeDecorator):
    impl = postgresql.INET
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return str(value) if value else None

    def process_result_value(self, value, dialect):
        return IPNetwork(str(value)) if value else None

    @property
    def python_type(self):
        return IPNetwork


class MACAddressType(types.TypeDecorator):
    impl = postgresql.MACADDR
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return str(value) if value else None

    def process_result_value(self, value, dialect):
        return EUI(value) if value else None

    @property
    def python_type(self):
        return EUI


#####################################################
#### SQLalchemy Base models and versioning manager ####
class Base(DeclarativeBase):

    def as_dict(self):
        """
        Return rows as dict
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.c}

    def as_json(self):
        """
        Return rows as json
        """
        return dumps(self.as_dict())

    @classmethod
    def from_dict(cls, input: dict):
        """
        Builds a row object from an inputted dictionary, casting from strings/
        integers/etc to the appropriate "mapped" python types for our models
        """
        casted = {}
        for col_name, value in input.items():

            if col_name not in cls.__table__.c.keys():
                raise UMnetDBModelError(
                    f"Invalid column name {col_name} for {cls.__tablename__}"
                )

            col = cls.__table__.c[col_name]

            # for list types, evaluate each item
            if col.type._is_array:
                if not isinstance(value, list):
                    raise UMnetDBModelError(
                        f"column {col_name} for {cls.__tablename__} requires list input"
                    )
                casted[col_name] = [cls._cast_value(i, col) for i in value]

            # for non-list types, convert input value
            else:
                casted[col_name] = cls._cast_value(value, col)

        return cls(**casted)

    @classmethod
    def _cast_value(cls, value, col):
        """
        Casts a particular input value to the db type
        """

        # forcing empty strings/lists etc to 'None'
        # for nullable values
        if col.nullable and not value:
            return None

        try:
            return col.type.python_type(value)
        except Exception as e:
            raise UMnetDBModelError(
                f"Invalid input '{value}' for {cls.__tablename__} {col.name}: {e}"
            )

    def __repr__(self):
        """
        Row repr, eg "Table(pk1_name='pk1_val', pk2_name='pk2_val'..)"
        """
        return (
            f"{self.__class__.__name__}("
            + ", ".join(
                [
                    f"{k.name}='{getattr(self, k.name)}'"
                    for k in self.__table__.primary_key.columns
                ]
            )
            + ")"
        )


versioning_manager.init(Base)


# mapped columns must be defined after versioning manager is initialized
class Versioned(object):
    """
    Versioned mixin
    """

    __versioned__ = {"exclude": ["last_updated"]}
    first_seen: Mapped[datetime]
    last_updated: Mapped[datetime]


class NonVersioned(object):
    """
    NonVersioned Mixin
    """

    first_seen: Mapped[datetime]
    last_updated: Mapped[datetime]


####################################
#### umnetdb table definitions ####
class Device(Versioned, Base):
    __tablename__ = "device"

    __versioned__ = {"exclude": ["last_updated", "uptime"]}

    name: Mapped[str] = mapped_column(primary_key=True)
    hostname: Mapped[str]
    ip: Mapped[IPAddress] = mapped_column(IPAddressType)
    version: Mapped[Optional[str]]
    vendor: Mapped[Optional[str]]
    model: Mapped[Optional[str]] = mapped_column(String(40))
    serial: Mapped[Optional[str]]
    uptime: Mapped[timedelta]


class Neighbor(Versioned, Base):
    __tablename__ = "neighbor"

    device: Mapped[str] = mapped_column(primary_key=True)
    port: Mapped[str] = mapped_column(primary_key=True)
    remote_device: Mapped[str]
    remote_port: Mapped[str]


class Lag(Versioned, Base):
    """
    Table of LAG members, statuses, and their parent mappings
    """

    __tablename__ = "lag"

    device: Mapped[str] = mapped_column(primary_key=True)
    member: Mapped[str] = mapped_column(primary_key=True)
    parent: Mapped[str] = mapped_column(primary_key=True)
    protocol: Mapped[str]
    admin_up: Mapped[bool]
    oper_up: Mapped[bool]
    peer_link: Mapped[bool]
    vpc_id: Mapped[int]


class ARP(NonVersioned, Base):
    __tablename__ = "arp"

    device: Mapped[str] = mapped_column(primary_key=True)
    interface: Mapped[str] = mapped_column(String(50), primary_key=True)
    ip: Mapped[IPAddress] = mapped_column(IPAddressType, primary_key=True)
    mac: Mapped[EUI] = mapped_column(MACAddressType, primary_key=True)


class IPInterface(Versioned, Base):
    __tablename__ = "ip_interface"

    device: Mapped[str] = mapped_column(primary_key=True)
    ip_address: Mapped[IPNetwork] = mapped_column(IPNetworkType, primary_key=True)
    interface: Mapped[str] = mapped_column(String(50), primary_key=True)
    description: Mapped[Optional[str]]
    mtu: Mapped[int]
    admin_up: Mapped[bool]
    oper_up: Mapped[bool]
    vrf: Mapped[Optional[str]]
    secondary: Mapped[bool]
    helpers: Mapped[list[str]] = mapped_column(ARRAY(String))


class Route(Versioned, Base):
    """
    Device route tables. Note that we mean *active* routes (the FIB).
    In reality pulling the FIB directly off a device is not
    straightforward, and helpful information like protocol and age are not present.
    As a result, this data is actually populated via "show ip route vrf all" (cisco),
    "show route active-path" (junos), "show routing route" (panos)
    """

    __tablename__ = "route"

    # also want to exclude 'age' from being versioned
    __versioned__ = {"exclude": ["last_updated", "age"]}

    device: Mapped[str] = mapped_column(primary_key=True)
    vrf: Mapped[str] = mapped_column(primary_key=True)
    prefix: Mapped[IPNetwork] = mapped_column(IPNetworkType, primary_key=True)
    learned_from: Mapped[str] = mapped_column(primary_key=True)

    nh_ip: Mapped[Optional[IPAddress]] = mapped_column(IPAddressType)
    nh_interface: Mapped[Optional[str]]
    nh_table: Mapped[str]

    protocol: Mapped[str]
    age: Mapped[Optional[timedelta]]

    mpls_label: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    vxlan_vni: Mapped[Optional[int]]
    vxlan_endpoint: Mapped[Optional[IPAddress]] = mapped_column(IPAddressType)


class VNI(Versioned, Base):
    __tablename__ = "vni"

    device: Mapped[str] = mapped_column(primary_key=True)
    vni: Mapped[str] = mapped_column(primary_key=True)
    vrf: Mapped[Optional[str]]
    vlan_id: Mapped[Optional[int]]


class MPLS(Versioned, Base):
    """
    MPLS forwarding tables.
    Note that for aggregate labels the "nh_interface" is actually the
    VRF name!
    """

    __tablename__ = "mpls"

    device: Mapped[str] = mapped_column(primary_key=True)
    in_label: Mapped[int] = mapped_column(primary_key=True)
    out_label: Mapped[list[str]] = mapped_column(ARRAY(String))
    nh_interface: Mapped[str] = mapped_column(primary_key=True)
    aggregate: Mapped[bool]

    # NB: string instead of IP type because I've seen malformed FEC data
    # (eg 2607:f018:fffd:100:ffff:ffff:ffff:ff48/12)
    fec: Mapped[Optional[str]]
    nh_ip: Mapped[Optional[IPAddress]] = mapped_column(IPAddressType)
    rd: Mapped[Optional[str]]


class Inventory(Versioned, Base):
    """
    Inventory data
    """

    __tablename__ = "inventory"

    device: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(primary_key=True)
    subtype: Mapped[Optional[str]]
    part_number: Mapped[Optional[str]]
    serial_number: Mapped[Optional[str]]
