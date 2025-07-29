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
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Receivables System Options")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Receivables System Options", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)

        if page.get_by_role("button", name="Create").is_visible():
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(5000)

            #Select the BU

            page.get_by_title("Search: Business Unit").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Business Unit").fill(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(1000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BSNSS_UNIT"]).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)

        #Enter the Billing and Revenue section

        page.get_by_label("Split Amount").fill(str(datadictvalue["C_SPLIT_AMNT"]))
        page.get_by_label("Days in Days Sales Outstanding Calculation").fill(str(datadictvalue["C_DAYS_IN_DAYS_SALES_OTSTNDNG_CLCLTN"]))
        page.get_by_label("Sales Credit Percent Limit").fill(str(datadictvalue["C_SALES_CRDT_PRCNT_LIMIT"]))
        if datadictvalue["C_RQR_SLSPRSN"] == 'Yes':
            page.get_by_text("Require salesperson").check()
        if datadictvalue["C_PRINT_REMIT_TO_ADDRSS"] == 'Yes':
            page.get_by_text("Print remit-to address").check()
        if datadictvalue["C_PRINT_HOME_CNTRY"] == 'Yes':
            page.get_by_text("Print home country").click()
        page.get_by_label("Default Country").select_option(datadictvalue["C_DFLT_CNTRY"])
        page.get_by_label("Application Rule Set").type(datadictvalue["C_APPLCTN_RULE_SET"])
        page.get_by_role("option", name=datadictvalue["C_APPLCTN_RULE_SET"]).click()
        page.get_by_label("Discount Basis").select_option(datadictvalue["C_DSCNT_BASIS"])
        if datadictvalue["C_ALLOW_UNRND_DSCNT"] == 'Yes':
            page.get_by_text("Allow unearned discounts").check()
        if datadictvalue["C_DSCNT_ON_PRTL_PYMNT"] == 'Yes':
            page.get_by_text("Discount on partial payment").check()
        if datadictvalue["C_ALLOW_ANY_BSNSS_UNIT_TO_PRCSS_RCPTS"] == 'Yes':
            page.get_by_text("Allow any business unit to process receipts").check()
        if datadictvalue["C_EXCPTN_RULE_ADJSTMNT_ACTVTY"] != '':
            page.get_by_label("Exception Rule Adjustment Activity").type(datadictvalue["C_EXCPTN_RULE_ADJSTMNT_ACTVTY"])
            page.get_by_role("option", name=datadictvalue["C_EXCPTN_RULE_ADJSTMNT_ACTVTY"]).click()
        page.get_by_label("Exception Rule Adjustment Reason").select_option(datadictvalue["C_EXCPTN_RULE_ADJSTMNT_RSN"])
        if datadictvalue["C_CRDT_CARD_RCPT_MTHD"] != '':
            page.get_by_label("Credit Card Receipt Method").type(datadictvalue["C_CRDT_CARD_RCPT_MTHD"])
            page.get_by_role("option", name=datadictvalue["C_CRDT_CARD_RCPT_MTHD"]).click()
        if datadictvalue["C_BANK_ACCNT_RCPT_MTHD"] != '':
            page.get_by_label("Bank Account Receipt Method").type(datadictvalue["C_CRDT_CARD_RCPT_MTHD"])
            page.get_by_role("option", name=datadictvalue["C_BANK_ACCNT_RCPT_MTHD"]).click()

        #Accounting

        page.get_by_label("Tax Account").click()
        page.get_by_label("Tax Account").fill(datadictvalue["C_TAX_ACCNT"])
        page.get_by_label("Unallocated Revenue Account").fill(datadictvalue["C_UNLLCTD_RVN_ACCNT"])
        page.get_by_label("Cross-Currency Rounding").fill(datadictvalue["C_ACCNTNG_CROSS_CRRNCY_RNDNG_ACCNT"])
        page.get_by_label("Realized Gains Account").fill(datadictvalue["C_ACCNTNG_RLZD_GNS_ACCNT"])
        page.get_by_label("Realized Losses Account").fill(datadictvalue["C_ACCNTNG_RLZD_LSS_ACCNT"])
        if datadictvalue["C_ATMTC_JRNL_IMPRT"] == 'Yes':
            page.get_by_text("Automatic journal import").check()
        if datadictvalue["C_USE_HDR_LEVEL_RNDNG"] == 'Yes':
            page.get_by_text("Use header level rounding").check()
            page.get_by_label("Header Rounding Account").fill(datadictvalue["C_HDR_RNDNG_ACCNT"])
        page.get_by_label("Days per Posting Cycle").fill(str(datadictvalue["C_DAYS_PER_PSTNG_CYCL"]))
        # if datadictvalue["C_ENBL_MLTFND_ACCNTNG"] == 'Yes':
        #     page.get_by_text("Enable multifund accounting").click()

        #Transactions

        page.get_by_label("Tax Invoice Printing Options").select_option(datadictvalue["C_TAX_INVC_PRNTNG_OPTNS"])
        page.get_by_label("Document Number Generation").select_option(datadictvalue["C_DCMNT_NMBR_GNRTN_LEVEL"])
        page.get_by_label("Item Validation Organization").click()
        if datadictvalue["C_ITEM_VLDTN_ORGNZTN"] != '':
            page.get_by_label("Item Validation Organization").type(datadictvalue["C_ITEM_VLDTN_ORGNZTN"])
            page.get_by_role("option", name=datadictvalue["C_ITEM_VLDTN_ORGNZTN"]).click()
        if datadictvalue["C_ALLOW_CHNG_TO_PRNTD_TRNSCTNS"] == 'Yes':
            page.get_by_text("Allow change to printed").check()
        if datadictvalue["C_ALLOW_TRNSCTN_DLTN"] == 'Yes':
            page.get_by_text("Allow transaction deletion").check()
        if datadictvalue["C_ENBL_RCRRNG_BLLNG"] == 'Yes':
            page.get_by_text("Enable recurring billing").check()

        #Transaction Delivery Using Email

        page.get_by_label("From Email").nth(0).click()
        page.get_by_label("From Email").nth(0).fill(datadictvalue["C_TRNSCTN_FROM_EMAIL"])
        page.get_by_label("From Name").nth(0).fill(datadictvalue["C_TRNSCTN_FROM_NAME"])
        page.get_by_label("Reply-to Email").nth(0).fill(datadictvalue["C_REPLY_TO_EMAIL"])
        page.get_by_label("Email Subject",exact=True).nth(0).fill(datadictvalue["C_TRNSCTN_EMAIL_SBJCT"])
        page.get_by_label("Include Business Unit in Email Subject").nth(0).select_option(datadictvalue["C_TRNSCTN_INCLD_BSNSS_UNIT_IN_EMAIL_SBJCT"])
        page.get_by_label("Include Transaction Number in Email Subject").select_option(datadictvalue["C_INCLD_TRNSCTN_NMBR_IN_EMAIL_SBJCT"])
        page.get_by_label("Email Body").nth(0).fill(datadictvalue["C_EMAIL_BODY"])

        #Statement Delivery Using Email

        page.get_by_label("From Email").nth(1).click()
        page.get_by_label("From Email").nth(1).fill(datadictvalue["C_FROM_EMAIL"])
        page.get_by_label("From Name").nth(1).fill(datadictvalue["C_FROM_NAME"])
        page.get_by_label("Reply-to Email").nth(1).fill(datadictvalue["C_REPLY_TO_EMAIL"])
        page.get_by_label("Email Subject",exact=True).nth(1).fill(datadictvalue["C_EMAIL_SBJCT"])
        page.get_by_label("Include Business Unit in Email Subject").nth(1).select_option(datadictvalue["C_INCLD_BSNSS_UNIT_IN_EMAIL_SBJCT"])
        page.get_by_label("Include Statement Date in Email Subject").select_option(datadictvalue["C_INCLD_STTMNT_NMBR_IN_EMAIL_SBJCT"])
        page.get_by_label("Email Body").nth(1).fill(datadictvalue["C_EMAIL_BODY"])

        #Late Charges
        if datadictvalue["C_ASSSS_LATE_CHRGS"] == 'Yes':
            page.get_by_text("Assess late charges").check()
        page.get_by_label("Average Daily Balance Calculation Basis").click()
        page.get_by_label("Average Daily Balance Calculation Basis").select_option(datadictvalue["C_AVRG_DAILY_BLNC_CLCLTN_BASIS"])
        page.get_by_label("Average Daily Balance Calculation Period").select_option(datadictvalue["C_AVRG_DAILY_BLNC_CLCLTN_PRD"])
        if datadictvalue["C_INTRST_INVC_TRNSCTN_TYPE"]!='':
            page.get_by_label("Interest Invoice Transaction").type(datadictvalue["C_INTRST_INVC_TRNSCTN_TYPE"])
            page.get_by_role("option", name=datadictvalue["C_INTRST_INVC_TRNSCTN_TYPE"]).click()
        if datadictvalue["C_DEBIT_MEMO_CHRG_TRNSCTN_TYPE"] != '':
            page.get_by_label("Debit Memo Charge Transaction").type(datadictvalue["C_DEBIT_MEMO_CHRG_TRNSCTN_TYPE"])
            page.get_by_role("option", name=datadictvalue["C_DEBIT_MEMO_CHRG_TRNSCTN_TYPE"]).click()
        page.get_by_label("Interest Charge Activity").select_option(datadictvalue["C_INTRST_CHRG_ACTVTY"])
        page.get_by_label("Penalty Charge Activity").select_option(datadictvalue["C_PNLTY_CHRG_ACTVTY"])
        if datadictvalue["C_LATE_CHRG_TRNSCTN_SRC"] != '':
            page.get_by_label("Late Charge Transaction Source").type(datadictvalue["C_LATE_CHRG_TRNSCTN_SRC"])
            page.get_by_role("option", name=datadictvalue["C_LATE_CHRG_TRNSCTN_SRC"]).click()

        # Customers
        page.get_by_label("Grouping Rule").select_option(datadictvalue["C_GRPNG_RULE"])
        if datadictvalue["C_CRT_RCPRCL_CSTMR"] == 'Yes':
            page.get_by_text("Create reciprocal customer").check()

        #AutoInvoice
        if datadictvalue["C_PURGE_INTRFC_TBLS"] == 'Yes':
            page.get_by_text("Purge interface tables").check()
        page.get_by_label("Maximum Memory in Bytes").click()
        page.get_by_label("Maximum Memory in Bytes").fill(str(datadictvalue["C_MXMM_MMRY_IN_BYTES"]))
        page.get_by_label("Log File Message Level").fill(str(datadictvalue["C_LOG_FILE_MSSG_LEVEL"]))
        page.get_by_label("Accounting Dates Out of Order").select_option(datadictvalue["C_ACCNTNG_DATES_OUT_OF_ORDER"])

        #Tuning Segments
        page.get_by_label("Accounting Flexfield").click()
        page.get_by_label("Accounting Flexfield").select_option(datadictvalue["C_ACCNTNG_FLXFLD"])
        page.get_by_label("System Items").select_option(datadictvalue["C_SYSTM_ITEMS"])
        page.wait_for_timeout(2000)

        #Cash Processing

        page.get_by_role("link", name="Cash Processing").click()
        page.wait_for_timeout(1000)
        if datadictvalue["C_ATCSH_RULE_SET"] != '':
            page.get_by_label("AutoCash Rule Set").type(datadictvalue["C_ATCSH_RULE_SET"])
            page.get_by_role("option", name=datadictvalue["C_ATCSH_RULE_SET"]).click()
        page.get_by_label("Match Receipts By", exact=True).select_option(datadictvalue["C_MATCH_RCPTS_BY"])
        page.get_by_label("Match Receipts By 2", exact=True).select_option(datadictvalue["C_MATCH_RCPTS_BY_2"])
        page.get_by_label("Match Receipts By 3", exact=True).select_option(datadictvalue["C_MATCH_RCPTS_BY_3"])
        page.get_by_label("Match Receipts By 4", exact=True).select_option(datadictvalue["C_MATCH_RCPTS_BY_4"])
        if datadictvalue["C_USE_AUTO_APPLY"] == 'Yes':
            page.get_by_text("Use AutoApply").check()
        page.get_by_label("Days to AutoApply a Receipt").fill(datadictvalue["C_DAYS_TO_ATPPLY_A_RCPT"])
        if datadictvalue["C_RQR_BLLNG_LCTN_FOR_RCPTS"] == 'Yes':
            page.get_by_text("Require billing location for").check()
        if datadictvalue["C_ALLOW_PYMNT_OF_UNRLTD_TRNSCTNS"] == 'Yes':
            page.get_by_text("Allow payment of unrelated").check()
        # if datadictvalue["C_ENBL_CHNNL_RVN_MGMNT_INTGRTN"] == 'Yes':
        #     page.get_by_text("Enable channel revenue").check()
        #     page.get_by_label("Lockbox Claim for Invalid").select_option(datadictvalue["C_LCKBX_FOR_INVLD_TRNSCTN_RFRNC"])
        page.get_by_label("From Write-Off Limit per").fill(str(datadictvalue["C_FROM_WRITE_OFF_LIMIT_PER_RCPT"]))
        page.get_by_label("To Write-Off Limit per Receipt").fill(str(datadictvalue["C_TO_WRITE_OFF_LIMIT_PER_RCPT"]))
        page.get_by_label("Minimum Refund Amount").fill(str(datadictvalue["C_MNMM_RFND_AMNT"]))
        page.get_by_label("Chargeback Due Date").select_option(datadictvalue["C_CHRGBCK_DUE_DATE"])
        if datadictvalue["C_ALLOW_PYMNT_DLTN"] == 'Yes':
            page.get_by_text("Allow payment deletion").click()
        # if datadictvalue["C_ATMTCH_RULE_SET"] != '':
        #     page.get_by_label("AutoMatch Rule Set").type(datadictvalue["C_ATMTCH_RULE_SET"])
        #     page.get_by_role("option", name=datadictvalue["C_ATMTCH_RULE_SET"]).click()

        #Application Exception Rule

        if datadictvalue["C_APPLCTN_EXCPTN_RULE_SET"] !='':
            page.get_by_label("Application Exception Rule Set").type(datadictvalue["C_APPLCTN_EXCPTN_RULE_SET"])
            page.get_by_role("option", name=datadictvalue["C_APPLCTN_EXCPTN_RULE_SET"]).click()
        if datadictvalue["C_EXCPTN_RULE_WRITE_OFF_ACTVTY"] != '':
            page.get_by_label("Exception Rule Write-Off").type(datadictvalue["C_EXCPTN_RULE_WRITE_OFF_ACTVTY"])
            page.get_by_role("option", name=datadictvalue["C_EXCPTN_RULE_WRITE_OFF_ACTVTY"]).click()
        if datadictvalue["C_EXCPTN_RULE_RFND_PYMNT_MTHD"] != '':
            page.get_by_label("Exception Rule Refund Payment").type(datadictvalue["C_EXCPTN_RULE_RFND_PYMNT_MTHD"])
            page.get_by_role("option", name=datadictvalue["C_EXCPTN_RULE_RFND_PYMNT_MTHD"]).click()

        #Accounting

        page.get_by_label("Realized Gains Account").click()
        page.get_by_label("Realized Gains Account").clear()
        page.get_by_label("Realized Gains Account").fill(datadictvalue["C_RLZD_GAINS_ACCNT"])
        page.get_by_label("Realized Losses Account").clear()
        page.get_by_label("Realized Losses Account").fill(datadictvalue["C_RLZD_LSSSS_ACCNT"])
        page.get_by_label("Cross-Currency Rate Type").clear()
        if datadictvalue["C_CROSS_CRRNCY_RATE_TYPE"] != '':
            page.get_by_label("Cross-Currency Rate Type").fill(datadictvalue["C_CROSS_CRRNCY_RATE_TYPE"])
            page.get_by_role("option", name=datadictvalue["C_CROSS_CRRNCY_RATE_TYPE"]).click()
        page.get_by_label("Cross-Currency Rounding").clear()
        page.get_by_label("Cross-Currency Rounding").fill(datadictvalue["C_CROSS_CRRNCY_RNDNG_ACCNT"])

        #Automatic Receipts

        page.get_by_label("Receipt Confirmation").click()
        page.get_by_label("Receipt Confirmation").fill(str(datadictvalue["C_RCPT_CNFRMTN_THRSHLD_AMNT"]))
        page.get_by_label("Invoices per Commit").fill(str(datadictvalue["C_INVCS_PER_CMMT"]))
        page.get_by_label("Receipts per Commit").fill(str(datadictvalue["C_RCPTS_PER_CMMT"]))

        #Bills Receivable

        if datadictvalue["C_ENBL_BILLS_RCVBL"] == 'Yes':
            page.get_by_text("Enable bills receivable").check()
        page.get_by_label("Bills Receivable Transaction").click()
        if datadictvalue["C_BILLS_RCVBL_TRNSCTN_SRC"] != '':
            page.get_by_label("Bills Receivable Transaction").type(datadictvalue["C_BILLS_RCVBL_TRNSCTN_SRC"])
            page.get_by_role("option", name=datadictvalue["C_BILLS_RCVBL_TRNSCTN_SRC"]).click()
        if datadictvalue["C_ALLOW_FCTRNG_OF_BILLS_RCVBL_WTHT_RCRS"] == 'Yes':
            page.get_by_text("Allow factoring of bills").check()

        # Save the data

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        if page.locator("//div[text()='Warning']//following::button[1]").is_visible():
            page.locator("//div[text()='Warning']//following::button[1]").click()
        if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
            page.locator("//div[text()='Confirmation']//following::button[1]").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Receivables System Options saved Successfully")
            datadictvalue["RowStatus"] = "Receivables System Options added successfully"

        except Exception as e:
            print("Receivables System Options not saved")
            datadictvalue["RowStatus"] = "Receivables System Options not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, RECEIVABLES_SYS_OPT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, RECEIVABLES_SYS_OPT, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, RECEIVABLES_SYS_OPT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + RECEIVABLES_SYS_OPT)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + RECEIVABLES_SYS_OPT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
