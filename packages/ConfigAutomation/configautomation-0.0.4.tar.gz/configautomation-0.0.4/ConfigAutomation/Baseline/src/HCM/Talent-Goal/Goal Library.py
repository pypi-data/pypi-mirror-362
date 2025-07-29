from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    # Navigation
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Navigator").click()
    page.wait_for_timeout(2000)
    page.get_by_title("My Client Groups", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Goals").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Performance Goal Library").click()
    page.wait_for_timeout(5000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        page.get_by_label("Add").click()
        page.wait_for_timeout(5000)

        #Library Info
        page.get_by_role("combobox", name="Status").click()
        #page.get_by_role("combobox", name="Status").fill("")
        #page.get_by_role("combobox", name="Status").type(datadictvalue["C_STTS"])
        page.get_by_role("row", name=datadictvalue["C_STTS"], exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Type").first.click()
        #page.get_by_role("combobox", name="Type").first.fill("")
        #page.get_by_role("combobox", name="Type").first.type(datadictvalue["C_TYPE"])
        page.get_by_role("row", name=datadictvalue["C_TYPE"], exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Available To").click()
        page.get_by_role("combobox", name="Available To").fill("")
        page.get_by_role("combobox", name="Available To").type(datadictvalue["C_AVLBL_TO"])
        page.get_by_role("row", name=datadictvalue["C_AVLBL_TO"]).click()
        page.wait_for_timeout(2000)

        #Basic Info
        page.get_by_label("Goal Name").click()
        page.get_by_label("Goal Name").type(datadictvalue["C_GOAL_NAME"])
        page.wait_for_timeout(2000)
        page.get_by_label("Start Date").click()
        page.get_by_label("Start Date").type(datadictvalue["C_START_DATE"])
        page.wait_for_timeout(2000)
        page.get_by_label("Target Date").click()
        page.get_by_label("Target Date").type(datadictvalue["C_TRGT_DATE"])
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Priority").click()
        page.get_by_role("combobox", name="Priority").type(datadictvalue["C_PRRTY"])
        page.get_by_role("row", name=datadictvalue["C_PRRTY"]).click()
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Category").click()
        page.get_by_role("combobox", name="Category").type(datadictvalue["C_CTGRY"])
        page.get_by_role("row", name=datadictvalue["C_CTGRY"]).click()
        page.wait_for_timeout(2000)
        page.locator("#richText2SuccessCriteria").get_by_role("textbox").click()
        page.locator("#richText2SuccessCriteria").get_by_role("textbox").fill(datadictvalue["C_SCCSS_CRTR"])
        page.wait_for_timeout(2000)

        #Measurements
        if datadictvalue["C_THIS_IS_A_MSRBL_GOAL"] == "Enable":
            page.locator("//div[@aria-labelledby='library-goals-detail-basicInfoCreate-switch-labelled-by|label']").click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Unit of Measure").click()
            page.get_by_role("combobox", name="Unit of Measure").type(datadictvalue["C_UNIT_OF_MSR"])
            page.get_by_role("row", name=datadictvalue["C_UNIT_OF_MSR"]).click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Target Type").click()
            page.get_by_role("row", name=datadictvalue["C_TRGT_TYPE"]).click()
            page.wait_for_timeout(2000)
            page.get_by_label("Target Value").click()
            page.get_by_label("Target Value").type(datadictvalue["C_TRGT_VALUE"])
            page.wait_for_timeout(2000)

        #Tasks
        # page.get_by_label("Add Tasks").click()
        # page.wait_for_timeout(3000)
        # page.keyboard.press("Space")
        # page.get_by_label("Task Name").click()
        # page.get_by_label("Task Name").type(datadictvalue["C_TASK_NAME"])
        # page.wait_for_timeout(1000)
        # page.get_by_role("row", name="Tasks").get_by_label("Start Date").click()
        # page.get_by_role("row", name="Tasks").get_by_label("Start Date").type(datadictvalue["C_START_DATE_1"])
        # page.wait_for_timeout(1000)
        # page.get_by_role("row", name="Tasks").get_by_label("Target Date").click()
        # page.get_by_role("row", name="Tasks").get_by_label("Target Date").type(datadictvalue["C_TRGT_DATE_1"])
        # page.get_by_role("row", name="Tasks").get_by_label("Target Date").press("Tab")
        # page.wait_for_timeout(2000)
        # page.get_by_role("row", name="Tasks").get_by_label("Type").nth(1).click()
        # page.get_by_role("row", name="Tasks").get_by_label("Type").nth(1).type(datadictvalue["C_TYPE_1"])
        # page.get_by_role("row", name=datadictvalue["C_TYPE_1"]).click()
        # page.get_by_role("row", name="Tasks").get_by_label("Type").nth(1).press("Tab")
        # page.wait_for_timeout(2000)
        # page.get_by_role("row", name="Tasks").get_by_label("Priority").nth(1).click()
        # page.get_by_role("row", name="Tasks").get_by_label("Priority").nth(1).type(datadictvalue["C_PRRTY_2"])
        # page.get_by_role("row", name=datadictvalue["C_PRRTY_2"]).click()
        # page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create").click()

        page.wait_for_timeout(5000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Library Goals")).to_be_visible()
            print("Library Goals Saved Successfully")
            datadictvalue["RowStatus"] = "Library Goals Saved Successfully"
        except Exception as e:
            print("Library Goalss not saved")
            datadictvalue["RowStatus"] = "Library Goals not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GOAL_CONFIG_WRKBK, GOAL_LIBRARY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GOAL_CONFIG_WRKBK, GOAL_LIBRARY,PRCS_DIR_PATH + GOAL_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GOAL_CONFIG_WRKBK, GOAL_LIBRARY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GOAL_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GOAL_CONFIG_WRKBK)[0] + "_" + GOAL_LIBRARY + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




