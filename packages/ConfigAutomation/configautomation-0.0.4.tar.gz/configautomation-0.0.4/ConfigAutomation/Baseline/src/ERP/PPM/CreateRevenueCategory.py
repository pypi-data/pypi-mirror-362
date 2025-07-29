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
    page.get_by_role("textbox").fill("Manage Revenue Categories")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Revenue Categories", exact=True).click()

    # Create Revenue Categories
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="New").nth(1).click()
        page.wait_for_timeout(2000)
        page.get_by_label("Lookup Code", exact=True).click()
        page.get_by_label("Lookup Code", exact=True).fill(datadictvalue["C_LKP_CODE"])
        page.wait_for_timeout(1000)

        # Entering Display Sequence
        if datadictvalue["C_DSPLY_SQNC"]!= '':
            # page.get_by_role("row", name="Expand Lookup Code Display").get_by_label("Display Sequence").fill(str(datadictvalue["C_DSPLY_SQNC"]))
            page.locator("//span[text()='Display Sequence']//following::input[2]").fill(str(datadictvalue["C_DSPLY_SQNC"]))
            page.wait_for_timeout(1000)

        #  Enable flag yes or no
        if datadictvalue["C_ENBLD"] == 'Yes':
            page.get_by_role("table", name="This table lists the standard lookup codes belonging to the selected lookup type").locator("//tr//td//input[@type='checkbox']").first.check()
        if datadictvalue["C_ENBLD"] == 'No':
            page.get_by_role("table", name="This table lists the standard lookup codes belonging to the selected lookup type").locator("//tr//td//input[@type='checkbox']").first.uncheck()

        # Entering Start Date & End Date
        if datadictvalue["C_START_DATE"]!='':
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar Start Date Select Date").first.locator("input").nth(0).fill(datadictvalue["C_START_DATE"])
            page.locator("//input[contains(@id,'id2')]").nth(0).fill(datadictvalue["C_START_DATE"])

        if datadictvalue["C_END_DATE"] != '':
            # page.get_by_role("cell",name="m/d/yy Press down arrow to access Calendar End Date Select Date").first.locator("input").nth(0).fill(datadictvalue["C_END_DATE"])
            page.locator("//input[contains(@id,'id1')]").nth(0).fill(datadictvalue["C_END_DATE"].strftime('%m/%d/%y'))
        page.wait_for_timeout(2000)
        page.locator("//table[contains(@summary,'lookup codes')]").get_by_label("Meaning").first.fill(datadictvalue["C_MNNG"])
        # page.get_by_role("row", name="Expand Lookup Code Display").get_by_label("Meaning").fill(datadictvalue["C_MNNG"])
        page.wait_for_timeout(2000)

        # Entering Description
        if datadictvalue["C_DSCRPTN"]!= '':
            # page.get_by_role("row", name="Expand Lookup Code Display").get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.locator("//table[contains(@summary,'lookup codes')]").get_by_label("Description").first.fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(1000)

        # Entering Tag
        if datadictvalue["C_TAG"] != '':
            #page.get_by_role("row", name="Expand Lookup Code Display").get_by_label("Tag").fill(datadictvalue["C_TAG"])
            page.locator("//table[contains(@summary,'lookup codes')]").get_by_label("Tag").first.fill(datadictvalue["C_TAG"])
            page.wait_for_timeout(1000)

        page.get_by_role("button", name="Save", exact=True).click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1

    # Save the data
    page.get_by_role("button", name="Save and Close").click()


    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Revenue Categories Saved Successfully")
        datadictvalue["RowStatus"] = "Revenue Categories are added successfully"

    except Exception as e:
        print("Revenue Categories not saved")
        datadictvalue["RowStatus"] = "Revenue Categories are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, REV_CAT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, REV_CAT, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, REV_CAT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + REV_CAT)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + REV_CAT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    