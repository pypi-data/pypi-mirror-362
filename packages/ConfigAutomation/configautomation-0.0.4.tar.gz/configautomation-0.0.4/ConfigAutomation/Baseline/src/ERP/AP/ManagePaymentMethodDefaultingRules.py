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
    page.get_by_role("textbox").fill("Manage Payment Method Defaulting Rules")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Payment Method Defaulting Rules", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Create").first.click()
        page.wait_for_timeout(2000)
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Payment Method").type(datadictvalue["C_PYMNT_MTHD"], delay=100)
        page.get_by_role("option", name=datadictvalue["C_PYMNT_MTHD"]).click()
        page.wait_for_timeout(2000)

        #Defaulting Conditions

        page.locator("//label[text()='Business Units']//following::label[text()='" + datadictvalue[
            "C_BSNSS_UNITS"] + "'][1]").click()
        if datadictvalue["C_BSNSS_UNITS"] == 'Specific':
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Add Row").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Business Unit").type(datadictvalue["C_SPCFC_BSNSS_UNIT"], delay=100)
            page.get_by_role("option", name=datadictvalue["C_SPCFC_BSNSS_UNIT"]).click()
        page.wait_for_timeout(2000)
        page.locator("//label[text()='First Party Legal Entities']//following::label[text()='" + datadictvalue[
            "C_FIRST_PARTY_LEGAL_ENTTS"] + "'][1]").click()
        if datadictvalue["C_FIRST_PARTY_LEGAL_ENTTS"] == 'Specific':
            page.get_by_role("button", name="Add Row").nth(1).click()
            page.wait_for_timeout(1000)
            page.get_by_label("First Party Legal Entity").type(datadictvalue["C_SPCFC_LEGAL_ENTTY"], delay=100)
            page.get_by_role("option", name=datadictvalue["C_SPCFC_LEGAL_ENTTY"]).click()
        page.wait_for_timeout(2000)
        page.locator("//label[text()='Payment Process Transaction Types']//following::label[text()='" + datadictvalue[
            "C_PYMNT_PRCSS_TRNSCTN_TYPES"] + "'][1]").click()
        if datadictvalue["C_PYMNT_PRCSS_TRNSCTN_TYPES"] == 'Specific':
            page.get_by_role("button", name="Add Row").nth(2).click()
            page.wait_for_timeout(1000)
            page.get_by_label("Operator").select_option(datadictvalue["C_OPRTR"])
            page.get_by_label("Type").select_option(datadictvalue["C_TYPE"])
        page.wait_for_timeout(2000)
        page.get_by_label("Currency").select_option(datadictvalue["C_CRRNCY"])
        page.get_by_label("Payee Location").select_option(datadictvalue["C_PAYEE_LCTN"])

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
            print("Manage Payment Method Defaulting Rules Saved Successfully")
            datadictvalue["RowStatus"] = "Manage Payment Method Defaulting Rules are added successfully"

        except Exception as e:
            print("Manage Payment Method Defaulting Rules not saved")
            datadictvalue["RowStatus"] = "Manage Payment Method Defaulting Rules are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYMENT_METHOD_DEFAULTING_RULE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYMENT_METHOD_DEFAULTING_RULE, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, PAYMENT_METHOD_DEFAULTING_RULE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + PAYMENT_METHOD_DEFAULTING_RULE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
            0] + "_" + PAYMENT_METHOD_DEFAULTING_RULE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
