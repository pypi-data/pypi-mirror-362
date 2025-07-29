from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.wait_for_timeout(5000)
    page.get_by_placeholder("User name").click()
    page.get_by_placeholder("User name").fill(IMPLUSRID)
    page.get_by_role("textbox", name="Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox").type("Manage Business Unit")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.get_by_role("link", name="Manage Business Unit", exact=True).first.click()
        page.wait_for_timeout(4000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)
        page.get_by_role("heading", name="Create Business Unit").is_visible()
        page.get_by_label("Name").click()
        page.get_by_label("Name").type(datadictvalue["C_NAME"])
        # page.get_by_label("Manager").click()
        # page.get_by_label("Manager").type("")
        # page.get_by_label("Manager").press("Enter")
        page.get_by_label("Location").click()
        page.get_by_label("Location").type(datadictvalue["C_LCTN"])
        page.get_by_label("Location").press("Enter")
        if datadictvalue["C_STATUS"] == "A":
            if not page.locator('input[type=checkbox]').is_checked():
                page.locator('input[type=checkbox]').click()
        page.get_by_label("Default Set").click()
        page.get_by_label("Default Set").type(datadictvalue["C_DFLT_SET"])
        page.get_by_label("Default Set").press("Enter")
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(6000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)
        try:
            expect(page.get_by_role("link", name="Manage Business Unit", exact=True)).to_be_visible()
            print("Added Business Unit Saved Successfully")
            datadictvalue["RowStatus"] = "Added Business Unit and code"
        except Exception as e:
            print("Unable to save Business Unit")
            datadictvalue["RowStatus"] = "Unable to Add Business Unit and code"
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Added Business Unit Successfully"
        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, BUSINESS_UNIT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, BUSINESS_UNIT, PRCS_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, BUSINESS_UNIT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_ENTSTRUCT_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_ENTSTRUCT_CONFIG_WRKBK)[0] + "_" + BUSINESS_UNIT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
