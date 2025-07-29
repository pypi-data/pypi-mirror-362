from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *



# Need To Run Manage Primary Ledger to create Ledger
def configure(playwright: Playwright, rowcount, datadict,videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="Offering").click()
    page.get_by_text("General Ledger").click()
    page.get_by_title("General Ledger", exact=True).click()
    page.wait_for_timeout(2000)

    i = 0
    while i < rowcount:
        page.wait_for_timeout(3000)
        datadictvalue = datadict[i]

        page.get_by_role("row", name="Specify Ledger Options").nth(0).get_by_role("link").nth(1).click()
        page.get_by_label("Primary Ledger", exact=True).click()
        page.get_by_label("Primary Ledger", exact=True).select_option("Select and Add")

        page.get_by_role("button", name="Apply and Go to Task").click()
        page.wait_for_timeout(2000)
        page.locator("//div[@title='Manage Primary Ledgers']//following::input[1]").fill(datadictvalue["C_NAME"])
        page.locator("//div[@title='Manage Primary Ledgers']//following::input[1]").press("Enter")
        page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name=datadictvalue["C_NAME"]).nth(1).click()
        #page.get_by_text(datadictvalue["C_NAME"]).click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()


        # General Information
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        # Accounting Calender

        page.get_by_title("Search: First Opened Period").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Period Name").click()
        page.get_by_label("Period Name").fill(datadictvalue["C_FIRST_OPND_PRD"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FIRST_OPND_PRD"]).click()
        page.get_by_role("button", name="OK").click()

        page.get_by_label("Number of Future Enterable").fill(str(datadictvalue["C_NMBR_OF_FTR_ENTRBL_PRD"]))

        # Subledger Accounting
        page.get_by_label("Accounting Method").click()
        page.get_by_label("Accounting Method").select_option(datadictvalue["C_ACCNTNG_MTHD"])
        page.get_by_title("Search: Journal Language").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Description").nth(1).fill(datadictvalue["C_JRNL_LNGG"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("cell", name=datadictvalue["C_JRNL_LNGG"], exact=True).locator("span").click()
        page.get_by_role("button", name="OK").click()

        # Period Close

        page.get_by_label("Retained Earnings Account").fill(datadictvalue["C_RTND_ERNGS_ACCNT"])
        page.wait_for_timeout(2000)

        page.get_by_label("Cumulative Translation").fill(datadictvalue["C_CMLTV_TRNSLTN_ADJSTMNT_ACCNT"])

        if datadictvalue["C_NET_CLSNG_BLNC_JRNL"] == 'Yes':
            if not page.locator("//label[text()='Net Closing Balance Journal']//following::label[1]").is_checked():
                page.locator("//label[text()='Net Closing Balance Journal']//following::label[1]").click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="OK").click()
        if datadictvalue["C_NET_CLSNG_BLNC_JRNL"] == 'No':
            if page.locator("//label[text()='Net Closing Balance Journal']//following::label[1]").is_checked():
                page.locator("//label[text()='Net Closing Balance Journal']//following::label[1]").uncheck()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="OK").click()

        page.get_by_label("Default Period End Rate Type").fill(datadictvalue["C_DFLT_PRD_END_RATE_TYPE"])
        page.get_by_label("Default Period Average Rate").fill(datadictvalue["C_DFLT_PRD_AVRGE_RATE_TYPE"])

        if datadictvalue["C_PRVNT_GL_PRD_CLOSE_WHEN_OPEN_SBLDGR_PRDS_EXIST"] == 'Yes':
            page.locator("//label[text()='Prevent General Ledger Period Closure When Open Subledger Periods Exist']//following::label[1]").check()

        if datadictvalue["C_PRVNT_GL_PRD_CLOSE_WHEN_OPEN_SBLDGR_PRDS_EXIST"] == 'No':
            page.locator("//label[text()='Prevent General Ledger Period Closure When Open Subledger Periods Exist']//following::label[1]").uncheck()

        # Journal Processing

        if datadictvalue["C_ENBL_SSPNS_GNRL_LDGR"] == 'Yes':
            page.locator("//label[text()='General Ledger']//following::label[1]").check()

        if datadictvalue["C_ENBL_SSPNS_GNRL_LDGR"] == 'No':
            page.locator("//label[text()='General Ledger']//following::label[1]").uncheck()

        if datadictvalue["C_ENBL_SSPNS_SBLDGR_ACCNTNG"] == 'Yes':
           page.locator("//label[text()='Subledger Accounting']").check()

        if datadictvalue["C_ENBL_SSPNS_SBLDGR_ACCNTNG"] == 'No':
            page.locator("//label[text()='Subledger Accounting']").uncheck()

        page.get_by_label("Default Suspense Account").fill(datadictvalue["C_DFLT_SSPNS_ACCNT"])
        page.get_by_label("Rounding Account").fill(datadictvalue["C_RNDNG_ACCNT"])
        page.get_by_label("Entered Currency Balancing").fill(datadictvalue["C_ENTRD_CRRNCY_BLNCNG_ACCNT"])
        page.get_by_label("Balancing Threshold Percent").fill(datadictvalue["C_BLNCNG_THRSHLD_PRCNT"])

        if datadictvalue["C_RQR_MNLLY_ENTRD_JRNLS_BLNCD_BY_CRRNCY"] == 'Yes':
            page.locator("//label[text()='Require manually entered journals balance by currency']//following::label[1]").check()

        if datadictvalue["C_RQR_MNLLY_ENTRD_JRNLS_BLNCD_BY_CRRNCY"] == 'No':
            page.locator("//label[text()='Require manually entered journals balance by currency']//following::label[1]").uncheck()

        # "Enable journal approval"

        if datadictvalue["C_ENBL_JRNL_APPRVL"] == 'Yes':
           page.get_by_text("Enable journal and manual subledger entry approval").check()

        if datadictvalue["C_ENBL_JRNL_APPRVL"] == 'No':
            page.get_by_text("Enable journal and manual subledger entry approval").uncheck()

        # page.get_by_text("Notify when prior period").click()

        if datadictvalue["C_NTFY_WHEN_PRIOR_PRD_JRNL_IS_ENTRD"] == 'Yes':
            page.get_by_text("Notify when prior period journal is entered").check()

        if datadictvalue["C_NTFY_WHEN_PRIOR_PRD_JRNL_IS_ENTRD"] == 'No':
           page.get_by_text("Notify when prior period journal is entered").uncheck()
        # "Allow mixed statistical
        if datadictvalue["C_ALLOW_MIXED_STSTCL_AND_MNTRY_JRNLS"] == 'Yes':
            page.get_by_text("Allow mixed statistical and monetary journals").check()

        if datadictvalue["C_ALLOW_MIXED_STSTCL_AND_MNTRY_JRNLS"] == 'No':
            page.get_by_text("Allow mixed statistical and monetary journals").uncheck()

        if datadictvalue["C_VLDT_RFRNC_DATE"] == 'Yes':
            page.get_by_text("Validate reference date").check()

        if datadictvalue["C_VLDT_RFRNC_DATE"] == 'No':
            page.get_by_text("Validate reference date").uncheck()

        if datadictvalue["C_ENBL_RCNCLTN"] == 'Yes':
            page.get_by_text("Enable reconciliation").check()

        if datadictvalue["C_ENBL_RCNCLTN"] == 'No':
           page.get_by_text("Enable reconciliation").uncheck()

        if datadictvalue["C_SPRT_JRNLS_BY_ACCNTNG_DATE_DRNG_JRNL_IMPRT"] == 'Yes':
            page.get_by_text("Separate journals by accounting date during journal import").check()

        if datadictvalue["C_SPRT_JRNLS_BY_ACCNTNG_DATE_DRNG_JRNL_IMPRT"] == 'No':
            page.get_by_text("Separate journals by accounting date during journal import").uncheck()

        # page.get_by_text("Enable intercompany accounting").click()

        if datadictvalue["C_ENBL_INTRCMPNY_ACCNTNG"] == 'Yes':
            page.get_by_text("Enable intercompany accounting").check()

        if datadictvalue["C_ENBL_INTRCMPNY_ACCNTNG"] == 'No':
            page.get_by_text("Enable intercompany accounting").uncheck()

        page.wait_for_timeout(5000)
        page.get_by_label("Journal Reversal Criteria Set").type(datadictvalue["C_JRNL_RVRSL_CRTR_SET"])
        page.get_by_label("Journal Reversal Criteria Set").press("Tab")

        # page.get_by_title("Search: Journal Reversal").click()
        # page.get_by_role("link", name="Search...").click()
        # page.get_by_role("textbox", name="Journal Reversal Criteria Set").clear()
        # page.get_by_role("textbox", name="Journal Reversal Criteria Set").fill(datadictvalue["C_JRNL_RVRSL_CRTR_SET"])
        # page.get_by_role("button", name="Search", exact=True).click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_JRNL_RVRSL_CRTR_SET"]).click()
        # page.get_by_role("button", name="OK").click()

        if datadictvalue["C_RUN_ATRVRS_AFTER_OPEN_PRD"] == 'Yes':
            page.get_by_text("Run AutoReverse after open period").check()

        if datadictvalue["C_RUN_ATRVRS_AFTER_OPEN_PRD"] == 'No':
            page.get_by_text("Run AutoReverse after open period").uncheck()

        # page.get_by_text("Synchronize Reversals Between").click()

        if datadictvalue["C_SYNCHRNZ_RVRSLS_BTWN_PRMRY_AND_SCNDRY_LDGRS"] == 'Yes':
            page.get_by_text("Synchronize Reversals Between Primary and Secondary Ledgers").check()

        if datadictvalue["C_SYNCHRNZ_RVRSLS_BTWN_PRMRY_AND_SCNDRY_LDGRS"] == 'No':
            page.get_by_text("Synchronize Reversals Between Primary and Secondary Ledgers").uncheck()

        page.get_by_text(datadictvalue["C_SQNCNG_BY"], exact=True).click()

        if datadictvalue["C_ENFRC_DCMNT_SQNCNG_PYBLS"] == 'Yes':
            page.get_by_text("Payables").nth(1).check()

        if datadictvalue["C_ENFRC_DCMNT_SQNCNG_PYBLS"] == 'No':
            page.get_by_text("Payables").nth(1).uncheck()

        if datadictvalue["C_ENFRC_DCMNT_SQNCNG_RCVBLS"] == 'Yes':
            page.get_by_text("Receivables").nth(1).check()

        if datadictvalue["C_ENFRC_DCMNT_SQNCNG_RCVBLS"] == 'No':
            page.get_by_text("Receivables").nth(1).uncheck()

        if datadictvalue["C_ENFRC_CHRNLGCL_ORDER_ON_DCMNT_DATE_PYBLS"] == 'Yes':
            page.get_by_text("Payables").nth(2).check()

        if datadictvalue["C_ENFRC_CHRNLGCL_ORDER_ON_DCMNT_DATE_PYBLS"] == 'No':
            page.get_by_text("Payables").nth(2).uncheck()

        if datadictvalue["C_ENFRC_CHRNLGCL_ORDER_ON_DCMNT_DATE_RCVBLS"] == 'Yes':
            page.get_by_text("Receivables").nth(2).check()

        elif datadictvalue["C_ENFRC_CHRNLGCL_ORDER_ON_DCMNT_DATE_RCVBLS"] == 'No':
            page.get_by_text("Receivables").nth(2).uncheck()

        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        i = i + 1


        try:
            expect(page.get_by_text("Search Tasks")).to_be_visible()
            print("Specify PrimaryLedger Saved Successfully")
            datadictvalue["RowStatus"] = "Successfully Added Ledger"

        except Exception as e:
            print("Specify PrimaryLedger not saved")
            datadictvalue["RowStatus"] = "Specify PrimaryLedger not saved"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, LEDGER):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, LEDGER, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, LEDGER)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + LEDGER)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + LEDGER + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
