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
    page.get_by_role("textbox").fill("Manage Invoice Tolerances")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Invoice Tolerances", exact=True).click()

    PrevType = ""
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        if datadictvalue["C_TYPE"] != PrevType:
            # Save the prev type data if the row contains a new type
            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Save and Close").click()
                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("Invoice Tolerance Saved")
                    datadict[i - 1]["RowStatus"] = "Invoice Tolerance Saved"
                except Exception as e:
                    print("Unable to save Invoice Tolerance")
                    datadict[i - 1]["RowStatus"] = "Unable to save Invoice Tolerance"

                page.wait_for_timeout(3000)
            page.get_by_role("button", name="Create").click()

            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.get_by_label("Type").select_option(datadictvalue["C_TYPE"])
            page.wait_for_timeout(2000)
            PrevType = datadictvalue["C_TYPE"]

        #update the tolerances
        if datadictvalue["C_ACTVE"] == 'Yes':
            page.get_by_role("cell", name=datadictvalue["C_TLRNCS"]).locator("label").first.check()
            page.wait_for_timeout(2000)
            page.get_by_role("cell", name=datadictvalue["C_TLRNCS"]).get_by_label("Tolerance Limit").fill(str(datadictvalue["C_TLRNCS_LIMIT"]))

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Do the save of the last tolerance type before signing out
        if i == rowcount:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()

            try:
                expect(page.get_by_role("button", name="Done")).to_be_visible()
                print("Invoice Tolerance Saved")
                datadict[i - 1]["RowStatus"] = "Invoice Tolerance Saved"
            except Exception as e:
                print("Unable to save Invoice Tolerance")
                datadict[i - 1]["RowStatus"] = "Unable to save Invoice Tolerance"
    
    page.wait_for_timeout(5000)
    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, INVOICE_TOLERANCES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, INVOICE_TOLERANCES, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, INVOICE_TOLERANCES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + INVOICE_TOLERANCES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
            0] + "_" + INVOICE_TOLERANCES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))