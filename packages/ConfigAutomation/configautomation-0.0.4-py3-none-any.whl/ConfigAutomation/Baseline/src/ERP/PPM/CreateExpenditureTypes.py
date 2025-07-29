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
    page.get_by_role("textbox").fill("Manage Expenditure Types")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Expenditure Types", exact=True).click()

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        if datadictvalue["C_EXPNDTR_TYPE"] != PrevName:

            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save", exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Add Row").first.click()
            page.wait_for_timeout(4000)
            page.get_by_label("Expenditure Type").click()
            page.get_by_label("Expenditure Type").fill(datadictvalue["C_EXPNDTR_TYPE"])
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(2000)
            # Entering Expenditure Category
            # page.get_by_title("Search: Expenditure Category").click()
            # page.get_by_role("link", name="Search...").click()
            # page.get_by_label("Name").click()
            # page.get_by_label("Name").fill(datadictvalue["C_EXPNDTR_CTGRY"])
            # page.get_by_role("button", name="Search", exact=True).click()
            # page.wait_for_timeout(2000)
            # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_EXPNDTR_CTGRY"], exact=True).click()
            # page.get_by_role("button", name="OK").click()
            page.get_by_label("Expenditure Category").click()
            page.get_by_label("Expenditure Category").fill(datadictvalue["C_EXPNDTR_CTGRY"])
            page.wait_for_timeout(2000)

            # Entering Revenue Category
            page.get_by_role("cell", name="Revenue Category", exact=True).click()
            page.get_by_label("Revenue Category").select_option(datadictvalue["C_RVN_CTGRY"])
            page.get_by_label("Unit of Measure").click()
            page.get_by_label("Unit of Measure").fill(datadictvalue["C_UNIT_OF_MSR"])
            page.wait_for_timeout(2000)

            if datadictvalue["C_FROM_DATE"]:
                page.locator(
                    "//span[text()='From Date']//following::input[contains(@id,'inputDate2::content')]").clear()
                page.locator(
                    "//span[text()='From Date']//following::input[contains(@id,'inputDate2::content')]").fill(
                    datadictvalue["C_FROM_DATE"])

            # Enable/Disable Attributes
            if datadictvalue["C_RATE_RQRD"] == 'Yes':
                page.locator("// a[ @ title = 'Search: Unit of Measure'] // following::label[1]").first.check()
            if datadictvalue["C_RATE_RQRD"] == 'No' or '':
                page.locator(
                    "// a[ @ title = 'Search: Unit of Measure'] // following::label[1]").first.uncheck()
            page.wait_for_timeout(3000)
            if datadictvalue["C_PRCDS_OF_SALE"] == 'Yes':
                page.locator("// a[ @ title = 'Search: Unit of Measure'] // following::label[2]").first.check()
            if datadictvalue["C_PRCDS_OF_SALE"] == 'No' or '':
                page.locator(
                    "// a[ @ title = 'Search: Unit of Measure'] // following::label[2]").first.uncheck()
            PrevName = datadictvalue["C_EXPNDTR_TYPE"]

        page.wait_for_timeout(2000)

        # Expenditure type
        if datadictvalue["C_EXP_TP_NAME"] != "":

            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Add Row").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_label("Name").click()
            page.get_by_label("Name").select_option(datadictvalue["C_EXP_TP_NAME"])
            page.locator("//span[text()='From Date']//following::input[contains(@id,'inputDate3::content')]").fill(
                datadictvalue["C_EXP_TP_FROM_DATE"])
            if datadictvalue["C_TO_DATE"] != '':
                page.locator(
                    "//span[text()='To Date']//following::input[contains(@id,'inputDate4::content')]").first.fill(
                    datadictvalue["C_EXP_TP_TO_DATE"].strftime("%m/%d/%Y"))
            page.wait_for_timeout(3000)

        if datadictvalue["C_CODE"] != '':
            page.get_by_role("button", name="Add Row").nth(2).click()
            page.wait_for_timeout(2000)
            page.get_by_role("table", name="Assigned Sets").locator("a").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Code", exact=True).click()
            page.get_by_label("Code", exact=True).fill(datadictvalue["C_CODE"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=(datadictvalue["C_CODE"]), exact=True).click()
            page.get_by_role("button", name="OK", exact=True).click()
            page.wait_for_timeout(3000)

        # Selecting Business Unit
        if datadictvalue["C_BSNSS_UNIT"] != '':
            page.get_by_role("button", name="Add Row").nth(3).click()
            page.wait_for_timeout(2000)
            page.get_by_role("table", name="Tax Classification Codes").locator("a").first.click()
            # page.get_by_title("Search: Business Unit").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Business Unit").click()
            page.get_by_label("Business Unit").fill(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BSNSS_UNIT"]).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        # Selecting Tax Classification Codes
        if datadictvalue["C_TX_CLSSFCTN_CODE"] != '':
            page.get_by_role("table", name="Tax Classification Codes").locator("a").nth(1).click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_TX_CLSSFCTN_CODE"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TX_CLSSFCTN_CODE"]).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)


        # page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)
        i = i + 1
    page.get_by_role("button", name="Save and Close").click()
    # page.get_by_role("button", name="Cancel").click()

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Contract Types Saved Successfully")
        datadictvalue["RowStatus"] = "Contract Types are added successfully"

    except Exception as e:
        print("Contract Types not saved")
        datadictvalue["RowStatus"] = "Contract Types not added"

    OraSignOut(page, context, browser, videodir)
    return datadict



# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, EXP_TYP):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, EXP_TYP, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, EXP_TYP)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + EXP_TYP)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + EXP_TYP + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))