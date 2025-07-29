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
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Legal Entity")
    page.get_by_role("textbox").press("Enter")

    # Looping the values based on excel rows
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        # Navigating to Manage Legal Entity page & Entering the data
        page.get_by_role("link", name="Manage Legal Entity", exact=True).click()
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Legal Entity Identifier").click()
        page.get_by_label("Legal Entity Identifier").fill(datadictvalue["C_LEGAL_ENTTY_IDNTFR"])
        page.get_by_placeholder("m/d/yy").nth(0).clear()
        page.get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_START_DATE"])
        page.get_by_placeholder("m/d/yy").nth(1).clear()
        page.get_by_placeholder("m/d/yy").nth(1).fill(datadictvalue["C_END_DATE"])
        page.get_by_label("Place of Registration").fill(datadictvalue["C_PLACE_OF_RGSTRTN"])
        page.get_by_label("Legal Address").click()
        page.get_by_title("Search: Legal Address").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Address Line").click()
        page.get_by_label("Address Line").fill(datadictvalue["C_ADDRSS_LINE1"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ADDRSS_LINE1"]).nth(0).click()
        page.get_by_role("button", name="OK").click()
        page.get_by_label("EIN or TIN").click()
        page.get_by_label("EIN or TIN").fill(datadictvalue["C_EIN_OR_TIN"])
        page.get_by_label("Legal Reporting Unit").click()
        page.get_by_label("Legal Reporting Unit").fill(datadictvalue["C_LEGAL_RPRTNG_UNIT_RGSTRTN_NMBR"])
        if datadictvalue["C_PYRLL_STTTRY_UNIT"] == "Yes":
            page.get_by_text("Payroll statutory unit", exact=True).check()
        if datadictvalue["C_LEGAL_EMPLYR"] == "Yes":
            page.get_by_text("Legal employer").check()

        # Saving and closing the record
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(8000)

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Legal Entity created successfully")
            datadictvalue["RowStatus"] = "Successfully Added Legal Entity"

        except Exception as e:
            print("Unable to save the Legal Entity")
            datadictvalue["RowStatus"] = "Unable to save the Legal Entity"

    # Signout from the application
    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, LEGAL_ENTITY_SHEET):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, LEGAL_ENTITY_SHEET, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, LEGAL_ENTITY_SHEET)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + LEGAL_ENTITY_SHEET)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
                0] + "_" + LEGAL_ENTITY_SHEET + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
