from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *
from datetime import datetime


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Manage Payables Calendars")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Payables Calendars", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        #Enter the general info

        page.get_by_label("Name", exact=True).click()
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Calendar Type").select_option(datadictvalue["C_CLNDR_TYPE"])
        page.wait_for_timeout(2000)
        page.get_by_label("Period Frequency").select_option(datadictvalue["C_PRD_FRQNCY"])
        page.locator("//label[text()='Start Date']//following::input[1]").fill(datadictvalue["C_START_DATE"].strftime("%m/%d/%Y"))
        page.get_by_label("Period Name Format").select_option(datadictvalue["C_PRD_NAME_FRMT"])
        page.locator("//label[text()='From Date']//following::input[1]").fill(datadictvalue["C_FROM_DATE"].strftime("%m/%d/%Y"))
        page.locator("//label[text()='To Date']//following::input[1]").fill(datadictvalue["C_TO_DATE"].strftime("%m/%d/%Y"))

        # Add the Period Info
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Period Name Prefix").fill(datadictvalue["C_PRDS_NAME_PRFX"])
        page.get_by_label("Year").fill(str(datadictvalue["C_YEAR"]))
        page.get_by_label("Sequence").clear()
        page.get_by_label("Sequence").fill(str(datadictvalue["C_SQNC"]))
        page.locator("//span[text()='Start Date']//following::input[contains(@placeholder,'m/d/yy')][1]").fill(datadictvalue["C_PRD_START_DATE"].strftime("%m/%d/%Y"))
        page.locator("//span[text()='End Date']//following::input[contains(@placeholder,'m/d/yy')][2]").fill(datadictvalue["C_END_DATE"].strftime("%m/%d/%Y"))
        if page.locator("//span[text()='Due Date']//following::input[contains(@placeholder,'m/d/yy')][3]").is_visible():
            page.locator("//span[text()='Due Date']//following::input[contains(@placeholder,'m/d/yy')][3]").fill(datadictvalue["C_DUE_DATE"])

        # Save the data
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        i = i + 1
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Payables Calendars Saved Successfully")
            datadictvalue["RowStatus"] = "Payables Calendars are added successfully"

        except Exception as e:
            print("Payables Calendars not saved")
            datadictvalue["RowStatus"] = "Payables Calendars are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYABLES_CALENDAR):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYABLES_CALENDAR, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, PAYABLES_CALENDAR)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + PAYABLES_CALENDAR)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
            0] + "_" + PAYABLES_CALENDAR + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
