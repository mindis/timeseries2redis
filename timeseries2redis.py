import redis
import pandas as pd
import datetime
import time
import random



class Timeseries(object):
	"""

	"""
	def __init__(self):
		self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
		#r.flushdb()
	
	def __convert_to_df(self, data):
	    df = pd.DataFrame(data)
	    keys = df.keys()
	    for key in keys:
	        if key == "date":
	            df["date"] = pd.to_datetime(df["date"])
	        else:
	            df[key] = pd.to_numeric(df[key])
	    return df.set_index("date")

	def write_ts(self, identifier, data, structure = ["date", "bid", "ask", "volume", "count"], trim=None):
	    #create pipeline
	    pipe = self.r.pipeline()
	    #dict as input
	    for key in structure:
	        #prepare redis key
	        redis_key = identifier+":"+key
	        value = data[key]
	        pipe.rpush(redis_key, value)
	    #add ltrim
	    if trim != None:
	        for key in structure:
	            #prepare redis key
	            redis_key = identifier+":"+key
	            pipe.ltrim(redis_key,-trim,-1)
	    pipe.execute()
	    
	def read_ts(self, identifier, start=0, end=-1, structure = ["date", "bid", "ask", "volume", "count"], to_dataframe=False):
	    #create pipeline
	    pipe = self.r.pipeline()
	    #list as input for structure
	    for key in structure:
	        #prepare redis key
	        redis_key = identifier+":"+key
	        pipe.lrange(redis_key, start, end)
	    data = pipe.execute()
	    data = dict(zip(structure, data))
	    if to_dataframe == True:
	        return self.__convert_to_df(data)
	    else:
	        return data
