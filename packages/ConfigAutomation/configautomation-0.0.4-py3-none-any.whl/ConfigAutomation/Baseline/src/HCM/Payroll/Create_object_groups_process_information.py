from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.get_by_role("link", name="Home", exact=True).click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="My Client Groups").click()
    page.get_by_role("link", name="Payroll").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Object Groups").click()
    page.wait_for_timeout(4000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        # Select Legislative data group
        page.get_by_role("combobox", name="Legislative Data Group").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTV_DATA_GROUP"], exact=True).click()
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)

        # Create Object Group
        page.get_by_role("button", name="Create").click()

        # Fill name
        page.locator("//div[text()='Create Object Group']//following::label[text()='Name']//following::input[1]").clear()
        page.locator("//div[text()='Create Object Group']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_NAME"])

        # Select type as Deduction Card Group
        page.locator("//div[text()='Create Object Group']//following::label[text()='Legislative Data Group']//following::input[1]").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
        page.wait_for_timeout(3000)

        # Select Continue to enter more details
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(2000)


        # Select Start Date
        page.locator("//label[text()='Start Date']//following::input[1]").clear()
        page.locator("//label[text()='Start Date']//following::input[1]").fill(datadictvalue["C_START_DATE"])

        # Select End Date
        page.locator("//label[text()='End Date']//following::input[1]").clear()
        page.locator("//label[text()='End Date']//following::input[1]").fill(datadictvalue["C_END_DATE"])

        # Enter Description
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(2000)

        #Enter ObjectGroupStore
        if datadictvalue["C_OBJCT_GRP_CNTXT_SGMNT"] == 'Bank Correction':
            page.get_by_role("combobox", name="Context Segment", exact=True).click()
            page.get_by_text("Bank Correction").click()
            #page.get_by_role("combobox", name="Context Segment", exact=True).select_option(datadictvalue["C_OBJCT_GRP_CNTXT_SGMNT"])

            if datadictvalue["C_BANK_CRRCTN_ASSGNMNT_NMBR"] != 'N/A' or '':
                page.get_by_role("button", name="Add Row").click()
                page.get_by_label("Assignment Number").clear()
                page.get_by_label("Assignment Number").fill(datadictvalue["C_BANK_CRRCTN_ASSGNMNT_NMBR"])
                page.get_by_label("Employee Name").clear()
                page.get_by_label("Employee Name").fill(datadictvalue["C_BANK_CRRCTN_EMPLY_NAME"])
                page.get_by_role("cell", name="Press down arrow to access Calendar Payment Date Select Date", exact=True).get_by_placeholder("m/d/yy").clear()
                page.get_by_role("cell", name="Press down arrow to access Calendar Payment Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_BANK_CRRCTN_PYMNT_DATE"])
                page.get_by_role("cell", name="Press down arrow to access Calendar Process Date Select Date", exact=True).get_by_placeholder("m/d/yy").clear()
                page.get_by_role("cell", name="Press down arrow to access Calendar Process Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_BANK_CRRCTN_PRCSS_DATE"])
                page.get_by_label("Payment Reference").clear()
                page.get_by_label("Payment Reference").fill(datadictvalue["C_BANK_CRRCTN_PYMNT_RFRNC"])
                page.get_by_label("Amount").clear()
                page.get_by_label("Amount").fill(str(datadictvalue["C_BANK_CRRCTN_AMNT"]))
                page.get_by_label("Check Number").clear()
                page.get_by_label("Check Number").fill(str(datadictvalue["C_BANK_CRRCTN_CHCK_NMBR"]))
                page.get_by_label("Replacement Branch Number").clear()
                page.get_by_label("Replacement Branch Number").fill(str(datadictvalue["C_BANK_CRRCTN_RPLCCMNT_BRNCH_NMBR"]))
                page.get_by_label("Replacement Account Type").clear()
                page.get_by_label("Replacement Account Type").fill(datadictvalue["C_BANK_CRRCTN_RPLCMNT_ACCNT_TYPE"])
                page.wait_for_timeout(2000)
                page.get_by_label("Replacement Account Number").clear()
                page.get_by_label("Replacement Account Number").fill(str(datadictvalue["C_BANK_CRRCTN_RPLCMNT_ACCNT_NMBR"]))
                page.wait_for_timeout(2000)

        if datadictvalue["C_OBJCT_GRP_CNTXT_SGMNT"] == 'Global Transfer Balance Adjustment':
            page.get_by_role("combobox", name="Context Segment", exact=True).click()
            page.get_by_text("Global Transfer Balance").click()
            page.get_by_role("button", name="Search", exact=True).click()

            if datadictvalue["C_GLBL_TRNSFR_BLNC_ADJSTMNT_SQNC_NMBR"] != 'N/A' or '':
                page.get_by_role("button", name="Add Row").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Source Defined Balance").click()
                page.get_by_title("Search: Source Defined Balance").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Value").click()
                page.get_by_label("Value").fill(datadictvalue["C_GLBL_TRNSFR_BLNC_ADJSTMNT_SRC_DFND_BLNC"])
                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_GLBL_TRNSFR_BLNC_ADJSTMNT_SRC_DFND_BLNC"]).click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Target Balance").click()
                page.get_by_title("Search: Target Balance").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Value").click()
                page.get_by_label("Value").fill(datadictvalue["C_GLBL_TRNSFR_BLNC_ADJSTMNT_TRGT_BLNC"])
                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_GLBL_TRNSFR_BLNC_ADJSTMNT_TRGT_BLNC"]).click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Prerequisite Target Element").click()
                page.get_by_title("Search: Prerequisite Target").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Value").click()
                page.get_by_label("Value").fill(datadictvalue["C_GLBL_TRNSFR_BLNC_ADJSTMNT_PRRQST_TRGT_ELMNT"])
                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_GLBL_TRNSFR_BLNC_ADJSTMNT_PRRQST_TRGT_ELMNT"]).nth(0).click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)


        #page.get_by_role("button", name="Cancel").click()
        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(2000)

        i = i + 1
        # Validation
        try:
            expect(page.get_by_role("heading", name="Object Groups")).to_be_visible()
            print("Object Group Elements Created Successfully")

        except Exception as e:
            print("Object Group Creation Elements UnSuccessfull")


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_PRO_I):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_PRO_I, PRCS_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_PRO_I)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_OBJ_GRP_CONFIG_WRKBK)[0] + "_" +DST_OBJ_GRP_PRO_I)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_OBJ_GRP_CONFIG_WRKBK)[0] + "_" +DST_OBJ_GRP_PRO_I + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))