from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *


# The script is incomplete. Need Banks details (CM) to enable the GL fields.

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    # Sign In - Instance
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(15000)
    # Navigate to the Required Page
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Receipt Classes and Methods")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Receipt Classes and Methods").click()
    page.wait_for_timeout(3000)
    # page.pause()

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        if datadictvalue["C_NAME"] != PrevName:
            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Save and Close").click()
                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("Receipt Classes and Methods Saved")
                    datadict[i - 1]["RowStatus"] = "Receipt classes and methods Saved"
                except Exception as e:
                    print("Unable to save Receipt Classes and Methods")
                    datadict[i - 1]["RowStatus"] = "Unable to save Receipt classes and methods"

                page.wait_for_timeout(3000)

            # Create Receipt Classes & Methods

            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(5000)

            # Name
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])

            # Creation Method
            page.get_by_label("Creation Method").select_option(datadictvalue["C_CRTN_MTHD"])

            # Remittance Method
            page.get_by_label("Remittance Method").select_option(datadictvalue["C_RMTTNC_MTHD"])

            # Clearence Method
            page.get_by_label("Clearance Method").select_option(datadictvalue["C_CLRNC_MTHD"])

            # Require confirmation
            if datadictvalue["C_RQR_CNFRMTN"] == 'Yes':
                page.get_by_text("Require confirmation").click()

            # Context Value
            if datadictvalue["C_CNTXT_VALUE"]!='':
                page.get_by_label("Context Value").select_option(datadictvalue["C_CNTXT_VALUE"])

            # Regional Information
            # if datadictvalue["Regional Information"]!='':
            #     page.get_by_label("Regional Information").select_option(datadictvalue[""])

            # Click on Save button
            # page.get_by_role("button", name="Save", exact=True).click()
            page.wait_for_timeout(2000)

            PrevName = datadictvalue["C_NAME"]

        # Receipt Methods
        if datadictvalue["C_RCPT_NAME"] != '':
            page.get_by_role("button", name="Add Row").click()
            page.wait_for_timeout(3000)
            # page.locator("//a[@title='Expand']//following::td[1]").first.click()
            page.locator("//a[@title='Expand']//preceding::td[1]").first.click()
            page.wait_for_timeout(5000)
            # page.get_by_role("row", name="Expand Name").get_by_label("Name", exact=True).first.click()
            page.get_by_role("row", name="Expand Name").get_by_label("Name", exact=True).first.fill(datadictvalue["C_RCPT_NAME"])
            page.get_by_label("Printed Name").first.fill(datadictvalue["C_PRNTD_NAME"])
            page.locator("//a[@title='Select Date']//preceding::input[2]").first.fill(datadictvalue["C_EFFCTV_START_DATE"].strftime('%m/%d/%y'))
            if datadictvalue["C_EFFCTV_END_DATE"]!='':
                page.locator("//a[@title='Select Date']//preceding::input[2]").nth(1).fill(datadictvalue["C_EFFCTV_END_DATE"].strftime('%m/%d/%y'))
            # page.get_by_role("row", name="Expand Name Printed Name m/d/").locator("label").nth(4)

        # Remittance Bank Account
        if datadictvalue["C_BANK"] != '':
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(5000)
            if page.locator("//div[text()='Error']//following::button[text()='OK']").nth(0).is_visible():
                page.locator("//div[text()='Error']//following::button[text()='OK']").nth(0).click()
            if page.get_by_label("Business Unit").is_enabled():
                page.get_by_title("Search: Business Unit").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_role("textbox", name="Business Unit").click()
                page.get_by_role("textbox", name="Business Unit").fill(datadictvalue["C_BSNSS_UNIT"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BSNSS_UNIT"]).click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(5000)
                if page.locator("//div[text()='Warning']//following::button[text()='es']").nth(0).is_visible():
                    page.locator("//div[text()='Warning']//following::button[text()='es']").nth(0).click()
                    page.wait_for_timeout(2000)

            page.get_by_title("Search: Bank").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Bank Name").click()
            page.get_by_label("Bank Name").fill(datadictvalue["C_BANK"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_BANK"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            if datadictvalue["C_BRNCH"] != '':
                page.get_by_title("Search: Branch").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Branch Name").fill(datadictvalue["C_BRNCH"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.get_by_role("cell", name=datadictvalue["C_BRNCH"], exact=True).click()
                page.get_by_role("button", name="OK").click()
            page.get_by_title("Search: Account").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Bank Account Name").fill(datadictvalue["C_ACCNT"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_ACCNT"], exact=True).locator("span").click()
            page.get_by_role("button", name="OK").click()
            if datadictvalue["C_PRMRY"] == 'Yes':
                page.get_by_text("Primary", exact=True).check()
            if datadictvalue["C_PRMRY"] == 'No':
                page.get_by_text("Primary", exact=True).uncheck()
            if datadictvalue["C_OVRRD_BANK"] == 'Yes':
                page.get_by_text("Override bank").check()
            if datadictvalue["C_OVRRD_BANK"] == 'No':
                page.get_by_text("Override bank").uncheck()
            page.get_by_label("Minimum Receipt Amount").fill(datadictvalue["C_MNMM_RCPT_ACCNT"])
            page.get_by_label("Clearing Days").fill(datadictvalue["C_CLRNG_DAYS"])
            page.get_by_label("Risk Elimination Days").fill(datadictvalue["C_RISK_ELMNTN_DAYS"])
            if datadictvalue["C_RCPT_EFFCTV_START_DATE"]!='':
                page.locator("//label[text()='Effective Start Date']//following::input[1]").fill(datadictvalue["C_RCPT_EFFCTV_START_DATE"].strftime('%m/%d/%y'))
            if datadictvalue["C_RCPT_EFFCTV_END_DATE"]!='':
                page.locator("//label[text()='Effective End Date']//following::input[1]").fill(datadictvalue["C_RCPT_EFFCTV_END_DATE"].strftime('%m/%d/%y'))
            page.get_by_label("Context Value").select_option(datadictvalue["C_RCPT_CNTXT_VALUE"])
            if page.get_by_label("Cash").is_enabled():
                page.get_by_label("Cash").clear()
                page.get_by_label("Cash").fill(datadictvalue["C_CASH"])
            if page.get_by_label("Receipt Confirmation").is_enabled():
                page.get_by_label("Receipt Confirmation").clear()
                page.get_by_label("Receipt Confirmation").fill(datadictvalue["C_RCPT_CNFRMTN"])
            if page.get_by_label("Remittance").is_enabled():
                page.get_by_label("Remittance").clear()
                page.get_by_label("Remittance").fill(datadictvalue["C_RMTTNC"])
            if page.get_by_label("Factoring").is_enabled():
                page.get_by_label("Factoring").clear()
                page.get_by_label("Factoring").fill(datadictvalue["C_FCTRNG"])
            if page.get_by_label("Short Term Debt").is_enabled():
                page.get_by_label("Short Term Debt").clear()
                page.get_by_label("Short Term Debt").fill(datadictvalue["C_SHORT_TERM_DEBT"])
            if page.get_by_label("Unapplied Receipts").is_enabled():
                page.get_by_label("Unapplied Receipts").clear()
                page.get_by_label("Unapplied Receipts").fill(datadictvalue["C_UNPPLD_RCPT"])
            if page.get_by_label("Unidentified Receipts").is_enabled():
                page.get_by_label("Unidentified Receipts").clear()
                page.get_by_label("Unidentified Receipts").fill(datadictvalue["C_UNDNTFD_RCPT"])
            if page.get_by_label("On-Account Receipts").is_enabled():
                page.get_by_label("On-Account Receipts").clear()
                page.get_by_label("On-Account Receipts").fill(datadictvalue["C_ON_ACCNT_RCPT"])
            page.get_by_label("Unearned Discounts").select_option(datadictvalue["C_UNRND_DSCNT"])
            page.get_by_label("Earned Discounts", exact=True).select_option(datadictvalue["C_ERND_DSCNT"])
            # page.get_by_label("Claim Investigation").select_option("0")
            page.get_by_role("button", name="Save and Close").click()

        # page.get_by_role("button", name="Cancel").click()

        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1
        page.wait_for_timeout(3000)

    if i == rowcount:

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
    # page.get_by_role("button", name="Done").click()

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Receipt Classes and Methods Saved Successfully")

    except Exception as e:
        print("Receipt Classes and Methods not Saved")


    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, RECEIPT_CLASSES_AND_METHODS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, RECEIPT_CLASSES_AND_METHODS, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, RECEIPT_CLASSES_AND_METHODS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + RECEIPT_CLASSES_AND_METHODS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + RECEIPT_CLASSES_AND_METHODS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))