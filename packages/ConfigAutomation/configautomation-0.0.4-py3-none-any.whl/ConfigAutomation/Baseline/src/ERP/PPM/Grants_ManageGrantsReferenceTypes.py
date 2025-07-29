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
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Grants Reference Types")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Grants Reference Types", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(1000)
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(1000)
        # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"].strftime("%m/%d/%Y"))
        page.locator("//input[contains(@id,'id1')]").first.fill(datadictvalue["C_FROM_DATE"].strftime('%m/%d/%y'))
        if datadictvalue["C_TO_DATE"] != '':
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"].strftime("%m/%d/%Y"))
            page.locator("//input[contains(@id,'id3')]").first.fill(datadictvalue["C_TO_DATE"].strftime('%m/%d/%y'))
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)

        i = i + 1

        if i == rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(5000)
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Grants Reference Types saved Successfully")
            datadictvalue["RowStatus"] = "Grants Reference Types added successfully"

        except Exception as e:
            print("Grants Reference Types not saved")
            datadictvalue["RowStatus"] = "Grants Reference Types not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, GRANTS_REF_TYPES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, GRANTS_REF_TYPES,
                             PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, GRANTS_REF_TYPES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[0] + "_" + GRANTS_REF_TYPES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[
            0] + "_" + GRANTS_REF_TYPES + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
