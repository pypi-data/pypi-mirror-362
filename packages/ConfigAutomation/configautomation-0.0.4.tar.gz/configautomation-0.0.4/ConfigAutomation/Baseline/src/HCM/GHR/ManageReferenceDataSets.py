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

    page.get_by_role("textbox").fill("Manage Reference Data Sets")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Reference Data Sets").click()
    page.wait_for_timeout(2000)
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="New").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Set Code").nth(1).click()
        page.get_by_label("Set Code").nth(1).type(datadictvalue["C_CODE"])
        page.get_by_label("Set Name").nth(1).click()
        page.get_by_label("Set Name").nth(1).type(datadictvalue["C_NAME"])
        page.get_by_label("Description").click()
        page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Save", exact=True).click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"
        i = i + 1
        page.wait_for_timeout(5000)
    page.get_by_role("button", name="Save and Close").click()
    try:
        expect(page.get_by_role("link", name="Manage Reference Data Sets")).to_be_visible()
        print("Reference Data Set Saved")
        datadictvalue["RowStatus"] = "Reference Data Set Saved"
    except Exception as e:
        print("Unable to save rating model")
        datadictvalue["RowStatus"] = "Unable to save Reference Data Set"

    page.wait_for_timeout(2000)
    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, REFERENCE_DATA_SET):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, REFERENCE_DATA_SET, PRCS_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, REFERENCE_DATA_SET)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_ENTSTRUCT_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_ENTSTRUCT_CONFIG_WRKBK)[0] + "_" + REFERENCE_DATA_SET + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

