from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *



def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    # Sign In - Instance
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    # Navigate to the Required Page
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Receipt Sources")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Receipt Sources").click()
    page.wait_for_timeout(3000)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
    # Create Receipt Sources
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        if page.locator("//div[text()='Create Receipt Source']//following::label[text()='Business Unit']//following::input[1]").is_enabled():
            page.locator("//div[text()='Create Receipt Source']//following::label[text()='Business Unit']//following::input[1]").fill(datadictvalue["C_BSNSS_UNIT"])
        page.locator("//div[text()='Create Receipt Source']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_NAME"])
        page.locator("//div[text()='Create Receipt Source']//following::label[text()='Description']//following::input[1]").fill(datadictvalue["C_DSCRPTN"])
        if datadictvalue["C_RCPT_SRC_TYPE"] == 'Automatic':
            page.get_by_text("Automatic").nth(1).click()
        if datadictvalue["C_RCPT_SRC_TYPE"] == 'Manual':
            page.get_by_text("Manual").nth(1).click()
        page.get_by_label("Receipt Class").fill(datadictvalue["C_RCPT_CLASS"])

        if datadictvalue["C_BTCH_NMBRNG"] == 'Automatic':
            page.get_by_text("Automatic").nth(2).click()
        if datadictvalue["C_BTCH_NMBRNG"] == 'Manual':
            page.get_by_text("Manual").nth(2).click()
        page.locator("//div[text()='Create Receipt Source']//following::label[text()='Effective Start Date']//following::input[1]").fill('')
        page.locator("//div[text()='Create Receipt Source']//following::label[text()='Effective Start Date']//following::input[1]").fill(datadictvalue["C_EFFCTV_START_DATE"].strftime('%m/%d/%y'))
        page.locator("//div[text()='Create Receipt Source']//following::label[text()='Effective End Date']//following::input[1]").fill(datadictvalue["C_EFFCTV_END_DATE"])

        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Save and Close
    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(3000)

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Manage Receipt Sources Saved Successfully")

    except Exception as e:
        print("Manage Receipt Sources not Saved")


    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, RECEIPT_SOURCE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, RECEIPT_SOURCE, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, RECEIPT_SOURCE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + RECEIPT_SOURCE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + RECEIPT_SOURCE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))