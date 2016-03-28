from common import Common
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
        for i in range(1,6):
            rand = int(random.random()*len(file_list))
            related.append(file_list[rand])
        return related
