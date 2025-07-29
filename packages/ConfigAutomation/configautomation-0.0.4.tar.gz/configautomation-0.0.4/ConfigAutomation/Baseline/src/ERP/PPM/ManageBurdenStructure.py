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
    page.get_by_role("textbox").fill("Manage Burden Structures")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Burden Structures").click()
    page.wait_for_timeout(3000)


    # Create Burden Structure

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        if datadictvalue["C_NAME"] != PrevName:
            page.get_by_role("button", name="Add Row").first.click()
            page.wait_for_timeout(2000)
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.get_by_label("Structure Type").select_option(datadictvalue["C_STRCTR_TYPE"])
            if datadictvalue["C_USE_IN_SCHDL_OVRRDS"] == 'Yes':
                page.locator("//span[text()='Use in Schedule Overrides']//following::label[contains(@id,'Label0')][1]").check()
                if datadictvalue["C_USE_AS_OVRRD_DFLT"] == 'Yes' :
                    page.locator("//span[text() ='Use as Override Default']//following::label[contains( @ id, 'Label0')][2]").check()

            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"])
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"])

            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"])
            page.locator("//input[contains(@id,'inputDate2')]").first.fill(datadictvalue["C_FROM_DATE"])

            if datadictvalue["C_TO_DATE"]!='':
                # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"])
                page.locator("//input[contains(@id,'inputDate4')]").first.fill(datadictvalue["C_TO_DATE"])


            # Cost Base Assignments
            if datadictvalue["C_COST_BASE"] != '':
                page.get_by_role("button", name="Add Row").nth(1).click()
                page.wait_for_timeout(1000)
                page.get_by_role("row", name="Search Autocompletes on TAB").locator("a").click()
                page.get_by_role("link", name="Search...").click()
                # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").fill(datadictvalue["C_COST_BASE"])
                page.locator("//div[text()='Search and Select: Cost Base']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_COST_BASE"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.get_by_role("cell", name=datadictvalue["C_COST_BASE"], exact=True).click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)

            # Burden Cost Code
            page.get_by_role("button", name="Add Row").nth(2).click()
            page.wait_for_timeout(1000)
            page.locator("//span[text()='Burden Cost Code']//following::input[1]").fill(datadictvalue["C_BRDN_COST_CODE"])


            page.get_by_role("link", name="Expenditure Types").click()
            page.wait_for_timeout(1000)
            # Add Expenditure type
            PrevName = datadictvalue["C_NAME"]
            print("Name:", PrevName)

        page.get_by_role("button", name="Add Row").nth(2).click()
        page.wait_for_timeout(1000)
        page.locator("//span[text()='Expenditure Type']//following::input[1]").fill(datadictvalue["C_EXPNDTR_TYPE"])
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)
        # Repeating the loop
        i = i + 1

        # Save and Close
        if i == rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)


        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Burden Structure Saved Successfully")
            datadictvalue["RowStatus"] = "Burden Structure added successfully"

        except Exception as e:
            print("Burden Structure not saved")
            datadictvalue["RowStatus"] = "Burden Structure are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, MGE_BRDN_STR):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, MGE_BRDN_STR, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, MGE_BRDN_STR)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + MGE_BRDN_STR)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + MGE_BRDN_STR + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))