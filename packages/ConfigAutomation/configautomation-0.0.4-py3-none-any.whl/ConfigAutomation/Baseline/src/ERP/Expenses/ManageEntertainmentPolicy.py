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
    page.wait_for_timeout(15000)
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
        page.locator("[id=\"__af_Z_window\"]").get_by_text("Entertainment", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_label("Policy Name").click()
        page.get_by_label("Policy Name").fill(datadictvalue["C_PLCY_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        #select the attendee informations

        if datadictvalue["C_ATTND_INFRMTN"] == 'Capture number of attendees for expense lines above the specified amount':
            page.get_by_text("Capture number of attendees for expense lines above the specified amount").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Policy Amount").fill(str(datadictvalue["C_PLCY_AMT"]))
            page.get_by_role("row", name="Capture number of attendees for expense lines above the specified amount Policy Amount Policy Amount Currency", exact=True).get_by_label("Currency").select_option(datadictvalue["C_PLCY_AMNT_CRRNCY"])

        if datadictvalue["C_ATTND_INFRMTN"] == 'Capture attendee information':
            page.get_by_text("Capture attendee information").click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_DSPLY_EMPLY_ATTND_INFRMTN"] == 'Yes':
                page.get_by_text("Display employee attendee").check()
                # page.get_by_role("row", name="Display employee attendee information Attendee Amount Require at least one employee as attendee", exact=True).get_by_label("Attendee Amount").select_option(datadictvalue["C_ATTND_AMNT"])
                page.locator("//label[text()='Attendee Amount']//following::select[1]").nth(0).select_option(datadictvalue["C_ATTND_AMNT"])
                if datadictvalue["C_RQR_AT_LEAST_ONE_EMPLY_AS_ATTND"] == 'Yes':
                    page.get_by_text("Require at least one employee").check()
            if datadictvalue["C_DSPLY_EMPLY_ATTND_INFRMTN"] == 'No':
                page.get_by_text("Display employee attendee").uncheck()
            if datadictvalue["C_DSPLY_NNMPLY_ATTND_INFRMTN"] == 'Yes':
                page.get_by_text("Display nonemployee attendee").check()
                page.wait_for_timeout(2000)
                page.get_by_label("Attendee Type", exact=True).select_option(datadictvalue["C_ATTND_TYPE"])
                # page.get_by_role("cell", name="Attendee Type Attendee Amount Job Title", exact=True).get_by_label("Attendee Amount").select_option(datadictvalue["C_NNMPLY_ATTND_AMNT"])
                page.locator("//label[text()='Attendee Amount']//following::select[1]").nth(1).select_option(datadictvalue["C_NNMPLY_ATTND_AMNT"])
                page.get_by_label("Job Title").select_option(datadictvalue["C_JOB_TITLE"])
                if datadictvalue["C_ENBL_NNMPLY_CRTN"] == 'Yes':
                    page.get_by_text("Enable nonemployee creation").check()
                if datadictvalue["C_ENBL_NNMPLY_CRTN"] == 'No':
                    page.get_by_text("Enable nonemployee creation").uncheck()
                if datadictvalue["C_RQR_ATLST_ONE_NNMPLY_AS_ATTND"] == 'Yes':
                    page.get_by_text("Require at least one nonemployee as attendee").check()
                if datadictvalue["C_RQR_ATLST_ONE_NNMPLY_AS_ATTND"] == 'No':
                    page.get_by_text("Require at least one nonemployee as attendee").uncheck()
            if datadictvalue["C_DSPLY_NNMPLY_ATTND_INFRMTN"] == 'No':
                page.get_by_text("Display nonemployee attendee").uncheck()

            #Enter the Rate Definition

            if datadictvalue["C_ENBL_RATE_LIMIT"] == 'Yes':
                page.get_by_text("Enable rate limit").check()
                page.wait_for_timeout(2000)
                if datadictvalue["C_SNGL_INSTNC_LIMIT"] == 'Yes':
                    page.get_by_text("Single instance limit").check()
                if datadictvalue["C_SNGL_INSTNC_LIMIT"] == 'No':
                    page.get_by_text("Single instance limit").uncheck()
                if datadictvalue["C_DAILY_SUM_LIMIT"] == 'Yes':
                    page.get_by_text("Daily sum limit").check()
                if datadictvalue["C_DAILY_SUM_LIMIT"] == 'No':
                    page.get_by_text("Daily sum limit").uncheck()
                if datadictvalue["C_YRLY_LIMIT"] == 'Yes':
                    page.get_by_text("Yearly limit").check()
                    page.wait_for_timeout(1000)
                    page.get_by_label("Period Start Month").click()
                    page.get_by_label("Period Start Month").select_option(datadictvalue["C_PRD_START_MONTH"])
                    page.wait_for_timeout(1000)
                    page.get_by_label("Period Start Day").fill(str(datadictvalue["C_PRD_START_DAY"]))
                if datadictvalue["C_YRLY_LIMIT"] == 'No':
                    page.get_by_text("Yearly limit").uncheck()

                #Select the Rate Currency
                if datadictvalue["C_MLTPL_CRRNCY"] == 'Yes':
                    page.get_by_text("Multiple currencies").click()
                if datadictvalue["C_SNGL_CRRNCY"] == 'Yes':
                    page.get_by_text("Single currency").click()
                    page.get_by_label("Currency", exact=True).nth(1).select_option(datadictvalue["C_CRRNCY"])

            #Select the Rate Determinants

            if datadictvalue["C_ATTND_AMNT"] == 'Required' and datadictvalue["C_RQR_AT_LEAST_ONE_EMPLY_AS_ATTND"] =='Yes':
                if datadictvalue["C_EMPLY"] == 'Yes':
                    page.get_by_text("Employee", exact=True).check()
                    page.wait_for_timeout(1000)
                    if datadictvalue["C_ROLE"] == 'Yes':
                        page.get_by_text("Role", exact=True).check()
                        page.wait_for_timeout(1000)
                        page.get_by_label("Role Type").select_option(datadictvalue["C_ROLE_TYPE"])
                if datadictvalue["C_EMPLY"] == 'No':
                    page.get_by_text("Employee", exact=True).uncheck()
            if datadictvalue["C_ATTND_TYPE"] == 'Required' and datadictvalue["C_NNMPLY_ATTND_AMNT"] == 'Required' and datadictvalue["C_RQR_ATLST_ONE_NNMPLY_AS_ATTND"] == 'Yes':
                if datadictvalue["C_NON_EMPLY_ATTND_TYPES"] == 'Yes':
                    page.get_by_text("Nonemployee Attendee Types").check()

            # Policy Enforcement
            page.get_by_text(datadictvalue["C_RMBRS_UPPR_LIMIT_WHEN_EXPNS_EXCDS_DFND_RATE"]).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_RMBRS_UPPR_LIMIT_WHEN_EXPNS_EXCDS_DFND_RATE"] == 'Generate policy violation when expense exceeds defined rate':
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

            #Enter the Rates

            if datadictvalue["C_RATE"] != '':
                page.get_by_role("button", name="Create Rates").click()
                page.wait_for_timeout(2000)
                page.get_by_role("textbox", name="Single instance limit").fill(str(datadictvalue["C_RATE"]))
                if page.get_by_role("textbox", name="Daily sum limit").is_visible():
                    page.get_by_role("textbox", name="Daily sum limit").fill(str(datadictvalue["C_RATE_DAILY_SUM_LIMIT"]))
                if page.get_by_role("textbox", name="Yearly limit").is_visible():
                    page.get_by_role("textbox", name="Yearly limit").fill(str(datadictvalue["C_RATE_YRLY_LIMIT"]))
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
            print("Entertainment Expense Policy Saved Successfully")
            datadictvalue["RowStatus"] = "Entertainment Expense Policy saved successfully"

        except Exception as e:
            print("Entertainment Expense Policy not saved")
            datadictvalue["RowStatus"] = "Entertainment Expense Policy not added"


    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, ENTERTAINMENT_POLICY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, ENTERTAINMENT_POLICY, PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, ENTERTAINMENT_POLICY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[0] + "_" + ENTERTAINMENT_POLICY)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + ENTERTAINMENT_POLICY + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))








