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
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Benefit Rates").click()
    page.wait_for_timeout(1000)
    page.get_by_role("link", name="Rates and Coverages").click()
    page.wait_for_timeout(1000)
    page.get_by_role("link", name="Standard Rates").click()
    page.wait_for_timeout(1000)

    i = 0
    while i < rowcount:

        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)
        print(i)
        print(datadictvalue["C_RATE_NAME"])
        print(datadictvalue["C_PLAN_NAME"])
        page.get_by_role("link", name="Rates and Coverages").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Rate Name").click()
        page.get_by_label("Rate Name").type(datadictvalue["C_RATE_NAME"])
        page.get_by_label("Plan Name").click()
        page.get_by_label("Plan Name").type(datadictvalue["C_PLAN_NAME"])
        page.get_by_placeholder("mm-dd-yyyy").first.click()
        page.get_by_placeholder("mm-dd-yyyy").first.clear()
        page.get_by_placeholder("mm-dd-yyyy").first.fill(datadictvalue["C_EFFCTV_START_DATE"])
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(4000)

        if page.get_by_role("link", name=datadictvalue["C_RATE_NAME"]).is_visible():
            page.get_by_role("link", name=datadictvalue["C_RATE_NAME"]).click()
            print("Rate Name is visible")

            if page.get_by_text(datadictvalue["C_VRBL_RATES"]).is_visible():
                print("Variable Rates Already added")

            else:
                if datadictvalue["C_VRBL_RATES"] != '':
                    page.get_by_role("link", name="Variable Profile Name").click()
                    page.get_by_role("button", name="Select and Add").click()
                    page.get_by_role("combobox", name="Profile Name").click()
                    page.wait_for_timeout(1000)
                    page.get_by_role("combobox", name="Profile Name").clear()
                    page.get_by_role("combobox", name="Profile Name").type(datadictvalue["C_VRBL_RATES"])
                    # page.get_by_title("Profile Name").click()
                    # page.get_by_role("link", name="Search...").click()
                    # page.get_by_role("textbox", name="Profile Name").clear()
                    # page.get_by_role("textbox", name="Profile Name").type(datadictvalue["C_VRBL_RATES"])
                    # page.get_by_role("button", name="Search", exact=True).click()
                    # page.wait_for_timeout(3000)
                    # page.locator("//span[text()='"+datadictvalue["C_VRBL_RATES"]+"'][1]").nth(1).click()
                    # page.get_by_role("button", name="OK").nth(1).click()
                    page.wait_for_timeout(2000)
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(3000)

            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(4000)

        else:
            page.get_by_title("Create").click()
            # page.pause()
            page.get_by_text("Create Standard Rate").click()
            page.wait_for_timeout(6000)

            # Session Effective Date
            page.get_by_placeholder("mm-dd-yyyy").clear()
            page.get_by_placeholder("mm-dd-yyyy").type(datadictvalue["C_EFFCTV_START_DATE"])

            # Rate Name
            page.wait_for_timeout(4000)
            page.get_by_label("Rate Name").click()
            page.wait_for_timeout(3000)
            if page.get_by_role("button", name="Yes").is_visible():
                page.get_by_role("button", name="Yes").click()
            page.get_by_label("Rate Name",exact=True).click()
            page.get_by_label("Rate Name",exact=True).type(datadictvalue["C_RATE_NAME"])
            page.wait_for_timeout(2000)
            # Plan Name
            page.get_by_title("Plan Name").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Plan Name").type(datadictvalue["C_PLAN_NAME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_PLAN_NAME"],exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)
            # Option

            # page.get_by_role("combobox", name="Option").click()
            # page.get_by_text(datadictvalue["C_OPTION"], exact=True).click()
            if datadictvalue["C_OPTION"] != '':
                page.get_by_role("combobox", name="Option").click()
                page.get_by_text(datadictvalue["C_OPTION"], exact=True).click()

            # Restrict Rate on Program
            if datadictvalue["C_RSTRCT_ON_PRGRM"]!='':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Restrict Rate on Program").click()
                page.get_by_text(datadictvalue["C_RSTRCT_ON_PRGRM"], exact=True).click()

            # Status
            if datadictvalue["C_STATUS"]!='':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Status").click()
                page.get_by_text(datadictvalue["C_STATUS"], exact=True).click()

            # Legislative Data Group
            if datadictvalue["C_LEGAL_EMPLYR"]!='':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Legislative Data Group").click()
                page.get_by_text(datadictvalue["C_LEGAL_EMPLYR"], exact=True).click()

            # Rate Display Type
            if datadictvalue["C_RATE_DSPLY_TYPE"]!='':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Rate Display Type").click()
                page.get_by_text(datadictvalue["C_RATE_DSPLY_TYPE"], exact=True).click()

            # Short Name
            if datadictvalue["C_SHORT_NAME"]!='':
                page.get_by_label("Short Name").clear()
                page.get_by_label("Short Name").type(datadictvalue["C_SHORT_NAME"])

            # Short Code
            if datadictvalue["C_SHRT_CODE"] != '':
                page.get_by_label("Short Code").clear()
                page.get_by_label("Short Code").type(datadictvalue["C_SHRT_CODE"])

            # Activity Type
            if datadictvalue["C_ACTVTY_TYPE"]!='':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Activity Type").click()
                page.get_by_text(datadictvalue["C_ACTVTY_TYPE"], exact=True).click()

            # Tax Type Code
            if datadictvalue["C_TAX_TYPE_CODE"]!='':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Tax Type Code").click()
                page.get_by_text(datadictvalue["C_TAX_TYPE_CODE"], exact=True).click()

            # Unit of Measure
            if datadictvalue["C_UNIT_OF_MSR"]!='':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Unit of Measure").click()
                page.get_by_text(datadictvalue["C_UNIT_OF_MSR"], exact=True).click()

            # Parent or Child Rate Type
            if datadictvalue["C_PARENT_OR_CHILD_RATE_TYPE"]!='':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Parent or Child Rate Type").click()
                page.get_by_text(datadictvalue["C_PARENT_OR_CHILD_RATE_TYPE"], exact=True).click()

            # Payroll Element
            if datadictvalue["C_PYRLL_ELEMENT"]!='':
                page.wait_for_timeout(3000)
                page.get_by_title("Payroll Element").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_role("textbox", name="Element Name").type(datadictvalue["C_PYRLL_ELEMENT"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.wait_for_timeout(3000)
                page.get_by_text(datadictvalue["C_PYRLL_ELEMENT"], exact=True).first.click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)


                # page.get_by_role("combobox", name="Payroll Element").click()
                # page.get_by_role("combobox", name="Payroll Element").type(datadictvalue["C_PYRLL_ELEMENT"])
                #page.get_by_role("combobox", name="Payroll Element").press("Tab")
                #page.get_by_text(datadictvalue["C_PYRLL_ELEMENT"], exact=True).click()

            # Element Input Value
            if datadictvalue["C_ELMNT_INPUT_VALUE"]!='':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Element Input Value").click()
                page.get_by_text(datadictvalue["C_ELMNT_INPUT_VALUE"], exact=True).click()

            # Extra Input Formula
            if datadictvalue["C_EXTRA_INPUT_FRMLA"]!='':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Extra Input Formula").click()
                page.get_by_text(datadictvalue["C_EXTRA_INPUT_FRMLA"], exact=True).click()

            # Value Passed to Payroll
            if datadictvalue["C_VLUE_PSSD_TO_PYRLL"]!='':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Value Passed to Payroll").click()
                page.get_by_text(datadictvalue["C_VLUE_PSSD_TO_PYRLL"], exact=True).click()

            # Element and input values
            if datadictvalue["C_ELMNT_AND_INPUT_VALUES_RQRD"] != '':
                if datadictvalue["C_ELMNT_AND_INPUT_VALUES_RQRD"]=='Yes':
                    page.get_by_text("Element and input values").check()
                elif datadictvalue["C_ELMNT_AND_INPUT_VALUES_RQRD"]=='No':
                    page.get_by_text("Element and input values").uncheck()

            # Assign on enrollment
            if datadictvalue["C_ASSIGN_ON_ENRLLMNT"] != '':
                if datadictvalue["C_ASSIGN_ON_ENRLLMNT"]=='Yes':
                    page.get_by_text("Assign on enrollment").check()
                elif datadictvalue["C_ASSIGN_ON_ENRLLMNT"]=='No':
                    page.get_by_text("Assign on enrollment").uncheck()

            # Display on enrollment
            if datadictvalue["C_DSPLY_ON_ENRLLMNT"] != '':
                if datadictvalue["C_DSPLY_ON_ENRLLMNT"]=='Yes':
                    page.get_by_text("Display on enrollment").check()
                elif datadictvalue["C_DSPLY_ON_ENRLLMNT"]=='No':
                    page.get_by_text("Display on enrollment").uncheck()

            # Calculation Method
            if datadictvalue["C_CLCLTN_METHOD"] == "Flat amount":
                page.wait_for_timeout(3000)
                print("Calculation method")
                page.get_by_role("combobox", name="Calculation Method").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CLCLTN_METHOD"], exact=True).click()

                # Participants enter value during enrollment
                #if datadictvalue["C_PRTCPNTS_ENT_VALUE_DRNG_ENRLLMNT"] == 'Yes':
                    # page.get_by_text("Participants enter value during enrollment", exact=True).click()
                    # page.wait_for_timeout(3000)
                    #
                    # # Minimum Election Value
                    # page.get_by_label("Minimum Election Value", exact=True).clear()
                    # page.get_by_label("Minimum Election Value", exact=True).type(str(datadictvalue["C_MNM_ELCTN_VALUE"]))
                    #
                    # # Maximum Election Value
                    # page.get_by_label("Maximum Election Value", exact=True).clear()
                    # page.get_by_label("Maximum Election Value", exact=True).type(str(datadictvalue["C_MXMM_ELCTN_VALUE"]))
                    #
                    # # Increment
                    # page.get_by_label("Increment", exact=True).clear()
                    # page.get_by_label("Increment", exact=True).type(str(datadictvalue["C_INCRMNT"]))
                    #
                    # # Default
                    # page.get_by_label("Default", exact=True).clear()
                    # page.get_by_label("Default", exact=True).type(str(datadictvalue["C_DFLT"]))

                if datadictvalue["C_VALUE"] != '':
                    page.get_by_label("Value", exact=True).clear()
                    page.get_by_label("Value", exact=True).type(str(datadictvalue["C_VALUE"]))

            if datadictvalue["C_CLCLTN_METHOD"] == 'Set annual rate equal to coverage':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Calculation Method").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CLCLTN_METHOD"], exact=True).click()

            if datadictvalue["C_CLCLTN_METHOD"] == 'No standard values used':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Calculation Method").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CLCLTN_METHOD"], exact=True).click()

            if datadictvalue["C_CLCLTN_METHOD"] == 'Multiple of coverage':
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Calculation Method").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CLCLTN_METHOD"], exact=True).click()
                page.wait_for_timeout(2000)

                # Multiplier
                page.get_by_label("Multiplier",exact=True).clear()
                page.get_by_label("Multiplier",exact=True).type(str(datadictvalue["C_MLTPLER"]))

                # Operator
                if datadictvalue["C_OPRTR"] != '':
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Operator").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OPRTR"], exact=True).click()

                #PrevRateName = datadictvalue["C_NAME"]

            if datadictvalue["C_VRBL_RATES"]!='':

                page.get_by_role("link", name="Variable Profile Name").click()
                page.get_by_role("button", name="Select and Add").click()
                page.get_by_role("combobox", name="Profile Name").click()
                page.wait_for_timeout(1000)
                page.get_by_role("combobox", name="Profile Name").clear()
                page.get_by_role("combobox", name="Profile Name").type(datadictvalue["C_VRBL_RATES"])
                # page.get_by_title("Profile Name").click()
                # page.get_by_role("link", name="Search...").click()
                # page.get_by_role("textbox", name="Profile Name").clear()
                # page.get_by_role("textbox", name="Profile Name").type(datadictvalue["C_VRBL_RATES"])
                # page.get_by_role("button", name="Search", exact=True).click()
                # page.wait_for_timeout(3000)
                # page.locator("//span[text()='"+datadictvalue["C_VRBL_RATES"]+"'][1]").nth(1).click()
                # page.get_by_role("button", name="OK").nth(1).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)

            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(4000)

        try:
            expect(page.get_by_role("heading", name="Overview")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Standard Rates Created Successfully")
            datadictvalue["RowStatus"] = "Created Standard Rates Successfully"
        except Exception as e:
            print("Unable to Save Standard Rates")
            datadictvalue["RowStatus"] = "Unable to Save Standard Rates"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_RATES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_RATES, PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_RATES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_RATES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_RATES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))





