api_key = "AIzaSyBeYT5lJU1-VrMMOxRFGc-W7IyuKPLpEqk"

from apiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=api_key)

print(youtube)

req = youtube.search().list(q='interview', part='snippet', type='video', maxResults = 50)

res = req.execute()

#print(res)

#print(len(res['items']))

#print(res['items'][0]) # view all info of the first video returned

for item in res['items']:          # print all the titles(minor change to this in order to print the URL's of the videos in the web page)
    print(item['snippet']['title'])
    print(item['id']['videoId'])
    print(item['snippet']['description'])

      