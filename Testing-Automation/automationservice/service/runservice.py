import ast
import base64
import json
from threading import Thread
from datetime import datetime
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from playwright.sync_api import sync_playwright
from weasyprint import HTML
import pdfkit
from io import BytesIO
from xhtml2pdf import pisa
from Automation.settings import logger
from automationservice.models import Testcase_Run, Testcase_Scenario_Template, \
    Testcase_Result, Client, Module_master, ScreenshotBlob, Batchcode
import os
import sys
from django.conf import settings
from utilityservice.vysfinlist import VysfinList
from utilityservice.vysfinpaginator import VysfinPaginator
from .util import SuccessMessage,SuccessStatus,Success,Status
from ..data.response.automationresp import Aut_Response
from userservice.models.usermodels import Employee

success_obj = Success()

class Module_Selection:
    def select_module(self, page,Module,client):
        try:
            if Module == 'ECF':
                page.get_by_title("ECF Claim").locator("i").click()
                page.get_by_text("ECF Claim", exact=True).click()
                logger.info("test")
            elif Module == 'Vendor':
                if client == 'NF' and client == 'NAC':
                    page.get_by_title("Vendor").locator("i").click()
                    page.get_by_text("Vendor", exact=True).click()
                elif client == 'WR':
                    page.locator("p.nl-link:has-text('Vendor')").click()
            elif Module == 'AP':
                if client == 'NF':
                    page.get_by_role("button").click()
                    page.get_by_text("Accounts Payable", exact=True).nth(0).click()
                elif client == 'NAC':
                    page.get_by_title("AP").locator("i").click()
                elif client == 'KVB':
                    page.get_by_title("Accounts Payable").locator("i").click()
                    page.get_by_text("Accounts Payable", exact=True).click()
        except Exception as e:
            logger.info(e)



class automationserv:

    def template_create(self, data, value,user_id):

        if value == 1:
            status = Status.partial
        elif value == 2:
            status = Status.complete

        with transaction.atomic():

            if data.get('id') is not None:
                id = data.get('id')
                Testcase_Scenario_Template.objects.filter(id=id).update(
                    client_name=data['client_name'],
                    Project_module=data['Project_module'],
                    Testcase_scenario_name=data['Testcase_scenario_name'],
                    Testcase_scenario_template=data['Testcase_scenario_template'],
                    environment=data['environment'],
                    Steps=data['steps'],
                    url=data['environment_url'],
                    updated_date=datetime.now(),
                    full_partial=status,
                    updated_by = user_id
                )

                Testcase_Run.objects.filter(testcase_scn_id=id).update(
                    module=data['Project_module'],
                    Testcase_template_input = json.dumps(data['Testcase_scenario_template']),
                    updated_date=datetime.now(),
                    environment=data['environment'],
                    url=data['environment_url'],
                    client_name=data['client_name'],
                    full_partial=status,
                    updated_by=user_id,
                    Testcase_scenario_name=data['Testcase_scenario_name']
                )
                success_obj.set_status(SuccessStatus.SUCCESS)
                success_obj.set_message("Template updated Suceessfully")
                return success_obj

            else:
                prefix = "AUT"
                module = data['Project_module'].upper()  # ECF
                env = data['environment'].upper()  # SIT or DO
                client = data['client_name'].upper()

                # Count how many test cases already exist for this module + environment
                existing_count = Testcase_Scenario_Template.objects.filter(
                    Project_module=data['Project_module'],
                    environment=data['environment'],
                    client_name=data['client_name']
                ).count()

                suffix = f"{existing_count + 1:03}"  # Pad number like 001, 002, ...
                testcase_code = f"{prefix}{module}{env}{client}{suffix}"  # AUTECFSIT001
                test = Testcase_Scenario_Template.objects.create(client_name=data['client_name'],
                                                                 Project_module=data['Project_module'],
                                                                 Testcase_scenario_name=data['Testcase_scenario_name'],
                                                                 Testcase_scenario_template=data['Testcase_scenario_template'],
                                                                 environment=data['environment'],
                                                                 url=data['environment_url'],
                                                                 Steps=data['steps'],
                                                                 created_date=datetime.now(),
                                                                 full_partial = status,
                                                                 Testcase_code=testcase_code,
                                                                 created_by=user_id,
                                                                 updated_date=datetime.now(),
                                                                 updated_by=user_id)
                test_id = test.id
                template = data['Testcase_scenario_template']
                template_input = json.dumps(template)
                Testcase_Run.objects.create(
                    module=data['Project_module'],
                    Testcase_template_input=template_input,
                    Testcase_code=testcase_code,
                    created_date=datetime.now(),
                    environment=data['environment'],
                    testcase_scn_id=test_id,
                    url=data['environment_url'],
                    client_name=data['client_name'],
                    full_partial=status,
                    created_by=user_id,
                    updated_date = datetime.now(),
                    updated_by = user_id,
                    Testcase_scenario_name = data['Testcase_scenario_name']
                )
                success_obj.set_status(SuccessStatus.SUCCESS)
                success_obj.set_message("Template created Suceessfully")
                return success_obj

    def get_template(self, id):
        condition = Q()
        if id is not None:
            condition &= Q(id=id)
        template = Testcase_Scenario_Template.objects.filter(condition).values()
        empty_list = VysfinList()
        for i in template:
            temp_response = Aut_Response()
            temp_response.set_id(i['id'])
            temp_response.set_environment(i['environment'])
            temp_response.set_client_name(i['client_name'])
            temp_response.set_project_module(i['Project_module'])
            temp_response.set_url(i['url'])
            temp_response.set_Testcase_scenario_template(i["Testcase_scenario_template"])
            temp_response.set_Testcase_scenario_name(i['Testcase_scenario_name'])
            empty_list.append(temp_response)
        return empty_list



