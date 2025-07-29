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
    page.get_by_role("link", name="Manage Chart of Accounts Structures").click()
    page.wait_for_timeout(2000)
    page.get_by_label("Module").click()
    page.get_by_label("Module").type("General ledger")
    page.get_by_label("Module").press("Enter")
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Manage Structure Instances").click()

    i = 0
    datadictvalue = datadict[i]
    page.get_by_role("button", name="Create").click()
    page.wait_for_timeout(2000)
    page.get_by_label("Structure Instance Code").click()
    page.get_by_label("Structure Instance Code").type(datadictvalue["C_COA_STRCTR_NAME"])
    page.get_by_label("Structure Instance Code").press("Tab")
    page.get_by_label("API name").click()
    page.get_by_label("API name").press("Tab")
    page.get_by_label("Name", exact=True).click()
    page.get_by_label("Name", exact=True).type(datadictvalue["C_COA_STRCTR_NAME"])
    page.get_by_label("Name", exact=True).press("Tab")

    if not page.get_by_text("Enabled", exact=True).is_checked():
        page.get_by_text("Enabled", exact=True).click()
    if not page.get_by_text("Dynamic combination creation allowed").is_checked():
        page.get_by_text("Dynamic combination creation allowed").click()
    if not page.get_by_text("Shorthand alias enabled").is_checked():
        page.get_by_text("Shorthand alias enabled").click()

    page.get_by_label("Structure Name").click()
    page.get_by_label("Structure Name").select_option(datadictvalue["C_COA_STRCTR_NAME"])
    page.wait_for_timeout(3000)

    j = 0
    while j < rowcount:
        datadictvalue = datadict[j]
        page.get_by_role("cell", name=datadictvalue["C_SGMNT"], exact=True).first.click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Edit", exact=True).click()
        page.wait_for_timeout(2000)
        if not page.locator("[id=\"__af_Z_window\"]").get_by_text("Required", exact=True).is_checked():
            page.locator("[id=\"__af_Z_window\"]").get_by_text("Required", exact=True).click()
        if not page.locator("[id=\"__af_Z_window\"]").get_by_text("Displayed").is_checked():
            page.locator("[id=\"__af_Z_window\"]").get_by_text("Displayed").click()
        if not page.get_by_text("BI enabled").is_checked():
            page.get_by_text("BI enabled").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Query Required").click()
        page.get_by_label("Query Required").select_option("Optional")
        page.get_by_label("Query Required").press("Tab")
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="OK").click()
        print("Row Added - ", str(j))
        j = j + 1

    datadictvalue["RowStatus"] = "Successfully Created COA Add Structure"
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(5000)

    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, CHART_OF_ACCOUNT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, CHART_OF_ACCOUNT, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, CHART_OF_ACCOUNT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + CHART_OF_ACCOUNT)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + CHART_OF_ACCOUNT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))