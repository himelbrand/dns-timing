import os
import sys
import datetime
import pause
import argparse

def time_url(url):
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    os.system('sudo systemd-resolve --flush-caches')
    cmd_miss = 'dig {} +time=3 -u | grep time | tail -1'.format(url) 
    cmd_hit = 'dig {} +norecurse +time=3 -u | grep time | tail -1'.format(url) 
    try:
        miss = int(os.popen(cmd_miss).read().split()[3])
        hit = int(os.popen(cmd_hit).read().split()[3])
    except: #timed out 3 times
        miss = -1
        hit = -1
    return '{} {} {} {}\n'.format(url,hit,miss,dt_string)
    

def main(start,end,part,filename):
    f = open(filename)
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

def parse_args():
    parser = argparse.ArgumentParser(prog='dns-timing.py',description='Collects dns lookup times for cache miss and hit from list of urls.')
    parser.add_argument('max_vm',  type=int,help='a positive integer for the max number of vms.')
    parser.add_argument('vm', type=int,help='an integer for the vm number.')
    parser.add_argument('iters', type=int, help='number of iterations to run the script over the segment of urls.')
    parser.add_argument('-input', dest='input', default='1M_webrank',help='path to input file containing urls to time (default: "1M_webrank").')
    parser.add_argument('-dd',dest='days', metavar='D',default=1, type=int, help='an integer for the iteration delay in days (default: 1).')
    parser.add_argument('-hd',dest='hours', metavar='H',default=1, type=int, help='an integer for the iteration delay in hours (default: 1).')
    args = parser.parse_args()
    if args.max_vm <= 0:
        raise argparse.ArgumentTypeError(f'{args.max_vm} is an invalid positive integer.')
    if not (1 <= args.vm <= args.max_vm):
        raise argparse.ArgumentTypeError(f'{args.vm} is an invalid vm number, must be an integer between 1 and {args.max_vm}.')
    if args.max_vm <= 0:
        raise argparse.ArgumentTypeError(f'{args.iters} is an invalid positive integer.')
    return args

def get_urls_count(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    return len(lines)

if __name__ == '__main__':
    args = parse_args()
    url_count = get_urls_count(args.input)
    partition_size = int(url_count//args.max_vm)
    start = (args.vm-1)*partition_size
    end = start + partition_size if args.vm < args.max_vm else int(url_count+1)
    i = 0
    while i < args.iters:
        start_time = datetime.datetime.now()
        main(start,end,args.vm,args.input)
        start_time += datetime.timedelta(days=args.days,hours=args.hours)
        pause.until(start_time)
        i+=1
