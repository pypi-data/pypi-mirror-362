# -*- encoding: utf-8 -*-

'''
@File    :   dnspython_helper.py
@Time    :   2025/07/16 12:07:59
@Author  :   test233
@Version :   1.0
'''


import dns.resolver
from loguru import logger

def domain_to_ip(domain: str, dns_server: str = None) -> list:
    """
    解析域名到IP地址列表
    :param domain: 域名（例如：www.baidu.com）
    :param dns_server: 指定的DNS服务器（可选）
    :return: IP地址列表，如果解析失败则返回空列表
    """
    resolver = dns.resolver.Resolver()
    # 如果指定了DNS服务器，则使用该服务器
    if dns_server is not None:
        resolver.nameservers = [dns_server]
    try:
        # 解析域名的A记录（IPv4地址）
        answer = resolver.resolve(domain, 'A')
        return [str(ip) for ip in answer]
    except Exception as e:
        # 记录解析失败日志，并打印异常信息
        logger.debug(f'Failed to query IP for domain: {domain}', exc_info=True)
        return []

def domain_to_cname(domain: str, dns_server: str = None) -> list:
    """
    解析域名到CNAME记录列表
    :param domain: 域名（例如：www.baidu.com）
    :param dns_server: 指定的DNS服务器（可选）
    :return: CNAME记录列表，如果解析失败则返回空列表
    """
    resolver = dns.resolver.Resolver()
    # 如果指定了DNS服务器，则使用该服务器
    if dns_server is not None:
        resolver.nameservers = [dns_server]
    try:
        # 解析域名的CNAME记录
        answer = resolver.resolve(domain, 'CNAME')
        return [str(record.target).strip(".").lower() for record in answer]
    except Exception as e:
        # 记录解析失败日志，并打印异常信息
        logger.debug(f'Failed to query CNAME for domain: {domain}', exc_info=True)
        return []

if __name__ == '__main__':
    # 测试域名解析
    domain = 'www.baidu.com'
    print(f"Domain: {domain}")
    print(f"IP Addresses: {domain_to_ip(domain)}")
    print(f"CNAME Records: {domain_to_cname(domain)}")
