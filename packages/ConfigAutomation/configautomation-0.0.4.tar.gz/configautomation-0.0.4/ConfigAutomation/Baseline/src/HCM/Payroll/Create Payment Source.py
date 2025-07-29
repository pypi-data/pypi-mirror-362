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

        #Search for Organization Payment Method
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill("")
        page.get_by_label("Name").type(datadictvalue["C_ORG_PAY_MTHD_NAME"])
        page.get_by_role("combobox", name="Legislative Data Group").click()
        page.get_by_text(datadictvalue["C_LGSLTV_DATA_GROUP"], exact=True).first.click()
        page.get_by_placeholder("mm-dd-yyyy").click()
        page.get_by_placeholder("mm-dd-yyyy").fill("")
        page.get_by_placeholder("mm-dd-yyyy").type(datadictvalue["C_EFFCTV_DATE"])
        page.get_by_placeholder("mm-dd-yyyy").press("Tab")
        page.wait_for_timeout(4000)
        page.get_by_role("combobox", name="Payment Type").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYMNT_TYPE"]).click()
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(4000)

        #Edit Organization payment Method
        page.locator("//a[text()='" + datadictvalue["C_ORG_PAY_MTHD_NAME"] + "']//following::a[@title='Edit']").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text("Correct").click()
        page.wait_for_timeout(4000)

        if page.get_by_role("button", name="Yes").is_visible():
            page.get_by_role("button", name="Yes").click()

        #Create payment Source
        page.get_by_role("button", name="Create").first.click()
        page.get_by_label("Name", exact=True).click()
        page.get_by_label("Name", exact=True).type(datadictvalue["C_PAY_SRC_NAME"])

        page.get_by_title("Search: Bank Account Name").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Bank Account", exact=True).click()
        page.get_by_label("Bank Account", exact=True).type(datadictvalue["C_BANK_ACCNT_NAME"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("cell", name=datadictvalue["C_BANK_ACCNT_NAME"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        page.get_by_label("Bank Name").type(datadictvalue["C_BANK_NAME"])
        page.get_by_label("Bank Reference").nth(1).type(datadictvalue["C_BANK_RFRNC"])
        page.get_by_label("Company Name").type(datadictvalue["C_CMPNY_NAME"])
        page.get_by_label("Company Reference", exact=True).type(datadictvalue["C_CMPNY_RFRNC"])

        #page.get_by_text("Yes")
        #page.get_by_title("Search: Report Category for Workers").click()
        #page.get_by_title("Search: Report Category for Third-Party Payees").click()
        # page.get_by_label("Transaction Limit").type(datadictvalue["C_TRNSCTN_LIMIT"])
        # page.get_by_label("Payment Limit").type(datadictvalue["C_PYMNT_LIMIT"])
        # page.get_by_label("Payment Reference").type(datadictvalue["C_PYMNT_RFRNC"])
        # page.get_by_label("Payment Free Text").type(datadictvalue["C_PYMNT_FREE_TEXT"])
        # page.get_by_label("Additional Payment Text").type(datadictvalue["C_ADDTNL_PYMNT_TEXT"])
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(6000)

        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(6000)

        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(20000)


        try:
            expect(page.get_by_role("heading", name="Organization Payment Methods")).to_be_visible()
            print("Added Organization Payment Source Saved Successfully")
            datadictvalue["RowStatus"] = "Added Organization Payment Source"
        except Exception as e:
            print("Unable to save Organization Payment Source")
            datadictvalue["RowStatus"] = "Unable to Add Organization Payment Source"
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Added Organization Payment Source Successfully"
        i = i + 1



    OraSignOut(page, context, browser, videodir)
    return datadict

print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, CREATE_PAYMENT_SOURCE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, CREATE_PAYMENT_SOURCE, PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK, CREATE_PAYMENT_SOURCE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + CREATE_PAYMENT_SOURCE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + CREATE_PAYMENT_SOURCE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


