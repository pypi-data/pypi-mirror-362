from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    # Navigate to Derived Factors page
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Benefits Administration", exact=True).click()
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Benefit Groups").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(3000)

        # Benefits Group Name
        page.locator("//div[text()='Create Benefit Group']//following::label[text()='Benefits Group Name']//following::input").first.clear()
        page.locator("//div[text()='Create Benefit Group']//following::label[text()='Benefits Group Name']//following::input").first.type(datadictvalue["C_BNFT_GROUP_NAME"])

        # Benefits Group Description
        page.locator("//div[text()='Create Benefit Group']//following::label[text()='Benefits Group Description']//following::input").first.clear()
        page.locator("//div[text()='Create Benefit Group']//following::label[text()='Benefits Group Description']//following::input").first.type(datadictvalue["C_BNFT_GROUP_DSCRPTN"])

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("heading", name="Benefit Groups")).to_be_visible()
            page.wait_for_timeout(3000)
            print("User Defined Criteria Created Successfully")
            datadictvalue["RowStatus"] = "User Defined Criteria Created Successfully"
        except Exception as e:
            print("Unable to Create User Defined Criteria")
            datadictvalue["RowStatus"] = "Unable to Save User Defined Criteria"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_GROUP):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_GROUP,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_GROUP)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_GROUP)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_GROUP + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))





