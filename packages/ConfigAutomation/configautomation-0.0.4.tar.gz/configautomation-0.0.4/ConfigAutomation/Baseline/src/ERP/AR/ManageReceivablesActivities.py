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
    page.get_by_role("textbox").fill("Manage Receivables Activities")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Receivables Activities", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)
        if page.get_by_label("Business Unit").is_enabled():
            page.get_by_label("Business Unit").click()
            page.get_by_label("Business Unit").type(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("option", name=datadictvalue["C_BSNSS_UNIT"]).click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Activity Type").select_option(datadictvalue["C_ACTVTY_TYPE"])
        if datadictvalue["C_ACTV"] == 'Yes':
            page.get_by_text("Active").check()
        if datadictvalue["C_ACTV"] != 'Yes':
            page.get_by_text("Active").uncheck()
        page.wait_for_timeout(3000)
        if page.get_by_label("GL Account Source").is_enabled():
            page.get_by_label("GL Account Source").select_option("Activity GL account")
            page.get_by_label("GL Account Source").click()
            page.wait_for_timeout(2000)
            page.get_by_label("GL Account Source").select_option(datadictvalue["C_GL_ACCNT_SRC"])
            page.wait_for_timeout(5000)
        if page.get_by_label("Tax Rate Code Source").is_visible():
            if page.get_by_label("Tax Rate Code Source").is_enabled():
                page.get_by_label("Tax Rate Code Source").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Tax Rate Code Source").select_option(datadictvalue["C_TAX_RATE_CODE_SRC"])
                page.wait_for_timeout(3000)
        if page.get_by_label("Activity GL Account").is_enabled():
            page.get_by_label("Activity GL Account").fill(datadictvalue["C_ACTVTY_GL_ACCNT"])
        # if page.get_by_label("Tax Rate Code", exact=True).is_visible():
        #     page.get_by_label("Tax Rate Code", exact=True).fill(datadictvalue["C_TAX_RATE_CODE"])
        # if datadictvalue["C_TAX_RATE_CODE_SRC"] == 'Invoice':
        #     if datadictvalue["C_RCVRBL"] == 'Yes':
        #         page.get_by_text("Recoverable").check()
        #     if datadictvalue["C_RCVRBL"] != 'Yes':
        #         page.get_by_text("Recoverable").uncheck()

        # Save the data
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        # if page.locator("//div[text()='Warning']//following::button[1]").is_visible():
        #     page.locator("//div[text()='Warning']//following::button[1]").click()
        # if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
        #     page.locator("//div[text()='Confirmation']//following::button[1]").click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        if i == rowcount:
          page.get_by_role("button", name="Save and Close").click()
          page.wait_for_timeout(2000)

          try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Receivables Activity saved Successfully")
            datadictvalue["RowStatus"] = "Receivables Activity added successfully"

          except Exception as e:
            print("Receivables Activity not saved")
            datadictvalue["RowStatus"] = "Receivables Activity not added"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, RECEIVABLES_ACTIVITY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, RECEIVABLES_ACTIVITY, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, RECEIVABLES_ACTIVITY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + RECEIVABLES_ACTIVITY)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + RECEIVABLES_ACTIVITY + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))