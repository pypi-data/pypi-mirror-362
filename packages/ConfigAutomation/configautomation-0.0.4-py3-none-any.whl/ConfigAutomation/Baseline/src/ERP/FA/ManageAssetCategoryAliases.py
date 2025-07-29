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
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Asset Category Aliases")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Asset Category Aliases", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_role("table", name="Search Results").get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_title("Search: Major Category").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Value").fill(datadictvalue["C_MAJOR_CTGRY"])
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("cell", name=datadictvalue["C_MAJOR_CTGRY"], exact=True).nth(1).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(500)
        page.get_by_title("Search: Minor Category").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Value").fill(datadictvalue["C_MINOR_CTGRY"])
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("cell", name=datadictvalue["C_MINOR_CTGRY"], exact=True).nth(1).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)
        page.get_by_role("table", name="Search Results").get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        if datadictvalue["C_ENBLD"] == 'Yes':
            if not page.get_by_role("table", name="Search Results").locator("//input[@type='checkbox']").is_checked():
                page.get_by_role("table", name="Search Results").locator("//input[@type='checkbox']").click()

        elif datadictvalue["C_ENBLD"] == 'No':
            if page.get_by_role("table", name="Search Results").locator("//input[@type='checkbox']").is_checked():
                page.get_by_role("table", name="Search Results").locator("//input[@type='checkbox']").click()
        # page.get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_START_DATE"])
        # page.get_by_placeholder("m/d/yy").nth(1).fill(datadictvalue["C_END_DATE"])
        page.wait_for_timeout(2000)

        # Save the data
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        if page.locator("//div[text()='Warning']//following::button[1]").is_visible():
            page.locator("//div[text()='Warning']//following::button[1]").click()
        if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
            page.locator("//div[text()='Confirmation']//following::button[1]").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Asset Category Aliases saved Successfully")
            datadictvalue["RowStatus"] = "Asset Category Aliases added successfully"

        except Exception as e:
            print("Asset Category Aliases not saved")
            datadictvalue["RowStatus"] = "Asset Category Aliases not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_CATEGORY_ALIASES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_CATEGORY_ALIASES, PRCS_DIR_PATH + FA_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + FA_WORKBOOK, MANAGE_CATEGORY_ALIASES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANAGE_CATEGORY_ALIASES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[
            0] + "_" + MANAGE_CATEGORY_ALIASES + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
