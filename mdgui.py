import mdapi
import mtkinter as tk

import io
from PIL import Image, ImageTk
import shutil
from time import sleep
import mp3play
import eyed3
import json

from utils import format_number, date_dict, format_date, \
     format_time, dict_without_keys

os = mdapi.os


# TODO: Add global MusicDownloader variable containt tags of videos
# TODO: Fix errors if get_tags return None

# TODO: Add debug message if predownloaded video should be removed
# TODO: Don't remove predownloaded video if it has already downloaded

# TODO: Fix players and progress bars (.after())
# TODO: Add main cycle

# ISSUE: Error when searching new while downloading old: raise
# Exception in downloading thread

# [F?] ISSUE: Parallelism and player

# MAYBE: last.fm api implement 

# keys that mustn't get into a widget's configure call
SERVICE_KEYS = ('class', 'events', 'command')

# keys of languages of program and sites
LANGUAGE_KEYS = ('en', 'ru', 'uk')
SITE_KEYS = ('youtube', 'musicbr', 'soundcl', 'lastdfm')

# classes using bg and fg params with causes errors
NOBGFG_CLASSES = ('Spinbox', 'Combobox', 'Progressbar')


class MusicDownloaderGUI:
    
    def __init__ (self, api, layout, localization, theme, settings):
        self.settings = settings

        self.expanded = False
        self.settings_is_open = False
        self.current_video = None

        app_widgets = layout['app_widgets']
        tag_widgets = layout['tag_widgets']
        set_widgets = layout['set_widgets']

        app_widgets_configs = {element_id: {} for element_id in layout['app_widgets']}
        tag_widgets_configs = {element_id: {} for element_id in layout['tag_widgets']}
        set_widgets_configs = {element_id: {} for element_id in layout['set_widgets']}

        for option_source in (localization, theme):
            for element_id in option_source['app_widgets']:
                for option_key in option_source['app_widgets'][element_id]:
                    app_widgets_configs[element_id][option_key] \
                        = option_source['app_widgets'][element_id][option_key]

            for element_id in option_source['tag_widgets']:
                for option_key in option_source['tag_widgets'][element_id]:
                    tag_widgets_configs[element_id][option_key] \
                        = option_source['tag_widgets'][element_id][option_key]

            for element_id in option_source['set_widgets']:
                for option_key in option_source['set_widgets'][element_id]:
                    set_widgets_configs[element_id][option_key] \
                        = option_source['set_widgets'][element_id][option_key]

        self.app_widgets = app_widgets
        self.tag_widgets = tag_widgets
        self.set_widgets = set_widgets

        self.app_widgets_configs = app_widgets_configs
        self.tag_widgets_configs = tag_widgets_configs
        self.set_widgets_configs = set_widgets_configs
                    
        
        self.configure()

        self.api = api

        self.downloaded_videos = []
        self.accepted_videos = []
        #self.tags_found_videos = []





    def configure (self):

        elements_default_bg = None
        elements_default_fg = None
        
        app = tk.Tk()
        app_measure = self.app_widgets['app']
        app_configs = self.app_widgets_configs['app']
        
        if 'title' in app_configs:
            app.title(app_configs['title'])
        if 'bg' in app_configs:
            app.configure(bg=app_configs['bg'])
        if 'image' in app_configs:
            app.configure(image=app_configs['image'])
        if 'width' in app_measure and 'height' in app_measure:
            app.geometry(f"{app_measure['width']}x{app_measure['height']}")
        if 'resizable_x' in app_measure:
            app.resizable(x=app_measure['resizable_x'])
        if 'resizable_y' in app_measure:
            app.resizable(y=app_measure['resizable_y'])
        if 'elements_default_bg' in app_configs:
            elements_default_bg = app_configs['elements_default_bg']
        if 'elements_default_fg' in app_configs:
            elements_default_fg = app_configs['elements_default_fg']

        for element_id in self.app_widgets:
            configs = self.app_widgets[element_id]
            if not 'class' in configs:
                continue
            init_configs = self.app_widgets_configs[element_id]
            widget_class_name = configs['class']

            if not 'bg' in init_configs:
                if elements_default_bg is not None:
                    if not widget_class_name in NOBGFG_CLASSES:
                        init_configs['bg'] = elements_default_bg
            if not 'fg' in init_configs:
                if elements_default_fg is not None:
                    if not widget_class_name in NOBGFG_CLASSES:
                        init_configs['fg'] = elements_default_fg
            
            widget_class = getattr(tk, widget_class_name)
            widget = widget_class(app, **init_configs)
            
            if 'command' in configs:
                func = getattr(self, configs['command'])
                widget.configure(command=func)
                print('assigned func', func, 'to widget', configs)

            if 'events' in configs:
                for event in configs['events']:
                    func = getattr(self, configs['events'][event])
                    widget.bind(event, func)
                
            setattr(self, element_id, widget)

        for element_id in self.tag_widgets:
            configs = self.tag_widgets[element_id]
            if not 'class' in configs:
                continue
            init_configs = self.tag_widgets_configs[element_id]
            widget_class_name = configs['class']

            if not 'bg' in init_configs:
                if elements_default_bg is not None:
                    if not widget_class_name in NOBGFG_CLASSES:
                        init_configs['bg'] = elements_default_bg
            if not 'fg' in init_configs:
                if elements_default_fg is not None:
                    if not widget_class_name in NOBGFG_CLASSES:
                        init_configs['fg'] = elements_default_fg
            
            widget_class = getattr(tk, widget_class_name)
            widget = widget_class(app, **init_configs)
            
            if 'command' in configs:
                func = getattr(self, configs['command'])
                widget.configure(command=func)

            if 'events' in configs:
                for event in configs['events']:
                    func = getattr(self, configs['events'][event])
                    widget.bind(event, func)
                
            setattr(self, element_id, widget)

        self.app = app

        



    def search (self, *args):
        self.progress_bar.configure(mode='indeterminate', value=50)
        self._clear_cache()
        
        query = self.entry_query.get()
        self.api.search(query)
        
        self.downloaded_videos = []
        self.accepted_videos = []
        self.tags_found_videos = []
        
        self._wait_for_downloading_webpage()
        
        results = self.api.get_search_results()
        self.last_results = results
        self.tags = [{} for i in range(3)]
        self.current_video = 0
        self.button_previous.configure(state='disabled')
        self.button_next.configure(state='normal')

        self._show_current_video()

        self.downloaded_videos.append(0)
        # or not append if not predownload

        # turn state of button and progressbar when video downloaded
        # and download track to player
        self.button_download.configure(state='normal')
        self.button_play.configure(text='►', command=self.play_song)

        if self.expanded:
            self._set_tags()
            self._configure_tags_entries()



    def get_results (self, query):
        ...

    def previous (self, *args):
        if not self.current_video <= 0:
            self.current_video -= 1
            self._show_current_video()
            self.button_play.configure(text='►', command=self.play_song)
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
            self.button_play.configure(text='►', command=self.play_song)
            if self.current_video in self.accepted_videos:
                self.button_download.configure(state='disable')
            else:
                self.button_download.configure(state='normal')
        if self.current_video == len(self.last_results['entries'])-1:
            self.button_next.configure(state='disabled')
        if self.current_video > 0:
            self.button_previous.configure(state='normal')
        

    def download (self, *args):
        # it doesn't mean download, just name of function by the text of button
        temp_dir = self.settings['temp_dir']
        if self.api.is_downloading_video():
            self._wait_for_downloading_video()
        if not self.current_video in self.downloaded_videos:
            self._download_current_video()
            self._wait_for_downloading_video()
        self._wait_for_downloading_video()
        
        video = self._get_current_video_info()
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

        self.song.stop()
        self.song.close()

        tags = self._get_current_video_tags()
        file = eyed3.load(pathto)
        if 'title' in tags: file.tag.title = tags['title']
        if 'artist' in tags: file.tag.artist = tags['artist'] 
        if 'album' in tags: file.tag.album = tags['album']
        if 'lyrics' in tags: file.tag.lyrics.set(tags['lyrics'])
        file.tag.save()
        

    def to_queue (self):
        ...

    def play_song (self):
        temp_dir = self.settings['temp_directory']
        if self.api.is_downloading_video():
            self._wait_for_downloading_video()
        if not self.current_video in self.downloaded_videos:
            self._download_current_video()
            self._wait_for_downloading_video()
        song_info = self._get_current_video_info()
        song_id = song_info['id']
        filename = rf'{temp_dir}\{song_id}.mp3'
        # or may be not .mp3?
        self.song = mp3play.load(filename)
        self.song.play()

        self.button_play.configure(text='||', command=self.pause_song)

        # <CHANGE ALL CHANGE ALL>
        #
        
        track = song_info['track'] if 'track' in song_info else None
        artist = song_info['artist'] if 'artist' in song_info else None

        #if track and artist:
        lyrics = self.api.get_lyrics(track, artist)
        print(' = LYRICS = ')
        print(lyrics)
        self._get_current_video_tags()['lyrics'] = lyrics

        #
        # </CHANGE ALL CHANGE ALL>

    def pause_song (self):
        self.song.pause()
        self.button_play.configure(text='//', command=self.unpause_song)

    def unpause_song (self):
        self.song.unpause()
        self.button_play.configure(text='||', command=self.pause_song)

    def expand (self, *args):
        app = self.tag_widgets['app']
        self._set_geometry(app['width'], app['height'])
        self.button_expand.configure(text=self.tag_widgets_configs['button_expand']['text'],
                                     command=self.reduce)
        self.expanded = True
        if self.current_video is not None:
            self._set_tags()
            self._configure_tags_entries()
        

    def reduce (self, *args):
        app = self.app_widgets['app']
        self._set_geometry(app['width'], app['height'])
        self.button_expand.configure(text=self.app_widgets_configs['button_expand']['text'],
                                     command=self.expand)
        self.expanded = False


    def open_settings (self):

        elements_default_bg = None
        elements_default_fg = None
        
        if self.settings_is_open:
            self.settings_window.focus_force()
            return
        
        print("="*60)
        print("==================== SETTINGS DEBUG =====================")
        print("="*60)

        settings_window_measure = self.set_widgets['settings_window']
        settings_window_configs = self.set_widgets_configs['settings_window']
        
        settings_window = tk.Toplevel()
        self.settings_window = settings_window
        self.settings_is_open = True

        if 'title' in settings_window_configs:
            settings_window.title(settings_window_configs['title'])
        if 'bg' in settings_window_configs:
            settings_window.configure(bg=settings_window_configs['bg'])
        if 'image' in settings_window_configs:
            settings_window.configure(image=settings_window_configs['image'])
        if 'width' in settings_window_measure and 'height' in settings_window_measure:
            settings_window.geometry(
                f"{settings_window_measure['width']}x{settings_window_measure['height']}"
                )
        if 'resizable_x' in settings_window_measure:
            settings_window.resizable(x=settings_window_measure['resizable_x'])
        if 'resizable_y' in settings_window_measure:
            settings_window.resizable(y=settings_window_measure['resizable_y'])
        
        for element_id in self.set_widgets:
            configs = self.set_widgets[element_id]
            if not 'class' in configs:
                continue
            init_configs = self.set_widgets_configs[element_id]
            widget_class_name = configs['class']

            if not 'bg' in init_configs:
                if elements_default_bg is not None:
                    if not widget_class_name in NOBGFG_CLASSES:
                        init_configs['bg'] = elements_default_bg
            if not 'fg' in init_configs:
                if elements_default_fg is not None:
                    if not widget_class_name in NOBGFG_CLASSES:
                        init_configs['fg'] = elements_default_fg
                        
            widget_class = getattr(tk, widget_class_name)
            widget = widget_class(settings_window, **init_configs)
            
            if 'command' in configs:
                func = getattr(self, configs['command'])
                widget.configure(command=func)
                
            setattr(self, element_id, widget)

        for element_id in self.set_widgets:
            if not 'class' in self.set_widgets[element_id]:
                continue
            widget = getattr(self, element_id)
            configs = dict_without_keys(self.set_widgets[element_id], SERVICE_KEYS)
            widget.place(**configs)

        self._set_settings(self.settings)


    def apply_settings (self):
        settings = self._get_settings()
        self._save_settings(settings)
        self.settings_window.destroy()
        self.settings_is_open = False

    def cancel_settings (self):
        self.settings_window.destroy()
        self.settings_is_open = False

    def close_settings (self):
        settings = self._get_settings()
        if settings != self.settings:
            # make askyesno
            if yes:
                self.apply_settings()
            else:
                self.cancel_settings()

    def run (self):
        for element_id in self.app_widgets:
            if not 'class' in self.app_widgets[element_id]:
                continue
            widget = getattr(self, element_id)
            configs = dict_without_keys(self.app_widgets[element_id], SERVICE_KEYS)
            widget.place(**configs)

        for element_id in self.tag_widgets:
            if not 'class' in self.tag_widgets[element_id]:
                continue
            widget = getattr(self, element_id)
            configs = dict_without_keys(self.tag_widgets[element_id], SERVICE_KEYS)
            widget.place(**configs)

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


    def _get_current_video_info (self):
        return self.last_results['entries'][self.current_video]


    def _get_current_video_tags (self):
        return self.tags[self.current_video]
    


    def _set_preview (self, image, title,
                      uploader, views, likes,
                      date, duration):
        print('_set_preview', title)
        
        self.label_image.current_image = image
        self.label_image.configure(image=self.label_image.current_image)

        self._set_title(title, 260)
        self.label_uploader.configure(text=uploader)
        self.label_views.configure(text=views)
        self.label_likes.configure(text=likes)
        self.label_date.configure(text=date)
        self.label_remaining_time.configure(text=duration)



    def _show_current_video (self):
        video = self._get_current_video_info()
        print('_show_current_video', video['title'])

        self._set_preview(**self._format_video_info(video))


    def _get_settings (self):
        if self.settings_is_open:
            settings = {} 
            settings['bitrate'] = self.s_spinner_bitrate.get()
            settings['limit'] = self.s_entry_limit.get()
            settings['predownload'] = self.s_chbox_predownload.get()
            settings['temp_directory'] = self.s_entry_temp_directory.get()
            settings['last_options'] = self.s_chbox_last_options.get()
            settings['default_filename'] = self.s_entry_default_filename.get()
            settings['default_directory'] = self.s_entry_default_directory.get()
            settings['connect_to_database'] = self.s_chbox_connect_to_database.get()
            settings['database_location'] = self.s_entry_database_location.get()
            settings['parallel_threads'] = self.s_spinner_parallel_threads.get()
            settings['fps'] = self.s_spinner_fps.get()
            settings['layout'] = self.s_list_layout.get()
            settings['theme'] = self.s_list_theme.get()
            lang_values = self.s_list_language['values']
            lang_index = lang_values.index(self.s_list_language.get())
            settings['language_key'] = LANGUAGE_KEYS[lang_index]
            settings['language'] = self.s_list_language.get()
            site_values = self.s_list_first_tag_priority['values']
            site_index = site_values.index(self.s_list_first_tag_priority.get())
            settings['first_tag_priority_key'] = SITE_KEYS[site_index]
            settings['first_tag_priority'] = self.s_list_first_tag_priority.get()
            site_values = self.s_list_second_tag_priority['values']
            site_index = site_values.index(self.s_list_second_tag_priority.get())
            settings['second_tag_priority_key'] = SITE_KEYS[site_index]
            settings['second_tag_priority'] = self.s_list_second_tag_priority.get()
            settings['zip_files'] = self.s_chbox_zip_files.get()
            settings['zip_algorithm'] = self.s_list_zip_algorithm.get()
            return settings
        else:
            return self.settings

    def _set_settings (self, settings):
        if self.settings_is_open:
            self.s_spinner_bitrate.set(settings['bitrate'])
            self.s_entry_limit.delete(0, 'end')
            self.s_entry_limit.insert(0, settings['limit'])
            self.s_chbox_predownload.set(settings['predownload'])
            self.s_entry_temp_directory.delete(0, 'end')
            self.s_entry_temp_directory.insert(0, settings['temp_directory'])
            self.s_chbox_last_options.set(settings['last_options'])
            self.s_entry_default_filename.delete(0, 'end')
            self.s_entry_default_filename.insert(0, settings['default_filename'])
            self.s_entry_default_directory.delete(0, 'end')
            self.s_entry_default_directory.insert(0, settings['default_directory'])
            self.s_chbox_connect_to_database.set(settings['connect_to_database'])
            self.s_entry_database_location.delete(0, 'end')
            self.s_entry_database_location.insert(0, settings['database_location'])
            self.s_spinner_parallel_threads.set(settings['parallel_threads'])
            self.s_spinner_fps.set(settings['fps'])
            self.s_list_layout.set(settings['layout'])
            self.s_list_theme.set(settings['theme'])
            lang_index = LANGUAGE_KEYS.index(settings['language_key'])
            language = self.s_list_language['values'][lang_index]
            self.s_list_language.set(language)
            site_index = SITE_KEYS.index(settings['first_tag_priority_key'])
            site = self.s_list_first_tag_priority['values'][site_index]
            self.s_list_first_tag_priority.set(site)
            site_index = SITE_KEYS.index(settings['second_tag_priority_key'])
            site = self.s_list_second_tag_priority['values'][site_index]
            self.s_list_second_tag_priority.set(site)
            self.s_chbox_zip_files.set(settings['zip_files'])
            self.s_list_zip_algorithm.set(settings['zip_algorithm'])

    def _save_settings (self, settings):
        settings_file = open('settings_file', 'w')
        json.dump(settings, settings_file)


    def _find_tags (self, videoinfo=None):
        if videoinfo is None:
            #if self.current_video in self.tags_found_videos:
            if self.current_video in self.tags:
                return self._get_current_video_tags()
            
            videoinfo = self._get_current_video_info()
            
        tags = self.api.get_tags(videoinfo)
        
        print('\n= TAGS GOT! =\n')
        print(tags)
        return tags

    def _set_tags (self, tags=None, overwrite=False):
        if tags is None:
            tags = self._find_tags()

        current_tags = self._get_current_video_tags()
            
        if 'title' in tags:
            if overwrite or not 'title' in current_tags or not current_tags['title']:
                current_tags['title'] = tags['title']
        if 'artist' in tags:
            if overwrite or not 'artist' in current_tags or not current_tags['artist']:
                current_tags['artist'] = tags['artist']
        if 'album' in tags:
            if overwrite or not 'album' in current_tags or not current_tags['album']:
                current_tags['album'] = tags['album']
        print('o o o YEAR o o o')
        print('TAGS TAGS TAGS: ', tags)
        print('CURRENT TAGS CURRENT TAGS:', current_tags)
        print('year' in tags)
        print('year' in current_tags)
        print('overwrite', overwrite)
        if 'year' in current_tags: print(current_tags['year'])
        if 'year' in tags:
            if overwrite or not 'year' in current_tags or not current_tags['year']:
                current_tags['year'] = tags['year']
                

    def _configure_tags_entries (self, tags=None):
        if tags is None:
            tags = self._get_current_video_tags()

        self.entry_tag_title.delete(0, 'end')
        self.entry_tag_artist.delete(0, 'end')
        self.entry_tag_from.delete(0, 'end')
        self.entry_tag_year.delete(0, 'end')

        if 'title' in tags and tags['title']:
            self.entry_tag_title.insert(0, tags['title'])
        if 'artist' in tags and tags['artist']:
            self.entry_tag_artist.insert(0, tags['artist'])
        if 'album' in tags and tags['album']:
            self.entry_tag_from.insert(0, tags['album'])
        if 'year' in tags and tags['year']:
            self.entry_tag_year.insert(0, str(tags['year']))



    def _set_title (self, title, coef):
        '''
        fontsize = coef // len(title)
        font = self.appearence['label_title']['font']
        font[1] = fontsize
        for i, s in enumerate(title):
            if ord(s) > 64000:
                title = title[:i] + '?' + title[i+1:]
        self.label_title.configure(text=title, font=font)
        '''
        print('_set_title', title)

        font_params = self.app_widgets_configs['label_title']['font']
        print('FONT GOT: ', font_params)
        required_width = self.app_widgets['label_title']['width']
        # 10 because tkinter.Font won't take 'Roboto' as font family
        print('TODAYS REQUIRED WIDTH', required_width)
        font = tk.tkfont.Font(self.app, font_params)
        print('TKFONT ACTUAL:', font.actual())
        size = 2
        font.configure(size=size)
        while font.measure(title) < required_width:
            print('At size', size, 'width of text is', font.measure(title))
            size += 1
            if size > 18: break
            font.configure(size=size)
        print("= OPTIMAL FONT SIZE :", (size-1), "=")
        font_params[1] = size - 1
        print("FONT PARAMS:", font_params)
        self.label_title.configure(text=title, font=font_params)
        
        


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
        video_url = self._get_current_video_info()['webpage_url']
        self.api.download(video_url)
        self.downloaded_videos.append(self.current_video)
        print(f'video {self.current_video} was added to downloaded')
        print(self.downloaded_videos)

    def _clear_cache (self):
        temp_dir = self.settings['temp_directory']
        for video_num in self.downloaded_videos:
            video_id = self.last_results['entries'][video_num]['id']
            filepath = rf'{temp_dir}\{video_id}.mp3'
            # or may be not .mp3?
            print(filepath, 'will be removed!')
            os.remove(filepath)




if __name__ == '__main__':
    musicdownloader = MusicDownloader(
        layout_ex,
        localization_ex,
        theme_ex,
        settings_ex)
    musicdownloader.run()
