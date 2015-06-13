import json
from datetime import datetime

from flask import Flask, Response
from flask.ext.pymongo import PyMongo
from werkzeug.contrib.cache import MemcachedCache
from flask_restful import Resource, Api

cache = MemcachedCache(['127.0.0.1:11211'])

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'relevant_church'
app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_USERNAME'] = 'cjemison'
app.config['MONGO_PASSWORD'] = 'cjemison'
mongo = PyMongo(app)
api = Api(app)


class addHeader(object):
    def __init__(self, d=dict()):
        self.arg1 = d

    def __call__(self, original_func):
        def wrappee(*args, **kwargs):
            d = original_func(*args, **kwargs)
            data = json.dumps(d, indent=4)
            r = Response(json.dumps(d), content_type='application/json; charset=utf-8')
            for key, value in self.arg1.iteritems():
                r.headers.add(key, value)
            r.headers.add("Access-Control-Allow-Origin", "*")
            r.headers.add("Access-Control-Allow-Methods", "POST,GET,PUT,DELETE,OPTIONS")
            r.headers.add("Access-Control-Allow-Headers", "Last-Modified, Authorization, Lang")
            return r

        return wrappee


class HelloWorld(Resource):
    @addHeader({"Last-Modified": datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
                "Content-Language": "en",
                "Cache-Control": "no-store, must-revalidate, no-cache, max-age=0"})
    def get(self):
        links = cache.get("links")
        if links is None:
            links = mongo.db.links.find_one()
            if links is None:
                d = dict()
                d['links'] = list()
                d['links'].append(
                    {"url": 'https://www.linkedin.com/in/corneliusjemison', 'type': 'link', 'name': 'linkedin'})
                mongo.db.links.insert(d)
            id = str(links['_id'])
            del links['_id']
            links['id'] = id
            cache.set('links', links, timeout=5 * 60)
        return links

# @app.route('/')
# def hello_world():
#     rv = cache.get('my-item')
#     if rv is None:
#         online_users = mongo.db.myusers.find_one()
#         rv = online_users['name']
#         cache.set('my-item', rv, timeout=5 * 60)
#     return render_template('index.html', name=rv)

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
