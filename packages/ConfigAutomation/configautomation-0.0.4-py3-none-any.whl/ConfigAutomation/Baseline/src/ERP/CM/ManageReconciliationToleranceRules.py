from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Bank Statement Reconciliation Tolerance Rules")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Bank Statement Reconciliation Tolerance Rules", exact=True).click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Create
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)

        # Name
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])

        # Description
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        # Status
        if datadictvalue["C_ACTV"] != '':
            if datadictvalue["C_ACTV"] == "Yes":
                page.get_by_text("Active", exact=True).check()
            elif datadictvalue["C_ACTV"] == "No" or '':
                page.get_by_text("Active", exact=True).uncheck()
            page.wait_for_timeout(2000)

        # Date Tolerance
        if datadictvalue["C_ENBL"] == "Yes":
            page.get_by_text("Enable").first.check()
            page.get_by_label("Days Before").fill(str(datadictvalue["C_DAYS_BFR"]))
            page.get_by_label("Days After").fill(str(datadictvalue["C_DAYS_AFTER"]))
            page.wait_for_timeout(3000)

        # Amount Tolerance
        if datadictvalue["C_ENBL_AMT_TLRNC"] == "Yes":
            page.get_by_text("Enable").nth(1).check()
            page.get_by_label("Amount Below").fill(str(datadictvalue["C_AMNT_BELOW"]))
            page.get_by_label("Amount Above").fill(str(datadictvalue["C_AMNT_ABOVE"]))
            page.wait_for_timeout(2000)

        # Percentage Amount Tolerance
        if datadictvalue["C_ENBL_PRCNTG_AMT_TLRNC"] == "Yes":
            page.get_by_text("Enable").nth(2).check()
            page.get_by_label("Percent Below").fill(str(datadictvalue["C_PRCNT_BELOW"]))
            page.get_by_label("Percent Above").fill(str(datadictvalue["C_PRCNT_ABOVE"]))
            page.wait_for_timeout(2000)

        # Save and Close
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()

        # Validation :- Checking for the confirmation
        try:
            expect(page.get_by_text("Information")).to_be_visible()
            print("Tolerance Rule Saved Successfully")
            datadictvalue["RowStatus"] = "Tolerance Rule Saved Successfully"
        except Exception as e:
            print("Tolerance Rule Saved UnSuccessfully")
            datadictvalue["RowStatus"] = "Tolerance Rule Saved UnSuccessfully"

        page.wait_for_timeout(2000)
        page.get_by_role("button", name="OK").click()

        i = i + 1

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, BANK_STATEMENT_REC_TOLERANCE_RULE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, BANK_STATEMENT_REC_TOLERANCE_RULE, PRCS_DIR_PATH + CM_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + CM_WORKBOOK, BANK_STATEMENT_REC_TOLERANCE_RULE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0] + "_" + BANK_STATEMENT_REC_TOLERANCE_RULE)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[
                0] + "_" + BANK_STATEMENT_REC_TOLERANCE_RULE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
