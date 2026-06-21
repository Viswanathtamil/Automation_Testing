import json


class auth_error:
    code = None
    http_status = None
    description = None
    def get(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    def set_code(self, code):
        self.code = code
    def set_http_status(self,http_status):
        self.http_status = http_status
    def set_description(self, description):
        self.description = description



    # def get_code(self):
    #     return self.code
    #
    # def get_description(self):
    #     return self.description