class Report:
    def test_report_pdf(request, clientnme, module, from_date, to_date, code, envirnment, id, batchcode):

        if id is not None:
            records = Testcase_Result.objects.filter(id=id).values(
                'client_name', 'status', "Message", "code", 'Module', 'screenshoot',
                'Testcase_Result', 'outputdata', 'Testcase_code', 'updated_by',
                'created_date', 'Test_scnarios', 'environment', 'Testcase_scenario_name', 'batch_code','url'
            )
            scenario_name = Testcase_Result.objects.get(id=id).Testcase_scenario_name
        else:
            condition = Q()
            if clientnme is not None:
                condition &= Q(client_name=clientnme)
            if module is not None:
                condition &= Q(Module=module)
            if from_date is not None and to_date is not None:
                condition &= Q(created_date__range=[from_date, to_date])
            if code is not None:
                condition &= Q(Testcase_code=code)
            if envirnment is not None:
                condition &= Q(environment=envirnment)
            if batchcode is not None:
                condition &= Q(batch_code=batchcode)

            records = Testcase_Result.objects.filter(condition).values(
                'client_name', 'status', "Message", "code", 'Module', 'screenshoot',
                'Testcase_Result', 'outputdata', 'Testcase_code', 'updated_by',
                'created_date', 'Test_scnarios', 'environment', 'Testcase_scenario_name', 'batch_code','url'
            )
            scenario_name = Testcase_Result.objects.filter(condition).values_list('Testcase_scenario_name',flat=True).first()

        data_set = []
        for rec in records:
            fetchcode = rec.get('code', '')
            fetchuserid = rec.get('updated_by','')
            name_fetch = Employee.objects.filter(user_id=fetchuserid).values('user_name')
            employee_name = name_fetch[0]['user_name']
            try:
                parsed = json.loads(rec['outputdata']) if rec.get('outputdata') else {}
            except Exception:
                parsed = {}

            try:
                screenshot_list = json.loads(rec['screenshoot']) if rec.get('screenshoot') else []
            except Exception:
                screenshot_list = []
            screenshots_by_section = {}
            for path in screenshot_list:
                try:
                    section = path.split("/")[-2]
                    blob = ScreenshotBlob.objects.filter(file_path=path).first()
                    if blob and blob.image_blob:
                        base64_img = base64.b64encode(blob.image_blob).decode("utf-8")
                        screenshots_by_section.setdefault(section, []).append(base64_img)
                except Exception:
                    continue

            # -------- PROCESS SECTION DATA --------
            for section_name, section_data in parsed.items():
                if section_name != "Testcase_scnarios" and isinstance(section_data, dict):
                    updated_section = {}
                    for key, value in section_data.items():
                        if isinstance(value, dict):
                            field_key = str(value.get("field_key", "")).strip().lower()
                            if "button" in field_key or "click" in field_key:
                                continue
                        formatted_key = str(key)
                        if isinstance(value, dict):
                            field_value = value.get("field_value", "")
                        else:
                            field_value = value
                        field_value_str = str(field_value)
                        if "password" in str(key).lower():
                            formatted_value = "*" * len(field_value_str)
                        elif "{{code}}" in field_value_str:
                            formatted_value = field_value_str.replace("{{code}}",str(fetchcode))
                        else:
                            formatted_value = field_value_str

                        if isinstance(value, dict):
                            value["field_value"] = formatted_value
                            updated_section[formatted_key] = value
                        else:
                            updated_section[formatted_key] = {"field_value": formatted_value}

                    # ---------- ADD SCREENSHOTS ----------
                    updated_section["images"] = screenshots_by_section.get(section_name, [])
                    parsed[section_name] = updated_section

            rec['input_parsed'] = parsed
            rec['updated_by'] = employee_name

            data_set.append(rec)

        html = render_to_string(
            "report_template.html",
            {"records": data_set}
        )
        pdf_file = HTML(string=html).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{scenario_name}_{datetime.now().strftime("%d-%m-%Y")}.pdf"'
        return response



    def view_report(self, id, batchcode):
        condition = Q()
        if id is not None:
            condition &= Q(id=id)
        elif batchcode is not None:
            condition &= Q(batch_code=batchcode)

        records = Testcase_Result.objects.filter(condition).values(
            'client_name', 'status', "Message", "code", 'Module', 'screenshoot',
            'Testcase_Result', 'outputdata', 'Testcase_code',
            'created_date', 'Test_scnarios', 'environment', 'Testcase_scenario_name', 'batch_code'
        )

        data_set = []

        for rec in records:
            screenshots = []

            try:
                screenshot_list = json.loads(rec['screenshoot'])  # string → list
            except Exception as e:
                screenshot_list = []

            for path in screenshot_list:
                blob_obj = ScreenshotBlob.objects.filter(file_path=path).first()

                if blob_obj and blob_obj.image_blob:
                    base64_str = base64.b64encode(blob_obj.image_blob).decode("utf-8")
                    screenshots.append(base64_str)

            rec['base64_images'] = screenshots
            data_set.append(rec)
        return data_set


