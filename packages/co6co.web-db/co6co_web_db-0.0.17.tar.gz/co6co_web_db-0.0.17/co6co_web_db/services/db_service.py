from sqlalchemy.ext.asyncio import create_async_engine

from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

# from model.pos.DbModelPo import User, Process
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sanic.response import json

from sanic import Sanic, Blueprint
from sanic.blueprint_group import BlueprintGroup
import asyncio
import time
import typing
from sanic.log import logger
from sanic import Blueprint, Request
from typing import TypeVar
from co6co_db_ext.db_session import db_service
import multiprocessing


def injectDbSessionFactory(app: Sanic, settings: dict = {}, engineUrl: str = None, sessionApi: list = ["/api"]):
    """
    挂在 DBSession_factory
    """
    service: db_service = None

    # sanic_session 包使用了 cockie 未能满足使用需求 已修改其他方式的 session 实现
    # session_interface = InMemorySessionInterface(session_name="mem_session", cookie_name=app.name, prefix=app.name)
    # Session(app, interface=session_interface)
    if settings != None or engineUrl != None:
        service = db_service(settings, engineUrl)
        app.ctx.service = service
        service.sync_init_tables()

    @app.main_process_start
    async def inject_session_factory(app: Sanic):

        app.shared_ctx.cache = multiprocessing.Manager().dict()
        # app.shared_ctx.cache["db_session_factory"]=_async_session_factory

    def checkApi(request: Request):
        for api in sessionApi:
            if api in request.path:
                return True
        return False

    @app.middleware("request")
    async def inject_session(request: Request):
        # await session_interface.open(request)
        if checkApi(request):
            # logger.info("mount DbSession 。。。")
            if service != None and service.useAsync:
                request.app.ctx.session_fatcory = service.async_session_factory
                request.ctx.session = service.async_session_factory()
                request.ctx.session_ctx_token = service.base_model_session_ctx.set(request.ctx.session)
            elif service != None:
                request.ctx.session = service.session

    @app.middleware("response")
    async def close_session(request: Request, response):
        # await session_interface.save(request, response)
        if hasattr(request.ctx, "session_ctx_token"):
            try:
                if service != None and service.useAsync:
                    service.base_model_session_ctx.reset(request.ctx.session_ctx_token)
                    await request.ctx.session.close()
                # logger.info("close DbSession。")
                # await request.ctx.session.dispose()
            except Exception as e:
                logger.err(e)
                # logger.error("close DbSession。Error")
