import os
from collections import Counter
import argparse

def create_poc(invalids,fname):
    with open(fname) as f:
        data = f.readlines()
        data = [l.split()[1:] for l in data]
    with open(f'filtered_{fname}','w+') as f:
        rank = 1
        for d in data:
            url,visits = d
            if url in invalids:
                continue
            f.write('%d\t%s\t%s\n'%(rank,url,visits))
            rank += 1

def print_invalid(filename,basedir):
    files = os.listdir(basedir)
    invalid = Counter()
    valid = Counter()
    for fname in files:
        if '.trace' not in fname:
            continue
        print(fname)
        with open(f'{basedir}/{fname}') as f:
            lines = f.readlines()
            data_lines = [line.split() for line in lines]
            for dl in data_lines:
                if len(dl) < 3:
                    continue
                url = dl[0]
                hit = int(dl[1])
                if hit == -1:
                    invalid[url] += 1
                else:
                    valid[url] += 1
    for url in invalid.keys():
        print('url:%s, timeout count:%d, valid count:%d'%(url,invalid[url],valid[url]))
    print('suspected as invalid:')
    for url in invalid.keys():
        if valid[url] == 0:
            print(url)    
    ans = '?'
    while ans.lower() != 'y' and ans.lower() != 'n':
        ans = input('Do you wish to create a filtered urls list file without these urls? (y/n)')
    if ans.lower() == 'y':
        create_poc(set(invalid.keys()),filename)
        print('\n\nCreated new urls list!')
    else:
        print('\n\nNew urls list was not created!')

def parse_args():
    parser = argparse.ArgumentParser(prog='find-invalid.py',description='Displays suspect urls from file that might be invalid and creates a new urls list file on demand.')
    parser.add_argument('-filename',  default='1M_webrank',help='path to input file containing urls to time (default: "1M_webrank").')
    parser.add_argument('-basedir', default='.' ,help='path to base directory containing collected times (default: ".").')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    print_invalid(args.filename,args.basedir)