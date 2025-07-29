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
    page.get_by_role("textbox").fill("Manage Burden Schedules")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Burden Schedules", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)

        #Burden Schedules
        page.get_by_role("button", name="Add Row").first.click()
        page.wait_for_timeout(3000)
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Type").select_option(datadictvalue["C_BRDN_TYPE"])
        page.get_by_title("Search: Default Burden").click()
        page.get_by_role("link", name="Search...").click()
        # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").fill(datadictvalue["C_DFLT_BRDN_STRCTR"])
        page.locator("//div[text()='Search and Select: Default Burden Structure']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_DFLT_BRDN_STRCTR"])
        page.get_by_role("button", name="Search", exact=True).click()
        # page.get_by_role("cell", name=datadictvalue["C_DFLT_BRDN_STRCTR"], exact=True).click()
        page.get_by_role("cell", name=datadictvalue["C_DFLT_BRDN_STRCTR"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_title("Search: Default Organization").click()
        page.get_by_role("link", name="Search...").click()
        # page.get_by_role("cell", name="*Name Name Name").get_by_label("Name").fill(datadictvalue["C_DFLT_ORGNZTN_HRRCHY"])
        page.locator("//div[text()='Search and Select: Default Organization Hierarchy']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_DFLT_ORGNZTN_HRRCHY"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DFLT_ORGNZTN_HRRCHY"]).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_title("Search: Hierarchy Version").click()
        page.get_by_role("link", name="Search...").click()
        # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").fill(datadictvalue["C_BRDN_HRRCHY_VRSN"])
        page.locator("//div[text()='Search and Select: Hierarchy Version']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_HRRCHY_VRSN"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("//div[text()='Search and Select: Hierarchy Version']//following::span[text()='"+ datadictvalue["C_HRRCHY_VRSN"] +"']").first.click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_HRRCHY_VRSN"]).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_title("Search: Hierarchy Start").click()
        page.get_by_role("link", name="Search...").click()
        # page.get_by_role("cell", name="Name Name Name Classification").get_by_label("Name", exact=True).fill(datadictvalue["C_BRDN_HRRCHY_START_ORGNZTN"])
        page.locator("//div[text()='Search and Select: Hierarchy Start Organization']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_BRDN_HRRCHY_START_ORGNZTN"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BRDN_HRRCHY_START_ORGNZTN"]).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"])
        page.locator("//input[contains(@id,'inputDate2')]").first.fill(datadictvalue["C_FROM_DATE"])
        if datadictvalue["C_TO_DATE"] != '':
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"])
            page.locator("//input[contains(@id,'inputDate4')]").first.fill(datadictvalue["C_TO_DATE"])
        page.wait_for_timeout(2000)

        #Burden Schedule Versions
        page.get_by_role("button", name="Add Row").nth(1).click()
        page.wait_for_timeout(2000)
        page.get_by_label("Version", exact=True).click()
        page.get_by_label("Version", exact=True).fill(str(datadictvalue["C_VRSN"]))
        # page.get_by_role("table", name='Burden Schedule Versions').get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date").nth(1).locator("input").nth(0).fill(datadictvalue["C_BRDN_FROM_DATE"])
        page.locator("//input[contains(@id,'inputDate6')]").first.fill(datadictvalue["C_BRDN_FROM_DATE"])
        if datadictvalue["C_BRDN_TO_DATE"] != '':
            # page.get_by_role("table", name='Burden Schedule Versions').get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date").nth(1).locator("input").nth(0).fill(datadictvalue["C_BRDN_TO_DATE"])
            page.locator("//input[contains(@id,'inputDate8')]").first.fill(datadictvalue["C_BRDN_TO_DATE"])
        page.get_by_title("Search: Burden Structure").click()
        page.get_by_role("link", name="Search...").click()
        # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").clear()
        # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").fill(datadictvalue["C_BRDN_STRCTR"])
        page.locator("//div[text()='Search and Select: Burden Structure']//following::label[text()='Name']//following::input[1]").clear()
        page.locator("//div[text()='Search and Select: Burden Structure']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_BRDN_STRCTR"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name=datadictvalue["C_BRDN_STRCTR"], exact=True).first.click()
        # page.get_by_role("cell", name=datadictvalue["C_BRDN_STRCTR"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_title("Search: Organization Hierarchy").click()
        page.get_by_role("link", name="Search...").click()
        # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").clear()
        # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").fill(datadictvalue["C_ORGNZTN_HRRCHY"])
        page.locator("//div[text()='Search and Select: Organization Hierarchy']//following::label[text()='Name']//following::input[1]").clear()
        page.locator("//div[text()='Search and Select: Organization Hierarchy']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_ORGNZTN_HRRCHY"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("//div[text()='Search and Select: Organization Hierarchy']//following::span[text()='"+datadictvalue["C_ORGNZTN_HRRCHY"]+"']").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_role("table", name='Burden Schedule Versions').get_by_title("Search: Hierarchy Version").click()
        page.get_by_role("link", name="Search...").click()
        # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").clear()
        # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").fill(datadictvalue["C_BRDN_HRRCHY_VRSN"])
        page.locator("//div[text()='Search and Select: Hierarchy Version']//following::label[text()='Name']//following::input[1]").clear()
        page.locator("//div[text()='Search and Select: Hierarchy Version']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_BRDN_HRRCHY_VRSN"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("//div[text()='Search and Select: Hierarchy Version']//following::span[text()='"+datadictvalue["C_BRDN_HRRCHY_VRSN"]+"']").first.click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_role("table", name='Burden Schedule Versions').get_by_title("Search: Hierarchy Start Organization").click()
        page.get_by_role("link", name="Search...").click()
        # page.get_by_role("cell", name="Name Name Name").get_by_label("Name", exact=True).clear()
        # page.get_by_role("cell", name="Name Name Name").get_by_label("Name", exact=True).fill(datadictvalue["C_BRDN_HRRCHY_START_ORGNZTN"])
        page.locator("//div[text()='Search and Select: Hierarchy Start Organization']//following::label[text()='Name']//following::input[1]").clear()
        page.locator("//div[text()='Search and Select: Hierarchy Start Organization']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_BRDN_HRRCHY_START_ORGNZTN"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("//div[text()='Search and Select: Hierarchy Start Organization']//following::span[text()='"+datadictvalue["C_BRDN_HRRCHY_START_ORGNZTN"]+"']").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_HOLD_VRSN_FROM_BUILD"] == 'Yes':
            page.get_by_role("table", name='Burden Schedule Versions').locator("//input[@type='checkbox']").check()
        page.wait_for_timeout(2000)

        # Burden Multipliers
        page.get_by_role("button", name="Add Row").nth(2).click()
        page.wait_for_timeout(2000)
        page.get_by_title("Search: Organization", exact=True).click()
        page.get_by_role("link", name="Search...").click()
        # page.get_by_role("cell", name="Name Name Name Classification").get_by_label("Name", exact=True).clear()
        # page.get_by_role("cell", name="Name Name Name Classification").get_by_label("Name", exact=True).fill(datadictvalue["C_ORGNZTN"])
        page.locator("//div[text()='Search and Select: Organization']//following::label[text()='Name']//following::input[1]").clear()
        page.locator("//div[text()='Search and Select: Organization']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_ORGNZTN"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ORGNZTN"]).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Burden Cost Code").select_option(datadictvalue["C_BRDN_COST_CODE"])
        page.get_by_label("Multiplier", exact=True).fill(str(datadictvalue["C_MLTPLR"]))
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Burden Schedule saved Successfully")
            datadictvalue["RowStatus"] = "Burden Schedule added successfully"

        except Exception as e:
            print("Burden Schedule not saved")
            datadictvalue["RowStatus"] = "Burden Schedule not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, BRDN_SCHDL):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, BRDN_SCHDL,
                             PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, BRDN_SCHDL)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + BRDN_SCHDL)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + BRDN_SCHDL + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

