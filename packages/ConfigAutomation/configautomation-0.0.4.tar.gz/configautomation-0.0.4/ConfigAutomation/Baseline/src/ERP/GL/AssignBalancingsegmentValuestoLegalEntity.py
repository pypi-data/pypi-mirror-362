from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *



# Need To Run Manage Primary Ledger to create Ledger
def configure(playwright: Playwright, rowcount, datadict,videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="Offering").click()
    page.get_by_text("Financials", exact=True).click()
    page.get_by_title("Legal Structures", exact=True).click()
    page.wait_for_timeout(2000)

    page.get_by_label("Search Tasks").fill("Assign Balancing Segment Values to Legal Entities")
    page.get_by_role("button", name="Search").click()
    page.get_by_role("cell", name="Assign Balancing Segment").first.click()
    page.wait_for_timeout(2000)

    page.get_by_role("link", name="Assign Balancing Segment").first.click()
    page.get_by_label("Primary Ledger", exact=True).click()
    page.get_by_label("Primary Ledger", exact=True).select_option("Select and Add")
    page.get_by_role("button", name="Apply and Go to Task").click()
    page.wait_for_timeout(2000)

    i = 0
    while i < rowcount:

        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        if i==0:

            page.get_by_text(datadictvalue["C_LDGR"]).first.click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)


        if i >= 0:
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)
            page.get_by_title("Search: Company Value").click()
            page.get_by_text(datadictvalue["C_BLNCNG_SGMNT"]).click()
            page.wait_for_timeout(2000)
            page.get_by_title("Save and Close").click()
            page.wait_for_timeout(2000)

        if i == rowcount:
            page.get_by_role("button", name="Save and Close").click()

        try:
            expect(page.get_by_text("Search Tasks")).to_be_visible()
            print("Assign Balancing Segment Values to Legal Entities Saved Successfully")
            datadictvalue["RowStatus"] = "Assign Balancing Segment Values to Legal Entities added successfully"

        except Exception as e:
            print("Assign Balancing Segment Values to Legal Entities not saved")
            datadictvalue["RowStatus"] = "Assign Balancing Segment Values to Legal Entities not saved"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, ASSIGN_BAL_SGMT_VALUE_LE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, ASSIGN_BAL_SGMT_VALUE_LE, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, ASSIGN_BAL_SGMT_VALUE_LE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + ASSIGN_BAL_SGMT_VALUE_LE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + ASSIGN_BAL_SGMT_VALUE_LE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))