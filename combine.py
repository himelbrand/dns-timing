import os
import re
files = os.listdir()
comb_num = 0
for f in files:
    if bool(re.match(r'dns(\d+).times',f)):
        comb_num = int(re.sub(r'dns(\d+).times',r'\1',f))
out_f = 'dns%s.times'%(comb_num+1)
times = dict()
if comb_num:
    with open('dns%s.times'%(comb_num)) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            times[line[0]] = {'miss':int(line[2]),'hit':int(line[1])}
with open(out_f,'w+') as out:
    for i in range(1,7):
        with open('dns%s.trace'%(i)) as t:
            lines = t.readlines()
            for line in lines:
                line = line.split()
                url = line[0]
                hit = int(line[1])
                miss = int(line[2])
                if url not in times:
                    times[url] = {'miss':miss,'hit':hit}
                else:
                    times[url] = {'miss':(miss+comb_num*times[url]['miss'])/(comb_num+1),'hit':(hit+comb_num*times[url]['hit'])/(comb_num+1)}
    for url in times.keys():
        out.write('%s %s %s\n'%(url,times[url]['hit'],times[url]['miss']))