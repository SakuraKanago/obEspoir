# coding=utf-8
"""
author = jamon
"""


class NodeType(object):
    PROXY = 0        # 代理节点
    ROUTE = 1        # 路由节点
    SERVICE = 2      # 服务节点

    @classmethod
    def to_dict(cls):
        return [cls.PROXY, cls.ROUTE, cls.SERVICE]

    @classmethod
    def get_type(cls, node_type_str):
        return {"proxy": cls.PROXY, "route": cls.ROUTE, "service": cls.SERVICE}.get(node_type_str)

    @classmethod
    def get_name(cls, node_type):
        return {cls.PROXY: "proxy", cls.ROUTE: "route", cls.SERVICE: "service"}.get(node_type)


class ConnectionStatus(object):
    ESTABLISHED = 1    # 连接已建立
    LOSE = 2           # 连接断开
