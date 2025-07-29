from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Journal Sources")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Journal Sources", exact=True).click()
    # page.pause()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(1000)
        page.get_by_label("Source Key").click()
        page.get_by_label("Source Key").fill(datadictvalue["C_SRC_KEY"])
        page.wait_for_timeout(1000)
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(1000)
        page.get_by_label("Freeze Journals").select_option(datadictvalue["C_FRZ_JRNLS"])
        page.get_by_label("Accounting Date Rule").select_option(datadictvalue["C_ACCNTNG_DATE_RULE"])
        page.wait_for_timeout(2000)

        if datadictvalue["C_IMPRT_JRNL_RFRNCS"] == 'Yes':
            page.locator("//span[text()='Import Journal References']//following::label[contains(@id,'Label0')][1]").check()
        if datadictvalue["C_IMPRT_JRNL_RFRNCS"] == 'No':
            page.locator("//span[text()='Import Journal References']//following::label[contains(@id,'Label0')][1]')]").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_RQR_JRNL_APPRVL"] == 'Yes':
            page.wait_for_timeout(2000)
            page.locator("//span[text()='Require Journal Approval']//following::label[contains(@id,'Label0')][2]").check()
        if datadictvalue["C_RQR_JRNL_APPRVL"] == 'No':
            page.locator("//span[text()='Require Journal Approval']//following::label[contains(@id,'Label0')][2]").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_IMPRT_USNG_KEY"] == 'Yes':
            page.wait_for_timeout(2000)
            page.locator("//span[text()='Import Using Key']//following::label[contains(@id,'Label0')][3]").check()
        if datadictvalue["C_IMPRT_USNG_KEY"] == 'No':
           page.locator("//span[text()='Import Using Key']//following::label[contains(@id,'Label0')][3]").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_LIMIT_JRNL_TO_SNGL_CRRNCY"] == 'Yes':
            page.wait_for_timeout(2000)
            page.locator("//span[text()='Limit Journal to Single Currency']//following::label[contains(@id,'Label0')][4]").check()
        if datadictvalue["C_LIMIT_JRNL_TO_SNGL_CRRNCY"] == 'No':
            page.locator("//span[text()='Limit Journal to Single Currency']//following::label[contains(@id,'Label0')][4]").uncheck()

        i = i + 1
    page.get_by_role("button", name="Save", exact=True).click()
    page.wait_for_timeout(3000)

    if page.get_by_role("button", name="OK").is_visible():
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(2000)

    try:
        expect(page.get_by_role("heading", name="Search")).to_be_visible()
        print("Legal Sets created successfully")
        datadictvalue["RowStatus"] = "Successfully Added Ledger sets"
    except Exception as e:
        print("Unable to save the Legal Sets")
        datadictvalue["RowStatus"] = "Unable to save the Legal Sets"

    print("Row Added - ", str(i))
    datadictvalue["RowStatus"] = "Successfully Added Journal Sources"

    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, JRNL_SOURCES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, JRNL_SOURCES, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, JRNL_SOURCES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + JRNL_SOURCES)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
                0] + "_" + JRNL_SOURCES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))