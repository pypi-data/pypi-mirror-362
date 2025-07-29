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
    page.get_by_role("textbox").fill("Manage Ceilings")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Ceilings", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(500)
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(500)
        page.get_by_label("Reference Data Set").select_option(datadictvalue["C_RFRNC_DATA_SET"])
        page.wait_for_timeout(500)

        page.get_by_label("Ceiling Type").select_option(datadictvalue["C_CLNG_TYPE"])
        page.get_by_label("Currency").click()
        page.get_by_label("Currency").select_option(datadictvalue["C_CRRNCY"])
        page.wait_for_timeout(1000)

        #Amounts

        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(1000)
        page.get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_FROM_DATE_PLCD_IN_SRVC"])
        page.get_by_placeholder("m/d/yy").nth(1).fill(datadictvalue["C_TO_DATE_PLCD_IN_SRVC"])
        if page.get_by_label("Year of Life").is_visible():
            page.get_by_label("Year of Life").fill(str(datadictvalue["C_YEAR_OF_LIFE"]))
        page.get_by_label("Amount").fill(str(datadictvalue["C_AMNT"]))

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
            print("Ceiling created Successfully")
            datadictvalue["RowStatus"] = "Ceiling created successfully"

        except Exception as e:
            print("Ceiling not saved")
            datadictvalue["RowStatus"] = "Ceiling not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_DEPRECIATION_CEILING):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_DEPRECIATION_CEILING, PRCS_DIR_PATH + FA_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + FA_WORKBOOK, MANAGE_DEPRECIATION_CEILING)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANAGE_DEPRECIATION_CEILING)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[
            0] + "_" + MANAGE_DEPRECIATION_CEILING + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

