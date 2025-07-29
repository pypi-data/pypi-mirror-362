from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)

    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Payment System")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Payment Systems").click()

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        if datadictvalue["C_NAME"] != PrevName:

            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)
    #Header
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.get_by_label("Code").click()
            page.get_by_label("Code").fill(datadictvalue["C_CODE"])
            page.get_by_label("Processing Model").click()
            page.get_by_label("Processing Model").select_option(datadictvalue["C_PRCSSNG_MODEL"])
            page.locator("//label[text()='Bank']//following::input[1]").click()
            page.locator("//label[text()='Bank']//following::input[1]").fill(datadictvalue["C_BANK"])

            page.get_by_label("Network Communication").select_option(datadictvalue["C_NTWRK_CMMNCTN_CHRCTR_SET"])
            page.get_by_label("Transmission Servlet Base URL").click()
            page.get_by_label("Transmission Servlet Base URL").fill(datadictvalue["C_TRNSMSSN_SRVLT_BASE_URL"])
            page.get_by_label("Administrative URL").click()
            page.get_by_label("Administrative URL").fill(datadictvalue["C_ADMNSTRTV_URL"])
            page.locator("//label[text()='From Date']//following::input[1]").fill(datadictvalue["C_FROM_DATE"])
            page.locator("//label[text()='To Date']//following::input[1]").fill(datadictvalue["C_TO_DATE"])

    #Funds Capture

            if datadictvalue["C_CRDT_CARD"] == 'Yes':
                page.get_by_text("Credit card", exact=True).check()
            if datadictvalue["C_ELCTRNC_FNDS_TRNSFR"] == 'Yes':
                page.get_by_text("Electronic funds transfer", exact=True).check()
            if datadictvalue["C_DEBIT_CARD"] == 'Yes':
                page.get_by_text("Debit card").check()
            if datadictvalue["C_ELCTRNC_FUNDS_TRNSFR_AND_PSTV_PAY"] == 'Yes':
                page.get_by_text("Electronic funds transfer and").check()
            PrevName = datadictvalue["C_NAME"]

    #Formats
            j = 0
            while j < rowcount:

                datadictvalue = datadict[j]

                if PrevName == datadictvalue["C_NAME"]:
                    if datadictvalue["C_FRMT_NAME"] != "":
                        page.wait_for_timeout(2000)
                        page.get_by_role("button", name="Add Row").first.click()
                        page.locator("//h2[text()='Formats']//following::input[1]").click()
                        page.wait_for_timeout(1000)
                        page.get_by_title("Search: Name").first.click()

                        page.get_by_role("link", name="Search...").click()
                        page.get_by_label("Format").click()
                        page.get_by_label("Format").fill(datadictvalue["C_FRMT_NAME"])
                        page.get_by_role("button", name="Search", exact=True).click()
                        page.get_by_role("cell", name=datadictvalue['C_FRMT_NAME'], exact=True).first.click()
                        page.get_by_role("button", name="OK", exact=True).click()
                        page.wait_for_timeout(2000)

                j = j + 1

            k = 0
            while k < rowcount:

                datadictvalue = datadict[k]
                if PrevName == datadictvalue["C_NAME"]:
                    page.get_by_role("button", name="Add Row").nth(1).click()

                    page.wait_for_timeout(3000)
                    page.locator("//div[@title='Transmission Protocols']//following::select[1]").select_option(datadictvalue["C_TRNSMSSN_PRTCLS_NAME"])
                    page.wait_for_timeout(1000)

                k = k + 1
            page.get_by_role("button", name="Save and Close").click()


            try:
                expect(page.locator("//div[text()='Confirmation']//following::button[1]")).to_be_visible()
                page.locator("//div[text()='Confirmation']//following::button[1]").click()
                print("Row Saved Successfully")
                datadictvalue["RowStatus"] = "Configuration Saved Successfully"
            except Exception as e:
                print("Saved UnSuccessfully")
                datadictvalue["RowStatus"] = "Configuration Saved UnSuccessfully"


        i = i + 1



    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYMENT_SYSTEM):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYMENT_SYSTEM, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, PAYMENT_SYSTEM)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + PAYMENT_SYSTEM)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
                0] + "_" + PAYMENT_SYSTEM + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))