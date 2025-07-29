from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox").type("Manage Banks")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Bank").first.click()
    page.wait_for_timeout(4000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(5000)
        page.get_by_label("Country").click()
        page.get_by_label("Country").type(datadictvalue["C_CNTRY"])
        page.get_by_label("Country").press("Tab")
        page.wait_for_timeout(3000)
        if page.get_by_role("cell", name=datadictvalue["C_CNTRY"], exact=True).first.is_visible():
            page.get_by_role("cell", name=datadictvalue["C_CNTRY"], exact=True).first.click()
            page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Bank Name", exact=True).click()
        page.get_by_label("Bank Name", exact=True).type(datadictvalue["C_BANK_NAME"])
        page.get_by_label("Description").click()
        page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])

        # page.get_by_label("Bank Code").press("Enter")
        # page.get_by_label("Bank Code").press("Enter")
        # page.get_by_label("Taxpayer ID").press("Enter")
        # page.get_by_label("Tax Registration Number").press("Enter")
        # page.get_by_label("Tax Registration Number").press("Enter")

        page.wait_for_timeout(1000)
        # page.get_by_role("button", name="Save", exact=True).click()
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)
        if page.get_by_text("Information").is_visible():
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)

        try:
            expect(page.get_by_role("heading", name="Manage Banks")).to_be_visible()
            print("Added Bank details Saved Successfully")
            datadictvalue["RowStatus"] = "Added Bank details and code"
        except Exception as e:
            print("Unable to save Bank details")
            datadictvalue["RowStatus"] = "Unable to Add Bank details and code"
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Added Bank details Successfully"
        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, MANAGE_BANK):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, MANAGE_BANK, PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK, MANAGE_BANK)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + MANAGE_BANK)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + MANAGE_BANK + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
