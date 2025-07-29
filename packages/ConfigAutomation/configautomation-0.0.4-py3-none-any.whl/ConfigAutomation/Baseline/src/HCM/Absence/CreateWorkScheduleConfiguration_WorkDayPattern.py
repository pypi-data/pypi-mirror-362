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
    page.get_by_role("textbox").type("Work Workday Patterns")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Work Workday Patterns", exact=True).click()

    WRKDAYNAME = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        page.pause()

        if datadictvalue["C_NAME"] != WRKDAYNAME:

            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Save and Close").click()
                try:
                    expect(page.get_by_role("heading", name="Work Workday Patterns")).to_be_visible()
                    print("Work Schedule Configuration Workday Patterns Saved")
                    datadict[i - 1]["RowStatus"] = "Work Schedule Configuration Workday Patterns Saved"
                except Exception as e:
                    print("Unable to save Work Schedule Configuration Workday Patterns")
                    datadict[i - 1]["RowStatus"] = "Unable to save Work Schedule Configuration Workday Patterns"

                page.wait_for_timeout(3000)

            #page.get_by_role("cell", name="Create Workday Pattern", exact=True).locator("a").click()
            page.get_by_title("Create Workday Pattern").nth(2).click()
            page.get_by_role("link", name=datadictvalue["C_CRT_WRKDY_PTTRN"]).click()
            page.wait_for_timeout(3000)

            # Name
            if datadictvalue["C_NAME"] != 'N/A':
                page.get_by_label("Name").clear()
                page.get_by_label("Name").type(datadictvalue["C_NAME"])

            # Description
            if datadictvalue["C_DSCRPTN"] != 'N/A':
                page.get_by_label("Description").clear()
                page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])

            # Lenght in Days
            if datadictvalue["C_LNGTH_IN_DAYS"] != 'N/A':
                page.get_by_label("Length in Days").clear()
                page.get_by_label("Length in Days").type(str(datadictvalue["C_LNGTH_IN_DAYS"]))

            WRKDAYNAME = datadictvalue["C_NAME"]

        # Adding a Row for Workday Pattern Details
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(3000)

        # Start Day
        if datadictvalue["C_START_DAY"] != 'N/A':
            page.get_by_label("Start Day").first.clear()
            page.get_by_label("Start Day").first.type(str(datadictvalue["C_START_DAY"]))

        # End Day
        if datadictvalue["C_END_DAY"] != 'N/A':
            page.get_by_label("End Day").first.clear()
            page.get_by_label("End Day").first.type(str(datadictvalue["C_END_DAY"]))

        # Sequence
        if datadictvalue["C_SQNC"] != 'N/A':
            page.get_by_label("Sequence").first.clear()
            page.get_by_label("Sequence").first.type(str(datadictvalue["C_SQNC"]))

        # Shift Name
        if datadictvalue["C_SHIFT_NAME"] != 'N/A':
            page.locator("//a[@title='Search: Shift Name']//preceding::input[1]").first.first.type(datadictvalue["C_SHIFT_NAME"])
            page.get_by_label("Name", exact=True).click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Saving the record
        if i == rowcount:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()


    try:
        expect(page.get_by_role("heading", name="Work Workday Patterns")).to_be_visible()
        page.wait_for_timeout(3000)
        print("Work Schedule Configuration Workday Patterns Created Successfully")
        datadictvalue["RowStatus"] = "Created Work Schedule Configuration Workday Patterns Successfully"
    except Exception as e:
        print("Unable to Save Work Schedule Configuration Workday Patterns")
        datadictvalue["RowStatus"] = "Unable to Save Work Schedule Configuration Workday Patterns"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + WORK_SCH_CONFIG, WORK_WRKDAY_PATTERN):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + WORK_SCH_CONFIG, WORK_WRKDAY_PATTERN, PRCS_DIR_PATH + WORK_SCH_CONFIG)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + WORK_SCH_CONFIG, WORK_WRKDAY_PATTERN)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", WORK_SCH_CONFIG)[0])
        write_status(output,RESULTS_DIR_PATH + re.split(".xlsx", WORK_SCH_CONFIG)[0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))