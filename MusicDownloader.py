# MusicDownloaderApp v0.6.7.1 by Namerif

import mdgui
import mdapi

import json

# [F?] ISSUE: Searching second song, button play still pause

VERSION = '0.6.7.1'

settings_ex = {
    'bitrate': 256,
    'videolimit': 3,
    'predownload': True,
    'temp_dir': 'F:', #'C:\\Windows\\Temp',
    'path': 'F:\\Music\\Music',
    'filename': '{artist} - {track}.mp3',
    'layout': 'default',
    'language': 'en',
    'theme': 'default'
    }


def load_settings ():
    return settings_ex


def load_layout (name):
    try:
        layout_file = open(rf'res\layouts\{name}.json', 'r')
    except FileNotFoundError:
        layout_file = open(r'res\layouts\default.json', 'r')
    layout = json.load(layout_file)
    layout_file.close()
    return layout

def load_localization (lang):
    # get system language
    try:
        loc_file = open(rf'res\localizations\strings-{lang}.json', 'r')
    except FileNotFoundError:
        loc_file = open(r'res\localizations\strings-en.json', 'r')
    loc = json.load(loc_file)
    loc_file.close()
    return loc

def load_theme (name):
    try:
        theme_file = open(rf'res\themes\{name}.json', 'r')
    except FileNotFoundError:
        theme_file = open(r'res\themes\default.json', 'r')
    theme = json.load(theme_file)
    theme_file.close()
    return theme



settings = load_settings()
layout = load_layout(settings['layout'])
localization = load_localization(settings['language'])
theme = load_theme(settings['theme'])


music_api = mdapi.MusicDownloaderAPI(settings)

music_downloader = mdgui.MusicDownloader(music_api, layout, localization, theme, settings)

music_downloader.run()

