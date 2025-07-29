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
    page.get_by_role("textbox").fill("Manage Expense Report Audit Rules By Expense Templates And Types")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Expense Report Audit Rules By Expense Templates And Types").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Business Unit").select_option(datadictvalue["C_BSNSS_UNIT"])

        page.get_by_role("button", name="Add Row").click()
        page.get_by_label("Expense Template", exact=True).click()
        page.get_by_label("Expense Template", exact=True).select_option(datadictvalue["C_EXPNS_TMPLT"])
        page.wait_for_timeout(2000)
        page.get_by_label("Type", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_label("Type", exact=True).select_option(datadictvalue["C_TYPE"])
        page.wait_for_timeout(2000)
        page.get_by_label("Currency").select_option(datadictvalue["C_CRRNCY"])
        page.get_by_label("Amount", exact=True).fill(str(datadictvalue["C_AMNT"]))
        page.get_by_label("Cumulative Amount").fill(datadictvalue["C_CMLTV_AMNT"])

        page.get_by_role("button", name="Save and Close").click()

        #Validation

        try:
            expect(page.get_by_text("Confirmation")).to_be_visible()
            page.get_by_role("button", name="OK").click()
            # page.locator("//div[text()='Confirmation']//following::button[1]").click()
            print("Expense Report Audit Rules Saved Successfully")
            # datadictvalue["RowStatus"] = "Configuration Saved Successfully"
        except Exception as e:
            print("Expense Report Audit Rules not Saved")
            # datadictvalue["RowStatus"] = "Expense Profile Value not Saved"

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, AUDIT_RULES_BY_EXP_TYPE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, AUDIT_RULES_BY_EXP_TYPE, PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, AUDIT_RULES_BY_EXP_TYPE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[0] + "_" + AUDIT_RULES_BY_EXP_TYPE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + AUDIT_RULES_BY_EXP_TYPE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))