import os
import time
import numpy.random as random
import multiprocessing as mp
import numpy as np
from bisect import bisect_left
import re

f = open('1M_poc_webrank')
line = f.readline()
urls = []
p = []
ranges = []
total_access = 13499388626164 #used another script to get count
while line:
    line_data = line.split()
    per_day = int(line_data[2])
    urls.append(line_data[1])
    p.append(per_day/total_access)
    if len(ranges):
        ranges.append(ranges[-1]+per_day)
    else:
        ranges.append(per_day)
    line = f.readline()
f.close()
trace_lengths = [int(1e6),int(2e6),int(5e6),int(1e7),int(2e7),int(5e7)]
ranges = list(np.array(ranges)/total_access)

def main():
    times = dict()
    with open('poc_dns7.times') as f:
        lines = f.readlines()
        for line in lines:
            url,hit,miss = line.split()
            times[url] = (hit,miss)
    for t_len in trace_lengths:
        filename = 'poc_dns_%dM'%(t_len//(int(1e6)))
        count = len(list(filter(lambda x: re.search(filename,x),os.listdir()))) + 1
        suffix = '.trace'
        filename = filename + '_%d'%(count) + suffix
        with open(filename,'w') as f:
            for i in range(t_len):
                idx = bisect_left(ranges,random.rand())
                url = urls[idx]
                hit,miss = times[url]
                f.write('%s %s %s\n'%(url,hit,miss))       
        
if __name__ == '__main__':
    main()
    print('done')
