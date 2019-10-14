from bs4 import BeautifulSoup
import audiojack
from threading import Thread


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
            res.append(video)
        return res

    def set_param (self, name, value):
        ydl.params[name] = value

    def get_search_results (self, query, download=False, download_first=True, limit=3):
        query = query.replace(' ', '+')
        url = 'http://youtube.com/results?search_query=' + query
        info = ydl.extract_info(url, download=download, limit=limit)
        self.download(info['entries'][0]['webpage_url'])
        res = self._add_images(info['entries'])
        return res

    def get_lyrics (self, song_title, song_artist):
        artist = song_artist.lower()
        title = song_title.lower()
        artist = artist.replace(' ', '')
        title = title.replace(' ', '')

        url = "http://azlyrics.com/lyrics/"+artist+"/"+title+".html"
        print(url)

        content = urllib.request.urlopen(url).read()
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
        thr = Thread(target=ydl.download, args=(video_urls,))
        thr.start()
        
        
