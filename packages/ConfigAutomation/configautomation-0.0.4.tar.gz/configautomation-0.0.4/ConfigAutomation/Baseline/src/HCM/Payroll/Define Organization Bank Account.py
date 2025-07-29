from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox").type("Manage Bank Accounts")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Bank Accounts").first.click()
    page.wait_for_timeout(4000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(5000)

        page.get_by_label("Bank Branch").click()
        page.get_by_label("Bank Branch").type(datadictvalue["C_BRNCH_NAME"])
        page.wait_for_timeout(1000)
        page.get_by_role("option", name=datadictvalue["C_BRNCH_NAME"]).click()
        page.wait_for_timeout(1000)
        page.get_by_label("Account Name", exact=True).click()
        page.get_by_label("Account Name", exact=True).type(datadictvalue["C_ACCNT_NAME"])
        page.get_by_label("Account Number", exact=True).click()
        page.get_by_label("Account Number", exact=True).type(str(datadictvalue["C_ACCNT_NMBR"]))
        page.get_by_label("Currency", exact=True).click()
        page.get_by_label("Currency", exact=True).select_option(datadictvalue["C_CRRNCY"])
        page.get_by_label("Legal Entity Name").click()
        page.get_by_label("Legal Entity Name").type(datadictvalue["C_LEGAL_ENTTY_NAME"])
        page.get_by_label("Legal Entity Name").press("Tab")
        page.get_by_label("Account Type").click()
        page.get_by_label("Account Type").select_option(datadictvalue["C_ACCNT_TYPE"])
        page.get_by_label("Description").click()
        page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])

        # page.get_by_label("IBAN").click()
        # page.get_by_label("Check Digit").click()
        # page.get_by_label("Secondary Account Reference").click()
        # page.get_by_label("Account Suffix").click()

        if datadictvalue["C_ACCNT_USE"] == "Payroll":
            if not page.get_by_text(datadictvalue["C_ACCNT_USE"]).is_checked():
                page.get_by_text(datadictvalue["C_ACCNT_USE"]).click()

        page.wait_for_timeout(1000)
        # page.get_by_role("button", name="Save", exact=True).click()
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)
        if page.get_by_text("Information").is_visible():
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)

        try:
            expect(page.get_by_role("heading", name="Manage Bank Accounts")).to_be_visible()
            print("Added Bank Accounts details Saved Successfully")
            datadictvalue["RowStatus"] = "Added Bank Accounts details and code"
        except Exception as e:
            print("Unable to save Bank Accounts details")
            datadictvalue["RowStatus"] = "Unable to Add Bank Accounts details and code"
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Added Bank Accounts details Successfully"
        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, MANAGE_BANK_ACCOUNTS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, MANAGE_BANK_ACCOUNTS, PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK, MANAGE_BANK_ACCOUNTS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + MANAGE_BANK_ACCOUNTS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + MANAGE_BANK_ACCOUNTS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
