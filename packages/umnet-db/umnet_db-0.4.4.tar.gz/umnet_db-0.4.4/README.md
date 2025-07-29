# umnet-db
A postgres database for storing normalized network data. umnet-db uses [sqlalachemy](https://www.sqlalchemy.org/) to define its models, and it uses [postgresql-audit](https://github.com/kvesteri/postgresql-audit)
to track changes.

## Tables
This is a current (as of April 2024) list of the tables in the database and the IOS/NXOS commands that they (roughly) map to. For specific details on what's in each table check out `umnet_db.models`
| Table Name | Router show command |
| ----------- | -------------- |
| device | show version |
| neighbor | show lldp neighbor |
| lag | show etherchannel summ |
| arp | show ip arp |
| ip_interface | show ip interface |
| route | show ip route |
| vni | show vni information |
| mpls | show mpls switching |
| inventory | show inventory |

## Querying
The package installs two cli scripts you can use to query the database: `umnetdb-lookup` to query any of the tables listed above, and `umnetdb-diff` to query the `activity` (audit) table for changes.
Note that the cli query functionality is still pretty crude. Feel free to request new features by creating an issue!

### umnetdb-lookup
`umnetdb-lookup` allows you to query any table and filter by columns. Use the `--help` flag to get a list of columns for each table.
You can use '%' to do a 'LIKE' query as well. Here's an example that pulls version information for both arbl DLs:
```
amylieb@wintermute:~$ umnetdb-lookup device --name dl-arbl-%
name        ip            version   vendor   model              serial        uptime               first_seen                   last_updated
dl-arbl-1   172.23.14.2   9.3(9)    Cisco    N9K-C93360YC-FX2   FDO261320CY   982 days, 23:14:45   2025-04-23 12:46:06.525076   2025-04-24 15:30:42.971169
dl-arbl-2   172.23.14.3   9.3(9)    Cisco    N9K-C93360YC-FX2   FDO26141XDN   982 days, 22:44:23   2025-04-23 14:03:50.738133   2025-04-24 15:30:43.243889
```
For IP-based columns you can match on 'le' (contains), 'ge' (contained by), or 'eq' exact match. By default 'ge' is assumed. Here is
a L3info-style search for `141.213.135.0/24`, followed by an ARP entries search on dl-arbl-1 for that same network. The second query restricts the output columns
so we only see the IP and MACs.
```
amylieb@wintermute:~$ umnetdb-lookup ip_interface --ip_address 141.213.135.0/24
device      ip_address         interface   description        mtu    admin_up   oper_up   vrf                  secondary   helpers                                  first_seen                   last_updated
dl-arbl-1   141.213.135.2/24   Vlan301     NGFW-ITS-COMM-AL   9000   True       True      VRF-ITS-STAFF-NGFW   False       ['141.211.147.234', '141.211.147.198']   2025-04-23 12:46:06.722875   2025-04-24 14:28:14.047813
dl-arbl-2   141.213.135.3/24   Vlan301     NGFW-ITS-COMM-AL   9000   True       True      VRF-ITS-STAFF-NGFW   False       ['141.211.147.234', '141.211.147.198']   2025-04-23 14:03:50.887761   2025-04-24 14:28:14.259398
amylieb@wintermute:~$
amylieb@wintermute:~$ umnetdb-lookup arp --ip 141.213.135.0/24 --device dl-arbl-1 --columns ip mac
ip                mac
141.213.135.1     00-00-5E-00-01-01
141.213.135.3     5C-31-92-17-0F-5B
141.213.135.6     9C-7B-EF-BE-DC-B2
141.213.135.9     E8-CF-83-1D-58-8D
141.213.135.12    40-B0-34-FA-39-68
141.213.135.19    D0-46-0C-B2-A6-CC
141.213.135.21    B4-B5-2F-DA-2A-28
141.213.135.25    3C-52-82-6D-D0-D3
141.213.135.27    AC-91-A1-C1-BE-D1
141.213.135.29    00-E0-DB-75-0E-A0
141.213.135.41    C8-D9-D2-18-18-8A
```
You can also sort the output by column. Here's a list of devices sorted by uptime:
```
amylieb@wintermute:~$ umnetdb-lookup device --columns name ip serial uptime --sort-by uptime --descending
name                            ip                serial         uptime
nsbs-core                       141.215.2.117     JAE1827027A    3378 days, 4:46:00
d-fxbdn-1                       198.108.10.44     BP0213300477   3130 days, 5:04:39
fcn-core                        141.215.2.81      JAE17430BY0    2858 days, 23:09:00
s-arbl3-9100-b3-1               10.233.0.16       BP0211222320   2843 days, 10:21:29
s-equad-trb416-bd-2             10.233.77.35      CU0213054709   2836 days, 9:42:21
s-equad-trb416-bd-4             10.233.77.37      CU0213024313   2836 days, 9:22:50
s-ncrc080-125-1                 10.233.4.5        CT0210519657   2836 days, 9:03:34
s-ggbl-1633-2                   10.233.237.12     BP0213500882   2823 days, 9:02:03
s-ggbl-1633-1                   10.233.237.11     FP0213436703   2823 days, 9:01:00
s-stad-1m2285a-ma-2             10.233.93.21      CV0215150587   2764 days, 9:42:24
fcn-vg-sw2-b4                   10.215.5.44       FOC2022W3TE    2583 days, 3:22:00
fcn-vg-sw1                      10.215.5.34       FCW1810A3H2    2583 days, 0:48:00
```
