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
    page.wait_for_timeout(40000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(30000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Time Rule Templates")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Time Rule Templates", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        # Template Type
        page.get_by_role("row", name="*Template Type", exact=True).get_by_role("combobox").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TMPLT_TYPE"]).click()
        page.wait_for_timeout(2000)

        # Formula Name
        page.get_by_title("Search: Formula Name").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Formula Name").type(datadictvalue["C_FRML_NAME"])
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FRML_NAME"], exact=True).click()
        page.get_by_role("cell", name=datadictvalue["C_FRML_NAME"], exact=True).locator("span").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(5000)

        # Name
        page.get_by_label("Name", exact=True).clear()
        page.get_by_label("Name").type(datadictvalue["C_NAME"])
        page.wait_for_timeout(3000)

        # Description
        page.get_by_label("Description").clear()
        page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(2000)

        # Rule Classification
        page.get_by_role("combobox", name="Rule Classification").click()
        page.get_by_text(datadictvalue["C_RULE_CLSSFCTN"], exact=True).click()
        page.wait_for_timeout(4000)

        # Summation Level
        if datadictvalue["C_TCE_SAVE"] == "N/A":
            page.get_by_role("combobox", name="Summation Level").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SMMTN_LEVEL"], exact=True).click()
            page.wait_for_timeout(3000)

        # Reporting Level
        page.get_by_role("combobox", name="Reporting Level").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RPRTNG_LEVEL"]).click()
        page.wait_for_timeout(3000)

        # Suppress Duplicate Messages Display
        page.get_by_role("combobox", name="Suppress Duplicate Messages").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SPPRSS_DPLCT_MSSGS_DSPLY"]).click()
        page.wait_for_timeout(3000)

        # Process Empty Time Card
        page.get_by_role("combobox", name="Process Empty Time Card").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRCSS_EMPTY_TIME_CARD"]).click()
        page.wait_for_timeout(3000)

        # Selecting Time Card Events That Trigger Rule
        # Save
        if datadictvalue["C_TCE_SAVE"] == "Yes":
            page.get_by_text("Save", exact=True).check()
        if datadictvalue["C_TCE_SAVE"] == "No":
            page.get_by_text("Save", exact=True).uncheck()
            page.wait_for_timeout(2000)
        # Submit
        if datadictvalue["C_TCE_SUBMIT"] == "Yes":
            page.get_by_text("Submit", exact=True).check()
        if datadictvalue["C_TCE_SUBMIT"] == "No":
            page.get_by_text("Submit", exact=True).uncheck()
            page.wait_for_timeout(2000)
        # ReSubmit
        if datadictvalue["C_TCE_RESBMT"] == "Yes":
            page.get_by_text("Resubmit").check()
        if datadictvalue["C_TCE_RESBMT"] == "No":
            page.get_by_text("Resubmit").uncheck()
            page.wait_for_timeout(2000)
        # Delete
        if datadictvalue["C_TCE_DLT"] == "Yes":
            page.get_by_text("Delete").check()
        if datadictvalue["C_TCE_DLT"] == "No":
            page.get_by_text("Delete").uncheck()
            page.wait_for_timeout(2000)

        # Clicking on Next button
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(2000)

        # Selecting Parameter Type for Define Limit
        page.locator("//span[text()='DEFINED_LIMIT']//following::input[1]").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRMTR_TYPE"]).click()
        page.wait_for_timeout(2000)

        # # Selecting Parameter Type for Message_Code
        # page.locator("//span[text()='MESSAGE_CODE']//following::input[1]").click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text("Fixed text").click()
        #
        # # Selecting Parameter Type for WORKED_TIME_CONDITION
        # page.locator("//span[text()='WORKED_TIME_CONDITION']//following::input[1]").click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text("Fixed text").click()

        # Selecting Required
        page.get_by_role("row", name="1 DEFINED_LIMIT Parameter").get_by_label("Required").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RQRD"]).click()
        page.wait_for_timeout(2000)
        # page.get_by_role("cell", name="MESSAGE_CODE Parameter Type").get_by_label("Required").click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text("No").click()
        # page.get_by_role("row", name="3 WORKED_TIME_CONDITION").get_by_label("Required").click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text("No").click()

        # Selecting Value Set
        page.get_by_role("row", name="1 DEFINED_LIMIT Parameter").get_by_label("Required").first.click()
        page.wait_for_timeout(3000)
        # page.get_by_role("cell", name="1 DEFINED_LIMIT Parameter").get_by_label("Value Set").first.click()
        # page.get_by_role("cell", name="1 DEFINED_LIMIT Parameter").get_by_label("Value Set").first.type(datadictvalue["C_VALUE_SET"])
        page.get_by_title("Search: Value Set").first.click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Value Set Code").type(datadictvalue["C_VALUE_SET"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VALUE_SET"]).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        # Entering Display Name for Define Limit
        page.get_by_role("row", name="1 DEFINED_LIMIT Parameter").get_by_label("Display Name").first.clear()
        page.get_by_role("row", name="1 DEFINED_LIMIT Parameter").get_by_label("Display Name").type(datadictvalue["C_DSPLY_NAME"])
        page.wait_for_timeout(2000)

        # # Entering Display Name for Message_Code
        # page.get_by_role("cell", name="MESSAGE_CODE Parameter Type").get_by_label("Display Name").clear()
        # page.get_by_role("cell", name="MESSAGE_CODE Parameter Type").get_by_label("Display Name").type(datadictvalue["C_DSPLY_NAME"])

        # # Entering Display Name for WORKED_TIME_CONDITION
        # page.get_by_role("row", name="3 WORKED_TIME_CONDITION").get_by_label("Display Name").clear()
        # page.get_by_role("row", name="3 WORKED_TIME_CONDITION").get_by_label("Display Name").type(datadictvalue["C_DSPLY_NAME"])

        # Clicking on Next button
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(2000)

        # Message Severity
        if datadictvalue["C_MSSG_SVRTY"] != 'N/A':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Message Severity").click()
            page.get_by_text(datadictvalue["C_MSSG_SVRTY"]).click()

        # Display Name
        if datadictvalue["C_OUT_DSPLY_NAME"] != "N/A":
            page.get_by_label("Display Name").clear()
            page.get_by_label("Display Name").type(datadictvalue["C_OUT_DSPLY_NAME"])
            page.wait_for_timeout(2000)

        # Clicking on Next button
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(2000)

        # Entering the Explanation
        if datadictvalue["C_EXPLNTN"] != 'N/A':
            page.get_by_label("Explanation", exact=True).click()
            page.get_by_label("Explanation", exact=True).type(datadictvalue["C_EXPLNTN"])
            page.wait_for_timeout(2000)

        # Clicking on Next button
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(2000)

        # Saving the Record
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="OK").click()

        try:
            expect(page.get_by_role("heading", name="Rule Templates")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Manage Time Repository Rule Templates-Time entry rule Created Successfully")
            datadictvalue["RowStatus"] = "Created Manage Time Repository Rule Templates-Time entry rule Successfully"
        except Exception as e:
            print("Unable to Save Manage Time Repository Rule Templates-Time entry rule")
            datadictvalue["RowStatus"] = "Unable to Save Manage Time Repository Rule Templates-Time entry rule"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, TIME_REPOSITORY_TEMP_TIME_ENT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, TIME_REPOSITORY_TEMP_TIME_ENT, PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, TIME_REPOSITORY_TEMP_TIME_ENT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0])
        write_status(output,
                     RESULTS_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
