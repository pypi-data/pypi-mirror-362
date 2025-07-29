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

    # Navigate to Document Upload page
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Benefits Administration", exact=True).click()
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Benefit Rates").click()
    page.get_by_role("link", name="Rates and Coverages").click()
    page.get_by_role("link", name="Variable Rate Profiles").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)
        print(i)
        print(datadictvalue["C_PRFL_NAME"])

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)

        # Session Effective Date
        page.get_by_placeholder("mm-dd-yyyy").clear()
        page.get_by_placeholder("mm-dd-yyyy").type(datadictvalue["C_EFFCTV_START_DATE"])

        # Profile Name
        page.get_by_label("Profile Name").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Yes").click()
        page.get_by_label("Profile Name").type(datadictvalue["C_PRFL_NAME"])

        # Activity Type
        if datadictvalue["C_ACTVTY_TYPE"] != '':
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Activity Type").click()
            page.get_by_text(datadictvalue["C_ACTVTY_TYPE"], exact=True).click()

        # Defined Rate Frequency
        if datadictvalue["C_DFND_RATE_FRQNCY"]!='':
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Defined Rate Frequency").click()
            page.get_by_text(datadictvalue["C_DFND_RATE_FRQNCY"], exact=True).click()

        # Status
        if datadictvalue["C_STTS"]!='':
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Status").click()
            page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

        # Tax Type Rule
        if datadictvalue["C_TAX_TYPE_RULE"]!='':
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Tax Type Rule").click()
            page.get_by_text(datadictvalue["C_TAX_TYPE_RULE"], exact=True).click()

        # Treatment Rule
        if datadictvalue["C_TRMNT_RULE"]!='':
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Treatment Rule").click()
            page.get_by_text(datadictvalue["C_TRMNT_RULE"], exact=True).click()

        # Eligibility Profile
        if datadictvalue["C_ELGBLTY_PRFL"] != '':
            # page.pause()
            page.get_by_title("Search: Eligibility Profile").click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Name", exact=True).type(datadictvalue["C_ELGBLTY_PRFL"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            # page.get_by_text(datadictvalue["C_ELGBLTY_PRFL"]).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ELGBLTY_PRFL"]).click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="OK").click()
            # page.pause()
            page.wait_for_timeout(3000)


        # Calculation Method
        if datadictvalue["C_CLTN_MTD"] == 'Flat amount':
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Calculation Method").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CLTN_MTD"], exact=True).click()

            # Participants enter value during enrollment
            if datadictvalue["C_PRTCPNTS_ENT_VALUE_DRNG_ENRLLMNT"] == 'Yes':
                page.get_by_text("Participants enter value during enrollment", exact=True).click()
                page.wait_for_timeout(3000)

                # Minimum Election Value
                page.get_by_label("Minimum Election Value", exact=True).clear()
                page.get_by_label("Minimum Election Value", exact=True).type(str(datadictvalue["C_MNM_ELCTN_VALUE"]))

                # Maximum Election Value
                page.get_by_label("Maximum Election Value", exact=True).clear()
                page.get_by_label("Maximum Election Value", exact=True).type(str(datadictvalue["C_MXMM_ELCTN_VALUE"]))

                # Increment
                page.get_by_label("Increment", exact=True).clear()
                page.get_by_label("Increment", exact=True).type(str(datadictvalue["C_INCRMNT"]))

                # Default
                page.get_by_label("Default", exact=True).clear()
                page.get_by_label("Default", exact=True).type(str(datadictvalue["C_DFLT"]))

            if datadictvalue["C_PRTCPNTS_ENT_VALUE_DRNG_ENRLLMNT"] == 'No':
                page.get_by_label("Value", exact=True).clear()
                page.get_by_label("Value", exact=True).click()
                page.get_by_label("Value", exact=True).type(str(datadictvalue["C_VALUE"]))

            # Annual Values
            if datadictvalue["C_ANNL_MINMM_ELCTN_VALUE"]!='':
                page.get_by_label("Annual Minimum Election Value").clear()
                page.get_by_label("Annual Minimum Election Value").type(datadictvalue["C_ANNL_MINMM_ELCTN_VALUE"])
            if datadictvalue["C_ANNL_MXMM_ELCTN_VALUE"]!='':
                page.get_by_label("Annual Maximum Election Value").clear()
                page.get_by_label("Annual Maximum Election Value").type(datadictvalue["C_ANNL_MXMM_ELCTN_VALUE"])

        if datadictvalue["C_CLTN_MTD"] == "Multiple of coverage":
            # page.pause()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Calculation Method").click()
            page.get_by_text(datadictvalue["C_CLTN_MTD"], exact=True).click()
            page.wait_for_timeout(2000)

            # Multiplier
            page.get_by_label("Multiplier",exact=True).clear()
            page.get_by_label("Multiplier",exact=True).type(str(datadictvalue["C_MLTPLER"]))

            # Coverage Operator
            if datadictvalue["C_CVRGE_NAME"] != '':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Coverage Operator").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CVRGE_NAME"], exact=True).click()

            # Limits
            if datadictvalue["C_LOW_LIMIT_VALUE"] != '':
                page.get_by_label("Low Limit Value", exact=True).clear()
                page.get_by_label("Low Limit Value", exact=True).type(datadictvalue["C_LOW_LIMIT_VALUE"])
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Low Limit Value Formula").click()
                page.get_by_text(datadictvalue["C_LOW_LMT_VALUE_FRML"], exact=True).click()

            if datadictvalue["C_UPPER_LIMIT_VALUE"] != '':
                page.get_by_label("Upper Limit Value").clear()
                page.get_by_label("Upper Limit Value").type(datadictvalue["C_UPPER_LIMIT_VALUE"])
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Upper Limit Value Formula").click()
                page.get_by_text(datadictvalue["C_UPPER_LIMIT_VALUE_FRML"], exact=True).click()

        # Rounding Rule
        if datadictvalue["C_RNDNG_RULE"] != '':
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Rounding Rule").click()
            page.get_by_text(datadictvalue["C_RNDNG_RULE"], exact=True).click()

        if datadictvalue["C_RNDNG_FRML"] != '':
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Rounding Formula").click()
            page.get_by_text(datadictvalue["C_RNDNG_FRML"], exact=True).click()

        # Ultimate Calculated Limits
        if datadictvalue["C_ULT_LOW_LMT_VALUE"] != '':
            page.get_by_label("Ultimate Low Limit Value", exact=True).clear()
            page.get_by_label("Ultimate Low Limit Value", exact=True).type(datadictvalue["C_ULT_LOW_LMT_VALUE"])
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Ultimate Low Limit Value Formula").click()
            page.get_by_text(datadictvalue["C_ULTMT_LOW_LIMIT_VALUE_FRML"], exact=True).click()

        if datadictvalue["C_ULTMT_HIGH_LIMIT_VALUE"] != '':
            page.get_by_label("Ultimate High Upper Limit Value", exact=True).clear()
            page.get_by_label("Ultimate High Upper Limit Value", exact=True).type(
                datadictvalue["C_ULTMT_HIGH_LIMIT_VALUE"])
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Ultimate High Limit Value Formula").click()
            page.get_by_text(datadictvalue["C_ULTMT_HIGH_LIMIT_VALUE_FRML"], exact=True).click()

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)

        try:
            expect(page.get_by_role("heading", name="Overview")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Benefit Variable Coverages Created Successfully")
            datadictvalue["RowStatus"] = "Created Benefit Variable Coverages Successfully"
        except Exception as e:
            print("Unable to Save Benefit Variable Coverages")
            datadictvalue["RowStatus"] = "Unable to Save Benefit Variable Coverages"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, VARIABLE_RATE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, VARIABLE_RATE,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, VARIABLE_RATE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + VARIABLE_RATE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + VARIABLE_RATE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