class runserv:
    def runprocess(self, testcasecode, client,testcase_id,user_id):
        runtime_context = {}
        test_code = ast.literal_eval(testcasecode)
        test_run = Testcase_Run.objects.filter(Testcase_code__in=test_code)
        for run in test_run:
            stop_current_run = False
            scenrios_status_dict = {}
            testcode = run.Testcase_code
            test_ids = list(Testcase_Result.objects.filter(Testcase_code=testcode,status='Yet to start').values_list('id', flat=True))
            input_str = run.Testcase_template_input
            module = run.module
            url = run.url
            environment = run.environment
            batchcode = run.batch_code
            test_case = json.loads(input_str)
            Batchcode.objects.filter(batch_code=batchcode).update(status="Started", client_name=client, Module=module, environment=environment, updated_date=datetime.now(), updated_by=user_id)
            try:
                sys.stderr.fileno()
            except Exception:
                sys.stderr = open(os.devnull, "w")
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"], slow_mo=1000)
            context = browser.new_context(viewport={"width": 1350, "height": 650})
            page = context.new_page()
            page.goto(url)
            page.wait_for_timeout(5000)

            def resolve_runtime_value(value, context):
                if isinstance(value, str) and "{{" in value and "}}" in value:
                    for k, v in context.items():
                        value = value.replace(f"{{{{{k}}}}}", str(v))
                return value

            def handle_dialog(dialog):
                logger.info(f"Dialog message: {dialog.message}")
                dialog.accept()

            def wait_for_screen_to_load(page):
                try:
                    page.wait_for_selector(".loading-text", timeout=3000)
                    try:
                        page.wait_for_selector(".loading-text", state="detached", timeout=5000)
                    except:
                        page.wait_for_selector(".loading-text", state="hidden", timeout=5000)
                except:
                    logger.info("No loading-text found, or it disappeared too quickly.")

            def is_valid_date(value):
                try:
                    datetime.strptime(value, "%d-%m-%Y")
                    return True
                except ValueError:
                    return False

            def save_screenshot_blob(relative_path, screenshot_bytes):
                ScreenshotBlob.objects.create(
                    file_path=relative_path,
                    image_blob=screenshot_bytes
                )

            def fetch_scenario_map(test_ids, result):
                qs = (
                    Testcase_Result.objects
                    .filter(id__in=test_ids)
                    .values_list('id', 'Test_scnarios')
                )
                result.update(dict(qs))

            scenario_map = {}
            t = Thread(target=fetch_scenario_map, args=(test_ids, scenario_map))
            t.start()
            t.join()
            try:
                for index, test_id in enumerate(test_ids):
                    if stop_current_run:
                        def fail_result():
                            Testcase_Result.objects.filter(id__in=test_ids,status='Yet to start').update(status="Failed",
                                                                              test_implement_status="Failed",
                                                                              Testcase_Result="Fail")
                            Batchcode.objects.filter(batch_code=batchcode).update(status="Failed")

                        t1 = Thread(target=fail_result)
                        t1.start()
                        t1.join()
                        break
                    logger.info(f"Running for Testcase ID: {test_id}")

                    expected_scenario = scenario_map.get(int(test_id))

                    if not expected_scenario:
                        logger.info(f"No scenario mapped for test_id {test_id}")
                        continue
                    logger.info(f"Scenario to run: {expected_scenario}")

                    Thread(
                        target=lambda: Testcase_Result.objects.filter(id=test_id).update(
                            client_name=client,
                            Module=module,
                            environment=environment,
                            status="STARTED",
                            updated_date=datetime.now(),
                            updated_by=user_id
                        )
                    ).start()
                    input_data = next(
                        (d for d in test_case['data']
                         if d.get("Testcase_scnarios") == expected_scenario),
                        None
                    )

                    if not input_data:
                        logger.info(f"Scenario {expected_scenario} not found in JSON")
                        continue

                    logger.info(f"Executing scenario: {expected_scenario}")
                    logger.info(input_data)
                    scenario_name = input_data.get("Testcase_scnarios", "Unnamed")
                    logger.info(f"Scenario: {scenario_name}")
                    section_status_dict = {}
                    date = datetime.now().strftime('%Y-%m-%d')
                    safe_module = "".join(c if c.isalnum() or c in " _-" else "_" for c in module)
                    safe_scenario = "".join(c if c.isalnum() or c in " _-" else "_" for c in scenario_name)
                    screenshot_paths = []
                    i = 0
                    for section_key, section_value in input_data.items():
                        if section_key == "Testcase_scnarios":
                            continue
                        if stop_current_run:
                            break
                        section_name = section_key
                        logger.info(f"Current Section: {section_name}")
                        safe_section = "".join(c if c.isalnum() or c in " _-" else "_" for c in section_name)
                        fail_fields = []
                        success_fields = []
                        merged_steps = section_value if isinstance(section_value, list) else [section_value]
                        message = ""
                        for section in merged_steps:
                            for field_name, field_data in section.items():
                                field_type = field_data.get("field_type")
                                field_key = field_data.get("field_key")
                                field_value = field_data.get("field_value")
                                value_type = field_data.get("value_type")
                                key = resolve_runtime_value(field_key, runtime_context)
                                value = resolve_runtime_value(field_value, runtime_context)
                                try:
                                    scenrios_status_dict[scenario_name] = 'Started'
                                    if key.startswith("button"):
                                        page.once("dialog", handle_dialog)
                                        locator = page.get_by_role("button", name=value)
                                        if locator.count() > 0:
                                            btn_type = locator.get_attribute("type")
                                            if btn_type is None or btn_type == "button" or btn_type == 'submit':
                                                locator.nth(0).click()
                                                wait_for_screen_to_load(page)
                                                if client == 'NF' and (module == 'ECF' or module == 'AP'):
                                                    wait_for_screen_to_load(page)
                                        elif locator.count() == 0:
                                                locator = page.locator(f"#{value}")
                                                if client == 'KVB' and value in ['invoice-detail-0074','invoice-detail-0056']:
                                                    page.wait_for_timeout(3000)
                                                locator.nth(0).click()
                                                wait_for_screen_to_load(page)
                                                if client == 'NF' and (module == 'ECF' or module == 'AP'):
                                                    wait_for_screen_to_load(page)
                                                elif client == 'KVB' and value in ['invoice-detail-0074','invoice-detail-0056']:
                                                    rows = page.locator("#summary-table-07 table tr")
                                                    row_count = rows.count()
                                                    logger.info("Total Rows Found:", row_count)
                                                    for i in range(1, row_count-1):
                                                        row = rows.nth(i)
                                                        ok_button = row.locator("label:has-text('OK')")
                                                        if ok_button.count() > 0:
                                                            ok_button.first.click()
                                                            logger.info(f"OK clicked for row {i}")
                                                        else:
                                                            logger.info(f"OK button not found for row {i}")

                                        toast = page.locator(".toast-top-right.toast-container")
                                        toast_count = toast.count()
                                        if toast_count > 0:
                                            message = toast.inner_text()
                                            logger.info(f"Toast message: {message}")
                                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                                            filename = f"screenshot_{timestamp}.png"
                                            screenshot_bytes = page.screenshot()
                                            relative_path = f"{date}/{client}/{environment}/{safe_module}/{safe_scenario}/{safe_section}/{filename}"
                                            t_img = Thread(target=save_screenshot_blob, args=(relative_path, screenshot_bytes))
                                            t_img.start()
                                            t_img.join()
                                            screenshot_paths.append(relative_path)
                                        else:
                                            message = ""
                                            logger.info("No toast message visible")
                                    elif key == 'module':
                                        page.get_by_text(f"{value}", exact=True).nth(0).click()
                                    elif key in ["create-ecf-0063","invoice-detail-0220"] and value_type == 'dynamic':
                                        nom = datetime.now().strftime("%d-%m-%Y-%H%M%S")
                                        page.locator(f'[id="{key}"]').fill(nom)
                                    elif key == "tooltip":
                                        page.locator(f'[mattooltip="{value}"]').click(force=True)
                                    elif key == "link":
                                        page.locator("a", has_text=f"{value}").click()
                                    elif key == "textbox":
                                        editor = page.locator(".editor-pad[contenteditable='true']:visible")
                                        editor.type(value)
                                    elif key == 'click':
                                        if client == 'NAC' and module == 'Vendor' and value == 'payment':
                                            page.get_by_text(f"{value}", exact=True).nth(i).click()
                                            i += 1
                                        elif client == 'NF' and module == 'AP' and value == 'invdetail-0016':
                                            rows = page.locator('#invdetail-0015 tbody tr')
                                            count = rows.count()
                                            for i in range(count):
                                                i += i
                                                page.locator('tbody tr').locator('label:has-text("OK")').nth(i).click()
                                        else:
                                            text_locator = page.get_by_text(f"{value}", exact=True)
                                            if text_locator.count() > 0:
                                                text_locator.first.click()
                                                wait_for_screen_to_load(page)
                                            else:
                                                form_locator = page.locator(f'[formcontrolname="{value}"]')
                                                placeholder_locator = page.locator(f'[placeholder="{value}"]')
                                                id_locator = page.locator(f'[id="{value}"]')
                                                if form_locator.count() > 0:
                                                    form_locator.click()
                                                elif placeholder_locator.count() > 0:
                                                    placeholder_locator.click()
                                                elif id_locator.count() > 0:
                                                    id_locator.click()
                                    elif key == 'file' or key.startswith('file-type'):
                                        file_path = os.path.join(settings.MEDIA_ROOT, value)

                                        if key == 'file':
                                            page.set_input_files('input[type="file"]', file_path)
                                        elif key.startswith('file-type'):
                                            with page.expect_file_chooser() as fc_info:
                                                page.locator(f'#{key}').click()
                                            file_chooser = fc_info.value
                                            file_chooser.set_files(file_path)
                                    elif value.startswith('Horizontal_scroll'):
                                        page.locator(".table-responsive").evaluate("el => el.scrollLeft = el.scrollWidth")
                                        scroll_container = page.locator(".table-responsive")
                                        page.wait_for_timeout(2000)
                                    elif value.startswith('Vertical_scroll'):
                                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                                        page.wait_for_timeout(2000)
                                    elif value.startswith('Bottomto_top_scroll'):
                                        page.evaluate("window.scrollTo(0, 0)")
                                        page.wait_for_timeout(2000)
                                    elif is_valid_date(value):
                                        if value_type == 'dynamic':
                                            value = datetime.now().strftime("%d-%m-%Y")
                                        form_locator = page.locator(f'[formcontrolname="{key}"]')
                                        placeholder_locator = page.locator(f'[placeholder="{key}"]')
                                        id_locator = page.locator(f'[id="{key}"]')

                                        if form_locator.count() > 0:
                                            locator = form_locator
                                        elif placeholder_locator.count() > 0:
                                            locator = placeholder_locator
                                        elif id_locator.count() > 0:
                                            locator = id_locator
                                        else:
                                            raise Exception(f"No valid locator found for key: {key}")

                                        locator.wait_for(state="attached")

                                        # Find the parent container for this date field
                                        parent = locator.locator("xpath=ancestor::*[contains(@class, 'mat-form-field')]")

                                        # Find the calendar toggle button inside that parent
                                        calendar_button = parent.locator("button[aria-label='Open calendar']")

                                        # Click the correct calendar button for this field
                                        calendar_button.click()

                                        # Parse the input date
                                        dt = datetime.strptime(value, "%d-%m-%Y")
                                        # Navigate and select year, month, and day
                                        page.locator('.mat-calendar-period-button').click()
                                        page.locator(".mat-calendar-body-cell-content", has_text=str(dt.year)).click()
                                        page.locator(".mat-calendar-body-cell-content", has_text=dt.strftime("%b")[:3]).click()
                                        page.locator(".mat-calendar-body-cell-content", has_text=str(dt.day)).first.click()
                                    else:
                                        form_locator = page.locator(f'[formcontrolname="{key}"]')
                                        placeholder_locator = page.locator(f'[placeholder="{key}"]')
                                        id_locator = page.locator(f'[id="{key}"]')
                                        if form_locator.count() > 0:
                                            locator = form_locator.nth(0)
                                        elif placeholder_locator.count() > 0:
                                            locator = placeholder_locator.nth(0)
                                        elif id_locator.count() > 0:
                                            locator = id_locator.nth(0)
                                        locator.wait_for(state="attached")
                                        try:
                                            tag_name = locator.evaluate("el => el.tagName.toLowerCase()")
                                            if tag_name == 'mat-select':
                                                form_locator = page.locator(f'[formcontrolname="{key}"] .mat-mdc-select-trigger')
                                                placeholder_locator = page.locator(f'[placeholder="{key}"] .mat-mdc-select-trigger')
                                                id_locator = page.locator(f'[id="{key}"] .mat-mdc-select-trigger')
                                                if form_locator.count() > 0:
                                                    locator = form_locator.nth(0)
                                                elif placeholder_locator.count() > 0:
                                                    locator = placeholder_locator.nth(0)
                                                elif id_locator.count() > 0:
                                                    locator = id_locator.nth(0)
                                                locator.scroll_into_view_if_needed()
                                                locator.click(force=True)
                                            else:
                                                if ((module == 'ECF' and client == 'NF') or (module == 'Vendor' and client == 'WR' and key == 'create_pan') or (module == 'ECF' and client == 'KVB') or (module == 'Vendor' and client == 'VBHC' and key not in ['mat-select-value-1', 'catalog-0005'])):
                                                    locator.click(force=True)
                                                    locator.fill(value)
                                                    if module == 'Vendor' and client == 'WR' and key=='create_pan':
                                                        locator.first.press("Enter")
                                                else:
                                                    locator.fill(value)
                                            options = page.locator('mat-option')
                                            if options.count() > 0:
                                                if module!='TA':
                                                    locator.press("Backspace")
                                                page.wait_for_timeout(2000)
                                                mat_option = page.locator(f'mat-option >> text="{value}"')
                                                if mat_option.count() > 0:
                                                    mat_option.first.click()
                                                else:
                                                    options.nth(0).click()
                                                success_fields.append(key)
                                        except:
                                            locator.click()
                                            page.locator(f'mat-option >> text="{value}"').click()
                                            success_fields.append(key)
                                    success_fields.append(key)
                                except Exception as e:
                                    fail_fields.append(key)
                                    stop_current_run = True
                                    logger.error(f'fail_field:{key}:{value}')
                                    break
                        status = "✓" if not fail_fields else "✗"
                        section_status_dict[section_key] = status
                        scenrios_status_dict[scenario_name]='Processing'
                        def section_status_update():
                            Testcase_Result.objects.filter(id=test_id).update(
                                test_implement_status=section_status_dict,
                                status="Processing",
                                environment=environment,
                                updated_date=datetime.now(),
                                updated_by=user_id
                            )
                            Testcase_Run.objects.filter(Testcase_code=testcode).update(status=scenrios_status_dict, updated_date=datetime.now(), updated_by=user_id)
                            Batchcode.objects.filter(batch_code=batchcode).update(status="Processing",updated_date=datetime.now(),updated_by=user_id)
                        t = Thread(target=section_status_update)
                        t.start()
                        t.join()
                        logger.info(f"{section_key} : {status}")

                    code = None
                    rows = page.locator('tbody tr')
                    if module in ['Vendor', 'TA'] and status != '✗' and rows.count() > 0:
                        code = rows.nth(0).locator('td').nth(1).inner_text()
                        logger.info(f"First row code: {code}")
                    elif module in ['ECF','PRPO'] and status != '✗':
                        code = rows.first.locator("td").nth(2).inner_text()
                        logger.info(f"First row code:{code}")

                    if code and ((module in ['Vendor', 'ECF', 'TA', 'JV'] and index == 0) or (module == 'PRPO' and index % 2 == 0)):
                        runtime_context["code"] = code
                        logger.info(f"Runtime context updated: {runtime_context}")

                    if client == 'NF' and status != '✗':
                        page.get_by_text("person").click()
                        page.locator("a").filter(has_text="Logout").click()
                        logger.info("Logged out")
                    elif client in ['NAC', 'KVB', 'VBHC'] and status != '✗':
                        page.get_by_text("logout", exact=True).click()

                    if "✗" in section_status_dict.values():
                        final_status = "Failed"
                        final_result = "Fail"
                    else:
                        final_status = "Success"
                        final_result = "Pass"

                    scenrios_status_dict[scenario_name] = final_status
                    def save_result():
                        Testcase_Result.objects.filter(id=test_id).update(
                            client_name=client,
                            status=final_status,
                            Testcase_Result=final_result,
                            inputdata=input_str,
                            outputdata=json.dumps(input_data),
                            screenshoot=json.dumps(screenshot_paths),
                            code=runtime_context.get("code", ""),
                            Message=message,
                            Module=module,
                            environment=environment,
                            updated_date=datetime.now(),
                            updated_by=user_id
                        )

                        Testcase_Run.objects.filter(Testcase_code=testcode).update(
                            status=scenrios_status_dict,
                            updated_date=datetime.now(),
                            updated_by=user_id
                        )
                        # Batchcode.objects.filter(batch_code=batchcode).update(status=final_status, updated_date=datetime.now(), updated_by=user_id)
                    t2 = Thread(target=save_result)
                    t2.start()
                    continue
            except Exception as e:
                logger.error(f"Error in ECF creation:{e}")
                def save_result():
                    Testcase_Result.objects.filter(id=test_id).update(
                        client_name=client,
                        status='Failed',
                        Testcase_Result='Fail',
                        inputdata=input_str,
                        outputdata=json.dumps(input_data),
                        screenshoot=json.dumps(screenshot_paths),
                        Module=module,
                        remarks=str(e),
                        Message=message,
                        environment=environment,
                        updated_date=datetime.now(),
                        updated_by=user_id,
                        test_implement_status=section_status_dict
                    )
                    Testcase_Run.objects.filter(Testcase_code=testcasecode).update(status=scenrios_status_dict,updated_date=datetime.now(), updated_by=user_id)
                    # Batchcode.objects.filter(batch_code=batchcode).update(status='Failed', updated_date=datetime.now(), updated_by=user_id)
                Thread(target=save_result).start()
                context.close()
                browser.close()
                continue
            finally:
                if context:
                    context.close()
                if browser:
                    browser.close()
                if playwright:
                    playwright.stop()
        has_failed = Testcase_Result.objects.filter(batch_code=batchcode, status='Failed').exists()
        Batchcode.objects.filter(batch_code=batchcode).update(status='Failed' if has_failed else 'Success',updated_date=datetime.now(),updated_by=user_id)

    def report_summary(self,vys_page,client,envir,module,code,status,from_date,to_date,batch_code,user_id):
        condition = Q()
        if client is not None:
            condition &= Q(client_name=client)
        if envir is not None:
            condition &= Q(environment=envir)
        if module is not None:
            condition &= Q(Module=module)
        if code is not None:
            condition &= Q(Testcase_code=code)
        if status is not None:
            condition &= Q(status=status)
        if from_date is not None and to_date is not None:
            condition &= Q(created_date__range=[from_date, to_date])
        elif from_date is not None:
            condition &= Q(created_date=from_date)
        elif to_date is not None:
            condition &= Q(created_date=to_date)
        if batch_code is not None:
            condition &= Q(batch_code=batch_code)
        template = Testcase_Result.objects.order_by('-id').filter(condition, created_by=user_id).values()[
                     vys_page.get_offset():vys_page.get_query_limit()]
        empty_list = VysfinList()
        for i in template:
            temp_response = Aut_Response()
            temp_response.set_id(i['id'])
            temp_response.set_client_name(i['client_name'])
            temp_response.set_project_module(i['Module'])
            temp_response.set_testcase_code(i['Testcase_code'])
            temp_response.set_Testcase_scenario_name(i['Test_scnarios'])
            temp_response.set_updated_date(i['created_date'].strftime('%d-%m-%Y'))
            temp_response.set_status(i['status'])
            temp_response.set_environment(i['environment'])
            temp_response.set_batch_code(i['batch_code'])
            temp_response.set_crno(i['code'])
            user_id = i['updated_by']
            name_fetch = Employee.objects.filter(user_id=user_id).values('user_name')
            name = name_fetch[0]['user_name']
            temp_response.set_name(name)
            empty_list.append(temp_response)
            vpage = VysfinPaginator(template, vys_page.get_index(), 10)
            empty_list.set_pagination(vpage)
        return empty_list

    def template_summary(self,vys_page,status,client,envir,module,code):
        condition = Q()
        if status is not None:
            condition &= Q(status__in=status)
        if client is not None:
            condition &= Q(client_name=client)
        if envir is not None:
            condition &= Q(environment=envir)
        if module is not None:
            condition &= Q(module=module)
        if code is not None:
            condition &= Q(Testcase_code=code)
        template = Testcase_Scenario_Template.objects.order_by('-created_date').filter(condition).values()[
                     vys_page.get_offset():vys_page.get_query_limit()]
        empty_list = VysfinList()
        for i in template:
            temp_response = Aut_Response()
            temp_response.set_id(i['id'])
            temp_response.set_environment(i['environment'])
            temp_response.set_client_name(i['client_name'])
            temp_response.set_project_module(i['Project_module'])
            testcase_template = ast.literal_eval(i['Testcase_scenario_template'])
            scenario_names = [entry.get('Testcase_scnarios', 'Unnamed Scenario') for entry in testcase_template.get('data', [])]
            temp_response.set_Testcase_scenario_name(scenario_names)
            temp_response.set_createddate(i['created_date'].strftime('%d-%m-%Y'))
            temp_response.set_updated_date(i['updated_date'].strftime('%d-%m-%Y'))
            temp_response.set_activeinactive(i['active'])
            temp_response.set_status(i['full_partial'])
            temp_response.set_testcase_code(i['Testcase_code'])
            temp_response.set_scenario_name(i['Testcase_scenario_name'])
            empty_list.append(temp_response)
        vpage = VysfinPaginator(template, vys_page.get_index(), 10)
        empty_list.set_pagination(vpage)
        return empty_list

    def status_change(self,id,status):
        Testcase_Scenario_Template.objects.filter(id=id).update(active=status)
        Testcase_Run.objects.filter(testcase_scn_id=id).update(active=status)
        if status == 1:
            success_obj.set_status(SuccessStatus.SUCCESS)
            success_obj.set_message("Template active Suceessfully")
            return success_obj
        else:
            success_obj.set_status(SuccessStatus.SUCCESS)
            success_obj.set_message("Template inactive Suceessfully")
            return success_obj


    def run_summary(self,vys_page,status,client,envir,module,code,user_id):
        condition = Q()
        if status is not None:
            condition &= Q(status__in=status)
        if client is not None:
            condition &= Q(client_name=client)
        if envir is not None:
            condition &= Q(environment=envir)
        if module is not None:
            condition &= Q(module=module)
        if code is not None:
            condition &= Q(Testcase_code=code)
        template = Testcase_Run.objects.order_by('-updated_date').filter(condition,active=1,created_by=user_id).values()[
                     vys_page.get_offset():vys_page.get_query_limit()]
        empty_list = VysfinList()
        for i in template:
            temp_response = Aut_Response()
            temp_response.set_id(i['id'])
            temp_response.set_environment(i['environment'])
            temp_response.set_client_name(i['client_name'])
            temp_response.set_project_module(i['module'])
            temp_response.set_testcase_code(i['Testcase_code'])
            temp_response.set_status(i['status'])
            testcase_template = json.loads(i['Testcase_template_input'])
            # scenario_name = testcase_template['data'][0]['Testcase_scnarios']
            # temp_response.set_Testcase_scenario_name(scenario_name)
            scenario_names = [entry.get('Testcase_scnarios', 'Unnamed Scenario') for entry in testcase_template['data']]
            temp_response.set_Testcase_scenario_name(scenario_names)
            temp_response.set_createddate(i['created_date'].strftime('%d-%m-%Y'))
            temp_response.set_updated_date(i['updated_date'].strftime('%d-%m-%Y'))
            temp_response.set_batch_code(i['batch_code'])
            temp_response.set_scenario_name(i['Testcase_scenario_name'])
            user_id = i['updated_by']
            name_fetch = Employee.objects.filter(user_id=user_id).values('user_name')
            name = name_fetch[0]['user_name']
            temp_response.set_name(name)
            empty_list.append(temp_response)
        vpage = VysfinPaginator(template, vys_page.get_index(), 10)
        empty_list.set_pagination(vpage)
        return empty_list


    def process_summary(self,test_id):
            testcase_code = Testcase_Result.objects.get(id=test_id)
            data = {
                'Teststatus': testcase_code.test_implement_status,
                'status': testcase_code.status,
            }
            return data

    def get_scnario_name(self, testcasecode, user_id):
        try:
            test_codes = ast.literal_eval(testcasecode)

            # 1. Check existing results
            existing_results = Testcase_Result.objects.filter(
                Testcase_code__in=test_codes,
                status='Yet to start',
                created_by = user_id
            )

            if existing_results.exists():
                existing_data = [
                    {
                        "id": result.id,
                        "Testcase_code": result.Testcase_code,
                        "Test_scnarios": result.Test_scnarios,
                        "test_implement_status": result.test_implement_status,
                        "status": result.status,
                        "batch_code": result.batch_code
                    }
                    for result in existing_results
                ]
                return {"data": existing_data}

            batchcode = f"RUN{datetime.now().strftime('%y%m%d%H%M%S')}"
            created_entries = []

            # 2. Loop through multiple testcase codes
            testcase_objs = Testcase_Run.objects.filter(Testcase_code__in=test_codes)

            if not testcase_objs.exists():
                return {"error": "Testcase code not found."}

            for testcase_obj in testcase_objs:

                parsed_data = json.loads(testcase_obj.Testcase_template_input)
                scenarios = [item['Testcase_scnarios'] for item in parsed_data.get('data', [])]
                test_scenario_name = testcase_obj.Testcase_scenario_name

                for scenario in scenarios:
                    result_obj = Testcase_Result.objects.create(
                        Testcase_code=testcase_obj.Testcase_code,
                        Test_scnarios=scenario,
                        status="Yet to start",
                        test_implement_status="Yet to start",
                        created_date=datetime.now(),
                        created_by=user_id,
                        updated_date=datetime.now(),
                        updated_by=user_id,
                        Testcase_scenario_name=test_scenario_name,
                        batch_code=batchcode,
                        url=testcase_obj.url
                    )

                    created_entries.append({
                        "id": result_obj.id,
                        "Testcase_code": result_obj.Testcase_code,
                        "Test_scnarios": result_obj.Test_scnarios,
                        "status": result_obj.status,
                        "test_implement_status": result_obj.test_implement_status,
                        "Testcase_scenario_name": result_obj.Testcase_scenario_name,
                        "batch_code":result_obj.batch_code,
                        "url":result_obj.url
                    })
            Testcase_Run.objects.filter(Testcase_code__in=test_codes).update(batch_code=batchcode)
            Batchcode.objects.create(batch_code=batchcode,created_date=datetime.now(),created_by=user_id,updated_date=datetime.now(),updated_by=user_id,status='Started')
            return {"data": created_entries}

        except Exception as e:
            return {"error": str(e)}

    def dropdown_teastcasecode(self, clientname,module,environment):
        condition = Q()
        if clientname is not None:
            condition &= Q(client_name=clientname)
        if environment is not None:
            condition &= Q(environment=environment)
        if module is not None:
            condition &= Q(module=module)
        code=Testcase_Run.objects.filter(condition,full_partial=Status.complete,active=1).order_by('-updated_date', '-id')
        testcode=[]

        for i in code:
            case=i.Testcase_code
            testcode.append(case)
        return testcode

    def get_testcase(self,batchcode, user_id, vys_page):
        result = Testcase_Result.objects.order_by('id').filter(batch_code=batchcode,created_by=user_id).values()[
                     vys_page.get_offset():vys_page.get_query_limit()]
        empty_list = VysfinList()
        for i in result:
            temp_response = Aut_Response()
            temp_response.set_id(i['id'])
            temp_response.set_batch_code(i['batch_code'])
            temp_response.set_testcase_code(i['Testcase_code'])
            temp_response.set_Testcase_scenario_name(i['Test_scnarios'])
            temp_response.set_run_status(i['test_implement_status'])
            temp_response.set_status(i['status'])
            temp_response.set_environment(i['environment'])
            temp_response.set_project_module(i['Module'])
            temp_response.set_client_name(i['client_name'])
            empty_list.append(temp_response)
        vpage = VysfinPaginator(result, vys_page.get_index(), 10)
        empty_list.set_pagination(vpage)
        return empty_list

    def batch_summary(self,vys_page,status,client,envir,module,code,from_date,to_date,user_id):
        condition = Q()
        if status is not None:
            condition &= Q(status__in=status)
        if client is not None:
            condition &= Q(client_name=client)
        if envir is not None:
            condition &= Q(environment=envir)
        if module is not None:
            condition &= Q(module=module)
        if code is not None:
            condition &= Q(batch_code=code)
        if from_date is not None and to_date is not None:
            condition &= Q(created_date__range=[from_date, to_date])
        elif from_date is not None:
            condition &= Q(created_date=from_date)
        elif to_date is not None:
            condition &= Q(created_date=to_date)
        template = Batchcode.objects.order_by('-updated_date').filter(condition,created_by=user_id).values()[
                     vys_page.get_offset():vys_page.get_query_limit()]
        empty_list = VysfinList()
        for i in template:
            temp_response = Aut_Response()
            temp_response.set_id(i['id'])
            temp_response.set_environment(i['environment'])
            temp_response.set_client_name(i['client_name'])
            temp_response.set_project_module(i['Module'])
            temp_response.set_status(i['status'])
            temp_response.set_createddate(i['created_date'].strftime('%d-%m-%Y'))
            temp_response.set_updated_date(i['updated_date'].strftime('%d-%m-%Y'))
            temp_response.set_batch_code(i['batch_code'])
            user_id = i['updated_by']
            name_fetch = Employee.objects.filter(user_id=user_id).values('user_name')
            name = name_fetch[0]['user_name']
            temp_response.set_name(name)
            empty_list.append(temp_response)
        vpage = VysfinPaginator(template, vys_page.get_index(), 10)
        empty_list.set_pagination(vpage)
        return empty_list





class masterserv():
    def insert_client(self, data_list):
        for data in data_list.get('data'):
            if 'id' in data:
                Client.objects.filter(id=data['id']).update(
                    client_name = data['client'],
                    updated_date = datetime.now()
                )

            else:
                Client.objects.create(
                    client_name=data['client'],
                    created_date=datetime.now()
                )

        success_obj.set_status(SuccessStatus.SUCCESS)
        success_obj.set_message(SuccessMessage.CREATE_MESSAGE)
        return success_obj

    def insert_module(self, data_list):
        for data in data_list.get('data'):
            client = Client.objects.filter(client_name=data['client']).values('id').first()
            client_id = client['id']
            if 'id' in data:
                Module_master.objects.filter(id=data['id']).update(
                    client_id = client_id,
                    Project_module = data['module'],
                    updated_date = datetime.now()
                )

            else:
                Module_master.objects.create(
                    client_id =client_id,
                    Project_module=data['module'],
                    created_date=datetime.now()
                )
        success_obj.set_status(SuccessStatus.SUCCESS)
        success_obj.set_message(SuccessMessage.CREATE_MESSAGE)
        return success_obj