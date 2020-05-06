import os
import re
files = os.listdir()
comb_num = 0
for f in files:
    if bool(re.match(r'dns(\d+).times',f)):
        comb_num = int(re.sub(r'dns(\d+).times',r'\1',f))
out_f = 'poc_dns%s.times'%(comb_num+1)
times = dict()
# if comb_num:
#     with open('poc_dns%s.times'%(comb_num)) as f:
#         lines = f.readlines()
#         for line in lines:
#             line = line.split()
#             times[line[0]] = {'miss':int(line[2]),'hit':int(line[1])}
files = list(sorted(filter(lambda x: re.search(r'\.trace',x),files)))
with open(out_f,'w+') as out:
    for f in files:
        with open(f) as t:
            lines = t.readlines()
            for line in lines:
                line = line.split()
                if len(line) < 3:
                    continue
                url = line[0]
                hit = int(line[1])
                miss = int(line[2])
                if url not in times:
                    times[url] = {'miss':miss,'hit':hit}
                elif hit >= 0:
                    times[url] = {'miss':(miss+times[url]['miss']),'hit':(hit+times[url]['hit'])}
    for url in times.keys():
        out.write('%s %f %f\n'%(url,round(times[url]['hit']/(len(files)//6),5) if times[url]['hit'] > -1 else -1,round(times[url]['miss']/(len(files)//6),5) if times[url]['miss'] > -1 else -1 ))