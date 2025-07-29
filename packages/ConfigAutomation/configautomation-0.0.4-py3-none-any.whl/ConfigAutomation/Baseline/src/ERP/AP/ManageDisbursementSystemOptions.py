from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
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
    page.get_by_role("textbox").fill("Manage Disbursement System Options")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Disbursement System Options", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        if datadictvalue["C_SYSTM_STTNGS_ALLOW_PAYEE_BANK_ACCNT_OVRRD_ON_PRPSD_PYMNTS"] == 'Yes':
            page.wait_for_timeout(2000)
            if not page.get_by_text("Allow payee bank account override on proposed payments", exact=True).is_checked():
                page.get_by_text("Allow payee bank account override on proposed payments", exact=True).click()
        #
        elif datadictvalue["C_SYSTM_STTNGS_ALLOW_PAYEE_BANK_ACCNT_OVRRD_ON_PRPSD_PYMNTS"] == 'No':
            if page.get_by_text("Allow payee bank account override on proposed payments", exact=True).is_checked():
                page.get_by_text("Allow payee bank account override on proposed payments", exact=True).click()

        if datadictvalue["C_BASED_ONLY_ON_PYMNT_MTHD_DFLTNG_RULES_SETUP"] == 'Yes':
            page.get_by_role("group").get_by_text("Based only on payment method").click()
        if datadictvalue["C_OVRRD_DFLTNG_RULES_WHEN_PAYEE_DFLT_MTHD_SET"] == 'Yes':
            page.get_by_role("group").get_by_text("Override defaulting rules").click()

        page.get_by_label("Separate Remittance Advice from Email").fill(datadictvalue["C_SPRT_RMTTNC_ADVC_FROM_EMAIL"])
        page.get_by_label("Separate Remittance Advice Subject").fill(datadictvalue["C_SPRT_RMTTNC_ADVC_SBJCT"])
        page.get_by_label("Document", exact=True).select_option(datadictvalue["C_DCMNT"])
        page.get_by_label("Payment", exact=True).select_option(datadictvalue["C_PYMNT"])
        if datadictvalue["C_REVIEW_PRPSD_PYMNTS_AFTER_CRTN"] == 'Yes':
            page.wait_for_timeout(2000)
            if not page.get_by_text("Review proposed payments").is_checked():
                page.get_by_text("Review proposed payments").click()

            elif datadictvalue["C_REVIEW_PRPSD_PYMNTS_AFTER_CRTN"] == 'No':
                if page.get_by_text("Review proposed payments").is_checked():
                    page.get_by_text("Review proposed payments").click()

        page.get_by_label("Format", exact=True).click()
        page.get_by_label("Format", exact=True).select_option(datadictvalue["C_PYMNT_PRCSS_RQST_STTS_RPRT"])
        page.wait_for_timeout(5000)
        if datadictvalue["C_ATMTCLLY_SBMT_AT_PYMNT_PRCSS_RQST_CMPLTN"] == 'Yes':
            page.wait_for_timeout(2000)
            if not page.get_by_text("Automatically submit at").is_checked():
                    page.get_by_text("Automatically submit at").click()

            elif datadictvalue["C_ATMTCLLY_SBMT_AT_PYMNT_PRCSS_RQST_CMPLTN"] == 'No':
                if page.get_by_text("Automatically submit at").is_checked():
                    page.get_by_text("Automatically submit at").click()

        if datadictvalue["C_SAVE_FRMTTD_PYMNT_FILE_IN_DTBS"] == 'Yes':
            page.wait_for_timeout(2000)
            if not page.get_by_text("Save formatted payment file").is_checked():
                    page.get_by_text("Save formatted payment file").click()

            elif datadictvalue["C_SAVE_FRMTTD_PYMNT_FILE_IN_DTBS"] == 'No':
                if page.get_by_text("Save formatted payment file").is_checked():
                    page.get_by_text("Save formatted payment file").click()

            page.get_by_role("button", name="Add Row").click()
            page.wait_for_timeout(2000)
            page.get_by_title("Business Unit", exact=True).click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//label[text()='Business Unit ID']//following::input[2]").fill(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BSNSS_UNIT"]).click()
            page.get_by_role("button", name="OK").click()

            page.get_by_label("Payment Method Default Basis").select_option(datadictvalue["C_PYMNT_MTHD_DFLT_BASIS"])
            page.get_by_label("Allow Payee Bank Account Override on Proposed Payments", exact=True).select_option(datadictvalue["C_BSNSS_UNIT_ALLOW_PAYEE_BANK_ACCNT_OVRRD_ON_PRPSD_PYMNTS"])
            page.get_by_label("From Email", exact=True).fill(datadictvalue["C_FROM_EMAIL"])
            page.get_by_label("Subject", exact=True).fill(datadictvalue["C_SBJCT"])
            if datadictvalue["C_BANK_CHRG_BRR"] != '':
                page.get_by_label("Bank Charge Bearer").select_option(datadictvalue["C_BANK_CHRG_BRR"])

            if datadictvalue["C_PAY_EACH_DCMNT_ALONE"] == 'Yes':
                if not page.get_by_text("Pay each document alone").is_checked():
                    page.get_by_text("Pay each document alone").click()

            elif datadictvalue["C_PAY_EACH_DCMNT_ALONE"] == 'No':
                if  page.get_by_text("Pay each document alone").is_checked():
                    page.get_by_text("Pay each document alone").click()

            page.get_by_role("button", name="Save and Close").click()

        try:
            expect(page.get_by_role("button", name="OK")).to_be_visible()
            page.get_by_role("button", name="OK").click()
            print("Row Saved Successfully")
            datadictvalue["RowStatus"] = "Saved Successfully"
        except Exception as e:
            print("Row Saved UnSuccessfully")
            datadictvalue["RowStatus"] = "UnSuccessfull"


        i = i + 1


    try:
        expect(page.get_by_role("heading", name="Search")).to_be_visible()

        print("Disbursement System Options Saved Successfully")
        datadictvalue["RowStatus"] = "Disbursement System Options Saved Successfully"
    except Exception as e:
        print("Disbursement System Options Saved UnSuccessfully")
        datadictvalue["RowStatus"] = "Disbursement System Options Saved UnSuccessfully"
    page.wait_for_timeout(2000)

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, DISBURSEMENT_SYSTEM_OPTIONS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, DISBURSEMENT_SYSTEM_OPTIONS, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, DISBURSEMENT_SYSTEM_OPTIONS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + DISBURSEMENT_SYSTEM_OPTIONS)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
                0] + "_" +DISBURSEMENT_SYSTEM_OPTIONS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))