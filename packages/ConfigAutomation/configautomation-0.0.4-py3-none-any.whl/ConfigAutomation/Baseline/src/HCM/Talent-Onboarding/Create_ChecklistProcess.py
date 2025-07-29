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


    PrevOBName=''

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        if datadictvalue["C_OB_NAME"]!=PrevOBName:

            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)

            # Name
            page.get_by_label("Name", exact=True).clear()
            page.get_by_label("Name", exact=True).type(datadictvalue["C_OB_NAME"])

            # Checklist Code
            page.get_by_label("Checklist Code").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Checklist Code").clear()
            page.get_by_label("Checklist Code").type(datadictvalue["C_OB_CODE"])

            # Country
            page.get_by_label("Country").clear()
            page.get_by_label("Country").type(datadictvalue["C_OB_CNTRY"])

            # Category
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Category").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_CTGRY"], exact=True).click()
            page.wait_for_timeout(2000)

            #Archive After Months
            page.get_by_label("Archive After Months").clear()
            page.get_by_label("Archive After Months").type(str(datadictvalue["C_OB_ARCHV_AFTER_MNTHS"]))

            # Purge After Months
            page.get_by_label("Purge After Months").clear()
            page.get_by_label("Purge After Months").type(str(datadictvalue["C_OB_PURGE_AFTER_MNTHS"]))

            # Clicking on Ok Button
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(5000)

            # Action Name
            page.get_by_title("Search: Action Name").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_role("textbox", name="Action Name").type(datadictvalue["C_OB_ACTN_NAME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.locator("(//span[text()='Action Name']//following::span[text()='" + datadictvalue["C_OB_ACTN_NAME"] + "'])[1]").click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

            # Allocation Criteria
            if datadictvalue["C_OB_ALLCTN_CRTR"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Allocation Criteria").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_ALLCTN_CRTR"]).click()
                page.wait_for_timeout(2000)


            # Completion Criteria
            if datadictvalue["C_OB_CMPLTN_CRTR"]!='':
                page.get_by_role("combobox", name="Completion Criteria").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_CMPLTN_CRTR"]).click()
                page.wait_for_timeout(2000)

            # Status
            if datadictvalue["C_OB_STTS"]!='':
                page.get_by_role("combobox", name="Status").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_STTS"], exact=True).click()
                page.wait_for_timeout(2000)
            # Date From
            if datadictvalue["C_OB_DATE_FROM"]!='':
                # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar Date From Select Date",exact=True).get_by_placeholder("m/d/yy").clear()
                # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar Date From Select Date",exact=True).get_by_placeholder("m/d/yy").type(datadictvalue["C_OB_DATE_FROM"])
                page.locator("(//label[text()='Date From']//following::input[1])[1]").clear()
                page.locator("(//label[text()='Date From']//following::input[1])[1]").type(datadictvalue["C_OB_DATE_FROM"])

            # Date To
            if datadictvalue["C_OB_DATE_TO"]!='':
                # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar Date To Select Date",exact=True).get_by_placeholder("m/d/yy").clear()
                # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar Date To Select Date",exact=True).get_by_placeholder("m/d/yy").type(datadictvalue["C_OB_DT_T"])
                page.locator("(//label[text()='Date To']//following::input[1])[1]").clear()
                page.locator("(//label[text()='Date To']//following::input[1])[1]").type(datadictvalue["C_OB_DATE_TO"])

            # Eligibility Profile
            if datadictvalue["C_OB_ELGBLTY_PRFL"]!='':
                page.get_by_title("Search: Eligibility Profile").click()
                page.get_by_role("link", name="Search...").click()
                page.wait_for_timeout(2000)
                page.get_by_role("cell", name="Name Name Name Profile Usage").get_by_label("Name").type(datadictvalue["C_OB_ELGBLTY_PROFLE"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.wait_for_timeout(3000)
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_ELGBLTY_PRFL"],exact=True).click()
                page.get_by_role("button", name="OK").click()

            PrevOBName = datadictvalue["C_OB_NAME"]

            # Saving General Details
            page.get_by_role("button", name="Save", exact=True).click()
            page.get_by_role("button", name="OK").click()

            # Message
            page.get_by_role("link", name="Message").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Welcome Notification Title").click()
            page.get_by_label("Welcome Notification Title").type(datadictvalue["C_OB_WLCM_NTFCTN_TITLE"])
            page.get_by_label("Welcome Notification Text").click()
            page.get_by_label("Welcome Notification Text").type(datadictvalue["C_OB_WLCM_NTFCTN_TEXT"])

            page.get_by_role("button", name="Save", exact=True).click()
            page.wait_for_timeout(3000)
            if page.get_by_role("button", name="OK").is_visible():
                page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(4000)

        # Adding Tasks
        page.get_by_role("link", name="Tasks").click()
        page.get_by_role("button", name="Create").click()
        page.get_by_text("Create Task").click()

        # Name
        page.get_by_label("Name", exact=True).type(datadictvalue["C_OB_STEP_NAME"])

        # Code
        page.get_by_label("Code", exact=True).click()
        page.wait_for_timeout(5000)

        # Checklist Name
        page.get_by_title("Search: Checklist Name").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(2000)
        page.locator("//div[contains(@id,'checklistNameId::lovDialogId')]//following::input[@aria-label=' Name']").type(datadictvalue["C_OB_STEP_NAME"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_STEP_NAME"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)


        # Click on Save and Close for Task
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Click on Final Save and Close
        if i == rowcount:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)

        try:
            expect(page.get_by_role("heading", name="Checklist Templates")).to_be_visible()
            print("Checklists Process for Preboarding & Onboarding Saved Successfully")
            datadictvalue["RowStatus"] = "Checklists Process for Preboarding & Onboarding Saved Successfully"

        except Exception as e:
            print("Checklists Process for Preboarding & Onboardings not saved")
            datadictvalue["RowStatus"] = "Checklists Process for Preboarding & Onboarding not added"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + ONBOARDING_CONFIG_WRKBK, CHECKLIST_PROCESS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + ONBOARDING_CONFIG_WRKBK, CHECKLIST_PROCESS,PRCS_DIR_PATH + ONBOARDING_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + ONBOARDING_CONFIG_WRKBK, CHECKLIST_PROCESS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", ONBOARDING_CONFIG_WRKBK)[0] + "_" + CHECKLIST_PROCESS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", ONBOARDING_CONFIG_WRKBK)[0] + "_" + CHECKLIST_PROCESS + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




