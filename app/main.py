from .auth import *
from fastapi import FastAPI, Depends, HTTPException, status, Response
from typing import Annotated, Optional, Union, List
from gvm.protocols.gmpv208.entities.report_formats import ReportFormatType
from gvm.protocols.gmpv208.entities.hosts import HostsOrdering
from gvm.connections import UnixSocketConnection
from contextlib import asynccontextmanager
from gvm.protocols.gmp import Gmp
from .xml import root
import logging
import time
import os

# Logging
LOGGER = logging.getLogger("api")

# Socket Path
SOCKET = '/run/gvmd/gvmd.sock'

# Socket Connection
CONNECTION = None

# Description
DESCRIPTION = """This is a translation API that calls the XML API calls on the local
Greenbone Vulnerability Scanner and converts them to REST API calls for easier use by most systems."""

@asynccontextmanager
async def lifespan(app: FastAPI):
    LOGGER.info(f"System Starting...")
    counter = 0
    while True:
        if counter >= 60:
            LOGGER.critical("Connection to gvmd socket took too long. Forcing system exit.")
            raise SystemExit(1)
        try:
            global CONNECTION
            CONNECTION = UnixSocketConnection(path=SOCKET)
            with Gmp(connection=CONNECTION) as gmp:
                version = root(gmp.get_version())
                if version.status != 200:
                    LOGGER.critical(f"Version check recieved non-200 response. Response: {version.data}")
                    raise SystemExit(2)
                LOGGER.info(f"{version.status}, {version.status_text}. Startup complete and took {counter} second(s).")
                break
        except SystemExit:
            raise SystemExit(2)
        except:
            LOGGER.warning("Wating 1 second for gvmd socket.")
            time.sleep(1)
            counter += 1
    yield
    LOGGER.info("System shutting down...")

# Main App / API
app = FastAPI(
    title="Greenbone Rest API",
    description=DESCRIPTION,
    version=os.getenv("VERSION"),
    swagger_ui_parameters={"tagsSorter": "alpha", "operationsSorter": "alpha"},
    lifespan=lifespan
)

### AUTH DATA ###

@app.post("/authenticate", response_model=Token, tags=["auth"])
async def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        LOGGER.warning(f"user '{form_data.username}' has failed authentication")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires
    )
    LOGGER.info(f"user '{form_data.username}' has passed authentication")
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/describe_auth", tags=["auth"])
async def describe_auth(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Describe authentication methods

        Returns a list of all used authentication methods if such a list is available.

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.describe_auth(), media_type="application/xml")

@app.get("/is_authenticated", tags=["auth"])
async def is_authenticated(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Checks if the user is authenticated

        If the user is authenticated privileged GMP commands like get_tasks
        may be send to gvmd.

        Returns:
            bool: True if an authenticated connection to gvmd has been
            established.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.is_authenticated()

@app.patch("/modify_auth", tags=["auth"])
async def modify_auth(
    current_user: Annotated[User, Depends(get_current_active_user)],
    group_name: str,
    auth_conf_settings: dict
):
    """Modifies an existing auth.

        Arguments:

            group_name: Name of the group to be modified.
            auth_conf_settings: The new auth config.

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.modify_auth(group_name=group_name, auth_conf_settings=auth_conf_settings), media_type="application/xml")

### VERSION DATA ###

@app.get("/get/version", tags=["version"])
async def get_version(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Get the Greenbone Vulnerability Manager Protocol version used by the remote gvmd.

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_version(), media_type="application/xml")
    
@app.get("/get/protocol/version", tags=["version"])
async def get_protocol_version(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Determine the Greenbone Management Protocol (gmp) version used by python-gvm version.

        Returns:
            tuple: Implemented version of the Greenbone Management Protocol
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.get_protocol_version()

### TASK DATA ###

@app.get("/get/tasks", tags=["task"])
async def get_tasks(
    current_user: Annotated[User, Depends(get_current_active_user)],
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
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_tasks(filter_string=filter_string, filter_id=filter_id, trash=trash, details=details, schedules_only=schedules_only), media_type="application/xml")

@app.get("/get/task", tags=["task"])
async def get_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: str
    ):
    """Request a single task

        Arguments:

            task_id: UUID of an existing task

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_task(task_id), media_type="application/xml")

