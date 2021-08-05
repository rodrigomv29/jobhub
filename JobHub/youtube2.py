api_key = "AIzaSyBeYT5lJU1-VrMMOxRFGc-W7IyuKPLpEqk"

from googleapiclient.discovery import build


class Video:
    def __init__(self, title, link):
        self.title = title
        self.link = link
        
youtube = build('youtube', 'v3', developerKey=api_key)

print(youtube)

req = youtube.search().list(q='job resume', part='snippet', type='video', maxResults = 1)

res = req.execute()

resume_list = []

#youtube_json = res.json()

#print(res)

#print(len(res['items']))

#print(res['items'][0]) # view all info of the first video returned

for item in res['items']:  # print all the titles(minor change to this in order to print the URL's of the videos in the web page)
    video_title = item['snippet']['title']
    video_url = "https://www.youtube.com/watch?v=" + item['id']['videoId']
    resume_list.append(Video(video_title, video_url))
    
    #print(item['snippet']['title'])
    #print("https://www.youtube.com/watch?v=" + item['id']['videoId'])
    #print(item['snippet']['description'])