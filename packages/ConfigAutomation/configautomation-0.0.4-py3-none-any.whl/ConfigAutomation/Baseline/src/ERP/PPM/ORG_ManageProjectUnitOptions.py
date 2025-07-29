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
    page.get_by_role("textbox").fill("Manage Project Unit Options")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Project Unit Options", exact=True).click()

    # Create Service Types
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        #Code
        page.get_by_title("Search:  Code").click()
        page.wait_for_timeout(1000)
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Code").click()
        page.wait_for_timeout(1000)
        page.get_by_role("textbox", name="Code").fill(datadictvalue["C_CODE"])
        page.wait_for_timeout(1000)
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(1000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CODE"]).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(5000)

        #Name
        # page.get_by_title("Search:  Name").click()
        # page.wait_for_timeout(1000)
        # page.get_by_role("link", name="Search...").click()
        # page.get_by_role("textbox", name="Name").click()
        # page.get_by_role("textbox", name="Name").fill(datadictvalue["C_NAME"])
        # page.wait_for_timeout(1000)
        # page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_NAME"]).click()
        # page.get_by_role("button", name="OK").click()
        # page.wait_for_timeout(2000)

        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)

        page.get_by_role("link", name=datadictvalue["C_CODE"]).nth(0).click()
        page.wait_for_timeout(2000)

        page.get_by_title("Search: Default Set").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_DFLT_SET"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("cell", name=datadictvalue["C_DFLT_SET"], exact=True).locator("span").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(2000)

        # ***BU will be autopopulated after all the setups done***
        # page.get_by_text(datadictvalue["C_AVLBL_BSNSS_UNITS"]).click()
        # page.get_by_role("button", name="Move selected items to:").click()
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(5000)

        if datadictvalue.get("C_RQSTNS_INCLD_IN_SMMRZRN") == "Yes":
            # page.get_by_role("row", name="Requisitions Status: Requisitions", exact=True).locator("label").first.check()
            page.locator("(//label[contains(@id,'StatusReqChoice')])[1]").check()
            page.wait_for_timeout(3000)
            page.get_by_label("Status: Requisitions").click()
            page.get_by_label("Status: Requisitions").select_option(datadictvalue["C_RQSTNS_STTS"])
        if datadictvalue.get("C_RQSTNS_INCLD_IN_SMMRZRN") == "No":
            # page.get_by_role("row", name="Requisitions Status: Requisitions", exact=True).locator("label").first.uncheck()
            page.locator("(//label[contains(@id,'StatusReqChoice')])[1]").uncheck()

        if datadictvalue["C_PRCHS_ORDRS_INCLD_IN_SMMRZTN"] == 'Yes':
            # page.get_by_role("row", name="Purchase orders Status: Purchase orders", exact=True).locator("label").first.check()
            page.locator("(//label[contains(@id,'StatusPoChoice')])[1]").check()
        page.get_by_label("Status: Purchase orders").select_option(datadictvalue["C_PRCHS_ORDRS_STTS"])
        if datadictvalue["C_PRCHS_ORDRS_INCLD_IN_SMMRZTN"] == 'No':
            # page.get_by_role("row", name="Purchase orders Status: Purchase orders", exact=True).locator("label").first.uncheck()
            page.locator("(//label[contains(@id,'StatusPoChoice')])[1]").uncheck()
        page.get_by_label("Status: Purchase orders").select_option(datadictvalue["C_PRCHS_ORDRS_STTS"])
        # if datadictvalue["C_PRCHS_ORDRS_INCLD_IN_SMMRZTN"] == 'No':
        #     if page.get_by_role("row", name="Purchase orders Status: Purchase orders", exact=True).locator(
        #             "label").first.is_checked():
        #         page.get_by_role("row", name="Purchase orders Status: Purchase orders", exact=True).locator(
        #             "label").first.click()

        if datadictvalue["C_SPPLR_INVCS_INCLD_IN_SMMRZTN"] == 'Yes':
            # page.get_by_role("row", name="Supplier invoices Status: Supplier invoices", exact=True).locator("label").first.check()
            page.locator("(//label[contains(@id,'StatusSupinvChoice')])[1]").check()
        page.get_by_label("Status: Supplier invoices").select_option(datadictvalue["C_SPPLR_INVCS_STTS"])
        if datadictvalue["C_SPPLR_INVCS_INCLD_IN_SMMRZTN"] == 'No':
            # page.get_by_role("row", name="Supplier invoices Status: Supplier invoices", exact=True).locator("label").first.uncheck()
            page.locator("(//label[contains(@id,'StatusSupinvChoice')])[1]").uncheck()

        if datadictvalue["C_OTHR_CMMTMNTS_INCLD_IN_SMMRZTN"] == 'Yes':
            # page.get_by_role("row", name="Other commitments", exact=True).locator("label").first.check()
            page.locator("input[type='checkbox']").nth(3).check()
        if datadictvalue["C_OTHR_CMMTMNTS_INCLD_IN_SMMRZTN"] == 'No':
            # page.get_by_role("row", name="Other commitments", exact=True).locator("label").first.uncheck()
            page.locator("input[type='checkbox']").nth(3).uncheck()

        page.get_by_label("Basis").click()
        page.get_by_label("Basis").select_option(datadictvalue["C_PLNNNG_AMNT_ALLCTN_BASIS"])
        page.wait_for_timeout(2000)

        if page.get_by_role("button", name="OK").is_visible():
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        # Save & Close the data
        page.get_by_role("button", name="Save", exact=True)
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        if page.get_by_role("button", name="OK").is_visible():
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1


    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Manage Project Unit Options Saved Successfully")
        datadictvalue["RowStatus"] = "Manage Project Unit Options are added successfully"

    except Exception as e:
        print("Manage Project Unit Options not saved")
        datadictvalue["RowStatus"] = "Manage Project Unit Options are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_UNIT_OPTS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_UNIT_OPTS, PRCS_DIR_PATH + PPM_ORG_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_UNIT_OPTS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_ORG_CONFIG_WRKBK)[0] + "_" + PRJ_UNIT_OPTS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_ORG_CONFIG_WRKBK)[
            0] + "_" + PRJ_UNIT_OPTS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))