from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    # Login to the instance
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.wait_for_timeout(1000)
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    # Navigation
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Key Flexfields")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Key Flexfields").click()
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Search", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Manage Key Flexfields - Search
        if datadictvalue["C_KEY_FLXFLD_CODE"] != '':
            page.get_by_label("Key Flexfield Code").click()
            page.get_by_label("Key Flexfield Code").fill(datadictvalue["C_KEY_FLXFLD_CODE"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
        # Manage Structure
            page.get_by_role("button", name="Manage Structures").click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)

        # Create Key Flexfield Structure
            page.get_by_label("Structure Code").click()
            page.get_by_label("Structure Code").fill(str(datadictvalue["C_STRCTR_CODE"]))
            page.wait_for_timeout(3000)
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.wait_for_timeout(3000)
            if datadictvalue["C_DSCRPTN"] != '':
                page.get_by_label("Description").click()
                page.get_by_label("Description").fill(str(datadictvalue["C_DSCRPTN"]))
            page.get_by_label("Delimiter").click()
            page.get_by_label("Delimiter").select_option(datadictvalue["C_DLMTR"])
            page.wait_for_timeout(3000)
            if datadictvalue["C_ENBLD"] == 'Yes':
                page.get_by_text("Enabled").first.check()
            if datadictvalue["C_ENBLD"] == 'No':
                page.get_by_text("Enabled").first.uncheck()
                page.wait_for_timeout(3000)
            # Save
            page.get_by_role("button", name="Save", exact=True).click()
            page.wait_for_timeout(5000)

            # Segments
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Segment Code").click()
            page.get_by_label("Segment Code").fill(str(datadictvalue["C_SGMNT_CODE"]))
            page.wait_for_timeout(3000)
            if datadictvalue["C_API_NAME"] != '':
                page.get_by_label("API Name").click()
                page.get_by_label("API Name").clear()
                page.wait_for_timeout(3000)
                page.get_by_label("API Name").fill(str(datadictvalue["C_API_NAME"]))
                page.get_by_label("Name", exact=True).click()
                page.get_by_label("Name", exact=True).fill(str(datadictvalue["C_S_NAME"]))
                page.wait_for_timeout(3000)
            if datadictvalue["C_DSCRPTN"] != '':
                page.get_by_label("Description").click()
                page.get_by_label("Description").fill(datadictvalue["C_S_DSCRPTN"])
                page.wait_for_timeout(3000)
            page.get_by_label("Sequence Number").click()
            page.get_by_label("Sequence Number").fill(str(datadictvalue["C_SQNC"]))
            page.wait_for_timeout(3000)
            page.get_by_label("Prompt", exact=True).click()
            page.get_by_label("Prompt", exact=True).fill(str(datadictvalue["C_PRMPT"]))
            page.wait_for_timeout(3000)
            page.get_by_label("Short Prompt").click()
            page.get_by_label("Short Prompt").fill(str(datadictvalue["C_SHORT_PRMPT"]))
            page.wait_for_timeout(3000)
            if datadictvalue["C_S_ENBLD"] == 'Yes':
                page.get_by_text("Enabled").check()
            if datadictvalue["C_S_ENBLD"] == 'No':
                page.get_by_text("Enabled").uncheck()
                page.wait_for_timeout(3000)
            page.get_by_label("Display Width").click()
            page.get_by_label("Display Width").fill(str(datadictvalue["C_DSPLY_WIDTH"]))
            page.wait_for_timeout(3000)
            if datadictvalue["C_RANGE_TYPE"] != '':
                page.get_by_label("Range Type").select_option(datadictvalue["C_RANGE_TYPE"])
            page.wait_for_timeout(3000)
            if datadictvalue["C_CLMN"] != '':
                page.get_by_label("Column Name").click()
                page.get_by_title("Search: Column Name").click()
                page.get_by_text(str(datadictvalue["C_CLMN"])).click()
                page.wait_for_timeout(3000)
            if datadictvalue["C_DFLT_VALUE_SET_CODE"] != '':
                page.get_by_label("Default Value Set Code").click()
                page.get_by_label("Default Value Set Code").fill(str(datadictvalue["C_DFLT_VALUE_SET_CODE"]))
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Done").click()
            page.wait_for_timeout(3000)

            if datadictvalue["C_STRTR_INSTC_CODE"] != '':
                page.get_by_role("button", name="Manage Structure Instances").click()
                page.get_by_role("button", name="Create").click()
                page.wait_for_timeout(3000)
                page.get_by_label("Structure Instance Code").click()
                page.get_by_label("Structure Instance Code").fill(str(datadictvalue["C_STRTR_INSTC_CODE"]))
                page.wait_for_timeout(3000)
            page.get_by_label("API name").click()
            page.get_by_label("API name").clear()
            page.wait_for_timeout(3000)
            page.get_by_label("API name").fill(str(datadictvalue["C_SI_API_NAME"]))
            page.wait_for_timeout(3000)
            page.get_by_label("Name", exact=True).click()
            page.get_by_label("Name", exact=True).fill(str(datadictvalue["C_SI_NAME"]))
            page.wait_for_timeout(3000)
            if datadictvalue["C_SI_DSCRPTN"] != '':
                page.get_by_label("Description").click()
                page.get_by_label("Description").fill(datadictvalue["C_SI_DSCRPTN"])
                page.wait_for_timeout(3000)
            if datadictvalue["C_SI_ENBLD"] == 'Yes':
                page.get_by_text("Enabled").check()
            if datadictvalue["C_SI_ENBLD"] == 'No':
                page.get_by_text("Enabled").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_DYNMC_CMBTN_CRTN_ALLWD"] == 'Yes':
                page.get_by_text("Dynamic combination creation").check()
            if datadictvalue["C_DYNMC_CMBTN_CRTN_ALLWD"] == 'No':
                page.get_by_text("Dynamic combination creation").uncheck()
                page.wait_for_timeout(3000)
            page.get_by_label("Structure Name").select_option(str(datadictvalue["C_STRTR_NAME"]))
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
        page.get_by_role("button", name="Done").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Done").click()
        page.wait_for_timeout(3000)

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Key FlexFields Saved Successfully")
            datadictvalue["RowStatus"] = "Key FlexFields added Successfully"

        except Exception as e:
            print("Key FlexFields not saved")
            datadictvalue["RowStatus"] = "Key FlexFields not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_KFF):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_KFF, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_KFF)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH +
                               re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + MANAGE_KFF)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" +
                     MANAGE_KFF + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
