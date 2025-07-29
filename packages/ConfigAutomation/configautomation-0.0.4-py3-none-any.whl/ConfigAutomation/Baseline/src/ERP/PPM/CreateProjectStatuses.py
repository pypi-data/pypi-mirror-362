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
    page.get_by_role("textbox").fill("Manage Project Statuses")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Project Statuses", exact=True).click()

    # Create Project Statuses
    i = 1
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Add Row").first.click()
        page.wait_for_timeout(2000)
        if page.get_by_label("Status", exact=True).is_visible():
            page.get_by_label("Status", exact=True).fill(datadictvalue["C_PRJCT_STTS"])
        if page.get_by_label("Project Status").is_visible():
            page.get_by_label("Project Status").fill(datadictvalue["C_PRJCT_STTS"])
        page.wait_for_timeout(2000)
        if page.get_by_role("cell", name="Status Type", exact=True).is_visible():
            page.get_by_label("Status Type").select_option(datadictvalue["C_STTS_TYPE"])
        page.wait_for_timeout(2000)
        if page.get_by_role("cell", name="System Status", exact=True).is_visible():
            page.get_by_label("System Status").select_option(datadictvalue["C_SYSTM_STTS"])
        page.wait_for_timeout(2000)
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        # Entering From & To Date
        # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date",exact=True).get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_FROM_DATE"])
        page.locator("//input[contains(@id,'id2')][1]").nth(0).fill(datadictvalue["C_FROM_DATE"])
        if datadictvalue["C_TO_DATE"] != '':
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date",exact=True).get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_TO_DATE"])
            page.locator("//input[contains(@id,'id4')][1]").nth(0).fill(datadictvalue["C_TO_DATE"].strftime('%m/%d/%y'))

        page.wait_for_timeout(2000)

        # #Enable or Disable Initial Project Status
        if datadictvalue["C_INTL_PRJCT_STTS"] == 'Yes':
            page.locator("//table[@summary='Project Statuses']//following::input[@type='checkbox']//following::label").first.check()

        page.wait_for_timeout(2000)

        # Enable or Disable workflow
        if datadictvalue["C_ENBL_WRKFLW"] == 'Yes':
            page.locator("//table[@summary='Project Statuses']//following::input[@type='checkbox']//following::label").nth(1).check()

            page.wait_for_timeout(2000)

            # Entering Workflow attributes -Status After Change Accepted
            page.get_by_title("Search: Status After Change Accepted").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("cell", name="*Project Status Project").get_by_label("Project Status").click()
            page.get_by_role("cell", name="*Project Status Project").get_by_label("Project Status").fill(datadictvalue["C_STTS_AFTER_CHNG_ACCPTD"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_STTS_AFTER_CHNG_ACCPTD"],exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

            # Entering Workflow attributes -Status After Change Rejected
            page.get_by_title("Search: Status After Change Rejected").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("cell", name="*Project Status Project").get_by_label("Project Status").click()
            page.get_by_role("cell", name="*Project Status Project").get_by_label("Project Status").fill(datadictvalue["C_STTS_AFTER_CHNG_RJCTD"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_STTS_AFTER_CHNG_RJCTD"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        #Entering Details

        page.get_by_role("link", name="Status Controls").click()
        if datadictvalue["C_STTS_TYPE"] == "Project" and datadictvalue["C_SYSTM_STTS"] != "Closed":
            # Adjust transactions
            if datadictvalue["C_ADJST_TRNSCTNS"] == 'Yes':
                page.get_by_role("cell", name="Adjust transactions").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Adjust transactions").locator("label").check()
            if datadictvalue["C_ADJST_TRNSCTNS"] == 'No' or '':
                page.get_by_role("cell", name="Adjust transactions").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Adjust transactions").locator("label").uncheck()

            #Capitalize assets
            if datadictvalue["C_CPTLZ_ASSTS"] == 'Yes':
                page.get_by_role("cell", name="Capitalize assets").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Capitalize assets").locator("label").check()
            if datadictvalue["C_CPTLZ_ASSTS"] == 'No' or '':
                page.get_by_role("cell", name="Capitalize assets").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Capitalize assets").locator("label").uncheck()

            #Capitalized interest
            if datadictvalue["C_CPTLZD_INTRST"] == 'Yes':
                page.get_by_role("cell", name="Capitalized interest").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Capitalized interest").locator("label").check()
            if datadictvalue["C_CPTLZD_INTRST"] == 'No' or '':
                page.get_by_role("cell", name="Capitalized interest").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Capitalized interest").locator("label").uncheck()

            #Create burden transactions
            if datadictvalue["C_CRT_BRDN_TRNSCTNS"] == 'Yes':
                page.get_by_role("cell", name="Create burden transactions").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Create burden transactions").locator("label").check()
            if datadictvalue["C_CRT_BRDN_TRNSCTNS"] == 'No' or '':
                page.get_by_role("cell", name="Create burden transactions").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Create burden transactions").locator("label").uncheck()

            #Create new transactions
            if datadictvalue["C_CRT_NEW_TRNSCTNS"] == 'Yes':
                page.get_by_role("cell", name="Create new transactions").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Create new transactions").locator("label").check()
            if datadictvalue["C_CRT_NEW_TRNSCTNS"] == 'No' or '':
                page.get_by_role("cell", name="Create new transactions").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Create new transactions").locator("label").uncheck()

            #Progress reporting by team
            if datadictvalue["C_PRGRSS_RPRTNG_BY_TEAM_MMBRS"] == 'Yes':
                page.get_by_role("cell", name="Progress reporting by team").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Progress reporting by team").locator("label").check()
            if datadictvalue["C_PRGRSS_RPRTNG_BY_TEAM_MMBRS"] == 'No' or '':
                page.get_by_role("cell", name="Progress reporting by team").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Progress reporting by team").locator("label").uncheck()

            #Summarize project data
            if datadictvalue["C_SMMRZ_PRJCT_DATA"] == 'Yes':
                page.get_by_role("cell", name="Summarize project data").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Summarize project data").locator("label").check()
            if datadictvalue["C_SMMRZ_PRJCT_DATA"] == 'No' or '':
                page.get_by_role("cell", name="Summarize project data").click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Summarize project data").locator("label").uncheck()
            page.wait_for_timeout(3000)

        #Next Allowable status
        if datadictvalue["C_NXT_ALLWBL_STTSS"] != '':
            page.get_by_role("link", name="Next Allowable Statuses").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Next Allowable Status").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Next Allowable Status").select_option(datadictvalue["C_NXT_ALLWBL_STTSS"])
            page.wait_for_timeout(1000)
            page.get_by_role("link", name="Next Allowable Statuses").press("Tab")
            page.wait_for_timeout(3000)

        # if datadictvalue["C_NXT_ALLWBL_STTSS"] == 'Status Name':
            page.get_by_role("button", name="Add Row").nth(1).click()

            page.get_by_role("table", name="Next Allowable Statuses").get_by_label("Next Allowable Status").select_option(datadictvalue["C_SYSTM_STTS_NEXT_ALLWBL_STTS"])
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save", exact=True).click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1

    # Save the data
    page.get_by_role("button", name="Save and Close").click()

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Project Statuses Saved Successfully")
        datadictvalue["RowStatus"] = "Project Statuses are added successfully"

    except Exception as e:
        print("Project Statuses not saved")
        datadictvalue["RowStatus"] = "Project Statuses are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJ_STS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJ_STS, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJ_STS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + PRJ_STS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + PRJ_STS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))