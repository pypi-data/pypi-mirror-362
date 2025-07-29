from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("My Client Groups", exact=True).click()
    page.get_by_role("link", name="Performance").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Performance Roles").click()
    page.wait_for_timeout(5000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        # Click on Add Button
        page.get_by_label("Add").click()
        page.wait_for_timeout(4000)

        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_ROLE"])
        page.wait_for_timeout(1000)
        #page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        #page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Role Type").click()
        page.get_by_role("row", name=datadictvalue["C_ROLE_TYPE"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Status").click()
        page.get_by_role("row", name=datadictvalue["C_STTS"], exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_text("From Date").click()
        page.get_by_label("From Date").fill(datadictvalue["C_FROM_DATE"])
        page.get_by_label("From Date").press("Tab")
        page.wait_for_timeout(1000)
        page.get_by_text("To Date").click()
        page.get_by_label("To Date").fill(datadictvalue["C_TO_DATE"])
        page.get_by_label("To Date").press("Tab")
        page.wait_for_timeout(1000)
        if datadictvalue["C_TO_DATE"] !="":
            page.get_by_role("checkbox", name="Allow role to view worker, manager and participant ratings, comments and questionnaires").check()
            page.wait_for_timeout(1000)
        # Submit the Record (SUBMIT)
        page.get_by_role("button", name="Submit").click()


        page.wait_for_timeout(5000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Performance Roles")).to_be_visible()
            print("Performance Roles Saved Successfully")
            datadictvalue["RowStatus"] = "Performance Roles Submitted Successfully"
        except Exception as e:
            print("Review Periods not saved")
            datadictvalue["RowStatus"] = "Performance Roles not submitted"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, PERFORMANCE_ROLE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, PERFORMANCE_ROLE, PRCS_DIR_PATH + PERF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PERF_CONFIG_WRKBK, PERFORMANCE_ROLE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0] + "_" + PERFORMANCE_ROLE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
