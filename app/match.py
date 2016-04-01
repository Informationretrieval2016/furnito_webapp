from common import Common
from app import db
from models import Clicks
import random
import sys
sys.path.append('..')
import config

class Match:

    def __init__(self):
        self.com = Common()

    def match_test(self):
        related = []
        file_list = self.com.GetFileList(config.json_store)
        related = random.sample(file_list,8)
        return related

    def match_furniture(self, name, age, favoritestyle, gender):
        related_furniture = []
        scores = []
        related_furniture_one_list = Clicks.query.filter_by(furniture_one = name).all()
        if len(related_furniture_one_list) == 0:
            file_list = self.com.GetFileList(config.json_store)
            related_furniture = random.sample(file_list,8)
            print 'return random'
            return related_furniture
        for related_furniture_one in related_furniture_one_list:
            score = 1
            if related_furniture_one.age == age:
                score = score + 1
            if related_furniture_one.favoritestyle == favoritestyle:
                score = score + 1
            if related_furniture_one.gender == gender:
                score = score + 1
            if related_furniture_one.furniture_one in related_furniture:
                index = related_furniture.index(related_furniture_one.furniture_one)
                scores[index] = scores[index] + score
            else:
                related_furniture.append(related_furniture_one.furniture_one)
                scores.append(score)
        related_furniture = zip(related_furniture,scores)
        print 'return related'
        return [list(t) for t in zip(*(sorted(related_furniture, key=lambda s : s[1], reverse = True)))][0]



