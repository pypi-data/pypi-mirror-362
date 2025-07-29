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
    page.wait_for_timeout(5000)

    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Payment Method Defaulting Rules")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Payment Method Defaulting Rules").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("cell", name=datadictvalue["C_NAME"], exact=True).first.click()
        page.get_by_role("link", name="Edit").first.click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Payment Method").fill(datadictvalue["C_PYMNT_MTHD"])
        #Business Units

        if datadictvalue["C_ALL_BU"] == 'Yes':
            page.get_by_text("All", exact=True).first.click()
        if datadictvalue["C_SPCFC_BU"]  == 'Yes':
            page.get_by_text("Specific").first.click()
            #Add the field for BU if required
            page.get_by_role("button", name="Add Row").click()
            page.get_by_label(datadictvalue["Business Unit"]).click()

        # First Party Legal Entities

        if datadictvalue["C_ALL_FP"] == 'Yes':
            page.get_by_text("All", exact=True).nth(1).click()
        if datadictvalue["C_SPCFC_FP"] == 'Yes':
            page.get_by_text("Specific").nth(1).click()
            # Add the field for First Party Legal Entities if required
            page.get_by_role("button", name="Add Row").click()
            page.get_by_label("First Party Legal Entity").fill(datadictvalue["First Party Legal Entities"])


        # Payment Process Transaction Types

        if datadictvalue["C_ALL_PP"] == 'Yes':
            page.get_by_text("All", exact=True).nth(1).click()
        if datadictvalue["C_SPCFC_PP"] == 'Yes':
            page.get_by_text("Specific").nth(1).click()
            # Add the field for Payment Process Transaction Types if required
            page.get_by_role("button", name="Add Row").click()
            page.get_by_label("Type").fill(datadictvalue["Payment Process Transaction"])
        page.get_by_label("Currency").click()
        page.get_by_label("Currency").select_option(datadictvalue["C_CRRNCY"])
        page.get_by_label("Payee Location").click()
        page.get_by_label("Payee Location").select_option(datadictvalue["C_PY_LCTN"])

        page.get_by_role("button", name="Save and Close").click()
       #Validation

        try:
            expect(page.get_by_text("Confirmation")).to_be_visible()
            page.get_by_role("button", name="OK").click()
            print("Payment Method Default Rule Saved Successfully")
        except Exception as e:
            print("Payment Method Default Rule not Saved")


        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here *****
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, EXP_PAYMENT_METHOD_DEFAULTING_RULE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, EXP_PAYMENT_METHOD_DEFAULTING_RULE, PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, EXP_PAYMENT_METHOD_DEFAULTING_RULE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[0] + "_" + EXP_PAYMENT_METHOD_DEFAULTING_RULE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + EXP_PAYMENT_METHOD_DEFAULTING_RULE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))