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
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Asset keys")
    page.get_by_role("button", name="Search").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        page.wait_for_timeout(3000)
        page.get_by_role("link", name="Manage Asset keys").click()
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Add Row").click()

        #Asset key
        if page.get_by_label("Asset Key").is_visible():
            if datadictvalue["C_ASSET_KEY"]!= '':
                page.get_by_title("Search: Asset Key").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Value").click()
                page.get_by_label("Value").fill(datadictvalue["C_ASSET_KEY"])
                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
                page.wait_for_timeout(3000)
                page.get_by_role("cell", name=datadictvalue["C_ASSET_KEY"]).nth(1).click()
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)

        #Funding Source
        # if page.get_by_label("Funding Source").is_visible():
        #     page.get_by_title("Search: Funding Source").click()
        #     page.get_by_role("link", name="Search...").click()
        #     page.get_by_label("Value").click()
        #     page.get_by_label("Value").fill(datadictvalue[""])
        #     page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        #     page.get_by_role("cell", name=datadictvalue[""]).nth(1).click()
        #     page.get_by_role("button", name="OK").click()
        #     page.wait_for_timeout(3000)

        #Future Use

        # if page.get_by_label("Future Use").is_visible():
        #     page.get_by_title("Search: Future Use").click()
        #     page.get_by_role("link", name="Search...").click()
        #     page.get_by_label("Value").click()
        #     page.get_by_label("Value").fill(datadictvalue["C_SGMNT2"])
        #     page.get_by_label("Value").press("Enter")
        #     page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        #     page.get_by_role("cell", name=datadictvalue["C_SGMNT2"]).nth(1).click()
        #     page.wait_for_timeout(3000)
        #     page.get_by_role("button", name="OK").click()
        #     page.wait_for_timeout(3000)
        if datadictvalue['C_ENBLD'] == 'Yes':
            page.get_by_role("table", name="Search Results").locator("label").nth(3).click()

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Asset Keys Saved Successfully")
            datadictvalue["RowStatus"] = "Asset Keys saved successfully"

        except Exception as e:
            print("Asset Keys not saved")
            datadictvalue["RowStatus"] = "Asset Keys not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_ASSET_KEYS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_ASSET_KEYS, PRCS_DIR_PATH + FA_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + FA_WORKBOOK, MANAGE_ASSET_KEYS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANAGE_ASSET_KEYS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[
            0] + "_" + MANAGE_ASSET_KEYS + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




