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
    page.get_by_role("textbox").fill("Manage Expense Report Audit Selection Rules")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Expense Report Audit Selection Rules").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(2000)
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(2000)

        # Expense Report Audit Selection Rules-Random Selection Rules
        if datadictvalue["C_AUDIT_A_PRCNTG_OF_ALL_EXPNS_RPRTS"] == 'Yes':
            page.get_by_text("Audit a percentage of all expense reports").check()
            page.wait_for_timeout(2000)
            page.get_by_label("Audit Percentage").fill(str(datadictvalue["C_AUDIT_PRCNTG"]))
            # Ignore Expense Reports That Contain
            if datadictvalue["C_IGNR_EXPNS_RPRTS_THAT_CNTN-CRDT_LINES_ONLY"] == 'Yes':
                page.get_by_text("Credit lines only").check()
            if datadictvalue["C_IGNR_EXPNS_RPRTS_THAT_CNTN_EXPNS_ITEMS_RQR_RCPTS"] == 'Yes':
                page.get_by_text("Expense items that don't").check()
        if datadictvalue["C_AUDIT_A_PRCNTG_OF_ALL_EXPNS_RPRTS"] == 'No':
            page.get_by_text("Audit a percentage of all expense reports").uncheck()
        # Additional Selection Rules
        if datadictvalue["C_AUDIT_EXPNS_RPRTS_GRTR_THAN_A_SPCFD_AMNT"] == 'Yes':
            page.get_by_text("Audit expense reports greater").check()
            page.wait_for_timeout(5000)
            page.get_by_label("Currency").select_option(datadictvalue["C_CRRNCY"])
            page.get_by_label("Amount", exact=True).fill(str(datadictvalue["C_AMNT"]))
        if datadictvalue["C_AUDIT_EXPNS_RPRTS_WTH_RQRD_RCPTS"] == 'Yes':
            page.get_by_text("Audit expense reports with required receipts").check()
        if datadictvalue["C_AUDIT_EXPNS_RPRTS_WITH_MSSNG_IMGD_RCPTS"] == 'Yes':
            page.get_by_text("Audit expense reports with missing imaged receipts").check()
        if datadictvalue["C_AUDIT_EXPNS_RPRTS_WITH_PLCY_VLTNS"] == 'Yes':
            page.get_by_text("Audit expense reports with policy violations").check()
        if datadictvalue["C_AUDIT_EXPNS_RPRTS_OF_INDVDLS_ON_THE_AUDIT_LIST"] == 'Yes':
            page.get_by_text("Audit expense reports of individuals on the audit list").check()
        if datadictvalue["C_AUDIT_EXPNS_RPRTS_WITH_EXPNSS_OLDER_SPCFD_NMBR_OF_DAYS"] == 'Yes':
            page.get_by_text("Audit expense reports with expenses older than a specified number of days").check()
            page.wait_for_timeout(1000)
            page.get_by_label("Days", exact=True).fill(str(datadictvalue["C_DAYS"]))
        if datadictvalue["C_AUDIT_EXPNS_RPRTS_OF_INDVDLS_WITH_A_SPCFC_STTS"] == 'Yes':
            page.get_by_text("Audit expense reports of individuals with a specific status").check()

        #Confirmation Page Audit Type
        page.get_by_label("Automatic Approval").fill(datadictvalue["C_ATMTC_APPRVL"])
        page.get_by_label("Original Receipts Audit").fill(datadictvalue["C_ORGNL_RCPTS_AUDIT"])
        page.get_by_label("Imaged Receipts Audit").fill(datadictvalue["C_IMGD_RCPTS_AUDIT"])
        page.get_by_label("No Receipts Required Audit").fill(datadictvalue["C_NO_RCPTS_RQRD_AUDIT"])

        page.get_by_role("button", name="Save and Close").click()

        #Validation

        try:
            expect(page.get_by_text("Confirmation", exact=True)).to_be_visible()
            page.get_by_role("button", name="OK").click()
            print("Expense Report Audit Selection Rules Saved Successfully")
            # datadictvalue["RowStatus"] = "Configuration Saved Successfully"
        except Exception as e:
            print("Expense Report Audit Selection Rules not Saved")
            # datadictvalue["RowStatus"] = "Expense Profile Value not Saved"

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, AUDIT_SELC_RULE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, AUDIT_SELC_RULE, PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, AUDIT_SELC_RULE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[0] + "_" + AUDIT_SELC_RULE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + AUDIT_SELC_RULE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))