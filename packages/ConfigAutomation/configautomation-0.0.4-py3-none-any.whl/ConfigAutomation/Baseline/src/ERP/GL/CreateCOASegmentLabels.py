from playwright.sync_api import Playwright, sync_playwright
from ConfigAutomation.Baseline.src.ConfigFileNames import *
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
    page.get_by_role("link", name="Actions", exact=True).click()
    page.get_by_text("Manage Segment Labels").click()
    page.wait_for_timeout(2000)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        if datadictvalue["C_CSTM_SGMNT_LABEL"] != "":
            page.get_by_role("button", name="Add Row").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Segment Label Code").click()
            page.get_by_label("Segment Label Code").type(datadictvalue["C_SGMNT_LABEL_CODE"])
            page.get_by_label("Name", exact=True).first.click()
            page.get_by_label("Name", exact=True).first.type(datadictvalue["C_CSTM_SGMNT_LABEL"])
            page.get_by_label("Description").first.click()
            page.get_by_label("Description").first.type(datadictvalue["C_CSTM_SGMNT_LABEL"])
            page.wait_for_timeout(1000)
            page.get_by_label("BI Object Name").first.click()
            page.get_by_label("BI Object Name").first.type(str("Dim" + " " + "-" + " " + "Segment" + str(datadictvalue["C_SQNC_NMBR"])))
            #page.get_by_role("cell", name="Segment Label Code Name").get_by_label("BI Object Name").type("Dim" + " " + "-" + " " + datadictvalue["C_SGMNT_CLMN"])
            page.get_by_role("button", name="Save", exact=True).click()
            page.wait_for_timeout(3000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Successfully Created missed Segment labels"
        i = i + 1
    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Done").click()
    page.wait_for_timeout(4000)

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
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


