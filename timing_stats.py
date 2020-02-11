import numpy as np
import matplotlib.pyplot as plt

with open('poc_dns7.times') as f:
    lines = f.readlines()
    hits = np.array(list(filter(lambda x:x>=0,[float(line.split()[1]) for line in lines])))
    misses = np.array(list(filter(lambda x:x>=0,[float(line.split()[2]) for line in lines])))
mean_hits = []
mean_misses = []
std_hits = []
std_misses = []

xs = range(1,len(lines))

for i in xs:
    mean_hits.append(np.mean(hits[:i]))
    std_hits.append(np.std(hits[:i]))
    mean_misses.append(np.mean(misses[:i]))
    std_misses.append(np.std(misses[:i]))
    print(i)

plt.plot(xs,mean_hits)
plt.show()
plt.plot(xs,std_hits)
plt.show()
plt.plot(xs,mean_misses)
plt.show()
plt.plot(xs,std_misses)
plt.show()