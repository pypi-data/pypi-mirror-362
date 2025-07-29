from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *



def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    # Sign In - Instance
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    # Navigate to the Required Page
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage AutoMatch Rule Set")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage AutoMatch Rule Set").click()
    page.wait_for_timeout(3000)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        # Create Match Rule
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)
        #  General Information
        page.get_by_label("Set", exact=True).fill(datadictvalue["C_SET"])
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        page.locator("//label[text()='Start Date']//following::input[1]").clear()
        page.locator("//label[text()='Start Date']//following::input[1]").fill(datadictvalue["C_START_DATE"].strftime('%m/%d/%y'))
        page.locator("//label[text()='End Date']//following::input[1]").clear()
        page.locator("//label[text()='End Date']//following::input[1]").fill(datadictvalue["C_END_DATE"])


        if datadictvalue["C_ACTV"] == 'Yes' :
            if not page.get_by_text("Active").is_checked():
                page.get_by_text("Active").click()
        elif datadictvalue["C_ACTV"] == 'Yes' :
            if page.get_by_text("Active").is_checked():
                page.get_by_text("Active").click()


        # Receipt Application Recommendation Score
        page.get_by_label("Customer Recommendation").fill(str(datadictvalue["C_CSTMR_RCMMNDTN_THRSHLD"]))
        page.get_by_label("Minimum Match Threshold").fill(str(datadictvalue["C_MNMM_MATCH_THRSHLD"]))
        page.get_by_label("Combined Weighted Threshold").fill(str(datadictvalue["C_CMBND_WGHTD_THRSHLD"]))
        page.get_by_label("Days of Closed Invoices").fill(str(datadictvalue["C_DAYS_OF_CLSD_INVCS_THRSHLD"]))

        #Combined Weighted Threshold Details

        page.get_by_label("Customer Weight").fill(str(datadictvalue["C_CSTMR_WGHT"]))
        page.get_by_label("Transaction Weight").fill(str(datadictvalue["C_TRNSCTN_WGHT"]))
        page.get_by_label("Amount Weight").fill(str(datadictvalue["C_AMNT_WGHT"]))

        # Transaction Strings
        if datadictvalue["C_TRNSCTN_STRNG_LCTN"] != '':
            page.get_by_role("button", name="Add Row").first.click()
            page.get_by_label("String Location").select_option(datadictvalue["C_TRNSCTN_STRNG_LCTN"])
            page.get_by_label("String Value").select_option(datadictvalue["C_TRNSCTN_STRNG_VALUE"])
            page.get_by_label("Number of Characters").fill(datadictvalue["C_TRNSCTN_NMBR_OF_CHRCTRS "])

        if datadictvalue["C_RMTTNC_STRNG_LCTN"] != '':
            page.get_by_role("button", name="Add Row").nth(1).click()
            page.get_by_role("table", name="Remittance Strings").get_by_label("String Location").select_option(datadictvalue["C_RMTTNC_STRNG_LCTN"])
            page.get_by_role("table", name="Remittance Strings").get_by_label("String Value").select_option(datadictvalue["C_RMTTNC_STRNG_VALUE"])
            page.get_by_role("table", name="Remittance Strings").get_by_label("Number of Characters").fill(datadictvalue["C_RMTTNC_NMBR_OF_CHRCTRS"])


        # Save and Close

        page.get_by_role("button", name="Save and Close").click()


        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        page.wait_for_timeout(5000)

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Auto Match Rule Sets Saved Successfully")

    except Exception as e:
        print("Auto Match Rule Sets not Saved")


    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, AUTOMATCH_RULE_SET):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, AUTOMATCH_RULE_SET, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, AUTOMATCH_RULE_SET)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + AUTOMATCH_RULE_SET)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + AUTOMATCH_RULE_SET + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))