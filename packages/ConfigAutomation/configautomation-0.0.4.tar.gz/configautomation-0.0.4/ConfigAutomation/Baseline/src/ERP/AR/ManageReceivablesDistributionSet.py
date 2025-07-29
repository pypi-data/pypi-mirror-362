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
    page.get_by_role("textbox").fill("Manage Receivables Distribution Sets")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Receivables Distribution Sets", exact=True).click()

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
                    print("Receivables Distribution Set Saved")
                    datadict[i - 1]["RowStatus"] = "Receivables Distribution Set Saved"
                except Exception as e:
                    print("Unable to save Receivables Distribution Set")
                    datadict[i - 1]["RowStatus"] = "Unable to save Receivables Distribution Set"

                page.wait_for_timeout(2000)
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)
            page.locator("//div[text()='Create Receivables Distribution Set']//following::label[text()='Business Unit']//following::input[1]").type(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("option", name=datadictvalue["C_BSNSS_UNIT"]).click()
            page.locator("//div[text()='Create Receivables Distribution Set']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_NAME"])
            page.locator("//div[text()='Create Receivables Distribution Set']//following::label[text()='Description']//following::input[1]").fill(datadictvalue["C_DSCRPTN"])
            if datadictvalue["C_ACTV"] == 'Yes':
                page.locator("[id=\"__af_Z_window\"]").get_by_text("Active").check()
            if datadictvalue["C_ACTV"] != 'Yes':
                page.locator("[id=\"__af_Z_window\"]").get_by_text("Active").uncheck()
            PrevName = datadictvalue["C_NAME"]

        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Percentage").click()
        page.get_by_label("Percentage").fill(str(datadictvalue["C_PRCNTG"]))
        page.get_by_label("Account").fill(datadictvalue["C_ACCNT"])
        page.get_by_label("Line Description").fill(datadictvalue["C_LINE_DSCRPTN"])

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Save the data

        if i == rowcount:
            # page.get_by_role("button", name="&Cancel").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
            # if page.locator("//div[text()='Warning']//following::button[1]").is_visible():
            #     page.locator("//div[text()='Warning']//following::button[1]").click()
            # if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
            #     page.locator("//div[text()='Confirmation']//following::button[1]").click()

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Receivables Distribution Set saved Successfully")
            datadictvalue["RowStatus"] = "Receivables Distribution Set added successfully"

        except Exception as e:
            print("Receivables Distribution Set not saved")
            datadictvalue["RowStatus"] = "Receivables Distribution Set not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, RECEIVABLES_DSTRBTN):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, RECEIVABLES_DSTRBTN, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, RECEIVABLES_DSTRBTN)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + RECEIVABLES_DSTRBTN)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + RECEIVABLES_DSTRBTN + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))