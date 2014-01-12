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


import logging
logging.basicConfig(filename="SLSmart.log", level=logging.DEBUG)
requests_log = logging.getLogger("SLSmart")
requests_log.setLevel(logging.DEBUG)


class SLRequester():

    @classmethod
    @defer.inlineCallbacks
    def request(cls,payload={}):
        try:
            missing = []
            if not "S" in payload:
                missing.append("start")
            if not "Z" in payload:
                missing.append("destination")

            if not missing:
                payload["key"] = settings["key"]
                response = yield treq.get('https://api.trafiklab.se/sl/reseplanerare.json',
                          headers={'Content-Type': ['application/json']},
                          params=payload
                          )
                result = yield cls.parse(response)
                defer.returnValue(result)
            else:
                defer.returnValue("%s%s" %("missing", missing))

        except Exception as e:
            print e

    @classmethod
    @defer.inlineCallbacks
    def parse(cls,response):
        content = yield treq.text_content(response)
        json_content = json.loads(content)
        content = json.dumps(json_content, ensure_ascii=False,indent =2)
        defer.returnValue(content.encode("utf-8"))




class SLSmartResource(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def render_GET(self, request):
        self.get_response(request)
        return NOT_DONE_YET

    @defer.inlineCallbacks
    def get_response(self,request):
        payload = {}
        for arg in request.args:
            payload[arg] = request.args[arg][0]

        result = yield SLRequester.request(payload)
        request.setHeader("Content-Type", "application/json; charset=utf-8")
        request.write(result)
        request.finish()

reactor.listenTCP(8083, server.Site(SLSmartResource()))
reactor.run()

