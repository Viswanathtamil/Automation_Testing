import json


class Aut_Response:
    id = None
    client_name = None
    project_module = None
    Testcase_scenario_name = None
    Testcase_scenario_template = None
    environment = None
    created_date = None
    updated_date = None
    testcase_code = None
    status = None
    activeinactive = None
    url = None
    batch_code = None
    crno = None
    name = None
    run_status = None
    scenario_name = None
    def get(self):
      return json.dumps(self, default=lambda o: o.__dict__,
                         sort_keys=True, indent=4)

    def set_id(self, id):
        self.id = id

    def set_client_name(self, client_name):
        self.client_name = client_name

    def set_project_module(self,  project_module):
        self. project_module = project_module

    def set_url(self,  url):
        self. url = url

    def set_Testcase_scenario_name(self, Testcase_scenario_name):
        self.Testcase_scenario_name = Testcase_scenario_name

    def set_Testcase_scenario_template(self, Testcase_scenario_template):
        self.Testcase_scenario_template = Testcase_scenario_template

    def set_createddate(self, createddate):
        self.createddate = createddate

    def set_environment(self, environment):
        self.environment = environment

    def set_updated_date(self, updated_date):
        self.updated_date = updated_date

    def set_testcase_code(self, testcase_code):
        self.testcase_code = testcase_code

    def set_batch_code(self, batch_code):
        self.batch_code = batch_code

    def set_name(self, name):
        self.name = name

    def set_crno(self, crno):
        self.crno = crno

    def set_status(self, status):
        self.status = status
    def set_run_status(self, run_status):
        self.run_status = run_status

    def set_activeinactive(self, activeinactive):
        self.activeinactive = activeinactive

    def set_scenario_name(self, scenario_name):
        self.scenario_name = scenario_name



    def get_id(self):
        return self.id

    def get_client_name(self):
        return self.client_name

    def get_project_module(self):
        return self.project_module

    def get_Testcase_scenario_name(self):
        return self.Testcase_scenario_name

    def get_Testcase_scenario_template(self):
        return self.Testcase_scenario_template

    def get_environment(self):
        return self.environment

    def get_updated_date(self):
        return self.updated_date

    def get_createddate(self):
        return self.createddate