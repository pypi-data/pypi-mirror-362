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
    page.wait_for_timeout(5000)

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Manage Bank Statement Transaction Codes")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Bank Statement Transaction Codes", exact=True).click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        # Create
        if datadictvalue["C_TRNSCTN_CODE"] != '':
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)

        # Transaction Code
        page.get_by_label("Transaction Code").click()
        page.get_by_label("Transaction Code").fill(str(datadictvalue["C_TRNSCTN_CODE"]))
        page.wait_for_timeout(1000)

        # Description
        page.get_by_label("Description").fill(str(datadictvalue["C_DSCRPTN"]))
        page.wait_for_timeout(1000)

        # Transaction Type
        page.get_by_label("Transaction Type").select_option(datadictvalue["C_TRNSCTN_TYPE"])
        page.wait_for_timeout(1000)

        # Domain
        if datadictvalue["C_DMN"] != '':
            page.get_by_label("Domain").select_option(datadictvalue["C_DMN"])
            page.wait_for_timeout(1000)

        # Family
        if datadictvalue["C_FMLY"] != '':
            page.get_by_label("Family", exact=True).select_option(datadictvalue["C_FMLY"])
            page.wait_for_timeout(1000)

        # Subfamily
        if datadictvalue["C_SUB_FMLY"] != '':
            page.get_by_label("Subfamily").select_option(datadictvalue["C_SUB_FMLY"])
            page.wait_for_timeout(1000)

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Bank Statement Transaction Codes Saved Successfully")
            datadictvalue["RowStatus"] = "Bank Statement Transaction Codes are added successfully"

        except Exception as e:
            print("Bank Statement Transaction Codes are not added successfully")
            datadictvalue["RowStatus"] = "Bank Statement Transaction Codes are not added successfully"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, BANK_STMT_TRNSCTN_CODE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, BANK_STMT_TRNSCTN_CODE, PRCS_DIR_PATH + CM_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + CM_WORKBOOK, BANK_STMT_TRNSCTN_CODE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0] + "_" + BANK_STMT_TRNSCTN_CODE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0] + "_" + BANK_STMT_TRNSCTN_CODE +
                     "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
