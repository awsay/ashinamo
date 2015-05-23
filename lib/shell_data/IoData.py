#!/usr/bin/env python
#-*- coding:utf-8 -*-

import simplejson as json
import time 
import re

devices=['sda']
while True:
    now_data = {} # ��ǰ /proc/diskstats  ��ֵ
    last_data = {} # ��һ�� /proc/diskstats  ��ֵ, ʱ�����ɵ��ó������

    #��ȡ��ǰ����
    raw_data = file('/proc/diskstats').read()
    now_data['timestamp'] = time.time()
    for device in devices:
        pat = device + " .*"
        devicedata = re.search(pat, raw_data).group()
        tmp = devicedata.split() 
        now_data[tmp[0]] = {
            'number_of_issued_reads':tmp[1], # Field 1  
            'number_of_reads_merged':tmp[2], # Field 2
            'number_of_sectors_read':tmp[3], # Field 3
            'number_of_milliseconds_spent_reading':tmp[4],    # Field 4    
            'number_of_writes_completed':tmp[5],      # Field 5
            'number_of_writes_merged':tmp[6],         # Field 6
            'number_of_sectors_written':tmp[7],       # Field 7
            'number_of_milliseconds_spent_writing':tmp[8],    # Field 8
            'number_of_IOs_currently_in_progress':tmp[9],    # Field 9
            'number_of_milliseconds_spent_doing_IOs':tmp[10],    # Field 10
            'number_of_milliseconds_spent_doing_IOs_2':tmp[11],    # Field 11
        }

    # ��ȡ��ʷ����
    try:
        results = file('/tmp/proc_diskstats').read()
        last_data = json.loads("%s" % results.strip())
    except:
        last_data = now_data

    # ���浱ǰ���ݵ���ʷ���ݱ���
    fp = file('/tmp/proc_diskstats', 'w')
    fp.write(json.dumps(now_data))
    fp.close()

    # �����������ݣ��õ�Ҫ�����ֵ
    results = {}
    timecut = float(now_data['timestamp']) - float(last_data['timestamp'])
    if timecut > 0:
        for key in devices:
            reading = (int(now_data[key]['number_of_sectors_read']) - int(last_data[key]['number_of_sectors_read']))/float(2)/timecut
            writing = (int(now_data[key]['number_of_sectors_written']) - int(last_data[key]['number_of_sectors_written']))/float(2)/timecut
            results[key] = {'reading':int(reading), 'writing':int(writing)}
    else:
        # ��һ�μ��ص�ʱ����ʷ����Ϊ��, �޷����㣬���Գ�ʼ��Ϊ0
        for key in devices:
            results[key] = {'reading':0, 'writing':0}
    print results
    time.sleep(1)