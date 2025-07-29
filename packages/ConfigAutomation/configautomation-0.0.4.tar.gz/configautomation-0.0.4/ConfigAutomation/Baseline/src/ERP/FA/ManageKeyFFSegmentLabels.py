from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    # Login to the instances
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    # Navigation to Manage Asset Books
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Fixed Assets Key Flexfields")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Fixed Assets Key Flexfields").click()
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Search", exact=True).click()


    # PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        # if datadictvalue["C_STRCTR_CODE"] != PrevName:

            # Manage Segment Labels:
            # Selecting the required Field:
        if datadictvalue["C_KEY_FLXFLD_NAME"] == 'Asset Key Flexfield':
            page.get_by_role("cell", name="Asset Key Flexfield", exact=True).click()
        if datadictvalue["C_KEY_FLXFLD_NAME"] == 'Category Flexfield':
            page.get_by_role("cell", name="Category Flexfield", exact=True).click()
        if datadictvalue["C_KEY_FLXFLD_NAME"] == 'Location Flexfield':
            page.get_by_role("cell", name="Location Flexfield", exact=True).click()

        page.wait_for_timeout(2000)
        # Navigating to the Manage segment page
        page.get_by_role("link", name="Actions", exact=True).click()
        page.get_by_role("cell", name="Manage Segment Labels", exact=True).click()
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(2000)
        # Row Input
        page.get_by_label("Segment Label Code").fill(datadictvalue["C_SGMNT_LABEL"])
        # page.locator("//td[@title='Segment Label Code'][1]").fill(datadictvalue["C_SGMNT_LABEL"])
        page.get_by_role("cell", name="Segment Label Code Name").get_by_label("Name", exact=True).fill(datadictvalue["C_NAME1"])
        page.get_by_role("cell", name="Segment Label Code Name").get_by_label("Description").fill(datadictvalue["C_NAME1"])
        page.get_by_role("cell", name="Segment Label Code Name").get_by_label("BI Object Name").fill(datadictvalue["C_BI_OBJ_NAME"])
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save and Close").click()
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"


        i = i + 1

    # Validation

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("FA Key FF Manage Segment Labels Saved Successfully")

    except Exception as e:
        print("FA Key FF Manage Segment Labels not Saved")



    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_FA_KEYFF):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_FA_KEYFF, PRCS_DIR_PATH + FA_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + FA_WORKBOOK, MANAGE_FA_KEYFF)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANAGE_FA_KEYFF)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[
            0] + "_" + MANAGE_FA_KEYFF + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))