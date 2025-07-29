from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)

    #Navigation
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="My Client Groups").click()
    page.wait_for_timeout(1000)
    page.get_by_role("link", name="Show more quick actions").click()
    page.wait_for_timeout(1000)
    page.get_by_role("link", name="Third Parties").click()


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        #Search whether the party name is already present to avoid Duplicacy
        page.get_by_label("Party Name").clear()
        page.get_by_label("Party Name").type(datadictvalue["C_NAME"])
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Party Usage Code").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PARTY_USGE_CODE"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Party Type").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PARTY_TYPE"], exact=True).click()
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(5000)


        if page.get_by_role("cell", name=datadictvalue["C_NAME"], exact=True).first.is_visible():
            print(datadictvalue["C_NAME"] + "Already present in Application")
            page.wait_for_timeout(2000)
        else:
            page.get_by_role("button", name="Create", exact=True).click()
            page.wait_for_timeout(4000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text("Organization", exact=True).click()
            page.wait_for_timeout(1000)
            page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Party Usage Code").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PARTY_USGE_CODE"]).click()
            page.get_by_role("button", name="Continue").click()
            page.wait_for_timeout(5000)
            page.get_by_label("Name").click()
            page.get_by_label("Name").type(datadictvalue["C_NAME"])
            page.get_by_label("Name").press("Tab")
            page.wait_for_timeout(5000)

            #Add Address
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Address Line 1").click()
            page.get_by_label("Address Line 1").type(datadictvalue["C_ADDRSS_LINE_1"])
            page.get_by_label("Address Line 2").click()
            page.get_by_label("Address Line 2").type(datadictvalue["C_ADDRSS_LINE_2"])
            page.wait_for_timeout(1000)
            page.get_by_title("Postal Code").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(1000)
            page.get_by_role("textbox", name="Postal Code").click()
            page.get_by_role("textbox", name="Postal Code").type(str(datadictvalue["C_PSTL_CODE"]))
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            print(i)
            print(str(datadictvalue["C_PSTL_CODE"]) + "," + " " + datadictvalue["C_CITY"])
            page.wait_for_timeout(2000)
            page.get_by_text(str(datadictvalue["C_PSTL_CODE"]) + "," + " " + datadictvalue["C_CITY"]).first.click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="OK").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_placeholder("m/d/yy").click()
            page.get_by_placeholder("m/d/yy").fill("")
            page.get_by_placeholder("m/d/yy").type(datadictvalue["C_EFFCTV_DATE"])
            page.get_by_placeholder("m/d/yy").press("Tab")
            page.wait_for_timeout(1000)

            #Add Purpose
            page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Add Row").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name="Purpose", exact=True).locator("a").click()
            page.wait_for_timeout(1000)
            page.get_by_text(datadictvalue["C_PRPS"]).click()
            page.wait_for_timeout(1000)
            page.get_by_placeholder("m/d/yy").nth(1).click()
            page.get_by_placeholder("m/d/yy").nth(1).fill("")
            page.get_by_placeholder("m/d/yy").nth(1).type(datadictvalue["C_FROM_DATE"])
            page.get_by_placeholder("m/d/yy").nth(1).press("Tab")
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Set Primary").first.click()
            page.wait_for_timeout(4000)
            page.get_by_role("button", name="Submit").click()
            page.wait_for_timeout(5000)

            #Select LDG and Navigate to Organization payment method screen
            page.get_by_role("combobox", name="Legislative Data Group").click()
            page.get_by_text(datadictvalue["C_LGSLTV_DATA_GROUP"], exact=True).first.click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Yes").click()
            page.wait_for_timeout(4000)
            page.get_by_title("Search: Organization Payment").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(1000)
            page.get_by_role("textbox", name="Organization Payment Method").click()
            page.get_by_role("textbox", name="Organization Payment Method").type(str(datadictvalue["C_ORGNZTN_PYMNT_MTHOD"]))
            page.locator("//label[text()='Effective As-of Date']//following::input[1]").clear()
            page.locator("//label[text()='Effective As-of Date']//following::input[1]").type(datadictvalue["C_EFFCTV_DATE"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ORGNZTN_PYMNT_MTHOD"]).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(5000)
            page.get_by_placeholder("m/d/yy").clear()
            page.get_by_placeholder("m/d/yy").type(datadictvalue["C_EFFCTV_START_DATE"])
            page.get_by_placeholder("m/d/yy").press("Tab")
            # page.wait_for_timeout(5000)
            # page.get_by_placeholder("m/d/yy").first.click()
            # page.get_by_placeholder("m/d/yy").first.fill("")
            # page.get_by_placeholder("m/d/yy").first.type(datadictvalue["C_EFFCTV_START_DATE"])
            # page.wait_for_timeout(4000)
            if datadictvalue["C_ORGNZTN_PYMNT_MTHOD"] == "Direct Deposit":
                page.get_by_role("button", name="Create").click()
                page.wait_for_timeout(2000)
                page.get_by_role("textbox", name="Account Number").click()
                page.get_by_role("textbox", name="Account Number").type(str(datadictvalue["C_BANK_ACCNT"]))
                page.get_by_label("Account Type").click()
                page.wait_for_timeout(1000)
                page.get_by_text(datadictvalue["C_ACCNT_TYPE"]).click()
                page.wait_for_timeout(1000)
                page.get_by_role("textbox", name="Bank", exact=True).type(datadictvalue["C_BANK_NAME"])
                page.get_by_role("textbox", name="Bank Branch", exact=True).type(datadictvalue["C_BANK_BRNCH"])
                page.get_by_role("textbox", name="Routing Number").type(str(datadictvalue["C_ROUTE_NUM"]))
                page.wait_for_timeout(4000)
                page.pause()
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(4000)
                if page.locator("//span[text()='Y']").is_visible():
                    page.locator("//span[text()='Y']").click()
                    page.wait_for_timeout(3000)
            page.wait_for_timeout(5000)
            page.get_by_role("button", name="Save").click()
            page.wait_for_timeout(6000)
            page.get_by_role("button", name="Submit").click()
            page.wait_for_timeout(7000)


        try:
            expect(page.get_by_role("heading", name="Third Parties")).to_be_visible()
            print("Added Third Party Saved Successfully")
            datadictvalue["RowStatus"] = "Added Third Party and code"
        except Exception as e:
            print("Unable to save Third Party")
            datadictvalue["RowStatus"] = "Unable to Add Third Party and code"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, THIRD_PARTY_ORG):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, THIRD_PARTY_ORG, PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK, THIRD_PARTY_ORG)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + THIRD_PARTY_ORG)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + THIRD_PARTY_ORG + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
