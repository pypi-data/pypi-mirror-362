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
    page.get_by_role("textbox").fill("Manage Revenue Contingencies")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Revenue Contingencies").click()
    page.wait_for_timeout(3000)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        # Create Revenue Contingencies
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Revenue Contingency Set").fill(datadictvalue["C_RVN_CNTNGNCY_SET"])
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        page.locator("//label[text()='Start Date']//following::input[1]").fill('')
        page.locator("//label[text()='Start Date']//following::input[1]").fill(datadictvalue["C_START_DATE"].strftime('%m/%d/%y'))
        page.locator("//label[text()='End Date']//following::input[1]").fill(datadictvalue["C_END_DATE"])
        page.get_by_label("Comments").fill(datadictvalue["C_CMMNTS"])

        # Revenue Policy
        if datadictvalue["C_RVN_PLCY_THRSHLD"] == 'Yes':
            page.get_by_text("Refund policy threshold").click()
        if datadictvalue["C_PYMNT_TERMS_THRSHLD"] == 'Yes':
            page.get_by_text("Payment terms threshold").click()
        if datadictvalue["C_CRDT_CLASSFCTN"] == 'Yes':
            page.get_by_text("Credit classification").click()
        if datadictvalue["C_NONE"] == 'Yes':
           if not page.get_by_text("None").is_checked():
               page.get_by_text("None").click()
        if datadictvalue["C_NONE"] == 'No':
            if page.get_by_text("None").is_checked():
                page.get_by_text("None").click()

        # Contingency Removal Events

        page.get_by_label("Primary Removal Event").select_option(datadictvalue["C_PRMRY_RMVL_EVENT"] )
        page.get_by_label("Optional Removal Event", exact=True).select_option(datadictvalue["C_OPTNL_RMVL_EVENT"] )
        page.get_by_label("Days After Optional Removal").fill(str(datadictvalue["C_DAYS_AFTER_OPTNL_RMVL_EVENT"]))

        # Save and Close

        # page.get_by_role("button", name="Cancel").click()
        page.get_by_role("button", name="Save and Close").click()


        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1
        page.wait_for_timeout(3000)
    page.get_by_role("button", name="Done").click()
    page.wait_for_timeout(3000)



    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Auto Match Rule Sets Saved Successfully")

    except Exception as e:
        print("Auto Match Rule Sets not Saved")


    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, REVENUE_CONTINGENCIES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, REVENUE_CONTINGENCIES, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, REVENUE_CONTINGENCIES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + REVENUE_CONTINGENCIES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + REVENUE_CONTINGENCIES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))