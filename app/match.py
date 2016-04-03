from common import Common
from app import db
from models import Clicks, Comments
import random
import pandas as pd
import sys
sys.path.append('..')
import config

class Match:

    def __init__(self):
        self.com = Common()
        self.sentiment_doc = config.sentiment_path

    def match_test(self):
        related = []
        file_list = self.com.GetFileList(config.json_store)
        related = random.sample(file_list,8)
        return related

    def match_furniture(self, name, age, favoritestyle, gender):
        related_furniture = []
        scores = []
        related_furniture_one_list = Clicks.query.filter_by(furniture_one = name).all()
        related_furniture_two_list = Clicks.query.filter_by(furniture_two = name).all()
        if len(related_furniture_one_list) == 0 and len(related_furniture_two_list) == 0:
            file_list = self.com.GetFileList(config.json_store)
            related_furniture = random.sample(file_list,8)
            print 'return random'
            return related_furniture
        if len(related_furniture_one_list) != 0:
            for related_furniture_one in related_furniture_one_list:
                score = 1
                if related_furniture_one.age == age:
                    score = score + 1
                if related_furniture_one.favoritestyle == favoritestyle:
                    score = score + 1
                if related_furniture_one.gender == gender:
                    score = score + 1
                if config.json_store + related_furniture_one.furniture_two + '.json' in related_furniture:
                    index = related_furniture.index(related_furniture_one.furniture_two)
                    scores[index] = scores[index] + score
                else:
                    related_furniture.append(config.json_store + related_furniture_one.furniture_two + '.json')
                    scores.append(score)
        if len(related_furniture_two_list) != 0:
            for related_furniture_two in related_furniture_two_list:
                score = 1
                if related_furniture_two.age == age:
                    score = score + 1
                if related_furniture_two.favoritestyle == favoritestyle:
                    score = score + 1
                if related_furniture_two.gender == gender:
                    score = score + 1
                if config.json_store + related_furniture_two.furniture_one + '.json' in related_furniture:
                    index = related_furniture.index(related_furniture_two.furniture_one)
                    scores[index] = scores[index] + score
                else:
                    related_furniture.append(config.json_store + related_furniture_two.furniture_one + '.json')
                    scores.append(score)
        index = 0
        for rf in related_furniture:
            scores[index] += self.sentiment(self.get_comments(rf))
            index += 1
        related_furniture = zip(related_furniture,scores)
        related_furniture_list = [list(t) for t in zip(*(sorted(related_furniture, key=lambda s : s[1], reverse = True)))][0]
        if len(related_furniture_list) < 8:
            file_list = self.com.GetFileList(config.json_store)
            related_furniture_list.extend(random.sample(file_list,8-len(related_furniture_list)))
        print 'return related'
        return related_furniture_list

    def sentiment(self, comments):
        value = 0.0
        df = pd.read_csv(self.sentiment_doc, encoding = "utf-8")
        for comment in comments:
            words = comment.split()
            for word in words:
                value += df[df.word == 'a'].iloc[0,1]
        return value

    def get_comments(self, name):
        commentlist = []
        comments = Comments.query.filter_by(furniture_name = name).all()
        for comment in comments:
            commentlist.append(comment.comment)
        return commentlist



