from fastapi import APIRouter, Depends
from app.utils.auth import Auth, PASSWORD
from app.utils.xml import XMLResponse
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional, List
from gvm.protocols.gmpv208.entities.hosts import HostsOrdering
from app import LOGGING_PREFIX

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
    filter_string: Optional[str] = None,
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.get_tasks(filter_string=filter_string, filter_id=filter_id, trash=trash, details=details, schedules_only=schedules_only)

@ROUTER.get("/get/task", tags=["task"])
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.get_task(task_id)

@ROUTER.delete("/delete/task", tags=["task"])
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.delete_task(task_id=task_id, ultimate=ultimate)

@ROUTER.post("/create/task", tags=["task"])
async def create_task(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    name: str,
    config_id: str,
    target_id: str,
    scanner_id: str,
    alterable: Optional[bool] = None,
    hosts_ordering: Optional[HostsOrdering] = None,
    schedule_id: Optional[str] = None,
    alert_ids: Optional[List[str]] = None,
    comment: Optional[str] = None,
    schedule_periods: Optional[int] = None,
    observers: Optional[List[str]] = None,
    preferences: Optional[dict] = None,
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.create_task(name=name,config_id=config_id,target_id=target_id,scanner_id=scanner_id,alterable=alterable,hosts_ordering=hosts_ordering,schedule_id=schedule_id,alert_ids=alert_ids,comment=comment,schedule_periods=schedule_periods,observers=observers,preferences=preferences)

@ROUTER.patch("/modify/task", tags=["task"])
async def modify_task(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    task_id: str,
    name: Optional[str] = None,
    config_id: Optional[str] = None,
    target_id: Optional[str] = None,
    scanner_id: Optional[str] = None,
    alterable: Optional[bool] = None,
    hosts_ordering: Optional[HostsOrdering] = None,
    schedule_id: Optional[str] = None,
    schedule_periods: Optional[int] = None,
    comment: Optional[str] = None,
    alert_ids: Optional[List[str]] = None,
    observers: Optional[List[str]] = None,
    preferences: Optional[dict] = None,
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.modify_task(task_id=task_id,name=name,config_id=config_id,target_id=target_id,scanner_id=scanner_id,alterable=alterable,hosts_ordering=hosts_ordering,schedule_id=schedule_id,schedule_periods=schedule_periods,comment=comment,alert_ids=alert_ids,observers=observers,preferences=preferences)

@ROUTER.post("/stop/task", tags=["task"])
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.stop_task(task_id=task_id)

@ROUTER.post("/start/task", tags=["task"])
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.start_task(task_id=task_id)

@ROUTER.post("/clone/task", tags=["task"])
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.clone_task(task_id=task_id)

@ROUTER.patch("/move/task", tags=["task"])
async def move_task(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    task_id: str,
    slave_id: Optional[str] = None
    ):
    """Move an existing task to another GMP slave scanner or the master

        Arguments:

            task_id: UUID of the task to be moved
            slave_id: UUID of slave to reassign the task to, empty for master.

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.move_task(task_id=task_id, slave_id=slave_id)

@ROUTER.post("/resume/task", tags=["task"])
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.resume_task(task_id=task_id)