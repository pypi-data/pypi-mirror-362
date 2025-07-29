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
    page.wait_for_timeout(5000)

    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Candidate Dimension Source Names")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("row", name="Candidate Dimension Source Names Task").get_by_role("link").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(2000)

        # Sequence
        page.get_by_role("row", name="Sequence SourceName").get_by_label("Sequence").clear()
        page.get_by_role("row", name="Sequence SourceName").get_by_label("Sequence").type(str(datadictvalue["C_DSPLY_SQNC"]))
        page.wait_for_timeout(2000)
        # Name
        page.get_by_role("row", name="Sequence SourceName").get_by_label("SourceName").clear()
        page.get_by_role("row", name="Sequence SourceName").get_by_label("SourceName").type(datadictvalue["C_NAME"])
        page.wait_for_timeout(2000)
        # Save the Record
        page.get_by_role("button", name="Save",exact=True).click()

        try:
            expect(page.get_by_role("heading", name="Search")).to_be_visible()
            print("Candidate Dimension Source Names Saved Successfully")
            datadictvalue["RowStatus"] = "Candidate Dimension Source Names Saved Successfully"
        except Exception as e:
            print("Candidate Dimension Source Names not saved")
            datadictvalue["RowStatus"] = "Candidate Dimension Source Names not added"

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(3000)



    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + Recruiting_CONFIG_WRKBK, SOURCES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + Recruiting_CONFIG_WRKBK, SOURCES,PRCS_DIR_PATH + Recruiting_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + Recruiting_CONFIG_WRKBK, SOURCES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", Recruiting_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", Recruiting_CONFIG_WRKBK)[0] + "_" + SOURCES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

