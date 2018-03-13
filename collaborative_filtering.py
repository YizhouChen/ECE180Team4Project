import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from math import sqrt
import abc
from collections import defaultdict
import random

‘’‘distance metrics: pearson distance & cosine distance’‘’
def pearson(dataA, dataB, significanceWeighting = False):
    intersection = [obj for obj in dataA if obj in dataB]
    if len(intersection) == 0:
        return 0
    meanA = np.mean([dataA[obj] for obj in dataA.keys()])
    meanB = np.mean([dataB[obj] for obj in dataB.keys()])
    numerator = sum([(dataA[obj] - meanA) * (dataB[obj] - meanB) for obj in intersection])
    deviationA = sqrt(sum([(dataA[obj] - meanA) ** 2 for obj in intersection]))
    deviationB = sqrt(sum([(dataB[obj] - meanB) ** 2 for obj in intersection]))
    if (deviationA * deviationB) == 0:
        return 0
    correlation = numerator / (deviationA * deviationB)
    return correlation
def cosine(dataA, dataB):
    interSet = [obj for obj in dataA if obj in dataB]
    if len(interSet) == 0:
        return 0
    AB = sum([dataA[obj] * dataB[obj] for obj in interSet])
    normA = sqrt(sum([dataA[obj] ** 2 for obj in dataA]))
    normB = sqrt(sum([dataB[obj] ** 2 for obj in dataB]))
    denominator = normA * normB
    if denominator == 0:
        return -1
    return AB / denominator
    
def parseData(fname):
    with open(fname) as f:
        for line in f:
            yield eval(line)
class collaborativeFiltering():    
    def __init__(self):
        self.Items = None
        self.Users = None
        self.Ratings = None
    def load_dataset(self,fname):
        pd_dataset = pd.read_json(fname,lines=True)
        return pd_dataset
    def load_review(self):
        return list(parseData('review.json'))
    
    def construct_matrix(self,review):
        UserList = {} # 
        ItemList = {} # store all user-rating pair for specific item
        RatingList = {}
        for r in review:
            u,i = r['user_id'],r['business_id']
            RatingList[(u,i)] = r['stars']
            if u in ItemList:
                ItemList[u][i] = r['stars']
            else:
                ItemList[u] = {i:r['stars']}
            if i in UserList:
                UserList[i][u] = r['stars']
            else:
                UserList[i] = {u:r['stars']}
        self.Items = ItemList
        self.Users = UserList
        self.Ratings = RatingList
    def get_similar_users(self,userA,user,Item):
        '''first find top-k similar users'''
        similarities = [(cosine(Item[userA],Item[userB]),userB) for userB in user['user_id'] if userB != userA]
        similarities.sort(reverse = True)
        if len(similarities) == 0:
            return None
        elif len(similarities) < 50:
            k_sim = [(simi,name) for simi,name in similarities if simi > 0]
            return k_sim
        else:
            k_sim = [(simi,name) for simi,name in similarities if simi > 0.1]
            return k_sim
    def predict_rating(self,userA,itemA,k_sim,Item,Rating,business):
        score = 0
        denom = 0
        if k_sim == None:
            score = float(business[business['business_id'] == itemA]['stars'])
        else:
            for weight,us in k_sim:
                if itemA in Item[us]:
                    score += Rating[(us,itemA)]
                    denom += 1
            if denom != 0:
                score /= denom
            # if no similar user rated itemA, simply return average of itemA
            else:
                score = float(business[business['business_id'] == itemA]['stars'])
        # modify score if out of range
        if score < 1:
            score == 1
        if score > 5:
            score == 5
        return score
    def generate_user_item_pair(self,UserList,ItemList):
        i_idx = random.randint(0,len(ItemList))
        u_idx = random.randint(0,len(UserList))
        i_name = ItemList.at[i_idx,'business_id']
        u_name = UserList.at[u_idx,'user_id']
        return (u_name,i_name)
def main():
    CBCF = collaborativeFiltering()
    # load dataset
    businesses = CBCF.load_dataset('business.json')
    checkins = CBCF.load_dataset('checkin.json')
    tips = CBCF.load_dataset('tip.json')
    users = CBCF.load_dataset('user.json')
    review = CBCF.load_review()
    # construct user-item pairs
    CBCF.construct_matrix(review)
    Item = CBCF.Items
    User = CBCF.Users
    Rating = CBCF.Ratings
    # generate random user-item pair for test
    user123,item123 = CBCF.generate_user_item_pair(users,businesses)
    # predict scores
    ksim_mat = CBCF.get_similar_users(user123,users,Item)
    score123 = CBCF.predict_rating(user123,item123,ksim_mat,Item,Rating,businesses)
    print(score123)
main()
    
