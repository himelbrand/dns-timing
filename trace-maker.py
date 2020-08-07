import os
import time
import numpy.random as random
import multiprocessing as mp
import numpy as np
from bisect import bisect_left
import re
import argparse


urls = []
p = []
ranges = []
total_access = 0 
trace_lengths = []
times = dict()
def compute_total(fname):
    total_access = 0
    with open(fname) as f:
        line = f.readline()
        while line:
            _,_,count = line.split()
            count = int(count)
            total_access += count
            line = f.readline()
    return total_access

def main(): 
    for t_len in trace_lengths:
        filename = 'dns_%dM'%(t_len//(int(1e6)))
        count = len(list(filter(lambda x: re.search(filename,x),os.listdir()))) + 1
        suffix = '.trace'
        filename = filename + '_%d'%(count) + suffix
        with open(filename,'w') as f:
            for _ in range(t_len):
                idx = bisect_left(ranges,random.rand())
                url = urls[idx]
                hit,miss = times[url]['hit'],times[url]['miss']
                f.write('%s %s %s\n'%(url,hit,miss))     
        print(f'Finished creating {filename}')  

def init_globals(fname,basedir,vm_num,replace,r_hit,r_miss):   
    global total_access,p,urls,ranges
    total_access = compute_total(fname)
    f = open(fname)
    line = f.readline()
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
    ranges = list(np.array(ranges)/total_access)
    #aggregate times
    files = os.listdir(basedir)
    files = list(sorted(filter(lambda x: re.search(r'\.trace',x),files)))
    for f in files:
        with open(f'{basedir}/{f}') as t:
            lines = t.readlines()
            for line in lines:
                line = line.split()
                if len(line) < 3:
                    continue
                url = line[0]
                hit = int(line[1])
                miss = int(line[2])
                hit = hit if not replace or hit >=0 else r_hit
                miss = miss if not replace or miss >= 0 else r_miss
                if url not in times and hit >= 0:
                    times[url] = {'miss':miss,'hit':hit}
                elif hit >= 0:
                    times[url] = {'miss':(miss+times[url]['miss']),'hit':(hit+times[url]['hit'])}        
    for url in times.keys():
        times[url] = {
            'hit':round(times[url]['hit']/(len(files)//vm_num),5) if times[url]['hit'] >= 0 else -1,
            'miss':round(times[url]['miss']/(len(files)//vm_num),5) if times[url]['miss'] >= 0 else -1
            }

def parse_args():
    parser = argparse.ArgumentParser(prog='trace-maker.py',description='Creates new random traces from input file')
    parser.add_argument('-input', dest='input', default='filtered_1M_webrank',help='path to input file containing urls to time (default: "filtered_1M_webrank").')
    parser.add_argument('-length',dest='length', metavar='L',default=5e7, type=float, help='an integer for the number of requests in trace (default: 5e7).')
    parser.add_argument('-num',dest='num', metavar='N',default=1, type=int, help='an integer for the number of traces to create (default: 1).')
    parser.add_argument('-vm_num',dest='vm_num', default=6, type=int, help='a positive integer for the used number of vms.')
    parser.add_argument('-basedir', default='data' ,help='path to base directory containing collected times (default: "data").')
    parser.add_argument('-r_hit', default=1000, type=int, help='value for hit time in case of replace=True and negative time found (default: 1000).')
    parser.add_argument('-r_miss', default=10000, type=int, help='value for miss time in case of replace=True and negative time found (default: 10000).')
    parser.add_argument('--replace',dest='replace',const=True,default=False,action='store_const',help='if this flag is used then negative times will be replaced.')
    args = parser.parse_args()
    if int(args.length)%int(1e6):
        raise argparse.ArgumentTypeError(f'length argument must be a divisible by 1e6.')
    if args.num < 0:
        raise argparse.ArgumentTypeError(f'number of traces argument must be a positive integer.')
    if args.vm_num <= 0:
        raise argparse.ArgumentTypeError(f'{args.vm_num} is an invalid positive integer.')
    return args
if __name__ == '__main__':
    args = parse_args()
    init_globals(args.input,args.basedir,args.vm_num,args.replace,args.r_hit,args.r_miss)
    trace_lengths = [int(args.length)]*args.num
    main()
    print('Done.')
