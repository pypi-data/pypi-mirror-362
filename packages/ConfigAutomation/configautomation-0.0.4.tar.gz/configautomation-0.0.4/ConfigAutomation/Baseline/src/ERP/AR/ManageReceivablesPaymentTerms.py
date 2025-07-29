from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Receivables Payment Terms")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Receivables Payment Terms", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Create").click()

        #Payment terms Set.
        page.get_by_title("Search: Payment Terms Set").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Reference Data Set Name").click()
        page.get_by_label("Reference Data Set Name").fill(datadictvalue["C_PYMNT_TERMS_SET"])
        page.get_by_label("Reference Data Set Name").press("Enter")
        page.get_by_role("cell", name=datadictvalue["C_PYMNT_TERMS_SET"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(1000)

        #Name
        page.get_by_label("Name",exact=True).click()
        page.get_by_label("Name",exact=True).fill(datadictvalue["C_NAME"])

        #Description
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])


        #Allow discount on partial payments
        if datadictvalue["C_ALLOW_DSCNT_ON_PRTL_PYMNTS"]!='':
            if datadictvalue["C_ALLOW_DSCNT_ON_PRTL_PYMNTS"] == 'Yes':
                page.get_by_text("Allow discount on partial payments",exact=True).check()
            elif datadictvalue["C_ALLOW_DSCNT_ON_PRTL_PYMNTS"] == 'No':
                page.get_by_text("Allow discount on partial payments",exact=True).uncheck()

        #Prepayment
        if datadictvalue["C_PRPYMNT"]!='':
            if datadictvalue["C_PRPYMNT"] == 'Yes':
                page.get_by_text("Prepayment",exact=True).check()
            elif datadictvalue["C_PRPYMNT"] == 'No':
                page.get_by_text("Prepayment",exact=True).uncheck()

        #Credit check
        if datadictvalue["C_CRDT_CHECK"]!='':
            if datadictvalue["C_CRDT_CHECK"] == 'Yes':
                page.get_by_text("Credit check",exact=True).check()
            elif datadictvalue["C_CRDT_CHECK"] == 'No':
                page.get_by_text("Credit check",exact=True).uncheck()


        #Billing Cycle
        #page.get_by_title("Search: Billing Cycle").click()
        #page.get_by_role("link", name="Search...").click()
        #page.get_by_role("textbox", name="Billing Cycle").click()
        #page.get_by_role("textbox", name="Billing Cycle").fill(datadictvalue["C_BLLNG_CYCLE"])
        #page.get_by_role("button", name="Search", exact=True).click()
        #page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BLLNG_CYCLE"]).click()
        #page.get_by_role("button", name="OK").click()


        #Base Amount
        page.get_by_label("Base Amount").click()
        page.get_by_label("Base Amount").fill(str(datadictvalue["C_BASE_AMNT"]))
        page.wait_for_timeout(2000)

        #Discount Basis
        page.get_by_label("Discount Basis", exact=True).select_option(datadictvalue["C_DSCNT_BASIS"])
        page.wait_for_timeout(2000)

        #Discount Basis Date
        page.get_by_label("Discount Basis Date").select_option(datadictvalue["C_DSCNT_BASIS_DATE"])

        #From Date
        if datadictvalue["C_FROM_DATE"] != '':
            page.locator("//label[text()='From Date']//following::input[1]").fill(
                datadictvalue["C_FROM_DATE"].strftime('%m/%d/%y'))

        #To Date
        if datadictvalue["C_TO_DATE"] != '':
            page.locator("//label[text()='To Date']//following::input[1]").fill(
                datadictvalue["C_TO_DATE"].strftime('%m/%d/%y'))

        #Print Lead Days
        page.get_by_label("Print Lead Days").fill(datadictvalue["C_PRINT_LEAD_DAYS"])
        page.wait_for_timeout(3000)


        #Installment Option
        page.get_by_label("Installment Option").select_option(datadictvalue["C_INSTLLMNT_OPTN"])
        page.wait_for_timeout(3000)

        #payments
        page.get_by_role("button", name="Add Row").first.click()
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name="1", exact=True).click()
        page.wait_for_timeout(3000)
        #page.get_by_label("Sequence").click()
        #page.wait_for_timeout(3000)
        #page.get_by_label("Sequence").fill(datadictvalue["C_SQNCE"])
        #page.wait_for_timeout(3000)
        #page.get_by_label("Relative Amount").click()
        #page.get_by_label("Relative Amount").fill(datadictvalue["C_RLTV_AMNT"])
        #page.wait_for_timeout(3000)
        page.get_by_label("Days", exact=True).click()
        page.get_by_label("Days", exact=True).fill(str(datadictvalue["C_PYMNT_DAYS"]))
        page.wait_for_timeout(2000)

        #Discounts
        if datadictvalue["C_PRCNTG"] != "":
            page.get_by_role("button", name="Add Row").nth(1).click()
            page.wait_for_timeout(3000)
            page.get_by_label("Percentage").click()
            page.get_by_label("Percentage").fill(str(datadictvalue["C_PRCNTG"]))

            page.get_by_role("table", name="Discounts").get_by_label("Days").click()
            page.get_by_role("table", name="Discounts").get_by_label("Days").fill(str(datadictvalue["C_DYS"]))



        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save", exact=True).click()
        page.get_by_role("button", name="Save and Close").click()

        # Repeating the loop
        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Manage Receivable Payment Terms saved Successfully")
            datadictvalue["RowStatus"] = "Manage Receivable Payment Terms added successfully"

        except Exception as e:
            print("Manage Receivable Payment Terms not saved")
            datadictvalue["RowStatus"] = "Manage Receivable Payment Terms not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, PYMNT_TERMS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, PYMNT_TERMS, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, PYMNT_TERMS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + PYMNT_TERMS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + PYMNT_TERMS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))