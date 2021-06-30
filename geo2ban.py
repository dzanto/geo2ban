#!/usr/bin/env python

"""
The script monitors access.log
and adds addresses that are not included in ALLOWED_COUNTRIES to blackhole
"""

import os
import time
from geoip import geolite2
from datetime import datetime
from netaddr import IPAddress, IPSet


LOGFILE = 'access.log'
WHITELIST_FILE = 'whitelist.txt'
BANLIST_FILE = 'banlist.txt'
SLEEP_INTERVAL = 3
# QUERIES_PER_SECOND = 2
# MAX_QUERIES_PER_SLEEP_INTERVAL = SLEEP_INTERVAL * QUERIES_PER_SECOND

# Define the codes in ALLOWED_COUNTRIES from ISO 3166 Country Codes
# Examples: https://dev.maxmind.com/geoip/legacy/codes/iso3166/
ALLOWED_COUNTRIES = ('RU',)

banned_ips = set()
counter_ip = {}
whiteIPSet = IPSet()

def set_whitelist():
    """
    Fill whitelist with ip addresses from WHITELIST_FILE.
    """
    with open(WHITELIST_FILE) as wl_file:
        for line in wl_file:
            if line.startswith(('#', '\n', ' ')):
                continue
            whiteIPSet.add(line.replace('\n', ''))

def ip_checker(ip):
    """
    Getting country from geoip
    Checking IP for entering WHITELIST and ALLOWED_COUNTRIES
    Add bad address that is not included in ALLOWED_COUNTRIES to blackhole
    """
    geo_ip = geolite2.lookup(ip)
    if (geo_ip is None) or (geo_ip.country in ALLOWED_COUNTRIES):
        return None
    elif (ip in banned_ips) or (IPAddress(ip) in whiteIPSet):
        return None
    else:
        # os.system('ip route add blackhole {0}'.format(ip))
        banned_ips.add(ip)
        with open(BANLIST_FILE, 'a') as banlist:
            now_datetime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            banlist.write(f'{now_datetime} {ip} {geo_ip.country}\n')


        # Обработка частоты запросов:
        # counter_ip.setdefault(ip, 0)
        # counter_ip[ip] += 1
        # if (counter_ip[ip] >= MAX_QUERIES_PER_SLEEP_INTERVAL):
        #     bad_ips.add(ip)
        #     print(f'ip route add blackhole {ip}')
        #     os.system(f'ip route add blackhole {ip}')


def watch(fd):
    """
    Getting IPs from LOGFILE each SLEEP_INTERVAL
    """
    stat = os.fstat(fd)
    size = stat.st_size

    while True:
        stat = os.fstat(fd)
        if size != stat.st_size:
            buf = os.read(fd, stat.st_size - size)
            size = stat.st_size

            for line in buf.decode("utf-8").splitlines():
                split_line = line.split()
                ip = split_line[0]
                ip_checker(ip)

        banned_ips.clear()
        time.sleep(SLEEP_INTERVAL)

def main():
    set_whitelist()
    f = open(LOGFILE)
    f.seek(0, os.SEEK_END)
    watch(f.fileno())

main()
