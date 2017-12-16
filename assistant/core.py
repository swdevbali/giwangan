import urllib3
from bs4 import BeautifulSoup
from flask import json, request
from flask_restful import Resource


class AssistantCore(Resource):
    def get(self, url=None):
        # to made a way for easy unit testing
        if url is None:
            url = request.args.get('url')
        result = {}

        http = urllib3.PoolManager()
        r = http.request('GET', url)
        if r.status == 200:
            bs = BeautifulSoup(r.data, 'html.parser')

            result['title'] = bs.find('title').text
            imgs = bs.find_all('img')
            images = []
            for img in imgs:
                images.append({'src': img.get('src', ''),
                               'alt': img.get('alt', '')})

            result['text'] = bs.find('body').text
            result['images'] = images

            return json.dumps({'success': True, 'result': result}), 200, {'ContentType': 'application/json'}
        return json.dumps({'success': False, 'result': r.status}), 200, {'ContentType': 'application/json'}