@app.delete("/delete/task", tags=["task"])
async def delete_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: str,
    ultimate: Optional[bool] = False
    ):
    """Deletes an existing task

        Arguments:

            task_id: UUID of the task to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.delete_task(task_id=task_id, ultimate=ultimate), media_type="application/xml")

@app.post("/create/task", tags=["task"])
async def create_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
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
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.create_task(name=name,config_id=config_id,target_id=target_id,scanner_id=scanner_id,alterable=alterable,hosts_ordering=hosts_ordering,schedule_id=schedule_id,alert_ids=alert_ids,comment=comment,schedule_periods=schedule_periods,observers=observers,preferences=preferences), media_type="application/xml")

@app.patch("/modify/task", tags=["task"])
async def modify_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
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
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.modify_task(task_id=task_id,name=name,config_id=config_id,target_id=target_id,scanner_id=scanner_id,alterable=alterable,hosts_ordering=hosts_ordering,schedule_id=schedule_id,schedule_periods=schedule_periods,comment=comment,alert_ids=alert_ids,observers=observers,preferences=preferences), media_type="application/xml")

@app.post("/stop/task", tags=["task"])
async def stop_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: str
    ):
    """Stop an existing running task

        Arguments:

            task_id: UUID of the task to be stopped

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.stop_task(task_id=task_id), media_type="application/xml")

@app.post("/start/task", tags=["task"])
async def start_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: str
    ):
    """Start an existing task

        Arguments:

            task_id: UUID of the task to be started

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.start_task(task_id=task_id), media_type="application/xml")

@app.post("/clone/task", tags=["task"])
async def clone_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: str
    ):
    """Clone an existing task

        Arguments:

            task_id: UUID of existing task to clone from

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.clone_task(task_id=task_id), media_type="application/xml")

@app.patch("/move/task", tags=["task"])
async def move_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
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
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.move_task(task_id=task_id, slave_id=slave_id), media_type="application/xml")

@app.post("/resume/task", tags=["task"])
async def resume_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: str,
    ):
    """Resume an existing stopped task

        Arguments:

            task_id: UUID of the task to be resumed

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.resume_task(task_id=task_id), media_type="application/xml")

### REPORT DATA ###

@app.get("/get/report", tags=["report"])
async def get_report(
    current_user: Annotated[User, Depends(get_current_active_user)],
    report_id: str,
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    delta_report_id: Optional[str] = None,
    report_format_id: Optional[Union[str, ReportFormatType]] = None,
    ignore_pagination: Optional[bool] = None,
    details: Optional[bool] = True
):
    """Request a single report

        Arguments:

            report_id: UUID of an existing report
            filter_string: Filter term to use to filter results in the report
            filter_id: UUID of filter to use to filter results in the report
            delta_report_id: UUID of an existing report to compare report to.
            report_format_id: UUID of report format to use or ReportFormatType (enum)
            ignore_pagination: Whether to ignore the filter terms "first" and "rows".
            details: Request additional report information details defaults to True

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_report(report_id=report_id, filter_string=filter_string, filter_id=filter_id, delta_report_id=delta_report_id, report_format_id=report_format_id, ignore_pagination=ignore_pagination, details=details), media_type="application/xml")    

@app.get("/get/reports", tags=["report"])
async def get_reports(
    current_user: Annotated[User, Depends(get_current_active_user)],
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    note_details: Optional[bool] = None,
    override_details: Optional[bool] = None,
    ignore_pagination: Optional[bool] = None,
    details: Optional[bool] = None,
):
    """Request a list of reports

        Arguments:

            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            note_details: If notes are included, whether to include note details
            override_details: If overrides are included, whether to include override details
            ignore_pagination: Whether to ignore the filter terms "first" and "rows".
            details: Whether to exclude results

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_reports(filter_string=filter_string,filter_id=filter_id,note_details=note_details,override_details=override_details,ignore_pagination=ignore_pagination,details=details), media_type="application/xml")

@app.get("/get/report/format", tags=["report"])
async def get_report_format(
    current_user: Annotated[User, Depends(get_current_active_user)],
    report_format_id: Union[str, ReportFormatType]
):
    """Request a single report format

        Arguments:

            report_format_id: UUID of an existing report format or ReportFormatType (enum)
        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_report_format(report_format_id=report_format_id), media_type="application/xml")

@app.get("/get/report/formats", tags=["report"])
async def get_report_formats(
    current_user: Annotated[User, Depends(get_current_active_user)],
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    trash: Optional[bool] = None,
    alerts: Optional[bool] = None,
    params: Optional[bool] = None,
    details: Optional[bool] = None,
):
    """Request a single report format

        Arguments:

            report_format_id: UUID of an existing report format or ReportFormatType (enum)
        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_report_formats(filter_string=filter_string,filter_id=filter_id,trash=trash,alerts=alerts,params=params,details=details), media_type="application/xml")

@app.post("/clone/report/formats", tags=["report"])
async def get_report_formats(
    current_user: Annotated[User, Depends(get_current_active_user)],
    report_format_id: Union[str, ReportFormatType]
):
    """Clone a report format from an existing one

        Arguments:

            report_format_id: UUID of the existing report format or ReportFormatType (enum)

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.clone_report_format(report_format_id=report_format_id), media_type="application/xml")

