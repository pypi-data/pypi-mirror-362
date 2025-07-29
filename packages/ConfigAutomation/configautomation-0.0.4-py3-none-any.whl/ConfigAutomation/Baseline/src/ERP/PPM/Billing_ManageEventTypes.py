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
    page.wait_for_timeout(3000)

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Manage Event Types")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Event Types", exact=True).click()

    # Create Service Types
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        # *Event Type
        page.get_by_role("button", name="Add Row").first.click()
        page.wait_for_timeout(2000)
        page.get_by_label("Event Type").click()
        page.get_by_label("Event Type").fill(datadictvalue["C_EVENT_TYPE"])

        # Description
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        # *[L]Revenue Category
        page.get_by_label("Revenue Category").select_option(datadictvalue["C_RVN_CTGRY"])
        page.wait_for_timeout(2000)

        # If C_RVN is True
        if datadictvalue["C_RVN"]=="TRUE":
            page.get_by_role("table", name='Manage Event Types').locator("//input[@type='checkbox']").first.check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_RVN"]=="FALSE":
            page.get_by_role("table", name='Manage Event Types').locator("//input[@type='checkbox']").first.uncheck()
            page.wait_for_timeout(2000)

        if datadictvalue["C_INVC"] == "TRUE":
            page.get_by_role("table", name='Manage Event Types').locator("//input[@type='checkbox']").nth(1).check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_INVC"] == "FALSE":
            page.get_by_role("table", name='Manage Event Types').locator("//input[@type='checkbox']").nth(1).uncheck()

        if datadictvalue["C_ALLOW_ADJSTMNTS"] == "TRUE":
            page.get_by_role("table", name='Manage Event Types').locator("//input[@type='checkbox']").nth(2).check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_ALLOW_ADJSTMNTS"] == "FALSE":
            page.get_by_role("table", name='Manage Event Types').locator("//input[@type='checkbox']").nth(2).uncheck()
            page.wait_for_timeout(2000)

        #From date
        page.locator("//input[contains(@id,'inputDate2')][1]").first.click()
        page.locator("//input[contains(@id,'inputDate2')][1]").first.fill(datadictvalue["C_FROM_DATE"].strftime('%m/%d/%y'))

        #To date
        page.locator("//input[contains(@id,'inputDate4')][1]").first.click()
        page.locator("//input[contains(@id,'inputDate4')][1]").first.fill(datadictvalue["C_TO_DATE"])

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1

    # Save & Close the data
    page.get_by_role("button", name="Save and Close").click()

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Manage Event Types Saved Successfully")
        datadictvalue["RowStatus"] = "Manage Event Types are added successfully"

    except Exception as e:
        print("Manage Event Types not saved")
        datadictvalue["RowStatus"] = "Manage Event Types are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_BILLING_CONFIG_WRKBK, EVENT_TYPES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_BILLING_CONFIG_WRKBK, EVENT_TYPES, PRCS_DIR_PATH + PPM_BILLING_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_BILLING_CONFIG_WRKBK, EVENT_TYPES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_BILLING_CONFIG_WRKBK)[0] + "_" + EVENT_TYPES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_BILLING_CONFIG_WRKBK)[
            0] + "_" + EVENT_TYPES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))