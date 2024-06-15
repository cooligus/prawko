import json
import os
import requests

SECTION_ID = 15

with open('tmp/{}.json'.format(SECTION_ID)) as f:
    d = json.load(f)
    try:
        os.mkdir(os.path.join('tmp', str(SECTION_ID)))
    except OSError:
        pass
    for elem in d:
        if elem['Image'] != '':
            img_data = requests.get(elem['Image']).content
            with open(os.path.join('tmp', str(SECTION_ID), elem['Image'][-9:]) + '.jpg', 'wb') as handler:
                handler.write(img_data)
        if elem['Video'] != '':
            video_data = requests.get(elem['Video']).content
            with open(os.path.join('tmp', str(SECTION_ID), elem['Video'][-9:]) + '.mp4', 'wb') as handler:
                handler.write(video_data)