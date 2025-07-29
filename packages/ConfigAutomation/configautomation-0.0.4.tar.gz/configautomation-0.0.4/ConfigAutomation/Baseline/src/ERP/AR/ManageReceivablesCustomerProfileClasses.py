from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *



def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    # Sign In - Instance
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    # Navigate to the Required Page
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Receivables Customer Profile Classes")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Receivables Customer Profile Classes").click()
    page.wait_for_timeout(3000)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Create
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)
        # Header Data
        page.get_by_label("Profile Class Name").fill(datadictvalue["C_PRFL_CLASS_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Status").select_option(datadictvalue["C_STTS"])

        # Credit and Collections
        page.get_by_role("link", name="Profile Class").click()
        page.get_by_label("Collector").fill(datadictvalue["C_CLLCTR"])
        page.get_by_label("Credit Analyst").fill(datadictvalue["C_CRDT_ANLYST"])
        page.get_by_label("Credit Classification").select_option(datadictvalue["C_CRDT_CLSSFCTN"])
        page.get_by_label("Credit Review Cycle").select_option(datadictvalue["C_CRDT_RVW_CYCLE"])
        page.get_by_label("Credit Limit").fill(datadictvalue["C_CRDT_LIMIT"])
        page.get_by_label("Order Amount Limit").fill(datadictvalue["C_ORDER_AMNT_LIMIT"])
        page.get_by_label("Credit Currency").select_option(datadictvalue["C_CRDT_CRRNCY"])
        page.get_by_label("Tolerance").fill(str(datadictvalue["C_TLRNC"]))
        page.get_by_label("Conversion Rate Type").fill(datadictvalue["C_CNVRSN_RATE_TYPE"])
        page.get_by_label("Expiration Offset Days").fill(datadictvalue["C_EXPRTN_OFFST_DAYS"])
        if datadictvalue["C_INCLD_IN_CRDT_CHECK"] == 'Yes':
            if not page.get_by_text("Include in credit check").is_checked():
                page.get_by_text("Include in credit check").click()
        if datadictvalue["C_INCLD_IN_CRDT_CHECK"] == 'No':
            if page.get_by_text("Include in credit check").is_checked():
                page.get_by_text("Include in credit check").click()

        # Balance Forward Billing
        if datadictvalue["C_ENBL"] == 'Yes':
            page.get_by_text("Enable").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Yes").click()
            page.locator("//label[text()='Bill Level']//following::select[1]").click()
            page.locator("//label[text()='Bill Level']//following::select[1]").select_option(datadictvalue["C_BILL_LEVEL"])
            page.get_by_label("Bill Type").select_option(datadictvalue["C_BILL_TYPE"])

        # Terms
        page.get_by_role("combobox", name="Payment Terms").fill(datadictvalue["C_PYMNT_TERMS"])
        page.get_by_label("Discount Grace Days").fill(str(datadictvalue["C_DSCNT_GRACE_DAYS"]))
        if datadictvalue["C_ALLW_DSCNT"] == 'Yes':
            if not page.get_by_text("Allow discount").is_checked():
                page.get_by_text("Allow discount").click()
        if datadictvalue["C_ALLW_DSCNT"] == 'No':
            if page.get_by_text("Allow discount").is_checked():
                page.get_by_text("Allow discount").click()
        if datadictvalue["C_OVRRD_TERMS"] == 'Yes':
            page.get_by_text("Override terms").click()


        # Receipt Matching
        page.get_by_label("Match Receipts By").fill(datadictvalue["C_MTCH_RCPTS_BY"])
        page.get_by_label("AutoMatch Rule Set").fill(datadictvalue["C_ATMTCH_RULE_SET"])
        if datadictvalue["C_ATMTCLLY_UPDT_RCPT_MTCH_BY"] == 'Yes':
            if not page.get_by_text("Automatically update receipt").is_checked():
                page.get_by_text("Automatically update receipt").click()
        if datadictvalue["C_ATMTCLLY_UPDT_RCPT_MTCH_BY"] == 'No':
            if page.get_by_text("Automatically update receipt").is_checked():
                page.get_by_text("Automatically update receipt").click()
        page.get_by_label("AutoCash Rule Set").fill(datadictvalue["C_ATCSH_RULE_SET"])
        page.get_by_label("Remainder Rule Set").fill(datadictvalue["C_RMNDR_RULE_SET"])
        page.get_by_label("Application Exception Rule Set").fill(datadictvalue["C_APPLCTN_EXCPTN_RULE_SET"])
        if datadictvalue["C_ATRCPTS_INCLD_DSPTD_ITEMS"] == 'Yes':
            page.get_by_text("AutoReceipts include disputed").click()

        #Statement and Dunning
        if datadictvalue["C_SEND_STTMNT"] == 'Yes':
            if not page.get_by_text("Send statement").is_checked():
                page.get_by_text("Send statement").click()
        if datadictvalue["C_SEND_STTMNT"] == 'No':
            if page.get_by_text("Send statement").is_checked():
                page.get_by_text("Send statement").click()


        page.get_by_label("Statement Cycle").fill(datadictvalue["C_STTMNT_CYCLE"])

        if datadictvalue["C_SEND_CRDT_BLNC"] == 'Yes':
            if not page.get_by_text("Send credit balance").is_checked():
                page.get_by_text("Send credit balance").click()
        if datadictvalue["C_SEND_CRDT_BLNC"] == 'No':
            if page.get_by_text("Send credit balance").is_checked():
                page.get_by_text("Send credit balance").click()

        if datadictvalue["C_SEND_DNNNG_LTTRS"] == 'Yes':
            if not page.get_by_text("Send dunning letters").is_checked():
                page.get_by_text("Send dunning letters").click()
        if datadictvalue["C_SEND_DNNNG_LTTRS"] == 'No':
            if page.get_by_text("Send dunning letters").is_checked():
                page.get_by_text("Send dunning letters").click()



        page.get_by_label("Preferred Contact Method").select_option(datadictvalue["C_PRFRRD_CNTCT_MTHD"])
        page.get_by_label("Statement Preferred Delivery").select_option(datadictvalue["C_STTMNT_PRFRRD_DLVRY_MTHD"])

        # invoice
        page.get_by_label("Grouping Rule").fill(datadictvalue["C_GRPNG_RULE"])

        # Additional Information
        page.get_by_label("Context Value").select_option(datadictvalue["C_CNTXT_VALUE"])
        page.get_by_label("Regional Information").select_option(datadictvalue["C_RGNL_INFRMTN"])
        # Late Charges
        page.get_by_role("link", name="Late Charges").click()

        if datadictvalue["C_LATE_CHRG_CLCLTN_MTHD"] != '':
            page.get_by_text("Enable late charges").click()
        #Charges and Reductions

            page.get_by_label("Late Charge Calculation Method").select_option(datadictvalue["C_LATE_CHRG_CLCLTN_MTHD"])
            page.get_by_label("Charge Reductions").select_option(datadictvalue["C_CHRG_RDCTNS"])

        # Charge Calculation Setup
            page.get_by_label("Late Charge Type").select_option(datadictvalue["C_LATE_CHRG_TYPE"])
            page.get_by_role("combobox", name="Payment Terms").fill(datadictvalue["C_PYMNT_TERMS"])
            page.get_by_label("Interest Calculation Formula").select_option(datadictvalue["C_INTRST_CLCLTN_FRML"])
            page.get_by_label("Interest Calculation Period").select_option(datadictvalue["C_INTRST_CLCLTN_PRD"])
            if datadictvalue["C_USE_MLTPL_INTRST_RATES"] == 'Yes':
                page.get_by_text("Use multiple interest rates").click()

            page.get_by_label("Receipt Grace Days").fill(str(datadictvalue["C_RCPT_GRACE_DAYS"]))
            page.get_by_label("Interest Days Period").fill(str(datadictvalue["C_INTRST_DAYS_PRD"]))
            page.get_by_label("Assess Late Charges Once").select_option(datadictvalue["C_ASSSS_LATE_CHRGS_ONCE"])
            page.get_by_placeholder("m/d/yy").fill(datadictvalue["C_CHRG_START_DATE"])
            page.get_by_label("Message Text").select_option(datadictvalue["C_MSSG_TEXT"])

        # Currency Setting
        if datadictvalue["C_CRRNCY"] != '':
            page.get_by_role("button", name="Add Row").click()

            page.get_by_label("Currency").select_option(datadictvalue["C_CRRNCY"])
            page.get_by_label("Conversion Rate Type").select_option(datadictvalue["C_LTS_CHRG_CNVRSN_RATE_TYPE"])
            page.get_by_label("Minimum Receipt Amount").fill(datadictvalue["C_MNMM_RCPT_AMNT"])
            page.get_by_label("Minimum Statement Amount").fill(datadictvalue["C_MNMM_STTMNT_AMNT"])
            page.get_by_label("Minimum Dunning Amount").fill(datadictvalue["C_MNMM_DNNNG_AMNT"])
            page.get_by_label("Minimum Dunning Invoice Amount").fill(datadictvalue["C_MNMM_DNNNG_INVC_AMNT"])

        if datadictvalue["C_MNMM_INVC_BLNC_OVRD_TYPE"] == 'Amount':
            page.get_by_label("Minimum Invoice Balance Overdue Type").select_option(datadictvalue["C_MNMM_INVC_BLNC_OVRD_TYPE"])
            page.wait_for_timeout(1000)
            page.get_by_label("Minimum Invoice Balance Overdue Amount").fill(datadictvalue["C_MNMM_INVC_BLNC_OVRD_AMNT"])

        if datadictvalue["C_MNMM_INVC_BLNC_OVRD_TYPE"] == 'Percent':
            page.get_by_label("Minimum Invoice Balance Overdue Type").select_option(datadictvalue["C_MNMM_INVC_BLNC_OVRD_TYPE"])
            page.wait_for_timeout(1000)
            page.get_by_label("Minimum Invoice Balance Overdue Percent").fill(datadictvalue["C_MNMM_INVC_BLNC_OVRD_PRCNT"])

        if datadictvalue["C_MNMM_CSTMR_BLNC_OVRD_TYPE"] == 'Amount':
            page.get_by_label("Minimum Customer Balance Overdue Type").select_option(datadictvalue["C_MNMM_CSTMR_BLNC_OVRD_TYPE"])
            page.wait_for_timeout(1000)
            page.get_by_label("Minimum Customer Balance Overdue Amount").fill(datadictvalue["C_MNMM_CSTMR_BLNC_OVRD_AMNT"])

        if datadictvalue["C_MNMM_CSTMR_BLNC_OVRD_TYPE"] == 'Percent':
            page.get_by_label("Minimum Customer Balance Overdue Type").select_option(datadictvalue["C_MNMM_CSTMR_BLNC_OVRD_TYPE"])
            page.wait_for_timeout(1000)
            page.get_by_label("Minimum Customer Balance Overdue Percent").fill(datadictvalue["C_MNMM_CSTMR_BLNC_OVRD_PRCNT"])


            page.get_by_label("Minimum Late Charge per").fill(datadictvalue["C_MNMM_LATE_CHRG_PER_INVC"])
            page.get_by_label("Maximum Late Charge per").fill(datadictvalue["C_MXMM_LATE_CHRG_PER_INVC"])
            page.get_by_label("Context Value").select_option(datadictvalue["C_LTS_CHRG_CNTXT_VALUE"])

            if datadictvalue["C_INTRST_CHRG_TYPE"] == 'Charge Schedule':
                page.get_by_label("Interest Charge Type").select_option(datadictvalue["C_INTRST_CHRG_TYPE"]) # if selected
                page.get_by_label("Interest Charge Schedule").select_option(datadictvalue["C_INTRST_CHRG_SCHDL"])
            if datadictvalue["C_INTRST_CHRG_TYPE"] == 'Fixed amount':
                page.get_by_label("Interest Charge Type").select_option(datadictvalue["C_INTRST_CHRG_TYPE"]) # if
                page.get_by_label("Interest Charge Amount").fill(datadictvalue["C_INTRST_CHRG_AMNT"])
            if datadictvalue["C_INTRST_CHRG_TYPE"] == 'Fixed rate':
                page.get_by_label("Interest Charge Type").select_option(datadictvalue["C_INTRST_CHRG_TYPE"]) # if selected
                page.get_by_label("Interest Charge Rate").fill(datadictvalue["C_INTRST_CHRG_RATE"])

            if datadictvalue["C_PNLTY_CHRG_TYPE"] == 'Charge schedule':
                page.get_by_label("Penalty Charge Type").select_option(datadictvalue["C_PNLTY_CHRG_TYPE"])
                page.get_by_label("Penalty Charge Schedule").select_option(datadictvalue["C_PNLTY_CHRG_SCHDL"])
            if datadictvalue["C_PNLTY_CHRG_TYPE"] == 'Fixed amount':
                page.get_by_label("Penalty Charge Type").select_option(datadictvalue["C_PNLTY_CHRG_TYPE"])
                page.get_by_label("Penalty Charge Amount").fill(datadictvalue["C_PNLTY_CHRG_AMNT"])
            if datadictvalue["C_PNLTY_CHRG_TYPE"] == 'Fixed rate':
                page.get_by_label("Penalty Charge Type").select_option(datadictvalue["C_PNLTY_CHRG_TYPE"])
                page.get_by_label("Penalty Charge Rate").fill(datadictvalue["C_PNLTY_CHRG_RATE"])

       # Save and Close
        page.wait_for_timeout(2000)
        page.locator("//button[text()='ave and Close']").click()


        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1
        page.wait_for_timeout(3000)
    page.get_by_role("button", name="Done").click()
    page.wait_for_timeout(3000)



    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Receivables Customer Profile Classes Saved Successfully")

    except Exception as e:
        print("Receivables Customer Profile Classes not Saved")


    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, RECEIVABLE_CUSTOMER_PROF):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, RECEIVABLE_CUSTOMER_PROF, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, RECEIVABLE_CUSTOMER_PROF)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + RECEIVABLE_CUSTOMER_PROF)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + RECEIVABLE_CUSTOMER_PROF + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))