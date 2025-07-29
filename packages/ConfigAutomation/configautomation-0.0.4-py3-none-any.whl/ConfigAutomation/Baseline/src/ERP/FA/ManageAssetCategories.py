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
    page.wait_for_timeout(5000)

    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Asset Categories")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Asset Categories").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)
        #Create Category

        # page.get_by_label("Major Category").fill(datadictvalue["C_MJR_CTGRY"])
        if page.get_by_title("Search: Major").is_visible():
           page.get_by_title("Search: Major").click()
        if page.get_by_title("Search: Major Category").is_visible():
           page.get_by_title("Search: Major Category").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Value", exact=True).fill(datadictvalue["C_MJR_CTGRY"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("//span[text()='Value']//following::span[text()='"+datadictvalue["C_MJR_CTGRY"]+"'][1]").click()
        page.get_by_role("button", name="OK", exact=True).click()
        page.wait_for_timeout(2000)
        if page.get_by_title("Search: Minor").is_visible():
            page.get_by_title("Search: Minor").click()
        if page.get_by_title("Search: Minor Category").is_visible():
            page.get_by_title("Search: Minor Category").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Value", exact=True).fill(datadictvalue["C_MNR_CTGRY"])
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("cell", name=datadictvalue["C_MNR_CTGRY"], exact=True).nth(1).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="OK", exact=True).click()
        page.wait_for_timeout(3000)
        if page.get_by_title("Search: SubMinor").is_visible():
            page.get_by_title("Search: SubMinor").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Value", exact=True).fill(datadictvalue["C_SGMNT3"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_SGMNT3"], exact=True).first.click()
            page.get_by_role("button", name="OK", exact=True).click()
            page.wait_for_timeout(2000)
        #page.get_by_label("Minor Category").fill(datadictvalue["C_MNR_CTGRY"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        #page.get_by_label("Category Type").select_option(datadictvalue["C_CTGRY_TYPE"])
        page.get_by_label("Ownership").select_option(datadictvalue["C_OWNRSHP"])
        page.get_by_label("Property Type").select_option(datadictvalue["C_PRPTY_TYPE"])
        page.get_by_label("Property Class").select_option(datadictvalue["C_PRPTY_CLASS"])

        if datadictvalue["C_CPTLZD"] == 'Yes' :
            if not page.get_by_text("Capitalized").is_checked():
                page.get_by_text("Capitalized").click()
        elif datadictvalue["C_CPTLZD"] == 'No':
            if page.get_by_text("Capitalized").is_checked():
                page.get_by_text("Capitalized").click()

        if datadictvalue["C_ENBLD"] == 'Yes':
            if not page.get_by_text("Enabled").is_checked():
                page.get_by_text("Enabled").click()
        elif datadictvalue["C_ENBLD"] == 'No':
            if page.get_by_text("Enabled").is_checked():
                page.get_by_text("Enabled").click()

        if datadictvalue["C_IN_PHYSCL_INVNTRY"] == 'Yes':
            if not page.get_by_text("In physical inventory").is_checked():
                page.get_by_text("In physical inventory").click()
        elif datadictvalue["C_IN_PHYSCL_INVNTRY"] == 'No':
            if page.get_by_text("In physical inventory").is_checked():
                page.get_by_text("In physical inventory").click()
        if datadictvalue["C_CNTXT_VALUE"] != '':
            page.get_by_label("Context Value").select_option(datadictvalue["C_CNTXT_VALUE"])

        # Book
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(3000)
        page.get_by_label("Book", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_label("Book", exact=True).select_option(datadictvalue["C_BOOK"])
        page.wait_for_timeout(5000)

        # Navigation to Default Tab
        page.get_by_role("link", name="Accounts").click()
        page.wait_for_timeout(3000)

        #Accounting Rules
        page.get_by_label("Asset Cost").fill(datadictvalue["C_ASSET_COST"])
        page.get_by_label("Asset Clearing").fill(datadictvalue["C_ASSET_CLRNG"])
        page.get_by_label("Depreciation Expense", exact=True).fill(datadictvalue["C_DPRCTN_EXPNS"])
        page.get_by_label("Depreciation Reserve", exact=True).fill(datadictvalue["C_DPRCTN_RSRV"])
        page.get_by_label("Bonus Depreciation Expense").fill(datadictvalue["C_BONUS_DPRCTN_EXPNS"])
        page.get_by_label("Bonus Depreciation Reserve").fill(datadictvalue["C_BONUS_DPRCTN_RSRV"])
        page.get_by_label("CIP Cost").fill(datadictvalue["C_CIP_COST"])

        page.get_by_label("CIP Clearing").fill(datadictvalue["C_CIP_CLRNG"])
        page.get_by_label("Unplanned Depreciation Expense").fill(datadictvalue["C_UNPLNND_DPRCTN_EXPNS"])
        page.get_by_label("Impairment Expense").fill(datadictvalue["C_IMPRMNT_EXPNS"])
        page.get_by_label("Impairment Reserve").fill(datadictvalue["C_IMPRMNT_RSRV"])
        page.get_by_label("Revaluation Reserve", exact=True).fill(datadictvalue["C_RVLTN_RSRV"])
        page.get_by_label("Revaluation Reserve Amortization").fill(datadictvalue["C_RVLTN_RSRV_AMRTZN"])
        page.get_by_label("Revaluation Loss Expense").fill(datadictvalue["C_RVLTN_LOSS_EXPNS"])

        if datadictvalue["C_DFLT_DPRCTN_EXPNS_CMBNTN"] == 'Yes' :
            page.get_by_text("Default depreciation expense").click()

        # page.get_by_label("Statutory Category").fill(datadictvalue[""])
        # page.get_by_label("Statutory Subcategory").fill(datadictvalue[""])
        # page.get_by_role("cell", name="Default depreciation expense combination Statutory Category Search: Statutory Category Autocompletes on TAB Statutory Subcategory Search: Statutory Subcategory Autocompletes on TAB Context Value Regional Information", exact=True).get_by_label("Context Value").select_option(datadictvalue["C_ACCNT_CNTXT_VALUE"])
        # page.get_by_label("Regional Information").select_option(datadictvalue["C_RGNL_INFRMTN"])

        # Navigation to Default Tab
        page.get_by_role("link", name="Default Rules").click()
        page.wait_for_timeout(3000)


        page.get_by_role("button", name="Add Row").nth(1).click()
        page.get_by_role("cell", name="Context Value").nth(2).get_by_label("Context Value").first.select_option(datadictvalue["C_DFLT_CNTXT_VALUE"])

        if datadictvalue["C_DPRCT"] == 'Yes':
            if not page.get_by_text("Depreciate").is_checked():
                page.get_by_text("Depreciate").click()
        elif datadictvalue["C_DPRCT"] == 'No':
            if page.get_by_text("Depreciate").is_checked():
                page.get_by_text("Depreciate").click()

        page.wait_for_timeout(3000)
        page.get_by_title("Depreciation Method").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Name").fill(datadictvalue["C_MTHD"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name=datadictvalue["C_MTHD"], exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="OK", exact=True).click()
        page.wait_for_timeout(2000)

        page.get_by_label("Life in Years").first.select_option(str(datadictvalue["C_LIFE_IN_YEARS"]))
        page.wait_for_timeout(1000)
        page.get_by_label("Life in Months").first.select_option(str(datadictvalue["C_LIFE_IN_MNTHS"]))
        page.wait_for_timeout(1000)
        #page.locator("//select[contains(@name,'lifeInMonths')]").select_option(datadictvalue["C_LIFE_IN_MNTHS"])
        page.get_by_label("Depreciation Limit Type").select_option(datadictvalue["C_DPRCTN_LIMIT_TYPE"])
        page.get_by_label("Bonus Rule").select_option(datadictvalue["C_BONUS_RULE"])
        page.get_by_label("Prorate Convention", exact=True).select_option(datadictvalue["C_PRRT_CNVNTN"])
        page.wait_for_timeout(1000)
        page.get_by_label("Retirement Convention").select_option(datadictvalue["C_RTRMNT_CNVNTN"])
        page.wait_for_timeout(1000)
        # page.get_by_label("Default Salvage Percent").fill(datadictvalue["C_DFLT_SLVG_PRCNT"])
        # page.get_by_label("Capital Gains Threshold Years").fill(datadictvalue["C_CPTL_GAINS_THRSHLD_YEARS"])
        # page.get_by_role("cell", name="Capital Gains Threshold Years Months", exact=True).get_by_label("Months").fill(datadictvalue["C_CPTL_GAIN_THRSHLD_MNTH"])
        # page.get_by_label("Price Index").select_option(datadictvalue["C_PRICE_INDEX"])
        #
        # if datadictvalue["C_MASS_PRPRTY_ELGBL"] == 'Yes':
        #     page.get_by_text("Mass property eligible").click()
        #
        # #Default Subcomponent Rules
        # page.get_by_label("Rule", exact=True).select_option(datadictvalue["C_RULE"])
        # page.get_by_label("Minimum Years").fill(datadictvalue["C_MNMM_YEARS"])
        # page.get_by_role("cell", name="Minimum Years Months", exact=True).get_by_label("Months").fill(datadictvalue["C_MNTHS"])
        #
        # page.get_by_label("Recognize Gain or Loss").select_option(datadictvalue["C_RCGNZ_GAIN_OR_LOSS"])
        # page.get_by_label("Terminal Gain or Loss").select_option(datadictvalue["C_TRMNL_GAIN_OR_LOSS"])
        #
        # if datadictvalue["C_RCPTR_EXCSS_RSRV"] == 'Yes':
        #     page.get_by_text("Recapture excess reserve").click()
        # if datadictvalue["C_LIMIT_NET_PRCDS_TO_COST"] == 'Yes':
        #     page.get_by_text("Limit net proceeds to cost").click()
        #
        # page.get_by_label("Tracking Method").select_option(datadictvalue["C_TRCKNG_MTHD"])
        # page.get_by_label("Group Asset Number").fill(datadictvalue["C_GROUP_ASSET_NMBR"])

        #page.get_by_role("button", name="Cancel").click()
        page.get_by_role("button", name="Save and Close").click()


        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Validation

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Expense Asset Category Saved Successfully")

        except Exception as e:
            print("Expense Asset Category not Saved")

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_ASSET_CATEGORIES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_ASSET_CATEGORIES, PRCS_DIR_PATH + FA_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + FA_WORKBOOK, MANAGE_ASSET_CATEGORIES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANAGE_ASSET_CATEGORIES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[
            0] + "_" + MANAGE_ASSET_CATEGORIES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))