__author__ = 'alanh'



'''
body should be a json object. E.g. the result of json.loads(jsonString)
'''
class Response():

    def __init__(self, status, reason, body):
        self.status = status
        self.reason = reason
        self.body = body


