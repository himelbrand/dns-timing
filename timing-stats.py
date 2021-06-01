import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import re

def aggregate_times(args):        
    times = dict()
    if args.input:
        print(f'using data from {args.input}...')
        with open(args.input) as f:
            line = f.readline()
            while line:
                url,hit,miss = line.split()
                times[url] = {'hit':float(hit),'miss':float(miss)}
                line = f.readline()
        return times
    files = os.listdir(args.basedir)
    files = list(sorted(filter(lambda x: re.search(r'\.trace',x),files)))
    for f in files:
        with open(f'{args.basedir}/{f}') as t:
            lines = t.readlines()
            for line in lines:
                line = line.split()
                if len(line) < 3:
                    continue
                url = line[0]
                hit = int(line[1])
                miss = int(line[2])
                if 'May' in f or 'Jun' in f:
                    hit/=1000
                    miss/=1000    
                hit = hit if hit >=0 else 1000
                miss = miss if miss >= 0 else 10000
                if url not in times and hit >= 0:
                    times[url] = {'miss':[miss],'hit':[hit]}
                elif hit >= 0:
                    times[url]['miss'].append(miss)
                    times[url]['hit'].append(hit)  
   
    return times


def parse_args():
    parser = argparse.ArgumentParser(prog='timing-stats.py',description='Displays statistics about times collected')
    parser.add_argument('-basedir', default='data' ,help='path to base directory containing collected times (default: "data").')
    parser.add_argument('-vm_num',dest='vm_num', default=6, type=int, help='a positive integer for the used number of vms.')
    parser.add_argument('-i',metavar='INPUT_PATH',dest='input', default=None, help='path for aggregated times input file, if not given aggregation is done from files in basedir.')
    parser.add_argument('--logscale',dest='log_scale',default=True,action='store_const',const=True,help='flag to make histogram plot y-scale be in log-scale.')
    args = parser.parse_args()
    if args.vm_num <= 0:
        raise argparse.ArgumentTypeError(f'{args.vm_num} is an invalid positive integer.')
    return args


if __name__ == "__main__":
    args = parse_args()
    flatten = lambda t: [item for sublist in t for item in sublist]
    if os.path.exists('flat-hits') and os.path.exists('flat-misses'):
        with open('flat-hits') as f:
            print('Loading hits')
            lines = f.readlines()
            valid_h = [float(n) for n in lines]
        with open('flat-misses') as f:
            print('Loading misses')
            lines = f.readlines()
            valid_m = [float(n) for n in lines]
    else:
        print('aggregating times...')
        times = aggregate_times(args)
        print('filtering times...')
        flat_hits = flatten([times[url]['hit'] for url in times])
        flat_misses = flatten([times[url]['miss'] for url in times])
        valid_h = list(filter(lambda x:x>=0,flat_hits))
        valid_m = list(filter(lambda x:x>=0,flat_misses))
        with open('flat-hits','w') as f:
            f.write('\n'.join([str(n) for n in valid_h]))
        with open('flat-misses','w') as f:
            f.write('\n'.join([str(n) for n in valid_m]))
    print('converting to numpy...')
    hits = np.array(valid_h)
    misses = np.array(valid_m)
    print('Some stats...')
    print(f'Max. value of misses: {misses.max()}')
    print(f'Max. value of hits: {hits.max()}')
    print(f'Min. value of misses: {misses.min()}')
    print(f'Min. value of hits: {hits.min()}')
    print(f'Mean of misses: {misses.mean()}')
    print(f'Mean of hits: {hits.mean()}')
    print(f'Std. of misses: {misses.std()}')
    print(f'Std. of hits: {hits.std()}')

    print('Plotting combined Histogram...')
    plt.close()
    plt.figure(figsize=(7,5))
    plt.ylabel(f'Frequency{" - log scale" if args.log_scale else ""}',fontsize=20)
    plt.xlabel('Access Time (ms)',fontsize=20)
    plt.xticks(fontsize=15,rotation=45)
    plt.yticks(fontsize=15)
    plt.hist(misses,label='Misses',color='#ffa50080',density=True,bins=100)
    plt.hist(hits,label='Hits',color='#9D839F',density=True,bins=100)
    plt.legend(fontsize=18)
    if args.log_scale:
        plt.yscale('log')
    plt.tight_layout()
    plt.show()
    plt.pause(0.01)
    input("Press enter to continue...")
    plt.close()


