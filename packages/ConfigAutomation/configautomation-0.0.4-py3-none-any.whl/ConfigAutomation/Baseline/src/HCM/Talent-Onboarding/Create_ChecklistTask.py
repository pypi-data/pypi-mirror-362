from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)

    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Checklist Templates")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Checklist Templates", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        #search and Select Step Name
        page.get_by_placeholder("Enter checklist name").click()
        page.get_by_placeholder("Enter checklist name").fill("")
        page.wait_for_timeout(1000)

        # Entering Checklist Name and click on checklist name
        page.get_by_placeholder("Enter checklist name").type(datadictvalue["C_STEP_NAME"])
        # page.get_by_role("link", name="Search").nth(1).click()
        page.locator("//h1[text()='Checklist Templates']//following::img[@title='Search']").click()
        page.wait_for_timeout(3000)
        page.get_by_role("link", name=datadictvalue["C_STEP_NAME"]).click()
        page.wait_for_timeout(4000)

        #Create Task
        page.get_by_role("link", name="Tasks").click()
        page.get_by_role("button", name="Create").click()
        page.get_by_text("Create Task", exact=True).click()
        page.wait_for_timeout(5000)
        page.get_by_label("Name", exact=True).click()
        page.get_by_label("Name", exact=True).type(datadictvalue["C_OB_NAME"])
        page.wait_for_timeout(3000)
        page.get_by_label("Sequence").fill("")
        page.get_by_label("Sequence").type(str(datadictvalue["C_OB_SQNC"]))
        page.get_by_label("Code", exact=True).click()
        page.wait_for_timeout(4000)
        page.get_by_label("Code", exact=True).fill("")
        page.get_by_label("Code", exact=True).type(datadictvalue["C_OB_CODE"])
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Status").click()
        page.get_by_text(datadictvalue["C_OB_STTS"], exact=True).click()
        page.wait_for_timeout(1000)
        if datadictvalue["C_OB_ELGBLTY_PRFL"]!='':
            page.get_by_label("Eligibility Profile").click()
            page.get_by_label("Eligibility Profile").clear()
            page.get_by_label("Eligibility Profile").type(datadictvalue["C_OB_ELGBLTY_PRFL"])

        # Selecting Required
        if datadictvalue["C_OB_RQRD"] == "Yes":
            if page.get_by_role("row", name="Required", exact=True).get_by_role("row").locator("label").is_visible():
                page.get_by_role("row", name="Required", exact=True).get_by_role("row").locator("label").click()
                page.wait_for_timeout(2000)

        # Action Name
        page.get_by_label("Target Duration").click()
        page.get_by_label("Target Duration").type(str(datadictvalue["C_OB_TRGT_DRTN"]))
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="UOM", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_TRGT_DRTN_UNIT"]).click()
        page.wait_for_timeout(1000)
        page.get_by_label("Expire").click()
        page.get_by_label("Expire").type(str(datadictvalue["C_OB_EXPR_DAYS"]))
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Days").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_EXPRY_RLTV_TO"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Performer", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_PRFRMR"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Owner", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_OWNER"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Task Type", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_TASK_TYPE"], exact=True).click()
        page.wait_for_timeout(5000)

        if datadictvalue["C_OB_TASK_TYPE"] == "Video":
            page.get_by_role("combobox", name="VideoAttrType").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VIDEO_TYPE"]).click()
            page.wait_for_timeout(3000)
            page.get_by_role("textbox", name="URL").click()
            page.get_by_label("URL").first.type(datadictvalue["C_URL"])
            page.wait_for_timeout(2000)

        if datadictvalue["C_OB_TASK_TYPE"] == "External URL":
            page.get_by_role("combobox", name="Task Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_TASK_TYPE"]).click()
            page.wait_for_timeout(3000)
            page.get_by_role("textbox", name="URL").click()
            page.get_by_label("URL").first.type(datadictvalue["C_URL"])
            page.wait_for_timeout(2000)

        if datadictvalue["C_OB_TASK_TYPE"] == "I-9 Verification":
            page.get_by_role("combobox", name="I-9 Section").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_I9_SCTN"]).click()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Template ID").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_I9_CNFGRTN"]).click()
            page.wait_for_timeout(2000)

        if datadictvalue["C_OB_TASK_TYPE"] == "Electronic Signature":
            page.get_by_role("combobox", name="Signature Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SGNTR_TYPE"]).click()
            page.wait_for_timeout(3000)
            page.get_by_role("textbox", name="Report Path").click()
            page.get_by_role("textbox", name="Report Path").type(datadictvalue["C_RPRT_PATH"])
            page.wait_for_timeout(1000)
            page.get_by_title("Search: DocumentTypeName").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Type", exact=True).click()
            page.get_by_label("Type", exact=True).type(datadictvalue["C_DCMNT_TYPE"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_DCMNT_TYPE"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Documents Are For").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DCMNT_ARE_FOR"]).click()
            page.wait_for_timeout(2000)

        if datadictvalue["C_OB_TASK_TYPE"] == "Application Task":
            page.get_by_role("combobox", name="Application Task").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_APPLCTN_TASK"]).click()
            page.wait_for_timeout(2000)

        if datadictvalue["C_OB_TASK_TYPE"] == "Document":
            # page.get_by_role("row", name="Attachments", exact=True).get_by_role("row").locator("label").click()
            page.locator("//label[text()='Attachments']//following::label[1]").click()
            page.wait_for_timeout(3000)
            page.get_by_title("Search: AttachmentDocumentTypeName").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Type", exact=True).click()
            page.get_by_label("Type", exact=True).type(datadictvalue["C_OB_ADD_ATTCHMNTS_TO_DCMNT_RCRDS"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_OB_ADD_ATTCHMNTS_TO_DCMNT_RCRDS"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Attachments Are For").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ATTCHMNTS_ARE_FOR"]).click()
            page.wait_for_timeout(2000)

        page.get_by_role("link", name="Notes").click()
        page.wait_for_timeout(5000)
        if not page.get_by_label("Editor editing area: main").is_visible():
            page.get_by_role("link", name="Notes").click()

        page.get_by_label("Editor editing area: main").click()
        page.get_by_label("Editor editing area: main").fill(datadictvalue["C_OB_NOTES"])
        page.wait_for_timeout(3000)

        # Saving and closing the Record
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)
        if page.get_by_text("Warning").is_visible():
            page.get_by_role("button", name="Yes").click()
            page.wait_for_timeout(7000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)

        try:
            expect(page.get_by_role("heading", name="Checklist Templates")).to_be_visible()
            print("Checklist Tasks for Preboarding & Onboarding Saved Successfully")
            datadictvalue["RowStatus"] = "Checklist Tasks for Preboarding & Onboarding Saved Successfully"
        except Exception as e:
            print("Checklist Tasks for Preboarding & Onboardings not saved")
            datadictvalue["RowStatus"] = "Checklist Tasks for Preboarding & Onboarding not added"

        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + ONBOARDING_CONFIG_WRKBK, CHECKLIST_TASK):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + ONBOARDING_CONFIG_WRKBK, CHECKLIST_TASK,PRCS_DIR_PATH + ONBOARDING_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + ONBOARDING_CONFIG_WRKBK, CHECKLIST_TASK)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", ONBOARDING_CONFIG_WRKBK)[0] + "_" + CHECKLIST_TASK)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", ONBOARDING_CONFIG_WRKBK)[0] + "_" + CHECKLIST_TASK + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




