from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    # Navigate to Enrolment Authorization page
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Benefits Administration", exact=True).click()
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Enrollment Authorizations").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(3000)

        # Enter Start Date
        if datadictvalue["C_START_DATE"] !='':
            page.get_by_placeholder("m/d/yy").nth(0).clear()
            page.get_by_placeholder("m/d/yy").nth(0).type(datadictvalue["C_START_DATE"])

        # Enter End Date
        if datadictvalue["C_END_DATE"] != '':
            page.get_by_placeholder("m/d/yy").nth(1).clear()
            page.get_by_placeholder("m/d/yy").nth(1).type(datadictvalue["C_START_DATE"])

        # Enter Description
        if datadictvalue["C_DSCRPTN"]!='':
            page.get_by_label("Description").clear()
            page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])


        # Select Program Name
        if datadictvalue["C_PRGRM_NAME"]!='':
            # page.get_by_role("combobox", name="Program Name").click()
            page.locator("//label[text()='Program Name']//following::input[1]").click()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_PRGRM_NAME"],exact=True).click()

        # Enter Authorization text
        if datadictvalue["C_ATHRZTN_TEXT"]!='':
            page.get_by_label("Editor editing area: main").click()
            page.get_by_label("Editor editing area: main").type(datadictvalue["C_ATHRZTN_TEXT"])

        # Click on Save and Close
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        context.tracing.stop(path="trace.zip")
        try:
            expect(page.get_by_role("heading", name="Enrollment Authorizations")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Enrolment Authorization Created Successfully")
            datadictvalue["RowStatus"] = "Enrolment Authorization Created Successfully"
        except Exception as e:
            print("Unable to Create Enrolment Authorization")
            datadictvalue["RowStatus"] = "Unable to Save Enrolment Authorization"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, ENROLL_AUTH):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, ENROLL_AUTH,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, ENROLL_AUTH)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + ENROLL_AUTH)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + ENROLL_AUTH + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
