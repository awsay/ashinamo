#!/usr/bin/env python
#-*- coding:utf-8 -*-

now_data = {}
status = 0; msgs=""; results="";
try:
    raw_data = file('/proc/meminfo').read()
    temps = raw_data.strip().split('\n')
    for temp in temps:
        tmp = temp.split()
        now_data[tmp[0]]=tmp[1]
    results={}
    results['memtotal']=int(now_data['MemTotal:'])
    #results['memused']=int(now_data['MemTotal:'])-int(now_data['MemFree:'])-int(now_data['Buffers:'])-int(now_data['Cached:'])
    results['memused']=int(now_data['MemTotal:'])-int(now_data['MemFree:'])
    results['buffers']=int(now_data['Buffers:'])
    results['cached']=int(now_data['Cached:'])
    print 0, '', results
except Exception,e:
    print 1, e, ''
