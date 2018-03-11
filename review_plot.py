import collaborative_filtering
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from math import sqrt
from collections import defaultdict
import random

CBCF = collaborativeFiltering()
# load dataset
businesses = CBCF.load_dataset('business.json')
checkins = CBCF.load_dataset('checkin.json')
tips = CBCF.load_dataset('tip.json')
users = CBCF.load_dataset('user.json')
review = CBCF.load_review()

# count number of ratings for each star
from collections import defaultdict
rateCount = defaultdict(int)
for r in review:
    rateCount[r['stars']] += 1
rateCount
plt.bar(list(rateCount.keys()),rateCount.values())
plt.xlabel('stars')
plt.ylabel('count')
plt.title('number of reviews for each star')
plt.show()

# count number of ratings for each star across time
from collections import defaultdict
rateCount_t = defaultdict(int)
for r in review:
    year = r['date'].split('-')[0]
    rateCount_t[(r['stars'],year)] += 1
rateCount_t
rate_list = np.zeros((14,5))
for star,year in rateCount_t:
    rate_list[int(year)-2004,star-1] = rateCount_t[(star,year)]
rate_list
barWidth = 0.15
# bar plot of count of stars vs time
r1 = np.arange(2004-2004,2018-2004)
r2 = [x + barWidth for x in r1]
r3 = [x + 2*barWidth for x in r1]
r4 = [x + 3*barWidth for x in r1]
r5 = [x + 4*barWidth for x in r1]
fig = plt.figure(figsize=(40,20))
plt.rc('font',size=30)
plt.bar(r1,rate_list[:,0],width=barWidth)
plt.bar(r2,rate_list[:,1],width=barWidth)
plt.bar(r3,rate_list[:,2],width=barWidth)
plt.bar(r4,rate_list[:,3],width=barWidth)
plt.bar(r5,rate_list[:,4],width=barWidth)
plt.xticks(r2, [str(d) for d in range(4,18)])
plt.legend(['1 star','2 star','3 star','4 star','5 star'])
plt.ylabel('count')
plt.title('number of reviews for each star')
plt.show()
plt.savefig('histogram of each star rating vs time.jpg')
# plot of count of review vs time
fig = plt.figure(figsize=(40,30))
plt.rc('font',size=30)
plt.plot(r1,rate_list[:,0],linewidth=6)
plt.plot(r1,rate_list[:,1],linewidth=6)
plt.plot(r1,rate_list[:,2],linewidth=6)
plt.plot(r1,rate_list[:,3],linewidth=6)
plt.plot(r1,rate_list[:,4],linewidth=6)
plt.xticks(r1, [str(d) for d in range(2004,2018)])
plt.legend(['1 star','2 star','3 star','4 star','5 star'])
plt.ylabel('count')
plt.title('number of reviews for each star level')
plt.savefig('plot of each star rating vs time.jpg')
plt.show()
'''results show that number of reviews explodes with time, 
   but after 2013, only number of 5-star ratings explodes
   while number of other star level ratings didn't show 
   comparable increase '''
star_label = ['1 star','2 star','3 star','4 star','5 star']
for idx in range(14):
    fig = plt.figure(figsize=(15,15))
    plt.rc('font',size=20)
    plt.pie(rate_list[-idx,:],labels = star_label,autopct='%1.2f%%')
    plt.title('pie chart for year %s'%(2017-idx))
    plt.savefig('pie chart for year %s.jpg' %(2017-idx))
    plt.show()
