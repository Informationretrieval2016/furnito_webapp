from common import Common
import sys
import operator
from vsm import VSM
sys.path.append('..')
import config 

class Search:

    def __init__(self):
        self.com = Common()
        self.json = config.json_store
        self.vsm = VSM()

    def search_hardmatch(self, name):
    	'''
        #usage: A search function for test
        #arg: search query
        #return: path of json files which contain search query
    	'''
        src = self.json;
        furniture_list = self.com.GetFileList(src)
        for furniture in furniture_list:
            if name not in furniture:
                furniture_list.remove(furniture)
        return furniture_list

    def search_bm25(self,query):
        furniture_list = []
        query = " ".join(query.split())
        query_list = query.split()
        furniture_dict = self.vsm.bm25_vector_space(query_list)
        furniture_dict = sorted(furniture_dict.items(), key = operator.itemgetter(1), reverse = True)
        furniture_list = [ (self.json + furniture[0] + '.json') for furniture in furniture_dict]
        return furniture_list

# search = Search()
# search.search_bm25("chair")

