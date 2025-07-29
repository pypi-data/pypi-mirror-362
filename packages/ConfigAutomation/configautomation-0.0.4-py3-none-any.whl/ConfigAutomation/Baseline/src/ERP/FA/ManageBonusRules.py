from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
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
    page.get_by_role("textbox").fill("Manage Bonus Rules")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Bonus Rules", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(2000)
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(1000)
        page.get_by_label("Reference Data Set").select_option(datadictvalue["C_RFRNC_DATA_SET"])
        page.wait_for_timeout(1000)
        page.get_by_label("Calculation Basis").click()
        page.get_by_label("Calculation Basis").select_option(datadictvalue["C_CLCLTN_BASIS"])

        if datadictvalue["C_CLCLTN_BASIS"] == 'Annual depreciation' or datadictvalue["C_CLCLTN_BASIS"] == 'Cost':
            page.get_by_label("Rate Type").click()
            page.get_by_label("Rate Type").select_option(datadictvalue["C_RATE_TYPE"])
            page.wait_for_timeout(2000)
            if datadictvalue["C_RATE_TYPE"] == 'Period':
                page.get_by_label("Calendar Name").select_option(datadictvalue["C_CLNDR_NAME"])
            page.get_by_label("Bonus Class").click()
            page.get_by_label("Bonus Class").select_option(datadictvalue["C_BONUS_CLASS"])
        if datadictvalue["C_CLCLTN_BASIS"] == 'Basis used by depreciation method':
            page.wait_for_timeout(2000)
            if datadictvalue["C_ONE_TIME_DPRCTN"] == 'Yes':
                page.get_by_text("One time depreciation").check()
            if datadictvalue["C_ONE_TIME_DPRCTN"] == 'No':
                page.get_by_text("One time depreciation").uncheck()
        if datadictvalue["C_CLCLTN_BASIS"] == 'Change in cost':
            page.get_by_label("Rate Type").select_option(datadictvalue["C_RATE_TYPE"])
            page.wait_for_timeout(2000)
            if datadictvalue["C_RATE_TYPE"] == 'Period':
                page.get_by_label("Calendar Name").select_option(datadictvalue["C_CLNDR_NAME"])
            page.get_by_label("Recapture Year").click()
            page.get_by_label("Recapture Year").fill(str(datadictvalue["C_RCPTR_YEAR"]))
            if datadictvalue["C_ONE_TIME_DPRCTN"] == 'Yes':
                page.get_by_text("One time depreciation").check()
            if datadictvalue["C_ONE_TIME_DPRCTN"] == 'No':
                page.get_by_text("One time depreciation").uncheck()


        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_CLCLTN_BASIS"] == 'Basis used by depreciation method' or datadictvalue["C_RATE_TYPE"] == 'Year':
            page.get_by_label("From Year").fill(str(datadictvalue["C_FROM_YEAR"]))
            page.wait_for_timeout(1000)
            page.get_by_label("To Year").fill(str(datadictvalue["C_TO_YEAR"]))
            page.wait_for_timeout(1000)
            page.get_by_label("Rate Percent").fill(str(datadictvalue["C_RATE_PRCNT"]))
            page.wait_for_timeout(1000)
        if datadictvalue["C_RATE_TYPE"] == 'Period':
            page.get_by_role("table", name="Bonus Rate").locator("a").nth(0).click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Period Name").fill(datadictvalue["C_FROM_PRD"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FROM_PRD"]).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)
            page.get_by_role("table", name="Bonus Rate").locator("a").nth(1).click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Period Name").fill(datadictvalue["C_TO_PRD"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TO_PRD"]).click()
            page.get_by_role("button", name="OK").click()
            page.get_by_label("Rate Percent").fill(str(datadictvalue["C_RATE_PRCNT"]))
            page.wait_for_timeout(3000)

        # Save the data
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        if page.locator("//div[text()='Warning']//following::button[1]").is_visible():
            page.locator("//div[text()='Warning']//following::button[1]").click()
        if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
            page.locator("//div[text()='Confirmation']//following::button[1]").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Bonus Rule Saved Successfully")
            datadictvalue["RowStatus"] = "Bonus Rule added successfully"

        except Exception as e:
            print("Bonus Rule not saved")
            datadictvalue["RowStatus"] = "Bonus Rule not added"

    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_BONUS_RULE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_BONUS_RULE, PRCS_DIR_PATH + FA_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + FA_WORKBOOK, MANAGE_BONUS_RULE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANAGE_BONUS_RULE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANAGE_BONUS_RULE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

