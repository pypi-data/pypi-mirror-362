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
    page.get_by_role("textbox").fill("Manage Expenditure Categories")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Expenditure Categories", exact=True).click()

     # Create Expenditure Categories
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        #Adding new row
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(2000)

        #Entering Name
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_EXPNDTR_NAME"])
        page.wait_for_timeout(1000)

        # Entering Description
        if datadictvalue["C_DSCRPTN"] != '':
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(3000)

        # Entering From & To Date
        if datadictvalue["C_FROM_DATE"]!='':
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date").first.locator("input").nth(0).fill(datadictvalue["C_FROM_DATE"])
            page.locator("//input[contains(@id,'inputDate2')]").first.fill(datadictvalue["C_FROM_DATE"])
        if datadictvalue["C_TO_DATE"] != '':
            # page.get_by_role("cell",name="m/d/yy Press down arrow to access Calendar To Date To Date").first.locator("input").nth(0).fill(datadictvalue["C_TO_DATE"])
            page.locator("//input[contains(@id,'inputDate4')]").first.fill(datadictvalue["C_TO_DATE"])
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

    #Repeating the loop
        i = i + 1

    # Save & Close the data
    page.get_by_role("button", name="Save and Close", exact=True).click()
    page.wait_for_timeout(2000)


    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Expenditure Categories Saved Successfully")
        datadictvalue["RowStatus"] = "Expenditure Categories are added successfully"

    except Exception as e:
        print("Expenditure Categories not saved")
        datadictvalue["RowStatus"] = "Expenditure Categories are not added"


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, EXP_CAT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, EXP_CAT, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, EXP_CAT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + EXP_CAT)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + EXP_CAT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))