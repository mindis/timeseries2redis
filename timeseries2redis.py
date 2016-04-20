import datetime
import time
import redis
import pandas as pd


class TickData(object):
	"""
	Redis Timeseries read write functionality
	Pleae note: Change for columns of the timeseries is available through change of the structure list variable in set function
				e.g. structure = ["date", "open", "high", "low", "close"]

	"""
	def __init__(self, identifier, structure = ["date", "bid", "ask", "volume", "count"], to_dataframe = True):
		self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
		self.structure = structure
		self.to_dataframe = to_dataframe
		self.identifier = identifier
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

	def set(self, data, trim=None):
	    #create pipeline
	    pipe = self.r.pipeline()
	    #dict as input
	    for key in self.structure:
	        #prepare redis key
	        redis_key = self.identifier+":"+key
	        value = data[key]
	        pipe.rpush(redis_key, value)
	    #add ltrim
	    if trim != None:
	        for key in structure:
	            #prepare redis key
	            redis_key = self.identifier+":"+key
	            pipe.ltrim(redis_key,-trim,-1)
	    pipe.execute()
	    
	def get(self, start=0, end=-1):
	    #create pipeline
	    pipe = self.r.pipeline()
	    #list as input for structure
	    for key in self.structure:
	        #prepare redis key
	        redis_key = self.identifier+":"+key
	        pipe.lrange(redis_key, start, end)
	    data = pipe.execute()
	    data = dict(zip(self.structure, data))
	    if self.to_dataframe == True:
	        return self.__convert_to_df(data)
	    else:
	        return data

	def __getitem__(self, index):
	    if isinstance(index, int):
	        # process index as an integer
	        return self.get(self.identifier, start=index)
	    elif isinstance(index, slice):
	        start, stop = index.indices(len(self))    # index is a slice
	        # process slice
	        return self.get(self.identifier, start=start, end=end)
	    else:
	        raise TypeError("index must be int or slice")
