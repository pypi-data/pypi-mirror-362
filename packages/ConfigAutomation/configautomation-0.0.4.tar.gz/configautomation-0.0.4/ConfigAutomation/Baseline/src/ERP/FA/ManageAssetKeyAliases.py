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
    page.get_by_role("textbox").fill("Manage Asset Key Aliases")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Asset Key Aliases").click()


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create").click()
        page.get_by_role("table", name="Search Results").get_by_label("Name").click()
        page.get_by_role("table", name="Search Results").get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Asset Key").click()
        page.get_by_label("Asset Key").fill(datadictvalue["C_SGMNT1"])
        page.wait_for_timeout(5000)

        #page.get_by_role("link", name="Search...").click()
        #page.get_by_label("Value").click()
        #page.get_by_label("Value").fill(datadictvalue["C_SGMNT1"])
        #page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        #page.wait_for_timeout(3000)
        #page.get_by_role("cell", name=datadictvalue["C_SGMNT1"], exact=True).click()
        #page.wait_for_timeout(3000)
        #page.get_by_role("button", name="OK").click()
        #page.wait_for_timeout(3000)

        page.get_by_role("table", name="Search Results").get_by_label("Description").click()
        page.get_by_role("table", name="Search Results").get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        page.wait_for_timeout(3000)

        if datadictvalue["C_ENBLD"] == 'Yes':
            if not page.get_by_role("table", name="Search Results").locator("//input[@type='checkbox']").is_checked():
                page.get_by_role("table", name="Search Results").locator("//input[@type='checkbox']").click()

        elif datadictvalue["C_ENBLD"] == 'No':
            if page.get_by_role("table", name="Search Results").locator("//input[@type='checkbox']").is_checked():
                page.get_by_role("table", name="Search Results").locator("//input[@type='checkbox']").click()

        # page.get_by_role("cell", name="Press down arrow to access Calendar Start Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_START_DATE"])
        # page.wait_for_timeout(3000)
        #
        # page.get_by_role("cell", name="Press down arrow to access Calendar End Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_END_DATE"])
        # page.wait_for_timeout(3000)

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        if page.get_by_role("button", name="Yes").is_visible():
            page.get_by_role("button", name="Yes").click()




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
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_ASSETKEY_ALIASES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_ASSETKEY_ALIASES, PRCS_DIR_PATH + FA_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + FA_WORKBOOK, MANAGE_ASSETKEY_ALIASES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANAGE_ASSETKEY_ALIASES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[
            0] + "_" + MANAGE_ASSETKEY_ALIASES + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




