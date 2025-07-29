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
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Manage Payment Methods")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Payment Methods", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Code").fill(datadictvalue["C_CODE"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Alias").fill(datadictvalue["C_ALIAS"])
        page.get_by_label("Anticipated Float Value").fill(datadictvalue["C_ANTCPTD_DSBRSMNT_FLOAT"])
        page.locator("//label[text()='From Date']//following::input[1]").fill("")
        page.locator("//label[text()='From Date']//following::input[1]").fill(str(datadictvalue["C_FROM_DATE"]))
        if datadictvalue["C_TO_DATE"] != '':
            page.locator("//label[text()='To Date']//following::input[1]").fill(datadictvalue["C_TO_DATE"].strftime("%m/%d/%Y"))

        #Usage Rules

        page.get_by_role("link", name="Usage Rules").click()

        if datadictvalue["C_ATMTCLLY_ASSGN_PYMNT_MTHD_TO_ALL_PYS"] =='Yes':
            page.get_by_text("Automatically assign payment").check()
        if datadictvalue["C_ATMTCLLY_ASSGN_PYMNT_MTHD_TO_ALL_PYS"] =='No':
            page.get_by_text("Automatically assign payment").uncheck()

        #Payables

        page.get_by_role("link", name="Payables").click()

        if datadictvalue["C_ENBL_FOR_USE_IN_PYBLS"] == 'Yes':
            page.get_by_text("Enable for use in Payables").check()
        if datadictvalue["C_ENBL_FOR_USE_IN_PYBLS"] == 'No':
            page.get_by_text("Enable for use in Payables").uncheck()
        page.wait_for_timeout(2000)
        page.locator("//label[text()='Business Units']//following::label[text()='"+datadictvalue["C_BSNSS_UNITS"]+"'][1]").click()
        if datadictvalue["C_BSNSS_UNITS"] == 'Specific':
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Add Row").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Business Unit").type(datadictvalue["C_SPCFC_BSNSS_UNIT"], delay=20)
            page.get_by_role("option", name=datadictvalue["C_SPCFC_BSNSS_UNIT"]).click()
        page.wait_for_timeout(2000)

        page.locator("//label[text()='First Party Legal Entities']//following::label[text()='" +datadictvalue["C_FIRST_PRTY_LEGAL_ENTTS"]+"'][1]").click()
        if datadictvalue["C_FIRST_PRTY_LEGAL_ENTTS"] == 'Specific':
            page.get_by_role("button", name="New").click()
            page.wait_for_timeout(1000)
            page.get_by_label("First Party Legal Entity").type(datadictvalue["C_SPCFC_LEGAL_ENTTY"], delay=20)
            page.get_by_role("option", name=datadictvalue["C_SPCFC_LEGAL_ENTTY"]).click()
        page.wait_for_timeout(2000)

        page.locator("//label[text()='Payment Process Transaction Types']//following::label[text()='" +datadictvalue["C_PYMNT_PRCSS_TRNSCTN_TYPES"]+"'][1]").click()
        if datadictvalue["C_PYMNT_PRCSS_TRNSCTN_TYPES"] == 'Specific':
            page.get_by_role("button", name="New").nth(1).click()
            page.wait_for_timeout(1000)
            page.get_by_label("Type").select_option(datadictvalue["C_TYPE"])
        page.wait_for_timeout(2000)

        page.get_by_label("Currency").select_option(datadictvalue["C_CRRNCY"])
        page.get_by_label("Payee Location").select_option(datadictvalue["C_PAYEE_LCTN"])

        #Receivables
        page.wait_for_timeout(1000)
        page.get_by_role("link", name="Receivables for Customer").click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_ENBL_FOR_USE_IN_RCVBLS"] == 'Yes':
            page.get_by_text("Enable for use in Receivables").check()
        if datadictvalue["C_ENBL_FOR_USE_IN_RCVBLS"] == 'No':
            page.get_by_text("Enable for use in Receivables").uncheck()
        page.locator("//label[text()='Business Units']//following::label[text()='" + datadictvalue[
            "C_RCVBLS_BSNSS_UNITS"] + "'][1]").click()
        if datadictvalue["C_RCVBLS_BSNSS_UNITS"] == 'Specific':
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="New").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Business Unit").type(datadictvalue["C_RCVBLS_SPCFC_BSNSS_UNIT"], delay=20)
            page.get_by_role("option", name=datadictvalue["C_RCVBLS_SPCFC_BSNSS_UNIT"]).click()
        page.wait_for_timeout(2000)
        page.locator("//label[text()='First Party Legal Entities']//following::label[text()='" + datadictvalue[
            "C_RCVBLS_FIRST_PARTY_LEGAL_ENTTS"] + "'][1]").click()
        if datadictvalue["C_RCVBLS_FIRST_PARTY_LEGAL_ENTTS"] == 'Specific':
            page.get_by_role("button", name="New").nth(1).click()
            page.wait_for_timeout(1000)
            page.get_by_label("First Party Legal Entity").type(datadictvalue["C_RCVBLS_SPCFC_LEGAL_ENTTY"], delay=20)
            page.get_by_role("option", name=datadictvalue["C_RCVBLS_SPCFC_LEGAL_ENTTY"]).click()
        page.wait_for_timeout(2000)
        page.locator("//label[text()='Payment Process Transaction Types']//following::label[text()='" + datadictvalue[
            "C_RCVBLS_PYMNT_PRCSS_TRNSCTN_TYPES"] + "'][1]").click()
        if datadictvalue["C_RCVBLS_PYMNT_PRCSS_TRNSCTN_TYPES"] == 'Specific':
            page.get_by_role("button", name="New").nth(2).click()
            page.wait_for_timeout(1000)
            page.get_by_label("Type").select_option(datadictvalue["C_RCVBLS_TYPE"])
        page.wait_for_timeout(2000)
        page.get_by_label("Currency").select_option(datadictvalue["C_RCVBLS_CRRNCY"])
        page.get_by_label("Payee Location").select_option(datadictvalue["C_RCVBLS_PAYEE_LCTN"])

        #Cash Management
        page.wait_for_timeout(1000)
        page.get_by_role("link", name="Cash Management").click()
        if datadictvalue["C_ENBL_FOR_USE_IN_CASH_MNGMNT"] =='Yes':
            page.get_by_text("Enable for use in Cash").check()
        if datadictvalue["C_ENBL_FOR_USE_IN_CASH_MNGMNT"] =='No':
            page.get_by_text("Enable for use in Cash").uncheck()
        page.locator("//label[text()='Payment Process Transaction Types']//following::label[text()='" + datadictvalue[
            "C_CM_PYMNT_PRCSS_TRNSCTN_TYPES"] + "'][1]").click()
        if datadictvalue["C_CM_PYMNT_PRCSS_TRNSCTN_TYPES"] == 'Specific':
            page.get_by_role("button", name="New").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Type").select_option(datadictvalue["C_CM_TYPE"])
        page.wait_for_timeout(2000)

        #Validations
        page.get_by_role("link", name="Validations").click()
        page.wait_for_timeout(2000)

        #Predefined Validation
        if datadictvalue["C_VLDTN"] != '':
            page.get_by_role("button", name="Add Row").first.click()
            page.wait_for_timeout(2000)
            page.get_by_label("Validation").select_option(datadictvalue["C_VLDTN"])
            page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar Validation Start Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(str(datadictvalue["C_VLDTN_START_DATE"]))
            if datadictvalue["C_VLDTN_TO_DATE"] != '':
                page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_VLDTN_TO_DATE"].strftime("%m/%d/%Y"))
            if datadictvalue["C_PRE_NAME"] != '':
                page.locator("//span[text()='"+datadictvalue["C_PRE_NAME"]+"']//following::input[2]").fill(datadictvalue["C_PRE_VALUE"])

        #User defined validation
        if datadictvalue["C_FIELD"] != "":
            page.get_by_role("button", name="Add Row").nth(1).click()
            page.wait_for_timeout(3000)
            page.get_by_label("Field").click()
            page.get_by_label("Field").select_option(datadictvalue["C_FIELD"])

            page.wait_for_timeout(4000)

            if page.get_by_label("Condition").is_enabled():
                page.get_by_label("Condition").click()
                page.get_by_label("Condition").select_option(datadictvalue["C_CNDTN"])
            page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date",
                             exact=True).get_by_placeholder("m/d/yy").fill(str(datadictvalue["C_USER_FROM_DATE"]))
            if datadictvalue["C_USER_TO_DATE"] != '':
                page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date").nth(3).locator("input").first.fill(datadictvalue["C_USER_TO_DATE"].strftime("%m/%d/%Y"))
            if datadictvalue["C_USER_VALUE"] != '':
                page.locator("//span[text()='"+datadictvalue["C_USER_NAME"]+"']//following::input[1]").fill(datadictvalue["C_USER_VALUE"])
            page.wait_for_timeout(2000)

        # Bills Payable
        page.get_by_role("link", name="Bills Payable").click()
        page.wait_for_timeout(1000)
        if datadictvalue["C_USE_PYMNT_MTHD_TO_ISSUE_BILLS_PYBL"] == 'Yes':
            page.get_by_role("cell", name="Bills Payable", exact=True).locator("label").check()
        if datadictvalue["C_USE_PYMNT_MTHD_TO_ISSUE_BILLS_PYBL"] == 'No' or '':
            page.get_by_role("cell", name="Bills Payable", exact=True).locator("label").uncheck()
        page.get_by_label("Maturity Date Override").fill(datadictvalue["C_MTRTY_DATE_OVRRD"])

        # Save the data
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)
        if page.get_by_role("button", name="Yes").is_visible():
            page.get_by_role("button", name="Yes").click()
        if page.get_by_role("button", name="OK").is_visible():
            page.get_by_role("button", name="OK").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Payment Methods Saved Successfully")
            datadictvalue["RowStatus"] = "Payment Methods are added successfully"

        except Exception as e:
            print("Payment Methods not saved")
            datadictvalue["RowStatus"] = "Payment Methods are not added"


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYMENT_METHODS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYMENT_METHODS, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, PAYMENT_METHODS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + PAYMENT_METHODS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
            0] + "_" + PAYMENT_METHODS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
