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

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Manage Tax Fields")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Tax Fields").click()

    i = 0
    while i < rowcount:

        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        # Search the Business Unit

        if page.get_by_role("table",
                            name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).is_visible():
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
            page.get_by_role("link", name=datadictvalue["C_BSNSS_UNIT"]).click()
        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
            page.get_by_role("link", name=datadictvalue["C_BSNSS_UNIT"]).click()

        if datadictvalue["C_DSPLY_TAX_FLDS_ON_EXPNS_RPRT"] == 'Yes':

            #Enable the Display tax fields on expense report if it is required

            page.get_by_text("Display tax fields on expense report", exact=True).check()
            page.wait_for_timeout(2000)

            # Enter the Tax Fields for All Other Locations
            page.get_by_label("Merchant Name").select_option(datadictvalue["C_MRCHNT_NAME"])
            page.get_by_label("Receipt Number").select_option(datadictvalue["C_RCPT_NMBR"])
            page.get_by_label("Tax Registration Number").select_option(datadictvalue["C_TAX_RGSTRTN_NMBR"])
            page.get_by_label("Taxpayer ID").select_option(datadictvalue["C_TXPYR_ID"])
            page.get_by_label("Merchant Reference").select_option(datadictvalue["C_MRCHNT_RFRNC"])
            page.get_by_label("Tax Classification Code").select_option(datadictvalue["C_TAX_CLSSFCTN_CODE"])

            #Enter the Tax Fields for Specific Countries

            if datadictvalue["C_CNTRY_OR_TRRRTY"] != '':
                page.get_by_role("button", name="Add Row").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Country or Territory").select_option(datadictvalue["C_CNTRY_OR_TRRRTY"])
                page.get_by_role("table", name="Tax Fields for Specific").get_by_label("Merchant Name").select_option(datadictvalue["C_SPCFC_MRCHNT_NAME"])
                page.get_by_role("table", name="Tax Fields for Specific").get_by_label("Taxpayer ID").select_option(datadictvalue["C_SPCFC_TXPYR_ID"])
                page.get_by_role("table", name="Tax Fields for Specific").get_by_label("Receipt Number").select_option(datadictvalue["C_SPCFC_RCPT_NMBR"])
                page.get_by_role("table", name="Tax Fields for Specific").get_by_label("Merchant Reference").select_option(datadictvalue["C_SPCFC_MRCHNT_RFRNC"])
                page.get_by_role("table", name="Tax Fields for Specific").get_by_label("Tax Registration Number").select_option(datadictvalue["C_SPCFC_TAX_RGSTRTN_NMBR"])
                page.get_by_role("table", name="Tax Fields for Specific").get_by_label("Tax Classification Code").select_option(datadictvalue["C_SPCFC_TAX_CLSSFCTN_CODE"])
            page.wait_for_timeout(2000)
        else:
            if datadictvalue["C_DSPLY_TAX_FLDS_ON_EXPNS_RPRT"] == 'No':
                page.get_by_text("Display tax fields on expense report", exact=True).uncheck()
                page.wait_for_timeout(2000)

            # Save the data

        # Clicking on the Detach button because UI page is keep on moving
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Detach").click()
        page.wait_for_timeout(1000)
        page.get_by_role("link", name="Close").click()
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        if page.get_by_role("button", name="Yes").is_visible():
            page.get_by_role("button", name="Yes").click()
        if page.get_by_role("button", name="OK").is_visible():
            page.get_by_role("button", name="OK").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Tax fields Saved Successfully")
            datadictvalue["RowStatus"] = "Tax fields are saved successfully"

        except Exception as e:
            print("Tax fields not saved")
            datadictvalue["RowStatus"] = "Tax fields are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, TAX_FIELDS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, TAX_FIELDS,
                             PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, TAX_FIELDS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
                                   0] + "_" + TAX_FIELDS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + TAX_FIELDS + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))



