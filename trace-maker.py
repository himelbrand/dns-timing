import os
import time
import numpy.random as random
import multiprocessing as mp

f = open('1M_poc_webrank')
line = f.readline()
urls = []
p = []
total_access = 13499388626164 #used another script to get count
while line:
    line_data = line.split()
    per_day = int(line_data[2])
    urls.append(line_data[1])
    p.append(per_day/total_access)
    line = f.readline()
f.close()
trace_lengths = [int(1e5),int(1e6),int(1e7)] #10M requests long trace
        
def main():
    times = dict()
    with open('poc_dns7.times') as f:
        lines = f.readlines()
        for line in lines:
            url,hit,miss = line.split()
            times[url] = (hit,miss)
    for t_len in trace_lengths:
        with open('poc_dns_%d.trace'%t_len,'w') as f:
            for i in range(t_len):
                url = random.choice(urls,p=p)
                hit,miss = times[url]
                f.write('%s %s %s\n'%(url,hit,miss))
                if i%100 == 0:
                    f.flush()
        
        
if __name__ == '__main__':
    main()