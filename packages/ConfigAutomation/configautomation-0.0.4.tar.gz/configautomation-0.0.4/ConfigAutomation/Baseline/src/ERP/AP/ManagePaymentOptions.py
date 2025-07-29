from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
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
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="Offering").click()
    page.get_by_text("Financials", exact=True).click()
    page.wait_for_timeout(2000)

    # Navigating to respective option in Legal Search field and searching
    page.locator("//td[text()='Payables']").click()
    page.wait_for_timeout(2000)
    page.get_by_label("Search Tasks").click()
    page.get_by_label("Search Tasks").fill("Manage Payment Options")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(2000)
    page.locator("//a[text()='Manage Payment Options']//following::a[1]").click()  # page.get_by_role("link", name="Manage Invoice Options").click()
    page.get_by_label("Business Unit", exact=True).select_option("Select and Add")
    page.get_by_role("button", name="Apply and Go to Task").click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_label("Name").fill(datadictvalue["C_BSNSS_UNIT"])
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name=datadictvalue["C_BSNSS_UNIT"], exact=True).click()
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        #Payment Accounting and Overrides

        if datadictvalue["C_ALLOW_PYMNT_DATE_BFR_THE_SYSTM_DATE"] == 'Yes':
            page.get_by_text("Allow payment date before the").check()
        if datadictvalue["C_ALLOW_PYMNT_DATE_BFR_THE_SYSTM_DATE"] == 'No':
            page.get_by_text("Allow payment date before the").uncheck()
        if datadictvalue["C_ALLOW_OVRRD_OF_SPPLR_SITE_BANK_ACCNT"] == 'Yes':
            page.get_by_text("Allow override of supplier").check()
        if datadictvalue["C_ALLOW_OVRRD_OF_SPPLR_SITE_BANK_ACCNT"] == 'No':
            page.get_by_text("Allow override of supplier").uncheck()
        if datadictvalue["C_ALLOW_DCMNT_CTGRY_OVRRD"] == 'Yes':
            page.get_by_text("Allow document category").check()
        if datadictvalue["C_ALLOW_DCMNT_CTGRY_OVRRD"] == 'No':
            page.get_by_text("Allow document category").uncheck()
        if datadictvalue["C_ALLOW_PAYEE_OVRRD_FOR_THIRD_PARTY_PYMNTS"] == 'Yes':
            page.get_by_text("Allow payee override for").check()
        if datadictvalue["C_ALLOW_PAYEE_OVRRD_FOR_THIRD_PARTY_PYMNTS"] == 'No':
            page.get_by_text("Allow payee override for").uncheck()
        page.get_by_text(datadictvalue["C_ACCNT_FOR_PYMNT"], exact=True).click()
        page.wait_for_timeout(3000)
        if page.get_by_role("button", name="OK").is_visible():
            page.get_by_role("button", name="OK").click()

        #Currency Conversion

        if datadictvalue["C_RQR_CNVRSN_RATE_ENTRY"] == 'Yes':
            page.get_by_text("Require conversion rate entry").check()
        if datadictvalue["C_RQR_CNVRSN_RATE_ENTRY"] == 'No':
            page.get_by_text("Require conversion rate entry").uncheck()
        page.get_by_title("Conversion Rate Type").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Conversion Rate Type").clear()
        page.get_by_role("textbox", name="Conversion Rate Type").fill(datadictvalue["C_CNVRSN_RATE_TYPE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CNVRSN_RATE_TYPE"]).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        #Bank Charges

        page.get_by_label("Bank Charge Deduction Type").select_option(datadictvalue["C_BANK_CHRG_DDCTN_TYPE"])
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(4000)

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)

        try:
            expect(page.get_by_text("Search Tasks")).to_be_visible()
            print("Payment options Saved Successfully")
            datadictvalue["RowStatus"] = "Payment options are added successfully"
        except Exception as e:
            print("Payment options not saved")
            datadictvalue["RowStatus"] = "Payment options are not added"
        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYMENT_OPTIONS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYMENT_OPTIONS, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, PAYMENT_OPTIONS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + PAYMENT_OPTIONS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
            0] + "_" + PAYMENT_OPTIONS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))