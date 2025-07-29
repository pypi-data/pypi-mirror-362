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
    page.wait_for_timeout(40000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Assignment Status")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Assignment Status", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("link", name="Assignment Statuses").click()
        page.get_by_role("button", name="Add").click()
        page.get_by_label("Status", exact=True).click()
        page.get_by_label("Status", exact=True).type(datadictvalue["C_USER_STTS"])
        page.get_by_label("Code").click()
        page.get_by_label("Code").type(datadictvalue["C_ASGNMNT_STTS_CODE"])
        page.get_by_role("combobox", name="Pay Status").click()
        page.get_by_text(datadictvalue["C_PAY_STTS"], exact=True).click()
        page.get_by_role("combobox", name="HR Status").click()
        page.get_by_text(datadictvalue["C_HR_STTS"], exact=True).click()
        page.locator("//label[text()='Start Date']//following::input[1]").clear()
        page.locator("//label[text()='Start Date']//following::input[1]").type(datadictvalue["C_START_DATE"].strftime('%m/%d/%y'))
        page.get_by_role("combobox", name="Default").click()
        page.wait_for_timeout(2000)
        page.get_by_text(datadictvalue["C_DFLT"],exact=True).click()
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(3000)
        if page.get_by_role("button", name="OK").is_visible():
            page.get_by_role("button", name="OK").click()
            page.get_by_role("button", name="Cancel").click()
            print("Assignment already available in Application")
        try:
            expect(page.get_by_role("heading", name="Workforce Structures")).to_be_visible()
            print("Assignment Saved Successfully")
            datadictvalue["RowStatus"] = "Assignment Saved"
        except Exception as e:
            print("Unable to save Assignment")
            datadictvalue["RowStatus"] = "Unable to save Assignment"

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Assignment Added Successfully"
        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_ASSGN_STATUS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_ASSGN_STATUS, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_ASSGN_STATUS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0]+ "_" + MANAGE_ASSGN_STATUS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + MANAGE_ASSGN_STATUS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
