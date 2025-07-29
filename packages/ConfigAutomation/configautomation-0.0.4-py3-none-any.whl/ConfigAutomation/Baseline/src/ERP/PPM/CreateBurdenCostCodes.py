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
    page.get_by_role("textbox").fill("Manage Burden Cost Codes")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Burden Cost Codes", exact=True).click()

    # Create Burden Cost Codes
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Add Row").click()
        page.get_by_label("Burden Cost Code").click()
        page.get_by_label("Burden Cost Code").fill(datadictvalue["C_BRDN_COST_CODES"])

        # Enter Cost Base Description
        if datadictvalue["C_DSCRPTN"] != '':
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(2000)

        if datadictvalue["C_EXPNDTR_TYPE"] != '':
            page.locator("//span[text() ='Expenditure Type']//following::input[contains( @ name, 'expenditureTypeNameId')]").fill(datadictvalue["C_EXPNDTR_TYPE"])
            # page.get_by_role("cell", name="Search Autocompletes on TAB").locator("a").click()
            # page.get_by_role("link", name="Search...").click()
            # page.get_by_label("Name").click()
            # page.get_by_label("Name").fill(datadictvalue["C_EXPNDTR_TYPE"])
            # page.get_by_role("button", name="Search", exact=True).click()
            # page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name=datadictvalue["C_EXPNDTR_TYPE"], exact=True).click()
            # page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        #Enable & Disable Report as direct cost
        # page.get_by_role("row", name="Expand Burden Cost Code").locator("label").nth(2).check()
        if datadictvalue["C_RPRT_AS_DRCT_COST"]=='YES' or 'Yes':
            page.locator("//table[@summary='This table contains column headers corresponding to the data body table below']//following::input[@type='checkbox']//following::label[1]").click()
        # Entering From & To Date
        # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date",exact=True).get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_FROM_DATE"])
        page.locator("//input[contains(@id,'inputDate2')]").first.fill(datadictvalue["C_FROM_DATE"])
        if datadictvalue["C_TO_DATE"] != '':
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date",exact=True).get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_TO_DATE"])
            page.get_by_role("cell", name="Press down arrow to access Calendar To Date Select Date").locator("//input").first.fill(datadictvalue["C_TO_DATE"])
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
        print("Burden Cost Codes Saved Successfully")
        datadictvalue["RowStatus"] = "Burden Cost Codes are added successfully"

    except Exception as e:
        print("Burden Cost Codes not saved")
        datadictvalue["RowStatus"] = "Burden Cost Codes are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, BRDN_CST_CDS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, BRDN_CST_CDS, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, BRDN_CST_CDS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + BRDN_CST_CDS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + BRDN_CST_CDS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))