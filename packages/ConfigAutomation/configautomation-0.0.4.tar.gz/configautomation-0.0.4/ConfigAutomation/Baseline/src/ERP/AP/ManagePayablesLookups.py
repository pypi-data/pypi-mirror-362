from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
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
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Manage Payables Lookups")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Payables Lookups", exact=True).click()
    page.get_by_label("Lookup Type", exact=True).fill("Pay Group")
    page.get_by_label("User Module Name").fill("Payables")
    page.get_by_role("button", name="Search", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Create").nth(1).click()
        page.get_by_label("Lookup Code").click()
        page.get_by_label("Lookup Code").fill(datadictvalue["C_LKUP_CODE"])
        page.wait_for_timeout(1000)
        page.get_by_label("Reference Data Set").select_option(datadictvalue["C_RFRNC_DATE_SET"])
        page.wait_for_timeout(1000)
        page.locator("//span[text()='Display Sequence']//following::input[2]").fill(datadictvalue["C_DSPLY_SQNC"])
        page.wait_for_timeout(1000)
        if datadictvalue["C_ENBLD"] == 'Yes':
            page.locator("//span[text()='Enabled']//following::label[contains(@id,'sbc1::Label0')][1]").check()
        if datadictvalue["C_ENBLD"] == 'No':
            page.locator("//span[text()='Enabled']//following::label[contains(@id,'sbc1::Label0')][1]").uncheck()
        page.wait_for_timeout(1000)
        if datadictvalue["C_START_DATE"] != '':
            page.locator("//span[text()='Start Date']//following::input[contains(@placeholder,'m/d/yy')][1]").fill(datadictvalue["C_START_DATE"].strftime("%m/%d/%Y"))
        page.wait_for_timeout(1000)
        if datadictvalue["C_END_DATE"] != '':
            page.locator("//span[text()='End Date']//following::input[contains(@placeholder,'m/d/yy')][2]").fill(datadictvalue["C_END_DATE"].strftime("%m/%d/%Y"))
        page.wait_for_timeout(1000)
        page.locator("//span[text()='Meaning']//following::input[contains(@id,'it4::content')][1]").fill(datadictvalue["C_MNNG"])
        page.wait_for_timeout(1000)
        page.locator("//span[text()='Description']//following::input[contains(@id,'it5::content')][1]").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(1000)
        page.locator("//span[text()='Tag']//following::input[contains(@id,'it9::content')][1]").fill(datadictvalue["C_TAG"])

        # Save the data
        page.get_by_role("button", name="Save and Close").click()

        i = i + 1
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Payable lookups Saved Successfully")
            datadictvalue["RowStatus"] = "Payable lookups are added successfully"

        except Exception as e:
            print("Payable lookups not saved")
            datadictvalue["RowStatus"] = "Payable lookups are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAY_GROUP):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAY_GROUP, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, PAY_GROUP)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + PAY_GROUP)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
            0] + "_" + PAY_GROUP + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))