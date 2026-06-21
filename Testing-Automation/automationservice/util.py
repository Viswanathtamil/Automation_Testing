import json
class SuccessStatus:
    DEFAULT = 'true'
    HTTP = 200
    SUCCESS = 'success'

class SuccessMessage:
    CREATE_MESSAGE = 'Successfully Created'

class Success:
    status = None
    message = None

    def get(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def set_status(self, status):
        self.status = status

    def set_message(self, message):
        self.message = message



class Error:
    code = None
    description = None
    errorcode=None
    def __init__(self):
        pass

    def set_code(self, code):
        self.code = code

    def errorcode(self, errorcode):
        self.errorcode = errorcode

    def set_description(self, description):
        self.description = description

    def get_code(self):
        return self.code

    def get_description(self):
        return self.description

    def get(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)