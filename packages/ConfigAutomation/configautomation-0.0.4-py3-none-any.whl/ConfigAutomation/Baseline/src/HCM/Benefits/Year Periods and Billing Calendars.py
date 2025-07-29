from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Navigator").click()
    page.wait_for_timeout(2000)
    page.get_by_title("Benefits Administration", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.get_by_role("link", name="Year Periods and Billing").click()
    page.wait_for_timeout(4000)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_placeholder("mm-dd-yyyy").first.fill("")
        page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_START_DATE"])
        page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
        page.get_by_placeholder("mm-dd-yyyy").nth(1).fill("")
        page.get_by_placeholder("mm-dd-yyyy").nth(1).type(datadictvalue["C_END_DATE"])
        page.get_by_placeholder("mm-dd-yyyy").nth(1).press("Tab")
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Period Type").click()
        page.get_by_text(datadictvalue["C_PRD_TYPE"], exact=True).click()
        page.wait_for_timeout(2000)
        #page.get_by_role("button", name="Save").click()
        page.get_by_title("Save").click()
        page.wait_for_timeout(1000)
        page.get_by_text("Save and Close").click()
        page.wait_for_timeout(5000)
        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Year Periods and Billing Calendars")).to_be_visible()
            print("Added Year Periods and Billing Calendars Saved Successfully")
            datadictvalue["RowStatus"] = "Added Year Periods and Billing Calendars"
        except Exception as e:
            print("Unable to save Year Periods and Billing Calendars")
            datadictvalue["RowStatus"] = "Unable to Add Year Periods and Billing Calendars"


    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, PROGRAM_PLANYEARS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, PROGRAM_PLANYEARS,
                             PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, PROGRAM_PLANYEARS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + PROGRAM_PLANYEARS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[
            0] + "_" + PROGRAM_PLANYEARS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


