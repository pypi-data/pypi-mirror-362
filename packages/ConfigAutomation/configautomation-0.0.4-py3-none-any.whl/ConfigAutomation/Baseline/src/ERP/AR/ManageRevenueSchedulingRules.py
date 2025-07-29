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
    page.get_by_role("textbox").fill("Manage Revenue Scheduling Rules")
    # page.get_by_role("textbox").fill("Manage Value Sets")  #
    page.get_by_role("button", name="Search").click()
    # page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Revenue Scheduling Rules", exact=True).click()  #

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create").click()
        page.locator("//div[text()='Create Revenue Scheduling Rule']//following::label[text()='Set']//following::input[1]").click()
        page.locator("//div[text()='Create Revenue Scheduling Rule']//following::label[text()='Set']//following::input[1]").type(datadictvalue["C_SET"])
        page.wait_for_timeout(3000)
        page.get_by_role("option", name="COMMON Common Set").click()
        page.locator("//div[text()='Create Revenue Scheduling Rule']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_NAME"])
        page.locator("//div[text()='Create Revenue Scheduling Rule']//following::label[text()='Description']//following::input[1]").fill(datadictvalue["C_DSCRPTN"])
        if datadictvalue["C_ACTV"] == 'Yes':
            if not page.locator("[id=\"__af_Z_window\"]").get_by_text("Active").is_checked():
                page.locator("[id=\"__af_Z_window\"]").get_by_text("Active").click()
        elif datadictvalue["C_ACTV"] == 'No':
            if page.locator("[id=\"__af_Z_window\"]").get_by_text("Active").is_checked():
                page.locator("[id=\"__af_Z_window\"]").get_by_text("Active").click()
        page.wait_for_timeout(3000)
        page.locator("//div[text()='Create Revenue Scheduling Rule']//following::label[text()='Type']//following::select[1]").click()
        page.locator("//div[text()='Create Revenue Scheduling Rule']//following::label[text()='Type']//following::select[1]").select_option(datadictvalue["C_TYPE"])
        page.wait_for_timeout(3000)
        if datadictvalue["C_NMBR_OF_PRDS"] != "":
            page.locator("//div[text()='Create Revenue Scheduling Rule']//following::label[text()='Number of Periods']//following::input[1]").click()
            page.locator("//div[text()='Create Revenue Scheduling Rule']//following::label[text()='Number of Periods']//following::input[1]").fill(str(datadictvalue["C_NMBR_OF_PRDS"]))
        if datadictvalue["C_DFRRD_RVN"] == 'Yes':
            page.get_by_text("Deferred revenue", exact=True).click()
        page.get_by_label("Context Value").click()
        page.get_by_role("heading", name="Schedule", exact=True).click()
        page.get_by_role("button", name="Done").click()


        i = i + 1
    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(2000)


    # Validation
    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("AR-Revenue Schedule Rules Executed Successfully")

    except Exception as e:
        print("AR-Revenue Schedule Rules Executed UnSuccessfully")
    page.get_by_role("button", name="Done").click()

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, REVENUE_SCHDLNG_RULES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, REVENUE_SCHDLNG_RULES, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, REVENUE_SCHDLNG_RULES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + REVENUE_SCHDLNG_RULES)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + REVENUE_SCHDLNG_RULES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
