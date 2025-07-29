from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *



def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    # Login to the instance
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    # Navigation
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage AutoCash Rule Sets")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage AutoCash Rule Sets").click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        # Create Cash Rule
        page.get_by_role("button", name="Create").click()

        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Set", exact=True).click()
        page.get_by_label("Set", exact=True).fill(datadictvalue["C_SET"])
        # page.get_by_role("option", name=datadictvalue["C_SET"]).click()
        if datadictvalue["C_ACTV"] == 'Yes':
            if not page.get_by_text("Active").is_checked():
                page.get_by_text("Active").click()
        elif datadictvalue["C_ACTV"] == 'No':
            if page.get_by_text("Active").is_checked():
                page.get_by_text("Active").click()

        #Open Balance Calculations

        page.get_by_label("Discount").select_option(datadictvalue["C_DSCNT"])

        if datadictvalue["C_INCLD_ITEMS_IN_DSPT"] == 'Yes':
            if not page.get_by_text("Include items in dispute").is_checked():
                page.get_by_text("Include items in dispute").click()
        elif datadictvalue["C_INCLD_ITEMS_IN_DSPT"] == 'No':
            if page.get_by_text("Include items in dispute").is_checked():
                page.get_by_text("Include items in dispute").click()

        if datadictvalue["C_INCLD_LATE_CHRGS"] == 'Yes':
            if not page.get_by_text("Include late charges").is_checked():
                page.get_by_text("Include late charges").click()
        elif datadictvalue["C_INCLD_LATE_CHRGS"] == 'No':
            if page.get_by_text("Include late charges").is_checked():
                page.get_by_text("Include late charges").click()

        # Automatic Matching Rule

        page.get_by_label("Remaining Remittance Amount").select_option(datadictvalue["C_RMNNG_RMTTNC_AMNT"])
        if datadictvalue["C_APPLY_PRTL_RCPTS"] == 'Yes':
            if not page.get_by_text("Apply partial receipts").is_checked():
                page.get_by_text("Apply partial receipts").click()
        elif datadictvalue["C_APPLY_PRTL_RCPTS"] == 'No':
            if page.get_by_text("Apply partial receipts").is_checked():
                page.get_by_text("Apply partial receipts").click()

        page.get_by_label("Context Value").select_option(datadictvalue["C_CNTXT_VALUE"])
        # Add Rules
        page.get_by_role("button", name="Add Row").click()
        page.get_by_label("Sequence").fill(str(datadictvalue["C_SQNC"]))
        page.get_by_label("Rule").select_option(datadictvalue["C_RULE"])

        # Save and Close
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        page.wait_for_timeout(5000)

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Auto Cash Rule Sets Saved Successfully")

    except Exception as e:
        print("Auto Cash Rule Sets not Saved")


    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, AUTOCASH_RULE_SET):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, AUTOCASH_RULE_SET, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, AUTOCASH_RULE_SET)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + AUTOCASH_RULE_SET)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + AUTOCASH_RULE_SET + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))