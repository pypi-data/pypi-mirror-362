from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill("Curtis.Feitty")
    page.get_by_placeholder("Password").fill("j2#sr#3D")
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
    page.get_by_role("link", name="Goal Plans").click()
    page.wait_for_timeout(5000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        page.get_by_label("Add").click()
        page.wait_for_timeout(5000)

        # Details Info
        page.get_by_role("textbox", name="Goal Plan", exact=True).click()
        page.get_by_role("textbox", name="Goal Plan", exact=True).type(datadictvalue["C_GOAL_PLAN"])
        # page.get_by_role("combobox", name="Status").fill("")
        # page.get_by_role("combobox", name="Status").type(datadictvalue["C_STTS"])
        page.get_by_role("combobox", name="Review Period").click()
        # page.get_by_role("combobox", name="Review Period").fill("")
        # page.get_by_role("combobox", name="Review Period").type(datadictvalue["C_RVW_PRD"])
        page.get_by_text(datadictvalue["C_RVW_PRD"], exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_label("Start Date").click()
        page.get_by_label("Start Date").fill("")
        page.get_by_label("Start Date").type(datadictvalue["C_START_DATE"].strftime('%m/%d/%y'))
        page.wait_for_timeout(2000)
        page.get_by_label("End Date").click()
        page.get_by_label("End Date").fill("")
        page.get_by_label("End Date").type(datadictvalue["C_END_DATE"].strftime('%m/%d/%y'))
        page.wait_for_timeout(1000)
        page.get_by_label("End Date").press("Tab")
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Allow Updates to Goals By").click()
        page.get_by_role("combobox", name="Allow Updates to Goals By").type(datadictvalue["C_ALLOW_UPDTS_TO_GOALS_BY"])
        page.get_by_role("row", name=datadictvalue["C_ALLOW_UPDTS_TO_GOALS_BY"], exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Allow Updates to Goals By").press("Tab")
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Evaluation Type").first.click()
        page.get_by_role("combobox", name="Evaluation Type").type(datadictvalue["C_EVLTN_TYPE"])
        page.get_by_role("row", name=datadictvalue["C_EVLTN_TYPE"], exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_text("Actions for Workers and Managers on HR").first.click()
        page.get_by_text("Actions for Workers and Managers on HR").type(datadictvalue["C_ACTNS_FOR_WRKRS_AND_MNGRS_ON_HR_ASSGND_GOALS"])
        page.get_by_role("option", name=datadictvalue["C_ACTNS_FOR_WRKRS_AND_MNGRS_ON_HR_ASSGND_GOALS"]).locator("div").nth(1).click()
        page.wait_for_timeout(1000)
        page.get_by_text("Maximum Goals for This Goal").first.click()
        page.get_by_text("Maximum Goals for This Goal").type(str(datadictvalue["C_MXMM_GOALS_FOR_THIS_GOAL_PLAN"]))
        page.wait_for_timeout(2000)
        page.get_by_text("Performance Document Types").first.click()
        page.get_by_text("Performance Document Types").first.type(datadictvalue["C_PRFRMNC_DCMNT_TYPES"], delay=50)
        page.get_by_label(datadictvalue["C_PRFRMNC_DCMNT_TYPES"]).click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)

        page.get_by_placeholder("Search by plan name").type(datadictvalue["C_GOAL_PLAN"])
        page.get_by_placeholder("Search by plan name").press("Enter")
        page.wait_for_timeout(2000)
        page.get_by_role("link", name=datadictvalue["C_GOAL_PLAN"],exact=True).click()
        page.get_by_label("Add Goals").click()
        page.wait_for_timeout(4000)
        page.get_by_placeholder("Start writing a clear and").click()
        page.get_by_placeholder("Start writing a clear and").type(datadictvalue["C_WHAT_YOUR_GOAL"])
        page.wait_for_timeout(1000)
        page.get_by_placeholder("Add details about this goal").click()
        page.get_by_placeholder("Add details about this goal").type(datadictvalue["C_ANY_ADDTNL_INFO_YOU_WANT_TO_ADD"])
        page.wait_for_timeout(1000)
        page.get_by_label("How will you know you have").click()
        page.get_by_label("How will you know you have").type(datadictvalue["C_HOW_WILL_YOU_KNOW_YOU_HAVE_ACHVD_YOUR_GOAL"])
        page.wait_for_timeout(1000)
        page.get_by_text("Allow managers to delete this goal").click()
        # page.get_by_text("Allow managers to delete this goal").type(datadictvalue["C_ALLOW_MNGRS_TO_DLT_THIS_GOAL"])
        page.wait_for_timeout(2000)
        # page.get_by_text(datadictvalue["C_ALLOW_MNGRS_TO_DLT_THIS_GOAL"]).click()
        page.get_by_role("row", name=datadictvalue["C_ALLOW_MNGRS_TO_DLT_THIS_GOAL"]).click()
        # page.locator("//span[text()='"+datadictvalue["C_ALLOW_MNGRS_TO_DLT_THIS_GOAL"]+"']").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Start Date").click()
        page.get_by_label("Start Date").fill("")
        page.get_by_label("Start Date").type(datadictvalue["C_START_DATE_1"].strftime('%m/%d/%y'))
        page.wait_for_timeout(2000)
        page.get_by_label("Target Date").click()
        page.get_by_label("Target Date").fill("")
        page.get_by_label("Target Date").type(datadictvalue["C_TRGT_DATE"].strftime('%m/%d/%y'))
        page.wait_for_timeout(1000)
        page.get_by_label("Target Date").press("Tab")
        page.wait_for_timeout(2000)
        page.get_by_text("Category").click()
        page.get_by_text("Category").type(datadictvalue["C_CTGRY"])
        # page.get_by_role("row", name=datadictvalue["C_CTGRY"]).click()
        page.wait_for_timeout(2000)

        if datadictvalue["C_ALLOW_ASSGNS_TO_EDIT_GOAL_DFNTN"] == "Enable":
            if not page.get_by_label("Allow assignees to edit goal definition").is_checked():
                page.get_by_label("Allow assignees to edit goal definition").click()
                page.wait_for_timeout(2000)
        page.get_by_label("Header Toolbar").get_by_label("Add").click()
        page.wait_for_timeout(15000)
        page.get_by_label("Go back").click()
        page.wait_for_timeout(5000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Goal Plans")).to_be_visible()
            print("Goals Plans Saved Successfully")
            datadictvalue["RowStatus"] = "Goals Plans Saved Successfully"
        except Exception as e:
            print("Goals Plans not saved")
            datadictvalue["RowStatus"] = "Goals Plans not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GOAL_CONFIG_WRKBK, GOAL_PLAN):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GOAL_CONFIG_WRKBK, GOAL_PLAN,PRCS_DIR_PATH + GOAL_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GOAL_CONFIG_WRKBK, GOAL_PLAN)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GOAL_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GOAL_CONFIG_WRKBK)[0] + "_" + GOAL_PLAN + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




