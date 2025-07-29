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
    page.get_by_label("Search Tasks").fill("Manage Common Options for Payables and Procurement")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(2000)
    page.locator("//a[text()='Manage Common Options for Payables and Procurement']//following::a[1]").click()    # page.get_by_role("link", name="Manage Common Options for Payables and Procurement").click()
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
        page.locator("//h1[text()='Default Distributions']//following::input[1]").fill(datadictvalue["C_LBLTY"])
        page.get_by_label("Prepayment", exact=True).fill(datadictvalue["C_PRPYMNT"])
        page.get_by_label("Bill Payable").fill(datadictvalue["C_BILL_PYBL"])
        page.get_by_label("Conversion Rate Variance Gain").fill(datadictvalue["C_CNVRSN_RATE_VRNC_GAIN"])
        page.get_by_label("Conversion Rate Variance Loss").fill(datadictvalue["C_CNVRSN_RATE_VRNC_LOSS"])
        page.get_by_label("Discount Taken").fill(datadictvalue["C_DSCNT_TAKEN"])
        page.get_by_label("Miscellaneous").fill(datadictvalue["C_MSCLLNS"])
        page.get_by_label("Freight").fill(datadictvalue["C_FRGHT"])
        page.get_by_label("Prepayment Tax Difference").fill(datadictvalue["C_PRPYMNT_TAX_DFFRNC"])
        page.wait_for_timeout(2000)
        page.get_by_label("Retainage").fill(datadictvalue["C_RTNG"])
        page.get_by_text(datadictvalue["C_OFFST_SGMNTS"]).click()
        page.wait_for_timeout(3000)
        if page.get_by_role("button", name="Yes").is_visible():
            page.get_by_role("button", name="Yes").click()

        page.locator("//h1[text()='One Time Payments']//following::input[1]").fill(datadictvalue["C_ONE_TIME_LBLTY"])
        page.get_by_label("Expense", exact=True).fill(datadictvalue["C_EXPNS"])
        page.wait_for_timeout(1000)


        if datadictvalue["C_RQR_CNVRSN_RATE_ENTRY"] == 'Yes':
            page.get_by_text("Require conversion rate entry").check()
        if datadictvalue["C_RQR_CNVRSN_RATE_ENTRY"] == 'No':
            page.get_by_text("Require conversion rate entry").uncheck()

        page.get_by_title("Conversion Rate Type").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Conversion Rate Type").fill(datadictvalue["C_CNVRSN_RATE_TYPE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Realized Gain Distribution").fill(datadictvalue["C_RLZD_GAIN_DSTRBTN"])
        page.get_by_label("Realized Loss Distribution").fill(datadictvalue["C_RLZD_LOSS_DSTRBTN"])
        page.get_by_label("Accrue Expense Items").select_option(datadictvalue["C_ACCR_EXPNS_ITEMS"])
        if datadictvalue["C_GPLSS_INVC_NMBRNG"] == 'Yes':
            page.get_by_text("Gapless invoice numbering").check()
        if datadictvalue["C_GPLSS_INVC_NMBRNG"] == 'No':
            page.get_by_text("Gapless invoice numbering").uncheck()

        if page.get_by_label("Buying Company Identifier").is_enabled():
            page.get_by_label("Buying Company Identifier").fill(datadictvalue["C_BYNG_CMPNY_DNTFR"])
        if datadictvalue["C_VAT_RGSTRTN_MMBR_STATE"] != '':
            page.get_by_title("VAT Registration Member State").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Territory Name").click()
            page.get_by_label("Territory Name").fill(datadictvalue["C_VAT_RGSTRTN_MMBR_STATE"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VAT_RGSTRTN_MMBR_STATE"]).click()
            page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_BILL_TO_LCTN"] != '':
            page.get_by_title("Bill-to Location").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_BILL_TO_LCTN"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BILL_TO_LCTN"]).click()
            page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_label("VAT Registration Number").fill(datadictvalue["C_VAT_RGSTRTN_NMBR"])
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(4000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Common options are added successfully"

        i = i + 1

    try:
        expect(page.get_by_text("Search Tasks")).to_be_visible()
        print("Common Options for Payables and Procurement Saved Successfully")

    except Exception as e:
        print("Common Options for Payables and Procurement not saved")

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, COMMON_OPTIONS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, COMMON_OPTIONS, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, COMMON_OPTIONS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + COMMON_OPTIONS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
            0] + "_" + COMMON_OPTIONS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

