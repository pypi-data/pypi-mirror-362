from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
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
    page.get_by_role("textbox").fill("Manage Payables Document Sequences")
    page.get_by_role("textbox").press("Enter")


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Manage Payables Document Sequences", exact=True).click()
        page.get_by_role("button", name="New").first.click()
        page.get_by_role("row", name="Expand Document Sequence Name").get_by_label("Document Sequence Name").fill(datadictvalue["C_DCMNT_SQNC_NAME"])
        page.locator("//span[text()='Application']//following::select[1]").select_option(datadictvalue["C_APPLCTN"])
        page.locator("//span[text()='Module']//following::input[2]").fill(datadictvalue["C_MDL"])
        page.locator("//h2[text()='Search Results']//following::span[text()='Type']//following::select[2]").select_option(datadictvalue["C_TYPE"])
        page.locator("//span[text()='Determinant Type']//following::select[3]").select_option(datadictvalue["C_DTRMNNT_TYPE"])
        page.locator("//span[text()='Start Date']//following::input[contains(@placeholder,'m/d/yy')][1]").fill(datadictvalue["C_START_DATE"].strftime("%m/%d/%Y"))
        page.locator("//span[text()='End Date']//following::input[contains(@placeholder,'m/d/yy')][2]").fill(datadictvalue["C_END_DATE"])
        page.get_by_title("Expand").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Initial Value").clear()
        page.get_by_label("Initial Value").fill(str(datadictvalue["C_INTL_VALUE"]))

        #Below field is not mentioned in the config workbook
        # page.get_by_role("row", name="Validate Transaction Date", exact=True).locator("label").nth(1).check()
        if datadictvalue["C_DSPLY_MSG"] == 'Yes':
            if not page.locator("//label[text()='Display Message?']//following::label[1]").is_checked():
             page.locator("//label[text()='Display Message?']//following::label[1]").click()
        if datadictvalue["C_DSPLY_MSG"] == 'No':
            if page.locator("//label[text()='Display Message?']//following::label[1]").is_checked():
             page.locator("//label[text()='Display Message?']//following::label[1]").click()
        # Below field is not mentioned in the config workbook
        # page.get_by_role("row", name="Audit", exact=True).locator("label").nth(1).check()
        if page.get_by_label("Cache Size").is_visible():
            page.get_by_label("Cache Size").clear()
            page.get_by_label("Cache Size").fill(datadictvalue["C_CACHE_SIZE"])
        #Add the assignment

        page.get_by_role("button", name="New").nth(1).click()
        page.get_by_title("Search: Document Sequence").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Document Sequence Category").fill(datadictvalue["C_DCMNT_SQNC_CTGRY_NAME"])
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.get_by_text(datadictvalue["C_DCMNT_SQNC_CTGRY_NAME"]).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Method").select_option(datadictvalue["C_MTHD"])
        page.get_by_role("cell", name="Press down arrow to access Calendar Start Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_ASSGNMNTS_START_DATE"].strftime("%m/%d/%Y"))
        if datadictvalue["C_ASSGNMNTS_END_DATE"] != '':
            page.locator("//span[text()='Method']//following::span[text()='End Date']//following::input[contains(@placeholder,'m/d/yy')][2]").fill(datadictvalue["C_ASSGNMNTS_END_DATE"].strftime("%m/%d/%Y"))

        page.wait_for_timeout(2000)
        if page.get_by_label("Ledger Value").is_visible():
            page.get_by_label("Ledger Value").fill(datadictvalue["C_LDGR_VALUE"])
        elif page.get_by_label("Business Unit Value").is_visible():
            page.get_by_label("Business Unit Value").fill("")
        elif page.get_by_label("Legal Entity Value").is_visible:
            page.get_by_label("Legal Entity Value").fill("")

        # Save the data
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        i = i + 1
        
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Payables Document Sequences Saved Successfully")
            datadictvalue["RowStatus"] = "Payables Document Sequences are added successfully"

        except Exception as e:
            print("Payables Document Sequences not saved")
            datadictvalue["RowStatus"] = "Payables Document Sequences are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYABLES_DOC_SEQUENCE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYABLES_DOC_SEQUENCE, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, PAYABLES_DOC_SEQUENCE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + PAYABLES_DOC_SEQUENCE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
            0] + "_" + PAYABLES_DOC_SEQUENCE+ "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))