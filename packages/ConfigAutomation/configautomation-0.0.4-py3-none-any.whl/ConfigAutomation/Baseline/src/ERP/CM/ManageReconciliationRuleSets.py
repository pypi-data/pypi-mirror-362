from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Bank Statement Reconciliation Rule Set")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Bank Statement Reconciliation Rule Sets", exact=True).click()
    page.wait_for_timeout(3000)

    PrevName = ''

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        if datadictvalue["C_NAME"] != PrevName:

            # Header Input
            page.get_by_role("button", name="Create").click()

            # Name
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.wait_for_timeout(2000)

            # Description
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(2000)
            PrevName = datadictvalue["C_NAME"]

        # Reconciliation Rules
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(1000)

        # Matching Rule
        page.get_by_title("Search: Matching Rule").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Matching Rule").fill(datadictvalue["C_MTCHNG_RULE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("cell", name=datadictvalue["C_MTCHNG_RULE"], exact=True).locator("span").click()
        page.get_by_role("button", name="OK").nth(1).click()

        # Tolerance Rule
        page.get_by_label("Tolerance Rule").click()
        page.get_by_label("Tolerance Rule").fill(datadictvalue["C_TLRNC_RULE"])
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1
    page.pause()
    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(2000)

    try:
        expect(page.get_by_role("heading", name="Manage Bank Statement Reconciliation Rule Sets")).to_be_visible()
        print("Reconciliation Rule Sets Saved Successfully")
        # datadictvalue["RowStatus"] = "Saved Successfully"
    except Exception as e:
        print("Reconciliation Rule Sets Saved UnSuccessfully")
        # datadictvalue["RowStatus"] = "UnSuccessfully"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, REC_RULE_SETS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, REC_RULE_SETS, PRCS_DIR_PATH + CM_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + CM_WORKBOOK, REC_RULE_SETS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0] + "_" + REC_RULE_SETS)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0] + "_" + REC_RULE_SETS +
                         "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
