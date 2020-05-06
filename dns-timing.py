import os
import sys
import datetime
import pause

def time_url(url):
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    os.system('sudo systemd-resolve --flush-caches')
    cmd = 'dig {} +time=3 -u | grep time | tail -1'.format(url) #defaults to 3 tries
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
    now = datetime.datetime.now()
    with open('{}.dns{}.trace'.format(now.strftime('%Y%h%d_%H:%M'),part), 'w') as f:
        for url in lines:
            line = time_url(url)
            f.write(line)
            i += 1
            if i%100 == 0:
                f.flush()
if __name__ == '__main__':
    argc = len(sys.argv) - 1
    if argc != 2:
        raise Exception('Must give a number between 1 and 6 as argument')
    vm_num = 0
    try:
        vm_num = int(sys.argv[1])
    except:
        raise Exception('Must give a number between 1 and 6 as argument')
    try:
        niters = int(sys.argv[2])
    except:
        raise Exception('Must give a number of itereations')
    if 1 > vm_num > 6:
        raise Exception('Must give a number between 1 and 6 as argument')
    partition_size = int(1e6//6)
    start = (vm_num-1)*partition_size
    end = start + partition_size if vm_num < 6 else int(1e6+1)
    i = 0
    while i < niters:
        start_time = datetime.datetime.now()
        main(start,end,vm_num)
        start_time += datetime.timedelta(days=1,hours=1)
        pause.until(start_time)
        i+=1
