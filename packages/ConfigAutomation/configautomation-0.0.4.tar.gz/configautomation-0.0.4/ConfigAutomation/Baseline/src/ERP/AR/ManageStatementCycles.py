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
    page.get_by_role("textbox").fill("Manage Statement Cycles")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Statement Cycles", exact=True).click()

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        if datadictvalue["C_NAME"] != PrevName:
            # Save the prev type data if the row contains a new type
            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Save and Close").click()
                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("Statement Cycle Saved")
                    datadict[i - 1]["RowStatus"] = "Statement Cycle Saved"
                except Exception as e:
                    print("Unable to save Statement Cycle")
                    datadict[i - 1]["RowStatus"] = "Unable to save Statement Cycle"

                page.wait_for_timeout(2000)
            page.get_by_role("button", name="Add Row").first.click()
            page.wait_for_timeout(2000)
            page.get_by_label("Name").nth(1).fill(datadictvalue["C_NAME"])
            page.get_by_label("Interval").nth(1).click()
            page.get_by_label("Interval").nth(1).select_option(datadictvalue["C_INTRVL"])
            if datadictvalue["C_ACTV"] == 'Yes':
                page.get_by_role("table", name="Search Results").locator("label").nth(2).check()
            if datadictvalue["C_ACTV"] != 'Yes':
                page.get_by_role("table", name="Search Results").locator("label").nth(2).uncheck()
            page.get_by_label("Description").nth(1).fill(datadictvalue["C_DSCRPTN"])
            PrevName = datadictvalue["C_NAME"]
            page.wait_for_timeout(2000)

        # Add Cycle dates

        page.get_by_role("button", name="Add Row").nth(1).click()
        page.wait_for_timeout(4000)
        page.get_by_label("Business Unit").type(datadictvalue["C_BSNSS_UNIT"])
        page.get_by_role("option", name=datadictvalue["C_BSNSS_UNIT"]).click()
        page.locator("//span[text()='Statement Date']//following::input[2]").fill(datadictvalue["C_STTMNT_DATE"].strftime("%m/%d/%Y"))
        if datadictvalue["C_SKIP"] == 'Yes':
            page.locator("//span[text()='Skip']//following::input[@type='checkbox']").check()
        if datadictvalue["C_SKIP"] == 'No' or '':
            page.locator("//span[text()='Skip']//following::input[@type='checkbox']").uncheck()
        page.wait_for_timeout(1000)
        
        #Save the individual row of data
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(4000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Save the data

        if i == rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(5000)
            # if page.locator("//div[text()='Warning']//following::button[1]").is_visible():
            #     page.locator("//div[text()='Warning']//following::button[1]").click()
            # if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
            #     page.locator("//div[text()='Confirmation']//following::button[1]").click()

            try:
                expect(page.get_by_role("button", name="Done")).to_be_visible()
                print("Statement Cycle saved Successfully")
                datadictvalue["RowStatus"] = "Statement Cycle added successfully"

            except Exception as e:
                print("Statement Cycle not saved")
                datadictvalue["RowStatus"] = "Statement Cycle not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, STATEMENT_CYCLE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, STATEMENT_CYCLE, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, STATEMENT_CYCLE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + STATEMENT_CYCLE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + STATEMENT_CYCLE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))