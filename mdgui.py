import mdapi
import tkinter as tk
from tkinter import ttk

import io
from PIL import Image, ImageTk
import shutil
from time import sleep
import mp3play

from utils import format_number, date_dict, format_date, format_time

os = mdapi.os


# TODO: Fix button next (raise an exception, doesn't becaming disable)
# TODO: Add debug message if predownloaded video should be removed
# TODO: Don't remove predownloaded video if it has already downloaded

# TODO: Add showing tags from video and other services (musicbrainz)
# TODO: Fix players and progress bars (.after())

# ISSUE: Parallelism and player

class MusicDownloader:

    ELEMENTS = [
        'app',
        'app_2',
        'label_query',
        'entry_query',
        'button_search',
        'label_image',
        'label_title',
        'label_uploader',
        'label_views',
        'label_likes',
        'label_date',
        'button_play',
        'progress_bar',
        'label_remaining_time',
        'button_previous',
        'button_next',
        'button_download',
        'button_toqueue',
        'entry_directory',
        'entry_filename',
        'entry_database',
        'chbox_predownload',
        'chbox_database',
        'chbox_tags_from_video',
        'chbox_lyrics',
        'chbox_zipfile',
        'chbox_reserved',
        'button_expand',
        'button_expand_2',
        
        'label_tag_title',
        'entry_tag_title',
        'label_tag_artist',
        'entry_tag_artist',
        'label_tag_genre',
        'entry_tag_genre',
        'label_tag_from',
        'entry_tag_from',
        'label_tag_source',
        'entry_tag_source',
        'label_tag_year',
        'entry_tag_year',
        'label_tag_instrument',
        'entry_tag_instrument',
        'label_tag_mood',
        'entry_tag_mood',
        'label_tag_mark',
        'entry_tag_mark'
        ]#,

    TAG_ELEMENTS = [
        'label_tag_title',
        'entry_tag_title'
        'label_tag_artist',
        'entry_tag_artist',
        'label_tag_genre',
        'entry_tag_genre',
        'label_tag_from',
        'entry_tag_from',
        'label_tag_source',
        'entry_tag_source',
        'label_tag_year',
        'entry_tag_year',
        'label_tag_instrument',
        'entry_tag_instrument',
        'label_tag_mood',
        'entry_tag_mood',
        'label_tag_mark',
        'entry_tag_mark'
        ]

    def __init__ (self, api, layout, localization, theme, settings):
        self.layout = layout
        self.loc = localization
        self.theme = theme
        self.settings = settings

        self.expanded = False

        appearence = {el: {} for el in self.ELEMENTS}

        # Merge all options of elements (in localization and theme)
        # to one dict (appearence)
        for el in self.ELEMENTS:
            if el in localization:
                for field in localization[el]:
                    print(el, field)
                    appearence[el][field] = localization[el][field]
            if el in theme:
                for field in theme[el]:
                    appearence[el][field] = theme[el][field]

        '''# Set bg of all elements to app bg, unless otherwise specified
        for el in appearence:
            if not 'bg' in appearence[el]:
                if 'bg' in appearence['app']:
                    appearence[el]['bg'] = appearence['app']['bg']'''

        self.appearence = appearence
        
        self.configure()

        self.api = api

        self.downloaded_videos = []
        self.accepted_videos = []



    def configure (self):
        self.app = tk.Tk()
        app_configs = self.appearence['app']
        app_measure = self.layout['app']
        
        if 'title' in app_configs:
            self.app.title(self.appearence['app']['title'])
        if 'bg' in app_configs:
            self.app.configure(bg=app_configs['bg'])
        if 'image' in app_configs:
            self.app.configure(image=app_configs['image'])
        if 'width' in app_measure and 'height' in app_measure:
            self._set_geometry(app_measure['width'], app_measure['height'])
        if 'resizable_x' in app_measure:
            self.app.resizable(x=app_measure['resizable_x'])
        if 'resizable_y' in app_measure:
            self.app.resizable(y=app_measure['resizable_y'])

        self.app.protocol('WM_DELETE_WINDOW', self.exit)

        root = self.app

        self.label_query = tk.Label(root, **self.appearence['label_query'])
        self.entry_query = tk.EntryWithPlaceholder(root, **self.appearence['entry_query'])
        self.button_search = tk.Button(root, **self.appearence['button_search'])
        self.button_search.configure(command=self.search)
        self.label_image = tk.Label(root, **self.appearence['label_image'])
        self.label_title = tk.Label(root, **self.appearence['label_title'])
        self.label_uploader = tk.Label(root, **self.appearence['label_uploader'])
        self.label_views = tk.Label(root, **self.appearence['label_views'])
        self.label_likes = tk.Label(root, **self.appearence['label_likes'])
        self.label_date = tk.Label(root, **self.appearence['label_date'])
        self.button_play = tk.Button(root, **self.appearence['button_play'])
        self.button_play.configure(command=self.play_song)
        self.progress_bar = ttk.Progressbar(root, **self.appearence['progress_bar'])
        self.label_remaining_time = tk.Label(root, **self.appearence['label_remaining_time'])
        self.button_previous = tk.Button(root, **self.appearence['button_previous'])
        self.button_previous.configure(command=self.previous, state='disabled')
        self.button_next = tk.Button(root, **self.appearence['button_next'])
        self.button_next.configure(command=self.next, state='disabled')
        self.button_download = tk.Button(root, **self.appearence['button_download'])
        self.button_download.configure(command=self.download)
        self.button_toqueue = tk.Button(root, **self.appearence['button_toqueue'])
        
        self.entry_directory = tk.Entry(root, **self.appearence['entry_directory'])
        self.entry_filename = tk.Entry(root, **self.appearence['entry_filename'])
        self.entry_database = tk.Entry(root, **self.appearence['entry_database'])
        self.chbox_predownload = tk.Checkbutton(root, **self.appearence['chbox_predownload'])
        self.chbox_database = tk.Checkbutton(root, **self.appearence['chbox_database'])
        self.chbox_tags_from_video = tk.Checkbutton(root, **self.appearence['chbox_tags_from_video'])
        self.chbox_lyrics = tk.Checkbutton(root, **self.appearence['chbox_lyrics'])
        self.chbox_zipfile = tk.Checkbutton(root, **self.appearence['chbox_zipfile'])
        self.chbox_reserved = tk.Checkbutton(root, **self.appearence['chbox_reserved'])
        self.button_expand = tk.Button(root, **self.appearence['button_expand'])
        self.button_expand.configure(command=self.expand)


        self.label_tag_title = tk.Label(root, **self.appearence['label_tag_title'])
        self.entry_tag_title = tk.Entry(root, **self.appearence['entry_tag_title'])
        self.label_tag_artist = tk.Label(root, **self.appearence['label_tag_artist'])
        self.entry_tag_artist = tk.Entry(root, **self.appearence['entry_tag_artist'])
        self.label_tag_genre = tk.Label(root, **self.appearence['label_tag_genre'])
        self.entry_tag_genre = tk.Entry(root, **self.appearence['entry_tag_genre'])
        self.label_tag_from = tk.Label(root, **self.appearence['label_tag_from'])
        self.entry_tag_from = tk.Entry(root, **self.appearence['entry_tag_from'])
        self.label_tag_source = tk.Label(root, **self.appearence['label_tag_source'])
        self.entry_tag_source = tk.Entry(root, **self.appearence['entry_tag_source'])
        self.label_tag_year = tk.Label(root, **self.appearence['label_tag_year'])
        self.entry_tag_year = tk.Entry(root, **self.appearence['entry_tag_year'])
        self.label_tag_instrument = tk.Label(root, **self.appearence['label_tag_instrument'])
        self.entry_tag_instrument = tk.Entry(root, **self.appearence['entry_tag_instrument'])
        self.label_tag_mood = tk.Label(root, **self.appearence['label_tag_mood'])
        self.entry_tag_mood = tk.Entry(root, **self.appearence['entry_tag_mood'])
        self.label_tag_mark = tk.Label(root, **self.appearence['label_tag_mark'])
        self.entry_tag_mark = tk.Entry(root, **self.appearence['entry_tag_mark'])

        self.entry_query.bind('<Return>', self.search)

        

    def search (self, *args):
        self.progress_bar.configure(mode='indeterminate', value=50)
        self._clear_cache()
        
        query = self.entry_query.get()
        self.api.search(query)
        self.downloaded_videos = []
        self.accepted_videos = []
        self._wait_for_downloading_webpage()
        
        results = self.api.get_search_results()
        self.last_results = results
        self.current_video = 0
        self.button_previous.configure(state='disabled')
        self.button_next.configure(state='normal')

        self._show_current_video()

        self.downloaded_videos.append(0)
        # or not append if not predownload

        # turn state of button and progressbar when video downloaded
        # and download track to player
        self.button_download.configure(state='normal')



    def get_results (self, query):
        ...

    def previous (self, *args):
        if not self.current_video <= 0:
            self.current_video -= 1
            self._show_current_video()
            self.button_play.configure(text='P', command=self.play_song)
            if self.current_video in self.accepted_videos:
                self.button_download.configure(state='disable')
            else:
                self.button_download.configure(state='normal')
        if self.current_video == 0:
            self.button_previous.configure(state='disabled')
        if self.current_video < len(self.last_results['entries'])-1:
            self.button_next.configure(state='normal')
        

    def next (self, *args):
        if not self.current_video >= len(self.last_results['entries'])-1:
            self.current_video += 1
            self._show_current_video()
            self.button_play.configure(text='P', command=self.play_song)
            if self.current_video in self.accepted_videos:
                self.button_download.configure(state='disable')
            else:
                self.button_download.configure(state='normal')
        if self.current_video == len(self.last_results['entries'])-1:
            self.button_next.configure(state='disabled')
        if self.current_video > 0:
            self.button_previous.configure(state='normal')
        

    def download (self, *args):
        # it doesn't mean download, name of function by the text of button
        temp_dir = self.settings['temp_dir']
        if self.api.is_downloading_video():
            self._wait_for_downloading_video()
        if not self.current_video in self.downloaded_videos:
            self._download_current_video()
            self._wait_for_downloading_video()
        self._wait_for_downloading_video()
        
        video = self.last_results['entries'][self.current_video]
        video_id = video['id']
        pathfrom = rf"{temp_dir}\{video_id}.mp3"
        # or may be not .mp3?
        dload_dir = self.settings['path']
        if 'track' in video and 'artist' in video:
            filename = self.settings['filename'].format(**video)
        else:
            filename = video['title']
        pathto = rf"{dload_dir}\{filename}"
        self.accepted_videos.append(self.current_video)
        self.button_download.configure(state='disabled')
        shutil.move(pathfrom, pathto)
        

    def to_queue (self):
        ...

    def play_song (self):
        temp_dir = self.settings['temp_dir']
        if self.api.is_downloading_video():
            self._wait_for_downloading_video()
        if not self.current_video in self.downloaded_videos:
            self._download_current_video()
            self._wait_for_downloading_video()
        song_id = self.last_results['entries'][self.current_video]['id']
        filename = rf'{temp_dir}\{song_id}.mp3'
        # or may be not .mp3?
        self.song = mp3play.load(filename)
        self.song.play()

        self.button_play.configure(text='||', command=self.pause_song)

    def pause_song (self):
        self.song.pause()
        self.button_play.configure(text='//', command=self.unpause_song)

    def unpause_song (self):
        self.song.unpause()
        self.button_play.configure(text='||', command=self.pause_song)

    def expand (self, *args):
        app_2 = self.layout['app_2']
        self._set_geometry(app_2['width'], app_2['height'])
        self.button_expand.configure(text=self.appearence['button_expand_2']['text'],
                                     command=self.reduce)
        

    def reduce (self, *args):
        app_1 = self.layout['app']
        self._set_geometry(app_1['width'], app_1['height'])
        self.button_expand.configure(text=self.appearence['button_expand']['text'],
                                     command=self.expand)

        

    def run (self):
        self.label_query.place(**self.layout['label_query'])
        self.entry_query.place(**self.layout['entry_query'])
        self.button_search.place(**self.layout['button_search'])
        self.label_image.place(**self.layout['label_image'])
        self.label_title.place(**self.layout['label_title'])
        self.label_uploader.place(**self.layout['label_uploader'])
        self.label_views.place(**self.layout['label_views'])
        self.label_likes.place(**self.layout['label_likes'])
        self.label_date.place(**self.layout['label_date'])
        self.button_play.place(**self.layout['button_play'])
        self.progress_bar.place(**self.layout['progress_bar'])
        self.label_remaining_time.place(**self.layout['label_remaining_time'])
        self.button_previous.place(**self.layout['button_previous'])
        self.button_next.place(**self.layout['button_next'])
        self.button_download.place(**self.layout['button_download'])
        self.button_toqueue.place(**self.layout['button_toqueue'])
        self.entry_directory.place(**self.layout['entry_directory'])
        self.entry_filename.place(**self.layout['entry_filename'])
        self.entry_database.place(**self.layout['entry_database'])
        self.chbox_predownload.place(**self.layout['chbox_predownload'])
        self.chbox_database.place(**self.layout['chbox_database'])
        self.chbox_tags_from_video.place(**self.layout['chbox_tags_from_video'])
        self.chbox_lyrics.place(**self.layout['chbox_lyrics'])
        self.chbox_zipfile.place(**self.layout['chbox_zipfile'])
        #self.chbox_reserved.place(**self.layout['chbox_reserved'])
        self.button_expand.place(**self.layout['button_expand'])


        self.label_tag_title.place(**self.layout['label_tag_title'])
        self.entry_tag_title.place(**self.layout['entry_tag_title'])
        self.label_tag_artist.place(**self.layout['label_tag_artist'])
        self.entry_tag_artist.place(**self.layout['entry_tag_artist'])
        self.label_tag_genre.place(**self.layout['label_tag_genre'])
        self.entry_tag_genre.place(**self.layout['entry_tag_genre'])
        self.label_tag_from.place(**self.layout['label_tag_from'])
        self.entry_tag_from.place(**self.layout['entry_tag_from'])
        self.label_tag_source.place(**self.layout['label_tag_source'])
        self.entry_tag_source.place(**self.layout['entry_tag_source'])
        self.label_tag_year.place(**self.layout['label_tag_year'])
        self.entry_tag_year.place(**self.layout['entry_tag_year'])
        self.label_tag_instrument.place(**self.layout['label_tag_instrument'])
        self.entry_tag_instrument.place(**self.layout['entry_tag_instrument'])
        self.label_tag_mood.place(**self.layout['label_tag_mood'])
        self.entry_tag_mood.place(**self.layout['entry_tag_mood'])
        self.label_tag_mark.place(**self.layout['label_tag_mark'])
        self.entry_tag_mark.place(**self.layout['entry_tag_mark'])

        self.app.mainloop()


    def exit (self, *args):
        self._clear_cache()
        self.app.destroy()


        
    def _set_geometry (self, width, height):
        self.app.geometry(f'{width}x{height}')


    @staticmethod
    def _format_video_info (video):
        
        img_file = io.BytesIO(video['image'])
        img = Image.open(img_file)
        image = ImageTk.PhotoImage(img)
        # to test transfer data parameter
        
        title = video['title']
        uploader = video['uploader']
        views = format_number(video['view_count'], 5)
        likes = format_number(video['like_count'], 5)
        date = format_date(date_dict(video['upload_date']))
        duration = format_time(video['duration'])
        
        return {'image': image,
                'title': title,
                'uploader': uploader,
                'views': views,
                'likes': likes,
                'date': date,
                'duration': duration}
    


    def _set_preview (self, image, title,
                      uploader, views, likes,
                      date, duration):
        
        self.label_image.current_image = image
        self.label_image.configure(image=self.label_image.current_image)

        self.label_title.configure(text=title)
        self.label_uploader.configure(text=uploader)
        self.label_views.configure(text=views)
        self.label_likes.configure(text=likes)
        self.label_date.configure(text=date)
        self.label_remaining_time.configure(text=duration)



    def _show_current_video (self):
        video = self.last_results['entries'][self.current_video]

        self._set_preview(**self._format_video_info(video))


    def _wait_for_downloading_webpage (self):
        if self.api.is_downloading_webpage():
            self.progress_bar.configure(mode='indeterminate')
            while self.api.is_downloading_webpage():
                self.progress_bar.step(5)
                self.progress_bar.update_idletasks()
                sleep(0.1)
            self.progress_bar.configure(mode='determinate')


    def _wait_for_downloading_video (self):
        if self.api.is_downloading_video():
            self.progress_bar.configure(mode='indeterminate')
            while self.api.is_downloading_video():
                self.progress_bar.step(5)
                self.progress_bar.update_idletasks()
                sleep(0.1)
            #sleep(5) # something going wrong if not sleep
            # may be because ffmpeg converting not _is_downloading
            self.progress_bar.configure(mode='determinate')

    def _download_current_video (self):
        video_url = self.last_results['entries'][self.current_video]['webpage_url']
        self.api.download(video_url)
        self.downloaded_videos.append(self.current_video)
        print(f'video {self.current_video} was added to downloaded')
        print(self.downloaded_videos)

    def _clear_cache (self):
        temp_dir = self.settings['temp_dir']
        for video_num in self.downloaded_videos:
            video_id = self.last_results['entries'][video_num]['id']
            filepath = rf'{temp_dir}\{video_id}.mp3'
            # or may be not .mp3?
            print(filepath, 'will be removed!')
            input()
            os.remove(filepath)




if __name__ == '__main__':
    musicdownloader = MusicDownloader(
        layout_ex,
        localization_ex,
        theme_ex,
        settings_ex)
    musicdownloader.run()



# CODE GENERATORS
'''
for el in TAG_ELEMENTS:
	if el.startswith('label'):
	      x = x1
	      s = "\n        },\n"
	      y += 35
	else:
	      x = x2
	      s = ",\n        'width': 120,\n        'height': 30\n        },\n"
	      y += 25
	print(f"    '{el}': {{")
	print(f"        'x': {x},")
	print(f"        'y': {y}", end='')
	print(s)

'''
