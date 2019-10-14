# -*- encoding: utf-8 -*-
#JSON converted to .py for edit
#by JsonToPy programm

DATA = {
    "title":"Default",
    "app": {
        "title":"MusicDownloader v0.5a"
        },

    "label_query": {
        "text":"Type your query below"
        },

    "entry_query": {
        "placeholder":"Rick Astley - Never Gonna Give You Up"
        },

    "button_search": {
        "text":"S"
        },

    "label_title": {
        "text":"Title Example 4K"
        },

    "label_uploader": {
        "text":"uploaderExample123"
        },

    "label_views": {
        "text":"Views Example K"
        },

    "label_likes": {
        "text":"Likes Example K"
        },

    "label_date": {
        "text":"12.28.2337"
        },

    "button_play": {
        "text":"P"
        },

    "label_remaining_time": {
        "text":"03 : 45"
        },

    "button_previous": {
        "text":"<<"
        },

    "button_next": {
        "text":">>"
        },

    "button_download": {
        "text":"Download"
        },

    "button_toqueue": {
        "text":"To Queue"
        },

    "chbox_predownload": {
        "text":"Predownload"
        },

    "chbox_tags_from_video": {
        "text":"Tags from video"
        },

    "chbox_lyrics": {
        "text":"Lyrics"
        },

    "chbox_zipfile": {
        "text":"Zipfile"
        },

    "chbox_database": {
        "text":"Database"
        },

    "button_expand": {
        "text":">"
        },

    "button_expand_2": {
        "text":"<"
        },

    "label_tag_title": {
        "text":"Title:"
        },

    "label_tag_artist": {
        "text":"Artist:"
        },

    "label_tag_genre": {
        "text":"Genre:"
        },

    "label_tag_from": {
        "text":"From:"
        },

    "label_tag_source": {
        "text":"Source:"
        },

    "label_tag_year": {
        "text":"Year:"
        },

    "label_tag_instrument": {
        "text":"Instrument:"
        },

    "label_tag_mood": {
        "text":"Mood:"
        },

    "label_tag_mark": {
        "text":"Mark:"
        }
    }


def Save ():
    import json
    json.dump(DATA, open("F:\Work\Programming\Python\MusicDownloader\data\localizations\strings.json", "w"))
    print("Data was saved to F:\Work\Programming\Python\MusicDownloader\data\localizations\strings.json.")

Save()
