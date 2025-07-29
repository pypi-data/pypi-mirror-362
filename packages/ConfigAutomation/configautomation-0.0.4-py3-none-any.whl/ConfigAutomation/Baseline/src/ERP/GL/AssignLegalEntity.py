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
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="Offering").click()
    page.get_by_text("Financials", exact=True).click()
    page.wait_for_timeout(2000)

    # Navigating to respective option in Legal Search field and searching
    page.get_by_text("Legal Structures").click()
    page.get_by_label("Search Tasks").click()
    page.get_by_label("Search Tasks").fill("Assign Legal Entities")
    page.get_by_role("button", name="Search").click()
    # page.get_by_role("link", name="Assign Legal Entities").click()
    page.get_by_role("row", name="Assign Legal Entities").get_by_role("link").nth(1).click()

    #Select Primary ledger
    page.get_by_label("Primary Ledger", exact=True).select_option("Select and Add")
    page.get_by_role("button", name="Apply and Go to Task").click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        if page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).is_visible():
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_PRMRY_LDGR"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).fill(datadictvalue["C_PRMRY_LDGR"])
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        page.get_by_role("table", name='Manage Primary Ledgers').get_by_text(datadictvalue["C_PRMRY_LDGR"]).first.click()
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        #Assign Legal entity to Ledger
        page.get_by_role("button", name="Select and Add").click()
        page.get_by_label("Legal Entity", exact=True).fill(datadictvalue["C_LEGAL_ENTTY"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LEGAL_ENTTY"]).first.click()
        page.get_by_role("button", name="Apply").click()
        page.get_by_role("button", name="Done").click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Setup: Financials")).to_be_visible()
            print("Legal entity assigned successfully")
            datadictvalue["RowStatus"] = "Successfully assigned Legal entities"

        except Exception as e:
            print("Unable to save the Legal entity assignment")
            datadictvalue["RowStatus"] = "Unable to save the Legal entity assignment"

    # Signout from the application
    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, ASSIGN_LEGAL_ENTITY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, ASSIGN_LEGAL_ENTITY, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, ASSIGN_LEGAL_ENTITY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + ASSIGN_LEGAL_ENTITY)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
            0] + "_" + ASSIGN_LEGAL_ENTITY + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))