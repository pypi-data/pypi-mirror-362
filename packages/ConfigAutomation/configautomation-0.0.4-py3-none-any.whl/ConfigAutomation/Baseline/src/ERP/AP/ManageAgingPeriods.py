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
    page.get_by_role("textbox").fill("Manage Aging Periods")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Aging Periods", exact=True).click()

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
                    print("Aging Period Saved")
                    datadict[i - 1]["RowStatus"] = "Aging Period Saved"
                except Exception as e:
                    print("Unable to save Aging Period")
                    datadict[i - 1]["RowStatus"] = "Unable to save Aging Period"

                page.wait_for_timeout(3000)
            page.get_by_role("button", name="Create").click()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            if datadictvalue["C_ACTVE"] == 'Yes':
                page.get_by_text("Active").check()
            if datadictvalue["C_ACTVE"] == 'No':
                page.get_by_text("Active").uncheck()
            PrevName = datadictvalue["C_NAME"]

        #Add the details

        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(2000)
        page.get_by_role("cell", name="Column Order").nth(1).locator("input").clear()
        page.get_by_role("cell", name="Column Order").nth(1).locator("input").fill(str(datadictvalue["C_CLMN"]))
        page.get_by_role("cell", name="From").nth(1).locator("input").fill(str(datadictvalue["C_FROM"]))
        page.get_by_role("cell", name="From").nth(1).locator("input").press("Tab")
        page.get_by_role("cell", name="To", exact=True).first.locator("input").fill(str(datadictvalue["C_TO"]))
        page.get_by_role("cell", name="First", exact=True).first.locator("input").fill(datadictvalue["C_FIRST"])
        page.get_by_role("cell", name="Second", exact=True).nth(1).locator("input").fill(datadictvalue["C_SCND"])

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Do the save of the last Aging Period before signing out
        if i == rowcount:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Aging Periods Saved Successfully")
            datadictvalue["RowStatus"] = "Aging Period are added successfully"

        except Exception as e:
            print("Aging Periods not saved")
            datadictvalue["RowStatus"] = "Aging Period not added"

    page.wait_for_timeout(2000)
    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, AGING_PERIODS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, AGING_PERIODS, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, AGING_PERIODS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + AGING_PERIODS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
            0] + "_" + AGING_PERIODS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))