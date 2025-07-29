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
    page.wait_for_timeout(20000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Document Types")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Document Types", exact=True).first.click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Document Types").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)
        page.get_by_label("Add", exact=True).click()
        page.wait_for_timeout(8000)
        page.get_by_label("Type", exact=True).click()
        page.get_by_label("Type", exact=True).type(datadictvalue["C_DCMNT_TYPE"])
        page.locator("//span[text()='Status']//following::a[1]").click()
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

        page.get_by_role("combobox", name="Category", exact=True).click()
        page.get_by_role("combobox", name="Category", exact=True).fill(datadictvalue["C_CTGRY"])
        page.wait_for_timeout(5000)
        page.get_by_text(datadictvalue["C_CTGRY"]).click()
        page.get_by_role("combobox", name="Country").click()
        page.get_by_role("combobox", name="Country").clear()
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Country").fill(datadictvalue["C_CNTRY"])
        page.get_by_text(datadictvalue["C_CNTRY"],exact=True).first.click()
        page.get_by_label("Minimum Attachments").clear()
        page.get_by_label("Minimum Attachments").type(str(datadictvalue["C_MNMM_ATTCHMNTS"]))

        if datadictvalue["C_APPRVL_RQRD"] == "Yes":
            page.locator("//span[text()='Approval Required']//following::oj-option[text()='Yes']").first.click()
        if datadictvalue["C_APPRVL_RQRD"] == "No" or '':
            page.locator("//span[text()='Approval Required']//following::oj-option[text()='No']").first.click()
        if datadictvalue["C_ALLOW_MLTPL_OCCRNCS"] == "Yes":
            page.locator("//span[text()='Allow multiple occurrences']//following::oj-option[text()='Yes']").first.click()
        if datadictvalue["C_ALLOW_MLTPL_OCCRNCS"] == "No" or '':
            page.locator("//span[text()='Allow multiple occurrences']//following::oj-option[text()='No']").first.click()
        if datadictvalue["C_PBLSH_RQRD"] == "Yes":
            page.locator("//span[text()='Publish Required']//following::oj-option[text()='Yes']").first.click()
        if datadictvalue["C_PBLSH_RQRD"] == "No" or '':
            page.locator("//span[text()='Publish Required']//following::oj-option[text()='No']").first.click()

        # Selecting Attributes
        if datadictvalue["C_DCMNT_NAME_APPLCBL"] == "Relevant":
            page.locator("//td[text()='Document Name']//following::input[1]").check()
            page.locator("//td[text()='Document Name']//following::input[2]").uncheck()
        if datadictvalue["C_DCMNT_NAME_APPLCBL"] == "Relevant - Required":
            page.locator("//td[text()='Document Name']//following::input[1]").check()
            page.locator("//td[text()='Document Name']//following::input[2]").check()
        if datadictvalue["C_DCMNT_NAME_APPLCBL"] == '':
            page.locator("//td[text()='Document Name']//following::input[1]").uncheck()
            page.locator("//td[text()='Document Name']//following::input[2]").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_DCMNT_NMBR_APPLCBL"] == "Relevant":
            page.locator("//td[text()='Document Number']//following::input[1]").check()
            page.locator("//td[text()='Document Number']//following::input[2]").uncheck()
        if datadictvalue["C_DCMNT_NMBR_APPLCBL"] == "Relevant - Required":
            page.locator("//td[text()='Document Number']//following::input[1]").check()
            page.locator("//td[text()='Document Number']//following::input[2]").check()
        if datadictvalue["C_DCMNT_NMBR_APPLCBL"] == '':
            page.locator("//td[text()='Document Number']//following::input[1]").uncheck()
            page.locator("//td[text()='Document Number']//following::input[2]").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_FROM_DATE_APPLCBL"] == "Relevant":
            page.locator("//td[text()='From Date']//following::input[1]").check()
            page.locator("//td[text()='From Date']//following::input[2]").uncheck()
        if datadictvalue["C_FROM_DATE_APPLCBL"] == "Relevant - Required":
            page.locator("//td[text()='From Date']//following::input[1]").check()
            page.locator("//td[text()='From Date']//following::input[2]").check()
        if datadictvalue["C_FROM_DATE_APPLCBL"] == '':
            page.locator("//td[text()='From Date']//following::input[1]").uncheck()
            page.locator("//td[text()='From Date']//following::input[2]").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_TO_DATE_APPLCBL"] == "Relevant":
            page.locator("//td[text()='To Date']//following::input[1]").check()
            page.locator("//td[text()='To Date']//following::input[2]").uncheck()
        if datadictvalue["C_TO_DATE_APPLCBL"] == "Relevant - Required":
            page.locator("//td[text()='To Date']//following::input[1]").check()
            page.locator("//td[text()='To Date']//following::input[2]").check()
        if datadictvalue["C_TO_DATE_APPLCBL"] == '':
            page.locator("//td[text()='To Date']//following::input[1]").uncheck()
            page.locator("//td[text()='To Date']//following::input[2]").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_ISSNG_CNTRY_APPLCBL"] == "Relevant":
            page.locator("//td[text()='Issuing Country']//following::input[1]").check()
            page.locator("//td[text()='Issuing Country']//following::input[2]").uncheck()
        if datadictvalue["C_ISSNG_CNTRY_APPLCBL"] == "Relevant - Required":
            page.locator("//td[text()='Issuing Country']//following::input[1]").check()
            page.locator("//td[text()='Issuing Country']//following::input[2]").check()
        if datadictvalue["C_ISSNG_CNTRY_APPLCBL"] == '':
            page.locator("//td[text()='Issuing Country']//following::input[1]").uncheck()
            page.locator("//td[text()='Issuing Country']//following::input[2]").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_ISSNG_LCTN_APPLCBL"] == "Relevant":
            page.locator("//td[text()='Issuing Location']//following::input[1]").check()
            page.locator("//td[text()='Issuing Location']//following::input[2]").uncheck()
        if datadictvalue["C_ISSNG_LCTN_APPLCBL"] == "Relevant - Required":
            page.locator("//td[text()='Issuing Location']//following::input[1]").check()
            page.locator("//td[text()='Issuing Location']//following::input[2]").check()
        if datadictvalue["C_ISSNG_LCTN_APPLCBL"] == '':
            page.locator("//td[text()='Issuing Location']//following::input[1]").uncheck()
            page.locator("//td[text()='Issuing Location']//following::input[2]").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_ISSNG_ATHRTY_APPLCBL"] == "Relevant":
            page.locator("//td[text()='Issuing Authority']//following::input[1]").check()
            page.locator("//td[text()='Issuing Authority']//following::input[2]").uncheck()
        if datadictvalue["C_ISSNG_ATHRTY_APPLCBL"] == "Relevant - Required":
            page.locator("//td[text()='Issuing Authority']//following::input[1]").check()
            page.locator("//td[text()='Issuing Authority']//following::input[2]").check()
        if datadictvalue["C_ISSNG_ATHRTY_APPLCBL"] == '':
            page.locator("//td[text()='Issuing Authority']//following::input[1]").uncheck()
            page.locator("//td[text()='Issuing Authority']//following::input[2]").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_ISSD_ON_APPLCBL"] == "Relevant":
            page.locator("//td[text()='Issued On']//following::input[1]").check()
            page.locator("//td[text()='Issued On']//following::input[2]").uncheck()
        if datadictvalue["C_ISSD_ON_APPLCBL"] == "Relevant - Required":
            page.locator("//td[text()='Issued On']//following::input[1]").check()
            page.locator("//td[text()='Issued On']//following::input[2]").check()
        if datadictvalue["C_ISSD_ON_APPLCBL"] == '':
            page.locator("//td[text()='Issued On']//following::input[1]").uncheck()
            page.locator("//td[text()='Issued On']//following::input[2]").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_ISSNG_CMMNTS_APPLCBL"] == "Relevant":
            page.locator("//td[text()='Issuing Comments']//following::input[1]").check()
            page.locator("//td[text()='Issuing Comments']//following::input[2]").uncheck()
        if datadictvalue["C_ISSNG_CMMNTS_APPLCBL"] == "Relevant - Required":
            page.locator("//td[text()='Issuing Comments']//following::input[1]").check()
            page.locator("//td[text()='Issuing Comments']//following::input[2]").check()
        if datadictvalue["C_ISSNG_CMMNTS_APPLCBL"] == '':
            page.locator("//td[text()='Issuing Comments']//following::input[1]").uncheck()
            page.locator("//td[text()='Issuing Comments']//following::input[2]").uncheck()
        page.wait_for_timeout(2000)

        # Selecting Document Record Preferences- Restrict Settings
        if page.locator("//span[text()='Restrict Create']//following::oj-option[text()='Yes']").first.is_enabled():
            if datadictvalue["C_RSTRCT_CRT"] == "Yes":
                page.locator("//span[text()='Restrict Create']//following::oj-option[text()='Yes']").first.click()
        if page.locator("//span[text()='Restrict Create']//following::oj-option[text()='Yes']").first.is_enabled():
            if datadictvalue["C_RSTRCT_CRT"] == "No" or '':
                page.locator("//span[text()='Restrict Create']//following::oj-option[text()='No']").first.click()
        if page.locator("//span[text()='Restrict Update']//following::oj-option[text()='Yes']").first.is_enabled():
            if datadictvalue["C_RSTRCT_UPDT"] == "Yes":
                page.locator("//span[text()='Restrict Update']//following::oj-option[text()='Yes']").first.click()
        if page.locator("//span[text()='Restrict Update']//following::oj-option[text()='Yes']").first.is_enabled():
            if datadictvalue["C_RSTRCT_UPDT"] == "No" or '':
                page.locator("//span[text()='Restrict Update']//following::oj-option[text()='No']").first.click()
        if page.locator("//span[text()='Restrict Delete']//following::oj-option[text()='Yes']").first.is_enabled():
            if datadictvalue["C_RSTRCT_DLT"] == "Yes":
                page.locator("//span[text()='Restrict Delete']//following::oj-option[text()='Yes']").first.click()
        if page.locator("//span[text()='Restrict Delete']//following::oj-option[text()='Yes']").first.is_enabled():
            if datadictvalue["C_RSTRCT_DLT"] == "No" or '':
                page.locator("//span[text()='Restrict Delete']//following::oj-option[text()='No']").first.click()

        # Saving the Record
        page.get_by_label("Create").click()
        page.wait_for_timeout(3000)
        try:
            expect(page.get_by_role("heading", name="Document Types")).to_be_visible()
            print("Manage Document Type Saved Successfully")
            datadictvalue["RowStatus"] = "Manage Document Type Saved"
        except Exception as e:
            print("Unable to save Manage Document Type")
            datadictvalue["RowStatus"] = "Unable to save Manage Document Type"

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Manage Document Type Added Successfully"
        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_DOCUMENT_TYPE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_DOCUMENT_TYPE, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_DOCUMENT_TYPE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0]+ "_" + MANAGE_DOCUMENT_TYPE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + MANAGE_DOCUMENT_TYPE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
