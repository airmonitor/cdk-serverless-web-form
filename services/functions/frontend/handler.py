# -*- coding: utf-8 -*-
"""fastapi application."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum
from ssm_cache import SSMParameterGroup

from logic.routers import twoforms, unsplash, accordion
from utils.helpers import openfile

SSM_GROUP = SSMParameterGroup(max_age=3600)
# AUTHORIZATION_KEY = SSM_GROUP.parameter(environ["AUTHORIZATION_KEY"])
# AUTHORIZATION_KEY = AUTHORIZATION_KEY.value
#
# CSRF_KEY = SSM_GROUP.parameter(environ["CSRF_KEY"])
# CSRF_KEY = CSRF_KEY.value


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(unsplash.router)
app.include_router(twoforms.router)
app.include_router(accordion.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """

    :param request:
    :return:
    """
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    """

    :param request:
    :param page_name:
    :return:
    """
    data = openfile(f"{page_name}.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


handler = Mangum(app)
