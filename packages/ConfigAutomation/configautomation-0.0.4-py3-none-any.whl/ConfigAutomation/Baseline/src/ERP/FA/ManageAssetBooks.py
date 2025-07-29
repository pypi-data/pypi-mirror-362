from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    # Login to the instances

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    # Navigation to Manage Asset Books
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Asset Books")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Asset Books").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        # Create Asset Books
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Book Class").select_option(datadictvalue["C_BOOK_CLASS"])

        if datadictvalue["C_BOOK_CLASS"] == 'Tax':
            page.get_by_label("Associated Corporate Book").select_option(datadictvalue["C_ASSCTD_CRPRT_BOOK"])
        page.get_by_title("Search: Ledger").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Ledger").fill(datadictvalue["C_LDGR"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LDGR"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Depreciation Calendar").click()
        page.get_by_label("Depreciation Calendar").select_option(datadictvalue["C_DPRCTN_CLNDR"])
        # page.get_by_label("Prorate Calendar").select_option(datadictvalue["C_PRRT_CLNDR"])
        page.get_by_label("Current Period").click()
        page.get_by_label("Current Period").fill(datadictvalue["C_CRRNT_PRD"])
        page.get_by_label("Divide Depreciation").select_option(datadictvalue["C_DVD_DPRCTN"])

        if datadictvalue["C_DPRCT_IF_RTRD_IN_THE_FIRST_YEAR"] == 'Yes':
            if not page.get_by_text("Depreciate if retired in the").is_checked():
                page.get_by_text("Depreciate if retired in the").click()
        if datadictvalue["C_DPRCT_IF_RTRD_IN_THE_FIRST_YEAR"] == 'No':
            if page.get_by_text("Depreciate if retired in the").is_checked():
                page.get_by_text("Depreciate if retired in the").click()


        if datadictvalue["C_ALLOW_AMRTZD_CHNGS"] == 'Yes':
            page.get_by_text("Allow amortized changes").click()
        if datadictvalue["C_ALLOW_COST_SIGN_CHNGS"] == 'Yes':
            page.get_by_text("Allow cost sign changes").click()
        if datadictvalue["C_ALLOW_IMPRMNT"] == 'Yes':
            page.get_by_text("Allow impairment").click()
        if datadictvalue["C_ALLOW_LDGR_PSTNG"] == 'Yes':
            page.get_by_text("Allow ledger posting").click()
        if datadictvalue["C_ALLOW_PHYSCL_INVNTRY"] == 'Yes':
            page.get_by_text("Allow physical inventory").click()
        if datadictvalue["C_ALLOW_LSD_ASSET"] == 'Yes':
            page.get_by_text("Allow leased assets").click()
        if datadictvalue["C_USE_NBV_THRSHLD_FOR_DPRCTN"] == 'Yes':
            page.get_by_text("Use NBV threshold for").click()

        page.get_by_label("Capital Gain Threshold Years").fill(datadictvalue["C_CPTL_GAIN_THRSHLD_YEARS"])
        page.get_by_label("Months").fill(datadictvalue["C_CPTL_GAIN_THRSHLD_MNTHS"])
        page.locator("//label[text()='Inactive On']//following::input[1]").fill(datadictvalue["C_INCTV_ON"])
        page.get_by_label("Annual Depreciation Rounding").select_option(datadictvalue["C_ANNL_DPRCTN_RNDNG"])
        # page.get_by_label("Context Value").select_option(datadictvalue[""])

        # Accounts
        page.get_by_label("Account Defaults").fill(datadictvalue["C_ACCNT_DFLTS"])
        page.get_by_label("Net Book Value Retired Gain").fill(str(datadictvalue["C_NET_BOOK_VALUE_RTRD_GAIN"]))
        page.get_by_label("Net Book Value Retired Loss").fill(str(datadictvalue["C_NET_BOOK_VALUE_RTRD_GAIN"]))
        page.get_by_label("Proceeds of Sale Gain").fill(str(datadictvalue["C_PRCDS_OF_SALE_GAIN"]))
        page.get_by_label("Proceeds of Sale Loss").fill(str(datadictvalue["C_PRCDS_OF_SALE_LOSS"]))
        page.get_by_label("Proceeds of Sale Clearing").fill(str(datadictvalue["C_PRCDS_OF_SALE_CLRNG"]))
        page.get_by_label("Cost of Removal Gain").fill(str(datadictvalue["C_COST_OF_RMVL_GAIN"]))
        page.get_by_label("Cost of Removal Loss").fill(str(datadictvalue["C_COST_OF_RMVL_LOSS"]))
        page.get_by_label("Cost of Removal Clearing").fill(str(datadictvalue["C_COST_OF_RMVL_CLRNG"]))
        page.get_by_label("Deferred Depreciation Expense").fill(str(datadictvalue["C_DFRRD_DPRCTN_EXPNS"]))
        page.get_by_label("Deferred Depreciation Reserve").fill(str(datadictvalue["C_DFRRD_DPRCTN_RSRV"]))
        # page.get_by_label("Nonsale Gain").fill(datadictvalue[""])

        page.get_by_role("link", name="Invoice Rules").click()
        if datadictvalue["C_USE_PYBLS_INVC_DATE_AS_DATE_PLCD_IN_SRVC"] == 'Yes':
            page.get_by_text("Use Payables invoice date as date placed in service").check()
        if datadictvalue["C_USE_PYBLS_INVC_DATE_AS_DATE_PLCD_IN_SRVC"] == 'No' or '':
            page.get_by_text("Use Payables invoice date as date placed in service").uncheck()

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        #Validation

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Asset Books Saved Successfully")

        except Exception as e:
            print("Asset Books not Saved")

        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_ASSET_BOOK):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_ASSET_BOOK, PRCS_DIR_PATH + FA_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + FA_WORKBOOK, MANAGE_ASSET_BOOK)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANAGE_ASSET_BOOK)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[
            0] + "_" + MANAGE_ASSET_BOOK + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
