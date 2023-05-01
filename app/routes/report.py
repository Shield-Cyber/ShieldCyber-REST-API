from fastapi import APIRouter, Depends, Response
from app.utils.auth import Auth, PASSWORD
from app.utils.xml import XMLResponse
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional, Union
from gvm.protocols.gmpv208.entities.report_formats import ReportFormatType
from app import LOGGING_PREFIX

ENDPOINT = "report"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.get("/get/report")
async def get_report(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
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
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.get_report(report_id=report_id, filter_string=filter_string, filter_id=filter_id, delta_report_id=delta_report_id, report_format_id=report_format_id, ignore_pagination=ignore_pagination, details=details)

@ROUTER.get("/get/reports")
async def get_reports(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
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
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.get_reports(filter_string=filter_string,filter_id=filter_id,note_details=note_details,override_details=override_details,ignore_pagination=ignore_pagination,details=details)

@ROUTER.get("/get/report/format")
async def get_report_format(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    report_format_id: Union[str, ReportFormatType]
):
    """Request a single report format

        Arguments:

            report_format_id: UUID of an existing report format or ReportFormatType (enum)
        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.get_report_format(report_format_id=report_format_id)

@ROUTER.get("/get/report/formats")
async def get_report_formats(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
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
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.get_report_formats(filter_string=filter_string,filter_id=filter_id,trash=trash,alerts=alerts,params=params,details=details)

@ROUTER.post("/clone/report/formats")
async def get_report_formats(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    report_format_id: Union[str, ReportFormatType]
):
    """Clone a report format from an existing one

        Arguments:

            report_format_id: UUID of the existing report format or ReportFormatType (enum)

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.clone_report_format(report_format_id=report_format_id)

@ROUTER.delete("/delete/report")
async def delete_report(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    report_id: str
):
    """Deletes an existing report

        Arguments:

            report_id: UUID of the report to be deleted.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.delete_report(report_id=report_id)

@ROUTER.delete("/delete/report/format")
async def delete_report(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    report_format_id: Union[str, ReportFormatType]
):
    """Clone a report format from an existing one

        Arguments:

            report_format_id: UUID of the existing report format or ReportFormatType (enum)

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.delete_report_format(report_format_id=report_format_id)

@ROUTER.post("/import/report")
async def import_report(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    report: str,
    task_id: str,
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
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.import_report(report=report,task_id=task_id,in_assets=in_assets)

@ROUTER.post("/import/report/format")
async def import_report_format(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    report_format: str
):
    """Import a report format from XML

        Arguments:

            report_format: Report format XML as string to import. This XML must contain a :code:`<get_report_formats_response>` root element.

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.import_report_format(report_format=report_format)

@ROUTER.patch("/modify/report/format")
async def modify_report_format(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    report_format_id: Union[str, ReportFormatType],
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
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.modify_report_format(report_format_id=report_format_id,active=active,name=name,summary=summary,param_name=param_name,param_value=param_value)

@ROUTER.get("/verify/report/format")
async def verify_report_format(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
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
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.verify_report_format(report_format_id=report_format_id)

@ROUTER.get("/get/system/reports")
async def get_system_reports(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
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
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.get_system_reports(name=name,duration=duration,start_time=start_time,end_time=end_time,brief=brief,slave_id=slave_id)
