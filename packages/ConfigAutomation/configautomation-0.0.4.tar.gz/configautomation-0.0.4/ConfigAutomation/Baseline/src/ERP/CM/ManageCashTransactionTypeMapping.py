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
    page.wait_for_timeout(5000)

    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Cash Transaction Type Mapping")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Cash Transaction Type Mapping", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Create
        page.get_by_role("button", name="Create").first.click()
        page.wait_for_timeout(2000)

        # Type
        page.get_by_label("Type", exact=True).select_option(datadictvalue["C_TYPE"])
        page.wait_for_timeout(2000)

        # Transaction Type
        page.get_by_label("Transaction Type").select_option(datadictvalue["C_TRNSCTN_TYPE"])
        page.wait_for_timeout(2000)

        # Method
        page.get_by_label("Method").click()
        page.get_by_label("Method").type(datadictvalue["C_MTHD"])

        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()

        # Payroll Payment Type Mapping
        if datadictvalue["C_PYRLL_TRNSCTN_TYPE"] != '':
            page.get_by_role("button", name="Create").nth(1).click()
            page.wait_for_timeout(3000)
            # Transaction Type
            page.locator("(//label[text()='Transaction Type']//following::select[1])[2]").select_option(datadictvalue["C_PYRLL_TRNSCTN_TYPE"])
            page.wait_for_timeout(2000)
            page.get_by_label("Payment Type").click()
            page.get_by_title("Search: Payment Type").click()
            page.get_by_role("combobox", name="Payment Type").fill(datadictvalue["C_PYMNT_TYPE"])
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Save and Close").click()

        # Validation :- Checking for the Method in the UI
        try:
            expect(page.get_by_role("cell", name=datadictvalue["C_MTHD"], exact=True)).to_be_visible()
            print("Transaction Type Mapping Saved Successfully")
            datadictvalue["RowStatus"] = "Transaction Type Mapping Saved Successfully"
        except Exception as e:
            print("Transaction Type Mapping Saved UnSuccessfully")
            datadictvalue["RowStatus"] = "Transaction Type Mapping Saved UnSuccessfully"

        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Done").click()

        i = i + 1

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, CASH_TRANS_TYPE_MAPPING):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, CASH_TRANS_TYPE_MAPPING, PRCS_DIR_PATH + CM_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + CM_WORKBOOK, CASH_TRANS_TYPE_MAPPING)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0] + "_" + CASH_TRANS_TYPE_MAPPING)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[
                0] + "_" + CASH_TRANS_TYPE_MAPPING + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
