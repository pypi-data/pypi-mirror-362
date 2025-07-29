from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)

    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Specify Supplier Numbering")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Specify Supplier Numbering", exact=True).click()
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_label("Next Supplier Number").click()
        page.get_by_label("Next Supplier Number").clear()
        page.get_by_label("Next Supplier Number").fill(str(datadictvalue["C_NEXT_SPPLR_NMBR"]))

        page.get_by_role("button", name="Save and Close").click()
        if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
            page.locator("//div[text()='Confirmation']//following::button[1]").click()

        i = i + 1

    #
    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Saved Successfully")
        datadictvalue["RowStatus"] = "Saved Successfully"
    except Exception as e:
        print("Saved UnSuccessfully")
        datadictvalue["RowStatus"] = "UnSuccessfull"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, SPECIFY_SUPPLIER_NUMBERING):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, SPECIFY_SUPPLIER_NUMBERING, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, SPECIFY_SUPPLIER_NUMBERING)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + SPECIFY_SUPPLIER_NUMBERING)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
                0] + "_" +SPECIFY_SUPPLIER_NUMBERING + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))