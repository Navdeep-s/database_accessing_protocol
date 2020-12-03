from collections import OrderedDict
import time,pickle
class LRUCache:
	def __init__(self,capacity=20,expiry_time=3600):
		self.cache = OrderedDict() #Of type OrderedDict
		self.capacity = capacity
		self.expiry_time=expiry_time
	#query must be a tuple of the form (field_name,field_value)
	#Example ('Name','Vineet')
	def get(self,query):
		if query not in self.cache:
			return(-1)
		query_response = self.cache[query]
		timestamp = query_response['timestamp']
		if time.time()-timestamp > self.expiry_time:
			self.cache.pop(query)
			return(-1)
		return query_response['query_response']
	#query_response is a string
	def put(self,query,query_response):
		self.cache[query] = {
			'query_response' : query_response,
			'timestamp' : time.time(),
		}
		if len(self.cache) > self.capacity:
			self.cache.popitem(last=False)
	def load_from_file(self,addr):
		b_file = open(addr,'rb')
		self.cache = pickle.load(b_file)
		b_file.close()

	def store_to_file(self,addr):
		f_out = open(addr,'wb')
		pickle.dump(self.cache,f_out)
		f_out.close()

	def clear_cache(self):
		self.cache = OrderedDict()