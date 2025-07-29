from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(6000)
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox").fill("Manage Bank Accounts")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Bank Accounts").first.click()
    page.wait_for_timeout(3000)

    i = 0

    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(5000)

        # Bank Branch
        if datadictvalue["C_BANK_BRNCH"] != '':
            page.get_by_label("Bank Branch").click()
            page.wait_for_timeout(2000)
            page.get_by_title("Search: Bank Branch").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_role("textbox", name="Bank Branch").click()
            page.get_by_role("textbox", name="Bank Branch").fill(str(datadictvalue["C_BANK_BRNCH"]))
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=(str(datadictvalue["C_BANK_BRNCH"])), exact=True).click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

            # Account Name
            page.get_by_label("Account Name", exact=True).click()
            page.get_by_label("Account Name", exact=True).fill(str(datadictvalue["C_ACCNT_NAME"]))
            page.wait_for_timeout(2000)

            # Account Number
            page.get_by_label("Account Number", exact=True).click()
            page.get_by_label("Account Number", exact=True).fill(str(datadictvalue["C_ACCNT_NMBR"]))
            page.wait_for_timeout(2000)

            # Currency
            page.get_by_label("Currency", exact=True).click()
            page.get_by_label("Currency", exact=True).select_option('USD - US Dollar')
            # page.get_by_label("Currency", exact=True).select_option(datadictvalue["C_CRRNY"]) - WB Value should be corrected
            page.wait_for_timeout(2000)

            # Legal Entity Name
            if datadictvalue["C_LEGAL_ENTITY_NAME"] != '':
                page.get_by_label("Legal Entity Name").click()
                page.wait_for_timeout(2000)
                page.get_by_title("Search: Legal Entity Name").click()
                page.get_by_role("link", name="Search...").click()
                page.wait_for_timeout(2000)
                page.get_by_role("textbox", name="Legal Entity").click()
                page.get_by_role("textbox", name="Legal Entity").fill(datadictvalue["C_LEGAL_ENTITY_NAME"])
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Search", exact=True).click()
                page.get_by_role("cell", name=datadictvalue["C_LEGAL_ENTITY_NAME"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)

            # Account Type
            if datadictvalue["C_ACCNT_TYPE"] != '':
                page.get_by_label("Account Type").click()
                page.get_by_label("Account Type").select_option(datadictvalue["C_ACCNT_TYPE"])
                page.wait_for_timeout(2000)

            # Description
            if datadictvalue["C_DSCRPTN"] != '':
                page.get_by_label("Description").click()
                page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
                page.wait_for_timeout(2000)

            # IBAN
            if datadictvalue["C_IBAN"] != '':
                page.get_by_label("C_IBAN").fill(datadictvalue["C_IBAN"])
                page.wait_for_timeout(2000)

            # Check Digit
            if datadictvalue["C_CHECK_DIGIT"] != '':
                page.get_by_label("Check Digit").fill(datadictvalue["C_CHECK_DIGIT"])
                page.wait_for_timeout(2000)

            # Secondary Account Reference
            if datadictvalue["C_SCNDRY_ACCNT_REFRNC"] != '':
                page.get_by_label("Secondary Account Reference").fill(datadictvalue["C_SCNDRY_ACCNT_REFRNC"])
                page.wait_for_timeout(2000)

            # Account Suffix
            if datadictvalue["C_ACCNT_SFFX"] != '':
                page.get_by_label("Account Suffix").fill(datadictvalue["C_ACCNT_SFFX"])
                page.wait_for_timeout(2000)

            # Account Use - (Payables/Payroll/Receivables)
            if datadictvalue["C_PYBL_USE"] == "Yes":
                if not page.get_by_text("Payables").is_checked():
                    page.get_by_text("Payables").click()
                    page.wait_for_timeout(2000)
            if datadictvalue["C_PYRLL_USE"] == "Yes":
                if not page.get_by_text("Payroll").is_checked():
                    page.get_by_text("Payroll").click()
                    page.wait_for_timeout(2000)
            if datadictvalue["C_RCVBL_USE"] == "Yes":
                if not page.get_by_text("Receivables").is_checked():
                    page.get_by_text("Receivables").click()
                    page.wait_for_timeout(2000)
        page.wait_for_timeout(2000)

        # General -- GL Accounts - (Cash/Cash Clearing/Reconciliation Differences)
        page.get_by_role("link", name="General").click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_CASH_ACCNT"] != '':
            # page.get_by_label("Cash", exact=True).first.click()
            page.locator("//input[@aria-label='Cash']").click()
            page.locator("//input[@aria-label='Cash']").fill(str(datadictvalue["C_CASH_ACCNT"]))
            page.wait_for_timeout(3000)
        if datadictvalue["C_CASH_CLRNG_ACCNT"] != '':
            # page.get_by_label("Cash Clearing").click()
            page.locator("//input[@aria-label='Cash Clearing']").click()
            page.locator("//input[@aria-label='Cash Clearing']").fill(str(datadictvalue["C_CASH_CLRNG_ACCNT"]))
            page.wait_for_timeout(3000)
        if datadictvalue["C_RCNCLLTN_DFFRNCS"] != '':
            page.get_by_label("Reconciliation Differences").click()
            # page.get_by_text("Reconciliation Differences").first.click()
            page.get_by_text("Reconciliation Differences").fill(str(datadictvalue["C_RCNCLLTN_DFFRNCS"]))
            page.wait_for_timeout(3000)
        # Enable multiple cash account combinations for reconciliation (Available in UI, but not in WB)
        # if datadictvalue["C_RCNCLLTN_DFFRNCS"] != '':
        #   page.get_by_text("Enable multiple cash account combinations for reconciliation")
        # page.get_by_text("GL Cash Account Segments").click()

        # Additional Information
        # Alternate Account Name
        if datadictvalue["C_ALTRNT_ACCNT_NAME"] != '':
            page.get_by_label("Alternate Account Name").fill(datadictvalue["C_ALTRNT_ACCNT_NAME"])

        # Account Holder
        if datadictvalue["C_ALTRNT_ACCNT_HLDR"] != '':
            page.get_by_label("Alternate Account Holder").fill(datadictvalue["C_ALTRNT_ACCNT_HLDR"])

        # Account Holder
        if datadictvalue["C_ACCNT_HLDR"] != '':
            page.get_by_label("Account Holder", exact=True).fill(datadictvalue["C_ACCNT_HLDR"])

        # EFT Number
        if datadictvalue["C_EFT_NMBR"] != '':
            page.get_by_label("EFT Number").fill(datadictvalue["C_EFT_NMBR"])

        # Agency Location Code
        if datadictvalue["C_AGNCY_LOC_CODE"] != '':
            page.get_by_label("Agency Location Code").fill(datadictvalue["C_AGNCY_LOC_CODE"])

        # Active
        if datadictvalue["C_ACTV"] != '':
            if datadictvalue["C_ACTV"] == "Yes":
                page.get_by_text("Active", exact=True).check()
            elif datadictvalue["C_ACTV"] == "No" or '':
                page.get_by_text("Active", exact=True).uncheck()
            page.wait_for_timeout(2000)

        # Multicurrency account
        if datadictvalue["C_MULTCRRNCY_ACCNT"] != '':
            if datadictvalue["C_MULTCRRNCY_ACCNT"] == "Yes":
                page.get_by_text("Multicurrency account", exact=True).check()
            elif datadictvalue["C_MULTCRRNCY_ACCNT"] == "No" or '':
                page.get_by_text("Multicurrency account", exact=True).uncheck()
            page.wait_for_timeout(2000)

        # Netting account
        if datadictvalue["C_NTTNG_ACCNT"] != '':
            if datadictvalue["C_NTTNG_ACCNT"] == "Yes":
                page.get_by_text("Netting account", exact=True).check()
            elif datadictvalue["C_NTTNG_ACCNT"] == "No" or '':
                page.get_by_text("Netting account", exact=True).uncheck()
            page.wait_for_timeout(2000)

        # Regional Information
        # page.get_by_label("Regional Information").is_visible():
        # page.get_by_label("Regional Information").select_option(datadictvalue["C_RGNL_INFO"])
        # page.wait_for_timeout(3000)

        # Create Account Contact
        if datadictvalue["C_PRFX"] != '':
            page.wait_for_timeout(3000)
            page.get_by_label("Expand Contacts").click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Create").first.click()
            page.wait_for_timeout(3000)
            page.get_by_label("Prefix").select_option(datadictvalue["C_PRFX"])
            page.wait_for_timeout(3000)
            page.get_by_label("First Name").click()
            page.get_by_label("First Name").fill(datadictvalue["C_FIRST_NAME"])
            page.get_by_label("Middle Name").click()
            page.get_by_label("Middle Name").fill(datadictvalue["C_MDDL_NAME"])
            page.get_by_label("Last Name").click()
            page.get_by_label("Last Name").fill(datadictvalue["C_LAST_NAME"])
            page.get_by_label("Comments").click()
            page.get_by_label("Comments").fill(datadictvalue["C_CMMNTS"])
            page.wait_for_timeout(3000)

            # Add Phone Number
            if datadictvalue["C_PHONE"] != '':
                page.get_by_role("button", name="Add Row").first.click()
                page.wait_for_timeout(2000)

                # Purpose
                page.locator("//span[text()='Purpose']//following::select").select_option(datadictvalue["C_PRPS_PHONE"])
                page.wait_for_timeout(2000)

                # Phone Country Code
                page.get_by_label("Phone Country Code").click()
                page.get_by_title("Search: Phone Country Code").click()
                page.get_by_role("link", name="Search...").click()
                page.wait_for_timeout(2000)
                page.get_by_role("textbox", name="Phone Country Code").clear()
                page.get_by_role("textbox", name="Phone Country Code").fill(str(datadictvalue["C_PHONE_CNTRY_CODE"]))
                page.get_by_role("button", name="Search", exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("cell", name=str(datadictvalue["C_PHONE_CNTRY_CODE"]), exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)

                # Area Code
                if datadictvalue["C_AREA_CODE"] != '':
                    page.get_by_label("Area Code").fill(str(datadictvalue["C_AREA_CODE"]))
                if datadictvalue["C_PHONE"] != '':
                    page.get_by_label("Phone", exact=True).fill(str(datadictvalue["C_PHONE"]))
                if datadictvalue["C_EXTNSN"] != '':
                    page.get_by_label("Extension").fill(datadictvalue["C_EXTNSN"])
                page.wait_for_timeout(3000)

            #  Add Address
            if datadictvalue["C_CITY"] != '':
                page.get_by_role("cell", name="Addresses This table contains column headers corresponding to the data body table below Addresses No data to display. Columns Hidden 2 Address date range : Current",
                                 exact=True).get_by_role("button").first.click()
                page.get_by_role("button", name="Create").click()
                page.get_by_label("Country", exact=True).select_option(datadictvalue["C_CNTRY"])
                page.get_by_label("Address Line 1").fill(datadictvalue["C_ADDRSS_LINE_1"])
                page.get_by_label("Address Line 2").fill(datadictvalue["C_ADDRSS_LINE_2"])
                page.get_by_label("City").fill(datadictvalue["C_CITY"])
                page.get_by_role("option", name=datadictvalue["C_CITY"]).click()
                page.get_by_label("Postal Code").fill(datadictvalue["Postal Code"])
                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)

            #  Add Email
            if datadictvalue["C_EMAIL"] != '':
                page.get_by_role("button", name="Add Row").nth(1).click()
                page.wait_for_timeout(2000)
                page.locator("//span[text()='Purpose']//following::select").select_option("Home")
                page.get_by_label("Email").fill(datadictvalue["C_EMAIL"])
                page.wait_for_timeout(3000)

            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)

        # Payment Documents:
        # if datadictvalue["C_PYMNT_DOC"] != '':
        #     page.get_by_role("button", name="Create").nth(1).click()
        #     page.wait_for_timeout(3000)
        #     page.get_by_label("Payment Document", exact=True).fill(datadictvalue["C_PYMNT_DOC"])
        #     page.locator("//label[text()='Format']//following::input[1]").fill(datadictvalue["C_FRMT"])
        #     page.get_by_role("option", name=datadictvalue["C_FRMT"], exact=True).click()
        #     page.get_by_label("First Available Document").fill(datadictvalue["C_FRST_AVLBLE_DOCMNT_NUM"])
        #     page.get_by_role("button", name="OK", exact=True).click()
        #     page.wait_for_timeout(3000)
        page.wait_for_timeout(3000)

        # Controls - Cash Management Controls
        page.get_by_role("link", name="Controls").click()
        page.wait_for_timeout(3000)
        if datadictvalue["C_MNL_RCNCLLTN_TLRNC_RULE"] != '':
            page.get_by_label("Manual Reconciliation Tolerance Rule").select_option(datadictvalue["C_MNL_RCNCLLTN_TLRNC_RULE"])
            page.wait_for_timeout(2000)
        if datadictvalue["C_BANK_EXCHNG_RATE_TYPE"] != '':
            page.get_by_label("Bank Exchange Rate Type").select_option(datadictvalue["C_BANK_EXCHNG_RATE_TYPE"])
            page.wait_for_timeout(2000)
        if datadictvalue["C_RVRSL_PRCSSNG_MTHD"] != '':
            page.get_by_label("Reversal Processing Method").select_option(datadictvalue["C_RVRSL_PRCSSNG_MTHD"])
            page.wait_for_timeout(2000)
        if datadictvalue["C_AUTO_RCNCLLTN_RULE_SET"] != '':
            page.get_by_label("Automatic Reconciliation Rule Set").click()
            page.get_by_title("Search: Automatic Reconciliation Rule Set").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Rule Set", exact=True).click()
            page.get_by_label("Rule Set", exact=True).fill(datadictvalue["C_AUTO_RCNCLLTN_RULE_SET"])
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_AUTO_RCNCLLTN_RULE_SET"], exact=True).first.click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="OK").click()
            # page.get_by_label("Automatic Reconciliation Rule Set").click()
            # page.get_by_label("Automatic Reconciliation Rule Set").fill(datadictvalue["C_AUTO_RCNCLLTN_RULE_SET"])
            page.wait_for_timeout(2000)

        # Bank Statement Processing
        if datadictvalue["C_PSNG_RULE_SET"] != '':
            page.get_by_label("Parsing Rule Set").select_option(datadictvalue["C_PSNG_RULE_SET"])
            page.wait_for_timeout(2000)
        # Bank Statement Transaction Creation Rules
        # Sequence
        if datadictvalue["C_SQNC"] != '':
            page.get_by_role("button", name="Add").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Rule", exact=True).fill("RES")
            page.wait_for_timeout(2000)
        if datadictvalue["C_DSCRPTN_BANK_STMNT_TRNSCTN_CRTN_RULES"] != '':
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN_BANK_STMNT_TRNSCTN_CRTN_RULES"])
            page.wait_for_timeout(2000)
        # Cash Positioning and Forecasting
        if datadictvalue["C_TRGT_BLNC"] != '':
            page.get_by_label("Target Balance").fill(datadictvalue["C_TRGT_BLNC"])
            page.wait_for_timeout(2000)
        if datadictvalue["C_TRNSCTN_CLNDR"] != '':
            page.get_by_label("Transaction Calendar").select_option(datadictvalue["C_TRNSCTN_CLNDR"])
            page.wait_for_timeout(2000)

        # Security
        page.get_by_role("link", name="Security").click()
        page.wait_for_timeout(2000)
        # Users and Roles
        if datadictvalue["C_SCR_BANK_ACCT_BY_USER_AND_ROLES"] == "Yes":
            if not page.get_by_text("Secure Bank Account by Users and Roles").is_checked():
                page.get_by_text("Secure Bank Account by Users and Roles").click()
                page.wait_for_timeout(2000)

        if datadictvalue["C_SCR_BANK_ACCT_BY_USER_AND_ROLES"] != '':
            page.get_by_text("Secure Bank Account by Users and Roles").click()
            page.get_by_label("Actions").locator("div").click()
            page.wait_for_timeout(2000)
            page.get_by_text("Select and Add", exact=True).click()
            page.get_by_label("Secure By").select_option(datadictvalue["C_SCR_BY"])
            page.wait_for_timeout(2000)
            page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        # Business Unit
        if datadictvalue["C_BSNSS_UNIT"] != '':
            page.get_by_role("link", name="Business Unit Access").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Business Unit").fill(datadictvalue["C_BSNSS_UNIT"])
            page.wait_for_timeout(2000)
            if datadictvalue["C_END_DATE"] != '':
                page.locator("//label[text()='End Date']//following::input[1]").clear()
                page.locator("//label[text()='End Date']//following::input[1]").fill(datadictvalue["C_END_DATE"])
                page.wait_for_timeout(2000)
            if datadictvalue["C_CASH"] != '':
                page.get_by_label("Cash", exact=True).fill(datadictvalue["C_CASH"])
            if datadictvalue["C_CASH_CLRNG"] != '':
                page.get_by_label("Cash Clearing", exact=True).fill(datadictvalue["C_CASH_CLRNG"])
            if datadictvalue["C_BANK_CHRGS"] != '':
                page.get_by_label("Bank Charges").fill(datadictvalue["C_BANK_CHRGS"])
            if datadictvalue["C_FRGN_EXHNG_GAIN"] != '':
                page.get_by_label("Foreign Exchange Gain").fill(datadictvalue["C_FRGN_EXHNG_GAIN"])
            if datadictvalue["C_FRGN_EXHNG_LOSS"] != '':
                page.get_by_label("Foreign Exchange Loss").fill(datadictvalue["C_FRGN_EXHNG_LOSS"])
                page.wait_for_timeout(2000)

        # Payment Document Categories by Payment Method
            # Payment Method
            if datadictvalue["C_PYMNT_MTHD"] != '':
                page.get_by_role("button", name="Add").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Payment Method", exact=True).click()
                page.get_by_label("Payment Method", exact=True).fill(datadictvalue["C_PYMNT_MTHD"])
                page.wait_for_timeout(2000)

                # Payment Document Category
                page.get_by_label("Payment Document Category").select_option(datadictvalue["C_PYMNT_DOC_CTGRY"])
                page.wait_for_timeout(3000)

            # Payment Method - uncommand the below code in case more than one payment methods need to be added
            # if datadictvalue["C_PYMNT_MTHD1"] != '':
            #     page.get_by_role("button", name="Add").click()
            #     page.wait_for_timeout(2000)
            #     page.get_by_label("Payment Method", exact=True).click()
            #     page.get_by_label("Payment Method", exact=True).fill(datadictvalue["C_PYMNT_MTHD1"])
            #     page.wait_for_timeout(2000)
            #
            #     # Payment Document Category
            #     page.get_by_label("Payment Document Category").select_option(datadictvalue["C_PYMNT_DOC_CTGRY1"])
            #     page.wait_for_timeout(2000)

            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        if page.get_by_text("Information").is_visible():
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)

        try:
            expect(page.get_by_role("heading", name="Manage Bank Accounts")).to_be_visible()
            print("Added Bank Accounts details Saved Successfully")
            datadictvalue["RowStatus"] = "Added Bank Accounts details and code"
        except Exception as e:
            print("Unable to save Bank Accounts details")
            datadictvalue["RowStatus"] = "Unable to Add Bank Accounts details and code"
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Added Bank Accounts details Successfully"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, BANK_ACCOUNT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, BANK_ACCOUNT, PRCS_DIR_PATH + CM_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + CM_WORKBOOK, BANK_ACCOUNT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0] + "_" + BANK_ACCOUNT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
