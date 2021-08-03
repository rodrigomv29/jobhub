import requests
import json
from datetime import datetime


url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
response = requests.get(url)
print(response.status_code)
r = response.json()
r_string = str(r)
data = json.loads(r_string)

item_url = ' https://hacker-news.firebaseio.com/v0/item/'
counter = 1
for article_id in data:
  story_request = requests.get(item_url + str(article_id) + '.json') #Get the requested story by article id
  #print(story_request.status_code)
  story_json = story_request.json() #Convert to json object
  title = story_json.get('title')
  author = story_json.get('by')
  link = story_json.get('url')
  unix_time = int(story_json.get('time'))
  print(str(counter) + '. Title: ' + title)
  print('    Author: ' + author)
  if link != None: #We go with this logic operator, since we should only get 'url' if it's not null
    print('    Link: ' + link)
  time_stamp = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
  print('    Time: ' + str(time_stamp)) # Look to convert Unix time to a standard date/ clock time
  print()
  counter += 1
  if counter == 26:
    break