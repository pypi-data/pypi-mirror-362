from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    #Sign In
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    #Navigation to Invoice Holds and Releases
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Invoice Holds and Releases")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Invoice Holds and Releases", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(1000)
        page.locator("//label[text()='Type']//following::select").select_option(datadictvalue["C_TYPE"])
        page.wait_for_timeout(2000)
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_placeholder("m/d/yy").fill(datadictvalue["C_INCTV_DATE"])

        # Checkbox - Checking - Enable or Not
        try:
            expect(page.locator("[id=\"__af_Z_window\"]").get_by_text("Allow Accounting")).to_be_visible()
            if datadictvalue["C_ALLOW_ACCNTNG"] == 'Yes':
                # page.wait_for_timeout(2000)
                page.locator("[id=\"__af_Z_window\"]").get_by_text("Allow Accounting").click()

        except Exception as e:
            print("Allow Accounting Not Enabled")

        try:
            expect(page.locator("[id=\"__af_Z_window\"]").get_by_text("Allow Manual Release")).to_be_visible()
            if datadictvalue["C_ALLOW_MNL_RLS"] == 'Yes':
                # page.wait_for_timeout(2000)
                page.locator("[id=\"__af_Z_window\"]").get_by_text("Allow Manual Release").click()

        except Exception as e:
            print("Allow Manual Release Not Enabled")

        try:
            expect(page.locator("[id=\"__af_Z_window\"]").get_by_text("Allow Holds Resolution Routing")).to_be_visible()
            if datadictvalue["C_ALLOW_HOLDS_RSLTN_RTNG"] == 'Yes':
                # page.wait_for_timeout(2000)
                page.locator("[id=\"__af_Z_window\"]").get_by_text("Allow Holds Resolution Routing").click()

        except Exception as e:
            print("Allow Holds Resolution Routing Not Enabled")

        # Save and Close
        page.get_by_role("button", name="Save and Close").click()

        page.wait_for_timeout(1000)
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Row Saved Successfully")
            datadictvalue["RowStatus"] = "Row Saved Successfully"
        except Exception as e:
            print("Row Saved UnSuccessfully")
            datadictvalue["RowStatus"] = "Row Saved UnSuccessfully"

        i = i + 1

    print("Row Added - ", str(i))
    page.get_by_role("button", name="Done").click()

    try:
        expect(page.get_by_role("heading", name="Search")).to_be_visible()

        print("Invoice Holds and Releases Saved Successfully")
        datadictvalue["RowStatus"] = "Invoice Holds and Releases Saved Successfully"
    except Exception as e:
        print("Invoice Holds and Releases Saved UnSuccessfully")
        datadictvalue["RowStatus"] = "Invoice Holds and Releases Saved UnSuccessfully"
    page.wait_for_timeout(2000)
    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, INVOICE_HOLDS_RELEASES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, INVOICE_HOLDS_RELEASES, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, INVOICE_HOLDS_RELEASES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + INVOICE_HOLDS_RELEASES)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
                0] + "_" +INVOICE_HOLDS_RELEASES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))