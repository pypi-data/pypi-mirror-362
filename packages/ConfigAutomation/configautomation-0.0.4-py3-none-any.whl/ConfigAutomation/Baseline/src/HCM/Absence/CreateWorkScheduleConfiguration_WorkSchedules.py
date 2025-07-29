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

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(40000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Work Schedules")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Work Schedules", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        # Name
        page.get_by_label("Name").clear()
        page.get_by_label("Name").type(datadictvalue["C_NAME"])

        # Type
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Type").click()
        page.get_by_text(datadictvalue["C_TYPE"]).click()

        # Effective from Date
        #page.get_by_role("row", name="*Effective from Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").clear()
        #page.get_by_role("row", name="*Effective from Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").type(str(datadictvalue["C_EFFCTV_FROM_DATE"]))
        page.locator("//label[text()='Effective from Date']//following::input[1]").clear()
        page.locator("//label[text()='Effective from Date']//following::input[1]").type(datadictvalue["C_EFFCTV_FROM_DATE"])

        # Effective to Date
        #page.get_by_role("row", name="*Effective to Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").clear()
        #page.get_by_role("row", name="*Effective to Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").type(str(datadictvalue["C_EFFCTV_TO_DATE"]))
        page.locator("//label[text()='Effective to Date']//following::input[1]").clear()
        page.locator("//label[text()='Effective to Date']//following::input[1]").type(datadictvalue["C_EFFCTV_TO_DATE"])

        # Category
        if datadictvalue["C_CTGRY"]!='':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Category").click()
            page.get_by_text(datadictvalue["C_CTGRY"]).click()

        # Description
        page.get_by_label("Description").clear()
        page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])

        # Patterns
        page.get_by_role("button", name="Add Row").first.click()
        page.wait_for_timeout(3000)

        ## Sequence
        page.get_by_label("Sequence").clear()
        page.get_by_label("Sequence").type(str(datadictvalue["C_SQNC"]))

        ## Pattern Name
        page.get_by_title("Search: Name").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(2000)
        #page.get_by_role("cell", name="Name Name Name Length in Days").get_by_label("Name").clear()
        #page.get_by_role("cell", name="Name Name Name Length in Days").get_by_label("Name").type(datadictvalue["C_WORK_SHIFT_NAME"])
        #page.get_by_role("button", name="Search", exact=True).click()
        #page.wait_for_timeout(3000)
        page.locator("//div[text()='Search and Select: Name']//following::input[3]").click()
        page.locator("//div[text()='Search and Select: Name']//following::input[3]").type(datadictvalue["C_WORK_SHIFT_NAME"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WORK_SHIFT_NAME"]).first.click()
        page.get_by_role("button", name="OK").click()

        # Expectations
        page.get_by_role("button", name="Add Row").nth(1).click()
        page.wait_for_timeout(3000)
        ## Exception Type
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Type").click()
        page.get_by_text(datadictvalue["C_EVENT_TYPE"],exact=True).click()

        ## Exception Name
        page.wait_for_timeout(2000)
        page.get_by_label("Name").nth(2).click()
        page.get_by_text(datadictvalue["C_EVENT_NAME"],exact=True).click()

        ##'Eligibility Profiles
        if datadictvalue["C_EP_NAME"] != '':
            page.get_by_role("button", name="Add Row").nth(2).click()
            page.wait_for_timeout(3000)

            page.get_by_role("table", name="Eligibility Profiles").locator("a")
            page.locator("//h1[text()='Eligibility Profiles']//following::a[10]").click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//div[text()='Search and Select: Name']//following::input[1]").click()
            page.locator("//div[text()='Search and Select: Name']//following::input[1]").type(datadictvalue["C_EP_NAME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_EP_NAME"]).first.click()
            page.get_by_role("button", name="OK").click()

        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(40000)
        page.get_by_role("button", name="OK").click()

        try:
            expect(page.get_by_role("heading", name="Work Schedules")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Work Schedule Configuration Work Schedules Created Successfully")
            datadictvalue["RowStatus"] = "Created Work Schedule Configuration Work Schedules Successfully"
        except Exception as e:
            print("Unable to Save Work Schedule Configuration Work Schedules")
            datadictvalue["RowStatus"] = "Unable to Save Work Schedule Configuration Work Schedules"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + WORK_SCH_CONFIG, WRK_SCHEDULES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + WORK_SCH_CONFIG, WRK_SCHEDULES,PRCS_DIR_PATH + WORK_SCH_CONFIG)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + WORK_SCH_CONFIG, WRK_SCHEDULES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", WORK_SCH_CONFIG)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", WORK_SCH_CONFIG)[0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
