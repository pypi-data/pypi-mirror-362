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
    page.get_by_role("textbox").fill("Manage Approval Limits")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Approval Limits", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(3000)
        page.get_by_role("table", name="Search Results").get_by_label("User Name").click()
        page.wait_for_timeout(2000)
        page.get_by_label("User Name").type(datadictvalue["C_USER_NAME"])
        page.get_by_role("option", name=datadictvalue["C_USER_NAME"]).click()
        page.wait_for_timeout(2000)
        page.get_by_label("Document Type").click()
        page.get_by_label("Document Type").select_option(datadictvalue["C_DCMNT_TYPE"])
        page.get_by_label("Currency").select_option(datadictvalue["C_CRRNCY"])
        page.get_by_label("Minimum Approval Amount").fill(str(datadictvalue["C_MNMM_APPRVL_AMNT"]))
        page.get_by_label("Maximum Approval Amount").fill(str(datadictvalue["C_MXMM_APPRVL_AMNT"]))

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"
        
        i = i + 1
        
        # Save the data

        if i == rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
            # if page.locator("//div[text()='Warning']//following::button[1]").is_visible():
            #     page.locator("//div[text()='Warning']//following::button[1]").click()
            # if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
            #     page.locator("//div[text()='Confirmation']//following::button[1]").click()


            try:
                expect(page.get_by_role("button", name="Done")).to_be_visible()
                print("Approval Limits saved Successfully")
                datadictvalue["RowStatus"] = "Approval Limits added successfully"

            except Exception as e:
                print("Approval Limits not saved")
                datadictvalue["RowStatus"] = "Approval Limits not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, APPROVAL_LIMITS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, APPROVAL_LIMITS, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, APPROVAL_LIMITS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + APPROVAL_LIMITS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + APPROVAL_LIMITS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))