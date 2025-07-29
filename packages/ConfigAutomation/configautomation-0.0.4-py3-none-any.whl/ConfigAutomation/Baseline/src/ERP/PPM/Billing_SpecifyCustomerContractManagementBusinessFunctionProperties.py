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
    page.get_by_role("textbox").fill("Specify Customer Contract Management Business Function Properties")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Specify Customer Contract Management Business Function Properties", exact=True).click()
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        #Select the Business Unit
        page.get_by_title("Business Unit", exact=True).click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Business Unit").fill(datadictvalue["C_BSNSS_UNIT"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BSNSS_UNIT"]).click()
        page.get_by_role("button", name="OK").click()
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(4000)

        #Enter the Hide section
        if datadictvalue["C_ENBL_MLTCRRNCY"] == 'Yes':
            page.get_by_text("Enable multicurrency").check()
        if datadictvalue["C_ENBL_MLTCRRNCY"] == 'No':
            page.get_by_text("Enable multicurrency").uncheck()
        if datadictvalue["C_ALLOW_RLTD_CSTMR_ACCNTS"] == 'Yes':
            page.get_by_text("Allow related customer").check()
        if datadictvalue["C_ALLOW_RLTD_CSTMR_ACCNTS"] == 'No':
            page.get_by_text("Allow related customer").uncheck()
        page.wait_for_timeout(2000)

        #Enter the Currency Conversion

        #Bill Transaction Currency to Contract Currency

        page.get_by_title("Search: Conversion Rate Type").first.click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Rate Type", exact=True).fill(datadictvalue["C_BILL_CNVRSN_RATE_TYPE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BILL_CNVRSN_RATE_TYPE"]).click()
        page.get_by_role("button", name="OK").click()
        page.get_by_label("Conversion Date Type").first.click()
        page.get_by_label("Conversion Date Type").first.select_option(datadictvalue["C_BILL_CNVRSN_DATE_TYPE"])
        if datadictvalue["C_BILL_CNVRSN_DATE_TYPE"] == 'Fixed date':
            page.locator("//div[@title='Bill Transaction Currency to Contract Currency']//following::label[text()='Conversion Date']//following::input[1]").fill(datadictvalue["C_CNVRSN_DATE"].strftime("%m/%d/%Y"))

        #Invoice Currency to Ledger Currency
        #nvoice Transaction
        page.get_by_title("Search: Conversion Rate Type").nth(1).click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Rate Type", exact=True).fill(datadictvalue["C_INVC_CNVRSN_RATE_TYPE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_INVC_CNVRSN_RATE_TYPE"]).click()
        page.get_by_role("button", name="OK").click()
        # page.get_by_role("cell", name="Invoice Transaction Enter").get_by_label("Conversion Date Type").select_option(datadictvalue["C_INVC_CNVRSN_DATE_TYPE"])
        page.locator("//div[@title='Invoice Transaction']//following::label[text()='Conversion Date Type'][1]").select_option(datadictvalue["C_INVC_CNVRSN_DATE_TYPE"])

        #Revenue Transaction
        page.get_by_title("Search: Conversion Rate Type").nth(2).click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Rate Type", exact=True).fill(datadictvalue["C_RVN_CNVRSN_RATE_TYPE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RVN_CNVRSN_RATE_TYPE"]).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        # page.get_by_role("cell", name="Revenue Transaction Enter").get_by_label("Conversion Date Type").select_option(datadictvalue["C_RVN_CNVRSN_DATE_TYPE"])
        # page.get_by_label("Conversion Date Type").nth(2).click()
        # page.get_by_label("Conversion Date Type").nth(2).select_option(datadictvalue["C_RVN_CNVRSN_DATE_TYPE"])
        page.locator("//div[@title='Revenue Transaction']//following::label[text()='Conversion Date Type'][1]").select_option(datadictvalue["C_RVN_CNVRSN_DATE_TYPE"])

        page.wait_for_timeout(2000)

        #Project Billing
        if datadictvalue["C_TRNSFR_RVN_TO_GNRL_LDGR"] == 'Yes':
            page.get_by_text("Transfer revenue to general").check()
        if datadictvalue["C_TRNSFR_RVN_TO_GNRL_LDGR"] == 'No':
            page.get_by_text("Transfer revenue to general").uncheck()
        if datadictvalue["C_RQR_CRDT_MM_RSN"] == 'Yes':
            page.get_by_text("Require credit memo reason").check()
        if datadictvalue["C_RQR_CRDT_MM_RSN"] == 'No':
            page.get_by_text("Require credit memo reason").uncheck()
        #Customer Billing
        # page.get_by_role("cell", name="Customer Billing").get_by_label("Invoice Numbering Method").click()
        # page.get_by_role("cell", name="Customer Billing").get_by_label("Invoice Numbering Method").select_option(datadictvalue["C_CSTMR_BLLNG_INVC_NMBRNG_MTHD"])
        page.locator("//div[@title='Customer Billing']//following::label[text()='Invoice Numbering Method'][1]").select_option(datadictvalue["C_CSTMR_BLLNG_INVC_NMBRNG_MTHD"])

        if datadictvalue["C_CSTMR_BLLNG_INVC_NMBRNG_MTHD"] == 'Manual':
            page.get_by_role("cell", name="Customer Billing").get_by_label("Invoice Number Type").select_option(datadictvalue["C_CSTMR_BLLNG_INVC_NMBR_TYPE"])
        if datadictvalue["C_CSTMR_BLLNG_INVC_NMBRNG_MTHD"] == 'Automatic':
            # page.get_by_role("cell", name="Customer Billing").get_by_label("Next Invoice Number").clear()
            # page.get_by_role("cell", name="Customer Billing").get_by_label("Next Invoice Number").fill(str(datadictvalue["C_NEXT_INVC_NMBR"]))
            page.locator("//div[@title='Customer Billing']//following::label[text()='Next Invoice Number'][1]").clear()
            page.locator("//div[@title='Customer Billing']//following::label[text()='Next Invoice Number'][1]").fill(str(datadictvalue["C_NEXT_INVC_NMBR"]))
        page.get_by_title("Invoice Batch Source").first.click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Name").clear()
        page.get_by_label("Name").fill(datadictvalue["C_CSTMR_BLLNG_INVC_BATCH_SRC"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CSTMR_BLLNG_INVC_BATCH_SRC"]).click()
        page.get_by_role("button", name="OK").click()
        if datadictvalue["C_RQR_MNL_ENTRY_OF_TRNSCTN_TYPE"] == 'Yes':
            page.get_by_text("Require manual entry of transaction type").check()
        if datadictvalue["C_RQR_MNL_ENTRY_OF_TRNSCTN_TYPE"] == 'No':
            page.get_by_text("Require manual entry of transaction type").uncheck()

        #Internal Billing
        # page.get_by_role("cell", name="Internal Billing").get_by_label("Invoice Numbering Method").click()
        # page.get_by_role("cell", name="Internal Billing").get_by_label("Invoice Numbering Method").select_option(datadictvalue["C_INVC_NMBRNG_MTHD"])
        page.locator("//div[@title='Internal Billing']//following::label[text()='Invoice Numbering Method'][1]").select_option(datadictvalue["C_INVC_NMBRNG_MTHD"])

        if datadictvalue["C_INVC_NMBRNG_MTHD"] == 'Manual':
            page.get_by_role("cell", name="Internal Billing").get_by_label("Invoice Number Type").select_option(
                datadictvalue["C_INVC_NMBR_TYPE"])
        if datadictvalue["C_INVC_NMBRNG_MTHD"] == 'Automatic':
            # page.get_by_role("cell", name="Internal Billing").get_by_label("Next Invoice Number").clear()
            # page.get_by_role("cell", name="Internal Billing").get_by_label("Next Invoice Number").fill(str(datadictvalue["C_NXT_NVC_NMBR"]))
            page.locator("//div[@title='Internal Billing']//following::label[text()='Next Invoice Number'][1]").clear()
            page.locator("//div[@title='Internal Billing']//following::label[text()='Next Invoice Number'][1]").fill(str(datadictvalue["C_NXT_NVC_NMBR"]))

        page.get_by_title("Invoice Batch Source").nth(1).click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Name").clear()
        page.get_by_label("Name").fill(datadictvalue["C_INVC_BATCH_SRC"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_INVC_BATCH_SRC"]).click()
        page.get_by_role("button", name="OK").click()
        # page.get_by_text("Release invoices on approval").check()

        #Terms Library
        #Common to Buy and Sell Intent
        if datadictvalue["C_GLBL_BSNSS_UNIT"] == 'Yes':
            page.get_by_text("Global business unit").check()
        if datadictvalue["C_GLBL_BSNSS_UNIT"] == 'No':
            page.get_by_text("Global business unit").uncheck()
        page.get_by_label("Clause Numbering Method").select_option(datadictvalue["C_CLS_NMBRNG_MTHD"])
        if datadictvalue["C_CLS_NMBRNG_MTHD"] == 'Automatic':
            page.get_by_label("Clause Numbering Level").select_option(datadictvalue["C_CLS_NMBRNG_LEVEL"])
            page.get_by_label("Clause Sequence Category").select_option(datadictvalue["C_CLS_SQNC_CTGRY"])

        #Sell Intent Only
        if datadictvalue["C_ENBL_CNTRCT_EXPRT"] == 'Yes':
            page.get_by_text("Enable Contract Expert").check()
        if datadictvalue["C_ENBL_CNTRCT_EXPRT"] == 'No':
            page.get_by_text("Enable Contract Expert").uncheck()
        if page.get_by_text("Automatically adopt global").is_enabled():
            if datadictvalue["C_ATMTCLLY_ADPT_GLBL_CLSS"] == 'Yes':
                page.get_by_text("Automatically adopt global").check()
            if datadictvalue["C_ATMTCLLY_ADPT_GLBL_CLSS"] == 'No':
                page.get_by_text("Automatically adopt global").uncheck()
        if datadictvalue["C_DSPLY_CLS_NMBR_IN_CLS_TTL"] == 'Yes':
            page.get_by_text("Display clause number in clause title").check()
        if datadictvalue["C_DSPLY_CLS_NMBR_IN_CLS_TTL"] == 'No':
            page.get_by_text("Display clause number in clause title").uncheck()
        page.get_by_label("Clause Layout Template").select_option(datadictvalue["C_CLS_LYT_TMPLT"])
        page.get_by_label("Deviations Layout Template").select_option(datadictvalue["C_DVTNS_LYT_TMPLT"])
        if datadictvalue["C_TRMS_LBRRY_ADMNSTRTR"] != '':
            page.get_by_role("link", name="Terms Library Administrator").click()
            page.get_by_label("ListName").fill(datadictvalue["C_TRMS_LBRRY_ADMNSTRTR"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_TRMS_LBRRY_ADMNSTRTR"], exact=True).click()
            page.get_by_role("button", name="OK").click()

        page.wait_for_timeout(3000)
        page.get_by_title("Save").click()
        page.get_by_text("&Save and Close").click()
        page.wait_for_timeout(2000)

        i = i + 1


        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Specify Customer Contract Management Business Function Properties Saved Successfully")
            datadictvalue["RowStatus"] = "Specify Customer Contract Management Business Function Properties are added successfully"

        except Exception as e:
            print("Specify Customer Contract Management Business Function Properties not saved")
            datadictvalue["RowStatus"] = "Specify Customer Contract Management Business Function Properties not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_BILLING_CONFIG_WRKBK, SPCFY_CSTMR_CNTRCT_MNGMNT_BSNSS_FNCTN_PRPRTS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_BILLING_CONFIG_WRKBK, SPCFY_CSTMR_CNTRCT_MNGMNT_BSNSS_FNCTN_PRPRTS,
                             PRCS_DIR_PATH + PPM_BILLING_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_BILLING_CONFIG_WRKBK, SPCFY_CSTMR_CNTRCT_MNGMNT_BSNSS_FNCTN_PRPRTS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_BILLING_CONFIG_WRKBK)[0] + "_" + SPCFY_CSTMR_CNTRCT_MNGMNT_BSNSS_FNCTN_PRPRTS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_BILLING_CONFIG_WRKBK)[
            0] + "_" + SPCFY_CSTMR_CNTRCT_MNGMNT_BSNSS_FNCTN_PRPRTS + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))






