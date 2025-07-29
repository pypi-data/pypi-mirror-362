from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
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
    page.wait_for_timeout(5000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Receipt Application Exception Rules")
    # page.get_by_role("textbox").fill("Manage Value Sets")  #
    page.get_by_role("button", name="Search").click()
    # page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Receipt Application Exception Rules", exact=True).click()  #

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Set", exact=True).click()
        page.get_by_label("Set", exact=True).type(datadictvalue["C_SET"])
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.locator("//label[text()='Start Date']//following::input[1]").clear()
        page.locator("//label[text()='Start Date']//following::input[1]").fill(datadictvalue["C_START_DATE"])
        page.locator("//label[text()='End Date']//following::input[1]").clear()
        page.locator("//label[text()='End Date']//following::input[1]").fill(datadictvalue["C_END_DATE"])
        if datadictvalue["C_ACTV"] == 'Yes':
            if not page.get_by_text("Active").is_checked():
                page.get_by_text("Active").click()
        elif datadictvalue["C_ACTV"] == 'No':
            if page.get_by_text("Active").is_checked():
                page.get_by_text("Active").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Add Row").click()
        #page.get_by_role("table", name="Exception Rules").get_by_role("cell").first.click()
        page.get_by_role("table", name="Exception Rules").get_by_role("cell").first.click()
        page.get_by_label("Condition").select_option("1")
        #page.get_by_label("Condition").click()
        #page.get_by_label("Condition").select_option(datadictvalue["C_CNDTN"])
        page.get_by_label("Amount").fill(str(datadictvalue["C_AMNT"]))
        page.get_by_label("Percentage").fill(str(datadictvalue["C_PRCNTG"]))
        page.get_by_label("Action").select_option(datadictvalue["C_ACTN"])
        #page.get_by_role("row", name="Condition Amount Percentage").locator("label").nth(4).f(datadictvalue["C_USER_RVW_RQRD"])
        if datadictvalue["C_USER_RVW_RQRD"] == 'Yes':
            page.get_by_text("User Review Required", exact=True).click()
        page.get_by_role("button", name="Save and Close").click()

        i = i + 1
        page.get_by_role("button", name="Done").click()


# Validation
    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("AR-Manage Receipt Application Exception Rules Executed Successfully")

    except Exception as e:
        print("AR-Manage Receipt Application Exception Rules Executed UnSuccessfully")
    page.get_by_role("button", name="Done").click()

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, APP_EXCEPTION_RULES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, APP_EXCEPTION_RULES, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, APP_EXCEPTION_RULES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + APP_EXCEPTION_RULES)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + APP_EXCEPTION_RULES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
