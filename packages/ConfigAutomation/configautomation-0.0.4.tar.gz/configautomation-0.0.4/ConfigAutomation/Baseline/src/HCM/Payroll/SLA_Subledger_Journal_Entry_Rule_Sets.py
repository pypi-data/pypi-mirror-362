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
    page.get_by_role("cell", name="Manage Subledger Journal Entry Rule Sets", exact=True).click()
    page.wait_for_timeout(2000)
    page.locator("//span[text()='Manage Subledger Journal Entry Rule Sets']//following::a[@title='Go to Task'][1]").click()
    page.wait_for_timeout(4000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        #Create Rule Set
        page.get_by_role("button", name="Create").click()

        #Name
        page.get_by_label("Name", exact=True).click()
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])

        #Short Name
        page.get_by_label("Short Name").click()
        page.get_by_label("Short Name").fill(datadictvalue["C_SHORT_NAME"])

        #Description
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        #Select Event Class
        page.get_by_label("Event Class").select_option(datadictvalue["C_EVENT_CLASS"])
        page.wait_for_timeout(2000)

        #Select Event Type
        page.get_by_title("Search: Event Type").click()
        page.get_by_role("cell", name=datadictvalue["C_EVENT_TYPE"], exact=True).click()
        page.wait_for_timeout(2000)

        #Select Chart of Accounts
        page.get_by_label("Chart of Accounts").click()
        page.get_by_label("Chart of Accounts").select_option(datadictvalue["C_CHART_OF_ACCNTS"])

        #Journal Entry - Select Accounting Date
        page.get_by_title("Search: Source").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Source").clear()
        page.get_by_label("Source").fill(datadictvalue["C_ACCNTNG_DATE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name=datadictvalue["C_ACCNTNG_DATE"], exact=True).locator("span").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        #Add Credit Journal lines
        #Add Row
        page.get_by_role("button", name="Add Row").first.click()
        page.wait_for_timeout(6000)

        #Line Type
        page.get_by_label("Line Type").click()
        page.get_by_label("Line Type").select_option(datadictvalue["C_LINE_TYPE_CRDT"])
        page.wait_for_timeout(2000)

        #Journal Line Rule
        page.get_by_title("Search: Journal Line Rule").click()
        page.get_by_text(datadictvalue["C_JRNL_LINE_RULE_CRDT"], exact=True).click()
        page.wait_for_timeout(5000)

        #Segment Rules
        #Segment 1 - Fund
        page.get_by_title("Search: SegmentName1").click()
        page.get_by_text(datadictvalue["C_SGMNT_RULES_CRDT_FUND"]).click()
        page.wait_for_timeout(2000)

        #Segment 2 - Cost Center
        page.get_by_title("Search: SegmentName2").click()
        page.get_by_text(datadictvalue["C_SGMNT_RULES_CRDT_COST_CNTR"]).click()
        page.wait_for_timeout(2000)

        #Segment 3 - Account
        page.get_by_title("Search: SegmentName3").click()
        page.get_by_text(datadictvalue["C_SGMNT_RULES_CRDT_ACCNT"]).click()
        page.wait_for_timeout(2000)

        #Segment 4 - Activity
        page.get_by_label("SegContentNameTrans4").click()
        # page.get_by_text(datadictvalue["C_SGMNT_RULES_CRDT_ACTVTY"]).click()
        page.get_by_label("SegContentNameTrans4").type(datadictvalue["C_SGMNT_RULES_CRDT_ACTVTY"])
        page.wait_for_timeout(2000)

        #Segment 5 - Interfund
        page.get_by_label("SegContentNameTrans5").click()
        page.get_by_label("SegContentNameTrans5").type(datadictvalue["C_SGMNT_RULES_CRDT_INTRFND"])
        # page.get_by_text(datadictvalue["C_SGMNT_RULES_CRDT_INTRFND"]).click()
        page.wait_for_timeout(2000)

        # Segment 5 - Future 1
        page.get_by_title("Search: SegmentName6").click()
        page.get_by_text(datadictvalue["C_SGMNT_RULES_CRDT_FTR_1"]).click()
        page.wait_for_timeout(2000)

        # Segment 5 - Future 2
        page.get_by_title("Search: SegmentName7").click()
        page.get_by_text(datadictvalue["C_SGMNT_RULES_CRDT_FTR_2"]).click()
        page.wait_for_timeout(2000)

        #Link Description Rule
        page.get_by_title("Search: Line Description Rule").click()
        page.get_by_text(datadictvalue["C_SGMNT_RULES_CRDT_LINE_DSCRPTN_RULE"]).click()
        page.wait_for_timeout(2000)

        # Add Debit Journal lines
        # Add Row
        page.get_by_role("button", name="Add Row").first.click()
        page.wait_for_timeout(4000)

        # Line Type
        page.get_by_label("Line Type").click()
        page.get_by_label("Line Type").select_option(datadictvalue["C_LINE_TYPE_DEBIT"])
        page.wait_for_timeout(2000)

        # Journal Line Rule
        page.get_by_title("Search: Journal Line Rule").click()
        page.get_by_text(datadictvalue["C_JRNL_LINE_RULE_DEBIT"], exact=True).click()
        page.wait_for_timeout(5000)

        # Segment Rules
        # Segment 1 - Fund
        page.get_by_title("Search: SegmentName1").first.click()
        page.get_by_role("cell", name=datadictvalue["C_SGMNT_RULES_DBT_FUND"], exact=True).locator("span").click()
        page.wait_for_timeout(2000)

        # Segment 2 - Cost Center
        page.get_by_title("Search: SegmentName2").first.click()
        page.get_by_role("cell", name=datadictvalue["C_SGMNT_RULES_DBT_COST_CNTR"], exact=True).locator("span").click()
        page.wait_for_timeout(2000)

        # Segment 3 - Account
        page.get_by_title("Search: SegmentName3").first.click()
        page.get_by_role("cell", name=datadictvalue["C_SGMNT_RULES_DBT_ACCNT"], exact=True).locator("span").click()
        page.wait_for_timeout(2000)

        # Segment 4 - Activity
        page.get_by_title("Search: SegmentName4").first.click()
        page.get_by_role("cell", name=datadictvalue["C_SGMNT_RULES_DBT_ACTVTY"], exact=True).locator("span").click()
        page.wait_for_timeout(2000)

        # Segment 5 - Interfund
        page.get_by_title("Search: SegmentName4").nth(1).click()
        page.get_by_role("cell", name=datadictvalue["C_SGMNT_RULES_DBT_INTRFND"], exact=True).locator("span").click()
        page.wait_for_timeout(2000)

        # Segment 5 - Future 1
        page.get_by_title("Search: SegmentName6").first.click()
        page.get_by_role("cell", name=datadictvalue["C_SGMNT_RULES_DBT_FTR_1"], exact=True).locator("span").click()
        page.wait_for_timeout(2000)

        # Segment 5 - Future 2
        page.get_by_title("Search: SegmentName7").first.click()
        page.get_by_role("cell", name=datadictvalue["C_SGMNT_RULES_DBT_FTR_2"], exact=True).locator("span").click()
        page.wait_for_timeout(2000)

        # Link Description Rule
        page.get_by_title("Search: Line Description Rule").first.click()
        page.get_by_role("cell", name=datadictvalue["C_SGMNT_RULES_DBT_LINE_DSCRPTN_RULE"], exact=True).locator("span").click()
        page.wait_for_timeout(3000)

        #Save and Close
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)

        i = i + 1


    # Validation
    try:
        expect(page.get_by_role("heading", name="Manage Subledger Journal Entry Rule Sets: Payroll")).to_be_visible()
        print("Payroll SLA Subledger Journal Entry Rule sets Created Successfully")

    except Exception as e:
        print("Payroll SLA Subledger Journal Entry Rule sets created Unsuccessfully")


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_SLA_CONFIG_WB, MAN_SBLDGR_JRNL_ENT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_SLA_CONFIG_WB, MAN_SBLDGR_JRNL_ENT, PRCS_DIR_PATH + PAYROLL_SLA_CONFIG_WB)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_SLA_CONFIG_WB, MAN_SBLDGR_JRNL_ENT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_SLA_CONFIG_WB)[0] + "_" +MAN_SBLDGR_JRNL_ENT)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_SLA_CONFIG_WB)[0] + "_" +MAN_SBLDGR_JRNL_ENT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))