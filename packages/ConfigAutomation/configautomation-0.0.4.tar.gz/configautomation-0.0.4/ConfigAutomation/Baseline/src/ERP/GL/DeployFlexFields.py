from playwright.sync_api import Playwright, sync_playwright
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
    page.get_by_role("button", name="Offering").click()
    page.get_by_text("Financials", exact=True).click()
    page.get_by_text("Financial Reporting Structures").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Manage Chart of Accounts Structures").click()
    page.get_by_label("Module").click()
    page.get_by_label("Module").type("General ledger")
    page.get_by_label("Module").press("Enter")
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Search", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Deploy Flexfield").click()
    page.wait_for_timeout(15000)

    page.get_by_text("Entity Usages Processed:").first.click()
    print("clicked")

    i = 0
    while (i < 5):
        DeploymentStartStatus = page.get_by_text("Entity Usages Processed:").first.text_content()
        DeploymentEndStatus = "Entity Usages Processed: 36 of 36 ."
        if (DeploymentStartStatus != DeploymentEndStatus):
            print("Deployment Status", DeploymentStartStatus)
            page.wait_for_timeout(15000)
            # page.get_by_role("table", name="%").locator("span").first.click()
            # page.wait_for_timeout(5000)
            DeploymentStartStatus = page.get_by_text("Entity Usages Processed:").first.text_content()

        elif(DeploymentStartStatus == DeploymentEndStatus):
            print("Deployed Successfully")

            break

        i = i + 1

        j =0
        while (j < 5):
            if page.get_by_role("button", name="Ok").is_enabled():
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Ok").click()
                break
            else:
                page.wait_for_timeout(25000)

        j = j + 1

    Status = page.get_by_role("cell", name="Deployed", exact=True).text_content()
    print(Status)
    print("Successfully Deployed COA")
    page.get_by_role("button", name="Done").click()

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, DEPLOYFLEXFIELDS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, DEPLOYFLEXFIELDS, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, DEPLOYFLEXFIELDS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + DEPLOYFLEXFIELDS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + DEPLOYFLEXFIELDS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

