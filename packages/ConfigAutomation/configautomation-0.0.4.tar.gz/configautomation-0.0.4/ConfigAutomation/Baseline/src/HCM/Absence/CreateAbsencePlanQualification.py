from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.pause()

    # Login to application
    # page.get_by_placeholder("User ID").click()
    # page.get_by_placeholder("User ID").fill(IMPLUSRID)
    # page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    # page.get_by_role("button", name="Sign In").click()
    # page.wait_for_timeout(5000)

    SingleSignONwithUserPwd(page)

    # Navigation
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Navigator").click()
    page.wait_for_timeout(2000)
    page.get_by_title("My Client Groups", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Absences", exact=True).click()
    page.wait_for_timeout(5000)

    # Search and Select Absence Plan
    page.get_by_placeholder("Search for tasks").click()
    page.get_by_placeholder("Search for tasks").type("Absence Plans")
    page.get_by_role("link", name="Search for tasks").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Absence Plans").click()
    page.wait_for_timeout(4000)

    page.pause()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        # Create Absence Plan
        page.get_by_role("button", name="Create").click()
        page.locator("//div[text()='Create Absence Plan']//following::input[1]").click()
        page.locator("//div[text()='Create Absence Plan']//following::input[1]").fill("")
        page.locator("//div[text()='Create Absence Plan']//following::input[1]").type(datadictvalue["C_EFFCTV_DATE"])
        page.wait_for_timeout(1000)
        page.locator("//div[text()='Create Absence Plan']//following::label[text()='Legislation']//following::input[1]").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTN"], exact=True).click()
        page.locator("//div[text()='Create Absence Plan']//following::label[text()='Plan Type']//following::input[1]").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLAN_TYPE"], exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(2000)

        # General Attribute - Plan Attributes
        page.get_by_label("Plan", exact=True).click()
        page.get_by_label("Plan", exact=True).type(datadictvalue["C_PLAN"])
        page.wait_for_timeout(1000)
        if datadictvalue["C_DSCRPTN"]!='N/A':
            page.get_by_label("Description").click()
            page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Plan UOM").click()
        page.wait_for_timeout(1000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLAN_UOM"], exact=True).click()
        page.wait_for_timeout(1000)
        if datadictvalue["C_ALTNTV_SCHDL_CTGRY"] != "N/A":
            page.get_by_role("combobox", name="Alternative Schedule Category").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ALTNTV_SCHDL_CTGRY"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_LGSLTV_GRPNG_CODE"] != "N/A":
            page.get_by_role("combobox", name="Legislative Grouping Code").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTV_GRPNG_CODE"])
            page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Legislative Data Group").click()
        page.get_by_text(datadictvalue["C_LGSLTV_DATA_GRP"], exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Status").click()
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

        if datadictvalue["C_CNCRRNT_ENTTLMNT"] != "No":
            page.get_by_text("Enable concurrent entitlement", exact=True).click()
            page.wait_for_timeout(1000)

        if datadictvalue["C_CNVRSN_FRML"] != "N/A":
            page.get_by_role("combobox", name="Conversion Formula").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CNVRSN_FRML"])
            page.wait_for_timeout(2000)

        # Plan Term - Rolling forward
        if datadictvalue["C_TYPE"] == 'Rolling forward':
            page.get_by_role("combobox", name="Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Type").click()
            page.get_by_text(datadictvalue["C_TYPE"]).click()
            page.get_by_role("combobox", name="Start Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_START_RULE"]).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_START_RULE"] == "Formula":
                if datadictvalue["C_START_FRML"] != "N/A":
                    page.get_by_role("row", name="Start Formula", exact=True).locator("label").click()
                    page.get_by_role("row", name="Start Formula", exact=True).locator("a").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_START_FRML"]).click()
                    page.wait_for_timeout(1000)

            if datadictvalue["C_START_RULE"] == "Absence start date":
                if datadictvalue["C_TERM_DRTN"] != "N/A":
                    page.get_by_text("Term Duration", exact=True).click()
                    page.get_by_label("Term Duration", exact=True).fill(str(datadictvalue["C_TERM_DRTN"]))
                    page.wait_for_timeout(2000)
                if datadictvalue["C_TERM_DRTN_UOM"] != "N/A":
                    page.get_by_text("Term Duration UOM").click()
                    page.get_by_role("combobox", name="Term Duration UOM").click()
                    #page.get_by_role("row", name="Term Duration UOM", exact=True).locator("a").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TERM_DRTN_UOM"]).click()
                    page.wait_for_timeout(2000)
                if datadictvalue["C_OVRLP_RULE"] != "N/A":
                    page.get_by_text("Overlap Rule").click()
                    page.get_by_role("row", name="Overlap Rule", exact=True).locator("a").click()
                    page.get_by_text(datadictvalue["C_OVRLP_RULE"]).click()
                    page.wait_for_timeout(2000)

        # Plan Term - Rolling backward
        if datadictvalue["C_TYPE"] == 'Rolling backward':
            page.get_by_role("combobox", name="Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Start Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_START_RULE"]).click()
            page.wait_for_timeout(3000)
            if datadictvalue["C_START_RULE"] == "Formula":
                if datadictvalue["C_START_FRML"] != "N/A":
                    page.get_by_role("combobox", name="Start Formula")
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_START_FRML"]).click()
                    page.wait_for_timeout(1000)

            if datadictvalue["C_START_RULE"] == "Absence start date":
                if datadictvalue["C_TERM_DRTN"] != "N/A":
                    page.get_by_text("Term Duration", exact=True).click()
                    page.get_by_label("Term Duration", exact=True).fill(str(datadictvalue["C_TERM_DRTN"]))
                    page.wait_for_timeout(2000)
                if datadictvalue["C_TERM_DRTN_UOM"] != "N/A":
                    page.get_by_role("combobox", name="Term Duration UOM").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TERM_DRTN_UOM"]).click()
                    page.wait_for_timeout(2000)
                if datadictvalue["C_OVRLP_RULE"] != "N/A":
                    page.get_by_role("combobox", name="Overlap Rule").click()
                    page.get_by_text(datadictvalue["C_OVRLP_RULE"]).click()
                    page.wait_for_timeout(2000)

        # Plan Term - Calendar year
        if datadictvalue["C_TYPE"] == 'Calendar Year':
            page.get_by_role("combobox", name="Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Calendar']//following::input[1]").click()
            page.locator("//label[text()='Calendar']//following::input[1]").type(datadictvalue["C_CLNDR"])

        # Plan Term - Absence duration
        if datadictvalue["C_TYPE"] == 'Absence Duration':
            page.get_by_role("combobox", name="Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
            page.wait_for_timeout(2000)

        # Legislative Information
        if datadictvalue["C_CNTXT_SGMNT"] != "N/A":
            page.get_by_role("combobox", name="Context Segment").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CNTXT_SGMNT"]).click()
            page.wait_for_timeout(4000)

        if datadictvalue["C_VCTN_PLAN_CRRNT_YEAR"] != "N/A":
            page.get_by_title("Search: Vacation Plan Current").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Value").click()
            page.get_by_label("Value").fill(datadictvalue["C_VCTN_PLAN_CRRNT_YEAR"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VCTN_PLAN_CRRNT_YEAR"]).click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        if datadictvalue["C_VCTN_PLAN_PRVS_YEAR"] != "N/A":
            page.get_by_title("Search: Vacation Plan Previous Year").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Value").click()
            page.get_by_label("Value").fill(datadictvalue["C_VCTN_PLAN_CRRNT_YEAR"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VCTN_PLAN_PRVS_YEAR"]).click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        if datadictvalue["C_ENTTLMNT_SNRTY_DAYS"] != "N/A":
            page.get_by_title("Search: Entitlement to Seniority Days").click()
            page.get_by_role("cell", name="Yes", exact=True).click()
            page.wait_for_timeout(2000)

        # Descriptive Information
        if datadictvalue["C_DI_CNTXT_SGMNT"] != "N/A":
            page.get_by_role("combobox", name="Context Segment").nth(1).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DI_CNTXT_SGMNT"]).click()

        # Participation
        page.get_by_role("link", name="Participation").click()
        page.wait_for_timeout(5000)
        page.get_by_role("combobox", name="Qualification Date Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_QLFCTN_DATE_RULE"]).click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_QLFCTN_DATE_RULE"] == "Formula":
            if datadictvalue["C_ER_FRML"] != "N/A":
                page.get_by_role("combobox", name="Formula").click()
                page.get_by_text(datadictvalue["C_ER_FRML"]).click()
                page.wait_for_timeout(2000)
        if datadictvalue["C_EVLT_ABSNC_RCRD"] != "No":
            if not page.get_by_text("Evaluate remaining entitlement without absence record").is_checked():
                page.get_by_text("Evaluate remaining entitlement without absence record", exact=True).click()
                page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Entitlement End Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ENTTLMNT_END_RULE"]).click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_ENTTLMNT_END_RULE"] == "Formula":
            if datadictvalue["C_ENTTLMNT_END_FRML"] != "N/A":
                page.get_by_role("combobox", name="Entitlement End Formula").click()
                page.locator("[id=\"__af_Z_window\"]").page.get_by_text(datadictvalue["C_ENTTLMNT_END_FRML"]).click()
                page.wait_for_timeout(2000)

        # Eligibility
        page.get_by_role("heading", name="Eligibility").click()
        page.wait_for_timeout(4000)
        page.get_by_role("button", name="Select and Add").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Sequence").click()
        page.get_by_label("Sequence").fill(str(datadictvalue["C_SQNC"]))
        page.wait_for_timeout(1000)
        page.get_by_title("Search: Eligibility Profile").click()
        page.wait_for_timeout(2000)
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("button", name="Advanced").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Name").nth(1).click()
        page.get_by_label("Name").nth(1).fill("")
        page.get_by_label("Name").nth(1).type(datadictvalue["C_ELGBTY_PROFL"])
        page.wait_for_timeout(2000)
        page.get_by_label("Status Operator").click()
        page.get_by_role("listbox").get_by_text("Is not blank").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(5000)
        page.get_by_role("cell", name=datadictvalue["C_ELGBTY_PROFL"]).nth(1).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="OK").first.click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_RQRD"] != "No":
            if not page.locator("[id=\"__af_Z_window\"]").get_by_text("Required").is_checked():
                page.locator("[id=\"__af_Z_window\"]").get_by_text("Required").click()
                page.wait_for_timeout(3000)
        page.get_by_title("Save and Close").click()
        page.wait_for_timeout(4000)

       #Entitlements
        page.get_by_role("link", name="Entitlements").click()
        page.wait_for_timeout(4000)
        if datadictvalue["C_ENTTLMNT_DFNTN_TYPE"] == "Matrix":
            page.get_by_text("Matrix", exact=True).click()
            page.wait_for_timeout(4000)

            # Qualification Band Matrix
            page.get_by_role("button", name="Add").first.click()
            page.wait_for_timeout(3000)
            page.get_by_label("Expression").click()
            page.get_by_label("Expression").fill(str(datadictvalue["C_QM_SQNC"]))
            page.wait_for_timeout(2000)
            page.get_by_role("link", name="Expression Builder").nth(0).click()
            page.wait_for_timeout(3000)
            page.locator("//div[text()='Expression:']//following::textarea[1]").click()
            page.locator("//div[text()='Expression:']//following::textarea[1]").type(str(datadictvalue["C_EXPRSSN_BLDR"]))
            page.get_by_role("button", name="OK").first.click()
            page.wait_for_timeout(2000)

            # Qualification Details
            page.get_by_role("heading", name="Qualification Details").click()
            page.get_by_role("button", name="Add").nth(1).click()
            page.wait_for_timeout(3000)
            page.get_by_label("Sequence").click()
            page.get_by_label("Sequence").fill(str(datadictvalue["C_QD_SQNC"]))
            page.wait_for_timeout(1000)
            page.get_by_label("Detail Name").click()
            page.get_by_label("Detail Name").fill(datadictvalue["C_DTL_NAME"])
            page.wait_for_timeout(1000)
            page.locator("//label[text()='Duration']//following::input[1]").click()
            page.locator("//label[text()='Duration']//following::input[1]").fill(str(datadictvalue["C_QD_DRTN"]))
            page.wait_for_timeout(1000)
            page.get_by_label("Payment Percentage", exact=True).click()
            page.get_by_label("Payment Percentage", exact=True).fill(str(datadictvalue["C_QD_PYMNT_PRCNTG"]))
            page.wait_for_timeout(1000)
            if datadictvalue["C_QD_ENTTLMNT_FRML"] != "N/A":
                page.get_by_role("combobox", name="Entitlement Formula").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_QD_ENTTLMNT_FRML"], exact=True).click()
                page.wait_for_timeout(1000)
            page.get_by_title("Save and Close").click()
            page.wait_for_timeout(3000)

        elif datadictvalue["C_ENTTLMNT_DFNTN_TYPE"] == "Formula":
            page.get_by_text("Formula", exact=True).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_ENTTLMNT_FRML"] != "N/A":
                page.get_by_role("combobox", name="Entitlement Formula").click()
                page.get_by_text(datadictvalue["C_ENTTLMNT_FRML"]).click()
                page.wait_for_timeout(2000)

        if datadictvalue["C_PYMNT_PRCNTG_OVRRD"] != "No":
             page.locator("//h1[text()='Entitlement Attributes']//following::label[5]").is_checked()
             page.locator("//h1[text()='Entitlement Attributes']//following::label[5]").click()
             page.wait_for_timeout(2000)

        page.get_by_role("combobox", name="Entitlement Start Date").click()
        page.get_by_text(datadictvalue["C_ENTTLMNT_START_DATE"]).click()
        page.wait_for_timeout(3000)


        # Entries and Balances
        page.get_by_role("link", name="Entries and Balances").click()
        page.wait_for_timeout(4000)
        # Rates
        if datadictvalue["C_ABSNC_PYMNT_RATE"] != "N/A":
            page.get_by_role("combobox", name="Absence Payment Rate Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_PYMNT_RATE"]).click()
            page.wait_for_timeout(3000)
            if datadictvalue["C_ABSNC_PYMNT_RATE"] != "Formula" or "Unpaid":
                if datadictvalue["C_RATE_NAME"] != "N/A":
                    page.locator("//label[text()='Absence Payment Rate Rule']//following::label[text()='Rate Name']//following::input[1]").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    page.wait_for_timeout(2000)
            if datadictvalue["C_ABSNC_PYMNT_RATE"] == "Formula":
                if datadictvalue["C_R_FRML"] != "N/A":
                    page.locator("//label[text()='Absence Payment Rate Rule']//following::label[text()='Formula']//following::input[1]").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_R_FRML"]).click()
                    page.wait_for_timeout(2000)

        # Payroll Integration
        if datadictvalue["C_TRNFR_PYRLL_PRCSSG"] == "Yes":
            if not page.get_by_text("Transfer absence payment information for payroll processing").first.is_checked():
                page.get_by_text("Transfer absence payment information for payroll processing").first.click()
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Element").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ELMNT"]).click()
                page.wait_for_timeout(1000)

        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(10000)

        try:
            expect(page.get_by_role("heading", name="Absence Plans")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Absence Plans Qualification Created Successfully")
            datadictvalue["RowStatus"] = "Created Absence Plan Qualification Successfully"
        except Exception as e:
            print("Unable to Save Absence Plans Qualification")
            datadictvalue["RowStatus"] = "Unable to Save Absence Plan Qualification"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_PLAN_QUALIFICATION):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_PLAN_QUALIFICATION,PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_PLAN_QUALIFICATION)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
