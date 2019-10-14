# -*- encoding: utf-8 -*-
#JSON converted to .py for edit
#by JsonToPy programm

DATA = {
    "title":"Default",
    "app": {
        "bg":"#252540"
        },

    "label_query": {
        "font": [
            "Roboto",
            16
            ],
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_title": {
        "font": [
            "Roboto",
            12,
            "bold"
            ],
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_image": {
        "bd":5,
        "relief":"groove",
        'bg': '#252540'
        },

    "label_uploader": {
        'font': [
            'Roboto',
            10
            ],
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_views": {
        'font': [
            'Roboto',
            10
            ],
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_likes": {
        'font': [
            'Roboto',
            10
            ],
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_date": {
        'font': [
            'Roboto',
            10
            ],
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "progress_bar": {
        "orient":"horizontal",
        "length":320,
        "mode":"determinate"
        },

    "label_remaining_time": {
        "font": [
            "Arial",
            12,
            "bold"
            ],
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "chbox_predownload": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "chbox_tags_from_video": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "chbox_lyrics": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "chbox_zipfile": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "chbox_database": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_tag_title": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_tag_artist": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_tag_genre": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_tag_from": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_tag_source": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_tag_year": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_tag_instrument": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_tag_mood": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        },

    "label_tag_mark": {
        'fg': '#F0F0F0',
        'bg': '#252540'
        }
    }


def Save ():
    import json
    json.dump(DATA, open(r"F:\Work\Programming\Python\MusicDownloader\data\themes\default.json", "w"))
    print("Data was saved to F:\Work\Programming\Python\MusicDownloader\data\themes\default.json.")

Save()
