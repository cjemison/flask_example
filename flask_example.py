import json

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
            r = Response(json.dumps(d), content_type='application/json; charset=utf-8')
            for key, value in self.arg1.iteritems():
                r.headers.add(key, value)
            return r

        return wrappee


class HelloWorld(Resource):
    @addHeader({"x-example": "value", "Last-Modified": "ex", })
    def get(self):
        d = dict()
        d['links'] = dict()
        d['links']['linkedin'] = 'https://www.linkedin.com/in/corneliusjemison'
        return d

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
