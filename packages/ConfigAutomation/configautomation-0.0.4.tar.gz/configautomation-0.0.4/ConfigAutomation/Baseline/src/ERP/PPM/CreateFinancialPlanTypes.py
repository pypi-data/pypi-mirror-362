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
    page.get_by_role("textbox").fill("Manage Financial Plan Types")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Financial Plan Types", exact=True).click()

    #Create Planning and Billing Resource Breakdown Structures
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_SPNSRD_PRJCT"]=='Yes' or 'Y':
            page.get_by_text("Financial Plan Type for Sponsored Project").click()
        elif datadictvalue["C_SPNSRD_PRJCT"]=='No' or 'N':
            page.get_by_text("Financial Plan Type for Non-").click()
        # page.get_by_role("cell", name=datadictvalue["C_SPNSRD_PRJCT"], exact=True).click()
        page.get_by_role("textbox", name="Name").click()
        page.get_by_role("textbox", name="Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(1000)
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(1000)
        # page.get_by_role("row", name="*From Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"])
        page.locator("//label[text()='From Date']//following::input[1]").nth(0).fill(datadictvalue["C_FROM_DATE"])
        if datadictvalue["C_TO_DATE"] != '':
            # page.get_by_role("row", name="To Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"])
            page.locator("//label[text()='To Date']//following::input[1]").first.fill(datadictvalue["C_TO_DATE"].strftime('%m/%d/%y'))
        page.get_by_label("Planning Amounts").click()
        page.get_by_label("Planning Amounts").select_option(datadictvalue["C_PLNNNG_ACCNTS"])
        if datadictvalue["C_DSGNT_AS_APPRVD_COST_BDGT_FRCST"] == 'Yes':
            page.get_by_text("Designate as approved cost").click()
        if datadictvalue["C_USE_WRKFLW_FOR_STTS_CHNGS"] == 'Yes':
            page.get_by_text("Use workflow for status").click()
        if datadictvalue["C_SET_AS_DFLT_FNNCL_PLAN_TYPE"] == 'Yes':
            page.get_by_text("Set as default award").click()
        if datadictvalue["C_ENBL_PLNNNG_IN_MLTPL_TRNSCTN_CRRNCS"] == 'Yes':
            page.get_by_text("Enable planning in multiple").click()
        if datadictvalue["C_ENBL_BDGTRY_CNTRLS"] == 'Yes':
            page.get_by_text("Enable budgetary controls").click()
        page.get_by_role("link", name="Set Assignments").click()
        page.get_by_role("button", name="Add Row").click()
        page.get_by_label("row.bindings.TransSetCode.").click()
        page.get_by_label("row.bindings.TransSetCode.").fill(datadictvalue["C_CODE"])
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Plan Settings").click()
        if datadictvalue["C_COST_QNTTY"] == 'Yes':
            page.get_by_text("Cost quantity").check()
        if datadictvalue["C_RAW_COST"] == 'Yes':
            page.get_by_text("Raw cost", exact=True).check()
        if datadictvalue["C_BRDND_COST"] == 'Yes':
            page.get_by_text("Burdened cost", exact=True).check()
        if datadictvalue["C_BRDND_COST"] != 'Yes':
            page.get_by_text("Burdened cost", exact=True).uncheck()
        if datadictvalue["C_RAW_COST_RATE"] == 'Yes':
            page.get_by_text("Raw cost rate").check()
        if datadictvalue["C_BRDND_COST_RATE"] == 'Yes':
            page.get_by_text("Burdened cost rate").check()
        if datadictvalue["C_BRDND_COST_RATE"] != 'Yes':
            page.get_by_text("Burdened cost rate").uncheck()
        page.get_by_label("Planning Level").click()
        page.get_by_label("Planning Level").select_option(datadictvalue["C_PLNNNG_LEVEL"])
        if datadictvalue["C_SPNSRD_PRJCT"] =='Financial Plan Type for Non-Sponsored Project':
            page.get_by_label("Calendar Type").click()
            page.get_by_label("Calendar Type").select_option(datadictvalue["C_CLNDR_TYPE"])
        page.get_by_label("Cost Rate Derivation Date Type").click()
        page.get_by_label("Cost Rate Derivation Date Type").select_option(datadictvalue["C_COST_RATE_DRVTN_DATE_TYPE"])
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Currency Settings").click()
        if datadictvalue["C_MNTN_MNL_SPRD_ON_DATE_CHNGS"] == 'Yes':
            page.get_by_text("Use same conversion attribute").click()
        page.get_by_label("Rate Type").click()
        page.get_by_label("Rate Type").fill(datadictvalue["C_RATE_TYPE"])
        page.get_by_label("Date Type").click()
        page.get_by_label("Date Type").select_option(datadictvalue["C_DATE_TYPE"])
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Rate Settings").click()
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Budgetary Control Settings").click()
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Generation Options").click()
        page.get_by_label("Generation Source").click()
        page.get_by_label("Generation Source").select_option(datadictvalue["C_GNRTN_SRC"])
        page.get_by_label("Generation Source").press("Tab")
        page.wait_for_timeout(2000)
        if datadictvalue["C_SRC_PLAN_VRSN"] != '' and 'Project plan type':
            page.get_by_role("row", name="Source Plan Version", exact=True).get_by_label("Source Plan Version").select_option(datadictvalue["C_SRC_PLAN_VRSN"])
        if datadictvalue["C_RTN_MNLLY_ADDED_BDGT_LINES"] == 'Yes':
            page.get_by_text("Retain manually added budget").check()
        if datadictvalue["C_RTN_MNLLY_ADDED_BDGT_LINES"] != 'Yes':
            page.get_by_text("Retain manually added budget").uncheck()
        if datadictvalue["C_RTN_OVRRD_RATES_FROM_SRC"] == 'Yes':
            page.get_by_text("Retain override rates from").check()
        if datadictvalue["C_RTN_OVRRD_RATES_FROM_SRC"] != 'Yes':
            page.get_by_text("Retain override rates from").uncheck()
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Reporting Options").click()
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Export Options").click()
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Export Options").click()
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Additional Information").click()
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save and Close").click()

        i = i + 1
    page.get_by_role("button", name="Done").click()

    # Validation
    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("PPM-Manage Financial Plan Type Executed Successfully")

    except Exception as e:
        print("PPM- Manage Financial Plan Type Executed UnSuccessfully")
    page.get_by_role("button", name="Done").click()

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, FIN_PLAN_TYPES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, FIN_PLAN_TYPES, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, FIN_PLAN_TYPES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
                                   0] + "_" + FIN_PLAN_TYPES)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
                0] + "_" + FIN_PLAN_TYPES + "_Results_" + datetime.now().strftime(
                "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
