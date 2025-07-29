from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *



def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User name").click()
    page.get_by_placeholder("User name").fill(IMPLUSRID)
    page.get_by_role("textbox", name="Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(2000)

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Legal Addresses")
    page.get_by_role("textbox").press("Enter")

    # Looping the values based on excel rows
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        # Navigating to Manage Legal Addresses page & Entering the data
        page.get_by_role("link", name="Manage Legal Addresses", exact=True).click()
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)
        page.locator("[id=\"__af_Z_window\"]").get_by_label("Address Line 1").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_label("Address Line 1").fill(str(datadictvalue["C_ADDRSS_LINE_1"]))
        page.locator("[id=\"__af_Z_window\"]").get_by_label("Address Line 2").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_label("Address Line 2").fill(datadictvalue["C_ADDRSS_LINE_2"])
        page.get_by_title("City", exact=True).click()
        page.get_by_role("link", name="Search...").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_label("City").nth(1).fill(datadictvalue["C_CITY"])
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.get_by_text(datadictvalue["C_CITY"]).first.click()
        page.get_by_role("button", name="OK").nth(1).click()
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Postal Code").type(str(datadictvalue["C_PSTL_CODE"]))
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # Saving and closing the record
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Address successfully added")
            datadictvalue["RowStatus"] = "Successfully Added Address"

        except Exception as e:
            print("Unable to save the Address")
            datadictvalue["RowStatus"] = "Unable to save the Address"

    # Signout from the application
    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, LEGAL_ADDRESS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, LEGAL_ADDRESS, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, LEGAL_ADDRESS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + LEGAL_ADDRESS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0]+ "_" + LEGAL_ADDRESS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))