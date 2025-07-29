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
    page.get_by_role("textbox").fill("Manage Distribution Sets")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Distribution Sets", exact=True).click()

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        if datadictvalue["C_NAME"] != PrevName:
            # Save the prev type data if the row contains a new type
            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Save and Close").click()
                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("Distribution sets Saved")
                    datadict[i - 1]["RowStatus"] = "Distribution sets Saved"
                except Exception as e:
                    print("Unable to save Distribution sets")
                    datadict[i - 1]["RowStatus"] = "Unable to save Distribution sets"

                page.wait_for_timeout(3000)

            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Business Unit").type(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.get_by_label("Distribution Percentage").select_option(str(datadictvalue["C_DSTRBTN_PRCNTG"]))
            page.locator("//label[text()='Inactive Date']//following::input[1]").fill(datadictvalue["C_INCTV_DATE"])
            PrevName = datadictvalue["C_NAME"]
        
        #Enter the line details

        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(3000)
        page.get_by_label("Line").first.clear()
        page.get_by_label("Line").first.fill(str(datadictvalue["C_LINE"]))
        page.get_by_label("Distribution", exact=True).first.fill(str(datadictvalue["C_DSTRBTN"]))
        page.locator("//span[text()='Description']//following::input[contains(@id,'i6::content')]").first.fill(datadictvalue["C_LINE_DSCRPTN"])
        page.get_by_label("Distribution Combination").first.fill(datadictvalue["C_DSTRBTN_CMBNTN"])
        if datadictvalue["C_INCM_TAX_TYPE"] != '':
            page.get_by_label("Income Tax Type").first.select_option(datadictvalue["C_INCM_TAX_TYPE"])

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Do the save of the last Distribution sets before signing out
        if i == rowcount:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Distribution sets Saved Successfully")
            datadictvalue["RowStatus"] = "Distribution sets are added successfully"

        except Exception as e:
            print("Distribution sets not saved")
            datadictvalue["RowStatus"] = "Distribution sets not added"

    page.wait_for_timeout(2000)
        
    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, DISTRIBUTION_SETS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, DISTRIBUTION_SETS, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, DISTRIBUTION_SETS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + DISTRIBUTION_SETS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
            0] + "_" + DISTRIBUTION_SETS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

