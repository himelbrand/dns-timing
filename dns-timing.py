import os
import sys

def time_url(url):
    os.system('sudo systemd-resolve --flush-caches')
    cmd = 'dig {} | grep time | tail -1'.format(url)
    miss = os.popen(cmd).read().split()[3]
    hit = os.popen(cmd).read().split()[3]
    os.system('sudo systemd-resolve --flush-caches')
    return '{} {} {}\n'.format(url,hit,miss)

def main(start,end,part):
    f = open('1M_webrank')
    lines = f.readlines()
    f.close()
    lines = [line.split()[1] for line in lines[start:end]]
    with open('dns{}.trace'.format(part), 'w') as f:
        for url in lines:
            line = time_url(url)
            f.write(line)

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