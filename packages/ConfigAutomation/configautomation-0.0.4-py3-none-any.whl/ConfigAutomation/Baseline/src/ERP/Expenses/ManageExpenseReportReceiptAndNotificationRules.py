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
    page.get_by_role("textbox").fill("Manage Expense Report Receipt And Notification Rules")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Expense Report Receipt and Notification Rules").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create").click()
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        #types of receipt required
        if datadictvalue["C_TYPE_OF_RCPT_RQRD"] == 'Original':
            page.get_by_text("Original", exact=True).click()
        if datadictvalue["C_TYPE_OF_RCPT_RQRD"] == 'Imaged':
            page.get_by_text("Imaged", exact=True).click()
        if datadictvalue["C_TYPE_OF_RCPT_RQRD"] == 'Both':
            page.get_by_text("Both", exact=True).click()
        if datadictvalue["C_TYPE_OF_RCPT_RQRD"] == 'Both':
            page.get_by_text("None").click()
        page.wait_for_timeout(4000)
        #Stage When Imaged Receipts Must Be Attached to Expense Report
        # page.get_by_text("Require reason if receipts are not attached before submission").click()
        if datadictvalue["C_STAGE_WHEN_IMGD_RCPTS_MUST_BE_ATTCHD_TO_EXPNS_RPRT"] == 'Before approval by expense auditor':
            page.get_by_text("Before approval by expense").click()
        if datadictvalue["C_STAGE_WHEN_IMGD_RCPTS_MUST_BE_ATTCHD_TO_EXPNS_RPRT"] == 'Prevent submission if receipts are not attached':
            page.get_by_text("Prevent submission if").click()
        if datadictvalue["C_STAGE_WHEN_IMGD_RCPTS_MUST_BE_ATTCHD_TO_EXPNS_RPRT"] == 'Require reason if receipts are not attached before submission':
            page.get_by_text("Require reason if receipts").click()
        if datadictvalue[
            "C_STAGE_WHEN_IMGD_RCPTS_MUST_BE_ATTCHD_TO_EXPNS_RPRT"] == 'Before approval by manager':
            page.get_by_text("Before approval by manager").click()
            page.get_by_label("Days to Wait for Imaged").fill(datadictvalue["Days To Wait For Imaged Receipts Until Expense Report Is Returned To Preparer"])

        #Receipt Tracking
        if datadictvalue["C_ENBL_OVRD_PRCSS"] == 'Yes' :
            page.get_by_text("Enable overdue process").check()
            page.get_by_label("Days to Wait for Overdue").fill(datadictvalue["C_DAYS_TO_WAIT_FOR_OVRD_RCPTS"])

        page.get_by_label("Notify Individual When").select_option(datadictvalue["C_NTFY_INDVDL_WHEN_RCPTS_ARE_RCVD"])
        if datadictvalue["C_SEND_MSSNG_RCPT_DCLRTN_NTFCTN"] == 'Yes':
            page.get_by_text("Send missing receipt").check()
        if datadictvalue["C_ENBL_HOLDS_PRCSS"] == 'Yes':
            page.get_by_text("Enable holds process").click()

        #Apply Hold Rule
            if datadictvalue["C_APPLY_HOLD_RULE"] == 'When receipts are overdue':
                page.get_by_text("When receipts are overdue", exact=True).click()
            elif datadictvalue["C_APPLY_HOLD_RULE"] == 'Until receipts are received':
                page.get_by_text("Until receipts are received").click()
        #Apply Hold Rule To
            if datadictvalue["C_APPLY_HOLD_RULE_TO"] == 'Report of both individuals and corporate card issuers':
                page.get_by_text("Report of both individuals").click()
            elif datadictvalue["C_APPLY_HOLD_RULE_TO"] == 'Report of individuals only':
                page.get_by_text("Report of individuals only").click()
            if datadictvalue["C_APPLY_HOLD_RULES_TO_EXPNS_RPRTS_LINE_PRJCT_RLTD_INFRMTN"] == 'Yes':
                page.get_by_text("Apply hold rules to expense").click()

        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save and Close").click()
        #Validation

        try:
            expect(page.locator("//div[text()='Confirmation']//following::button[1]")).to_be_visible()
            page.locator("//div[text()='Confirmation']//following::button[1]").click()
            print("Row Saved Successfully")
            datadictvalue["RowStatus"] = "Configuration Saved Successfully"
        except Exception as e:
            print("Saved UnSuccessfully")
            datadictvalue["RowStatus"] = "Configuration Saved UnSuccessfully"

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, RECEIPT_NOTIFI_RULE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, RECEIPT_NOTIFI_RULE, PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, RECEIPT_NOTIFI_RULE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[0] + "_" + RECEIPT_NOTIFI_RULE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + RECEIPT_NOTIFI_RULE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))