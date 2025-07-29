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
    page.get_by_role("textbox").fill("Manage Standard Memo Lines")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Standard Memo Lines", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)
        page.get_by_label("Memo Line Set").type(datadictvalue["C_MEMO_LINE_SET"])
        page.get_by_role("option", name=datadictvalue["C_MEMO_LINE_SET"]).click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Type").select_option(datadictvalue["C_TYPE"])
        page.wait_for_timeout(2000)
        if datadictvalue["C_TAX_CLSSFCTN"] != '':
            page.get_by_label("Tax Classification").type(datadictvalue["C_TAX_CLSSFCTN"])
            page.get_by_role("option", name=datadictvalue["C_TAX_CLSSFCTN"]).click()
        if datadictvalue["C_TAX_PRDCT_CTGRY"] != '':
            page.get_by_label("Tax Product Category").type(datadictvalue["C_TAX_PRDCT_CTGRY"])
            page.get_by_role("option", name=datadictvalue["C_TAX_PRDCT_CTGRY"]).click()
        page.get_by_label("Unit List Price").fill(datadictvalue["C_UNIT_LIST_PRICE"])
        if page.get_by_label("Unit of Measure").is_enabled():
            if datadictvalue["C_UNIT_OF_MSR"] != '':
                page.get_by_label("Unit of Measure").type(datadictvalue["C_UNIT_OF_MSR"])
                page.get_by_role("option", name=datadictvalue["C_UNIT_OF_MSR"]).click()
        page.get_by_label("Invoicing Rule").select_option(datadictvalue["C_INVCNG_RULE"])
        if datadictvalue["C_RVN_SCHDLNG_RULE"] != '':
            page.get_by_label("Rule", exact=True).type(datadictvalue["C_RVN_SCHDLNG_RULE"])
            page.get_by_role("option", name=datadictvalue["C_RVN_SCHDLNG_RULE"]).click()
        page.locator("//label[text()='From Date']//following::input[1]").clear()
        page.locator("//label[text()='From Date']//following::input[1]").fill(datadictvalue["C_FROM_DATE"].strftime("%m/%d/%Y"))
        if datadictvalue["C_TO_DATE"] != '':
            page.locator("//label[text()='To Date']//following::input[1]").fill(datadictvalue["C_TO_DATE"])
        if datadictvalue["C_BSNSS_UNIT"] != '':
            page.get_by_role("link", name="Create").click()
            page.wait_for_timeout(2000)
            page.get_by_title("Search: Business Unit").click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//div[text()='Search and Select: Business Unit']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_text(datadictvalue["C_BSNSS_UNIT"]).nth(2).click()
            page.get_by_role("button", name="OK").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_label("Revenue").click()
            page.get_by_label("Revenue").fill(datadictvalue["C_RVN"])
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        # Save the data

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        # if page.locator("//div[text()='Warning']//following::button[1]").is_visible():
        #     page.locator("//div[text()='Warning']//following::button[1]").click()
        # if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
        #     page.locator("//div[text()='Confirmation']//following::button[1]").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Standard Memo Lines saved Successfully")
            datadictvalue["RowStatus"] = "Standard Memo Lines added successfully"

        except Exception as e:
            print("Standard Memo Lines not saved")
            datadictvalue["RowStatus"] = "Standard Memo Lines not added"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, STAN_MEMO_LINES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, STAN_MEMO_LINES, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, STAN_MEMO_LINES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + STAN_MEMO_LINES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + STAN_MEMO_LINES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

