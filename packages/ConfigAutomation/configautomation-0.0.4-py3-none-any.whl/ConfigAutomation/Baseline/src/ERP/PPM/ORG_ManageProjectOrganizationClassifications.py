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
    page.get_by_role("textbox").fill("Manage Project Organization Classifications")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Project Organization Classifications", exact=True).click()
    page.wait_for_timeout(3000)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        # Search and edit the Project
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.locator("//label[text()='Effective Date']//following::input[1]").first.fill(datadictvalue["C_FROM_DATE"].strftime('%m/%d/%y'))
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(1000)

        # Selecting the Classification - Department
        page.get_by_role("cell", name=datadictvalue["C_NAME"]).click()
        page.get_by_role("button", name="Edit").click()

        # Review Selected Organizations - Non-editable fields
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Continue").click()

        # Classify Organizations
        if datadictvalue["C_CLSSFY_AS_PRJCT_AND_TASK_OWNNG_ORGNZTN"] == 'Yes':
           page.get_by_text("Classify as project and task").click()
        if datadictvalue["C_ALLW_INDRCT_PRJCTS"] == 'Yes':
            page.get_by_text("Allow Indirect Projects").click()
        if datadictvalue["C_ALLW_PRJCTS_ENBLD_FOR_CPTLZTN"] == 'Yes':
            page.get_by_text("Allow projects enabled for capitalization").click()
        if datadictvalue["C_ALLW_PRJCTS_ENBLD_FOR_BLLNG"] == 'Yes':
            page.get_by_text("Allow projects enabled for billing").click()
        if datadictvalue["C_CLSSFY_AS_PRJCT_EXPNDTR_ORGNZTN"] == 'Yes':
            page.get_by_text("Classify as project expenditure organization").click()

        page.get_by_role("button", name="Save and Continue").click()
        page.wait_for_timeout(3000)

        # Add Organizations to Tree (Disabled) - If enabled need to capture the fields
        page.get_by_role("button", name="Save and Continue").click()

        # Submit Process to Maintain Project Organizations
        page.get_by_label("Submission Notes").fill(datadictvalue["C_SBMSSN_NTS"])

        # page.get_by_role("button", name="Submit").click()
        # Warning
        # page.get_by_role("button", name="Yes").click()
        page.wait_for_timeout(1000)

        try:
            expect(page.get_by_text("Confirmation")).to_be_visible()
            page.get_by_role("button", name="OK").click()
            print("Project Organization Classification Saved Successfully")
            datadictvalue["RowStatus"] = "Burden Structure added successfully"

        except Exception as e:
            print("Project Organization Classification not saved")
            datadictvalue["RowStatus"] = "Project Organization Classification are not added"

        page.get_by_role("button", name="Cancel").click()


        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_ORG_CLASSIFICATIONS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_ORG_CLASSIFICATIONS, PRCS_DIR_PATH + PPM_ORG_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_ORG_CLASSIFICATIONS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_ORG_CONFIG_WRKBK)[0] + "_" + PRJ_ORG_CLASSIFICATIONS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_ORG_CONFIG_WRKBK)[
            0] + "_" + PRJ_ORG_CLASSIFICATIONS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))