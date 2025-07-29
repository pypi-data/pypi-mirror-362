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

    # Navigate to Setup and Maintenance
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Settings and Actions").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(3000)
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(5000)
    page.get_by_label("", exact=True).fill("Rate Definitions")
    page.get_by_label("", exact=True).click()
    page.get_by_role("button", name="Search").click()
    page.get_by_role("link", name="Rate Definitions").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        # Category
        #page.get_by_role("cell", name="*Category", exact=True).click()
        #page.get_by_role("row", name="*Category", exact=True).locator("a").click()
        #page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CTGRY"], exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Category").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CTGRY"], exact=True).click()
        page.wait_for_timeout(2000)

        # Effective Start Date
        if datadictvalue["C_EFFCTV_DATE"] != '':
            #page.get_by_role("cell", name="Create Rate Definition Close *Category *Effective Start Date m/d/yy Press down").get_by_placeholder("m/d/yy").clear()
            #page.get_by_role("cell", name="Create Rate Definition Close *Category *Effective Start Date m/d/yy Press down").get_by_placeholder("m/d/yy").fill(datadictvalue["C_EFCTV_DATE"])
            page.locator("//div[text()='Create Rate Definition']//following::input[3]").click()
            page.locator("//div[text()='Create Rate Definition']//following::input[3]").fill("")
            page.locator("//div[text()='Create Rate Definition']//following::input[3]").type(datadictvalue["C_EFFCTV_DATE"])
            #page.locator("//div[text()='Create Rate Definition']//following::input[3]").fill(datadictvalue["C_EFCTV_DATE"])
            page.wait_for_timeout(2000)

        # Legislative Data Group
        #page.get_by_role("row", name="*Legislative Data Group", exact=True).get_by_role("combobox").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Legislative Data Group").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTV_DATA_GRP"], exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        # Name
        #page.get_by_role("cell", name="Name", exact=True).first.click()
        #page.get_by_role("cell", name="*Name Code *Short Name").get_by_label("Name", exact=True).click()
        #page.get_by_role("cell", name="*Name Code *Short Name").get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
        page.locator("//label[text()='Name']//following::input[contains(@id,'it1::content')]").click()
        page.locator("//label[text()='Name']//following::input[contains(@id,'it1::content')]").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(2000)

        # Short Name
        page.get_by_label("Short Name").click()
        #page.get_by_role("cell", name="Short Name", exact=True).click()
        page.get_by_label("Short Name").fill(datadictvalue["C_SHORT_NAME"])
        page.wait_for_timeout(3000)

        # Element Name
        if datadictvalue["C_ELMNT_NAME"] != "N/A":
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Element Name", exact=True).click()
            page.get_by_text(datadictvalue["C_ELMNT_NAME"], exact=True).click()

        # Employment Level
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Employment Level").click()
        page.get_by_text(datadictvalue["C_EMPLYMNT_LEVEL"], exact=True).click()

        # Status
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Status").click()
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

        # Reporting Required
        if datadictvalue["C_RPRTNG_RQRD"] == "Yes":
            if not page.get_by_text("Reporting Required").is_checked():
                page.get_by_text("Reporting Required").click()
                page.wait_for_timeout(1000)

        # Calculate Live Rates
        if datadictvalue["C_CLCLT_LIVE_RATES"] == "Yes":
            if not page.get_by_text("Calculate Live Rates").is_checked():
                page.get_by_text("Calculate Live Rates").click()
                page.wait_for_timeout(1000)

        # Periodicity
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Periodicity", exact=True).click()
        page.get_by_text(datadictvalue["C_PRDCTY"], exact=True).click()

        # Periodicity Conversion Formula
        page.wait_for_timeout(3000)
        page.get_by_label("Periodicity Conversion Formula").click()
        page.get_by_title("Search: Periodicity").click()
        page.get_by_text(datadictvalue["C_PRDCTY_CNVRSN_FRML"], exact=True).click()

        # Factor Rule
        if datadictvalue["C_FCTR_RULE"] != "N/A":
            page.get_by_role("combobox", name="Factor Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FCTR_RULE"], exact=True).click()
            page.wait_for_timeout(3000)

        # Factor Rule Name
        if datadictvalue["C_RTRND_RULE_NAME"] != "N/A":
            page.get_by_label("Name", exact=True).nth(1).fill(str(datadictvalue["C_RTRND_RULE_NAME"]))

        # Currency
        page.get_by_text("Currency").click()
        page.get_by_label("Currency").click()
        page.get_by_label("Currency").fill(datadictvalue["C_CRRNCY"])

        # Decimal Display
        page.wait_for_timeout(1000)
        page.get_by_label("Decimal Display").click()
        page.get_by_label("Decimal Display").fill(str(datadictvalue["C_DCML_DSPLY"]))

        # Rounding Rule
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Rounding Rule").click()
        page.get_by_text(datadictvalue["C_RNDNG_RULE"], exact=True).click()

        # Minimum Rate Rule
        if datadictvalue["C_MNMM_RATE_RULE"] != "N/A":
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Minimum Rate Rule", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MNMM_RATE_RULE"], exact=True).click()
            #page.get_by_text(datadictvalue["C_MNMM_RATE_RULE"], exact=True).click()

        # Minimum Value
        if datadictvalue["C_MNMM_VALUE"] != "N/A":
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Minimum Value", exact=True).click()
            #page.get_by_text(datadictvalue["C_MNMM_VALUE"], exact=True).click()
            page.get_by_title("Search: Minimum Value").first.click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//div[text()='Search and Select: Rate Definition']//following::input[1]").click()
            page.locator("//div[text()='Search and Select: Rate Definition']//following::input[1]").type(datadictvalue["C_MNMM_VALUE"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MNMM_VALUE"]).click()
            page.get_by_role("button", name="OK").click()

        # Criteria Value
        if datadictvalue["C_MIN_CRTR_VALUE"] != "N/A":
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Criteria Value", exact=True).click()
            page.get_by_text(datadictvalue["C_MIN_CRTR_VALUE"], exact=True).click()

        # Limit Violation Action
        if datadictvalue["C_MIN_LMT_VLTN_ACTN"] != "N/A":
            page.wait_for_timeout(1000)
            #page.get_by_role("combobox", name="Limit Violation Action", exact=True).click()
            #page.get_by_text(datadictvalue["C_MIN_LMT_VLTN_ACTN"], exact=True).click()
            page.locator("//h2[text()='Returned Rate Details']//following::input[contains(@id,'LimitMode::content')][1]").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MIN_LMT_VLTN_ACTN"],exact=True).click()

        # C_MXMM_RATE_RULE
        if datadictvalue["C_MXMM_RATE_RULE"] != "N/A":
            page.wait_for_timeout(1000)
            #page.get_by_role("combobox", name="Minimum Rate Rule", exact=True).click()
            page.get_by_role("combobox", name="Maximum Rate Rule").click()
            #page.get_by_text(datadictvalue["C_MXMM_RATE_RULE"], exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MXMM_RATE_RULE"], exact=True).click()


        # Maximum Value
        if datadictvalue["C_MAX_MXMM_VALUE"] != "N/A":
            page.wait_for_timeout(1000)
            #page.get_by_role("combobox", name="Minimum Value", exact=True).click()
            page.get_by_role("textbox", name="Maximum Value").click()
            page.get_by_role("textbox", name="Maximum Value").fill(str(datadictvalue["C_MAX_MXMM_VALUE"]))
            #page.get_by_text(datadictvalue["C_MAX_MXMM_VALUE"], exact=True)

        # Criteria Value
        if datadictvalue["C_MAX_CRTR_VALUE"] != "N/A":
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Criteria Value", exact=True).click()
            page.get_by_text(datadictvalue["C_MAX_CRTR_VALUE"], exact=True).click()

        # Limit Violation Action
        if datadictvalue["C_MAX_LMT_VLTN_ACTN"] != "N/A":
            page.wait_for_timeout(1000)
            #page.get_by_role("combobox", name="Limit Violation Action", exact=True).click()
            #page.get_by_text(datadictvalue["C_MAX_LMT_VLTN_ACTN"], exact=True).click()
            page.locator("//h2[text()='Returned Rate Details']//following::input[contains(@id,'MaxLimitMode::content')]").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MAX_LMT_VLTN_ACTN"]).click()

        # Return Full-Time Rate
        if datadictvalue["C_RTRN_FULL_TIME_RATE"] != "No":
            if not page.get_by_text("Return Full-Time Rate").is_checked():
                page.get_by_text("Return Full-Time Rate").click()
                page.wait_for_timeout(1000)

        # Calculation Details - Contributor Type
        page.get_by_role("button", name="Create").click()
        page.get_by_role("combobox", name="Contributor Type").click()
        page.wait_for_timeout(5000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CNTRBTR_TYPE"], exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="OK").click()

        # Add or Subtract
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Add or Subtract").click()
        page.wait_for_timeout(5000)
        page.get_by_text(datadictvalue["C_ADD_SBTRCT"], exact=True).click()

        # Reference Date
        if datadictvalue["C_RFRNC_DATE"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_text("Reference Date").click()
            page.get_by_label("Reference Date").click()
            page.get_by_label("Reference Date").fill(datadictvalue["C_RFRNC_DATE"])

        # Balance Name
        if datadictvalue["C_BLNC_NAME"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_text("Balance Name").click()
            page.get_by_label("Balance Name").click()
            page.get_by_label("Balance Name").fill(datadictvalue["C_BLNC_NAME"])

        # Balance Dimension
        if datadictvalue["C_BLNC_DMNSN"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_text("Balance Dimension").click()
            page.get_by_label("Balance Dimension").click()
            page.get_by_label("Balance Dimension").fill(datadictvalue["C_BLNC_DMNSN"])

        # Rate Name
        if datadictvalue["C_RATE_NAME"] != "N/A":
            page.get_by_role("combobox", name="Rate Name").click()
            page.wait_for_timeout(5000)
            page.get_by_label("Rate Name").fill(datadictvalue["C_RATE_NAME"])

        # Periodicity
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Periodicity").click()
        page.get_by_text(datadictvalue["C_RD_PRDCTY"], exact=True).click()

        # Factor Rule
        if datadictvalue["C_RD_FCTR_RULE"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Factor Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RD_FCTR_RULE"], exact=True).click()

        # Factor Value
        if datadictvalue["C_RD_FCTR_VALUE"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_role("textbox", name="Factor Value").click()
            page.get_by_role("textbox", name="Factor Value").fill(str(datadictvalue["C_RD_FCTR_VALUE"]))

        # Criteria Value
        if datadictvalue["C_RD_CRTR_VALUE"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Criteria Value", exact=True).click()
            page.get_by_text(datadictvalue["C_RD_CRTR_VALUE"], exact=True).click()

        # Minimum Rate Rule
        if datadictvalue["C_RD_MNMM_RATE_RULE"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Minimum Rate Rule", exact=True).click()
            page.get_by_text(datadictvalue["C_RD_MNMM_RATE_RULE"], exact=True).click()

        # Minimum Value
        if datadictvalue["C_RD_MNMM_VALUE"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Minimum Value", exact=True).click()
            page.get_by_text(datadictvalue["C_RD_MNMM_VALUE"], exact=True).click()

        # Criteria Value
        if datadictvalue["C_RD_MNMM_CRTR_VALUE"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Criteria Value", exact=True).click()
            page.get_by_text(datadictvalue["C_RD_MNMM_CRTR_VALUE"], exact=True).click()

        # Limit Violation Action
        if datadictvalue["C_RD_MNMM_LIMIT_VLTN_ACTN"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Limit Violation Action", exact=True).click()
            page.get_by_text(datadictvalue["C_RD_MNMM_LIMIT_VLTN_ACTN"], exact=True).click()

        # C_MXMM_RATE_RULE
        if datadictvalue["C_RD_MXMM_RATE_RULE"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Maximum Rate Rule", exact=True).click()
            page.get_by_text(datadictvalue["C_RD_MXMM_RATE_RULE"], exact=True).click()

        # Maximum Value
        if datadictvalue["C_RD_MXMM_VALUE"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Maximum Value", exact=True).click()
            page.get_by_text(datadictvalue["C_RD_MXMM_VALUE"], exact=True).click()

        # Criteria Value
        if datadictvalue["C_RD_MXMM_CRTR_VALUE"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Criteria Value", exact=True).click()
            page.get_by_text(datadictvalue["C_RD_MXMM_CRTR_VALUE"], exact=True).click()

        # Limit Violation Action
        if datadictvalue["C_RD_MXMM_LIMIT_VLTN_ACTN"] != "N/A":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Limit Violation Action", exact=True).click()
            page.get_by_text(datadictvalue["C_RD_MXMM_LIMIT_VLTN_ACTN"], exact=True).click()

        # Return Full-Time Rate
        if datadictvalue["C_RD_RTRN_FULL_TIME"] != "N/A":
            if not page.get_by_text("Return Full-Time Rate").is_checked():
                page.get_by_text("Return Full-Time Rate").click()
                page.wait_for_timeout(3000)

        # Divisional Balance
        if datadictvalue["C_DVSNL_BLNC"] != "N/A":
            page.get_by_label("Divisional Balance").click()
            page.get_by_title("Search: Divisional Balance").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Name", exact=True).click()
            page.get_by_role("button", name="Search", exact=True).click()
            #page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(3000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DVSNL_BLNC"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            #page.get_by_role("cell", name="*pBalanceDimensionId", exact=True).locator("label").click()
            #page.get_by_label("pBalanceDimensionId").fill(str(datadictvalue["C_DVSNL_BLNC"]))
            #page.wait_for_timeout(3000)
            #page.get_by_role("button", name="Search", exact=True).click()

        # Save and Close
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Save and Continue", exact=True).click()

        # Submit
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Submit").click()
        # page.get_by_role("button", name="Yes").click()
        try:
            expect(page.get_by_role("heading", name="Rate Definitions")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Rate Definitions Created Successfully")
            datadictvalue["RowStatus"] = "Created Rate Definitions Successfully"
        except Exception as e:
            print("Unable to Save Rate Definitions")
            datadictvalue["RowStatus"] = "Unable to Save Rate Definitions"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, RATE_DEFINITION):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, RATE_DEFINITION,
                             PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK, RATE_DEFINITION)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[
            0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))