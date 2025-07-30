#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
from liquiclient.config import get_property
from redis.cluster import RedisCluster
from urllib.parse import urlencode


# 获取redis实例
def get_redis_client():
    mode = get_property("redis.mode")
    host = get_property("redis.host")
    port = get_property("redis.port")
    username = get_property("redis.username")
    password = get_property("redis.password")

    if mode != "cluster":
        # 构建连接参数，只包含非空的认证信息
        connection_params = {
            'host': host,
            'port': port,
            'decode_responses': True
        }

        # 只有当username和password都不为空时才添加认证参数
        if username and password:
            connection_params['username'] = username
            connection_params['password'] = password
        elif password:  # 只有密码没有用户名的情况
            connection_params['password'] = password

        client = redis.Redis(**connection_params)
    else:
        # 集群模式处理 - 修正URL构建，包含端口号
        if username and password:
            url = "redis://{}:{}@{}:{}".format(urlencode(username), urlencode(password), host, port)
        elif password:
            url = "redis://:{}@{}:{}".format(urlencode(password), host, port)
        else:
            url = "redis://{}:{}".format(host, port)
        client = RedisCluster.from_url(url, decode_responses=True)

    return client


# 获取redis实例
def get_redis_cluster_client(key):
    mode = get_property("redis.mode")
    host = get_property(key + ".redis.host")
    port = get_property(key + ".redis.port")
    username = get_property(key + ".redis.username")
    password = get_property(key + ".redis.password")

    if mode != "cluster":
        # 构建连接参数，只包含非空的认证信息
        connection_params = {
            'host': host,
            'port': port,
            'decode_responses': True
        }

        # 只有当username和password都不为空时才添加认证参数
        if username and password:
            connection_params['username'] = username
            connection_params['password'] = password
        elif password:  # 只有密码没有用户名的情况
            connection_params['password'] = password

        client = redis.Redis(**connection_params)
    else:
        # 集群模式处理 - 修正URL构建，包含端口号
        if username and password:
            url = "redis://{}:{}@{}:{}".format(urlencode(username), urlencode(password), host, port)
        elif password:
            url = "redis://:{}@{}:{}".format(urlencode(password), host, port)
        else:
            url = "redis://{}:{}".format(host, port)
        client = RedisCluster.from_url(url, decode_responses=True)

    return client