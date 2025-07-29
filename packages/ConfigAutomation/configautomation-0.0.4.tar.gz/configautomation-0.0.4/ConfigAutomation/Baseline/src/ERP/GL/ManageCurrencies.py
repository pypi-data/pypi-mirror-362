
from playwright.sync_api import Playwright, sync_playwright
from ConfigAutomation.Baseline.src.utils import *




def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Currencies")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Currencies", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_label("Currency Code").first.click()
        page.get_by_label("Currency Code").first.clear()
        page.get_by_label("Currency Code").first.fill(datadictvalue["C_CRRNCY_CODE"])

        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)

        if datadictvalue["C_ENBLD"] == 'Yes':
            page.wait_for_timeout(2000)
            page.get_by_role("table", name="Search Results").locator("label").nth(2).check()
        if datadictvalue["C_ENBLD"] == 'No':
            page.wait_for_timeout(2000)
            page.get_by_role("table", name="Search Results").locator("label").nth(2).uncheck()

        #     if not page.locator("//span[text()='Enabled']//following::label[contains(@id,'Label0')]").is_checked():
        #         page.locator("//span[text()='Enabled']//following::label[contains(@id,'Label0')]").click()
        # elif datadictvalue["C_ENBLD"] == 'No':
        #     if page.locator("//span[text()='Enabled']//following::label[contains(@id,'Label0')]").is_checked():
        #         page.locator("//span[text()='Enabled']//following::label[contains(@id,'Label0')]").click()

            page.get_by_role("button", name="Save", exact=True).click()
            page.wait_for_timeout(2000)

        i = i + 1
    page.get_by_role("button", name="Save and Close").click()



    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, CURRENCY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, CURRENCY, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, CURRENCY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + CURRENCY)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
                0] + "_" + CURRENCY + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))