from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
import time
from fastapi import FastAPI, Response
import logging
from contextlib import asynccontextmanager
from typing import Optional, Union
from gvm.protocols.gmpv208.entities.report_formats import ReportFormatType


# path to unix socket
path = '/run/gvmd/gvmd.sock'

# using the with statement to automatically connect and disconnect to gvmd
# while True:
#     try:
#         connection = UnixSocketConnection(path=path)
#         with Gmp(connection=connection) as gmp:
#             # get the response message returned as a utf-8 encoded string
#             response = gmp.get_version()

#             # print the response message
#             print(response)

#             print(gmp.authenticate("admin", "admin"))
#     except:
#         print("waiting 1 second for open socket")
#         time.sleep(1)

### ### ### ### ### ### ### ### ### ###

app = FastAPI()

logger = logging.getLogger("uvicorn")

connection = None

username = "admin"
password = "test123"

@app.on_event("startup")
async def startup():
    while True:
        try:
            global connection
            connection = UnixSocketConnection(path=path)
            with Gmp(connection=connection) as gmp:
                logger.info(gmp.get_version())
                break
        except:
            logger.warning("waiting 1 second for open socket")
            time.sleep(1)

@app.post("/authenticate")
async def authenticate(username: str, password: str):
    # connection = UnixSocketConnection(path=path)
    with Gmp(connection=connection) as gmp:
        return gmp.authenticate(username=username, password=password)

@app.get("/tasks")
async def get_tasks(
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    trash: Optional[bool] = None,
    details: Optional[bool] = None,
    schedules_only: Optional[bool] = None
):
    # connection = UnixSocketConnection(path=path)
    with Gmp(connection=connection) as gmp:
        # return gmp.get_tasks()
        gmp.authenticate(username=username, password=password)
        return Response(content=gmp.get_tasks(filter_string=filter_string, filter_id=filter_id, trash=trash, details=details, schedules_only=schedules_only), media_type="application/xml")
    
@app.get("/task")
async def get_task(id: str):
    # connection = UnixSocketConnection(path=path)
    with Gmp(connection=connection) as gmp:
        gmp.authenticate(username=username, password=password)
        return Response(content=gmp.get_task(id), media_type="application/xml")
    
@app.get("/report")
async def get_report(
    report_id: str,
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    delta_report_id: Optional[str] = None,
    report_format_id: Optional[Union[str, ReportFormatType]] = None,
    ignore_pagination: Optional[bool] = None,
    details: Optional[bool] = True
):
    with Gmp(connection=connection) as gmp:
        gmp.authenticate(username=username, password=password)
        return Response(content=gmp.get_report(report_id=report_id, filter_string=filter_string, filter_id=filter_id, delta_report_id=delta_report_id, report_format_id=report_format_id, ignore_pagination=ignore_pagination, details=details), media_type="application/xml")