@app.delete("/delete/report", tags=["report"])
async def delete_report(
    current_user: Annotated[User, Depends(get_current_active_user)],
    report_id: str
):
    """Deletes an existing report

        Arguments:

            report_id: UUID of the report to be deleted.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.delete_report(report_id=report_id), media_type="application/xml")

@app.delete("/delete/report/format", tags=["report"])
async def delete_report(
    current_user: Annotated[User, Depends(get_current_active_user)],
    report_format_id: Union[str, ReportFormatType]
):
    """Clone a report format from an existing one

        Arguments:

            report_format_id: UUID of the existing report format or ReportFormatType (enum)

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.delete_report_format(report_format_id=report_format_id), media_type="application/xml")

@app.post("/import/report", tags=["report"])
async def import_report(
    current_user: Annotated[User, Depends(get_current_active_user)],
    report: str,
    task_id: Optional[str] = None,
    in_assets: Optional[bool] = None,
):
    """Import a Report from XML

        Arguments:

            report: Report XML as string to import. This XML must contain a :code:`<report>` root element.
            task_id: UUID of task to import report to
            in_asset: Whether to create or update assets using the report

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.import_report(report=report,task_id=task_id,in_assets=in_assets), media_type="application/xml")

@app.post("/import/report/format", tags=["report"])
async def import_report_format(
    current_user: Annotated[User, Depends(get_current_active_user)],
    report_format: str
):
    """Import a report format from XML

        Arguments:

            report_format: Report format XML as string to import. This XML must contain a :code:`<get_report_formats_response>` root element.

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.import_report_format(report_format=report_format), media_type="application/xml")

@app.patch("/modify/report/format", tags=["report"])
async def modify_report_format(
    current_user: Annotated[User, Depends(get_current_active_user)],
    report_format_id: Optional[Union[str, ReportFormatType]] = None,
    active: Optional[bool] = None,
    name: Optional[str] = None,
    summary: Optional[str] = None,
    param_name: Optional[str] = None,
    param_value: Optional[str] = None,
):
    """Modifies an existing report format.

        Arguments:

            report_format_id: UUID of report format to modify or ReportFormatType (enum)
            active: Whether the report format is active.
            name: The name of the report format.
            summary: A summary of the report format.
            param_name: The name of the param.
            param_value: The value of the param.

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.modify_report_format(report_format_id=report_format_id,active=active,name=name,summary=summary,param_name=param_name,param_value=param_value), media_type="application/xml")

@app.get("/verify/report/format", tags=["report"])
async def verify_report_format(
    current_user: Annotated[User, Depends(get_current_active_user)],
    report_format_id: Union[str, ReportFormatType]
):
    """Verify an existing report format

        Verifies the trust level of an existing report format. It will be
        checked whether the signature of the report format currently matches the
        report format. This includes the script and files used to generate
        reports of this format. It is *not* verified if the report format works
        as expected by the user.

        Arguments:

            report_format_id: UUID of the report format to be verified or ReportFormatType (enum)

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.verify_report_format(report_format_id=report_format_id), media_type="application/xml")

@app.get("/get/system/reports", tags=["report"])
async def get_system_reports(
    current_user: Annotated[User, Depends(get_current_active_user)],
    name: Optional[str] = None,
    duration: Optional[int] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    brief: Optional[bool] = None,
    slave_id: Optional[str] = None
):
    """Verify an existing report format

        Verifies the trust level of an existing report format. It will be
        checked whether the signature of the report format currently matches the
        report format. This includes the script and files used to generate
        reports of this format. It is *not* verified if the report format works
        as expected by the user.

        Arguments:

            report_format_id: UUID of the report format to be verified or ReportFormatType (enum)

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_system_reports(name=name,duration=duration,start_time=start_time,end_time=end_time,brief=brief,slave_id=slave_id), media_type="application/xml")

### USER DATA ###

@app.get("/get/user", tags=["user"])
async def get_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_id: str
    ):
    """Request a single user

        Arguments:

            user_id: UUID of an existing user

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_user(user_id=user_id), media_type="application/xml")

@app.get("/get/user/settings", tags=["user"])
async def get_user_settings(
    current_user: Annotated[User, Depends(get_current_active_user)],
    filter_string: Optional[str] = None
    ):
    """Request a list of user settings

        Arguments:

            filter_string: Filter term to use for the query

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_user_settings(filter_string=filter_string), media_type="application/xml")

@app.get("/get/user/setting", tags=["user"])
async def get_user_setting(
    current_user: Annotated[User, Depends(get_current_active_user)],
    setting_id: str
    ):
    """Request a list of user settings

        Arguments:

            filter_string: Filter term to use for the query

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_user_setting(setting_id=setting_id), media_type="application/xml")
    
@app.get("/get/users", tags=["user"])
async def get_users(
    current_user: Annotated[User, Depends(get_current_active_user)],
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    ):
    """Request a list of users

        Arguments:

            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query

        Returns:
            The response.
        """
    with Gmp(connection=CONNECTION) as gmp:
        if verify_password(PASSWORD, current_user.hashed_password):
            gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_users(filter_id=filter_id, filter_string=filter_string), media_type="application/xml")
    
