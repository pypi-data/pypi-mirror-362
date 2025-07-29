from playwright.sync_api import Playwright, sync_playwright, expect
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
    page.get_by_role("textbox").fill("Manage Expenses System Options")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Expenses System Options").click()

    i = 0
    while i < rowcount:

        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Business Unit", exact=True).clear()
        page.get_by_label("Business Unit", exact=True).type(datadictvalue["C_BSNSS_UNIT"])
        page.get_by_role("option", name=datadictvalue["C_BSNSS_UNIT"]).click()

        #User Options for Expense Report
        page.get_by_role("link", name="User Options for Expense Report").click()
        page.get_by_label("Enable Payment Method").nth(1).select_option(datadictvalue["C_ENBL_PYMNT_MTHD"])
        page.get_by_label("Allow Reimbursement Currency Selection").nth(1).select_option(datadictvalue["C_ALLW_RMBRSMNT_CRRNCY_SLCTN"])

        if datadictvalue["C_ALLWD_CRRNCS"] != '' and datadictvalue["C_ALLW_RMBRSMNT_CRRNCY_SLCTN"] == 'Yes':
            page.wait_for_timeout(2000)
            page.get_by_role("row", name="Allowed Currencies", exact=True).locator("a").click()
            page.get_by_label(datadictvalue["C_ALLWD_CRRNCS"]).click()
            page.get_by_text("Create System Options:").click()
        page.wait_for_timeout(2000)

        page.get_by_label("Enable Attachments").nth(1).select_option(datadictvalue["C_ENBL_ATTCHMNTS"])
        page.get_by_label("Allow Overriding Approver").nth(1).select_option(datadictvalue["C_ALLW_OVRRDNG_APPRVR"])
        page.get_by_label("Enable Travel").nth(1).select_option(datadictvalue["C_ENBL_TRVL"])
        page.get_by_label("Enable Recurring Expenses").nth(1).select_option(datadictvalue["C_ENBL_RCRRNG_EXPNSS"])
        page.get_by_label("Allow Password Storage in Mobile Application").nth(1).select_option(datadictvalue["C_ALLW_PSSWRD_STRG_IN_MBL_APPLCTNS"])
        page.get_by_label("Enable Split Allocations").nth(1).select_option(datadictvalue["C_ENBL_SPLIT_ALLCTNS"])
        page.get_by_label("Enable Oracle Maps").nth(1).select_option(datadictvalue["C_ENBL_ORCL_MAPS"])
        page.wait_for_timeout(2000)

        #Corporate Options for Expense Report
        page.get_by_role("link", name="Corporate Options for Expense Report").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Enable Default the Report Owner as Attendee").nth(1).select_option(datadictvalue["C_ENBL_DFLT_THE_RPRT_OWNR_AS_ATTND"])
        page.get_by_label("Enable Expense Location Level").nth(1).select_option(datadictvalue["C_ENBL_EXPNS_LCTN_LVL"])
        page.get_by_label("Display Bar Code").nth(1).select_option(datadictvalue["C_DSPLY_BAR_CODE"])
        page.get_by_label("Require Project Fields for Project Users").nth(1).select_option(datadictvalue["C_RQR_PRJCT_FLDS_FOR_PRJCT_USERS"])
        page.get_by_label("Enable Descriptive Flexfields").nth(1).select_option(datadictvalue["C_ENBL_DSCRPTV_FLXFLDS"])
        page.get_by_label("Printable Expense Report Format").nth(1).select_option(datadictvalue["C_PRNTBL_EXPNS_RPRT_FRMT"])

        page.get_by_label("Enable Terms and Agreements", exact=True).click()
        page.wait_for_timeout(1000)
        # page.get_by_role("cell", name="Create System Options: Specific Business Unit").get_by_label("Enable Terms and Agreements", exact=True).get_by_title("Use setup from all business units").click()
        # page.wait_for_timeout(2000)
        page.get_by_label("Enable Terms and Agreements", exact=True).select_option(datadictvalue["C_ENBL_TERMS_AND_AGRMNTS"])
        page.get_by_text("Create System Options:").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Enable Corporate Policy URL").nth(1).click()
        page.get_by_label("Enable Corporate Policy URL").nth(1).select_option(datadictvalue["C_ENBL_CRPRT_PLCY_URL"])
        page.wait_for_timeout(2000)
        if datadictvalue["C_ENBL_CRPRT_PLCY_URL"] == 'Yes':
            page.locator("//label[text()='Enable Corporate Policy URL']//following::input[contains(@id, 'URL')][3]").fill(datadictvalue["C_URL"])
        page.get_by_label("Enable Corporate Card Transaction Age Limit").nth(1).select_option(datadictvalue["C_ENBL_CRPRT_CARD_TRNSCTN_AGE_LIMIT"])
        page.wait_for_timeout(2000)
        page.get_by_label("Enable Notifications for Credit Card Charges").nth(1).click()
        page.wait_for_timeout(3000)
        page.get_by_label("Enable Notifications for Credit Card Charges").nth(1).select_option(datadictvalue["C_ENBL_NTFCTNS_FOR_CRDT_CARD_CHRGS"])

        if datadictvalue["C_ENBL_CRPRT_CARD_TRNSCTN_AGE_LIMIT"] == 'Yes':
            page.locator("//label[text()='Enable Notifications for Credit Card Charges']//following::input[1]").click()
            page.locator("//label[text()='Enable Notifications for Credit Card Charges']//following::input[1]").clear()
            page.locator("//label[text()='Enable Notifications for Credit Card Charges']//following::input[1]").fill(str(datadictvalue["C_INCRMNT_DCRMNT"]))
        page.wait_for_timeout(2000)
        page.locator("//label[text()='Expense Report Number Prefix']//following::label[text()='"+datadictvalue["C_EXPNS_RPRT_NMBR_PRFX"]+"']").click()
        page.wait_for_timeout(2000)

        #Processing Options for Expense Report
        page.get_by_role("link", name="Processing Options for Expense Report").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Enable Payment Notification to Employee").nth(1).select_option(datadictvalue["C_ENBL_PYMNT_NTFCTN_TO_EMPLY"])
        if page.get_by_label("Enable Automatic Travel Expense Report Creation").nth(1).is_enabled():
            page.get_by_label("Enable Automatic Travel Expense Report Creation").nth(1).select_option(datadictvalue["C_ENBL_ATMTC_TRVL_EXPNS_RPRT_CRTN"])
        if page.get_by_label("Enable Report Creation for Users Before Card Charges Appear").nth(1).is_visible():
            page.get_by_label("Enable Report Creation for Users Before Card Charges Appear").nth(1).select_option(datadictvalue["C_ENBL_RPRT_CRTN_FOR_USERS_BFR_CARD_CHRGS_APPR"])
        page.get_by_label("Expense Report Audit Approval").nth(1).select_option(datadictvalue["C_EXPNS_RPRT_AUDIT_APPRVL"])
        page.locator("//label[text()='Processing Days Allowed After Termination']//following::label[text()='"+datadictvalue["C_PRCSSNG_DAYS_ALLWD_AFTER_TRMNTN"]+"']").first.click()
        if datadictvalue["C_PRCSSNG_DAYS_ALLWD_AFTER_TRMNTN"] =='Define value specific to business unit':
            page.locator("//label[text()='Processing Days Allowed After Termination']//following::input[3]").nth(1).clear()
            page.locator("//label[text()='Processing Days Allowed After Termination']//following::input[3]").nth(1).fill(str(datadictvalue["C_PRCSSNG_DAYS_ALLWD_AFTER_TRMNTN_VALUE"]))
        page.locator("//label[text()='Employee Liability Account']//following::label[text()='" + datadictvalue[
                "C_EMPL_LBLTY_ACCNT"] + "']").first.click()
        if datadictvalue["C_EMPL_LBLTY_ACCNT"] == 'Define value specific to business unit':
            page.locator("//label[text()='Employee Liability Account']//following::input[3]").nth(0).fill(datadictvalue["C_EMPL_LBLTY_ACCNT_VALUE"])
            page.wait_for_timeout(2000)
        if datadictvalue["C_INCTV_EMPLY_GRACE_PRD"] == 'Use setup from all business units':
            page.locator("//label[text()='Inactive Employee Grace Period in Days']//following::label[text()='"+datadictvalue["C_INCTV_EMPLY_GRACE_PRD"]+"']").nth(1).click()
        if datadictvalue["C_INCTV_EMPLY_GRACE_PRD"] == 'Define value specific to business unit':
            page.locator("//label[text()='Inactive Employee Grace Period in Days']//following::label[text()='" + datadictvalue[
                    "C_INCTV_EMPLY_GRACE_PRD"] + "']").nth(2).click()
            page.wait_for_timeout(1000)
            page.locator("//label[text()='Inactive Employee Grace Period in Days']//following::input[3]").nth(1).clear()
            page.locator("//label[text()='Inactive Employee Grace Period in Days']//following::input[3]").nth(1).fill(str(
                datadictvalue["C_INCTV_EMPLY_GRACE_PRD_VALUE"]))
        # page.locator("[id=\"__af_Z_window\"]").get_by_title("ValueMeaning").click()
        # page.get_by_role("link", name="Search...").click()
        # page.get_by_label("Meaning").fill(datadictvalue["C_PAY_GROUP_FOR_NGTV_EXPNS_RPRTS"])
        # page.get_by_role("button", name="Search", exact=True).click()
        # page.get_by_text(datadictvalue["C_PAY_GROUP_FOR_NGTV_EXPNS_RPRTS"], exact=True).click()
        # page.get_by_role("button", name="OK").click()
        page.locator("//div[text()='Create System Options: Specific Business Unit']//following::label[text()='Pay Group for Negative Expense Reports']//following::input[1]").fill(datadictvalue["C_PAY_GROUP_FOR_NGTV_EXPNS_RPRTS"])

        # page.get_by_label("Pay Group for Negative Expense Reports").nth(1).fill(datadictvalue["C_PAY_GROUP_FOR_NGTV_EXPNS_RPRTS"])
        # page.get_by_role("option", name=datadictvalue["C_PAY_GROUP_FOR_NGTV_EXPNS_RPRTS"]).click()

        #Save the data

        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        if page.get_by_role("button", name="Yes").is_visible():
            page.get_by_role("button", name="Yes").click()
        if page.get_by_role("button", name="OK").is_visible():
            page.get_by_role("button", name="OK").click()

        page.wait_for_timeout(4000)
        page.get_by_role("button", name="Save and Close").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Expenses System options Saved Successfully")
            datadictvalue["RowStatus"] = "Expenses System options are saved successfully"

        except Exception as e:
            print("Expenses System options not saved")
            datadictvalue["RowStatus"] = "Expenses System options are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, EXP_SYS_OPTIONS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, EXP_SYS_OPTIONS,
                             PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, EXP_SYS_OPTIONS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
                                   0] + "_" + EXP_SYS_OPTIONS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + EXP_SYS_OPTIONS + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

