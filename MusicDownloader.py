# MusicDownloaderApp v0.6.7.1 by Namerif

import mdgui
import mdapi

import json
import sys
import os
# Checkbox tick isn't visible
# Default background option

# [F?] ISSUE: Searching second song, button play still pause

VERSION = '0.8.0'

print("=== MUSIC DOWNLOADER ===")
print('VERSION:', VERSION)
print("DEVELOPED BY NAMERIF")

current_file = sys.executable if getattr(sys, 'frozen', False) else __file__

local_dir = '\\'.join(current_file.split('\\')[:-1]) # (os.path.dirname)


settings_ex = {
    'bitrate': 96,
    'limit': 3,
    'predownload': True,
    'temp_directory': 'F:', #'C:\\Windows\\Temp',
    'last_options': True,
    'default_filename': '{artist} - {track}.mp3',
    'default_directory': 'F:\\Music\\Music',
    'connect_to_database': False,
    'database_location': 'NONE',
    'parallel_threads': 3,
    'fps': 2,
    'layout': 'Default',
    'language': 'English',
    'language_key': 'en',
    'theme': 'Default',
    'first_tag_priority': 'Youtube',
    'first_tag_priority_key': 'youtube',
    'second_tag_priority': 'MusicBrainzngs',
    'second_tag_priority_key': 'musicbr',
    'zip_files': False,
    'zip_algorithm': 'NONE'
    }


def local_open (localfilepath, mode, *args, **kwargs):
    file = open(local_dir + '\\' + localfilepath, mode, *args, **kwargs)
    return file

def load_settings ():
    settings_file = local_open('settings_file', 'r')
    settings = json.load(settings_file)
    return settings

def save_settings (settings):
    settings_file = local_open('settings_file', 'w')
    json.dump(settings, settings_file)
    

def load_layout (name):
    try:
        layout_file = local_open(rf'res\layouts\{name}.json', 'r')
    except FileNotFoundError:
        layout_file = local_open(r'res\layouts\default.json', 'r')
    layout = json.load(layout_file)
    layout_file.close()
    return layout

def load_localization (lang):
    # get system language
    try:
        loc_file = local_open(rf'res\localizations\strings-{lang}.json', 'r')
    except FileNotFoundError:
        loc_file = local_open(r'res\localizations\strings-en.json', 'r')
    loc = json.load(loc_file)
    loc_file.close()
    return loc

def load_theme (name):
    try:
        theme_file = local_open(rf'res\themes\{name}.json', 'r')
    except FileNotFoundError:
        theme_file = local_open(r'res\themes\default.json', 'r')
    theme = json.load(theme_file)
    theme_file.close()
    return theme

def check_settings (settings):
    if settings['temp_directory'] == None or \
       settings['default_directory'] == None:
        init_settings(settings)

def init_settings (settings):
    if settings['temp_directory'] == None:
        settings['temp_directory'] = local_dir + '\\temp'
    if settings['default_directory'] == None:
        default_default_directory = os.environ['USERPROFILE'] + '\\Downloads'
        settings['default_directory'] = default_default_directory


########################################################
# SHELL CODE: for debug
'''
while True:
    try:
        SHELL_input_command = input(f'$@{__name__}/> ')
        if SHELL_input_command == 'exit':
            break
        elif SHELL_input_command.startswith('/'):
            exec(SHELL_input_command[1:])
        else:
            print(eval(SHELL_input_command))
    except Exception as e:
        SHELL_exception_class = e.__class__.__name__
        print(f'!: {SHELL_exception_class} : {e}')
        SHELL_last_error = e
'''
########################################################



settings = load_settings()
settings['ffmpeg_location'] = local_dir
check_settings(settings)

layout = load_layout(settings['layout'])
localization = load_localization(settings['language_key'])
theme = load_theme(settings['theme'])


music_api = mdapi.MusicDownloaderAPI(settings)

music_downloader = mdgui.MusicDownloaderGUI(music_api, layout, localization, theme, settings)
music_downloader._save_settings = save_settings

music_downloader.run()

