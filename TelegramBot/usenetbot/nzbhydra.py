from TelegramBot import NZBHYDRA_ENDPOINT, NZBHYDRA_STATS_ENDPOINT 
from TelegramBot.helpers.functions import get_readable_bytes

import xml.etree.ElementTree as ET
import requests
import json
import html 

    
class NzbHydra:	
	def __init__(self):		
		self.NZBHYDRA_ENDPOINT = NZBHYDRA_ENDPOINT 
		self.NZBHYDRA_STATS_ENDPOINT = NZBHYDRA_STATS_ENDPOINT
		self.client = requests.Session()
		
	def parse_xml(self, response, query):
	    root = ET.fromstring(response)

	    channel = root.find('channel')
	    search_result = [
	       [item.find('title').text,
           get_readable_bytes(int(item.find('size').text)) if item.find('size') is not None else '',
           item.find('guid').text]
           for item in channel.findall('item')]
           
	    title = f"Search Results For: {query}\n\n"
	    message = ""
	    for index, result in enumerate(search_result):
	    	message += f"Title : {result[0]}\n"
	    	message += f"Size: {result[1]}\n"
	    	message += f"ID: {result[2]}\n\n"
	    	if index == 100: break
	    		    
	    if message:
	    	message = html.escape(message)
	    	html_content = title + message
	    	return html_content	    		
	    return None		          	

	def query_search(self, query):
		response = self.client.get(self.NZBHYDRA_ENDPOINT, params={"t":"search", "q":query})
		return self.parse_xml(response.text, query)
		
	def movie_search(self, query):
		response = self.client.get(self.NZBHYDRA_ENDPOINT, params={"t":"movie", "q":query})
		return self.parse_xml(response.text,  query)
		
	def series_search(self, query):
		response = self.client.get(self.NZBHYDRA_ENDPOINT, params={"t":"tvsearch", "q":query})
		return self.parse_xml(response.text,  query)
			
	def imdb_movie_search(self, imdbid):
		response = self.client.get(self.NZBHYDRA_ENDPOINT, params={"t":"movie", "imdbid":imdbid})
		return self.parse_xml(response.text,  imdbid)
		
	def imdb_series_search(self, imdbid):
		response = self.client.get(self.NZBHYDRA_ENDPOINT, params={"t":"tvsearch", "imdbid":imdbid})
		return self.parse_xml(response.text,  imdbid)
						
	def list_indexers(self):
		response = self.client.get(self.NZBHYDRA_STATS_ENDPOINT)
		indexersDetail = response.json()["indexerApiAccessStats"]
		indexers_list = [indexersDetail[x]["indexerName"] for x in range(len(indexersDetail))]
		if not indexers_list: return None
		
		message= "List Of Indexers -\n\n"
		for indexer in indexers_list: message += f"* {indexer}\n"
		return message
