from flask import Flask
from flask.ext.pymongo import PyMongo
from flask import render_template
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


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@app.route('/')
def hello_world():
    rv = cache.get('my-item')
    if rv is None:
        print "Here"
        online_users = mongo.db.myusers.find_one()
        rv = online_users['name']
        cache.set('my-item', rv, timeout=5 * 60)
    return render_template('index.html', name=rv)


api.add_resource(HelloWorld, '/r/hello')

if __name__ == '__main__':
    app.run(debug=True)
