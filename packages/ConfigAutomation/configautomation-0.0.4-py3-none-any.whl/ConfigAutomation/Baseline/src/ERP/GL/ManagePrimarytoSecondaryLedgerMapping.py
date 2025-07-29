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
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Offering").click()
    page.get_by_text("Financials", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_text("General Ledger").first.click()
    page.wait_for_timeout(2000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_label("Search Tasks").click()
        page.get_by_label("Search Tasks").fill("Primary to Secondary Ledger Mapping")
        page.get_by_role("button", name="Search").click()
        page.wait_for_timeout(2000)
        page.get_by_role("table", name='Search Task Results').get_by_role("link", name="Complete Primary to Secondary").first.click()
        page.wait_for_timeout(3000)
        page.locator("//a[text()='Complete Primary to Secondary Ledger Mapping']//following::a[1]").first.click()

        page.get_by_label("Primary Ledger", exact=True).select_option("Select and Add")
        page.wait_for_timeout(2000)
        if page.get_by_label("Secondary Ledger", exact=True).is_enabled():
            page.get_by_label("Secondary Ledger", exact=True).select_option("Select and Add")
        page.get_by_role("button", name="Apply and Go to Task").click()
        page.wait_for_timeout(2000)

        if page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).is_visible():
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_RLTD_PRMRY_LDGR"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).fill(datadictvalue["C_RLTD_PRMRY_LDGR"])
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).press("Enter")
            page.wait_for_timeout(4000)

        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RLTD_PRMRY_LDGR"]).nth(1).click()
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        page.get_by_label("Secondary Ledger", exact=True).select_option("Select and Add")
        page.get_by_role("button", name="Apply and Go to Task").click()
        page.get_by_role("table", name='Secondary Ledgers').get_by_text(datadictvalue["C_NAME"]).nth(0).click()

        page.get_by_role("button", name="Save and Close").click()

        page.get_by_label("Post Journals Automatically").select_option(datadictvalue["C_POST_JRNLS_ATMTCLLY_FROM_SRC_LDGR"])
        page.get_by_label("Retain Journal Creator from").select_option(datadictvalue["C_RTIN_JRNL_CRTR_FROM_SRC_LDGR"])
        page.get_by_role("button", name="Add Row").click()
        page.get_by_label("Journal Source").select_option(datadictvalue["C_JRNL_SRC"])
        page.get_by_label("Journal Category").select_option(datadictvalue["C_JRNL_CTGRY"])
        page.get_by_role("cell", name="Transfer Journals to This Secondary Ledger").nth(1).get_by_label("Transfer Journals to This Secondary Ledger").select_option(datadictvalue["C_TRNSFR_JRNLS_TO_SCNDRY_LDGR"])

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Successfully Mapped"
        i = i + 1

        try:
            expect(page.get_by_text("Search Tasks")).to_be_visible()
            print("Mapping PrimaryLedger to Secondary Saved Successfully")
            datadictvalue["RowStatus"] = "Mapping PrimaryLedger to Secondary Saved Successfully"
        except Exception as e:
            print("Saved UnSuccessfully")
            datadictvalue["RowStatus"] = "Saved UnSuccessfully"

        # Signout from the application
    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, MANAGE_SECONDARY_LEDGERS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, MANAGE_SECONDARY_LEDGERS,  PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, MANAGE_SECONDARY_LEDGERS )
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + MANAGE_SECONDARY_LEDGERS)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
                0] + "_" + MANAGE_SECONDARY_LEDGERS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

