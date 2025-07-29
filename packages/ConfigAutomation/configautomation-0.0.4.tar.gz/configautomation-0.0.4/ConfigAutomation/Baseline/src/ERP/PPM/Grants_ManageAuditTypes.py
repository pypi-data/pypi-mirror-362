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
    page.get_by_role("textbox").fill("Manage Audit Types")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Audit Types", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="New").nth(1).click()
        page.wait_for_timeout(2000)
        page.get_by_role("table", name='lookup codes').get_by_role("cell").get_by_label("Lookup Code", exact=True).nth(
            0).fill(datadictvalue["C_LKP_CODE"])
        if datadictvalue["C_DSPLY_SQNC"] != '':
            page.get_by_role("table", name='lookup codes').get_by_role("cell").get_by_label("Display Sequence").nth(
                0).fill(str(datadictvalue["C_DSPLY_SQNC"]))
        page.wait_for_timeout(2000)
        if datadictvalue["C_ENBLD"] == 'Yes':
            page.get_by_role("table", name='lookup codes').get_by_role("cell").locator("label").nth(2).check()
        if datadictvalue["C_ENBLD"] != 'Yes':
            page.get_by_role("table", name='lookup codes').get_by_role("cell").locator("label").nth(2).uncheck()
        if datadictvalue["C_START_DATE"] != '':
            # page.get_by_role("table", name='lookup codes').get_by_role("cell").get_by_role("cell",name="m/d/yy Press down arrow to access Calendar Start Date Select Date").get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_START_DATE"])
            page.locator("//input[contains(@id,'id2')]").nth(0).fill(datadictvalue["C_START_DATE"].strftime('%m/%d/%y'))
        if datadictvalue["C_END_DATE"] != '':
            # page.get_by_role("table", name='lookup codes').get_by_role("cell").get_by_role("cell",name="m/d/yy Press down arrow to access Calendar End Date Select Date").get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_END_DATE"])
            page.locator("//input[contains(@id,'id1')]").nth(0).fill(datadictvalue["C_END_DATE"].strftime('%m/%d/%y'))
        page.get_by_role("table", name='lookup codes').get_by_role("cell").get_by_label("Meaning").nth(0).fill(
            datadictvalue["C_MNNG"])
        page.get_by_role("table", name='lookup codes').get_by_role("cell").get_by_label("Description").nth(0).fill(
            datadictvalue["C_DSCRPTN"])
        page.get_by_role("table", name='lookup codes').get_by_role("cell").get_by_label("Tag").nth(0).fill(
            datadictvalue["C_TAG"])

        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)

        i = i + 1

        if i == rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(5000)
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Audit Types saved Successfully")
            datadictvalue["RowStatus"] = "Audit Types added successfully"

        except Exception as e:
            print("Audit Types not saved")
            datadictvalue["RowStatus"] = "Audit Types not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, AUDIT_TYPES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, AUDIT_TYPES,
                             PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, AUDIT_TYPES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[0] + "_" + AUDIT_TYPES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[
            0] + "_" + AUDIT_TYPES + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))