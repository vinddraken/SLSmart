import requests

import json

import treq
from twisted.internet import defer, reactor

from twisted.web import server, resource

from twisted.web.server import NOT_DONE_YET


def read_dict_from_file(filename):
    with open(filename, "r+") as jsonfile:
        return json.loads(jsonfile.read())

settings = read_dict_from_file("api.key")

payload = {'key': settings["key"], 'S': 'gubbangen',"Z": "slussen"}


class SLRequester():

    @staticmethod
    @defer.inlineCallbacks
    def make_req():
        try:
            response = yield treq.get('https://api.trafiklab.se/sl/reseplanerare.json',
                      headers={'Content-Type': ['application/json']},
                      params=payload
                      )
            content = yield treq.text_content(response)
            json_content = json.loads(content)
            content = json.dumps(json_content, ensure_ascii=False,indent =2)
            defer.returnValue(content.encode("utf-8"))

        except Exception as e:
            print e


class SLSmartResource(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def render_GET(self, request):
        self.get_response(request)
        return NOT_DONE_YET

    @defer.inlineCallbacks
    def get_response(self,request):
        result = yield SLRequester.make_req()
        request.setHeader("Content-Type", "application/json; charset=utf-8")
        request.write(result)
        request.finish()

reactor.listenTCP(8083, server.Site(SLSmartResource()))
reactor.run()

