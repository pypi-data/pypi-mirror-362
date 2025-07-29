from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Manage Payment Terms")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Payment Terms", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Create").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Cutoff Day").fill(datadictvalue["C_CTFF_DAY"])
        page.get_by_label("Rank").fill(datadictvalue["C_RANK"])
        page.locator("//label[text()='From Date']//following::input[1]").click()
        page.locator("//label[text()='From Date']//following::input[1]").clear()
        page.locator("//label[text()='From Date']//following::input[1]").fill(datadictvalue["C_FROM_DATE"].strftime("%m/%d/%Y"))
        if datadictvalue["C_TO_DATE"] != '':
            page.locator("//label[text()='To Date']//following::input[1]").fill(datadictvalue["C_TO_DATE"].strftime("%m/%d/%Y"))

        # Installments
        page.get_by_role("button", name="Add Row").first.click()
        page.get_by_label("Due", exact=True).fill(str(datadictvalue["C_DUE"]))
        page.get_by_label("Amount Due").click()
        page.locator("//span[text()='Amount Due']//following::input[2]").fill(datadictvalue["C_AMNT_DUE"])
        page.get_by_label("Amount Due").fill(datadictvalue["C_AMNT_DUE"])
        if datadictvalue["C_CLNDR"] != '':
            page.get_by_label("Calendar").select_option(datadictvalue["C_CLNDR"])
        if datadictvalue["C_FIXED_DATE"] != '':
            page.locator("//span[text()='Fixed Date']//following::input[3]").fill(datadictvalue["C_FIXED_DATE"].strftime("%m/%d/%Y"))
            # page.get_by_role("row", name="Expand Due Amount Due").get_by_placeholder("m/d/yy").fill(datadictvalue["C_FIXED_DATE"].strftime("%m/%d/%Y"))
        page.wait_for_timeout(2000)
        page.get_by_label("Days", exact=True).fill(str(datadictvalue["C_INSTLLMNT_DAYS"]))
        page.wait_for_timeout(2000)
        page.get_by_label("Day of Month", exact=True).fill(str(datadictvalue["C_INSTLLMNT_DAY_OF_MONTH"]))
        page.get_by_label("Day of Month", exact=True).press("Tab")
        page.wait_for_timeout(2000)
        if page.get_by_label("Months Ahead", exact=True).is_enabled():
            page.get_by_label("Months Ahead", exact=True).fill(str(datadictvalue["C_INSTLLMNT_MNTHS_AHD"]))
        page.wait_for_timeout(2000)

        #Discount

        page.get_by_label("First Discount Percentage").click()
        page.get_by_label("First Discount Percentage").fill(str(datadictvalue["C_FIRST_DSCNT"]))
        page.get_by_label("First Discount Days").fill(str(datadictvalue["C_FIRST_DAYS"]))
        page.wait_for_timeout(1000)
        page.get_by_label("First Discount Day of Month").fill(str(datadictvalue["C_FIRST_DAY_OF_MONTH"]))
        page.wait_for_timeout(1000)
        if page.get_by_label("First Discount Months Ahead").is_enabled():
            page.get_by_label("First Discount Months Ahead").fill(str(datadictvalue["C_FIRST_MNTHS_AHD"]))

        page.get_by_label("Second Discount Percentage").click()
        page.get_by_label("Second Discount Percentage").fill(str(datadictvalue["C_SCND_DSCNT"]))
        page.wait_for_timeout(1000)
        page.get_by_label("Second Discount Days").fill(str(datadictvalue["C_SCND_DAYS"]))
        page.wait_for_timeout(1000)
        page.get_by_label("Second Discount Day of Month").fill(str(datadictvalue["C_SCND_DAY_OF_MONTH"]))
        page.wait_for_timeout(1000)
        if page.get_by_label("Second Discount Months Ahead").is_enabled():
            page.get_by_label("Second Discount Months Ahead").fill(str(datadictvalue["C_SCND_MNTHS_AHD"]))

        page.get_by_label("Third Discount Percentage").click()
        page.get_by_label("Third Discount Percentage").fill(str(datadictvalue["C_THIRD_DSCNT"]))
        page.wait_for_timeout(1000)
        page.get_by_label("Third Discount Days").fill(str(datadictvalue["C_THIRD_DAYS"]))
        page.wait_for_timeout(1000)
        page.get_by_label("Third Discount Day of Month").fill(str(datadictvalue["C_THIRD_DAY_OF_MONTH"]))
        page.wait_for_timeout(1000)
        if page.get_by_label("Third Discount Months Ahead").is_enabled():
            page.get_by_label("Third Discount Months Ahead").fill(str(datadictvalue["C_THIRD_MNTHS_AHD"]))

        # Set Assignments

        page.get_by_role("button", name="Add Row").nth(1).click()
        page.get_by_label("DspSetId").click()
        page.get_by_label("DspSetId").select_option(datadictvalue["C_SET_CODE"])
        page.wait_for_timeout(3000)

        #Save the data

        page.get_by_role("button", name="Save and Close").click()

        i = i + 1
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Payment Terms Saved Successfully")
            datadictvalue["RowStatus"] = "Payment Terms are added successfully"

        except Exception as e:
            print("Payment Terms not saved")
            datadictvalue["RowStatus"] = "Payment Terms are not added"


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYMENT_TERMS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYMENT_TERMS, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, PAYMENT_TERMS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + PAYMENT_TERMS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
            0] + "_" + PAYMENT_TERMS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

