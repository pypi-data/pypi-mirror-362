#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
from liquiclient.config import get_property
from redis.cluster import RedisCluster
from redis.sentinel import Sentinel
from urllib.parse import urlencode


# 获取redis实例
def get_redis_client():
    mode = get_property("redis.mode")
    host = get_property("redis.host")
    port = get_property("redis.port")
    username = get_property("redis.username")
    password = get_property("redis.password")

    if mode == "sentinel":
        # 哨兵模式处理
        sentinel_hosts = host  # 格式: "host1:port1,host2:port2,host3:port3"
        service_name = get_property("redis.sentinel")

        # 解析哨兵主机列表
        if isinstance(sentinel_hosts, str):
            sentinel_list = []
            for host_port in sentinel_hosts.split(','):
                host_port = host_port.strip()
                if ':' in host_port:
                    h, p = host_port.split(':', 1)
                    sentinel_list.append((h.strip(), int(p.strip())))
                else:
                    sentinel_list.append((host_port, 26379))  # 默认哨兵端口
        else:
            # 如果没有配置哨兵主机列表，使用默认配置
            sentinel_list = [(host, int(port) if port else 26379)]

        # 创建哨兵实例
        sentinel_kwargs = {}
        if username and password:
            sentinel_kwargs['username'] = username
            sentinel_kwargs['password'] = password
        elif password:
            sentinel_kwargs['password'] = password

        sentinel = Sentinel(sentinel_list, **sentinel_kwargs)

        # 获取主节点连接
        master_kwargs = {}
        if username and password:
            master_kwargs['username'] = username
            master_kwargs['password'] = password
        elif password:
            master_kwargs['password'] = password

        client = sentinel.master_for(service_name, **master_kwargs)

    elif mode == "cluster":
        # 集群模式处理 - 修正URL构建，包含端口号
        if username and password:
            url = "redis://{}:{}@{}:{}".format(urlencode(username), urlencode(password), host, port)
        elif password:
            url = "redis://:{}@{}:{}".format(urlencode(password), host, port)
        else:
            url = "redis://{}:{}".format(host, port)
        client = RedisCluster.from_url(url)
    else:
        # 单机模式处理
        # 构建连接参数，只包含非空的认证信息
        connection_params = {
            'host': host,
            'port': port
        }

        # 只有当username和password都不为空时才添加认证参数
        if username and password:
            connection_params['username'] = username
            connection_params['password'] = password
        elif password:  # 只有密码没有用户名的情况
            connection_params['password'] = password

        client = redis.Redis(**connection_params)

    return client


# 获取redis实例
def get_redis_cluster_client(key):
    mode = get_property("redis.mode")
    host = get_property(key + ".redis.host")
    port = get_property(key + ".redis.port")
    username = get_property(key + ".redis.username")
    password = get_property(key + ".redis.password")

    if mode == "sentinel":
        # 哨兵模式处理
        sentinel_hosts = host  # 格式: "host1:port1,host2:port2,host3:port3"
        service_name = get_property("redis.sentinel")

        # 解析哨兵主机列表
        if isinstance(sentinel_hosts, str):
            sentinel_list = []
            for host_port in sentinel_hosts.split(','):
                host_port = host_port.strip()
                if ':' in host_port:
                    h, p = host_port.split(':', 1)
                    sentinel_list.append((h.strip(), int(p.strip())))
                else:
                    sentinel_list.append((host_port, 26379))  # 默认哨兵端口
        else:
            # 如果没有配置哨兵主机列表，使用默认配置
            sentinel_list = [(host, int(port) if port else 26379)]

        # 创建哨兵实例
        sentinel_kwargs = {}
        if username and password:
            sentinel_kwargs['username'] = username
            sentinel_kwargs['password'] = password
        elif password:
            sentinel_kwargs['password'] = password

        sentinel = Sentinel(sentinel_list, **sentinel_kwargs)

        # 获取主节点连接
        master_kwargs = {}
        if username and password:
            master_kwargs['username'] = username
            master_kwargs['password'] = password
        elif password:
            master_kwargs['password'] = password

        client = sentinel.master_for(service_name, **master_kwargs)

    elif mode == "cluster":
        # 集群模式处理 - 修正URL构建，包含端口号
        if username and password:
            url = "redis://{}:{}@{}:{}".format(urlencode(username), urlencode(password), host, port)
        elif password:
            url = "redis://:{}@{}:{}".format(urlencode(password), host, port)
        else:
            url = "redis://{}:{}".format(host, port)
        client = RedisCluster.from_url(url)
    else:
        # 单机模式处理
        # 构建连接参数，只包含非空的认证信息
        connection_params = {
            'host': host,
            'port': port
        }

        # 只有当username和password都不为空时才添加认证参数
        if username and password:
            connection_params['username'] = username
            connection_params['password'] = password
        elif password:  # 只有密码没有用户名的情况
            connection_params['password'] = password

        client = redis.Redis(**connection_params)

    return client