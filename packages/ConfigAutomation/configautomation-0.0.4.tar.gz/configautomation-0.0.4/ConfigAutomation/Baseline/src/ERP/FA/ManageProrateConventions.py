from playwright.sync_api import Playwright, sync_playwright, expect
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
    page.get_by_role("textbox").fill("Manage Prorate Conventions")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Prorate Conventions", exact=True).click()

    # StartDate = ''
    # StartDate1 = ''
    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)

        #General info needs to be added only once
        if datadictvalue["C_NAME"] != PrevName:
            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(3000)
                if page.locator("//div[text()='Warning']//following::button[1]").is_visible():
                    page.locator("//div[text()='Warning']//following::button[1]").click()
                if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
                    page.locator("//div[text()='Confirmation']//following::button[1]").click()

                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("Prorate Conventions added successfully")

                except Exception as e:
                    print("Unable to save the Prorate Conventions")
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Name", exact=True).click()
            page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.get_by_label("Reference Data Set").click()
            page.get_by_label("Reference Data Set").select_option(datadictvalue["C_RFRNC_DATA_SET"])
            page.get_by_label("Fiscal Year Name").click()
            page.get_by_label("Fiscal Year Name").select_option(datadictvalue["C_FSCL_YEAR_NAME"])
            if datadictvalue["C_DPRCT_WHEN_DATE_PLCD_IN_SRVC"] == 'Yes':
                page.get_by_text("Depreciate when placed in").check()
            page.wait_for_timeout(1000)
            PrevName = datadictvalue["C_NAME"]

        #Add the Amounts
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(2000)
        page.locator("//input[contains(@id,'ConventionEndDate')]").first.click()
        page.locator("//input[contains(@id,'ConventionEndDate')]").first.fill(datadictvalue["C_END_DATE"])
        page.locator("//input[contains(@id,'ConventionEndDate')]//following::input[1]").first.click()
        page.locator("//input[contains(@id,'ConventionEndDate')]//following::input[1]").first.clear()
        page.locator("//input[contains(@id,'ConventionEndDate')]//following::input[1]").first.fill(datadictvalue["C_PRRT_DATE"])
        page.wait_for_timeout(500)
        # StartDate = page.get_by_role("table", name="Prorate Dates").nth(0).get_by_role("cell").nth(2).text_content()
        # print("Date:", StartDate)
        # StartDate1 = datadictvalue["C_START_DATE"]
        # print("Excel:", StartDate1)


        # #Amounts will be auto generated based on the 1st row
        # if i > 0:
        #
        #     page.get_by_role("button", name="Add Row").click()
        #     page.wait_for_timeout(500)

            # StartDate = page.get_by_role("table", name="Prorate Dates").nth(0).get_by_role("cell").nth(2).text_content()
            # print("Date:", StartDate)
            # StartDate1 = datadictvalue["C_START_DATE"]
            # print("Excel:", StartDate1)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        #Save the data

        if i == rowcount:
            page.wait_for_timeout(10000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
            if page.locator("//div[text()='Warning']//following::button[1]").is_visible():
                page.locator("//div[text()='Warning']//following::button[1]").click()
            if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
                page.locator("//div[text()='Confirmation']//following::button[1]").click()

            try:
                expect(page.get_by_role("button", name="Done")).to_be_visible()
                print("Prorate Conventions added successfully")

            except Exception as e:
                print("Unable to save the Prorate Conventions")

    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANGE_PRORATE_CONV):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANGE_PRORATE_CONV, PRCS_DIR_PATH + FA_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + FA_WORKBOOK, MANGE_PRORATE_CONV)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANGE_PRORATE_CONV)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANGE_PRORATE_CONV + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))