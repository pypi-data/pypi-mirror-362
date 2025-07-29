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
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(5000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage General Ledger Descriptive Flexfields")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage General Ledger Descriptive Flexfields", exact=True).click()


    page.get_by_label("Name").click()
    page.get_by_label("Name").fill("Journal Lines")
    page.get_by_role("button", name="Search", exact=True).click()

    page.get_by_role("cell", name="Journal Lines", exact=True).click()
    page.get_by_role("button", name="Edit").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create").click()
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
        page.get_by_label("Name", exact=True).click()
        # page.pause()
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        # if datadictvalue["C_SCRTY_ENBLD"] == 'Yes':
        #     if not page.get_by_text("Enabled", exact=True).is_checked():
        #        page.get_by_text("Enabled", exact=True).click()
        #
        # elif datadictvalue["C_SCRTY_ENBLD"] == 'No':
        #     if page.get_by_text("Enabled", exact=True).is_checked():
        #        page.get_by_text("Enabled", exact=True).click()


        page.get_by_label("Data Type").select_option(datadictvalue["C_DATA_TYPE"])
        page.get_by_title("Search: Table Column").click()
        page.get_by_role("cell", name=datadictvalue["C_TABLE_CLMN"], exact=True).click()
        #####

        page.get_by_label("Value Set").fill(datadictvalue["C_VALUE_SET"])
        page.get_by_label("Range Type").select_option(datadictvalue["C_RANGE_TYPE"])
        # page.get_by_text("Required").click()

        if datadictvalue["C_RQRD"] == 'Yes':
            if not page.get_by_text("Required").is_checked():
                page.get_by_text("Required").click()

        elif datadictvalue["C_RQRD"] == 'No':
            if page.get_by_text("Required").is_checked():
                page.get_by_text("Required").click()

        page.get_by_label("Prompt").fill(datadictvalue["C_PRMPT"])
        page.get_by_label("Display Type").select_option(datadictvalue["C_DSPLY_TYPE"])

        page.get_by_label("Display Size").click()
        page.get_by_label("Display Size").fill(str(datadictvalue["C_DSPLY_SIZE"]))
        page.get_by_label("Display Height").click()
        page.get_by_label("Display Height").fill(str(datadictvalue["C_DSPLY_HGHT"]))
        page.get_by_label("Definition Help Text").click()
        page.get_by_label("Definition Help Text").fill(datadictvalue["C_DFNTN_HELP_TEXT"])
        page.get_by_label("Instruction Help Text").click()
        page.get_by_label("Instruction Help Text").fill(datadictvalue["C_INSTRTN_HELP_TEXT"])
        # page.get_by_text("Read-only").click()

        if datadictvalue["C_DSPLY_TYPE"] == 'Check Box':
            page.get_by_label("Checked Value", exact=True).fill(datadictvalue["C_CHCKD_VALUE"])
            page.get_by_label("Unchecked Value").click()
            page.get_by_label("Unchecked Value").fill(datadictvalue["C_UNCHCKD_VALUE"])

        if datadictvalue["C_READ_ONLY"] == 'Yes':
            if not page.get_by_text("Read-only").is_checked():
                page.get_by_text("Read-only").click()

        elif datadictvalue["C_READ_ONLY"] == 'No':
            if page.get_by_text("Read-only").is_checked():
                page.get_by_text("Read-only").click()

        page.get_by_role("button", name="Save and Close").click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        page.wait_for_timeout(2000)
        i = i + 1
        page.wait_for_timeout(3000)
    page.get_by_role("button", name="Save and Close").click()
    # page.pause()

    # Validation
    try:
        expect(page.get_by_role("heading", name="Search")).to_be_visible()
        print("GL-Descriptive Flexfields Executed Successfully")
        datadictvalue["RowStatus"] = "GL-Descriptive Flexfields Executed Successfully"
    except Exception as e:
        print("Managed Conversion Rates UnSuccessfully")
        datadictvalue["RowStatus"] = "GL-Descriptive Flexfields Executed UnSuccessfully"




    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, MANAGE_GL_DESCRIPTIVE_FLEXFIELDS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, MANAGE_GL_DESCRIPTIVE_FLEXFIELDS, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, MANAGE_GL_DESCRIPTIVE_FLEXFIELDS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + LEGAL_ENTITY_SHEET)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
                0] + "_" + LEGAL_ENTITY_SHEET + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))