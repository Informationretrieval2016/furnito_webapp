import json
import sys
sys.path.append('..')
import config

class Common:

    def __init__(self):
        self.json = config.json_store

    def IsSubString(self, SubStrList,Str): 
        '''
        #usage: determine if a string contains other string
        #arg: SubStrList: a list of substrings you want to find if is in target string. Str: target String
        #return: if Str has all SubStr in SubStrList
        '''
        flag=True  
        for substr in SubStrList:  
            if not(substr in Str):      
                flag=False  
        return flag  
 
    def GetFileList(self, FindPath):
        '''
        #usage: get all json file.
        #arg: the path where json files are
        #return: a list of urls for all json files 
        '''  
        import os  
        FlagStr = ['.json']
        FileList=[]  
        FileNames=os.listdir(FindPath)  
        if (len(FileNames)>0):  
            for fn in FileNames:  
                if (len(FlagStr)>0):   
                    if (self.IsSubString(FlagStr,fn)):  
                        fullfilename=os.path.join(FindPath,fn)  
                        FileList.append(fullfilename)  
                else:  
                    fullfilename=os.path.join(FindPath,fn)  
                    FileList.append(fullfilename) 
        if (len(FileList)>0):
            FileList.sort()
        return FileList

    def readJSON(self, file):
        '''
        #usage: read a json file
        #arg: json file path
        #return: data in json structure
        '''
        json_data = open(file).read()
        data = json.loads(json_data)
        return data

    def getJSONData(self, name):
        '''
        #usage: get data from a json file by name
        #arg: name of json file
        #return: json data
        '''
        url = self.json + '/' + name + '.json'
        json_data = open(url).read()
        data = json.loads(json_data)
        return data