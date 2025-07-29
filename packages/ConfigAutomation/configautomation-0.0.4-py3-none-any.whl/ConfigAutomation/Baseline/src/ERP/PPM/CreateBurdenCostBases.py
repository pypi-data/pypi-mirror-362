from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Manage Burden Cost Bases")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Burden Cost Bases", exact=True).click()

    # Create Burden Cost Bases
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(1000)
        #Enter Cost Base
        page.get_by_label("Cost Base", exact=True).click()
        page.get_by_label("Cost Base", exact=True).fill(datadictvalue["C_COST_BASE"])
        page.wait_for_timeout(2000)
        # Enter Cost Base Description
        if datadictvalue["C_DSCRPTN"] != '':
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(1000)
        # Enter Report Order
        page.get_by_label("Report Order").click()
        page.get_by_label("Report Order").fill(str(datadictvalue["C_RPRT_ORDER"]))
        page.wait_for_timeout(2000)
        # Enter Cost Base Types
        page.get_by_label("Cost Base Type").select_option(datadictvalue["C_COST_BASE_TYPE"])
        page.wait_for_timeout(2000)

        # Entering From & To Date
        # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date",exact=True).get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_FROM_DATE"])
        page.locator("//input[contains(@id,'inputDate2')][1]").nth(0).fill(datadictvalue["C_FROM_DATE"])
        if datadictvalue["C_TO_DATE"] != '':
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date",exact=True).get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_TO_DATE"])
            page.locator("//input[contains(@id,'inputDate4')][1]").fill(datadictvalue["C_TO_DATE"])
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1

    # Save & Close the data
    page.get_by_role("button", name="Save and Close").click()

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Burden Cost Bases Saved Successfully")
        datadictvalue["RowStatus"] = "Burden Cost Bases are added successfully"

    except Exception as e:
        print("Burden Cost Bases not saved")
        datadictvalue["RowStatus"] = "Burden Cost Bases are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, BRDN_CST_BSS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, BRDN_CST_BSS, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, BRDN_CST_BSS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + BRDN_CST_BSS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + BRDN_CST_BSS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))