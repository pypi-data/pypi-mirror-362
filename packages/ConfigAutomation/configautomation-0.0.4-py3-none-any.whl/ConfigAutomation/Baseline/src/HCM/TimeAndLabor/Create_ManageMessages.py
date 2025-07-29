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

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Manage Messages")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Messages", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)
        page.pause()
        # Message Properties
        page.get_by_role("button", name="New").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Message Name").fill(datadictvalue["C_MSSG_NAME"])
        # page.get_by_label("Message Name").fill(datetime[""])
        page.get_by_label("Application").select_option(datadictvalue["C_APPLCTN"])
        page.wait_for_timeout(2000)
        page.get_by_label("Module").fill(datadictvalue["C_MDL"])  # Commented for batch testing
        page.wait_for_timeout(2000)
        page.get_by_label("Message Number").fill(str(datadictvalue["C_MSSG_NMBR"]))
        page.wait_for_timeout(2000)
        page.get_by_label("Translation Notes").fill(datadictvalue["C_TRNSLTN_NOTES"])
        page.wait_for_timeout(2000)
        page.get_by_label("Message Type").select_option(datadictvalue["C_MSSG_TYPE"])
        page.wait_for_timeout(2000)
        page.get_by_label("Category").select_option(datadictvalue["C_CTGRY"])
        page.wait_for_timeout(2000)
        page.get_by_label("Severity").select_option(datadictvalue["C_SCRTY"])
        page.wait_for_timeout(3000)
        if datadictvalue["C_LGGNG_ENBLD"] != '':
            if datadictvalue["C_LGGNG_ENBLD"] == "Yes":
                page.get_by_text("Logging Enabled", exact=True).check()
            elif datadictvalue["C_LGGNG_ENBLD"] == "No" or '':
                page.get_by_text("Logging Enabled", exact=True).uncheck()
            page.wait_for_timeout(2000)

        # if datadictvalue["C_LGGNG_ENBLD"] == "Yes":
        #     page.get_by_text("Logging Enabled").check()
        # Message Text
        page.wait_for_timeout(2000)
        page.get_by_label("Short Text").fill(datadictvalue["C_SHORT_TEXT"])
        page.wait_for_timeout(1000)
        page.get_by_label("User Details").fill(datadictvalue["C_USER_DTLS"])
        page.wait_for_timeout(1000)
        page.get_by_label("Administrator Details").fill(datadictvalue["C_ADMNSTRTR_DTLS"])
        page.wait_for_timeout(1000)
        page.get_by_label("Cause").fill(datadictvalue["C_CAUSE"])
        page.wait_for_timeout(1000)
        page.get_by_label("User Action").fill(datadictvalue["C_USER_ACTN"])
        page.wait_for_timeout(1000)
        page.get_by_label("Administrator Action").fill(datadictvalue["C_ADMNSTTR"])
        page.wait_for_timeout(1000)

        # Message Tokens
        page.wait_for_timeout(3000)
        if datadictvalue["C_TOKEN_NAME"] != '':
            page.get_by_role("button", name="New").click()
            page.wait_for_timeout(5000)
            page.get_by_label("Token Name").fill(datadictvalue["C_TOKEN_NAME"])
            page.wait_for_timeout(1000)
            page.get_by_label("Data Type").select_option(datadictvalue["C_DATA_TYPE"])
            page.wait_for_timeout(1000)
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        # Saving the Message Configuration
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close")
        page.wait_for_timeout(3000)
        # print("Row Added - ", str(i)) - Commented for batch testing
        # datadictvalue["RowStatus"] = "Row Added" - Commented for batch testing

        try:
            expect(page.get_by_role("heading", name="Manage Messages")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Manage Messages saved Successfully Saved Successfully")
            datadictvalue["RowStatus"] = "Manage Messages saved Successfully Saved Successfully"
        except Exception as e:
            print("Unable to Save Manage Messages")
            datadictvalue["RowStatus"] = "Unable to Save Manage Messages"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, MESSAGES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, MESSAGES, PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, MESSAGES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0] + "_" + MESSAGES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
