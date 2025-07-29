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
    page.get_by_role("textbox").fill("Balance Definitions")
    page.get_by_role("textbox").press("Enter")

    # Balance Definitions
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.get_by_role("link", name="Balance Definitions", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Create").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_label("Legislative Data Group").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTV_DATA_GROUP"], exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(1000)
        page.get_by_label("Reporting Name").click()
        page.get_by_label("Reporting Name").fill(datadictvalue["C_RPRTNG_NAME"])
        page.wait_for_timeout(1000)

        page.get_by_label("Balance Category").first.click()
        page.get_by_text(datadictvalue["C_BLNC_CTGRY"], exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_label("Unit of Measure").click()
        page.get_by_text(datadictvalue["C_UNIT_OF_MSR"]).click()
        page.wait_for_timeout(1000)
        if datadictvalue["C_UNIT_OF_MSR"] == 'Money':
            page.get_by_role("combobox", name="Currency").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CRRNCY"], exact=True).click()
        page.wait_for_timeout(2000)
        #Select Base Balance
        if datadictvalue["C_BASE_BLNC"] != '':
            page.get_by_title("Search: Base Balance").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.locator("//div[text()='Search and Select: Base Balance']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_BASE_BLNC"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BASE_BLNC"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        #Entering Primary Details
            # Select Elemenet Name
        if datadictvalue["C_ELMNT_NAME"] != '':
            page.get_by_title("Search: Element Name").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_role("textbox", name="Element Name").fill(datadictvalue["C_ELMNT_NAME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ELMNT_NAME"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)
            # Select Input Type
        if datadictvalue["C_INPUT_VALUE"] != '':
            page.get_by_role("combobox", name="Input Value").click()
            page.wait_for_timeout(1000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_INPUT_VALUE"], exact=True).click()

        #Next Tab
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(5000)

        #Capturing Dimension & Feeds details in another script as discussed with Vignesh(payroll team)
        # page.get_by_label("Dimension Name").click()
        # page.get_by_label("Elements").click()
        # page.get_by_label("Feeds").click()

        #Next Tab
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(5000)

        #Submit
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(5000)

        # #Click okay on the popup box
        # page.get_by_role("button", name="OK").click()
        # page.wait_for_timeout(2000)

        #Done to exit from task to create new row
        page.get_by_role("button", name="Done").click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Deferred Balances Saved Successfully")
        datadictvalue["RowStatus"] = "Deferred Balances are added successfully"

    except Exception as e:
        print("Deferred Balances not saved")
        datadictvalue["RowStatus"] = "Deferred Balances are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_DFRD_BLNCE_FEEDS, DFRD_CSTM_BLNCE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_DFRD_BLNCE_FEEDS, DFRD_CSTM_BLNCE, PRCS_DIR_PATH + PAYROLL_DFRD_BLNCE_FEEDS)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_DFRD_BLNCE_FEEDS, DFRD_CSTM_BLNCE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_DFRD_BLNCE_FEEDS)[0] + "_" +DFRD_CSTM_BLNCE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_DFRD_BLNCE_FEEDS)[0] + "_" +DFRD_CSTM_BLNCE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))