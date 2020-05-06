# with open('poc_dns_100000000.trace') as f:
#     urls = set()
#     line = f.readline()
#     while line:
#         urls.add(line.split()[0])
#         line = f.readline()
#     print(len(urls))
data = {}
with open('poc_dns7.times','r') as f:
    for line in f.readlines():
        split = line.split()
        url = split[0]
        hit = float(split[1])
        miss = float(split[2])
        data[url] = {'hit':hit*7,'miss':miss*7}
with open('poc_dns11.times','r') as f:
    for line in f.readlines():
        split = line.split()
        url = split[0]
        hit = float(split[1])*11
        miss = float(split[2])*11
        data[url]['hit'] += hit
        data[url]['miss'] += miss
        data[url]['hit'] = data[url]['hit']/18
        data[url]['miss'] = data[url]['miss']/18
with open('poc_dns18.times','w+') as f:
    for url in data:
        f.write('%s %f %f\n'%(url,data[url]['hit'],data[url]['miss']))