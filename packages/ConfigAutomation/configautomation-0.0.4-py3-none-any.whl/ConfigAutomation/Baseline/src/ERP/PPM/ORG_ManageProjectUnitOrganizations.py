from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Manage Project Unit Organizations")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Project Unit Organizations", exact=True).click()

    # Create Service Types
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        # *Code
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Code").click()
        page.get_by_label("Code").fill(datadictvalue["C_CODE"])

        # *Name
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(2000)

        # Save & Close the data
        page.get_by_role("button", name="Save and Close").click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1

    # Save & Close the data
    page.get_by_role("button", name="Save and Close").click()

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Manage Project Unit Organizations Saved Successfully")
        datadictvalue["RowStatus"] = "Manage Project Unit Organizations are added successfully"

    except Exception as e:
        print("Manage Project Unit Organizations not saved")
        datadictvalue["RowStatus"] = "Manage Project Unit Organizations are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_UNIT_ORG):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_UNIT_ORG, PRCS_DIR_PATH + PPM_ORG_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_UNIT_ORG)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_ORG_CONFIG_WRKBK)[0] + "_" + PRJ_UNIT_ORG)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_ORG_CONFIG_WRKBK)[
            0] + "_" + PRJ_UNIT_ORG + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))