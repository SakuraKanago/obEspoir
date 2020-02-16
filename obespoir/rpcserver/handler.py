# coding=utf-8
"""
author = jamon
"""

from obespoir.base.ob_handler import BaseHandler, RegisterEvent
from obespoir.share.ob_log import logger


@RegisterEvent(1000)
class LoginHandler(BaseHandler):

    async def execute(self, *args, **kwargs):
        logger.info("login_1000:{}  {}".format(args, kwargs))
        print("aaaaaaaa:", self.command_id, self.session_id)
        return {"code": 200}


@RegisterEvent(999, need_return=False)
class OfflineHandler(BaseHandler):

    async def execute(self, *args, **kwargs):
        logger.info("offline: {}, {}".format(args, kwargs))
        pass
        return {"code": 200}


@RegisterEvent(10000, need_return=True)
class HeartBeatHandler(BaseHandler):

    async def execute(self, *args, **kwargs):
        logger.info("heartbeat: {}, {}".format(args, kwargs))
        pass
        return {"code": 200}

