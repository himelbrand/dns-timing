import os
import sys
from datetime import datetime

def time_url(url):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    os.system('sudo systemd-resolve --flush-caches')
    cmd = 'dig {} +time=10 | grep time | tail -1'.format(url) #defaults to 3 tries
    try:
        miss = int(os.popen(cmd).read().split()[3])
        hit = int(os.popen(cmd).read().split()[3])
    except:
        miss = -1
        hit = -1
    return '{} {} {} {}\n'.format(url,hit,miss,dt_string)
    

def main(start,end,part):
    f = open('1M_webrank')
    lines = f.readlines()
    f.close()
    i = 1
    lines = [line.split()[1] for line in lines[start:end]]
    now = datetime.now()
    with open('{}.dns{}.trace'.format(now.strftime('%Y%h%d'),part), 'w') as f:
        for url in lines:
            line = time_url(url)
            f.write(line)
            i += 1
            if i%100 == 0:
                f.flush()
if __name__ == '__main__':
    argc = len(sys.argv) - 1
    if argc != 1:
        raise Exception('Must give a number between 1 and 6 as argument')
    vm_num = 0
    try:
        vm_num = int(sys.argv[1])
    except:
        raise Exception('Must give a number between 1 and 6 as argument')
    if 1 > vm_num > 6:
        raise Exception('Must give a number between 1 and 6 as argument')
    partition_size = int(1e6//6)
    start = (vm_num-1)*partition_size
    end = start + partition_size if vm_num < 6 else int(1e6+1)
    main(start,end,vm_num)