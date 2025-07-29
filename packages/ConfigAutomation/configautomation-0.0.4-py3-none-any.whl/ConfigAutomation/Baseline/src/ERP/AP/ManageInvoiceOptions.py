from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
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
    page.get_by_role("button", name="Offering").click()
    page.get_by_text("Financials", exact=True).click()
    page.wait_for_timeout(2000)

    # Navigating to respective option in Legal Search field and searching
    page.locator("//td[text()='Payables']").click()
    page.wait_for_timeout(2000)
    page.get_by_label("Search Tasks").click()
    page.get_by_label("Search Tasks").fill("Manage Invoice Options")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(2000)
    page.locator("//a[text()='Manage Invoice Options']//following::a[1]").click()#page.get_by_role("link", name="Manage Invoice Options").click()
    page.get_by_label("Business Unit", exact=True).select_option("Select and Add")
    page.get_by_role("button", name="Apply and Go to Task").click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_label("Name").fill(datadictvalue["C_BSNSS_UNIT"])
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name=datadictvalue["C_BSNSS_UNIT"], exact=True).click()
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        #Invoice Entry

        if datadictvalue["C_RQR_INVC_GRPNG"] == 'Yes':
            page.get_by_text("Require invoice grouping").check()
        if datadictvalue["C_RQR_INVC_GRPNG"] == 'No' or '':
            page.get_by_text("Require invoice grouping").uncheck()
        if datadictvalue["C_ALLOW_DCMNT_CTGRY_OVRRD"] == 'Yes':
            page.get_by_text("Allow document category").check()
        if datadictvalue["C_ALLOW_DCMNT_CTGRY_OVRRD"] == 'No' or '':
            page.get_by_text("Allow document category").uncheck()
        if datadictvalue["C_ALLOW_ADJSTMNTS_TO_PAID_INVCS"] == 'Yes':
            page.get_by_text("Allow adjustments to paid").check()
        if datadictvalue["C_ALLOW_ADJSTMNTS_TO_PAID_INVCS"] == 'No' or '':
            page.get_by_text("Allow adjustments to paid").uncheck()
        if datadictvalue["C_ALLOW_REMIT_TO_SPPLR_OVRRD_FOR_THRD-PARTY_PYMNTS"] == 'Yes':
            page.get_by_text("Allow remit-to supplier").check()
        if datadictvalue["C_ALLOW_REMIT_TO_SPPLR_OVRRD_FOR_THRD-PARTY_PYMNTS"] == 'No' or '':
            page.get_by_text("Allow remit-to supplier").uncheck()
        if datadictvalue["C_RCLCLT_INVC_INSTLLMNTS"] == 'Yes':
            page.get_by_text("Recalculate invoice").check()
        if datadictvalue["C_RCLCLT_INVC_INSTLLMNTS"] == 'No' or '':
            page.get_by_text("Recalculate invoice").uncheck()
        if datadictvalue["C_HOLD_UNMTCHD_INVCS"] == 'Yes':
            page.get_by_text("Hold unmatched invoices").check()
        if datadictvalue["C_HOLD_UNMTCHD_INVCS"] == 'No' or '':
            page.get_by_text("Hold unmatched invoices").uncheck()
        if datadictvalue["C_HOLD_UNMTCHD_INVCS"] == 'Yes':
            page.get_by_text("Hold unmatched invoices").check()
        if datadictvalue["C_HOLD_UNMTCHD_INVCS"] == 'No' or '':
            page.get_by_text("Hold unmatched invoices").uncheck()
        if datadictvalue["C_ENBL_INVC_ACCNT_CDNG_WRKFLW"] == 'Yes':
            page.get_by_text("Enable invoice account coding").check()
        if datadictvalue["C_ENBL_INVC_ACCNT_CDNG_WRKFLW"] == 'No' or '':
            page.get_by_text("Enable invoice account coding").uncheck()
        if datadictvalue["C_PRVNT_DELETN_OF_INVCS_ATCHMNTS"] == 'Yes':
            page.get_by_text("Prevent Deletion of Invoice").check()
        if datadictvalue["C_PRVNT_DELETN_OF_INVCS_ATCHMNTS"] == 'No' or '':
            page.get_by_text("Prevent Deletion of Invoice").uncheck()
        if datadictvalue["C_EVALTE_DUPLCTE_HOLD_DURNG_VLDTN"] == 'Yes':
            page.get_by_text("Evaluate duplicate invoice").check()
        if datadictvalue["C_EVALTE_DUPLCTE_HOLD_DURNG_VLDTN"] == 'No' or '':
            page.get_by_text("Evaluate duplicate invoice").uncheck()
        page.get_by_label("Receipt Acceptance Days").fill(datadictvalue["C_RCPT_CCPTNC_DAYS"])
        page.get_by_label("Invoice Currency").select_option(datadictvalue["C_INVC_CRRNCY"])
        page.get_by_label("Payment Currency").select_option(datadictvalue["C_PYMNT_CRRNCY"])
        if datadictvalue["C_INV_ENTRY_PAY_GROUP"] != '':
            page.get_by_title("Search: Pay Group").first.click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Pay Group").fill(datadictvalue["C_INV_ENTRY_PAY_GROUP"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_INV_ENTRY_PAY_GROUP"], exact=True).click()
            page.get_by_role("button", name="OK").click()
        page.locator("//label[text()='Payment Priority']//following::input[contains(@id,'i2::content')]").clear()
        page.locator("//label[text()='Payment Priority']//following::input[contains(@id,'i2::content')]").fill(str(datadictvalue["C_INV_ENTRY_PYMNT_PRRTY"]))
        page.locator("//label[text()='Payment Terms']//following::select[contains(@id,'soc4::content')]").select_option(datadictvalue["C_INV_ENTRY_PYMNT_TERMS"])
        page.get_by_label("Terms Date Basis").select_option(datadictvalue["C_TERMS_DATE_BASIS"])
        page.get_by_label("Pay Date Basis").select_option(datadictvalue["C_PAY_DATE_BASIS"])
        page.get_by_label("Accounting Date Basis").select_option(datadictvalue["C_ACCNTNG_DATE_BASIS"])
        page.get_by_label("Budget Date Basis").select_option(datadictvalue["C_BDGT_DATE_BASIS"])
        page.get_by_label("Account Derivation Method").select_option(datadictvalue["C_ACCNT_DRVRN_MTHD"])

        #Matching

        if datadictvalue["C_ALLOW_FINAL_MTCHNG"] == 'Yes':
            page.get_by_text("Allow final matching").check()
        if datadictvalue["C_ALLOW_FINAL_MTCHNG"] == 'No':
            page.get_by_text("Allow final matching").uncheck()
        if datadictvalue["C_ALLOW_MTCHNG_DSTRBTN_VRRD"] == 'Yes':
            page.get_by_text("Allow matching distribution").check()
        if datadictvalue["C_ALLOW_MTCHNG_DSTRBTN_VRRD"] == 'No':
            page.get_by_text("Allow matching distribution").uncheck()
        if datadictvalue["C_TRNSFR_PO_DSTRBTN_ADDTNL_INFRMTN"] == 'Yes':
            page.get_by_text("Transfer PO distribution").check()
        if datadictvalue["C_TRNSFR_PO_DSTRBTN_ADDTNL_INFRMTN"] == 'No':
            page.get_by_text("Transfer PO distribution").uncheck()
        page.get_by_label("Quantity Tolerances").select_option(datadictvalue["C_QNTTY_TLRNCS"])
        page.get_by_label("Amount Tolerances").select_option(datadictvalue["C_AMNT_TLRNCS"])

        #Discount

        if datadictvalue["C_EXCLD_TAX_FROM_CLCLTN"] == 'Yes':
            page.get_by_text("Exclude tax from calculation").check()
        if datadictvalue["C_EXCLD_TAX_FROM_CLCLTN"] == 'No':
            page.get_by_text("Exclude tax from calculation").uncheck()
        if datadictvalue["C_EXCLD_FRGHT_FROM_CLCLTN"] == 'Yes':
            page.get_by_text("Exclude freight from").check()
        if datadictvalue["C_EXCLD_FRGHT_FROM_CLCLTN"] == 'No':
            page.get_by_text("Exclude freight from").uncheck()
        page.get_by_text(datadictvalue["C_DSCNT_ALLCTN_MTHD"]).first.click()
        if datadictvalue["C_ALWYS_TAKE_DSCNT"] == 'Yes':
            page.get_by_text("Always take discount").check()
        if datadictvalue["C_ALWYS_TAKE_DSCNT"] == 'No':
            page.get_by_text("Always take discount").uncheck()

        #Prepayment

        page.locator("//label[text()='Payment Terms']//following::select[contains(@id,'soc5::content')]").select_option(datadictvalue["C_PRPYMNT_PYMNT_TERMS"])
        page.get_by_label("Settlement Days").fill(datadictvalue["C_STTLMNT_DAYS"])
        if datadictvalue["C_USE_DSTRBTN_FROM_PRCHS_ORDER"] == 'Yes':
            page.get_by_text("Use distribution from").check()
        if datadictvalue["C_USE_DSTRBTN_FROM_PRCHS_ORDER"] == 'No':
            page.get_by_text("Use distribution from").uncheck()
        if datadictvalue["C_SHOW_VLBL_PRPYMNTS_DRNG_INVC_ENTRY"] == 'Yes':
            page.get_by_text("Show available prepayments").check()
        if datadictvalue["C_SHOW_VLBL_PRPYMNTS_DRNG_INVC_ENTRY"] == 'No':
            page.get_by_text("Show available prepayments").uncheck()

        #Approval

        if datadictvalue["C_ENBL_INVC_APPRVL"] == 'Yes':
            page.get_by_text("Enable invoice approval").check()
        if datadictvalue["C_ENBL_INVC_APPRVL"] == 'No':
            page.get_by_text("Enable invoice approval").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_ALLOW_FORCE_APPRVL"] == 'Yes':
            if page.get_by_text("Allow force approval").is_enabled():
                page.get_by_text("Allow force approval").check()
        if datadictvalue["C_ALLOW_FORCE_APPRVL"] == 'No':
            if page.get_by_text("Allow force approval").is_enabled():
                page.get_by_text("Allow force approval").uncheck()
        if datadictvalue["C_RQR_VLDTN_BEFOR_APPRVL"] == 'Yes':
            if page.get_by_text("Require validation before").is_enabled():
                page.get_by_text("Require validation before").check()
        if datadictvalue["C_RQR_VLDTN_BEFOR_APPRVL"] == 'No':
            if page.get_by_text("Require validation before").is_enabled():
                page.get_by_text("Require validation before").uncheck()
        if page.get_by_text(datadictvalue["C_ACCNTNG_PRFRNC"]).is_enabled():
            page.get_by_text(datadictvalue["C_ACCNTNG_PRFRNC"]).click()

        #Interest

        if datadictvalue["C_CRT_NTRST_INVCS"] == 'Yes':
            page.get_by_text("Create interest invoices").check()
        if datadictvalue["C_CRT_NTRST_INVCS"] == 'No':
            page.get_by_text("Create interest invoices").uncheck()
            page.wait_for_timeout(2000)
        if page.get_by_label("Minimum Interest Amount").is_enabled():
            page.get_by_label("Minimum Interest Amount").fill(datadictvalue["C_MNMM_INTRST_AMNT"])
        if page.get_by_role("group", name="Interest Allocation Method").get_by_text(datadictvalue["C_DSCNT_ALLCTN_MTHD"]).is_enabled():
            page.get_by_role("group", name="Interest Allocation Method").get_by_text(datadictvalue["C_DSCNT_ALLCTN_MTHD"]).click()
        if page.get_by_label("Interest Expense Distribution").is_enabled():
            page.get_by_label("Interest Expense Distribution").fill(datadictvalue["C_INT_EXPNS_DSTBTN"])

        #Payment Request

        page.locator("//label[text()='Payment Terms']//following::select[contains(@id,'soc6::content')]").select_option(datadictvalue["C_PYMNT_RQST_PYMNT_TERMS"])
        if datadictvalue["C_PYMNT_RQST_PAY_GROUP"] != '':
            page.get_by_title("Search: Pay Group").nth(1).click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Pay Group").fill(datadictvalue["C_PYMNT_RQST_PAY_GROUP"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYMNT_RQST_PAY_GROUP"], exact=True).click()
            page.get_by_role("button", name="OK").click()
        page.locator("//label[text()='Payment Priority']//following::input[contains(@id,'i6::content')]").fill(str(datadictvalue["C_PYMNT_RQST_PYMNT_PRRTY"]))

        #Self-Service Invoices

        if datadictvalue["C_LMT_INVC_TO_SINGL_PRCHS_ORDER"] == 'Yes':
            page.get_by_text("Limit invoice to single").check()
        if datadictvalue["C_LMT_INVC_TO_SINGL_PRCHS_ORDER"] == 'No':
            page.get_by_text("Limit invoice to single").uncheck()
        if datadictvalue["C_ALLOW_INVC_BCKDTNG"] == 'Yes':
            page.get_by_text("Allow invoice backdating").check()
        if datadictvalue["C_ALLOW_INVC_BCKDTNG"] == 'No':
            page.get_by_text("Allow invoice backdating").uncheck()
        if datadictvalue["C_ALLOW_OVRBLLD_QNTTY_FOR_QNTTY_BASED_MTCHS"] == 'Yes':
            page.get_by_text("Allow overbilled quantity for").check()
        if datadictvalue["C_ALLOW_OVRBLLD_QNTTY_FOR_QNTTY_BASED_MTCHS"] == 'No':
            page.get_by_text("Allow overbilled quantity for").uncheck()
        if datadictvalue["C_ALLOW_OVRBLLNG_FOR_AMNT_BASED_MTCHS"] == 'Yes':
            page.get_by_text("Allow overbilling for amount-").check()
        if datadictvalue["C_ALLOW_OVRBLLNG_FOR_AMNT_BASED_MTCHS"] == 'No':
            page.get_by_text("Allow overbilling for amount-").uncheck()
        page.get_by_label("Allow Unit Price Change for").select_option(datadictvalue["C_ALLOW_UNIT_PRICE_CHNG_FOR_QNTTY_BASED_MTCHS"])
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(4000)

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)

        try:
            expect(page.get_by_text("Search Tasks")).to_be_visible()
            print("Invoice options Saved Successfully")
            datadictvalue["RowStatus"] = "Invoice options are added successfully"

        except Exception as e:
            print("Invoice options not saved")
            datadictvalue["RowStatus"] = "Invoice options are not added"
        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, INVOICE_OPTIONS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, INVOICE_OPTIONS, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, INVOICE_OPTIONS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + INVOICE_OPTIONS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
            0] + "_" + INVOICE_OPTIONS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))