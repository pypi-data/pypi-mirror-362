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
    page.get_by_role("textbox").fill("Manage Bank Statement Reconciliation Matching Rule")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Bank Statement").click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Create
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        # Name
        page.get_by_label("Name", exact=True).click()
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])

        # Description
        page.get_by_label("Description", exact=True).click()
        page.get_by_label("Description", exact=True).fill(datadictvalue["C_DSCRPTN"])

        if datadictvalue["C_ACTV"] != '':
            if datadictvalue["C_ACTV"] == "Yes":
                page.get_by_text("Active", exact=True).check()
            elif datadictvalue["C_ACTV"] == "No" or '':
                page.get_by_text("Active", exact=True).uncheck()
            page.wait_for_timeout(2000)

        # Transaction Sources
        if datadictvalue["C_PYBLS"] == "Yes":
            page.get_by_text("Payables").click()
        if datadictvalue["C_RCVBLS"] == "Yes":
            page.get_by_text("Receivables").click()
        if datadictvalue["C_PYRLL"] == "Yes":
            page.get_by_text("Payroll").click()
        if datadictvalue["C_EXTRNL"] == "Yes":
            page.get_by_text("External").click()
        page.wait_for_timeout(2000)

        # Matching Type - One to One
        if datadictvalue["C_MTHNG_TYPE"] == "One to One":
            page.get_by_label("Matching Type").click()
            page.get_by_label("Matching Type").select_option(datadictvalue["C_MTHNG_TYPE"])
            page.wait_for_timeout(3000)
        # Matching Criteria
            if datadictvalue["C_DATE"] == "Yes":
                page.get_by_text("Date", exact=True).click()
            if datadictvalue["C_USE_ADVNCD_CRTR"] == "Yes":
                page.get_by_text("Use Advanced Criteria").click()
            if datadictvalue["C_RCNCLTN_RFRNC"] == "Yes":
                page.get_by_text("Reconciliation Reference", exact=True).click()
            if datadictvalue["C_TRNSCTN_TYPE"] == "Yes":
                page.get_by_text("Transaction Type", exact=True).click()
        page.wait_for_timeout(2000)

        # Matching Type - One to Many
        if datadictvalue["C_MTHNG_TYPE"] == "One to Many":
            page.get_by_label("Matching Type").click()
            page.get_by_label("Matching Type").select_option(datadictvalue["C_MTHNG_TYPE"])
            page.wait_for_timeout(2000)
        # Matching Criteria
            if datadictvalue["C_SYSTM_TRNSCTN_GRPNG_ATTRBTS"] != '':
                page.get_by_role("checkbox", name=datadictvalue["C_SYSTM_TRNSCTN_GRPNG_ATTRBTS"], exact=True).click()
            if page.get_by_text("Reconciliation Reference", exact=True).is_enabled():
                if datadictvalue["C_RCNCLTN_RFRNC"] == "Yes":
                    page.get_by_text("Reconciliation Reference", exact=True).check()
                if datadictvalue["C_RCNCLTN_RFRNC"] == "No" or '':
                    page.get_by_text("Reconciliation Reference", exact=True).uncheck()
                page.wait_for_timeout(2000)
       # Save and Close
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()

        # Validation :- Checking for the confirmation
        try:
            expect(page.get_by_text("Information")).to_be_visible()
            print("Matching Rule Saved Successfully")
            datadictvalue["RowStatus"] = "Matching Rule Saved Successfully"
        except Exception as e:
            print("Matching Rule Saved UnSuccessfully")
            datadictvalue["RowStatus"] = "Matching Rule Saved UnSuccessful"

        page.wait_for_timeout(2000)
        page.get_by_role("button", name="OK").click()

        i = i + 1

        page.wait_for_timeout(2000)
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, BANK_STATEMENT_REC_MATCHING_RULE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, BANK_STATEMENT_REC_MATCHING_RULE, PRCS_DIR_PATH + CM_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + CM_WORKBOOK, BANK_STATEMENT_REC_MATCHING_RULE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0] + "_" + BANK_STATEMENT_REC_MATCHING_RULE)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[
                0] + "_" + BANK_STATEMENT_REC_MATCHING_RULE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
