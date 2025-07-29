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
    page.get_by_role("textbox").fill("Manage Transaction Types")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Transaction Types", exact=True).click()

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Transaction Type Set").type(datadictvalue["C_TRNSCTN_TYPE_SET"])
        page.get_by_role("option", name=datadictvalue["C_TRNSCTN_TYPE_SET"]).click()
        if datadictvalue["C_LEGAL_ENTTY"] != '':
            page.get_by_label("Legal Entity").type(datadictvalue["C_LEGAL_ENTTY"])
            page.get_by_role("option", name=datadictvalue["C_LEGAL_ENTTY"]).click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Transaction Class").select_option(datadictvalue["C_TRNSCTN_CLASS"])
        page.wait_for_timeout(2000)
        if page.get_by_label("Transaction Status").is_enabled():
            page.get_by_label("Transaction Status").select_option(datadictvalue["C_TRNSCTN_STTS"])
        if datadictvalue["C_FROM_DATE"] != '':
            page.locator("//label[text()='From Date']//following::input[1]").fill(datadictvalue["C_FROM_DATE"].strftime('%m/%d/%y'))
        if datadictvalue["C_TO_DATE"] != '':
            page.locator("//label[text()='To Date']//following::input[1]").fill(datadictvalue["C_TO_DATE"].strftime('%m/%d/%y'))
        if page.get_by_label("Creation Sign").is_enabled():
            page.get_by_label("Creation Sign").select_option(datadictvalue["C_CRTN_SIGN"])
        # page.get_by_label("Usage Category").select_option("1")
        if page.get_by_label("Generate Bill").is_enabled():
            page.get_by_label("Generate Bill").select_option(datadictvalue["C_GNRT_BILL"])
        if page.get_by_label("Invoice Type").is_enabled():
            if datadictvalue["C_INVC_TYPE"] != '':
                page.get_by_title("Search: Invoice Type").click()
                page.get_by_role("link", name="Search...").click()
                page.locator("//div[text()='Search and Select: Invoice Type']//following::label[text()='Name']//following::input[1]").get_by_label("Name").click()
                page.locator("//div[text()='Search and Select: Invoice Type']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_INVC_TYPE"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.get_by_role("cell", name=datadictvalue["C_INVC_TYPE"], exact=True).click()
                page.get_by_role("button", name="OK").click()
        if page.get_by_label("Credit Memo Type").is_enabled():
            if datadictvalue["C_CRDT_MEMO_TYPE"] != '':
                page.get_by_title("Search: Credit Memo Type").click()
                page.get_by_role("link", name="Search...").click()
                page.locator("//div[text()='Search and Select: Credit Memo Type']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_CRDT_MEMO_TYPE"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.get_by_role("cell", name=datadictvalue["C_CRDT_MEMO_TYPE"], exact=True).click()
                page.get_by_role("button", name="OK").click()
        if page.get_by_label("Application Rule Set").is_enabled():
            if datadictvalue["C_APPLCTN_RULE_SET"] != '':
                page.get_by_title("Search: Application Rule Set").click()
                page.get_by_role("link", name="Search...").click()
                page.locator("//div[text()='Search and Select: Application Rule Set']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_APPLCTN_RULE_SET"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.get_by_role("cell", name=datadictvalue["C_APPLCTN_RULE_SET"], exact=True).click()
                page.get_by_role("button", name="OK").click()
        if page.get_by_label("Payment Terms").is_enabled():
            if datadictvalue["C_PYMNT_TERMS"] != '':
                page.get_by_title("Search: Payment Terms").click()
                page.get_by_role("link", name="Search...").click()
                page.locator("//div[text()='Search and Select: Payment Terms']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_PYMNT_TERMS"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.get_by_role("cell", name=datadictvalue["C_PYMNT_TERMS"], exact=True).click()
                page.get_by_role("button", name="OK").click()
        if page.get_by_text("Open Receivable").is_enabled():
            if datadictvalue["C_OPEN_RCVBL"] == 'Y':
                page.get_by_text("Open Receivable").check()
            if datadictvalue["C_OPEN_RCVBL"] == 'N':
                page.get_by_text("Open Receivable").uncheck()
        if page.get_by_text("Allow freight").is_enabled():
            if datadictvalue["C_ALLOW_FRGHT"] == 'Y':
                page.get_by_text("Allow freight").check()
            if datadictvalue["C_ALLOW_FRGHT"] == 'N':
                page.get_by_text("Allow freight").uncheck()
        if page.get_by_text("Post to GL").is_enabled():
            if datadictvalue["C_POST_TO_GL"] == 'Y':
                page.get_by_text("Post to GL").check()
            if datadictvalue["C_POST_TO_GL"] == 'N':
                page.get_by_text("Post to GL").uncheck()
        if page.get_by_text("Allow adjustment posting").is_enabled():
            if datadictvalue["C_ALLOW_ADJSTMNT_PSTNG"] == 'Y':
                page.get_by_text("Allow adjustment posting").check()
            if datadictvalue["C_ALLOW_ADJSTMNT_PSTNG"] == 'N':
                page.get_by_text("Allow adjustment posting").uncheck()
        if page.get_by_text("Default tax classification").is_enabled():
            if datadictvalue["C_DFLT_TAX_CLSSFCTN_CODE"] == 'Y':
                page.get_by_text("Default tax classification").check()
            if datadictvalue["C_DFLT_TAX_CLSSFCTN_CODE"] == 'N':
                page.get_by_text("Default tax classification").uncheck()
        if page.get_by_text("Natural application only").is_enabled():
            if datadictvalue["C_NTRL_APPLCTN_ONLY"] == 'Y':
                page.get_by_text("Natural application only").check()
            if datadictvalue["C_NTRL_APPLCTN_ONLY"] == 'N':
                page.get_by_text("Natural application only").uncheck()
        if page.get_by_text("Allow overapplication").is_enabled():
            if datadictvalue["C_ALLOW_OVRPPLCTN"] == 'Y':
                page.get_by_text("Allow overapplication").check()
            if datadictvalue["C_ALLOW_OVRPPLCTN"] == 'N':
                page.get_by_text("Allow overapplication").uncheck()
        if page.get_by_text("Exclude from late charges").is_enabled():
            if datadictvalue["C_EXCLD_FROM_LATE_CHRGS_CLCLTN"] == 'Y':
                page.get_by_text("Exclude from late charges").check()
            if datadictvalue["C_EXCLD_FROM_LATE_CHRGS_CLCLTN"] == 'N':
                page.get_by_text("Exclude from late charges").uncheck()
        # if page.get_by_text("No future dates with").is_enabled():
        #     if datadictvalue[""] == 'Y':
                # page.get_by_text("No future dates with").check()
        page.wait_for_timeout(2000)

        if datadictvalue["C_BSNSS_UNIT"] != '':
            page.get_by_role("link", name="Create").click()
            page.wait_for_timeout(2000)
            page.get_by_title("Search: Business Unit").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.locator("//div[text()='Search and Select: Business Unit']//following::label[text()='Name']//following::input[1]").click()
            page.locator("//div[text()='Search and Select: Business Unit']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(1000)
            page.locator("//div[text()='Search and Select: Business Unit']//following::span[text()='"+datadictvalue["C_BSNSS_UNIT"]+"']").click()
            # page.get_by_text(datadictvalue["C_BSNSS_UNIT"]).nth(3).click()
            page.get_by_role("button", name="OK").nth(1).click()
            page.wait_for_timeout(2000)
            page.locator("(//div[text()='Create Reference Accounts']//following::label[text()='Revenue']//following::input[1])[1]").fill(datadictvalue["C_RVN"])
            page.locator("(//div[text()='Create Reference Accounts']//following::label[text()='Receivable']//following::input[1])[1]").fill(datadictvalue["C_RCVBL"])
            page.locator("(//div[text()='Create Reference Accounts']//following::label[text()='Tax']//following::input[1])[1]").fill(datadictvalue["C_TAX"])
            page.locator("(//div[text()='Create Reference Accounts']//following::label[text()='Freight']//following::input[1])[1]").fill(datadictvalue["C_FRGHT"])
            page.locator("(//div[text()='Create Reference Accounts']//following::label[text()='Unearned Revenue']//following::input[1])[1]").fill(datadictvalue["C_UNRND_RVN"])
            page.locator("(//div[text()='Create Reference Accounts']//following::label[text()='Unbilled Receivable']//following::input[1])[1]").fill(datadictvalue["C_UNBLLD_RCVBL"])
            page.locator("(//div[text()='Create Reference Accounts']//following::label[text()='AutoInvoice Clearing']//following::input[1])[1]").fill(datadictvalue["C_ATNVC_CLRNG"])
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Transaction Types saved Successfully")
            datadictvalue["RowStatus"] = "Transaction Types added successfully"

        except Exception as e:
            print("Transaction Types not saved")
            datadictvalue["RowStatus"] = "Transaction Types not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, TRANS_TYPES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, TRANS_TYPES, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, TRANS_TYPES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + TRANS_TYPES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + TRANS_TYPES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

