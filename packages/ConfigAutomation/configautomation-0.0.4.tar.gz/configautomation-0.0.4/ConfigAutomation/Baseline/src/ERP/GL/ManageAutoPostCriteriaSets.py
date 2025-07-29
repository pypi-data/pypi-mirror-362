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
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.get_by_label("", exact=True).fill("Manage AutoPost Criteria Sets")
    page.get_by_role("button", name="Search").click()
    # page.pause()
    page.get_by_role("link", name="Manage AutoPost Criteria Sets").click()

    PrevName=''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        if datadictvalue["C_NAME"] != PrevName:
            # Save the prev type data if the row contains a new type
            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Save and Close").click()
                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("AutoPost Criteria Sets Saved")
                    datadictvalue["RowStatus"] = "AutoPost Criteria Sets Saved"
                except Exception as e:
                    print("Unable to save AutoPost Criteria Sets")
                    datadictvalue["RowStatus"] = "Unable to save AutoPost Criteria Sets"

                page.wait_for_timeout(3000)

            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)

            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])

            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

            if datadictvalue["C_ENBLD"] == 'Yes':
                page.wait_for_timeout(2000)
                if not page.get_by_text("Enabled").is_checked():
                    page.get_by_text("Enabled").click()
            #
            elif datadictvalue["C_ENBLD"] == 'No':
                if page.get_by_text("Enabled").is_checked():
                    page.get_by_text("Enabled").click()

            if datadictvalue["C_USE_BTCH_CRTR_AS_APPRVL_SBMTTR"] == 'Yes':
                page.wait_for_timeout(2000)
                if not page.get_by_text("Use Batch Creator as Approval").is_checked():
                    page.get_by_text("Use Batch Creator as Approval").click()
            #
            elif datadictvalue["C_USE_BTCH_CRTR_AS_APPRVL_SBMTTR"] == 'No':
                if page.get_by_text("Use Batch Creator as Approval").is_checked():
                    page.get_by_text("Use Batch Creator as Approval").click()

            PrevName = datadictvalue["C_NAME"]

        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Add Row").dblclick()
        page.wait_for_timeout(2000)
        page.get_by_label("Priority").click()
        page.get_by_label("Priority").fill(str(datadictvalue["C_PRRTY"]))
        page.get_by_label("Ledger or Ledger Set", exact=True).fill(datadictvalue["C_LDGR_OR_LDGR_SET"])
        page.wait_for_timeout(2000)
        page.get_by_title("Search: Source").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Source").fill(datadictvalue["C_SRC"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("//div[text()='Search and Select: Source']//following::span[text()='"+datadictvalue["C_SRC"]+"'][1]").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Category").click()
        page.get_by_label("Category").type(datadictvalue["C_CTGRY"])
        page.locator("[id=\"__af_Z_window\"]").get_by_role("option", name=datadictvalue["C_CTGRY"], exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_label("Accounting Period").click()
        page.get_by_label("Accounting Period").type(datadictvalue["C_ACCNTNG_PRD"])
        page.locator("[id=\"__af_Z_window\"]").get_by_role("option", name=datadictvalue["C_ACCNTNG_PRD"]).click()
        if page.get_by_label("Balance Type").is_visible():
            if datadictvalue["C_BLNC_TYPE"] !='':
                page.get_by_label("Balance Type").click()
                page.get_by_label("Balance Type").select_option(datadictvalue["C_BLNC_TYPE"])

        if datadictvalue["C_PRCSS_ALL_CRTR"] == 'Yes':
            # if not page.get_by_text("Yes").is_checked():
                page.get_by_text("Yes").click()

        if datadictvalue["C_PRCSS_ALL_CRTR"] == 'No':
            # if page.get_by_text("No").is_checked():
                page.get_by_text("No").click()
        page.get_by_label("Number of Days Before").type(str(datadictvalue["C_NMBR_OF_DAYS_BFR_SBMSSN_DATE"]))
        page.get_by_label("Number of Days After").type(str(datadictvalue["C_NMBR_OF_DAYS_AFTER_SBMSSN_DATE"]))
        page.wait_for_timeout(3000)
        # page.get_by_role("button", name="Cancel")

        print("Row Added - ", str(i))
        i = i + 1

        if i==rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)

            try:
                expect(page.get_by_role("button", name="Done")).to_be_visible()
                print("AutoPost Criteria Sets Saved")
                datadictvalue["RowStatus"] = "AutoPost Criteria Sets Saved"
            except Exception as e:
                print("Unable to save AutoPost Criteria Sets")
                datadictvalue["RowStatus"] = "Unable to save AutoPost Criteria Sets"


    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, MANAGE_AUTO_POST_SETS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, MANAGE_AUTO_POST_SETS, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, MANAGE_AUTO_POST_SETS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + LEGAL_ENTITY_SHEET)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
                0] + "_" + LEGAL_ENTITY_SHEET + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))