from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Journal Categories")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Journal Categories", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Name").first.click()
        page.get_by_label("Name").first.fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(1000)
        page.get_by_label("Category Key").first.fill(datadictvalue["C_CTGRY_KEY"])
        page.wait_for_timeout(1000)
        page.get_by_label("Description").first.fill(datadictvalue["C_DSCRPTN"])

        if datadictvalue["C_EXCLD_FROM_MNL_JRNL"] == 'Yes':
            page.wait_for_timeout(2000)
            page.locator("//span[text()='Exclude from Manual Journal Entry']//following::label[contains(@id,'Checkbox')]").first.check()
        if datadictvalue["C_EXCLD_FROM_MNL_JRNL"] == 'No' or '':
            page.wait_for_timeout(2000)
            page.locator("//span[text()='Exclude from Manual Journal Entry']//following::label[contains(@id,'Checkbox')]").first.check()

        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(3000)
        if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
            page.locator("//div[text()='Confirmation']//following::button[1]").click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1
        if i==rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
            if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
                page.locator("//div[text()='Confirmation']//following::button[1]").click()

            try:
                expect(page.get_by_role("button", name="Done")).to_be_visible()
                print("Journal Categories added successfully")

            except Exception as e:
                print("Unable to save Journal Categories")

    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, JRNL_CATEGORIES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, JRNL_CATEGORIES, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, JRNL_CATEGORIES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + JRNL_CATEGORIES)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
                0] + "_" + JRNL_CATEGORIES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))