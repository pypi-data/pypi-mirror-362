from playwright.sync_api import Playwright, sync_playwright
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    # Login to the instance
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    # Navigation
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

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        if datadictvalue["C_KEY_FLXFLD_NAME"] != PrevName:
        # Select the FF Name
            if datadictvalue["C_KEY_FLXFLD_NAME"] == 'Asset Key Flexfield':
                page.get_by_role("cell", name="Asset Key Flexfield", exact=True).click()
            if datadictvalue["C_KEY_FLXFLD_NAME"] == 'Category Flexfield':
                page.get_by_role("cell", name="Category Flexfield", exact=True).click()
            if datadictvalue["C_KEY_FLXFLD_NAME"] == 'Location Flexfield':
                page.get_by_role("cell", name="Location Flexfield", exact=True).click()
        # Create the Structure
            page.get_by_role("button", name="Manage Structures").click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Structure Code").click()
            page.get_by_label("Structure Code").type(datadictvalue["C_STRCTR_CODE"])
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.get_by_label("Description").fill(datadictvalue["C_DSCRP"])
            page.get_by_label("Delimiter").select_option(datadictvalue["C_DLMTR"])

            if datadictvalue["C_ENBLD"] == 'Yes':
                if not page.get_by_role("row", name="Enabled", exact=True).locator("label").is_checked():
                    page.get_by_role("row", name="Enabled", exact=True).locator("label").click()
            if datadictvalue["C_ENBLD"] == 'No':
                if page.get_by_role("row", name="Enabled", exact=True).locator("label").is_checked():
                    page.get_by_role("row", name="Enabled", exact=True).locator("label").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(5000)
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill("")
            page.get_by_label("Name").type(datadictvalue["C_STRCTR_CODE"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("button", name="Edit").click()
            page.wait_for_timeout(5000)
            # Create the segment code
            j = 0
            while j < rowcount:
                datadictvalue = datadict[j]
                page.get_by_role("button", name="Create").click()

                page.get_by_label("Segment Code").click()
                # page.pause()
                page.get_by_label("Segment Code").fill(datadictvalue["C_SGMNT_CODE"])
                # page.get_by_label("API Name").fill()
                page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
                page.get_by_label("Description").fill(datadictvalue["C_DSCRP1"])
                page.get_by_label("Sequence Number").fill(datadictvalue["C_SQNC_NUM1"])
                page.get_by_label("Prompt", exact=True).fill(datadictvalue["C_PRMPT"])
                page.get_by_label("Short Prompt").fill(datadictvalue["C_SHORT_PMT"])
                if datadictvalue["C_ENBLD1"] == 'Yes':
                    if not page.get_by_text("Enabled").is_checked():
                        page.get_by_text("Enabled").click()
                elif datadictvalue["C_ENBLD1"] == 'No':
                    if page.get_by_text("Enabled").is_checked():
                        page.get_by_text("Enabled").click()

                page.get_by_label("Display Width").fill(datadictvalue["C_DSLPY_WIDTH"])
                page.get_by_label("Range Type").select_option(datadictvalue["C_RANGE_TYPE"])
                page.get_by_label("Column Name").fill(datadictvalue["C_CLM_NAME"])
                page.get_by_label("Default Value Set Code").fill(datadictvalue["C_DFLT_VALUE_SET_CODE"])

                page.get_by_role("button", name="Save", exact=True).click()

                page.locator("//button[text()='ave and Close']").click()

                print("Row Added - ", str(j))
                datadictvalue["RowStatus"] = "Successfully Created COA Add Structure"
                j = j + 1
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(5000)

        i = i + 1

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