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
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Common Lookups")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Common Lookups").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_label("Meaning").click()
        page.get_by_label("Meaning").type(datadictvalue["C_LKP_TYPE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.get_by_text(datadictvalue["C_LKP_TYPE"], exact=True).first.click()
        page.get_by_role("button",name="New").nth(1).click()
        page.wait_for_timeout(3000)
        page.get_by_label("Lookup Code", exact=True).type(datadictvalue["C_LKP_CODE"])
        page.get_by_label("Display Sequence").first.type(str(datadictvalue["C_DSPLY_SQNC"]))
        # page.locator("//span[text()='Start Date']//following::input[4]").click()
        page.get_by_role("table", name='selected lookup type').get_by_role("row").first.get_by_role("cell", name="Start Date").locator("input").first.click()
        page.wait_for_timeout(2000)
        page.get_by_role("table", name='selected lookup type').get_by_role("row").first.get_by_role("cell", name="Start Date").locator("input").first.type(datadictvalue["C_START_DATE"].strftime('%m/%d/%y'))
        page.get_by_role("table", name='selected lookup type').get_by_role("row").first.get_by_role("cell", name="End Date").locator("input").first.click()
        page.wait_for_timeout(2000)
        page.get_by_role("table", name='selected lookup type').get_by_role("row").first.get_by_role("cell", name="End Date").locator("input").first.type(datadictvalue["C_END_DATE"].strftime('%m/%d/%y'))
        page.get_by_role("cell", name="Meaning", exact=True).nth(1).get_by_label("Meaning").type(datadictvalue["C_LKP_CODE_MNNG"])
        page.get_by_label("Description").nth(1).click()
        page.get_by_label("Description").nth(1).type(datadictvalue["C_LKP_TYPE_DSCRPTN"])
        page.get_by_label("Tag").first.type(datadictvalue["C_TAG"])
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        try:
            expect(page.get_by_role("link", name="Manage Common Lookups")).to_be_visible()
            print("Bargaining Unit Saved Successfully")
            datadictvalue["RowStatus"] = "Bargaining Unit Saved"
        except Exception as e:
            print("Unable to save Bargaining Unit")
            datadictvalue["RowStatus"] = "Unable to save Bargaining Unit"
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Bargaining Unit Added Successfully"
        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, BARGAINING_UNIT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, BARGAINING_UNIT, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, BARGAINING_UNIT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0]+ "_" + BARGAINING_UNIT)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + BARGAINING_UNIT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

