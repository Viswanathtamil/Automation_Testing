import json


class auth_resp:
    status = None
    message = None

    def get(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    def set_status(self,status):
        self.status = status

    def set_message(self,message):
        self.message = message

class SuccessStatus:
    DEFAULT = 'true'
    HTTP = 200
    SUCCESS = 'success'

class SuccessMessage:
    ACTIVATED='Successfully Activated'
    INACTIVATED='Successfully Inactivated'
    DELETE_MESSAGE = 'Successfully Deleted'
    CREATE_MESSAGE = 'Successfully Created'
    DRAFT_CREATE_MESSAGE = 'Draft Successfully Created'
    UPDATE_MESSAGE = 'Successfully Updated'
    DRAFT_UPDATE_MESSAGE = 'Draft Successfully Updated'
    CLOSED_MESSAGE = 'Successfully Closed'
    SUCCESSFULLY_LOGOUT = 'Successfully logout'
    APPROVED_MESSAGE = 'Approved Successfully'
    REJECTED_MESSAGE = 'Rejected Successfully'
    INACTIVATED = 'Successfully Inactivated'
    ACTIVATED = 'Successfully Activated'
    EMAIL = ' Email Successfully Sended'