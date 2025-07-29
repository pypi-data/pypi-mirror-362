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
    page.wait_for_timeout(5000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Sponsors")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(1000)
    page.get_by_role("link", name="Manage Sponsors", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        #Select Name
        page.get_by_title("Manage Sponsors").click()

        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Name").click()
        page.get_by_role("textbox", name="Name").fill(datadictvalue["C_NAME"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_NAME"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        #Enter Sponsor Details
        page.get_by_role("link", name="Billing Details").click()

        if datadictvalue["C_FDRL"] == 'Yes':
            if not page.get_by_text("Federal").is_checked():
                page.get_by_text("Federal").click()
        elif datadictvalue["C_FDRL"] == 'No':
            if page.get_by_text("Federal").is_checked():
                page.get_by_text("Federal").click()
        page.wait_for_timeout(1000)

        if datadictvalue["C_SPNSR_ACCNT_NMBR"] != '':
            page.get_by_role("button", name="Add Row").click()
            page.get_by_title("Search: Account Number").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Account Number").click()
            page.get_by_role("textbox", name="Account Number").fill(str(datadictvalue["C_SPNSR_ACCNT_NMBR"]))
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SPNSR_ACCNT_NMBR"], exact=True).click()
            page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        #General Details
        page.get_by_role("link", name="General Details").click()
        page.get_by_label("Burden Schedule").fill(datadictvalue["C_BRDN_SCHDL"])

        if datadictvalue["C_TYPE"] != '':
            page.get_by_role("button", name="New").click()
            page.get_by_label("Type").fill(datadictvalue["C_TYPE"])
            page.get_by_label("Value").click()
            page.get_by_label("Value").fill(datadictvalue["C_VALUE"])
            page.get_by_label("Comments").click()
            page.get_by_label("Comments").fill(datadictvalue["C_CMMNTS"])

        # Save the data
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Done
        # page.get_by_role("button", name="Save and Close").click()
        # page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()

            print("Sponsors saved Successfully")
            datadictvalue["RowStatus"] = "Sponsors added successfully"

        except Exception as e:
            print("Sponsors not saved")
            datadictvalue["RowStatus"] = "Sponsors not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, SPONSORS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, SPONSORS,
                             PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, SPONSORS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[0] + "_" + SPONSORS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[
            0] + "_" + SPONSORS + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))