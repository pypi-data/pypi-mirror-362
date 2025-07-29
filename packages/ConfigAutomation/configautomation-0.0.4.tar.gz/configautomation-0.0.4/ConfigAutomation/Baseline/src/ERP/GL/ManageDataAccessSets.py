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
    page.get_by_role("textbox").fill("Manage Data Access Sets")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Data Access Sets", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Access Set Type").select_option(datadictvalue["C_ACCSS_SET_TYPE"])
        page.get_by_label("Chart of Accounts").select_option(datadictvalue["C_CHART_OF_ACCNTS"])
        page.get_by_label("Accounting Calendar").select_option(datadictvalue["C_ACCNTNG_CLNDR"])
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Add Row").click()
        page.get_by_label("Ledger or Ledger Set").click()
        page.get_by_title("Search: Ledger or Ledger Set").click()
        page.get_by_text(datadictvalue["C_LDGR_OR_LDGR_SET"]).click()
        page.wait_for_timeout(3000)
        page.get_by_label("Privilege").click()
        page.get_by_label("Privilege").select_option(datadictvalue["C_PRVLG"])

        page.get_by_role("button", name="Save and Close").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Data Access Sets created successfully")

        except Exception as e:
            print("Unable to save the data access sets")

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Successfully Added data access sets"

    OraSignOut(page, context, browser, videodir)
    return datadict




#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, DATA_ACCESS_SET):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, DATA_ACCESS_SET, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, DATA_ACCESS_SET)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + DATA_ACCESS_SET)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
                0] + "_" + DATA_ACCESS_SET + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))