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
    page.get_by_role("textbox").fill("Manage Project Unit Set Assignments")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Project Unit Set Assignments", exact=True).click()

    #Manage Project Unit Set Assignments
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        # Select Name
        page.get_by_title("Search:  Name").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Name").click()
        page.get_by_role("textbox", name="Name").fill(datadictvalue["C_NAME"])
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_NAME"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        # page.get_by_text(datadictvalue["C_NAME"], exact=True).click()
        page.get_by_role("link", name=(datadictvalue["C_NAME"])).click()
        page.get_by_role("button", name="Edit").click()
        page.wait_for_timeout(2000)

        #Select Project Definition
        page.get_by_role("cell", name="Project Definition", exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_title("Search: Reference Data Set").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Reference Data Set Code").click()
        page.get_by_role("textbox", name="Reference Data Set Code").fill(datadictvalue["C_PRJCT_DFNTN_RFRNC_DATA_SET_CODE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name=(datadictvalue["C_PRJCT_DFNTN_RFRNC_DATA_SET_CODE"]), exact=True).click()
        # page.get_by_text(datadictvalue["C_PRJCT_DFNTN_RFRNC_DATA_SET_CODE"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        # Select Project Transaction Types
        page.get_by_text("Project Transaction Types").click()
        # page.get_by_role("cell", name="Project Transaction Types", exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_title("Search: Reference Data Set").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Reference Data Set Code").click()
        page.get_by_role("textbox", name="Reference Data Set Code").fill( datadictvalue["C_PRJCT_TRNSCTN_TYPS_RFRNC_DATA_ST_CODE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name=(datadictvalue["C_PRJCT_TRNSCTN_TYPS_RFRNC_DATA_ST_CODE"]), exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        # Save and close the data
        page.get_by_role("button", name="Save", exact=True).click()
        page.get_by_role("button", name="Save and Close").click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1

        # Done
    page.get_by_role("button", name="Done").click()

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Project Unit Set Assignments Saved Successfully")
        datadictvalue["RowStatus"] = "Project Unit Set Assignments are added successfully"

    except Exception as e:
        print("Project Unit Set Assignments not saved")
        datadictvalue["RowStatus"] = "Project Unit Set Assignments are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict



# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_UNIT_SETS_ASSIGNMTS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_UNIT_SETS_ASSIGNMTS, PRCS_DIR_PATH + PPM_ORG_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_UNIT_SETS_ASSIGNMTS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_ORG_CONFIG_WRKBK)[0] + "_" + PRJ_UNIT_SETS_ASSIGNMTS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_ORG_CONFIG_WRKBK)[
            0] + "_" + PRJ_UNIT_SETS_ASSIGNMTS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))