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
    page.wait_for_timeout(2000)
    page.get_by_text("Financial Reporting Structures").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Chart of Accounts Value Sets").click()
    print(rowcount)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)
        page.get_by_label("Value Set Code").click()
        page.get_by_label("Value Set Code").type(datadictvalue["C_SGMNT"])
        page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Module").type(datadictvalue["C_MDL"])
        page.get_by_label("Module").press("Tab")
        page.get_by_label("Validation Type").select_option(datadictvalue["C_VLDTN_TYPE"])
        page.get_by_label("Value Data Type").click()
        page.get_by_label("Value Data Type").select_option(datadictvalue["C_VALUE_DATA_TYPE"])
        page.get_by_label("Value Subtype").click()
        page.get_by_label("Value Subtype").select_option(datadictvalue["C_VALUE_SBTYP"])
        page.get_by_label("Maximum Length").type(str(datadictvalue["C_DSPLY_WIDTH"]))
        page.get_by_label("Maximum Length").press("Tab")
        page.wait_for_timeout(1000)


        page.get_by_role("button", name="Save and Close").click()
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Successfully Added COA Add Value sets"
        i = i + 1
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

