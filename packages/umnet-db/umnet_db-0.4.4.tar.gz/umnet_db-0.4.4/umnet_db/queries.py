from ipaddress import ip_address, ip_network
from typing import List

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from .models import Route, IPInterface, Neighbor, MPLS, VNI
from .errors import UMnetDBLookupError


def neighbor_query(session: Session, device: str, port: str) -> Neighbor:
    """
    Looks up the neighbor object for a particular device in a particular row
    """
    result = session.scalar(
        select(Neighbor).where(Neighbor.device == device).where(Neighbor.port == port)
    )
    if not result:
        raise UMnetDBLookupError(f"{device} {port}", Neighbor)

    return result


def ip_interface_query(session: Session, ip: ip_address) -> IPInterface:
    """
    Finds the router that hosts this IP address (its default gateway)
    by querying the IPInterface table
    """
    result = session.scalar(
        select(IPInterface).where(text(f"'{ip}' = host(ip_address)"))
    )
    if not (result):
        raise UMnetDBLookupError(ip, IPInterface)
    return result


def lpm_query(s: Session, router: str, vrf: str, dest_ip: str) -> List[Route]:
    """
    Get the lpm(s) for an IP address on a particular router in a particular VRF
    """
    query = (
        select(Route)
        .where(text(f"'{dest_ip}' <<= prefix"))
        .where(Route.device == router)
        .where(Route.vrf == vrf)
        .order_by(text("masklen(prefix) desc"))
    )
    routes = s.scalars(query)

    if not routes:
        raise UMnetDBLookupError(f"{router} {vrf} {dest_ip}", Route)

    # Routes are ordered by prefix length - the longest ones
    # are first.
    lpm = None
    lpm_routes = []
    for route in routes:
        # if lpm is none this is the first loop iteration - set this route
        # to be the LPM and continue
        if lpm is None:
            lpm = ip_network(route.prefix).prefixlen
            lpm_routes.append(route)
            continue

        # if this route's prefixlen matches the lpm, save it to
        # our list of lpms
        if ip_network(route.prefix).prefixlen == lpm:
            lpm_routes.append(route)

        # otherwise the route has a shorter lpm and we've found them all
        elif ip_network(route.prefix).prefixlen <= lpm:
            break

    return lpm_routes


def mpls_query(s: Session, router: str, label: str) -> List[MPLS]:
    """
    Looks up a particular label on a particular router.
    Returns the MPLS label entries
    """
    query = select(MPLS).where(MPLS.device == router).where(MPLS.in_label == label)
    results = s.scalars(query)

    if not results:
        raise UMnetDBLookupError(f"{router} {label}", MPLS)

    return results


def l3vni_query(s: Session, router: str, vni: int) -> str:
    """
    Looks up a VNI on the router and returns the
    appropriate VRF
    """
    query = select(VNI.vrf).where(VNI.device == router).where(VNI.vni == vni)
    results = s.scalar(query)

    if not results:
        raise UMnetDBLookupError(f"vrf from {router} {vni}", VNI)

    return results
