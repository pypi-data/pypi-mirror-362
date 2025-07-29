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
    page.get_by_role("textbox").fill("Manage Project Transaction Sources")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Project Transaction Sources", exact=True).click()

    i = 0
    PrevName = ''
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)


        j = 0
        while j < rowcount:

            datadictvalue = datadict[j]

            if datadictvalue["C_TRNSCTN_SRC"] != PrevName or '':
            # Enter Transaction source
                page.get_by_role("button", name="Create").first.click()
                page.wait_for_timeout(2000)
                page.get_by_label("Transaction Source").fill(datadictvalue["C_TRNSCTN_SRC"])
                page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
                page.get_by_label("Processing Set Size").clear()
                page.get_by_label("Processing Set Size").fill(str(datadictvalue["C_PRCSSNG_SET_SIZE"]))
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(2000)
                PrevName = datadictvalue["C_TRNSCTN_SRC"]

            #Document
            if PrevName == datadictvalue["C_TRNSCTN_SRC"]:

                if datadictvalue["C_PCD_DCMNT"] != "":
                    page.wait_for_timeout(2000)
                page.get_by_role("button", name="Create").nth(1).click()
                page.wait_for_timeout(3000)
                page.get_by_label("Document", exact=True).fill(datadictvalue["C_PCD_DCMNT"])
                page.get_by_role("textbox", name="Description").fill(datadictvalue["C_PCD_DSCRPTN"])
                page.get_by_placeholder("m/d/yy").first.fill(datadictvalue["C_FROM_DATE"])
                if datadictvalue["C_TO_DATE"] != '':
                    page.get_by_placeholder("m/d/yy").nth(1).fill(datadictvalue["C_TO_DATE"])
                if datadictvalue["C_CMMTMNT_SRC"] == 'Yes':
                    page.get_by_text("Commitment source", exact=True).check()
                    page.wait_for_timeout(1000)
                    page.get_by_label("Commitment Type").select_option(datadictvalue["C_CMMTMNT_TYPE"])

            #Import options
                page.wait_for_timeout(2000)
                # if page.get_by_text("Import raw cost amounts").is_enabled():
                if datadictvalue["C_IMPRT_RAW_COST_AMNTS"] == 'Yes':
                    page.locator("//label[text()='Import raw cost amounts']").check()
                elif datadictvalue["C_IMPRT_RAW_COST_AMNTS"] == 'No' or '':
                    page.locator("//label[text()='Import raw cost amounts']").uncheck()
                if page.locator("//label[text()='Allow duplicate reference']").is_enabled():
                    if datadictvalue["C_ALLW_DPLCT_RFRNC"] == 'Yes':
                        page.locator("//label[text()='Allow duplicate reference']").check()
                if page.locator("//label[text()='Revalidate during import']").is_enabled():
                    if datadictvalue["C_RVLDT_DRNG_IMPRT"]== 'Yes':
                        page.locator("//label[text()='Revalidate during import']").check()
                if page.locator("//label[text()='Import burdened cost amounts']").is_enabled():
                    if datadictvalue["C_IMPRT_BRDND_COST_AMNTS"] == 'Yes':
                        page.locator("//label[text()='Import burdened cost amounts']").check()
                if page.locator("//label[text()='Allow override of person organization']").is_enabled():
                    if datadictvalue["C_ALLW_OVRRD_OF_PRSN_ORGNZTN"] == 'Yes':
                        page.locator("//label[text()='Allow override of person organization']").check()
            # if page.locator("//label[text()='Requires expenditure batch approval']").is_enabled():
            #     if datadictvalue["C_RQRS_EXPNDTR_BATCH_APPRVL"] == 'Yes':
            #         page.locator("//label[text()='Requires expenditure batch approval']").check()
            # if page.locator("//label[text()='Allow transactions for inactive or suspended person assignments']").is_enabled():
            #     if datadictvalue["C_ALLW_TRNSCTNS_FOR_INCTV_OR_SSPNDD_PRSN_ASSGNMNTS"] == 'Yes':
            #         page.locator("//label[text()='Allow transactions for inactive or suspended person assignments']").check()

            #Accounting options
                if page.locator("//label[text()='Accounted in Source Application']//following::select").is_enabled():
                    page.locator("//label[text()='Accounted in Source Application']//following::select").select_option(datadictvalue["C_ACCNTD_IN_SRC_APPLCTN"])
                if page.locator("//label[text()='Create raw cost accounting journal entries']").is_enabled():
                    if datadictvalue["C_CRT_RAW_COST_ACCNTNG_JRNL_ENTRS"] == 'Yes':
                        page.locator("//label[text()='Create raw cost accounting journal entries']").check()
                if page.locator("//label[text()='Create adjustment accounting journal entries']").is_enabled():
                    if datadictvalue[""] == 'Yes':
                        page.locator("//label[text()='Create adjustment accounting journal entries']").check()
                if page.locator("//label[text()='Import accounted cost when project periods are closed']").is_enabled():
                    if datadictvalue["C_CRT_ADJSTMNT_ACCNTNG_JRNL_ENTRS"] == 'Yes':
                        page.locator("//label[text()='Import accounted cost when project periods are closed']").click()
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(2000)

            #Document Entries

            if datadictvalue["C_NAME"] != '':
                page.get_by_role("button", name="Create").nth(2).click()
                page.get_by_label("Name").fill(datadictvalue["C_NAME"])
                page.get_by_role("textbox", name="Description").fill(datadictvalue["C_DE_DSCRPTN"])
                page.wait_for_timeout(2000)
                page.get_by_label("Expenditure Type Class").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Expenditure Type Class").select_option(datadictvalue["C_EXPNDTR_TYPE_CLSS"])
                # if datadictvalue["C_EXPNDTR_TYPE_CLSS"]=='Burden Transaction':
                #    page.get_by_label("Expenditure Type Class").select_option('1')
                # page.locator("//div[text()='Payroll: Edit Document Entry']//following::label[text()='Expenditure Type Class']").select_option(datadictvalue["C_EXPNDTR_TYPE_CLSS"])
                if page.get_by_text("Allow adjustments", exact=True).is_enabled():
                    if datadictvalue["C_ALLW_DJSTMNTS"] == 'Yes':
                        page.get_by_text("Allow adjustments", exact=True).check()
                if page.get_by_text("Allow reversals", exact=True).is_enabled():
                    if datadictvalue["C_ALLW_DJSTMNTS"] == 'Yes':
                        page.get_by_text("Allow reversals", exact=True).check()
                if page.get_by_text("Allow modifications to unprocessed transactions", exact=True).is_enabled():
                    if datadictvalue["C_ALLW_MDFCTNS_TO_UNPRCSSD_TRNSCTNS"] == 'Yes':
                        page.get_by_text("Allow modifications to unprocessed transactions", exact=True).check()
                if page.get_by_text("Process cross-charge transactions", exact=True).is_enabled():
                    if datadictvalue["C_PRCSS_CROSS_CHRG_TRNSCTNS"] == 'Yes':
                        page.get_by_text("Process cross-charge transactions", exact=True).check()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Save and Close").click()
                j = j + 1

            page.wait_for_timeout(2000)
            i = i + 1
            page.wait_for_timeout(2000)


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJCT_TRANS_SOURCES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJCT_TRANS_SOURCES, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJCT_TRANS_SOURCES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + PRJCT_TRANS_SOURCES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + PRJCT_TRANS_SOURCES + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




