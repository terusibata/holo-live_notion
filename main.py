import datetime
import requests, bs4
import re
import youtube_dl
from datetime import timedelta


from notion.client import NotionClient
from apiclient.discovery import build#channel取得

client = NotionClient(token_v2="19fecbb34a67d835d7454c78fd81c5ef51dcef561b8dd6d4f72007a5a42c0815ba3871347fc8e9348cd1a268e2d5ac74e20053ae8a638472b935e911b865aad4a71fff91825dded4f36394f8f9b8")

page=client.get_block("https://www.notion.so/cd6e7355eb3647a1af83d8c7406a820d?v=d33f10e7a7284fd1b611b0a3bc128257")
url ="https://www.notion.so/cd6e7355eb3647a1af83d8c7406a820d?v=d33f10e7a7284fd1b611b0a3bc128257"
cv=client.get_collection_view(url)

res = requests.get('https://schedule.hololive.tv/simple/hololive')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
el = soup.find_all("a")

down_dir = "E:\\ダウンロード\\自動ダウンロード"
outtmpl ='%(timestamp)s%(title)s.%(ext)s'
ydl = youtube_dl.YoutubeDL({'outtmpl':down_dir + outtmpl})


# for elem in el:
#     youtube_list = elem.get('href')
#     res = re.match("https://www.youtube.com/watch", youtube_list)

#     if (res != None):
#         youtube_dl -o 'E:\ダウンロード\自動ダウンロード' 'youtube_list
#         print(youtube_list)

# import gspread 
# from oauth2client.service_account import ServiceAccountCredentials

# SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# SERVICE_ACCOUNT_FILE = 'holo-live-317113-18da3d3127da.json'

# credentials= ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE,SCOPES)

# gs =gspread.authorize(credentials)

# SPREADSHEET_KEY = '1e90RjeiOzrPHDh1umiTvEZCOZc7G2HArdn-5EIwAbok'
# worksheet = gs.open_by_key(SPREADSHEET_KEY).worksheet("シート1")

# worksheet.update_acell('A1','Hello')

# print(worksheet.acell("G2").value)

#
import json
import urllib.request

#


count=0
youtube_list_math=True
for elem in el:
    youtube_list = elem.get('href')
    res = re.match("https://www.youtube.com/watch", youtube_list)
    if (res != None):
      for row in cv.collection.get_rows():
         if youtube_list==row.Column:
            youtube_list_math=False
         #print(row.Column)

      print(youtube_list_math)
      if youtube_list_math:
         class Helper:
            def __init__(self):
               pass
            def id_from_url(self, url: str):
               return url.rsplit("/",1)[1]

         class YouTubeStatus:
            def __init__(self, url: str):
               self.json_url = urllib.request.urlopen(url)
               self.data2 = json.loads(self.json_url.read())
            def get_video_date(self):
               return self.data2["items"][0]["snippet"]["publishedAt"]

         class YouTubeStatus2:
            def __init__(self, url: str):
               self.json_url = urllib.request.urlopen(url)
               self.data = json.loads(self.json_url.read())
            def get_video_title(self):
               return self.data["items"][0]["snippet"]["title"]
         
         class YouTubeStatus3:
            def __init__(self, url: str):
               self.json_url = urllib.request.urlopen(url)
               self.data3 = json.loads(self.json_url.read())
            def get_video_channeltitle(self):
               return self.data3["items"][0]["snippet"]["channelTitle"]

         api_key ="AIzaSyBEYAMb1sGi_clxC7M0jJpSrx7nDrNxSz8"
         YT_URL_FULL=youtube_list
         YT_URL = YT_URL_FULL.replace('watch?v=','')

         helper = Helper()
         video_id = helper.id_from_url(YT_URL)
         url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
         main_data2 = YouTubeStatus2(url)
         main_data = YouTubeStatus(url)
         main_data3 = YouTubeStatus3(url)
         channeltitle = main_data3.get_video_channeltitle()
         title = main_data2.get_video_title()
         date = main_data.get_video_date()
         print(date)
        
         #概要欄
         # youtube = build('youtube', 'v3', developerKey='AIzaSyBEYAMb1sGi_clxC7M0jJpSrx7nDrNxSz8')
         # video_id = youtube_list

         # video_response = youtube.videos().list(
         #    part='snippet',
         #    id=video_id,
         # ).execute()
         # print(video_response)
         #

         #サムネ
         youtube_list_IMG=f"https://img.youtube.com/vi/{youtube_list.replace('https://www.youtube.com/watch?v=','')}/maxresdefault.jpg"
         #

         #ジャンル
         if 'cover' in title:
            tag="歌ってみた"
         elif 'Cover' in title:
            tag="歌ってみた"
         elif '歌ってみた' in title:
            tag="歌ってみた"
         elif 'オリジナル' in title:
            tag="オリジナルソング"
         else:
            tag="配信アーカイブ"
         #

         #内容タグ
         if title.find('【')>=0&title.find('】')>=0:
            search_tag_1=int(title.find('【'))+1
            search_tag_2=int(title.find('】'))
            title_tag=title[search_tag_1:search_tag_2]
            if title_tag=="":
               title_tag="その他"
         else:
            title_tag="その他"
         #

         date_full=(date.replace("-",""))[:8]
         #count+=1
         print(f"チャンネル名:{channeltitle}")
         print(f"タイトル:{title}")
         row = cv.collection.add_row()
         row.name = title
         row.channel=channeltitle
         row.title_tag=title_tag
         row.Tags=tag
         row.Column=youtube_list
         row.Date=datetime.date(int(date_full[:4]),int(date_full[4:6]),int(date_full[6:8]))
         row.IMG=youtube_list_IMG

      youtube_list_math=True




      # worksheet.update_acell(f'A{count}',youtube_list)
      #   with ydl:
      #      result = ydl.extract_info(
      #         youtube_list,
      #         download=True 
      #      ) 
      # print(count)
      # print(youtube_list)

# print("The old title is:",page.title)

# page.title="ホロジュール"



# from apiclient.discovery import build

# API_KEY = 'AIzaSyBEYAMb1sGi_clxC7M0jJpSrx7nDrNxSz8'
# YOUTUBE_API_SERVICE_NAME = 'youtube'
# YOUTUBE_API_VERSION = 'v3'
# CHANNEL_ID = 'UCvaTdHTWBGv3MKj3KVqJVCw'

# youtube = build(
#     YOUTUBE_API_SERVICE_NAME,
#     YOUTUBE_API_VERSION,
#     developerKey=API_KEY
# )

# response = youtube.search().list(
#     part = "snippet",
#     channelId = CHANNEL_ID,
#     maxResults = 5,
#     order = "date",
#     type ='video'
#     ).execute()

# for item in response.get("items", []):
#     print(item['snippet']['title'])


