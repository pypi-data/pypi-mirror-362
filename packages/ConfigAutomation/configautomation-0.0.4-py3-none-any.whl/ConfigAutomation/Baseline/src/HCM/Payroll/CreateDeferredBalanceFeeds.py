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
    page.wait_for_timeout(40000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Balance Definitions")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Balance Definitions", exact=True).click()

    # Balance Definitions
    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        if datadictvalue["C_NAME"] != PrevName:
            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Save").click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Submit").click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Done").click()
                page.wait_for_timeout(2000)
                try:
                    page.get_by_role("button", name="Done").is_visible()
                    print("Custom Dimensions Saved")
                    datadict[i - 1]["RowStatus"] = "Custom Dimensions Saved"
                except Exception as e:
                    print("Unable to save Custom Dimensions")
                    datadict[i - 1]["RowStatus"] = "Unable to save Custom Dimensions"
                page.wait_for_timeout(3000)

            page.get_by_label("Name", exact=True).click()
            page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
            page.get_by_role("combobox", name="Legislative Data Group").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTV_DATA_GROUP"], exact=True).nth(0).click()
            page.get_by_role("button", name="Search", exact=True).click()
            # page.get_by_role("link", name="Edit").click()
            page.get_by_role("link", name=datadictvalue["C_NAME"], exact=True).click()
            page.wait_for_timeout(2000)
            page.get_by_placeholder("m/d/yy").clear()
            page.get_by_placeholder("m/d/yy").type(datadictvalue["C_EFFCTV_DATE"])
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Edit").click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name="Balance Feeds").click()
            page.wait_for_timeout(1000)
            PrevName = datadictvalue["C_NAME"]
            print("Name:", PrevName)

        if datadictvalue["C_ELMNT_CLSSFCTN"] != 'N/A' or '':
            page.get_by_role("button", name="Add Row").click()
            page.wait_for_timeout(2000)
            # Select Balance Classifications
            # page.get_by_title("Search: ClassificationName").click()
            # page.get_by_role("link", name="Search...").click()
            # page.get_by_label("Element Classification Name").click()
            # page.get_by_label("Element Classification Name").fill(datadictvalue["C_ELMNT_CLSSFCTN"])
            # # page.get_by_role("textbox", name="Element Classification Name").fill(datadictvalue["C_ELMNT_CLSSFCTN"])
            # page.get_by_role("button", name="Search", exact=True).click()
            # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ELMNT_CLSSFCTN"], exact=True).click()
            # page.get_by_role("button", name="OK").click()
            page.get_by_label("ClassificationName").first.type(datadictvalue["C_ELMNT_CLSSFCTN"])
            page.get_by_label("ClassificationName").press("Tab")
            page.wait_for_timeout(3000)

            page.get_by_role("combobox", name="Add or Subtract").nth(0).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ELMNT_CLSSFCTN_ADD_SBTRCT"], exact=True).nth(0).click()
            page.wait_for_timeout(2000)


        if datadictvalue["C_ELMNT_FDS"] != 'N/A' or '':
            page.locator("//span[text()='Edit']//preceding::img[3]").click()
            page.wait_for_timeout(3000)
            #Select Elemenet Name
            # page.get_by_title("Search: Element Name").nth(0).click()
            # page.get_by_role("link", name="Search...").click()
            # page.get_by_role("textbox", name="Element Name").fill(datadictvalue["C_ELMNT_FDS"])
            # page.get_by_role("button", name="Search", exact=True).click()
            # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ELMNT_FDS"], exact=True).click()
            # page.get_by_role("button", name="OK").click()
            page.get_by_label("Element Name").first.type(datadictvalue["C_ELMNT_FDS"])
            page.wait_for_timeout(5000)
            page.get_by_role("cell", name="InputValueName", exact=True).locator("a").click()
            page.wait_for_timeout(1000)
            page.get_by_role("cell", name="InputValueName", exact=True).locator("a").click()
            page.wait_for_timeout(1000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_INPUT_VALUE"], exact=True).nth(0).click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Add or Subtract").nth(0).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ADD_SBTRCT"], exact=True).nth(0).click()
            page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        if i == rowcount:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Submit").click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Done").click()
            page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Custom Balance Feeds Saved Successfully")
            datadictvalue["RowStatus"] = "Custom Balance Feeds are added successfully"
        except Exception as e:
            print("Custom Balance Feeds not saved")
            datadictvalue["RowStatus"] = "Custom Balance Feeds not added"

    page.wait_for_timeout(3000)
    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_DFRD_BLNCE_FEEDS, CSTM_BLNC_FDS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_DFRD_BLNCE_FEEDS, CSTM_BLNC_FDS, PRCS_DIR_PATH + PAYROLL_DFRD_BLNCE_FEEDS)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_DFRD_BLNCE_FEEDS, CSTM_BLNC_FDS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_DFRD_BLNCE_FEEDS)[0] + "_" +CSTM_BLNC_FDS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_DFRD_BLNCE_FEEDS)[0] + "_" +CSTM_BLNC_FDS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))