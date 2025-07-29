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
    page.get_by_role("textbox").fill("Manage Policies by Expense Category")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Policies by Expense Category").click()

    i = 0
    while i < rowcount:

        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_title("Create Policy").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text("Miscellaneous", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_label("Policy Name").click()
        page.get_by_label("Policy Name").fill(datadictvalue["C_PLCY_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        #Miscellaneous Eligibility Rule
        if datadictvalue["C_MNMM_NMBR_OF_DAYS_FOR_MSCLLNS_EXPNS_RMBRSMNT"]:
            page.get_by_text("Minimum Number of Days for Miscellaneous Expense Reimbursement").check()
            page.wait_for_timeout(1000)
            page.get_by_label("Days", exact=True).fill(str(datadictvalue["C_DAYS"]))
            if datadictvalue["C_BASED_ON_NMBR_OF_DAYS_IN_PRNT_LINE_DRNG_ITMZTN"] == 'Yes':
                page.get_by_text("Based on Number of Days in Parent Line During Itemization").check()

        #Rate Type
        page.get_by_text(datadictvalue["C_RATE_TYPE"], exact=True).click()
        page.wait_for_timeout(2000)

        #Rate Definition
        if datadictvalue["C_RATE_TYPE"] == 'Rate limit' or "Percentage reimbursement with upper limit":
            if datadictvalue["C_SNGL_INSTNC_LIMIT"] == 'Yes':
                page.get_by_text("Single instance limit").check()
            if datadictvalue["C_SNGL_INSTNC_LIMIT"] == 'No':
                page.get_by_text("Single instance limit").uncheck()
            if datadictvalue["C_DAILY_LIMIT"] == 'Yes':
                page.get_by_text("Daily sum limit").check()
            if datadictvalue["C_DAILY_LIMIT"] == 'No':
                page.get_by_text("Daily sum limit").uncheck()
            if datadictvalue["C_MNTHLY_LIMIT"] == 'Yes':
                page.get_by_text("Monthly limit").check()
            if datadictvalue["C_MNTHLY_LIMIT"] == 'No':
                page.get_by_text("Monthly limit").uncheck()
            if datadictvalue["C_YRLY_LIMIT"] == 'Yes':
                page.get_by_text("Yearly limit").check()
                page.wait_for_timeout(1000)
                page.get_by_label("Period Start Month").click()
                page.get_by_label("Period Start Month").select_option(datadictvalue["C_PRD_START_MONTH"])
                page.wait_for_timeout(1000)
                page.get_by_label("Period Start Day").fill(str(datadictvalue["C_PRD_START_DAY"]))
            if datadictvalue["C_YRLY_LIMIT"] == 'No':
                page.get_by_text("Yearly limit").uncheck()
            if datadictvalue["C_LFTM_LIMIT"] == 'Yes':
                page.get_by_text("Lifetime limit").check()
            if datadictvalue["C_LFTM_LIMIT"] == 'No':
                page.get_by_text("Lifetime limit").uncheck()

            #Select the Rate Currency
            if datadictvalue["C_MLTPL_CRRNCY"] == 'Yes':
                page.get_by_text("Multiple currencies").click()
            if datadictvalue["C_SNGL_CRRNCY"] == 'Yes':
                page.get_by_text("Single currency").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Currency", exact=True).select_option(datadictvalue["C_CRRNCY"])

        #Rate Determinants

        if datadictvalue["C_ROLE"] == 'Yes':
            page.get_by_text("Role", exact=True).check()
            page.wait_for_timeout(2000)
            page.get_by_label("Role Type").select_option(datadictvalue["C_ROLE_TYPE"])
        if datadictvalue["C_ROLE"] == 'No':
            page.get_by_text("Role", exact=True).uncheck()
        if datadictvalue["C_LCTN"] == 'Yes':
            page.get_by_text("Location", exact=True).check()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_GGRPHCL_LCTNS"], exact=True).click()
            if datadictvalue["C_GGRPHCL_LCTNS"] =='Zone':
                page.wait_for_timeout(2000)
                page.get_by_label("Zone Type").select_option(datadictvalue["C_ZONE_TYPE"])
        if datadictvalue["C_LCTN"] == 'No':
            page.get_by_text("Location", exact=True).uncheck()
        if datadictvalue["C_GNDR"] == 'Yes':
            page.get_by_text("Gender").check()
        if datadictvalue["C_GNDR"] == 'No':
            page.get_by_text("Gender").uncheck()

        # Policy Enforcement
        page.get_by_text(datadictvalue["C_RMBRS_UPPER_LIMIT_WHEN_EXPNS_EXCDS_DFND_RATE"]).click()
        page.wait_for_timeout(2000)
        if datadictvalue[
            "C_RMBRS_UPPER_LIMIT_WHEN_EXPNS_EXCDS_DFND_RATE"] == 'Generate policy violation when expense exceeds defined rate':
            page.wait_for_timeout(2000)
            if datadictvalue["C_PLCY_VLTN_WRNNG"] == 'Yes':
                page.get_by_text("Policy violation warning").check()
                page.wait_for_timeout(3000)
                page.get_by_label("Warning Tolerance Percentage").fill(str(datadictvalue["C_WRNNG_TLRNC_PRCNTG"]))
                if datadictvalue["C_DSPLY_WRNNG_TO_USER"] == 'Yes':
                    page.get_by_text("Display warning to user").check()
                if datadictvalue["C_DSPLY_WRNNG_TO_USER"] == 'No':
                    page.get_by_text("Display warning to user").uncheck()
                if datadictvalue["C_PRVNT_RPRT_SBMSSN"] == 'Yes':
                    page.get_by_text("Prevent report submission").check()
                    page.wait_for_timeout(3000)
                    page.get_by_label("Error Tolerance Percentage").fill(str(datadictvalue["C_ERROR_TLRNC_PRCNTG"]))

        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)

        # Enter the Rates

        if datadictvalue["C_RATE"] != '' and datadictvalue["C_ROLE"] != 'Yes' and datadictvalue["C_GNDR"] != 'Yes' and datadictvalue["C_LCTN"] != 'Yes':
            page.get_by_role("button", name="Create Rates").click()
            page.wait_for_timeout(2000)
            if page.get_by_role("textbox", name="Single instance limit").is_visible():
                page.get_by_role("textbox", name="Single instance limit").fill(str(datadictvalue["C_RATE"]))
            if page.get_by_role("textbox", name="Daily sum limit").is_visible():
                page.get_by_role("textbox", name="Daily sum limit").fill(str(datadictvalue["C_RATE_DAILY_SUM_LIMIT"]))
            if page.get_by_role("textbox", name="Monthly limit").is_visible():
                page.get_by_role("textbox", name="Monthly limit").fill(str(datadictvalue["C_RATE_MNTHLY_LIMIT"]))
            if page.get_by_role("textbox", name="Yearly limit").is_visible():
                page.get_by_role("textbox", name="Yearly limit").fill(str(datadictvalue["C_RATE_YRLY_LIMIT"]))
            if page.get_by_role("textbox", name="Lifetime limit").is_visible():
                page.get_by_role("textbox", name="Lifetime limit").fill(str(datadictvalue["C_RATE_LIFETME_LIMIT"]))
            page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar Start Date Select Date",
                             exact=True).locator("input").nth(0).fill(datadictvalue["C_START_DATE"].strftime("%m/%d/%Y"))
            if datadictvalue["C_END_DATE"] != '':
                page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar End Date Select Date",
                                 exact=True).locator("input").nth(0).fill(datadictvalue["C_END_DATE"].strftime("%m/%d/%Y"))
            page.wait_for_timeout(1000)
            page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)

            # Save the data

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        if page.get_by_role("button", name="Yes").is_visible():
            page.get_by_role("button", name="Yes").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Miscellaneous Expense Policy Saved Successfully")
            datadictvalue["RowStatus"] = "Miscellaneous Expense Policy saved successfully"

        except Exception as e:
            print("Miscellaneous Expense Policy not saved")
            datadictvalue["RowStatus"] = "Miscellaneous Expense Policy not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, MISC_EXP_POLICY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, MISC_EXP_POLICY, PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, MISC_EXP_POLICY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[0] + "_" + MISC_EXP_POLICY)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + MISC_EXP_POLICY + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))