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
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.get_by_label("", exact=True).fill("manage primary ledger")
    page.get_by_role("button", name="Search").click()
    page.get_by_role("link", name="Manage Primary Ledgers").click()


    i = 0
    while i < rowcount:

        page.wait_for_timeout(3000)
        datadictvalue = datadict[i]
        page.get_by_role("button", name="Create").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Chart of Accounts").click()
        page.get_by_label("Chart of Accounts").select_option(datadictvalue["C_COA_CHART_OF_ACCNTS"])
        page.get_by_label("Accounting Calendar").select_option(datadictvalue["C_ACCNTNG_CLNDR"])
        page.get_by_label("Currency").select_option(datadictvalue["C_CRRNCY"])
        page.get_by_label("Accounting Method").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Accounting Method").select_option(datadictvalue["C_ACCNTNG_MTHD"])
        page.wait_for_timeout(5000)
        page.get_by_label("Accounting Method").press("Tab")
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        i = i + 1


        try:
            expect(page.get_by_text("Search Tasks")).to_be_visible()
            print("PrimaryLedger Saved Successfully")
            datadictvalue["RowStatus"] = "PrimaryLedger Saved Successfully"
        except Exception as e:
            print("PrimaryLedger Saved UnSuccessfully")
            datadictvalue["RowStatus"] = "PrimaryLedger Saved UnSuccessfully"


    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, LEDGER):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, LEDGER, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, LEDGER)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + LEGAL_ENTITY_SHEET)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
                0] + "_" + LEGAL_ENTITY_SHEET + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))