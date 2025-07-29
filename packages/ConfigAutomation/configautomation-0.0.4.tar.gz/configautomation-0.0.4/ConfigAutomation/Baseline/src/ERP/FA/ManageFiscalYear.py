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
    page.get_by_role("textbox").fill("Manage Fiscal Years")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Fiscal Years", exact=True).click()


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)


        if i == 0:
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.get_by_label("Description").press("Tab")
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Add Row").click()
            page.get_by_label("Fiscal Year").click()
            page.get_by_label("Fiscal Year").fill(str(datadictvalue["C_FSCL_YEAR"]))
            page.get_by_role("cell", name="Press down arrow to access Calendar Start Date Select Date", exact=True).locator("//input[contains(@id,'FisYr1')]").first.fill(datadictvalue["C_START_DATE"])
            page.get_by_role("cell", name="Press down arrow to access Calendar End Date Select Date", exact=True).locator("//input[contains(@id,'FisYr1')]").first.fill(datadictvalue["C_END_DATE"])
            if datadictvalue["C_MDYR_START_DATE"] != '':
                page.get_by_role("cell", name="Press down arrow to access Calendar Midyear Start Date Select Date",exact=True).locator("//input[contains(@id,'FisYr1')]").first.fill(datadictvalue["C_MDYR_START_DATE"])

        if i > 0:
            page.get_by_role("button", name="Add Row").click()
            page.wait_for_timeout(3000)
            FiscalYear = page.get_by_role("table", name="Fiscal Year").get_by_role("cell").nth(2).text_content()
            print("Year:", FiscalYear)
            print("Excel:", datadictvalue["C_FSCL_YEAR"])
            # if datadictvalue["C_FSCL_YEAR"] == FiscalYear:
            #     page.get_by_role("button", name="Save", exact=True).click()
            #     page.wait_for_timeout(10000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        if i == rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
            if page.locator("//div[text()='Warning']//following::button[1]").is_visible():
                page.locator("//div[text()='Warning']//following::button[1]").click()
            if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
                page.locator("//div[text()='Confirmation']//following::button[1]").click()

            try:
                expect(page.get_by_role("button", name="Done")).to_be_visible()
                print("Fiscal Year added successfully")

            except Exception as e:
                print("Unable to save the Fiscal Year")

    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANGE_FISCAL_YEAR):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANGE_FISCAL_YEAR, PRCS_DIR_PATH + FA_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + FA_WORKBOOK, MANGE_FISCAL_YEAR)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANGE_FISCAL_YEAR)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANGE_FISCAL_YEAR + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))