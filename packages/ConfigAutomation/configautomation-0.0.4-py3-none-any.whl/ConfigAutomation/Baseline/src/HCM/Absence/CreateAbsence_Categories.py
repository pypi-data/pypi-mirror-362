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

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Absence Categories")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Absence Categories", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        # Effective Start
        if datadictvalue["C_EFFCTV_DATE"] != '':
            page.get_by_placeholder("m/d/yy").clear()
            page.get_by_placeholder("m/d/yy").type(datadictvalue["C_EFFCTV_DATE"])

        # Name
        if datadictvalue["C_NAME"]!='':
            page.get_by_label("Name").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Yes").click()
            page.get_by_label("Name").clear()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])

        # Description
        if datadictvalue["C_DSCRPTN"]!='':
            page.get_by_label("Description").clear()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        # Legislation
        if datadictvalue["C_LGSLTN"] != '':
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Legislation").click()
            page.get_by_text(datadictvalue["C_LGSLTN"], exact=True).click()

        # Status
        if datadictvalue["C_STTS"] != '':
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Status").click()
            page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

        # Save the Record
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(3000)

        # Associated Types
        page.get_by_role("button", name="Select and Add").click()
        page.wait_for_timeout(2000)
        #page.get_by_title("Search: Absence Type").click()
        #page.get_by_role("link", name="Search...").click()
        #page.wait_for_timeout(2000)
        page.get_by_label("Absence Type").click()
        page.get_by_label("Absence Type").fill(datadictvalue["C_TYPE"])
        #page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        #page.get_by_role("cell", name=datadictvalue["C_TYPE"], exact=True).locator("span").click()
        #page.get_by_role("cell", name=datadictvalue["C_TYPE"], exact=True).locator("span").click()
        #page.get_by_role("button", name="OK").nth(1).click()
        #page.wait_for_timeout(2000)

        # Status
        page.get_by_role("combobox", name="Status").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ASSCTD_STTS"], exact=True).click()

        # Clicking on Ok button
        page.get_by_role("button", name="OK").click()

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("heading", name="Absence Categories")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Absence Categories Created Successfully")
            datadictvalue["RowStatus"] = "Created Absence Categories Successfully"
        except Exception as e:
            print("Unable to Save Absence Categories")
            datadictvalue["RowStatus"] = "Unable to Save Absence Categories"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_CATEGORIES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_CATEGORIES,PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_CATEGORIES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




