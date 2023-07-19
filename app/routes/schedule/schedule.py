from fastapi import APIRouter, Depends, Response
from app.utils.auth import Auth
from app.utils.xml import XMLResponse
from app.utils.error import ErrorResponse
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional
from app import LOGGING_PREFIX

from . import models as Models

ENDPOINT = "schedule"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.post("/create")
async def create_schedule(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    Base: Models.CreateSchedule
    ):
    """Create a new schedule based in `iCalendar`_ data.

        Example:
            Requires https://pypi.org/project/icalendar/

            .. code-block:: python

                import pytz

                from datetime import datetime

                from icalendar import Calendar, Event

                cal = Calendar()

                cal.add('prodid', '-//Foo Bar//')
                cal.add('version', '2.0')

                event = Event()
                event.add('dtstamp', datetime.now(tz=pytz.UTC))
                event.add('dtstart', datetime(2020, 1, 1, tzinfo=pytz.utc))

                cal.add_component(event)

                gmp.create_schedule(
                    name="My Schedule",
                    icalendar=cal.to_ical(),
                    timezone='UTC'
                )

        Arguments:

            name: Name of the new schedule
            icalendar: `iCalendar`_ (RFC 5545) based data.
            timezone: Timezone to use for the icalender events e.g Europe/Berlin. If the datetime values in the icalendar data are missing timezone information this timezone gets applied. Otherwise the datetime values from the icalendar data are displayed in this timezone
            comment: Comment on schedule.

        Returns:
            The response.

        .. _iCalendar:
            https://tools.ietf.org/html/rfc5545
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.create_schedule(name=Base.name,icalendar=Base.icalendar,timezone=Base.timezone,comment=Base.comment)
        except Exception as err:
            return ErrorResponse(err)
        
@ROUTER.patch("/modify/{schedule_id}")
async def modify_schedule(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    schedule_id: str,
    Base: Models.ModifySchedule
    ):
    """Modifies an existing schedule

        Arguments:

            schedule_id: UUID of the schedule to be modified
            name: Name of the schedule
            icalendar: `iCalendar`_ (RFC 5545) based data.
            timezone: Timezone to use for the icalender events e.g Europe/Berlin. If the datetime values in the icalendar data are missing timezone information this timezone gets applied. Otherwise the datetime values from the icalendar data are displayed in this timezone
            comment: Comment on schedule.

        Returns:
            The response.

        .. _iCalendar:
            https://tools.ietf.org/html/rfc5545
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.modify_schedule(schedule_id=schedule_id,name=Base.name,icalendar=Base.icalendar,timezone=Base.timezone,comment=Base.comment)
        except Exception as err:
            return ErrorResponse(err)
        
@ROUTER.post("/clone/{schedule_id}")
async def clone_schedule(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    schedule_id: str
    ):
    """Clone an existing schedule

        Arguments:

            schedule_id: UUID of an existing schedule to clone from

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.clone_schedule(schedule_id=schedule_id)
        except Exception as err:
            return ErrorResponse(err)
        
@ROUTER.delete("/delete/{schedule_id}")
async def delete_schedule(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    schedule_id: str,
    ultimate: Optional[bool] = False
    ):
    """Deletes an existing schedule

        Arguments:
            schedule_id: UUID of the schedule to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.delete_schedule(schedule_id=schedule_id,ultimate=ultimate)
        except Exception as err:
            return ErrorResponse(err)

@ROUTER.get("/get/{schedule_id}")
async def get_schedule(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    schedule_id: str,
    tasks: Optional[bool] = None
    ):
    """Request a single schedule

        Arguments:

            schedule_id: UUID of an existing schedule
            tasks: Whether to include tasks using the schedules

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_schedule(schedule_id=schedule_id,tasks=tasks)
        except Exception as err:
            return ErrorResponse(err)
        
@ROUTER.get("/get/schedules")
async def get_schedules(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    trash: Optional[bool] = None,
    tasks: Optional[bool] = None,
    ):
    """Request a list of schedules

        Arguments:

            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan schedules instead
            tasks: Whether to include tasks using the schedules

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_schedules(filter_string=filter_string,filter_id=filter_id,trash=trash,tasks=tasks)
        except Exception as err:
            return ErrorResponse(err)