from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.get_by_label("", exact=True).fill("Manage Journal Reversal Criteria Sets")
    page.get_by_role("button", name="Search").click()
    # page.pause()
    page.get_by_role("link", name="Manage Journal Reversal Criteria Sets").click()


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Create").click()
        page.get_by_label("Name").click()

        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        page.get_by_role("cell", name=datadictvalue["C_NAME"],exact=True).click()
        page.get_by_role("button", name="Edit").click()
        page.wait_for_timeout(3000)

        if page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).is_visible():
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_CTGRY"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).fill(datadictvalue["C_CTGRY"])
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).press("Enter")
            page.wait_for_timeout(4000)

        # page.locator("//div[@title='Journal Reversal Criteria']//following::input[1]").click()
        # page.locator("//div[@title='Journal Reversal Criteria']//following::input[1]").fill(datadictvalue["C_CTGRY"])
        # page.locator("//div[@title='Journal Reversal Criteria']//following::input[1]").press("Enter")

        page.get_by_role("cell", name=datadictvalue["C_CTGRY"]).nth(1).click()
        page.get_by_label("Reversal Period").select_option(datadictvalue["C_RVRSL_PRD"])
        page.wait_for_timeout(2000)

        page.get_by_label("Meaning").select_option(datadictvalue["C_RVRSL_MTHD"])
        page.get_by_label("AutorevUIFlag").select_option(datadictvalue["C_ATMTC_RVRSL_OPTN"])

        try:
            expect(page.locator("//span[text()='Reversal Date']//following::select[@title='First day']")).to_be_visible()
            page.get_by_label("Reversal Date").click()
            page.get_by_label("Reversal Date").select_option(datadictvalue["C_RVRSL_DATE"])
            page.wait_for_timeout(5000)
        except Exception as e:
            page.get_by_role("button", name="Save and Close").click()
            # page.get_by_role("button", name="Cancel").click()

        # page.get_by_role("button", name="Save and Close")

        page.wait_for_timeout(5000)

        i = i + 1
        print("Row Added - ", str(i))

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Journal Reversal Added Successfully")
        datadictvalue["RowStatus"] = "Journal Reversal Added Successfully"
    except Exception as e:
        print("Journal Reversal Added UnSuccessfully")
        datadictvalue["RowStatus"] = "Journal Reversal Added UnSuccessfully"


    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, MANAGE_JRNL_REVERSALSETS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, MANAGE_JRNL_REVERSALSETS, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, MANAGE_JRNL_REVERSALSETS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + LEGAL_ENTITY_SHEET)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
                0] + "_" + LEGAL_ENTITY_SHEET + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))