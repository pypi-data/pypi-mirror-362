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
    page.get_by_role("textbox").fill("Manage Resources")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Resources", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        #Search the Resource name

        page.get_by_label("Person Name").fill(datadictvalue["C_PRSN_NAME"])
        page.get_by_role("combobox", name="Usage").click()
        page.get_by_text(datadictvalue["C_USAGE"]).click()
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name=datadictvalue["C_PRSN_NAME"]).nth(1).click()
        page.get_by_role("button", name="Add as Resource").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        #Add the Resource Information

        # page.get_by_role("row", name="*From Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"])
        page.locator("//label[text()='From Date']//following::input[1]").nth(0).fill(datadictvalue["C_FROM_DATE"])
        if datadictvalue["C_TO_DATE"]!= '':
            # page.get_by_role("row", name="To Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"].strftime("%m/%d/%Y"))
            page.locator("//label[text()='To Date']//following::input[1]").nth(0).fill(datadictvalue["C_FROM_DATE"])
        page.get_by_title("Search: Set").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Reference Data Set Code").fill(datadictvalue["C_SET"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("cell", name=datadictvalue["C_SET"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Sales Credit Type").fill(str(datadictvalue["C_SALES_CRDT_TYPE"]))
        page.get_by_title("Search: Organization").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Organization").fill(datadictvalue["C_ORGNZTN"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ORGNZTN"]).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Role").click()
        page.get_by_text(datadictvalue["C_ROLES"]).click()
        page.get_by_label("Sales Tax Geography").fill(datadictvalue["C_SALES_TAX_GGRPHY"])
        if datadictvalue["C_INSD_CITY_LMTS"] == 'Yes':
            page.get_by_text("Inside City Limits").check()
        if datadictvalue["C_INSD_CITY_LMTS"] != 'Yes':
            page.get_by_text("Inside City Limits").uncheck()

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Done").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Resources saved Successfully")
            datadictvalue["RowStatus"] = "Resources added successfully"

        except Exception as e:
            print("Resources not saved")
            datadictvalue["RowStatus"] = "Resources not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, RESOURCES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, RESOURCES,
                             PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, RESOURCES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[0] + "_" + RESOURCES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[
            0] + "_" + RESOURCES + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))