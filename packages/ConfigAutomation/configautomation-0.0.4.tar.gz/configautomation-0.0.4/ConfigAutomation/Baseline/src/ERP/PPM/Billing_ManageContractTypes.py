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
    page.get_by_role("textbox").fill("Manage Contract Types")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Contract Types", exact=True).click()

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        if datadictvalue["C_NAME"] != PrevName:
            # Save the prev type data if the row contains a new type
            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Cancel").click()
                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("Contract Types Saved")
                    datadict[i - 1]["RowStatus"] = "Contract Types Saved"
                except Exception as e:
                    print("Unable to save Contract Types")
                    datadict[i - 1]["RowStatus"] = "Unable to save Contract Types"

                page.wait_for_timeout(3000)

            #Create Contract Type
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Class", exact=True).select_option(datadictvalue["C_CLASS"])
            # page.get_by_label("Set", exact=True).select_option(datadictvalue["C_SET"])
            page.get_by_label("Set", exact=True).fill(datadictvalue["C_SET"])
            page.get_by_label("Set", exact=True).press("Tab")
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            if datadictvalue["C_ALLOW_LINES"] == 'Yes':
                page.get_by_text("Allow lines").check()
            if datadictvalue["C_ALLOW_LINES"] == 'No':
                page.get_by_text("Allow lines").uncheck()
            # page.get_by_role("row", name="*Start Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").clear()
            # page.get_by_role("row", name="*Start Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_START_DATE"].strftime("%m/%d/%Y"))
            page.locator("//label[text()='Start Date']//following::input[1]").fill(datadictvalue["C_START_DATE"].strftime("%m/%d/%Y"))
            if datadictvalue["C_END_DATE"] != '':
                page.locator("//label[text()='End Date']//following::input[1]").fill(datadictvalue["C_END_DATE"].strftime("%m/%d/%Y"))
            page.get_by_role("button", name="Continue").click()
            page.wait_for_timeout(3000)
            PrevName = datadictvalue["C_NAME"]

            #Enter Overview details
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.get_by_label("Code").fill(datadictvalue["C_CODE"])
            if datadictvalue["C_ENBL_ATMTC_LINE_NMBRNG"] == 'Yes':
                page.get_by_text("Enable automatic line numbering").check()
            if datadictvalue["C_ENBL_ATMTC_LINE_NMBRNG"] == 'No':
                page.get_by_text("Enable automatic line numbering").uncheck()
            if datadictvalue["C_RQRS_SGNTR"] == 'Yes':
                page.get_by_text("Requires signature").check()
            if datadictvalue["C_RQRS_SGNTR"] == 'No':
                page.get_by_text("Requires signature").uncheck()
            page.get_by_label("Buyer Role").select_option(datadictvalue["C_BUYER_ROLE"])
            page.get_by_label("Seller Role").click()
            page.get_by_label("Seller Role").select_option(datadictvalue["C_SELLER_ROLE"])
            page.wait_for_timeout(2000)
            page.get_by_label("Contract Owner Role").select_option(datadictvalue["C_CNTRCT_OWNER_ROLE"])
            page.wait_for_timeout(1000)
            page.get_by_label("Contract Layout Template").select_option(datadictvalue["C_CNTRCT_LYT_TMPLT"])
            page.wait_for_timeout(1000)
            page.get_by_label("Terms Layout Template").select_option(datadictvalue["C_TERMS_LYT_TMPLT"])
            if datadictvalue["C_NTFY_BFR_EXPRTN"] == 'Yes':
                page.get_by_text("Notify before expiration").check()
                page.wait_for_timeout(1000)
                page.get_by_label("Days to Expiration").fill(str(datadictvalue["C_DAYS_TO_EXPRTN"]))
                page.get_by_label("Contact role to be notified").select_option(
                    datadictvalue["C_CNTCT_ROLE_TO_BE_NTFD"])
            if datadictvalue["C_NTFY_BFR_EXPRTN"] == 'No':
                page.get_by_text("Notify before expiration").uncheck()

            page.get_by_label("Contract Numbering Method").select_option(datadictvalue["C_CNTRCT_NMBRNG_MTHD"])
            if datadictvalue["C_CNTRCT_NMBRNG_MTHD"] == 'Automatic':
                page.get_by_label("Contract Numbering Level").select_option(datadictvalue["C_CNTRCT_NMBRNG_LEVEL"])
                page.get_by_label("Contract Sequence Category").select_option(datadictvalue["C_CNTRCT_SQNC_CTGRY"])

        page.wait_for_timeout(2000)

        #Add Line Types
        if datadictvalue["C_LINE_TYPES_NAME"] != '':
            page.get_by_role("link", name="Line Types").click()
            page.get_by_role("button", name="Add").click()
            page.get_by_role("table", name="Line Types").get_by_label("Name").click()
            page.get_by_role("table", name="Line Types").get_by_label("Name").select_option(datadictvalue["C_LINE_TYPES_NAME"])
            page.wait_for_timeout(2000)

        #Add Additional Party Roles
        page.get_by_role("link", name="Additional Party Roles").click()
        page.wait_for_timeout(4000)
        page.get_by_role("button", name="Add").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Role", exact=True).click()
        page.get_by_label("Role", exact=True).select_option(datadictvalue["C_ROLE"])
        page.wait_for_timeout(1000)

        # Add Project Billing Options

        page.get_by_role("link", name="Project Billing Options").click()
        if datadictvalue["C_INTRCMPNY"] == 'Yes':
            page.get_by_text("Intercompany", exact=True).check()
        if datadictvalue["C_INTRCMPNY"] == 'No':
            page.get_by_text("Intercompany", exact=True).uncheck()
        if datadictvalue["C_INTRPRJCT"] == 'Yes':
            page.get_by_text("Interproject", exact=True).check()
        if datadictvalue["C_INTRPRJCT"] == 'No':
            page.get_by_text("Interproject", exact=True).uncheck()
        if datadictvalue["C_ENBL_BLLNG_CNTRLS"] == 'Yes':
            page.get_by_text("Enable billing controls").check()
            page.wait_for_timeout(1000)
            page.get_by_label("Billing Limit Type").select_option(datadictvalue["C_BLLNG_LIMIT_TYPE"])
        if datadictvalue["C_ENBL_BLLNG_CNTRLS"] == 'No':
            page.get_by_text("Enable billing controls").uncheck()
        page.wait_for_timeout(1000)

        # Add Advanced Authoring Options
        page.get_by_role("link", name="Advanced Authoring Options").click()
        if datadictvalue["C_ENBL_TERMS_ATHRNG"] == 'Yes':
            page.get_by_text("Enable terms authoring").check()
        if datadictvalue["C_ENBL_TERMS_ATHRNG"] == 'No':
            page.get_by_text("Enable terms authoring").uncheck()
        if datadictvalue["C_ENBL_RISK_MNGMNT"] == 'Yes':
            page.get_by_text("Enable risk management").check()
        if datadictvalue["C_ENBL_RISK_MNGMNT"] == 'No':
            page.get_by_text("Enable risk management").uncheck()
        if datadictvalue["C_ENBL_RLTD_CNTRCTS"] == 'Yes':
            page.get_by_text("Enable related contracts").check()
        if datadictvalue["C_ENBL_RLTD_CNTRCTS"] == 'No':
            page.get_by_text("Enable related contracts").uncheck()
        if page.get_by_text("Allow amendment without versioning").is_enabled():
            if datadictvalue["C_ALLOW_AMNDMNT_WTHT_VRSNNG"] == 'Yes':
                page.get_by_text("Allow amendment without versioning").check()
            if datadictvalue["C_ALLOW_AMNDMNT_WTHT_VRSNNG"] == 'No':
                page.get_by_text("Allow amendment without versioning").uncheck()

        # Add E-Signature
        if datadictvalue["C_RQRS_SGNTR"] == 'Yes':
            page.get_by_role("link", name="E-Signature").click()
            if datadictvalue["C_ENBL_ELCTRNC_SGNTR"] == 'Yes':
                page.get_by_text("Enable electronic signature").check()
                page.wait_for_timeout(1000)
                page.get_by_label("Solution Provider").select_option(datadictvalue["C_SLTN_PRVDR"])
                page.get_by_label("Email Subject").fill(datadictvalue["C_EMAIL_SBJCT"])
                page.get_by_label("Email Message").fill(datadictvalue["C_EMAIL_MSSG"])
            if datadictvalue["C_ENBL_ELCTRNC_SGNTR"] == 'No':
                page.get_by_text("Enable electronic signature").uncheck()

        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Do the save of the last Contract Types before signing out
        if i == rowcount:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Contract Types Saved Successfully")
            datadictvalue["RowStatus"] = "Contract Types are added successfully"

        except Exception as e:
            print("Contract Types not saved")
            datadictvalue["RowStatus"] = "Contract Types not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_BILLING_CONFIG_WRKBK, CONTRACT_TYPES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_BILLING_CONFIG_WRKBK, CONTRACT_TYPES,
                             PRCS_DIR_PATH + PPM_BILLING_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_BILLING_CONFIG_WRKBK, CONTRACT_TYPES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_BILLING_CONFIG_WRKBK)[0] + "_" + CONTRACT_TYPES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_BILLING_CONFIG_WRKBK)[
            0] + "_" + CONTRACT_TYPES + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
