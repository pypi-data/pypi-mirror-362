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
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Coverages", exact=True).click()


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        if datadictvalue["C_PLAN"] != "":
            page.get_by_label("Coverage Name").click()
            page.get_by_label("Coverage Name").clear()
            page.wait_for_timeout(1000)
            page.get_by_label("Coverage Name").type(datadictvalue["C_NAME"])
            page.get_by_label("Plan Name").click()
            page.get_by_label("Plan Name").clear()
            page.wait_for_timeout(1000)
            page.get_by_label("Plan Name").type(datadictvalue["C_PLAN"])
            page.get_by_placeholder("mm-dd-yyyy").first.click()
            page.get_by_placeholder("mm-dd-yyyy").clear()
            page.wait_for_timeout(1000)
            page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_EFFCTV_DATE"])
            page.wait_for_timeout(5000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(5000)

            if page.get_by_role("link", name=datadictvalue["C_NAME"]).is_visible():
                page.get_by_role("link", name=datadictvalue["C_NAME"]).click()
                page.wait_for_timeout(5000)

                if datadictvalue["C_VRBL_CVRG_PROFILE"] != '':
                    page.get_by_role("link", name="Variable Profiles").click()
                    page.get_by_role("button", name="Select and Add").click()
                    page.get_by_label("Sequence").type(str(datadictvalue["C_SQNC"]))
                    page.get_by_title("Profile Name").click()
                    page.get_by_role("link", name="Search...").click()
                    page.get_by_label("Variable Coverage Profile Name").clear()
                    page.get_by_label("Variable Coverage Profile Name").type(datadictvalue["C_VRBL_CVRG_PROFILE"])
                    page.get_by_role("button", name="Search", exact=True).click()
                    page.wait_for_timeout(3000)
                    page.locator("//span[text()='" + datadictvalue["C_VRBL_CVRG_PROFILE"] + "'][1]").nth(1).click()
                    page.get_by_role("button", name="OK").nth(1).click()
                    page.wait_for_timeout(5000)
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(3000)

                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(2000)


            else:
                page.get_by_role("button", name="Create").click()
                page.wait_for_timeout(3000)

                # Session Effective Date
                page.get_by_placeholder("mm-dd-yyyy").clear()
                page.get_by_placeholder("mm-dd-yyyy").type(datadictvalue["C_EFFCTV_DATE"])

                # Coverage Name
                page.get_by_label("Coverage Name").click()
                page.wait_for_timeout(4000)
                if page.get_by_role("button", name="Yes").is_visible():
                    page.get_by_role("button", name="Yes").click()
                    page.wait_for_timeout(2000)
                page.get_by_label("Coverage Name").type(datadictvalue["C_NAME"])

                # Plan Name
                page.get_by_title("Plan Name").click()
                page.wait_for_timeout(2000)
                page.get_by_role("link", name="Search...").click()
                page.get_by_role("textbox", name="Plan Name").type(datadictvalue["C_PLAN"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.wait_for_timeout(3000)
                page.get_by_text(datadictvalue["C_PLAN"]).click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)

                # Option
                if datadictvalue["C_OPTION"]!='':
                    page.get_by_title("Option").click()
                    page.get_by_role("link", name="More...").click()
                    page.wait_for_timeout(3000)
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OPTION"],exact=True).click()
                    page.get_by_role("button", name="OK").click()

                # Type
                if datadictvalue["C_TYPE"] != '':
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Type").click()
                    page.get_by_text(datadictvalue["C_TYPE"], exact=True).click()

                # Unit of Measure
                if datadictvalue["C_UNIT_MSR"] != '':
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Unit of Measure").click()
                    page.get_by_text(datadictvalue["C_UNIT_MSR"], exact=True).click()

                # Calculation Method
                if datadictvalue["C_CLCLTN_METHOD"] == 'Flat amount':
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Determination Rule").click()
                    page.get_by_text(datadictvalue["C_CLCLTN_METHOD"], exact=True).click()

                    # Participants enter value during enrollment
                    if datadictvalue["C_PRTCPNT_ENTERS_VALUE"]=='Yes':
                        page.get_by_text("Participants enter value during enrollment", exact=True).click()

                        # Minimum
                        page.get_by_label("Minimum",exact=True).clear()
                        page.get_by_label("Minimum",exact=True).type(str(datadictvalue["C_MNMM"]))

                        # Maximum
                        page.get_by_label("Maximum", exact=True).clear()
                        page.get_by_label("Maximum", exact=True).type(str(datadictvalue["C_MXMM"]))

                        # Increment Amount
                        page.get_by_label("Increment Amount", exact=True).clear()
                        page.get_by_label("Increment Amount", exact=True).type(str(datadictvalue["C_INCRMNT"]))

                        # Default Value
                        page.get_by_label("Default Value", exact=True).clear()
                        page.get_by_label("Default Value", exact=True).type(str(datadictvalue["C_DEFAULT_VALUE"]))

                    if datadictvalue["C_PRTCPNT_ENTERS_VALUE"] == 'No':
                        page.get_by_label("Flat Amount",exact=True).clear()
                        page.get_by_label("Flat Amount",exact=True).type(str(datadictvalue["C_FLAT_AMOUNT"]))

                if datadictvalue["C_CLCLTN_METHOD"] == 'Flat range':
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Determination Rule").click()
                    page.get_by_text(datadictvalue["C_CLCLTN_METHOD"], exact=True).click()

                    # Minimum
                    page.get_by_label("Minimum",exact=True).clear()
                    page.get_by_label("Minimum",exact=True).type(str(datadictvalue["C_MNMM"]))

                    # Maximum
                    page.get_by_label("Maximum", exact=True).clear()
                    page.get_by_label("Maximum", exact=True).type(str(datadictvalue["C_MXMM"]))

                    # Increment Amount
                    page.get_by_label("Increment Amount",exact=True).clear()
                    page.get_by_label("Increment Amount",exact=True).type(str(datadictvalue["C_INCRMNT"]))

                    # Default Value
                    page.get_by_label("Default Value",exact=True).clear()
                    page.get_by_label("Default Value",exact=True).type(str(datadictvalue["C_DEFAULT_VALUE"]))

                if datadictvalue["C_CLCLTN_METHOD"] == 'Multiple of compensation':
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Determination Rule").click()
                    page.get_by_text(datadictvalue["C_CLCLTN_METHOD"], exact=True).click()

                    # Multiplier
                    page.get_by_label("Multiplier",exact=True).clear()
                    page.get_by_label("Multiplier",exact=True).type(str(datadictvalue["C_MLTPLR"]))

                    # Compensation Factor
                    if datadictvalue["C_CMPNSTN_FACTOR"] != '':
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Compensation Factor").click()
                        page.get_by_text(datadictvalue["C_CMPNSTN_FACTOR"], exact=True).click()

                    # Operator
                    if datadictvalue["C_OPRTR"] != '':
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Operator").click()
                        page.get_by_text(datadictvalue["C_OPRTR"], exact=True).click()

                if datadictvalue["C_HIGH_LIMIT"] != "":
                    page.get_by_label("High Limit Value", exact=True).click()
                    page.get_by_label("High Limit Value", exact=True).type(str(datadictvalue["C_HIGH_LIMIT"]))

                # page.get_by_role("button", name="Save", exact=True).click()
                # page.wait_for_timeout(5000)

                if datadictvalue["C_VRBL_CVRG_PROFILE"] != '':
                    page.get_by_role("link", name="Variable Profiles").click()
                    page.get_by_role("button", name="Select and Add").click()
                    page.get_by_label("Sequence").type(str(datadictvalue["C_SQNC"]))
                    page.get_by_label("Profile Name").click()
                    page.get_by_label("Profile Name").clear()
                    page.wait_for_timeout(1000)
                    page.get_by_label("Profile Name").type(datadictvalue["C_VRBL_CVRG_PROFILE"])
                    page.wait_for_timeout(2000)
                    # page.get_by_role("link", name="Search...").click()
                    # page.get_by_label("Variable Coverage Profile Name").clear()
                    # page.get_by_label("Variable Coverage Profile Name").type(datadictvalue["C_VRBL_CVRG_PROFILE"])
                    # page.get_by_role("button", name="Search", exact=True).click()
                    #page.wait_for_timeout(3000)
                    # page.get_by_label("Variable Coverage Profile Name").click()
                    # #page.locator("tbody").filter(has_text=re.compile(r"^{datadictvalue['C_VRBL_CVRG_PROFILE']}")).get_by_role("cell").click()
                    # page.wait_for_timeout(2000)
                    # page.locator("//span[text()='"+datadictvalue["C_VRBL_CVRG_PROFILE"]+"']").nth(2).click()
                    # page.get_by_role("button", name="OK").nth(1).click()
                    # page.wait_for_timeout(5000)
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(7000)

                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(2000)

        try:
            expect(page.get_by_role("heading", name="Overview")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Benefit Coverages Created Successfully")
            datadictvalue["RowStatus"] = "Created Benefit Coverages Successfully"
        except Exception as e:
            print("Unable to Save Benefit Coverages")
            datadictvalue["RowStatus"] = "Unable to Save Benefit Coverages"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_COVERAGE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_COVERAGE,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_COVERAGE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_COVERAGE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[
            0] + "_" + BENEFIT_COVERAGE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))











