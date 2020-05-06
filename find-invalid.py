import os
from collections import Counter
def create_poc(invalids):
    with open('1M_webrank') as f:
        data = f.readlines()
        data = [l.split()[1:] for l in data]
    with open('1M_poc_webrank','w+') as f:
        rank = 1
        for d in data:
            url,visits = d
            if url in invalids:
                continue
            f.write('%d\t%s\t%s\n'%(rank,url,visits))
            rank += 1
def print_invalid():
    files = os.listdir()
    invalid = Counter()
    valid = Counter()
    high_hits_count = 0
    max_hit = -1
    max_miss = -1
    min_hit = float('inf')
    min_miss = float('inf')
    for fname in files:
        if '.trace' not in fname:
            continue
        with open(fname) as f:
            lines = f.readlines()
            data_lines = [line.split() for line in lines]
            for dl in data_lines:
                if len(dl) < 3:
                    continue
                url = dl[0]
                hit = int(dl[1])
                miss = int(dl[2])
                if hit == -1:
                    invalid[url] += 1
                else:
                    valid[url] += 1
                if hit > miss:
                    high_hits_count+=1
                    # print('url:%s,hit:%d,miss:%d'%(url,hit,miss))
                if max_hit < hit:
                    max_hit = hit
                if max_miss < miss:
                    max_miss = miss
                if hit >= 0 and hit < min_hit:
                    min_hit = hit
                if miss >= 0 and miss < min_miss:
                    min_miss = miss
                if 0 <= miss < 10:
                    print('url:%s,hit:%d,miss:%d'%(url,hit,miss))
    for url in invalid.keys():
        print('url:%s, timeout count:%d, valid count:%d'%(url,invalid[url],valid[url]))
    print('suspected as invalid:')
    for url in invalid.keys():
        if valid[url] == 0:
            print(url)    
    print('number of hits larger than miss: %d'%high_hits_count)
    print('max-hit:%d'%max_hit)
    print('max-miss:%d'%max_miss)
    print('min-hit:%d'%min_hit)
    print('min-miss:%d'%min_miss)
    # create_poc(set(invalid.keys()))
if __name__ == '__main__':
    print_invalid()