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
    page.wait_for_timeout(5000)

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Time Consumer Sets")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Time Consumer Sets", exact=True).click()
    page.wait_for_timeout(2000)

    i = 0

    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)

        # Name
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(str(datadictvalue["C_NAME"]))

        # Description
        if datadictvalue["C_DSCRPTN"] != "N/A" or '':
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(str(datadictvalue["C_DSCRPTN"]))

        # Time Consumer - Project Costing
        if datadictvalue["C_PRJCT_CSTNG"] == "Yes":
            page.get_by_text("Project Costing", exact=True).check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_PRJCT_EXCTN_MNGMNT"] == "Yes":
            page.get_by_text("Project Execution Management", exact=True).check()
            page.wait_for_timeout(2000)
        if datadictvalue["C_PYRLL"] == "Yes":
            page.get_by_text("Payroll", exact=True).check()
            page.wait_for_timeout(2000)

        if datadictvalue["C_ENBLE_TIME_CARD_SBMSSN_INFRMTNL_WRKFLW"] != '':
            page.get_by_role("combobox", name="Enable Informational Workflow for Bulk Time Card Submission").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ENBLE_TIME_CARD_SBMSSN_INFRMTNL_WRKFLW"], exact=True).click()
            page.wait_for_timeout(2000)
        # Enable Approval Workflow for Workers
        if datadictvalue["C_ENBLE_APPRVL_WRLFLW_FOR_WRKRS"] != '':
            page.get_by_role("combobox", name="Enable Approval Workflow for Workers").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ENBLE_APPRVL_WRLFLW_FOR_WRKRS"], exact=True).click()
            page.wait_for_timeout(2000)
        # Absence Approval Routing
        if datadictvalue["C_ABSNC_APPRVL_RTNG"] != '':
            page.get_by_role("combobox", name="Absence Approval Routing").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_APPRVL_RTNG"], exact=True).click()

        if page.get_by_role("heading", name="Time Consumer: Project Costing").is_visible():
            # Time Category
            if datadictvalue["C_PC_TIME_CTGRY"] != "N/A":
                page.locator("//div[@title='Time Consumer: Project Costing']//following::label[text()='Time Category']//following::input").first.click()
                page.locator("//div[@title='Time Consumer: Project Costing']//following::label[text()='Time Category']//following::input").first.fill(datadictvalue["C_PC_TIME_CTGRY"])
                page.wait_for_timeout(2000)
                page.get_by_role("option", name=(datadictvalue["C_PC_TIME_CTGRY"]))
                page.wait_for_timeout(2000)
            # Validate on Time Card Actions
            if datadictvalue["C_PC_VLDTE_ON_TIME_CARD_ACTNS"] != "N/A":
                page.locator("//div[@title='Time Consumer: Project Costing']//following::label[text()='Validate on Time Card Actions']//following::input").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PC_VLDTE_ON_TIME_CARD_ACTNS"], exact=True).click()
                page.wait_for_timeout(2000)
            # Required Time Card Status
            if datadictvalue["C_PC_RQRD_TIME_CARD_STTS"] != "N/A":
                page.locator("//div[@title='Time Consumer: Project Costing']//following::label[text()='Required Time Card Status']//following::input").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PC_RQRD_TIME_CARD_STTS"], exact=True).click()
                page.wait_for_timeout(2000)
            # Approval
            if datadictvalue["C_PC_APPRVL"] != "N/A":
                page.locator("//div[@title='Time Consumer: Project Costing']//following::label[text()='Approval']//following::input").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PC_APPRVL"], exact=True).click()
                # Entry Level Approval
                if datadictvalue["C_PC_ENTRY_LEVEL_APPRVL"] == "Yes":
                    page.locator("//div[@title='Time Consumer: Project Costing']//following::label[text()='Entry-level approval']").first.check()
                    page.wait_for_timeout(2000)
            # Time Data for Approval Rules to Evaluate
            if datadictvalue["C_PC_TIME_DATA_FOR_APPRVL_RULES_TO_EVLT"] != "N/A":
                page.locator("//div[@title='Time Consumer: Project Costing']//following::label[text()='Time Data for Approval Rules to Evaluate']//following::input").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PC_TIME_DATA_FOR_APPRVL_RULES_TO_EVLT"], exact=True).click()
                page.wait_for_timeout(2000)
            # Transfer on approval: Approval required
            if datadictvalue["C_PC_PC_APPRVL_RQRD"] == "No":
                page.locator("//div[@title='Time Consumer: Project Costing']//following::label[text()='Project Costing']").first.uncheck()
                page.wait_for_timeout(2000)
            if datadictvalue["C_PC_P_APPRVL_RQRD"] == "N/A":
                page.wait_for_timeout(2000)
            if datadictvalue["C_PC_PC_APPRVL_RQRD"] == "Yes":
                page.locator("//div[@title='Time Consumer: Project Costing']//following::label[text()='Project Costing']").first.check()
                page.wait_for_timeout(2000)
            if datadictvalue["C_PC_PC_APPRVL_RQRD"] == "N/A":
                #page.locator("//div[@title='Time Consumer: Project Costing']//following::label[text()='Project Costing']").first.check()
                page.wait_for_timeout(2000)
            if datadictvalue["C_PC_P_APPRVL_RQRD"] == "No":
                page.locator("//div[@title='Transfer Rules: Import and Process Cost Transactions']//following::label[text()='Payroll']").first.uncheck()
                page.wait_for_timeout(2000)
            if datadictvalue["C_PC_P_APPRVL_RQRD"] == "Yes":
                page.locator("//div[@title='Transfer Rules: Import and Process Cost Transactions']//following::label[text()='Payroll']").first.check()
                page.wait_for_timeout(2000)

        # Time Consumer - Payroll
        if page.get_by_role("heading", name="Time Consumer: Payroll").is_visible():
            # Time Category
            if datadictvalue["C_TIME_CTGRY"] != "N/A":
                page.locator("//div[@title='Time Consumer: Payroll']//following::label[text()='Time Category']//following::input[1]").first.click()
                page.locator("//div[@title='Time Consumer: Payroll']//following::label[text()='Time Category']//following::input[1]").first.fill(datadictvalue["C_TIME_CTGRY"])
                page.wait_for_timeout(2000)
                page.get_by_role("option", name=(datadictvalue["C_TIME_CTGRY"]))
                page.wait_for_timeout(2000)
            # Validate on Time Card Actions
            if datadictvalue["C_VLDTE_ON_TIME_CARD_ACTNS"] != "N/A":
                page.locator("//div[@title='Time Consumer: Payroll']//following::label[text()='Validate on Time Card Actions']//following::input").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VLDTE_ON_TIME_CARD_ACTNS"], exact=True).click()
                page.wait_for_timeout(2000)
            # Required Time Card Status
            if datadictvalue["C_RQRD_TIME_CARD_STTS"] != "N/A":
                page.locator("//div[@title='Time Consumer: Payroll']//following::label[text()='Required Time Card Status']//following::input").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RQRD_TIME_CARD_STTS"], exact=True).click()
                page.wait_for_timeout(2000)
            # Approval
            if datadictvalue["C_APPRVL"] != "N/A":
                page.locator("//div[@title='Time Consumer: Payroll']//following::label[text()='Approval']//following::input").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_APPRVL"], exact=True).click()
                # Entry Level Approval
                if datadictvalue["C_ENTRY_LEVEL_APPRVL"] == "Yes":
                    page.locator("//div[@title='Time Consumer: Payroll']//following::label[text()='Entry-level approval']").first.check()
                    page.wait_for_timeout(2000)
            # Time Data for Approval Rules to Evaluate
            if datadictvalue["C_TIME_DATA_FOR_APPRVL_RULES_TO_EVLT"] != "N/A":
                page.locator("//div[@title='Time Consumer: Payroll']//following::label[text()='Time Data for Approval Rules to Evaluate']//following::input").first.click()
                page.wait_for_timeout(2000)
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TIME_DATA_FOR_APPRVL_RULES_TO_EVLT"]).click()
                page.wait_for_timeout(2000)
            # Transfer on approval: Approval required
            if datadictvalue["C_P_PC_APPRVL_RQRD"] == "No":
                page.locator("//div[@title='Transfer Rules: Load Time Card Batches']//following::label[text()='Project Costing']").first.uncheck()
                page.wait_for_timeout(2000)
            if datadictvalue["C_P_P_APPRVL_RQRD"] == "Yes":
                page.locator("//div[@title='Time Consumer: Payroll']//following::label[text()='Payroll']").first.check()
                page.wait_for_timeout(2000)
            if datadictvalue["C_P_P_APPRVL_RQRD"] == "No":
                page.locator("//div[@title='Time Consumer: Payroll']//following::label[text()='Payroll']").first.uncheck()
                page.wait_for_timeout(2000)
            if datadictvalue["C_P_P_APPRVL_RQRD"] == "N/A":
                #page.locator("//div[@title='Time Consumer: Payroll']//following::label[text()='Payroll']").first.uncheck()
                page.wait_for_timeout(2000)
            if datadictvalue["C_P_PC_APPRVL_RQRD"] == "Yes":
                page.locator("//div[@title='Transfer Rules: Load Time Card Batches']//following::label[text()='Project Costing']").first.click()
                page.wait_for_timeout(2000)
            if datadictvalue["C_P_PC_APPRVL_RQRD"] == "N/A":
                #page.locator("//div[@title='Transfer Rules: Load Time Card Batches']//following::label[text()='Project Costing']").first.click()
                page.wait_for_timeout(2000)
        # Save and Close
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        try:
            expect(page.get_by_role("heading", name="Time Consumer Sets")).to_be_visible()
            print("TIME_CONSUMER_SETS Saved Successfully")
            datadictvalue["RowStatus"] = "Added TIME_CONSUMER_SETS"
        except Exception as e:
            print("Unable to save TIME_CONSUMER_SETS")
            datadictvalue["RowStatus"] = "Unable to Add TIME_CONSUMER_SETS"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, TIME_CONSUMER_SETS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, TIME_CONSUMER_SETS,
                             PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, TIME_CONSUMER_SETS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[
            0] + "_" + TIME_CONSUMER_SETS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
