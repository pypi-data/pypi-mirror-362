from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Offering").click()
    page.get_by_text("Financials", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_text("Organization Structures").click()
    page.get_by_role("textbox").fill("Assign Business Unit Business Function")
    page.get_by_role("textbox").press("Enter")
    page.locator("//a[text()='Assign Business Unit Business Function']//following::a[1]").click()


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_label("Business Unit", exact=True).select_option("Select and Add")
        page.get_by_role("button", name="Apply and Go to Task").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Name").fill(datadictvalue["C_BSNSS_UNIT_NAME"])
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("table", name='Business Units').get_by_role("cell", name=datadictvalue["C_BSNSS_UNIT_NAME"], exact=True).click()
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)
        # page.get_by_label("Name").fill(datadictvalue["C_BSNSS_UNIT_NAME"])
        # page.get_by_role("button", name="Search", exact=True).click()
        # page.get_by_role("cell", name=datadictvalue["C_BSNSS_UNIT_NAME"], exact=True).click()
        # page.get_by_label("Actions").locator("div").click()
        # page.get_by_role("cell", name="Assign Business Functions", exact=True).click()

        #Business Unit Functions
        if datadictvalue["C_RQSTNNG"] == 'Yes':
            page.get_by_role("row", name="Requisitioning").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_PYBLS_INVCNG"] == 'Yes':
            page.get_by_role("row", name="Payables Invoicing").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_PRCRMNT"] == 'Yes':
            page.get_by_role("row", name="Procurement", exact=True).locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_BLLNG_AND_RVN_MNGMNT"] == 'Yes':
            page.get_by_role("row", name="Billing and Revenue Management").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_CLLCTN_MNGMNT"] == 'Yes':
            page.get_by_role("row", name="Collections Management").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_CSTMR_PYMNTS"] == 'Yes':
            page.get_by_role("row", name="Customer Payments").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_EXPNS_MNGMNT"] == 'Yes':
            page.get_by_role("row", name="Expense Management").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_MTRLS_MNGMNT"] == 'Yes':
            page.get_by_role("row", name="Materials Management").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_PYBLS_PYMNT"] == 'Yes':
            page.get_by_role("row", name="Payables Payment").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_PRCRMNT_CNTRCT_MNGMNT"] == 'Yes':
            page.get_by_role("row", name="Procurement Contract Management").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_RCVNG"] == 'Yes':
            page.get_by_role("row", name="Receiving").locator("label").check()
            page.wait_for_timeout(2000)

        if datadictvalue["C_SALES"] == 'Yes':
            page.get_by_role("row", name="Sales").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_PRJCT_ACCNTNG"] == 'Yes':
            page.get_by_role("row", name="Project Accounting").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_CSTMR_CNTRCT_MNGMNT"] == 'Yes':
            page.get_by_role("row", name="Customer Contract Management").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_INCNTV_CMPNSTN"] == 'Yes':
            page.get_by_role("row", name="Incentive Compensation").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_RVN_CMPLNC_AND_ACCNTNG"] == 'Yes':
            page.get_by_role("row", name="Revenue Compliance and").locator("label").check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_SRVC_RQST_MNGMNT"] == 'Yes':
            page.get_by_role("row", name="Service Request Management").locator("label").check()
            page.wait_for_timeout(2000)

        # Financial Reporting

        page.get_by_title("Search: Primary Ledger").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Ledger", exact=True).fill(datadictvalue["C_PRMRY_LDGR"])
        page.get_by_label("Ledger", exact=True).click()
        page.get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("cell", name=datadictvalue["C_PRMRY_LDGR"], exact=True).locator("span").first.click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        if page.get_by_text("Below legal entity").first.is_visible():
            if datadictvalue["C_BELOW_LEGAL_ENTTY"] == 'Yes':
                page.get_by_text("Below legal entity").nth(1).check()

                if page.get_by_role("button", name="OK").is_visible():
                    page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.locator("//input[contains(@id,'legalEntityNameId')]").clear()
        page.locator("//input[contains(@id,'legalEntityNameId')]").fill(datadictvalue["C_LEGAL_ENTTY"])

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        if page.get_by_role("button", name="OK").is_visible():
            page.get_by_role("button", name="OK").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Actions", exact=True)).to_be_visible()
            print("Assign Business Unit Business Functions Saved Successfully")
            datadictvalue["RowStatus"] = "Assign Business Unit Business Functions Saved Successfully"

        except Exception as e:
            print("Assign Business Unit Business Functions not saved")
            datadictvalue["RowStatus"] = "Assign Business Unit Business Functions not saved"
    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, BU):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, BU, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, BU)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + BU)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
            0] + "_" + BU + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))