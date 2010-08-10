from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson as json

from nabazlib.Nabaztag import Nabaztag



class Hook(webapp.RequestHandler):

    def post(self):
        
        #get the credentials for the nazaztag 
        u = self.request.get("id")
        p = self.request.get("secret")
        
        #get the JSON payload. this is stored in the POST variable "payload"
        jsonstr = self.request.get("payload")
        
        #parse it
        obj = json.loads(jsonstr)
        
        #read out some interesting data
        reponame = obj['repository']['name']
        author = obj['commits'][0]['author']['name']
        msg = obj['commits'][0]['message']
        numcommits = len(obj['commits'])
        
        #construct the string we want to send to the rabbit
        txt = "Git alert! Git alert! %s just pushed %d commits to %s" %(author,numcommits,reponame)
        self.response.out.write(txt)
        
        #construct the nabaztag object and send the text
        myNabaztag = Nabaztag(u,p)
        myNabaztag.say(txt,voice='US-Liberty')


application = webapp.WSGIApplication([
    ('/', Hook)
], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
