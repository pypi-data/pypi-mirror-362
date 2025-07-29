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
    page.wait_for_timeout(5000)

    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Expense Report Audit And Receipt Rule Assignments")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Expense Report Audit And Receipt Rule Assignments").click()
    # page.pause()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        # Filtering the Business Unit
        if page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).is_visible():
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).fill(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).press("Enter")
            page.wait_for_timeout(2000)

        page.get_by_role("link", name=datadictvalue["C_BSNSS_UNIT"]).click()

        # Expense Report Audit Selection Rule :-
        page.get_by_role("button", name="Add Row").first.click()
        page.get_by_label("Name").select_option(datadictvalue["C_EXPNS_RPRT_NAME"])
        if datadictvalue["C_EXPNS_RPRT_START_DATE"] != '':
            page.get_by_role("cell", name="Press down arrow to access Calendar Effective Start Date Select Date").get_by_placeholder("m/d/yy").fill(datadictvalue["C_EXPNS_RPRT_START_DATE"].strftime('%m/%d/%y'))
        if datadictvalue["C_EXPNS_RPRT_EFFCTV_END_DATE"] != '':
            page.get_by_role("cell", name="Press down arrow to access Calendar Effective End Date Select Date").get_by_placeholder("m/d/yy").fill(datadictvalue["C_EXPNS_RPRT_EFFCTV_END_DATE"].strftime('%m/%d/%y'))

        # Expense Template and Type Selection Rule
        page.get_by_role("button", name="Add Row").nth(1).click()
        page.locator("//div[@title='Expense Template and Type Selection Rule']//following::select[contains(@id,'content')][1]").select_option(datadictvalue["C_EXPNS_TMPLT_NAME"])
        page.locator("//div[@title='Expense Template and Type Selection Rule']//following::input[contains(@id,'content')][1]").fill(datadictvalue["C_EXPNS_TMPLT_EFFCTV_START_DATE"].strftime('%m/%d/%y'))
        if datadictvalue["C_EXPNS_TMPLT_EFFCTV_END_DATE"] != '':
            page.locator("//div[@title='Expense Template and Type Selection Rule']//following::input[contains(@id,'content')][2]").fill(datadictvalue["C_EXPNS_TMPLT_EFFCTV_END_DATE"].strftime('%m/%d/%y'))

        # page.pause()
        # Audit List Rule

        page.get_by_role("button", name="Add Row").nth(2).click()
        page.locator("//div[@title='Audit List Rule']//following::select[contains(@id,'content')][1]").select_option(datadictvalue["C_AUDIT_NAME"])
        page.locator("//div[@title='Audit List Rule']//following::input[contains(@id,'content')][1]").fill(datadictvalue["C_AUDIT_EFFCTV_START_DATE"].strftime('%m/%d/%y'))
        if datadictvalue["C_AUDIT_EFFCTV_END_DATE"] != '':
            page.locator("//div[@title='Audit List Rule']//following::input[contains(@id,'content')][2]").fill(
            datadictvalue["C_AUDIT_EFFCTV_END_DATE"].strftime('%m/%d/%y'))

        # Receipt and Notification Rule
        page.get_by_role("button", name="Add Row").nth(3).click()
        page.locator("//div[@title='Receipt and Notification Rule']//following::select[contains(@id,'content')]").select_option(datadictvalue["C_RCPT_NAME"])
        page.locator("//div[@title='Receipt and Notification Rule']//following::input[contains(@id,'content')][1]").fill(datadictvalue["C_RCPT_EFFCTV_START_DATE"].strftime('%m/%d/%y'))
        if datadictvalue["C_RCPT_EFFCTV_END_DATE"] != '':
            page.locator("//div[@title='Receipt and Notification Rule']//following::input[contains(@id,'content')][2]").fill(datadictvalue["C_RCPT_EFFCTV_END_DATE"].strftime('%m/%d/%y'))

        page.get_by_role("button", name="Save and Close").click()
        # page.get_by_role("button", name="Cancel").click()

        # Validation

        try:
            expect(page.get_by_text("Confirmation")).to_be_visible()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)
            # page.locator("//div[text()='Confirmation']//following::button[1]").click()
            print("Expense Audit and Receipt Rule Saved Successfully")
            # datadictvalue["RowStatus"] = "Configuration Saved Successfully"
        except Exception as e:
            print("Expense Audit and Receipt Rule not Saved")
            # datadictvalue["RowStatus"] = "Expense Profile Value not Saved"

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, AUDIT_RECEIPT_RULE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, AUDIT_RECEIPT_RULE, PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, AUDIT_RECEIPT_RULE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[0] + "_" + AUDIT_RECEIPT_RULE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + AUDIT_RECEIPT_RULE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))