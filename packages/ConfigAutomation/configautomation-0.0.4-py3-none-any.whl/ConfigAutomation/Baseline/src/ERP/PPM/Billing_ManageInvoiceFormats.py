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
    page.get_by_role("textbox").fill("Manage Invoice Formats")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Invoice Formats", exact=True).click()

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        
        if datadictvalue["C_NAME"] != PrevName:
            # Save the prev type data if the row contains a new type
            if i > 0:
                page.wait_for_timeout(1000)
                page.get_by_role("button", name="Save", exact=True).click()
                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("Invoice formats Saved")
                    datadict[i - 1]["RowStatus"] = "Invoice formats Saved"
                except Exception as e:
                    print("Unable to save Invoice formats")
                    datadict[i - 1]["RowStatus"] = "Unable to save Invoice formats"

                page.wait_for_timeout(3000)

            page.get_by_role("button", name="Add Row").first.click()
            page.wait_for_timeout(2000)
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.wait_for_timeout(2000)
            page.get_by_label("Format Type").click()
            page.get_by_label("Format Type").select_option(datadictvalue["C_FRMT_TYPE"])
            page.wait_for_timeout(2000)
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"])
            page.locator("//input[contains(@id,'inputDate2')][1]").nth(0).fill(datadictvalue["C_FROM_DATE"].strftime("%m/%d/%Y"))
            if datadictvalue["C_TO_DATE"] != '':
                # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"].strftime("%m/%d/%Y"))
                page.locator("//input[contains(@id,'inputDate4')][1]").nth(0).fill(datadictvalue["C_TO_DATE"].strftime("%m/%d/%Y"))
            page.get_by_title("Search: Grouping Option").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Grouping Option").fill(
                datadictvalue["C_GRPPNG_OPTN"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_GRPPNG_OPTN"]).click()
            page.get_by_role("button", name="OK").click()
            # page.get_by_label("Grouping Option").click()
            # page.get_by_label("Grouping Option").type(datadictvalue["C_GRPPNG_OPTN"])
            # page.get_by_role("option", name=datadictvalue["C_GRPPNG_OPTN"]).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_CSTMR_INVC"] == 'Yes':
                page.locator("(//input[@type='checkbox'])[1]").check()
            if datadictvalue["C_CSTMR_INVC"] == 'No':
                page.locator("(//input[@type='checkbox'])[1]").uncheck()
            if datadictvalue["C_INTRNL_INVC"] == 'Yes':
                page.locator("(//input[@type='checkbox'])[2]").check()
            if datadictvalue["C_INTRNL_INVC"] == 'No':
                page.locator("(//input[@type='checkbox'])[2]").uncheck()
            if datadictvalue["C_FIXED_FRMT"] == 'Yes':
                page.locator("(//input[@type='checkbox'])[3]").check()
            if datadictvalue["C_FIXED_FRMT"] == 'No':
                page.locator("(//input[@type='checkbox'])[3]").uncheck()
            page.wait_for_timeout(2000)
            PrevName = datadictvalue["C_NAME"]
            page.wait_for_timeout(2000)


        page.get_by_role("button", name="Add Row").nth(1).click()
        page.wait_for_timeout(2000)
        page.get_by_title("Search: Attribute Name").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Attribute Name").fill(datadictvalue["C_FLD_NAME"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FLD_NAME"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        # page.get_by_label("Attribute Name").click()
        # page.get_by_label("Attribute Name").type(datadictvalue["C_FLD_NAME"])
        # page.get_by_role("option", name=datadictvalue["C_FLD_NAME"], exact=True).click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_EXCLD"] == 'Yes':
            page.get_by_role("table", name="Invoice Format Details").locator("label").nth(1).check()
        if datadictvalue["C_EXCLD"] == 'No':
            page.get_by_role("table", name="Invoice Format Details").locator("label").nth(1).uncheck()
        page.get_by_label("Start Position").clear()
        page.get_by_label("Start Position").fill(str(datadictvalue["C_START_PSTN"]))
        page.get_by_label("End Position").clear()
        page.get_by_label("End Position").fill(str(datadictvalue["C_END_PSTN"]))
        if datadictvalue["C_TEXT"] !='':
            page.get_by_label("Text").fill(datadictvalue["C_TEXT"])
        if datadictvalue["C_RIGHT_JSTFY"] == 'Yes':
            page.get_by_role("table", name="Invoice Format Details").locator("label").nth(4).check()
        if datadictvalue["C_RIGHT_JSTFY"] == 'No':
            page.get_by_role("table", name="Invoice Format Details").locator("label").nth(4).uncheck()


        # page.get_by_role("cell", name="Name", exact=True).click()
        # page.wait_for_timeout(2000)
        # page.get_by_role("button", name="Save", exact=True).click()
        # page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Do the save of the last Invoice formats before signing out
        if i == rowcount:
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Invoice formats Saved Successfully")
            datadictvalue["RowStatus"] = "Invoice formats are added successfully"

        except Exception as e:
            print("Invoice formats not saved")
            datadictvalue["RowStatus"] = "Invoice formats not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_BILLING_CONFIG_WRKBK, INV_FORMATS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_BILLING_CONFIG_WRKBK, INV_FORMATS,
                             PRCS_DIR_PATH + PPM_BILLING_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_BILLING_CONFIG_WRKBK, INV_FORMATS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_BILLING_CONFIG_WRKBK)[0] + "_" + INV_FORMATS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_BILLING_CONFIG_WRKBK)[
            0] + "_" + INV_FORMATS + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

