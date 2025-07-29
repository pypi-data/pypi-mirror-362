from playwright.sync_api import Playwright, sync_playwright
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
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="Offering").click()
    page.get_by_text("Financials", exact=True).click()
    page.get_by_text("Financial Reporting Structures").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Chart of Accounts Value Sets").click()
    print(rowcount)
    page.wait_for_timeout(2000)

    i = 0
    datadictvalue = datadict[i]
    page.get_by_label("Value Set Code").click()
    page.get_by_label("Value Set Code").type(datadictvalue["C_SGMNT"])
    page.get_by_label("Module").click()
    page.get_by_label("Module").type("General ledger")
    page.get_by_label("Module").press("Tab")
    page.get_by_role("button", name="Search", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("cell", name=datadictvalue["C_SGMNT"]).first.click()
    page.get_by_role("button", name="Manage Values").click()
    page.wait_for_timeout(2000)

    j = 0
    while j < rowcount:
        datadictvalue = datadict[j]



        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Value").nth(1).click()
        page.get_by_label("Value").nth(1).type(str(datadictvalue["C_VALUE"]))
        page.get_by_label("Description").nth(1).click()
        page.get_by_label("Description").nth(1).type(datadictvalue["C_DSCRPTN"])
        
        if datadictvalue["C_ENBLD"] == "Yes":
            if not page.locator("//span[text()='Enabled']//following::label[contains(@id,'Label0')]").first.is_checked():
                page.locator("//span[text()='Enabled']//following::label[contains(@id,'Label0')]").first.click()

        page.get_by_label("Summary").first.click()
        page.get_by_label("Summary").first.select_option(datadictvalue["C_SMMRY"])
        page.get_by_label("Allow Posting").first.click()
        page.get_by_label("Allow Posting").first.select_option(datadictvalue["C_ALLOW_PSTNG"])
        page.get_by_label("Allow Budgeting").first.click()
        page.get_by_label("Allow Budgeting").first.select_option(datadictvalue["C_ALLOW_BDGTNG"])
        page.get_by_label("Allow Budgeting").first.press("Tab")
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(3000)
        print("Row Added - ", str(j))
        j = j + 1
        datadictvalue["RowStatus"] = "Successfully Loaded values for Cost Center Value set"

    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(5000)

    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(5000)

    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, COST_CENTER):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, COST_CENTER, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, COST_CENTER)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + COST_CENTER)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + COST_CENTER + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))