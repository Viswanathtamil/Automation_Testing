import json
class SuccessStatus:
    DEFAULT = 'true'
    HTTP = 200
    SUCCESS = 'success'

class SuccessMessage:
    CREATE_MESSAGE = 'Successfully Created'
    UPDATE_MESSAGE = 'Successfully Updated'

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


class Status:
    partial = 1
    complete = 2