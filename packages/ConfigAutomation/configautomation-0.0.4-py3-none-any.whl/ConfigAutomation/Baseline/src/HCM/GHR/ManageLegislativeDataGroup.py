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
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)

    page.get_by_role("textbox").fill("Manage Legislative Data Group")
    page.get_by_role("textbox").press("Enter")
    
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.get_by_role("link", name="Manage Legislative Data Group").first.click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Name").click()
        page.get_by_label("Name").type(datadictvalue["C_NAME"])
        page.get_by_label("Name").press("Enter")
        page.get_by_label("Country").click()
        page.get_by_label("Country").type(datadictvalue["C_CNTRY"])
        page.get_by_label("Country").press("Enter")
        page.wait_for_timeout(4000)
        if page.get_by_text(datadictvalue["C_CNTRY"], exact=True).is_visible():
            page.get_by_text(datadictvalue["C_CNTRY"], exact=True).click()
            page.get_by_role("button", name="OK").click()
        # page.get_by_label("Currency").click()
        # page.get_by_label("Currency").type(datadictvalue["C_CRRNCY"])
        # page.get_by_label("Currency").press("Enter")
        # page.get_by_label("Cost Allocation Structure").click()
        # page.get_by_label("Cost Allocation Structure").type(datadictvalue["C_ENTRPRS_NAME"])
        # page.get_by_label("Cost Allocation Structure").press("Enter")
        #page.get_by_title("Submit").click()
        page.get_by_title("Cancel").click()

        try:
            expect(page.get_by_role("button", name="Done").click()).to_be_visible()
            print("Added Legislative Data Group Saved Successfully")
            datadictvalue["RowStatus"] = "Added Legislative Data Group and code"
        except Exception as e:
            print("Unable to save Legislative Data Group")
            datadictvalue["RowStatus"] = "Unable to Add Legislative Data Group and code"
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Added Legislative Data Group Successfully"
        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, LDG):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, LDG, PRCS_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, LDG)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_ENTSTRUCT_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_ENTSTRUCT_CONFIG_WRKBK)[0] + "_" + LDG +  "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
