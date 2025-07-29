from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    # Sign In - Instance
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    # Navigate to the Required Page
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Remit to Addresses")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Remit to Addresses").click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Create Remit - to - Address
        page.get_by_role("button", name="Create").first.click()
        page.wait_for_timeout(2000)
        page.get_by_label("Remit-to Address Set").type(datadictvalue["C_REMIT_TO_ADDRSS_SET"],delay=75)
        page.get_by_role("option", name=datadictvalue["C_REMIT_TO_ADDRSS_SET"]).click()
        page.get_by_label("Country", exact=True).select_option(datadictvalue["C_CNTRY"])
        page.get_by_label("Address Line 1").fill(datadictvalue["C_ADDRSS_LINE_1"])
        page.get_by_label("Address Line 2").fill(datadictvalue["C_ADDRSS_LINE_2"])
        #Note: City,County and State field values should be updated in the workbook
        page.get_by_title("City", exact=True).click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="City").click()
        page.get_by_role("textbox", name="City").fill(datadictvalue["C_CITY"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CITY"]+ "," + " " + datadictvalue["C_CNTY"] + "," + " " + datadictvalue["C_STATE"]).click()
        page.get_by_role("button", name="OK").click()
        page.get_by_label("State").clear()
        page.get_by_label("State").fill(datadictvalue["C_STATE"])
        if page.get_by_label("Postal Code").is_visible():
            page.get_by_label("Postal Code").fill(str(datadictvalue["C_PSTL_CODE"]))
        if page.get_by_text("Zip Code").is_visible():
            page.get_by_text("Zip Code").fill(str(datadictvalue["C_PSTL_CODE"]))
        page.get_by_label("County").clear()
        page.get_by_label("County").fill(datadictvalue["C_CNTY"])
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)

        # Create Site Address
        if datadictvalue["C_RCPT_CNTRY"] !='':
            page.get_by_role("button", name="Create").nth(1).click()
            page.locator("//h1[text()='Receipt from Criteria']//following::label[text()='Country']//following::input[1]").fill(datadictvalue["C_RCPT_CNTRY"])
            page.get_by_label("State").fill(datadictvalue["C_RCPT_STATE"])
            page.get_by_label("From Postal Code").fill(str(datadictvalue["C_FROM_PSTL_CODE"]))
            page.get_by_label("To Postal Code").fill(str(datadictvalue["C_TO_PSTL_CODE"]))
            page.get_by_label("Context Value").select_option(datadictvalue["C_CNTXT_VALUE"])
            page.get_by_role("button", name="Save and Close").click()
            if page.get_by_role("button", name="OK").is_visible():
                page.get_by_role("button", name="OK").click()


        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1
        page.wait_for_timeout(3000)
    page.get_by_role("button", name="Done").click()
    page.wait_for_timeout(3000)



    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Remit to Addresses Saved Successfully")

    except Exception as e:
        print("Remit to Addresses not Saved")


    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, REMIT_TO_ADDRESSES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, REMIT_TO_ADDRESSES, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, REMIT_TO_ADDRESSES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + REMIT_TO_ADDRESSES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + REMIT_TO_ADDRESSES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))