from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *
from datetime import datetime


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
    page.get_by_role("textbox").fill("Manage Accounting Calendars")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Accounting Calendars", exact=True).click()

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        if datadictvalue["C_NAME"] != PrevName:
            # Save the prev type data if the row contains a new type
            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(3000)
                if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
                    page.locator("//div[text()='Confirmation']//following::button[1]").click()

                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("Accounting calendar added successfully")

                except Exception as e:
                    print("Unable to save the Accounting Calendar")

                page.wait_for_timeout(3000)

            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.get_by_placeholder("m/d/yy").fill(datadictvalue["C_START_DATE"].strftime("%m/%d/%Y"))
            page.get_by_label("Period Frequency", exact=True).select_option(datadictvalue["C_PRD_FRQNCY"])
            if datadictvalue["C_BDGTRY_CNTRL_ONLY"] == 'Yes':
                page.get_by_text("Budgetary control only").click()
            page.get_by_label("Adjusting Period Frequency").select_option(datadictvalue["C_ADJSTNG_PRD_FRQNCY"])
            page.wait_for_timeout(2000)
            page.get_by_label("User-Defined Prefix").fill(datadictvalue["C_USER_DFND_PRFX"])
            page.get_by_label("Separator").click()
            page.get_by_label("Separator").select_option(datadictvalue["C_SPRTR"])
            page.wait_for_timeout(4000)
            page.locator("//label[text()='Format']//following::select[1]").click()
            page.locator("//label[text()='Format']//following::select[1]").select_option(datadictvalue["C_FRMT_FIRST_PRD"])
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Description").fill(datadictvalue["C_PRD_DSCRPTN"])
            page.wait_for_timeout(3000)
            PeriodName=page.locator("//span[text()='Period Name']//following::input[1]").get_attribute(name='value')
            print("Name:",PeriodName)
            print("Excel:", datadictvalue["C_PRD_NAME"])
            if datadictvalue["C_PRD_NAME"] == PeriodName:
                page.get_by_role("button", name="Save", exact=True).click()
                page.wait_for_timeout(10000)
            PrevName = datadictvalue["C_NAME"]

        PeriodName = page.locator("//span[text()='Period Name']//following::input[1]").get_attribute(name='value')
        if datadictvalue["C_PRD_NAME"] != PeriodName:
            page.get_by_role("button", name="Add Year").click()
            page.wait_for_timeout(5000)
            PeriodName = page.locator("//span[text()='Period Name']//following::input[1]").get_attribute(name='value')
            print("Name:", PeriodName)
            print("Excel:", datadictvalue["C_PRD_NAME"])
            if datadictvalue["C_PRD_NAME"] == PeriodName:
                page.get_by_role("button", name="Save", exact=True).click()
                page.wait_for_timeout(15000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        if i == rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
            if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
                page.locator("//div[text()='Confirmation']//following::button[1]").click()

            try:
                expect(page.get_by_role("button", name="Done")).to_be_visible()
                print("Accounting calendar added successfully")

            except Exception as e:
                print("Unable to save the Accounting Calendar")

    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, ACC_CALENDAR):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, ACC_CALENDAR, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, ACC_CALENDAR)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + ACC_CALENDAR)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + ACC_CALENDAR + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))