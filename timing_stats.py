import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns  # for nicer graphics
import pandas as pd  # for convinience
from collections import Counter

with open('poc_dns18.times') as f:
    lines = f.readlines()
    valid = list(filter(lambda x:x[0]>=0 and x[1]>=0,[(float(line.split()[1]),float(line.split()[2])) for line in lines]))
    hits = [x[0] for x in valid]
    # hits = hits + [-1*x for x in hits]
    misses = [x[1] for x in valid]
mean_hits = []
mean_misses = []
std_hits = []
std_misses = []
print(len(misses))
df = pd.DataFrame(data={'Latency (ms)':np.array(hits+misses),'Type':['hit' for m in hits]+['miss' for m in misses]})
vm = pd.DataFrame(data={'Latency (ms)':misses,'Type':['miss' for m in misses]})
vh = pd.DataFrame(data={'Latency (ms)':hits,'Type':['hit' for m in hits]})
missT = pd.DataFrame(data={'Type by latency':['Low' if m <150 else 'High' if m < 1000 else 'Very High' for m in misses]})
hitT = pd.DataFrame(data={'Type by latency':['Near zero' if m < 1 else 'Low' if m < 10 else 'Medium' if m < 50 else 'High' if m < 150 else 'Very High' for m in hits]})

def getType(x):
    # if x >= 10000:
    #     return 10000
    # if x >= 7500:
    #     return 7500
    # if x >= 5000:
    #     return 5000
    # if x >= 2500:
    #     return 2500
    if x >= 1000:
        return 1000
    if x >= 750:
        return 750
    if x >= 500:
        return 500
    if x >= 300:
        return 300
    if x >= 200:
        return 200
    if x >= 150:
        return 150
    if x >= 100:
        return 100
    if x >= 75:
        return 75
    if x >= 50:
        return 50
    if x >= 25:
        return 25
    if x >= 10: 
        return 10
    if x >= 5:
        return 5
    if x >= 2.5:
        return 2.5
    if x >= 1:
        return 1
    else:
        return 0.5
types_hits = [h for h in hits]
types_misses = [h for h in misses]

print(df.head())
print(vm.head())
xs = range(1,len(lines))
# for i in xs:
#     mean_hits.append(np.mean(hits[:i]))
#     std_hits.append(np.std(hits[:i]))
#     mean_misses.append(np.mean(misses[:i]))
#     std_misses.append(np.std(misses[:i]))
#     print(i)
# plt.hist(hits,bins=100,density=True)
print(max(misses))
# plt.xlim(0, 2000)
# plt.hist(misses,bins=100,density=True,histtype='step',color='blue')
# plt.hist(misses,bins=70,histtype='bar',color='red',align='left',density=True)
print(len(hits))
hc = Counter(types_hits)
total = sum(hc.values())

for key in hc.keys():
    hc[key] = hc[key]/total
hc1 = Counter(types_misses)
total = sum(hc1.values())
for key in hc1.keys():
    hc1[key] = hc1[key]/total
hitX = list(sorted([float(x) for x in hc.keys()]))
hitY = [hc[x] for x in hitX]
missX = list(sorted([float(x) for x in hc1.keys()]))
missY = [hc1[x] for x in missX]
# plt.plot(list(hc.keys()),list(hc.values()))
# plt.plot(hitX,hitY,color='red',label='1')
# plt.yscale('log')
plt.ylabel('log(frequency)',fontsize=20)
plt.xlabel('latency (ms)',fontsize=20)
plt.xticks(fontsize=12,rotation=45)
# plt.plot(missX,missY,'b-.',color='orange',label='Misses')
plt.yticks(fontsize=12)
# hits = [int(h) for h in hits]
# misses = [int(h) for h in misses]
# print(hc.most_common(1))
# print(hc1.most_common(1))

# plt.hist(misses,label='Misses',color='orange',density=True)
# plt.hist(hits,label='Hits',color='blue',density=True)
# plt.plot(hitX,hitY,'r:',color='blue',label='Hits')
# plt.legend()

# plt.hist(types_hits,density=True,label='2')
# plt.plot(missX,missY,label='3')
# plt.hist(types_misses,density=True,label='4')
# plt.legend()

# print(vm['Latency (ms)'].value_counts())
# plt.hist(hits,bins=40,histtype='bar',color='blue',log=True)
# sns.swarmplot(x='Type',y='Latency (ms)',data=vm)

# sns.distplot(hits,axlabel='Latency ms',kde_kws={'bw':0.05,'color':'red','kernel':'gau','gridsize':200},rug=True,rug_kws={'color':'#230fff0f'})
# sns.distplot(hits,kde_kws={'bw':0.5,'clip': (0, 5000)})
# sns.distplot(misses,kde=False,color='orange',norm_hist=True,label='Misses')
# sns.distplot(hits,kde=False,color='blue',norm_hist=True,label='Hits',bins=3)
# plt.legend()
# sns.distplot(np.array(misses)-np.array(hits),kde_kws={'bw':0.5,'clip': (0, 5000)})
hitT['Type by latency'].value_counts(normalize=True).plot(kind='bar', subplots=True,rot=0)
# plt.yscale('log')
# ax = vh['Latency (ms)'].value_counts(sort=False).hist(density=True)
# ax = sns.distplot(np.array(hits),axlabel='Latency ms',kde=True,kde_kws={'bw':0.5,'color':'red','clip': (-1.0, 1000)},rug=False,rug_kws={'color':'#230fff0f'})
# sns.distplot(miss["Type by latency"])
# ax = sns.swarmplot(misses,color='#ff0f0f05')
# sns.swarmplot(hits,color='blue',ax=ax)
plt.show()
def plt_show():
    '''Text-blocking version of plt.show()
    Use this instead of plt.show()'''
    # plt.draw()
    plt.pause(0.01)
    input("Press enter to continue...")
    plt.close()

plt_show()
# plt.plot(misses)
# plt.show()

