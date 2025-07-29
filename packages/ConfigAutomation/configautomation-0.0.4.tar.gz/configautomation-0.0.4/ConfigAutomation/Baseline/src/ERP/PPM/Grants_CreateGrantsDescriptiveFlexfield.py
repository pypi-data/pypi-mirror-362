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
    page.wait_for_timeout(5000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Descriptive Flexfields")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(1000)
    page.get_by_role("link", name="Manage Descriptive Flexfields", exact=True).click()

    #Search Configuration Item
    page.get_by_label("Name").click()
    page.get_by_label("Name").fill("Award Descriptive Flexfield")
    page.get_by_role("button", name="Search", exact=True).click()
    page.get_by_role("cell", name="Award Descriptive Flexfield", exact=True).click()
    page.get_by_role("button", name="Edit").click()
    page.wait_for_timeout(1000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create").first.click()
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
        page.get_by_label("Name", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(2000)
        page.get_by_label("Data Type").select_option(datadictvalue["C_DATA_TYPE"])
        page.wait_for_timeout(2000)

        # Select Value Set
        page.get_by_title("Search: Value Set").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Value Set").click()
        page.get_by_role("textbox", name="Value Set").fill(datadictvalue["C_VALUE_SET"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VALUE_SET"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        page.get_by_label("Range Type").select_option(datadictvalue["C_RANGE_TYPE"])
        page.wait_for_timeout(3000)

        if datadictvalue["C_RQRD"] == 'Yes':
            if not page.get_by_text("Required").is_checked():
                page.get_by_text("Required").click()

        elif datadictvalue["C_RQRD"] == 'No':
            if page.get_by_text("Required").is_checked():
                page.get_by_text("Required").click()

        page.wait_for_timeout(2000)
        page.get_by_label("Default Type").select_option(datadictvalue["C_INTL_VALUE_DFLT_TYPE"])
        page.get_by_label("Prompt").fill(datadictvalue["C_PRMPT"])
        page.get_by_label("Display Type").select_option(datadictvalue["C_DSPLY_TYPE"])
        page.get_by_label("Display Size").click()
        page.get_by_label("Display Size").fill(str(datadictvalue["C_DSPLY_SIZE"]))
        page.get_by_label("Display Height").click()
        page.get_by_label("Display Height").fill(str(datadictvalue["C_DSPLY_HGHT"]))
        page.get_by_label("Definition Help Text").click()
        page.get_by_label("Definition Help Text").fill(datadictvalue["C_DFNTN_HELP_TEXT"])
        page.get_by_label("Instruction Help Text").click()
        page.get_by_label("Instruction Help Text").fill(datadictvalue["C_INSTRCTN_HELP_TEXT"])

        if datadictvalue["C_DSPLY_TYPE"] == 'Check Box':
            page.get_by_label("Checked Value", exact=True).fill(datadictvalue["C_CHCKD_VALUE"])
            page.get_by_label("Unchecked Value").click()
            page.get_by_label("Unchecked Value").fill(datadictvalue["C_UNCHCKD-VALUE"])

        if datadictvalue["C_READ_ONLY"] == 'Yes':
            if not page.get_by_text("Read-only").is_checked():
                page.get_by_text("Read-only").click()

        elif datadictvalue["C_READ_ONLY"] == 'No':
            if page.get_by_text("Read-only").is_checked():
                page.get_by_text("Read-only").click()

        if datadictvalue["C_BI_ENBLD"] == 'Yes':
            page.get_by_text("BI Enabled").click()

        page.wait_for_timeout(2000)

        # Save the data
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)


        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1

        # Save the data
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Awards Descriptive Flexfields saved Successfully")
            datadictvalue["RowStatus"] = "Awards Descriptive Flexfields added successfully"

        except Exception as e:
            print("Awards Descriptive Flexfields not saved")
            datadictvalue["RowStatus"] = "Awards Descriptive Flexfields not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, GRANTS_DFF):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, GRANTS_DFF,
                             PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, GRANTS_DFF)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[0] + "_" + GRANTS_DFF)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[
            0] + "_" + GRANTS_DFF + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))