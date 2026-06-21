import json


class AuthResponse:
    token = None
    expiry = None
    name = None
    code = None
    employee_id = None
    user_id = None
    entity_id = None
    def get(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    def set_token(self,token):
        self.token=token

    def set_expiry(self,expiry):
        self.expiry = expiry

    def set_name(self,name):
        self.name = name

    def set_code(self,code):
        self.code = code

    def set_employee_id(self,employee_id):
        self.employee_id = employee_id

    def set_user_id(self,user_id):
        self.user_id = user_id

    def set_entity_id(self,entity_id):
        self.entity_id = entity_id