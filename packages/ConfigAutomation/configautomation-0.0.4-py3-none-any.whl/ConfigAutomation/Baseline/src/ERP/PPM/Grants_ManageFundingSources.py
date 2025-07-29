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
    page.get_by_role("textbox").fill("Manage Funding Sources")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Funding Sources").click()
    page.wait_for_timeout(2000)

    # Create Funding Sources
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Add").click()
        if datadictvalue["C_SRC_TYPE"] == 'Other Internal Funding Sources':
            page.locator("[id=\"__af_Z_window\"]").get_by_text("Add Internal Organization").click()
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
            page.get_by_text(datadictvalue["C_NAME"]).click()
            page.get_by_role("button", name="Next").click()
            if datadictvalue["C_NMBR"] != '':
                page.get_by_label("Number").click()
                page.get_by_label("Number").clear()
                page.get_by_label("Number").fill(str(datadictvalue["C_NMBR"]))
            page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Save and Close").click()


        elif datadictvalue["C_SRC_TYPE"] == 'External Funding Sources':
            page.get_by_text("Add Other Internal Funding").click()
            page.get_by_role("textbox", name="Name").fill(datadictvalue["C_NAME"])
            page.wait_for_timeout(5000)
            page.locator("//label[text()='Number']//following::input[1]").nth(1).click()
            page.locator("//label[text()='Number']//following::input[1]").nth(1).fill(str(datadictvalue["C_NMBR"]))
            page.locator("//label[text()='From Date']//following::input[1]").nth(0).fill(datadictvalue["C_FROM_DATE"])
            if datadictvalue["C_TO_DATE"] != '':
                page.locator("//label[text()='To Date']//following::input[1]").nth(0).fill(datadictvalue["C_TO_DATE"])
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

            # Save and Close
            page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1
    page.locator("//span[text()='ave and Close']").click()
    page.wait_for_timeout(2000)

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Funding Sources Saved Successfully")
        datadictvalue["RowStatus"] = "Funding Sources added successfully"

    except Exception as e:
        print("Funding Sources not saved")
        datadictvalue["RowStatus"] = "Funding Sources are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, FUND_SOURCES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, FUND_SOURCES,
                             PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, FUND_SOURCES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[0] + "_" + FUND_SOURCES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[
            0] + "_" + FUND_SOURCES + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))