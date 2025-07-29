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
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox").type("Configure Default Benefits Relationships")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        page.get_by_role("link", name="Configure Default Benefits Relationships").first.click()
        page.wait_for_timeout(4000)

        #Configure Default Benefits Relationships
        page.get_by_role("button", name="New").click()
        page.wait_for_timeout(4000)
        page.get_by_role("table", name=' Configure Default Benefits Relationships').get_by_role("row").first.locator("a").first.click()
        page.wait_for_timeout(1000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_USAGE"]).click()
        page.wait_for_timeout(2000)
        page.get_by_role("table", name=' Configure Default Benefits Relationships').get_by_role("row").first.locator("a").nth(1).click()
        page.wait_for_timeout(1000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CNTRY"], exact=True).click()
        page.get_by_placeholder("mm-dd-yyyy").first.fill("")
        page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_FROM_DATE"])
        page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
        page.get_by_placeholder("mm-dd-yyyy").nth(1).fill("")
        page.get_by_placeholder("mm-dd-yyyy").nth(1).type(datadictvalue["C_TO_DATE"])
        page.get_by_placeholder("mm-dd-yyyy").nth(1).press("Tab")
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(6000)
        page.get_by_role("button", name="Done").click()
        page.wait_for_timeout(6000)
        i = i + 1

        try:
            expect(page.get_by_role("link", name="Configure Default Benefits Relationships").first).to_be_visible()
            print("Added Configure Default Benefits Relationships Saved Successfully")
            datadictvalue["RowStatus"] = "Added Configure Default Benefits Relationships"
        except Exception as e:
            print("Unable to save Configure Default Benefits Relationships")
            datadictvalue["RowStatus"] = "Unable to Add Configure Default Benefits Relationships"


    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_RELATIONSHIP):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_RELATIONSHIP,
                             PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_RELATIONSHIP)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_RELATIONSHIP)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[
            0] + "_" + BENEFIT_RELATIONSHIP + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


