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
    page.get_by_role("textbox").fill("Manage Grants Personnel")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Grants Personnel", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Add Row").first.click()
        page.wait_for_timeout(2000)
        page.get_by_title("Search: Person Name").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_PRSN_NAME"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("cell", name=datadictvalue["C_PRSN_NAME"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        #Personnel Details
        if datadictvalue["C_PRSNNL_DTLS_PRNCPL_INVSTGTR"] == 'Yes':
            page.get_by_text("Principal investigator", exact=True).check()
        if datadictvalue["C_PRSNNL_DTLS_PRNCPL_INVSTGTR"] != 'Yes':
            page.get_by_text("Principal investigator", exact=True).uncheck()
        if datadictvalue["C_RVW_CMPLTD"] == 'Yes':
            page.get_by_text("Review completed").check()
            page.wait_for_timeout(4000)
            if datadictvalue["C_CRTFD_DATE"] != '':
                page.locator("//label[text()='Certified Date']//following::input[1]").click()
                page.locator("//label[text()='Certified Date']//following::input[1]").fill(datadictvalue["C_CRTFD_DATE"])
        if datadictvalue["C_RVW_CMPLTD"] == 'No':
            page.get_by_text("Review completed").uncheck()

        if datadictvalue["C_NAME"] != '':
            page.get_by_role("button", name="Add Row").nth(1).click()
            page.wait_for_timeout(1000)
            page.get_by_title("Search: Name").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Name").fill(datadictvalue["C_NAME"])
            page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_NAME"], exact=True).nth(0).click()
            page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)

        i = i + 1

        if i == rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(5000)
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Grants Personnel saved Successfully")
            datadictvalue["RowStatus"] = "Grants Personnel added successfully"

        except Exception as e:
            print("Grants Personnel not saved")
            datadictvalue["RowStatus"] = "Grants Personnel not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, GRANTS_PERSONNEL):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, GRANTS_PERSONNEL,
                             PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, GRANTS_PERSONNEL)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[
                                   0] + "_" + GRANTS_PERSONNEL)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[
            0] + "_" + GRANTS_PERSONNEL + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))