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
                if url not in times and hit >= 0:
                    times[url] = {'miss':miss,'hit':hit}
                elif hit >= 0:
                    times[url] = {'miss':(miss+times[url]['miss']),'hit':(hit+times[url]['hit'])}        
    for url in times.keys():
        times[url] = {
            'hit':round(times[url]['hit']/(len(files)//args.vm_num),5) if times[url]['hit'] >= 0 else -1,
            'miss':round(times[url]['miss']/(len(files)//args.vm_num),5) if times[url]['miss'] >= 0 else -1
            }
    if args.output:
        print(f'Saving aggregated times to {args.output}...')
        with open(args.output,'w+') as f:
            for url in times:
                f.write(f'{url} {times[url]["hit"]} {times[url]["miss"]}\n')
    return times
def parse_args():
    parser = argparse.ArgumentParser(prog='timing-stats.py',description='Displays statistics about times collected')
    parser.add_argument('-basedir', default='data' ,help='path to base directory containing collected times (default: "data").')
    parser.add_argument('-vm_num',dest='vm_num', default=6, type=int, help='a positive integer for the used number of vms.')
    parser.add_argument('-o',metavar='OUTPUT_PATH',dest='output', default='mean_times.out', help='path for aggregated times output file (default: "mean_times.out")')
    parser.add_argument('-i',metavar='INPUT_PATH',dest='input', default=None, help='path for aggregated times input file, if not given aggregation is done from files in basedir.')
    parser.add_argument('--logscale',dest='log_scale',default=False,action='store_const',const=True,help='flag to make histogram plot y-scale be in log-scale.')
    args = parser.parse_args()
    if args.vm_num <= 0:
        raise argparse.ArgumentTypeError(f'{args.vm_num} is an invalid positive integer.')
    return args

if __name__ == "__main__":
    print('parsing cmd args...')
    args = parse_args()
    print('aggregating times...')
    times = aggregate_times(args)
    print('filtering times...')
    valid = list(filter(lambda x:x[0]>=0 and x[1]>=0,[(times[url]['hit'],times[url]['miss']) for url in times]))
    print('splitting times...')
    hits = np.array([x[0] for x in valid])
    misses = np.array([x[1] for x in valid])
    print('Some stats...')
    print(f'Max. value of misses: {misses.max()}')
    print(f'Max. value of hits: {hits.max()}')
    print(f'Min. value of misses: {misses.min()}')
    print(f'Min. value of hits: {hits.min()}')
    print(f'Mean of misses: {misses.mean()}')
    print(f'Mean of hits: {hits.mean()}')
    print(f'Std. of misses: {misses.std()}')
    print(f'Std. of hits: {hits.std()}')

    print('Plotting Histogram...')
    plt.figure(figsize=(7,5))
    plt.ylabel(f'Frequency{" - log scale" if args.log_scale else ""}',fontsize=16)
    plt.xlabel('Access Time (ms)',fontsize=16)
    plt.xticks(fontsize=12,rotation=45)
    plt.yticks(fontsize=12)

    plt.hist(misses,label='Misses',color='#ffa50080',density=True,bins=75)
    plt.hist(hits,label='Hits',color='#9D839F',density=True,bins=75)
    plt.legend(fontsize='x-large')
    if args.log_scale:
        plt.yscale('log')
    plt.tight_layout()
    plt.show()
    plt.pause(0.01)
    input("Press enter to continue...")
    plt.close()


