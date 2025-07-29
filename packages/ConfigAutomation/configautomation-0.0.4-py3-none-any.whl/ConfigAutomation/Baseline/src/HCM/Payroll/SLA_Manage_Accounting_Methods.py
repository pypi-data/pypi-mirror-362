from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    #Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()

    #Navigate to SLA
    page.get_by_role("link", name="Manage Implementation Projects").click()
    page.get_by_label("Name").click()
    page.get_by_label("Name").fill("HCM Implementation Project")
    page.get_by_label("Name").press("Enter")
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="HCM Implementation Project").click()
    page.wait_for_timeout(3000)
    page.get_by_role("cell", name="Expand Task ListWorkforce Deployment", exact=True).get_by_role("link").click()
    page.wait_for_timeout(2000)
    page.get_by_role("cell", name="Expand Iterative Task ListDefine Payroll", exact=True).get_by_role("link").click()
    page.wait_for_timeout(2000)
    page.get_by_role("cell", name="Expand Task ListDefine Payroll Costing", exact=True).get_by_role("link").click()
    page.wait_for_timeout(2000)
    page.get_by_role("cell", name="Expand Task ListDefine Subledger Accounting Rules", exact=True).get_by_role("link").click()
    page.wait_for_timeout(3000)
    page.get_by_role("cell", name="Expand Task ListDefine Subledger Accounting Methods", exact=True).get_by_role("link").click()
    page.wait_for_timeout(3000)
    page.get_by_role("cell", name="Manage Accounting Methods", exact=True).click()
    page.wait_for_timeout(2000)
    page.locator("//span[text()='Manage Accounting Methods']//following::a[@title='Go to Task'][1]").click()
    page.wait_for_timeout(3000)

    page.pause()

    i = 0
    #while i < rowcount:
    datadictvalue = datadict[i]
    #Name & Description
    page.get_by_label("Expand Search").click()
    page.get_by_label("Name").click()
    page.get_by_label("Name").fill(datadictvalue["C_NAME"])
    page.get_by_role("button", name="Search", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name=datadictvalue["C_NAME"]).click()
    page.wait_for_timeout(5000)
    j = 0
    while j < rowcount:
        datadictvalue = datadict[j]
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name="Event Class", exact=True).get_by_label("Event Class").first.click()
        page.get_by_role("cell", name="Event Class", exact=True).get_by_label("Event Class").first.select_option(datadictvalue["C_EVENT_CLASS"])
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name="Event Type Search: Event Type Autocompletes on TAB", exact=True).get_by_label("Event Type").first.click()
        page.get_by_role("cell", name="Event Type Search: Event Type Autocompletes on TAB", exact=True).get_by_title("Search: Event Type").first.click()
        page.wait_for_timeout(2000)
        #page.get_by_label("Event Type").type(datadictvalue["C_EVENT_TYPE"])
        page.get_by_role("row", name=(datadictvalue["C_EVENT_TYPE"]), exact=True).get_by_role("cell").first.click()
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name="Rule Set Search: Rule Set Autocompletes on TAB", exact=True).get_by_label("Rule Set", exact=True).first.click()
        page.get_by_role("cell", name="Rule Set Search: Rule Set Autocompletes on TAB", exact=True).get_by_title("Search: Rule Set").first.click()
        page.wait_for_timeout(2000)
        page.get_by_role("cell", name=(datadictvalue["C_RULE_SET"]), exact=True).first.click()
        # page.get_by_role("link", name="Search...").click()
        # page.get_by_role("cell", name="Name Name Name Created by").get_by_label("Name").click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue(["C_RULE_SET"])).click()
        # page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        j = j + 1
    if j == rowcount:
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Activate").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Yes").click()
        page.wait_for_timeout(10000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(3000)

    # Validation
    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Payroll SLA Manage Accounting Rules Created Successfully")

    except Exception as e:
        print("Payroll SLA Manage Accounting Rules created Unsuccessfully")


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_SLA_CONFIG_WB, MAN_ACC_MTHDS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_SLA_CONFIG_WB, MAN_ACC_MTHDS, PRCS_DIR_PATH + PAYROLL_SLA_CONFIG_WB)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_SLA_CONFIG_WB, MAN_ACC_MTHDS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_SLA_CONFIG_WB)[0] + "_" +MAN_ACC_MTHDS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_SLA_CONFIG_WB)[0] + "_" +MAN_ACC_MTHDS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))