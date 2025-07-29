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
    page.get_by_role("textbox").fill("Manage Trading Community Source Systems")
    page.get_by_role("button", name="Search").click()
    page.get_by_role("link", name="Manage Trading Community Source Systems", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Code", exact=True).fill(datadictvalue["C_CODE"])
        page.get_by_role("combobox", name="Type").click()
        page.wait_for_timeout(2000)
        page.get_by_text(datadictvalue["C_TYPE"], exact=True).click()
        if datadictvalue["C_ENBL_FOR_ITEMS"] == 'Yes':
            page.get_by_text("Enable for Items").check()
        if datadictvalue["C_ENBL_FOR_TRDNG_CMMNTY_MMBRS"] == 'Yes':
            page.get_by_text("Enable for Trading Community Members").check()
        if datadictvalue["C_ENBL_FOR_ORDER_ORCHSTRTN_AND_PLNNNG"] == 'Yes':
            page.get_by_text("Enable for Order Orchestration and Planning").check()
        if datadictvalue["C_ENBL_FOR_ASSTS"] == 'Yes':
            page.get_by_text("Enable for Assets").check()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()

        i = i + 1
    page.get_by_role("button", name="Done").click()


    # Validation
    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("AR-Manage Trading Community Source Rules Executed Successfully")

    except Exception as e:
        print("AR-Manage Trading Community Source Rules Executed UnSuccessfully")
    page.get_by_role("button", name="Done").click()

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, TRADING_COMMUNITY_SOURCE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, TRADING_COMMUNITY_SOURCE, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, TRADING_COMMUNITY_SOURCE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + TRADING_COMMUNITY_SOURCE)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + TRADING_COMMUNITY_SOURCE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
