import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
def parseData(fname):
    
    with open(fname) as f:
        for line in f:
            yield eval(line)
 # load dataset
business = pd.read_json('business.json',lines=True)
checkin = pd.read_json('checkin.json',lines=True)
tip = pd.read_json('tip.json',lines=True)
user = pd.read_json('user.json',lines=True)
review = list(parseData('review.json'))

def check_has_null(table):
    truth_table = list(table.isnull().any())
    print(truth_table)
    return truth_table
def basic_info(table):
    length = len(table)
    types = type(table)
    columns = list(table.columns)
    info = dict()
    info['length'] = length
    info['type'] = types
    info['columns'] = columns
    return info
    
# average review_count
review_count = np.array(user['review_count'])
print('average review/person %f'% review_count.mean())
print('median %f' %np.median(review_count))
print('maximum review_count %d' % review_count.max())
print('minimum review_count %d' % review_count.min())

from collections import defaultdict
rateCount = defaultdict(int)
for r in review:
    rateCount[r['stars']] += 1
rateCount
