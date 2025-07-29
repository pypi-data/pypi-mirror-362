from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("My Client Groups", exact=True).click()
    page.get_by_role("link", name="Performance").click()
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Feedback Templates").click()
    page.wait_for_timeout(5000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(10000)

        # Click on Create Button
        page.get_by_label("Add Feedback Templates").click()
        page.wait_for_timeout(10000)

        # Name
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(1000)

        # Comments
        page.get_by_label("Comments").click()
        page.get_by_label("Comments").fill(datadictvalue["C_CMMNTS"])
        page.wait_for_timeout(1000)

        # Status
        page.get_by_role("combobox", name="Status").click()
        page.wait_for_timeout(3000)
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

        # Template Type
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Template Type").click()
        page.wait_for_timeout(1000)
        page.get_by_text(datadictvalue["C_TMPLT_TYPE"], exact=True).click()

        # Questionnaire
        page.get_by_role("combobox", name="Questionnaire").click()
        page.wait_for_timeout(3000)
        # page.get_by_title("Search: Questionnaire").click()
        # page.get_by_role("cell", name=datadictvalue["C_QSTNNR"], exact=True).click()
        page.get_by_text(datadictvalue["C_QSTNNR"], exact=True).click()

        # Include in Performance Document
        if datadictvalue["C_INCLD_IN_PRFRMNC_DCMNT"] == "Yes":
            if not page.get_by_text("Include in Performance Document").is_checked():
                page.get_by_text("Include in Performance Document").click()
                page.wait_for_timeout(3000)

        # Save and Close the Record (Save and Close)
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Create").click()

        page.wait_for_timeout(3000)

        i = i + 1

        try:
            expect(page.get_by_label("Feedback Templates", exact=True).get_by_role("heading", name="Feedback Templates")).to_be_visible()
            print("Feedback Template Saved Successfully")
            datadictvalue["RowStatus"] = "Feedback Template Submitted Successfully"
        except Exception as e:
            print("Feedback Template not saved")
            datadictvalue["RowStatus"] = "Feedback Template not submitted"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, FEEDBACK_TEMPLATE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, FEEDBACK_TEMPLATE, PRCS_DIR_PATH + PERF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PERF_CONFIG_WRKBK, FEEDBACK_TEMPLATE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0] + "_" + FEEDBACK_TEMPLATE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
