from bs4 import BeautifulSoup
import audiojack
from threading import Thread

os = audiojack.os
urllib = audiojack.urllib
youtube_dl = audiojack.youtube_dl

ydl_opts = {
    'format': 'bestaudio',
    'outtmpl': 'F:\\%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256'}]
    }



adj = audiojack.AudioJack()
ydl = youtube_dl.YoutubeDL(params=ydl_opts)

class MusicDownloaderAPI:
    
    def __init__ (self, settings):
        self.settings = settings
        #PARSE SETTINGS
        

    def _get_thumbnail_url (self, video_id):
        url = f"http://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
        return url

    def _get_image (self, url):
        img_req = urllib.request.urlopen(url)
        img = img_req.read()
        img_req.close()
        return img

    def _add_images (self, entries):
        res = []
        for video in entries:
            img_url = self._get_thumbnail_url(video['id'])
            img = self._get_image(img_url)
            video['image'] = img

    def _find_videos (self, query, download, download_first, limit):
        query = query.replace(' ', '+')
        url = 'http://youtube.com/results?search_query=' + query
        results = ydl.extract_info(url, download=download, limit=limit)
        self._add_images(results['entries'])
        self.last_results = results
        if download_first:
            self.download(results['entries'][0]['webpage_url'])
            

    def set_param (self, name, value):
        ydl.params[name] = value

    def search (self, query, download=False, download_first=True, limit=3):
        self.webpage_dwnd_thr = Thread(target=self._find_videos,
                                       args=(query, download, download_first, limit))
        self.webpage_dwnd_thr.start()

    def is_downloading_webpage (self):
        print('calling is_downloading_webpage')
        print('result:', self.webpage_dwnd_thr.isAlive())
        return self.webpage_dwnd_thr.isAlive()

    def get_search_results (self):
        return self.last_results

    def get_tags (self, video_info):
        try:
            tags = adj._get_metadata(adj._parse(video_info))[0]
        except:
            print("An exception occured while loading tags.")
            tags = {}

        print()
        
        if 'date' in tags and tags['date']:
            print(tags)
            tags['year'] = tags['date'][:4]
            print("tags['year'] = tags['date'][:4]", tags['year'])
        
        if 'track' in video_info and video_info['track']:
            tags['title'] = video_info['track']
        if 'artist' in video_info and video_info['artist']:
            tags['artist'] = video_info['artist']
        if 'album' in video_info and video_info['album']:
            tags['album'] = video_info['album']
        if 'release_year' in video_info and video_info['release_year']:
            tags['year'] = video_info['release_year']
        return tags

    def get_lyrics (self, song_title, song_artist):
        artist = song_artist.lower()
        title = song_title.lower()
        artist = artist.replace(' ', '')
        title = title.replace(' ', '')

        url = "http://azlyrics.com/lyrics/"+artist+"/"+title+".html"
        print(url)

        try:
            content = urllib.request.urlopen(url).read()
        except Exception:
            print("An error occured.")
            u = input()
            if u:
                content = urllib.request.urlopen(u).read()
            else:
                return "/NO LYRICS/"
            
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>','').replace('<br/>','').replace('</div>','').strip()
        return lyrics

    def download (self, video_urls):
        if not isinstance(video_urls, list):
            video_urls = [video_urls]
        self.video_dwnd_thr = Thread(target=ydl.download, args=(video_urls,))
        self.video_dwnd_thr.start()

    def is_downloading_video (self):
        return self.video_dwnd_thr.isAlive()
        
        
        
