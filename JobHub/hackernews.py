import requests
import json
from datetime import datetime


class Story:
    def __init__(self, title, author, link, time):
        self.title = title
        self.author = author
        self.link = link
        self.time = time


story_list = []
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
response = requests.get(url)
r = response.json()
r_string = str(r)
data = json.loads(r_string)

item_url = ' https://hacker-news.firebaseio.com/v0/item/'
counter = 1
for article_id in data:
    story_request = requests.get(item_url + str(article_id) + '.json')  # Get the requested story by article id
    story_json = story_request.json()  # Convert to json object
    story_title = story_json.get('title')
    story_author = story_json.get('by')
    unix_time = int(story_json.get('time'))
    story_link = story_json.get('url')
    comments_count = story_json.get('descendants')
    #print(comments_count)
    if story_link is not None:  # We go with this logic operator, since we should only get 'url' if it's not null - "!="
        #print(str(counter) + '. Title: ' + story_title)
        #print('    Author: ' + story_author)
        #print('    Link: ' + story_link)
        time_stamp = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
        #print('    Time: ' + str(time_stamp))  # Look to convert Unix time to a standard date/ clock time
        story_list.append(Story(story_title, story_author, story_link, time_stamp))
        counter += 1
    #print()
    #print(story_list[0].title)
    if counter == 11:
        break