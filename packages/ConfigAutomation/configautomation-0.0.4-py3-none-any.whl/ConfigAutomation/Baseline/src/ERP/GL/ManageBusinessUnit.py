
from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)

    page.get_by_role("textbox").fill("Manage Business Unit")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Business Unit", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Create").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(10000)
        page.get_by_label("Name").fill(datadictvalue["C_BSNSS_UNIT_NAME"])
        page.get_by_label("Location").fill(datadictvalue["C_LCTN"])
        page.get_by_label("Manager").fill(datadictvalue["C_MNGR"])
        page.get_by_label("Default Set").fill(datadictvalue["C_DFLT_SET"])

        if datadictvalue["C_ACTV"] == 'Yes':
            if not page.get_by_text("Active").is_checked():
                page.get_by_text("Active").click()
        elif datadictvalue["C_ACTV"] == 'No':
            if page.get_by_text("Active").is_checked():
                page.get_by_text("Active").click()

        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Save and Close").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("BU Created Successfully")
            datadictvalue["RowStatus"] = "BU Created Successfully"

        except Exception as e:
            print("BU not saved")
            datadictvalue["RowStatus"] = "BU not saved"
    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, BU):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, BU, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, BU)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + BU)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + BU + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))