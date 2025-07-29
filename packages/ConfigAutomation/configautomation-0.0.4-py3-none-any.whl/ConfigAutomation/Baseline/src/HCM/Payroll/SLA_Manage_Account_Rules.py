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
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="HCM Implementation Project").click()
    page.wait_for_timeout(5000)
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
    page.get_by_role("cell", name="Manage Account Rules", exact=True).click()
    page.wait_for_timeout(2000)
    page.locator("//span[text()='Manage Account Rules']//following::a[@title='Go to Task'][1]").click()
    page.wait_for_timeout(4000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        #Name & Description
        page.get_by_role("button", name="Create").click()
        page.get_by_label("Name", exact=True).click()
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
        page.get_by_label("Short Name").click()
        page.get_by_label("Short Name").fill(datadictvalue["C_SHORT_NAME"])
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Chart of Accounts").click()
        page.get_by_label("Chart of Accounts").fill(datadictvalue["C_CHART_OF_ACCNTS"])
        page.get_by_label("Rule Type").click()
        page.get_by_label("Rule Type").select_option(datadictvalue["C_RULE_TYPE"])
        page.wait_for_timeout(3000)
        page.locator("//label[text()='Rule Type']//following::select[2]").click()
        page.locator("//label[text()='Rule Type']//following::select[2]").select_option(datadictvalue["C_SGMNT"])
        page.wait_for_timeout(5000)
        #Value type
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Value Type").click()
        page.get_by_label("Value Type").select_option(datadictvalue["C_VALUE_TYPE"])

        # page.get_by_role("cell", name="Source Search: Source Autocompletes on TAB", exact=True)
        # page.get_by_label("//a[@title='Search: Source']").click()
        # page.get_by_label("//a[@title='Search: Source']").type(datadictvalue["C_VALUE"])
        # # page.locator("// a[ @ title = 'Search: Source']").click()
        #page.get_by_label("Value Type").press("Tab")
        page.wait_for_timeout(5000)
        page.get_by_title("Search: Source").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Subledger Application").select_option("20")
        page.locator("//div[text()='Search and Select: Source']//following::label[text()='Name']//following::input[1]").clear()
        page.locator("//div[text()='Search and Select: Source']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_VALUE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("cell", name=datadictvalue["C_VALUE"], exact=True).locator("span").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        #Conditions
        page.get_by_label("Conditions", exact=True).click()
        page.wait_for_timeout(3000)
        page.get_by_label("Conditions", exact=True).fill(datadictvalue["C_CNDTNS"])
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Validate")
        page.wait_for_timeout(4000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        i = i + 1

    page.get_by_role("button", name="Done").click()
    #page.get_by_role("button", name= "Cancel").click()
    # page.get_by_role("button", name="Save", exact=True).click()
    # page.get_by_role("button", name="Save and Close").click()

    # Validation
    try:
        expect(page.get_by_role("heading", name="Implementation Project: HCM Implementation Project")).to_be_visible()
        print("Payroll SLA Manage Accounting Rules Created Successfully")

    except Exception as e:
        print("Manage Account Rules: Payroll created Unsuccessfully")


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_SLA_CONFIG_WB, MAN_ACC_RULES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_SLA_CONFIG_WB, MAN_ACC_RULES, PRCS_DIR_PATH + PAYROLL_SLA_CONFIG_WB)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_SLA_CONFIG_WB, MAN_ACC_RULES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_SLA_CONFIG_WB)[0] + "_" +MAN_ACC_RULES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_SLA_CONFIG_WB)[0] + "_" +MAN_ACC_RULES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))