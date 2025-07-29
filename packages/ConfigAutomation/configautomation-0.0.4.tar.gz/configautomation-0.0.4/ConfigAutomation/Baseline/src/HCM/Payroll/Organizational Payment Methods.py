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
    page.get_by_role("textbox").type("Organization Payment Methods")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Organization Payment Methods").first.click()
    page.wait_for_timeout(4000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        # US Legislative Data Group
        page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Legislative Data Group").click()
        page.get_by_text(datadictvalue["C_LGSLTV_DATA_GROUP"], exact=True).nth(1).click()
        page.locator("//label[text()='Effective Date']//following::input[1]").click()
        page.locator("//label[text()='Effective Date']//following::input[1]").fill("")
        page.locator("//label[text()='Effective Date']//following::input[1]").type(datadictvalue["C_EFFCTV_DATE"])
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Continue").click()

        #Organization Payment Method
        page.get_by_label("Name", exact=True).click()
        page.get_by_label("Name", exact=True).type(datadictvalue["C_NAME"])
        page.get_by_role("combobox", name="Payment Type").click()
        page.get_by_text(datadictvalue["C_PYMNT_TYPE"]).click()
        page.get_by_role("combobox", name="Currency").click()
        page.get_by_text(datadictvalue["C_CRRNCY"], exact=True).first.click()

        #Payment Info
        page.get_by_label("Bank Name").type(datadictvalue["C_BANK_NAME"])
        #page.get_by_label("Bank Reference Type").type(datadictvalue["C_BANK_RFRNC_TYPE"])
        page.get_by_label("Bank Reference").nth(1).type(datadictvalue["C_BANK_RFRNC"])
        page.get_by_label("Company Name").type(datadictvalue["C_CMPNY_NAME"])
        page.get_by_label("Company Reference Type").type(datadictvalue["C_CMPNY_RFRNC_TYPE"])
        #page.get_by_label("Company Reference").nth(1).type(datadictvalue["C_CMPNY_RFRNC"])
        # page.get_by_label("Transaction Limit").type(datadictvalue["C_TRNSCTN_LIMIT"])
        # page.get_by_label("Payment Limit").type(datadictvalue["C_PYMNT_LIMIT"])
        # page.get_by_label("Payment Reference").type(datadictvalue["C_PYMNT_RFRNC"])
        # page.get_by_label("Payment Free Text").type(datadictvalue["C_PYMNT_FREE_TEXT"])
        # page.get_by_label("Additional Payment Text").type(datadictvalue["C_ADDTNL_PYMNT_TEXT"])
        page.wait_for_timeout(3000)
        if datadictvalue["C_PRNTFCTN_RQRD"] == "Yes":
            page.get_by_text("Prenotification Required").check()
            page.get_by_label("Prenotification Days").fill("")
            page.get_by_label("Prenotification Days").type(str(datadictvalue["C_PRNTFCTN_DAYS"]))
            page.get_by_label("Prenotification Amount").fill("")
            page.get_by_label("Prenotification Amount").type(str(datadictvalue["C_PRNTFCTN_AMNT"]))
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(6000)
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(5000)
        #Expect a Warning pop since payment source is not added to the Payment method
        if page.get_by_text("Warning").is_visible():
            if page.get_by_text("You didn't define a payment source").is_visible():
                page.get_by_role("button", name="Yes").click()
        #page.get_by_role("cell", name="Cancel", exact=True).click()
        page.wait_for_timeout(5000)

        try:
            expect(page.get_by_role("heading", name="Organization Payment Methods")).to_be_visible()
            print("Added Organization Payment Methods Saved Successfully")
            datadictvalue["RowStatus"] = "Added Organization Payment Methods"
        except Exception as e:
            print("Unable to save Organization Payment Methods")
            datadictvalue["RowStatus"] = "Unable to Add Organization Payment Methods"
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Added Organization Payment Methods Successfully"
        i = i + 1



    OraSignOut(page, context, browser, videodir)
    return datadict

print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, ORGANIZATION_PAYMENT_METHODS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, ORGANIZATION_PAYMENT_METHODS, PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK, ORGANIZATION_PAYMENT_METHODS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + ORGANIZATION_PAYMENT_METHODS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + ORGANIZATION_PAYMENT_METHODS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

