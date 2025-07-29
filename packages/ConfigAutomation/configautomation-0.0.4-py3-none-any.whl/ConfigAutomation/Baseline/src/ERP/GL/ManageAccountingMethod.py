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
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Manage Accounting Method")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Accounting Methods", exact=True).click()


    i = 0

    datadictvalue = datadict[i]
    #Search Standard Accural - for dulpicating

    page.get_by_label("Expand Search").click()
    page.get_by_label("Name").click()
    page.get_by_label("Name").type("Standard Accrual")
    page.get_by_label("Description").click()
    page.get_by_label("Description").fill("Standard accrual method of accounting")
    page.get_by_role("button", name="Search", exact=True).click()
    page.get_by_role("cell", name="Standard Accrual", exact=True).click()
    page.get_by_label("Actions").locator("div").click()
    page.get_by_text("Duplicate").click()
    page.wait_for_timeout(2000)
    page.get_by_label("Name", exact=True).type(datadictvalue["C_NAME"])
    page.get_by_label("Short Name").click()
    page.wait_for_timeout(2000)
    page.get_by_label("Short Name").fill(datadictvalue["C_SHORT_NAME"])
    page.get_by_label("Description").click()
    page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
    page.wait_for_timeout(2000)
    page.get_by_title("Search: Chart of Accounts").click()
    page.get_by_text(datadictvalue["C_CHART_OF_ACCNTS"]).first.click()

    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(4000)

    j = 0
    while j < rowcount:
        datadictvalue = datadict[j]

        page.get_by_text(datadictvalue["C_EVENT_CLASS"], exact=True).click()
        page.wait_for_timeout(2000)

        j = j + 1
    if page.get_by_role("button", name="Activate").is_visible():
        page.get_by_role("button", name="Activate").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Yes").click()
        page.wait_for_timeout(10000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(3000)

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Managed Accounting Methods Successfully")

    except Exception as e:
        print("Managed Accounting Methods Unsuccessful")

    print("Row Added - ", str(j))


    OraSignOut(page, context, browser, videodir)
    return datadict


#
#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, MANAGE_ACCOUNTING_METHOD):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, MANAGE_ACCOUNTING_METHOD, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, MANAGE_ACCOUNTING_METHOD)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))