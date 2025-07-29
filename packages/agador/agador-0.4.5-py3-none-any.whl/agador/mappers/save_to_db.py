# pylint: disable=too-few-public-methods, not-callable
from typing import Dict, Any
from datetime import datetime, timedelta
import logging

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import select, Column
from sqlalchemy.sql import sqltypes

from nornir.core.task import Result

from umnet_db.models import (
    Base,
    Device,
    Neighbor,
    ARP,
    IPInterface,
    Route,
    Lag,
    MPLS,
    VNI,
    Inventory,
)

from umnet_napalm.utils import abbr_interface

logger = logging.getLogger(__name__)

# Maping table columns to custom conversion
CUSTOM_COLUMN_CASTS = {
    # age and uptime from umnet_napalm come in as integers
    "age": lambda x: timedelta(seconds=x),
    "uptime": lambda x: timedelta(seconds=x),
}


class NapalmToDBError(Exception):
    pass


class ResultsToDb:
    """
    Generic class that maps nornir results to a particular table
    in the database
    """

    # db table to map to
    db: Base

    # name of column that holds the device name. For the Device table
    # this is 'name', for everything else it's device
    _device_col: str = "device"

    # when we update the table are we merging the device data or overwriting?
    # we almost always want to overwrite.
    _overwrite = True

    def __init__(self, hostname: str, host_ip: str, results: Result, engine: Engine):
        self._hostname = hostname
        self._host_ip = host_ip
        self._results = results
        self._e = engine
        self._timestamp = datetime.now()

        self.update()

    @property
    def pks(self) -> tuple:
        """
        List of column names that are primary keys for this table, it
        """
        return tuple(c.name for c in self.db.__table__.primary_key.columns)

    def _pk(self, row: Base) -> tuple:
        """
        extracts primary key data from a row object
        """
        return tuple(getattr(row, pk) for pk in self.pks)

    def update(self) -> bool:
        """
        Open a session with the database. Creates new row objects
        then either replace existing device's rows in
        the table with new ones or merge them in.

        Returs a bool that tells us if we modified the db or not
        Right now we're assuming any failure will result in an exception -
        if we get to the "commit" at the end that is a success.
        """

        with Session(self._e) as session:
            # pulling current and new rows
            logger.debug(
                "Getting current entries for %s %s",
                self._hostname,
                self.db.__tablename__,
            )
            curr_rows = self._get_current_rows(session)
            # logger.debug([r for r in curr_rows.values()])
            logger.debug("Retrieved %s current entries", len(curr_rows))

            logger.debug("Generating rows from given data")
            new_rows = self._create_rows()
            # logger.debug([r for r in new_rows.values()])
            logger.debug("Generated %s rows", len(new_rows))

            # now we must compare the keys of the new rows to the current ones
            for pk, new_data in new_rows.items():
                # adding rows that don't exist
                if pk not in curr_rows:
                    logger.debug(f"Adding new pk {pk}")
                    session.add(new_data)

                # for existing rows, copy over all columns except for 'first seen'
                else:
                    logger.debug(f"updating existing row {curr_rows[pk]}")
                    for k, v in new_data.as_dict().items():
                        if k != "first_seen":
                            setattr(curr_rows[pk], k, v)

            # if we are overwriting, we want to blow away any existing row
            # not in the current data
            if self._overwrite:
                for pk, curr_data in curr_rows.items():
                    if pk not in new_rows:
                        logger.debug(f"Deleting {pk} {curr_data}")
                        session.delete(curr_data)

            logger.debug("Committing data")
            session.commit()

            # the boolean returned indicates that we modified the database
            return True

    def _create_rows(self) -> Dict[tuple, Base]:
        """
        Generic "create rows" that works when there's a 1:1 mapping between
        the getter results and the DB.
        """
        rows = {}
        for result in self._results:
            row = self.db()
            self._result_to_row(row, result)
            rows[self._pk(row)] = row

        return rows

    def _result_to_row(self, row: Base, result: dict, mapping: dict = None):
        """
        generic "save items from this napalm results dictionary into the row's column
        attributes. If the results dictionary's keys don't map directly to
        the table attributes, provide a mapping so we know what maps to what.
        """
        if mapping:
            for k, v in mapping.items():
                col = getattr(self.db.__table__.columns, k)
                setattr(row, k, self._cast_col(col, result[v]))
        else:
            for k, v in result.items():
                col = getattr(self.db.__table__.columns, k, None)
                if col is not None:
                    setattr(row, k, self._cast_col(col, v))

        # adding first seen and last updated fields
        row.first_seen = self._timestamp
        row.last_updated = self._timestamp

        # also - set the 'device' attribute in the row if it's not already set
        # we don't get the device name from our napalm results
        if "device" in row.__table__.columns and not row.device:
            row.device = self._hostname

    def _get_current_rows(self, s: Session) -> Dict[tuple, Base]:
        """
        Pulls the current data for a particular device for this table
        """
        rows = s.scalars(
            select(self.db).where(getattr(self.db, self._device_col) == self._hostname)
        )
        if not rows:
            return {}
        return {self._pk(row): row for row in rows}

    def _cast_col(self, col: Column, entry: Any) -> Any:
        """
        Attempts to cast entries from napalm to the right python type.
        """
        # empty strings for non-string, nullable columns should get converted to None type
        if not (isinstance(col.type, sqltypes.String)) and not entry and col.nullable:
            return None

        # converting to python type if it's not that way already
        if entry and not (isinstance(entry, col.type.python_type)):
            # special handling of certain columns
            for cast_col_name, cast_function in CUSTOM_COLUMN_CASTS.items():
                if col.name == cast_col_name:
                    return cast_function(entry)

            # sqlalchemy types have an attribute 'python type'
            # that we can use for casting
            return col.type.python_type(entry)

        return entry


