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
    page.wait_for_timeout(5000)

    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Conversion Rates And Policies")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Conversion Rates And Policies").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        # Filtering the Business Unit
        if page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).is_visible():
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).type(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).press("Enter")
            page.wait_for_timeout(2000)

        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(2000)
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).type(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).press("Enter")
            page.wait_for_timeout(2000)

        page.get_by_role("link", name=datadictvalue["C_BSNSS_UNIT"]).click()

        # Issue with the UI - Handled by clicking detach button
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Detach").click()
        page.wait_for_timeout(2000)
        page.get_by_role("link", name="Close").click()
        page.wait_for_timeout(2000)

        page.get_by_label("Conversion Rate Type").fill(datadictvalue["C_CNVRSN_RATE_TYPE"])
        # page.get_by_role("option", name="Corporate Corporate Exchange").click()
        if datadictvalue["C_DFLT_CNVRSN_RATE"] == 'Yes':
            page.locator("//label[text()='Conversion Rate Type']//following::label[contains(@id,'Label0')][1]").check()
        page.get_by_label("Warning Tolerance Percentage").click()
        page.get_by_label("Warning Tolerance Percentage").fill(str(datadictvalue["C_WRNNG_TLRNC_PRCNTG"]))
        if datadictvalue["C_DSPLY_WRNNG_TO_USER"] == 'Yes':
            page.get_by_text("Display warning to user", exact=True).check()
        page.get_by_label("Error Tolerance Percentage").click()
        page.get_by_label("Error Tolerance Percentage").fill(str(datadictvalue["C_ERROR_TLRNC_PRCNTG"]))

        #Add Individual Currency exceptions

        page.get_by_role("button", name="Add Row").click()
        page.get_by_label("Currency").click()
        page.get_by_label("Currency").select_option(datadictvalue["C_CRRNCY"])
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save and Close").click()

        #Validation

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            # page.locator("//div[text()='Confirmation']//following::button[1]").click()
            print("Conversion Rates and Policies Saved Successfully")
            # datadictvalue["RowStatus"] = "Configuration Saved Successfully"
        except Exception as e:
            print("Conversion Rates and Policies Saved UnSuccessfully")
            # datadictvalue["RowStatus"] = "Conversion Rates and Policies Saved UnSuccessfully"

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, CONV_RATES_POLICY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, CONV_RATES_POLICY, PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, CONV_RATES_POLICY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[0] + "_" + CONV_RATES_POLICY)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + CONV_RATES_POLICY + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))