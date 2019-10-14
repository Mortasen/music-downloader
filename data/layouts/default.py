# -*- encoding: utf-8 -*-
#JSON converted to .py for edit
#by JsonToPy programm

DATA =  {
    'title':'Default',
    
    'app': {
        'width':520,
        'height':600
        },

    'app_2': {
        'width':750,
        'height':600
        },

    'label_query': {
        'x':150,
        'y':5
        },

    'entry_query': {
        'x':100,
        'y':45,
        'width':300,
        'height':25
        },

    'button_search': {
        'x':410,
        'y':45,
        'width':25,
        'height':25
        },

    'label_title': {
        'x':50,
        'y':80,
        'width':420
        },

    'button_previous': {
        'x':10,
        'y':80,
        'width':40,
        'height':30
        },

    'button_next': {
        'x':450,
        'y':80,
        'width':40,
        'height':30
        },

    'label_image': {
        'x':10,
        'y':120,
        'width':332,
        'height':192
        },

    'label_uploader': {
        'x':350,
        'y':160
        },

    'label_views': {
        'x':350,
        'y':195
        },

    'label_likes': {
        'x':350,
        'y':230
        },

    'label_date': {
        'x':350,
        'y':265
        },

    'button_play': {
        'x':50,
        'y':320,
        'width':25,
        'height':25
        },

    'progress_bar': {
        'x':90,
        'y':320
        },

    'label_remaining_time': {
        'x':420,
        'y':320
        },

    'button_download': {
        'x':25,
        'y':360,
        'width':210,
        'height':40
        },

    'button_toqueue': {
        'x':265,
        'y':360,
        'width':210,
        'height':40
        },

    'entry_directory': {
        'x':20,
        'y':480
        },

    'entry_filename': {
        'x':20,
        'y':510
        },

    'entry_database': {
        'x':20,
        'y':540
        },

    'chbox_predownload': {
        'x':200,
        'y':440
        },

    'chbox_tags_from_video': {
        'x':200,
        'y':470
        },

    'chbox_lyrics': {
        'x':200,
        'y':500
        },

    'chbox_zipfile': {
        'x':200,
        'y':530
        },

    'chbox_database': {
        'x':200,
        'y':560
        },

    'button_expand': {
        'x':500,
        'y':5,
        'width':20,
        'height':595
        },

    'label_tag_title': {
        'x':565,
        'y':15
        },

    'entry_tag_title': {
        'x':560,
        'y':40,
        'width':120,
        'height':30
        },

    'label_tag_artist': {
        'x':565,
        'y':75
        },

    'entry_tag_artist': {
        'x':560,
        'y':100,
        'width':120,
        'height':30
        },

    'label_tag_genre': {
        'x':565,
        'y':135
        },

    'entry_tag_genre': {
        'x':560,
        'y':160,
        'width':120,
        'height':30
        },

    'label_tag_from': {
        'x':565,
        'y':195
        },

    'entry_tag_from': {
        'x':560,
        'y':220,
        'width':120,
        'height':30
        },

    'label_tag_source': {
        'x':565,
        'y':255
        },

    'entry_tag_source': {
        'x':560,
        'y':280,
        'width':120,
        'height':30
        },

    'label_tag_year': {
        'x':565,
        'y':315
        },

    'entry_tag_year': {
        'x':560,
        'y':340,
        'width':120,
        'height':30
        },

    'label_tag_instrument': {
        'x':565,
        'y':375
        },

    'entry_tag_instrument': {
        'x':560,
        'y':400,
        'width':120,
        'height':30
        },

    'label_tag_mood': {
        'x':565,
        'y':435
        },

    'entry_tag_mood': {
        'x':560,
        'y':460,
        'width':120,
        'height':30
        },

    'label_tag_mark': {
        'x':565,
        'y':495
        },

    'entry_tag_mark': {
        'x':560,
        'y':520,
        'width':120,
        'height':30
        }
    }


def Save ():
    import json
    json.dump(DATA, open("F:\Work\Programming\Python\MusicDownloader\data\layouts\default.json", "w"))
    print("Data was saved to F:\Work\Programming\Python\MusicDownloader\data\layouts\default.json.")

Save()
