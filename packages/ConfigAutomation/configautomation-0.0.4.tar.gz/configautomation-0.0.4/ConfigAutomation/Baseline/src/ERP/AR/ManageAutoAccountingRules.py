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
    page.get_by_role("textbox").fill("Manage AutoAccounting Rules")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage AutoAccounting Rules", exact=True).click()

    AccType = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)

        if datadictvalue["C_ACCNT_TYPE"] != AccType:
            if i > 0:
                page.get_by_role("button", name="Done").click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Save", exact=True).click()
                page.wait_for_timeout(2000)

            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)

            #Select Business Unit
            if page.locator("//input[contains(@id,'businessUnitId')]").is_enabled():
                page.locator("[id=\"__af_Z_window\"]").get_by_title("Search: Business Unit").click()
                page.get_by_role("link", name="Search...").click()
                page.wait_for_timeout(2000)
                page.get_by_role("textbox", name="Business Unit").fill(datadictvalue["C_BSNSS_UNIT"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.locator("//div[text()='Search and Select: Business Unit']//following::span[text()='"+datadictvalue["C_BSNSS_UNIT"]+"']").click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)

            page.get_by_label("Account Type").click()
            page.get_by_label("Account Type").select_option(datadictvalue["C_ACCNT_TYPE"])
            page.get_by_text("Create AutoAccounting Rule").click()
            page.wait_for_timeout(2000)
            AccType = datadictvalue["C_ACCNT_TYPE"]
            print(("Prev:", AccType))
            # page.pause()

        base=page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name=datadictvalue["C_SGMNT"], exact=True)
        base1=page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name=datadictvalue["C_SGMNT"], exact=True).text_content()
        print(base1)
        page.wait_for_timeout(2000)
        expect(base).to_be_visible()
        base.scroll_into_view_if_needed()
        page.wait_for_timeout(3000)
        page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name=datadictvalue["C_SGMNT"], exact=True).click()

        if datadictvalue["C_SGMNT_VALUE_SRC"] != '':
            page.locator("//div[text()='Create AutoAccounting Rule']//following::span[text()='"+datadictvalue["C_SGMNT"]+"']//following::select[1]").click(delay=100)
            page.locator("//div[text()='Create AutoAccounting Rule']//following::span[text()='"+datadictvalue["C_SGMNT"]+"']//following::select[1]").select_option(datadictvalue["C_SGMNT_VALUE_SRC"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_SGMNT_CNSTNT_VALUE"] != '':
            page.locator("//div[text()='Create AutoAccounting Rule']//following::span[text()='"+datadictvalue["C_SGMNT"]+"']//following::a[@title='Search']").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Constant Value").click()
            page.get_by_label("Constant Value").fill(str(datadictvalue["C_SGMNT_CNSTNT_VALUE"]))
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=str(datadictvalue["C_SGMNT_CNSTNT_VALUE"]), exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(1000)

        AccType = datadictvalue["C_ACCNT_TYPE"]


        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Save the data

        if i == rowcount:
            page.get_by_role("button", name="Done").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(5000)
            # if page.locator("//div[text()='Warning']//following::button[1]").is_visible():
            #     page.locator("//div[text()='Warning']//following::button[1]").click()
            # if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
            #     page.locator("//div[text()='Confirmation']//following::button[1]").click()

            try:
                expect(page.get_by_role("button", name="Done")).to_be_visible()
                print("AutoAccounting Rules saved Successfully")
                datadictvalue["RowStatus"] = "AutoAccounting Rules added successfully"

            except Exception as e:
                print("AutoAccounting Rules not saved")
                datadictvalue["RowStatus"] = "AutoAccounting Rules not added"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, AUTO_ACC_RULE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, AUTO_ACC_RULE, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, AUTO_ACC_RULE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + AUTO_ACC_RULE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + AUTO_ACC_RULE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

