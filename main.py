from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson as json

from nabazlib.Nabaztag import Nabaztag



class Hook(webapp.RequestHandler):

    def post(self):
        
        
        u = self.request.get("id")
        p = self.request.get("secret")
        jsonstr = self.request.get("payload")
        obj = json.loads(jsonstr)
        reponame = obj['repository']['name']
        author = obj['commits'][0]['author']['name']
        msg = obj['commits'][0]['message']
        numcommits = len(obj['commits'])
        str = "Git alert! Git alert! %s just pushed %d commits to %s" %(author,numcommits,reponame)
        self.response.out.write(str)
        
        myNabaztag = Nabaztag(u,p)
       
        
        myNabaztag.say(str,voice='US-Liberty')


application = webapp.WSGIApplication([
    ('/', Hook)
], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