class UpdateDevice(ResultsToDb):
    """
    Takes "get facts" and maps it to the Device table
    """

    db = Device
    _device_col = "name"
    _overwrite = False

    def _create_rows(self) -> Dict[tuple, Device]:
        """
        Maps napalm "get facts" and a the hostname/ip from nornir
        to a row in the device table
        """
        device = self.db()

        device.name = self._hostname
        device.ip = self._host_ip

        get_facts_mapping = {
            "version": "os_version",
            "vendor": "vendor",
            "model": "model",
            "serial": "serial_number",
            "uptime": "uptime",
            "hostname": "hostname",
        }

        self._result_to_row(device, self._results, get_facts_mapping)
        return {self._pk(device): device}


class UpdateNeighbor(ResultsToDb):
    """
    Takes "show lldp neighbors" and maps it to the Device table
    """

    db = Neighbor

    def _create_rows(self) -> Dict[tuple, Neighbor]:
        rows = {}
        for port, neighs in self._results.items():
            for neigh in neighs:
                new_neigh = self.db(
                    device=self._hostname,
                    port=self._cleanup_interface(port),
                    remote_device=self._cleanup_hostname(neigh["hostname"]),
                    remote_port=self._cleanup_interface(neigh["port"]),
                    first_seen=self._timestamp,
                    last_updated=self._timestamp,
                )

                rows[self._pk(new_neigh)] = new_neigh

        return rows

    def _cleanup_hostname(self, hostname: str) -> str:
        return hostname.split(".")[0]

    def _cleanup_interface(self, interface: str) -> str:
        """
        Abbreviates cisco interfaces and converts logical to physical for junos
        """
        # want physical interface not logical
        if "." in interface:
            interface = interface.split(".")[0]

        return abbr_interface(interface)


class UpdateLAG(ResultsToDb):
    """
    Takes "get_lag_interfaces" and maps it to the LAG table.
    Note that the 'member' column of the LAG table is required, and
    as a result we're not going to save data on LAGs with no configured
    members.
    """

    db = Lag

    def _create_rows(self) -> Dict[tuple, Lag]:
        rows = {}
        for lag_name, lag_data in self._results.items():
            for member_name, member_data in lag_data.get("members", {}).items():
                new_member = self.db(
                    device=self._hostname,
                    member=member_name,
                    parent=lag_name,
                    protocol=lag_data["protocol"],
                    admin_up=member_data["admin_up"],
                    oper_up=member_data["oper_up"],
                    vpc_id=lag_data["mlag_id"],
                    peer_link=lag_data["peer_link"],
                    first_seen=self._timestamp,
                    last_updated=self._timestamp,
                )
                rows[self._pk(new_member)] = new_member

        return rows


class UpdateARP(ResultsToDb):
    """
    Takes "get_arp_table" and maps it to the ARP table. Note that we want to
    retain entries not currently seen
    """

    db = ARP
    _overwrite = False


class UpdateIPInterface(ResultsToDb):
    """
    Takes "get_ip_interfaces" and maps it to the IPInterface table
    """

    db = IPInterface


class UpdateRoute(ResultsToDb):
    """
    Takes "get_active_routes" and maps it to the Routes table
    """

    db = Route


class UpdateMPLS(ResultsToDb):
    """
    Takes "get_mpls_switching" and maps it to the MPLS table.
    Note that we actually need to query the DB for the
    device's routes in the default table to resolve
    next hops first!
    """

    db = MPLS


class UpdateVNI(ResultsToDb):
    """
    Takes "get_vni_information" and maps it to the VNI table
    """

    db = VNI


class UpdateInventory(ResultsToDb):
    """
    Takes "get_inventory" and maps it to the inventory table
    """

    db = Inventory
