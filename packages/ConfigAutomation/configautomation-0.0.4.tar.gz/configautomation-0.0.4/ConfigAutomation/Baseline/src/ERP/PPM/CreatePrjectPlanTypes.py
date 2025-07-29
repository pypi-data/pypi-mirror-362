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
    page.get_by_role("textbox").fill("Manage Project Plan Types")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Project Plan Types", exact=True).click()

    #Create Planning and Billing Resource Breakdown Structures
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Name").click()
        page.get_by_role("textbox", name="Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(1000)
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(1000)
        # page.get_by_role("row", name="*From Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"])
        page.locator("//label[text()='From Date']//following::input[1]").first.fill(datadictvalue["C_FROM_DATE"])
        if datadictvalue["C_TO_DATE"] != '':
            # page.get_by_role("row", name="To Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"])
            page.locator("//label[text()='To Date']//following::input[1]").first.fill(datadictvalue["C_TO_DATE"].strftime('%m/%d/%y'))

        page.get_by_role("heading", name="Setup Options").click()
        if datadictvalue["C_USE_THIRD_PARTY_SFTWR_FOR_SCHDLNG"] == 'Yes':
            page.get_by_text("Use third-party software for").click()
        if datadictvalue["C_ENBL_PLNNNG_IN_MLTPL_TRNSCTN_CRRNCS"] == 'Yes':
            page.get_by_text("Enable planning in multiple").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Add Row").click()
        page.get_by_label("row.bindings.TransSetCode.").click()
        page.get_by_label("row.bindings.TransSetCode.").fill(datadictvalue["C_CODE"])
        page.wait_for_timeout(3000)

        page.get_by_role("link", name="Plan Settings").click()
        if datadictvalue["C_ENBL_COSTS_FOR_PRJCT_PLAN"] == 'Yes':
            page.get_by_text("Enable costs for project plan").click()
        if datadictvalue["C_SET_UNPLNND_ASSGNMNTS_AS_PLNND_ASSGNMNTS"] == 'Yes':
            page.get_by_text("Set unplanned assignments as").click()
        page.get_by_label("Calendar Type").select_option(datadictvalue["C_CLNDR_TYPE"])
        page.get_by_label("Rate Derivation Date Type").select_option(datadictvalue["C_RATE_DRVTN_DATE_TYPE"])
        page.wait_for_timeout(3000)

        page.get_by_role("link", name="Task Settings").click()
        if datadictvalue["C_USE_TASK_PLNND_DATES_AS_TASK_ASSGNMNT_DATES"] == 'Yes':
            page.get_by_text("Use task planned dates as").click()
        if datadictvalue["C_SYNCHRNZ_TASK_TRNSCTN_DATES_WITH_PLNND_DATES"] == 'Yes':
            page.get_by_text("Synchronize task transaction").click()
        if datadictvalue["C_ATMTCLLY_ROLL_UP_TASK_PLNND_DATS"] == 'Yes':
            page.get_by_text("Automatically roll up task").click()
        page.get_by_label("Date Adjustment Buffer in Days").fill(str(datadictvalue["C_DATE_DJSTMNT_BFFR_IN_DAYS"]))
        page.wait_for_timeout(3000)

        page.get_by_role("link", name="Currency Settings").click()
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Rate Settings").click()
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Progress Settings").click()
        page.get_by_label("Physical Percent Complete Calculation Method").select_option(datadictvalue["C_PHYSCL_PRCNT_CMPLT_CLCLTN_MTHD"])
        page.get_by_label("ETC Method").select_option(datadictvalue["C_ETC_MTHD"])
        if datadictvalue["C_ALLW_NGTV_ETC_CLCLTN"] == 'Yes':
            page.get_by_text("Allow negative ETC calculation").click()
        if datadictvalue["C_UPDT_PLNND_QNTTY_WITH_EAC_QNTTY"] == 'Yes':
            page.get_by_text("Update planned quantity with").click()
        if datadictvalue["C_ATMTCLLY_GNRT_FRCST_VRSN"] == 'Yes':
            page.get_by_text("Automatically generate").click()
        page.get_by_label("Primary Physical Percent").select_option(datadictvalue["C_PRMRY_PHYSCL_PRCNT_CMPLT_BASIS"])
        page.wait_for_timeout(3000)

        page.get_by_role("link", name="Budget Generation Options").click()
        if datadictvalue["C_GNRT_BDGT_VRSN_WHEN_STTNG_BSLN_FOR_PRJCT_PLAN"] == 'Yes':
            page.get_by_text("Generate budget version when").click()
        page.get_by_label("Financial Plan Type").click()
        page.get_by_label("Financial Plan Type").select_option(datadictvalue["C_FNNCL_PLAN_TYPE"])
        if datadictvalue["C_ATMTCLLY_DSGNT_BDGT_VRSN_AS_BSLN"] == 'Yes':
            page.get_by_text("Automatically designate").click()
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Additional Information").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()

        i = i + 1
    page.get_by_role("button", name="Done").click()

    # Validation
    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("PPM-Manage Project Plan Type Executed Successfully")

    except Exception as e:
        print("PPM- Manage Project Plan Type Executed UnSuccessfully")
    page.get_by_role("button", name="Done").click()

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJ_PLAN_TYPES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJ_PLAN_TYPES, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJ_PLAN_TYPES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
                                   0] + "_" + PRJ_PLAN_TYPES)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
                0] + "_" + PRJ_PLAN_TYPES + "_Results_" + datetime.now().strftime(
                "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
