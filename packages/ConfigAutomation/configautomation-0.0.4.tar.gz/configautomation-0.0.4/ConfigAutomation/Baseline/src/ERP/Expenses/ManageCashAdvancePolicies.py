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
    page.get_by_role("textbox").fill("Manage Cash Advance And Authorization Policies")
    page.get_by_role("button", name="Search").click()
    page.get_by_role("link", name="Manage Cash Advance And Authorization Policies").click()
    # page.pause()
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create").click()
        page.get_by_label("Business Unit", exact=True).fill(datadictvalue["C_BSNSS_UNIT"])
        # page.get_by_role("option", name=datadictvalue["C_BSNSS_UNIT"]).click()
        page.get_by_label("Enable Advances", exact=True).click()
        page.get_by_label("Enable Advances", exact=True).select_option(datadictvalue["C_ENBL_ADVNCS"])
        page.wait_for_timeout(2000)
        if datadictvalue["C_ENBL_ADVNCS"] == 'Yes':
            page.get_by_label("Methods of Applying Advances").nth(1).click()
            page.get_by_label("Methods of Applying Advances").nth(1).select_option(datadictvalue["C_MTHDS_OF_APPLYNG_ADVNCS"])
            if datadictvalue["C_NMBR_OF_UNPPLD_ADVNCS"] == 'Use setup from all business units' :
                page.locator("//div[text()='Create Business Unit-Specific Cash Advance Policies']//following::label[text()='Number of Unapplied Advances']//following::input[1]").nth(0).click()
            elif datadictvalue["C_NMBR_OF_UNPPLD_ADVNCS"] == '':
                page.get_by_text("Define value specific to").first.click()
                page.get_by_label("*").fill(datadictvalue["C_NMBR_OF_UNPPLD_ADVNCS"])

            #Maximum Amount Allowed Per Cash Advance
            # if datadictvalue[""] == '':
            #     page.locator("//div[text()='Create Business Unit-Specific Cash Advance Policies']//following::label[text()='Maximum Amount Allowed per Cash Advance']//following::input[1]").nth(0).click()
            # elif datadictvalue[""] == '':
            #     page.locator("//div[text()='Create Business Unit-Specific Cash Advance Policies']//following::label[text()='Maximum Amount Allowed per Cash Advance']//following::input[2]").nth(0).click()
            #     page.locator("//div[text()='Create Business Unit-Specific Cash Advance Policies']//following::label[text()='Maximum Amount Allowed per Cash Advance']//following::input[3]").nth(0).fill(datadictvalue[""])

            #Prefix
            if datadictvalue["C_PRFX"] == 'Use setup from all business units':
                page.locator("//div[text()='Create Business Unit-Specific Cash Advance Policies']//following::label[text()='Prefix']//following::input[1]").nth(0).click()
            elif datadictvalue["C_PRFX"] != '':
                page.get_by_text("Define value specific to").nth(2).click()
                # page.locator["//label[text()='Define value specific to business unit']//following::input[contains(@id,'content')]"].fill(str(datadictvalue["C_PRFX"]))
            page.locator("//label[text()='Cash Advance Clearing Account']//following::input[1]").fill(datadictvalue["C_CASH_ADVNC_CLRNNG_ACCNT"])

        # Payment Group for Cash Advances

        # page.locator("(//label[text()='Payment Group for Cash Advances'])[2]//following::input[2]").fill(datadictvalue[""])

        # page.locator("[id=\"__af_Z_window\"]").get_by_title("ValueMeaning").click()
        # page.get_by_role("link", name="Search...").click()
        # page.get_by_label("Meaning").fill(datadictvalue[""])
        # page.get_by_role("button", name="Search", exact=True).click()
        # page.get_by_text(datadictvalue[""]).click()
        # page.get_by_role("button", name="OK").click()

        #Authorizations

        page.get_by_role("link", name="Authorizations").click()
        page.get_by_label("Enable Authorizations").nth(1).select_option(datadictvalue["C_ENBL_ATHRZTNS"])
        if datadictvalue["C_ENBL_ATHRZTNS"] == 'Yes':
            page.get_by_label("Attach Authorization").nth(1).click()
            page.get_by_label("Attach Authorization").nth(1).select_option(datadictvalue["C_ATTCH_ATHRZTN"])
            page.get_by_label("Behavior").nth(1).click()
            page.get_by_label("Behavior").nth(1).select_option(datadictvalue["C_BHVR"])
            page.wait_for_timeout(2000)

            if datadictvalue["C_ATHRZTNS_PRFX"] == 'Use setup from all business units':
                page.get_by_text("Use setup from all business").nth(3).click()
            elif datadictvalue["C_ATHRZTNS_PRFX"] == 'Define value specific to business unit':
                page.get_by_text("Define value specific to").first.click()

            if datadictvalue["C_VSBLTY_IN_DAYS"] == 'Use setup from all business units':
                page.locator("//div[text()='Create Business Unit-Specific Cash Advance Policies']//following::label[text()='Visibility in Days']//following::input[1]").nth(0).click()
            elif datadictvalue["C_VSBLTY_IN_DAYS"] != '':
                page.locator("//div[text()='Create Business Unit-Specific Cash Advance Policies']//following::label[text()='Visibility in Days']//following::input[2]").nth(0).click()
                page.locator("//div[text()='Create Business Unit-Specific Cash Advance Policies']//following::label[text()='Visibility in Days']//following::input[3]").nth(0).fill(datadictvalue["C_VSBLTY_IN_DAYS"])

        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Cancel").click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Save and Close").click()
        # page.pause()
        page.wait_for_timeout(2000)
        # page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Save and Close").click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

    # page.get_by_role("button", name="Save and Close").click()
    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Cash Advance Policies Saved Successfully")
    except Exception as e:
        print("Cash Advance Policies not saved")

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, CASH_ADVN_POLICY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, CASH_ADVN_POLICY, PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, CASH_ADVN_POLICY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[0] + "_" + CASH_ADVN_POLICY)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + CASH_ADVN_POLICY + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))