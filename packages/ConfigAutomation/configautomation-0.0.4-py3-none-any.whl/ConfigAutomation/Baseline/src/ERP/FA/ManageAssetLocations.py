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
    page.get_by_role("textbox").fill("Manage Asset Locations")
    page.get_by_role("button", name="Search").click()


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("link", name="Manage Asset Locations").click()

    # Configuring country
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(3000)
        if page.get_by_label("Country").is_visible():
            if datadictvalue["C_CNTRY"]!= '':
                page.get_by_title("Search: Country").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Value").click()
                page.get_by_label("Value").fill(datadictvalue["C_CNTRY"])
                page.wait_for_timeout(3000)
                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
                page.get_by_role("cell", name=datadictvalue["C_CNTRY"]).nth(1).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)

        # Configuring State
        if page.get_by_label("State/County").is_visible():
            if datadictvalue["C_STATE_CNTY"] != '':
                page.get_by_role("button", name="Add Row").click()
                page.get_by_title("Search: State/County").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Value").click()
                page.get_by_label("Value").fill(datadictvalue["C_STATE_CNTY"])
                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
                page.get_by_role("cell", name=datadictvalue["C_STATE_CNTY"]).nth(1).click()
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)

        # Configuring City
        if page.get_by_label("City").is_visible():
            if datadictvalue["C_CITY"] != '':
                page.get_by_role("button", name="Add Row").click()
                page.get_by_title("Search: City").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Value").click()
                page.get_by_label("Value").fill(datadictvalue["C_CITY"])
                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
                page.get_by_role("cell", name=datadictvalue["C_CITY"]).nth(1).click()
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)

        #Configuring Campus
        # if page.get_by_label("Campus").is_visible():
        #     page.get_by_title("Search: Campus").click()
        #     page.get_by_role("link", name="Search...").click()
        #     page.get_by_label("Value").click()
        #     page.get_by_label("Value").fill(datadictvalue[""])
        #     page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        #     page.get_by_role("cell", name=datadictvalue[""]).nth(1).click()
        #     page.wait_for_timeout(3000)
        #     page.get_by_role("button", name="OK").click()
        #     page.wait_for_timeout(3000)

        # Configuring Building
        #page.get_by_role("button", name="Add Row").click()
        if page.get_by_label("Building").is_visible():
            if datadictvalue["C_BLDNG"]!='':
                page.get_by_title("Search: Building").click()
                page.wait_for_timeout(3000)
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Value").click()
                page.get_by_label("Value").fill(datadictvalue["C_BLDNG"])
                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
                page.wait_for_timeout(3000)
                page.get_by_role("cell", name=datadictvalue["C_BLDNG"]).nth(1).click()
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)

        # Configuring Floor
        # if page.get_by_label("Floor").is_visible():
        #     page.get_by_title("Search: Floor").click()
        #     page.get_by_role("link", name="Search...").click()
        #     page.get_by_label("Value").click()
        #     page.get_by_label("Value").fill(datadictvalue[""])
        #     page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        #     page.get_by_role("cell", name=datadictvalue[""]).nth(1).click()
        #     page.wait_for_timeout(3000)
        #     page.get_by_role("button", name="OK").click()
        #     page.wait_for_timeout(3000)

        if datadictvalue['C_ENBLD'] == 'Yes':
            page.locator("//span[text()='Enabled']//following::label[contains(@id,'Label0')]").click()
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(3000)


        i = i + 1

        try:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Manage Asset Location Saved Successfully")
            datadictvalue["RowStatus"] = "Manage Asset Location saved successfully"

        except Exception as e:
            print("Manage Asset Location not saved")
            datadictvalue["RowStatus"] = "Manage Asset Location not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_ASSET_LOCATION):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_ASSET_LOCATION, PRCS_DIR_PATH + FA_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + FA_WORKBOOK, MANAGE_ASSET_LOCATION)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANAGE_ASSET_LOCATION)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[
            0] + "_" + MANAGE_ASSET_LOCATION + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))