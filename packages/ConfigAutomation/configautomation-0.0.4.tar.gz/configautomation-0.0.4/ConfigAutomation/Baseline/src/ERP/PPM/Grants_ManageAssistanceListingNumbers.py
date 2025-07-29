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
    page.get_by_role("textbox").fill("Manage Assistance Listing Numbers")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Manage Assistance Listing Numbers", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Number").fill(str(datadictvalue["C_NMBR"]))
        page.get_by_label("Program Title").fill(datadictvalue["C_PRGRM_TITLE"])
        page.get_by_label("Agency").fill(datadictvalue["C_AGNCY"])
        page.get_by_label("Assistance Type").fill(datadictvalue["C_ASSSTNC_TYPE"])
        if datadictvalue["C_LAST_UPDTD_DATE"] != '':
            page.locator("//a[@title='Select Date']//preceding::input[contains(@id,'id1')]").first.fill(datadictvalue["C_LAST_UPDTD_DATE"].strftime("%m/%d/%Y"))
        if datadictvalue["C_PBLSHD_DATE"] != '':
            page.locator("//a[@title='Select Date']//preceding::input[contains(@id,'id2')]").first.fill(datadictvalue["C_PBLSHD_DATE"].strftime("%m/%d/%Y"))

        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)

        i = i + 1

        if i == rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(8000)
    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Assistance Listing Numbers saved Successfully")
        datadictvalue["RowStatus"] = "Assistance Listing Numbers added successfully"

    except Exception as e:
        print("Assistance Listing Numbers not saved")
        datadictvalue["RowStatus"] = "Assistance Listing Numbers not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, ASSIST_LISTING_NUMBER):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, ASSIST_LISTING_NUMBER,
                             PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, ASSIST_LISTING_NUMBER)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[0] + "_" + ASSIST_LISTING_NUMBER)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[
            0] + "_" + ASSIST_LISTING_NUMBER + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))