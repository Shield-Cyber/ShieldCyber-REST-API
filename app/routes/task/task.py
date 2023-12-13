from fastapi import APIRouter, Depends
from app.utils.auth import Auth
from app.utils.xml import XMLResponse
from app.utils.error import ErrorResponse
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional, List
from gvm.protocols.gmpv208.entities.hosts import HostsOrdering
from app import LOGGING_PREFIX

from . import models as Models

ENDPOINT = "task"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.get("/get/tasks")
async def get_tasks(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    filter_string: Optional[str] = "rows=-1",
    filter_id: Optional[str] = None,
    trash: Optional[bool] = None,
    details: Optional[bool] = None,
    schedules_only: Optional[bool] = None
):
    """Request a list of tasks

        Arguments:
        
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan tasks instead
            details: Whether to include full task details
            schedules_only: Whether to only include id, name and schedule details

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_tasks(filter_string=filter_string, filter_id=filter_id, trash=trash, details=details, schedules_only=schedules_only)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.get("/get/{task_id}")
async def get_task(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    task_id: str
    ):
    """Request a single task

        Arguments:

            task_id: UUID of an existing task

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_task(task_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.delete("/delete/{task_id}")
async def delete_task(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    task_id: str,
    ultimate: Optional[bool] = False
    ):
    """Deletes an existing task

        Arguments:

            task_id: UUID of the task to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.delete_task(task_id=task_id, ultimate=ultimate)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.post("/create")
async def create_task(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    Base: Models.CreateTask
    ):
    """Create a new scan task

        Arguments:

            name: Name of the new task
            config_id: UUID of config to use by the task
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: Comment for the task
            alterable: Whether the task should be alterable
            alert_ids: List of UUIDs for alerts to be applied to the task
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the task should be run.
            schedule_periods: A limit to the number of times the task will be scheduled, or 0 for no limit
            observers: List of names or ids of users which should be allowed to observe this task
            preferences: Name/Value pairs of scanner preferences.

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.create_task(name=Base.name,config_id=Base.config_id,target_id=Base.target_id,scanner_id=Base.scanner_id,alterable=Base.alterable,hosts_ordering=Base.hosts_ordering,schedule_id=Base.schedule_id,alert_ids=Base.alert_ids,comment=Base.comment,schedule_periods=Base.schedule_periods,observers=Base.observers,preferences=Base.preferences)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.patch("/modify/{task_id}")
async def modify_task(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    Base: Models.ModifyTask
    ):
    """Modifies an existing task.

        Arguments:

            task_id: UUID of task to modify.
            name: The name of the task.
            config_id: UUID of scan config to use by the task
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: The comment on the task.
            alert_ids: List of UUIDs for alerts to be applied to the task
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the task should be run.
            schedule_periods: A limit to the number of times the task will be scheduled, or 0 for no limit.
            observers: List of names or ids of users which should be allowed to observe this task
            preferences: Name/Value pairs of scanner preferences.

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.modify_task(task_id=Base.task_id,name=Base.name,config_id=Base.config_id,target_id=Base.target_id,scanner_id=Base.scanner_id,alterable=Base.alterable,hosts_ordering=Base.hosts_ordering,schedule_id=Base.schedule_id,schedule_periods=Base.schedule_periods,comment=Base.comment,alert_ids=Base.alert_ids,observers=Base.observers,preferences=Base.preferences)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.post("/stop/{task_id}")
async def stop_task(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    task_id: str
    ):
    """Stop an existing running task

        Arguments:

            task_id: UUID of the task to be stopped

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.stop_task(task_id=task_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.post("/start/{task_id}")
async def start_task(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    task_id: str
    ):
    """Start an existing task

        Arguments:

            task_id: UUID of the task to be started

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.start_task(task_id=task_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.post("/clone/{task_id}")
async def clone_task(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    task_id: str
    ):
    """Clone an existing task

        Arguments:

            task_id: UUID of existing task to clone from

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.clone_task(task_id=task_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.patch("/move/{task_id}")
async def move_task(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    Base: Models.MoveTask
    ):
    """Move an existing task to another GMP slave scanner or the master

        Arguments:

            task_id: UUID of the task to be moved
            slave_id: UUID of slave to reassign the task to, empty for master.

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.move_task(task_id=Base.task_id, slave_id=Base.slave_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.post("/resume/{task_id}")
async def resume_task(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    task_id: str,
    ):
    """Resume an existing stopped task

        Arguments:

            task_id: UUID of the task to be resumed

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.resume_task(task_id=task_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")