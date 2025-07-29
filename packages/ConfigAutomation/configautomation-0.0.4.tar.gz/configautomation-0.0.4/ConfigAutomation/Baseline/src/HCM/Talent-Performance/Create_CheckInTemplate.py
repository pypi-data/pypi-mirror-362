from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("My Client Groups", exact=True).click()
    page.get_by_role("link", name="Performance").click()
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Check-In Templates").click()
    page.wait_for_timeout(5000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(10000)

        # Click on Add Button
        page.get_by_label("Add").click()
        page.wait_for_timeout(15000)

        # # Template Type
        # page.get_by_role("combobox", name="Template Type").click()
        # page.wait_for_timeout(3000)
        # page.get_by_role("gridcell", name=datadictvalue["C_CIT_TETY"], exact=True).click()

        # Name
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(1000)

        # Comments
        page.get_by_label("Comments").click()
        page.get_by_label("Comments").fill(datadictvalue["C_CMMNTS"])
        page.wait_for_timeout(1000)

        # Status
        page.get_by_role("combobox", name="Status").click()
        page.wait_for_timeout(3000)
        page.get_by_role("gridcell", name=datadictvalue["C_STTS"], exact=True).click()

        # From Date
        page.get_by_text("From Date").click()
        page.get_by_label("From Date").fill(datadictvalue["C_FROM_DATE"])
        page.wait_for_timeout(1000)

        # To Date
        page.get_by_text("To Date").click()
        page.get_by_label("To Date").fill(datadictvalue["C_TO_DATE"])
        page.wait_for_timeout(1000)

        # Review Period
        page.get_by_role("combobox", name="Review Period", exact=True).click()
        page.wait_for_timeout(3000)
        page.get_by_role("gridcell", name="Specific Review Periods", exact=True).click()

        # Select Review Periods
        page.get_by_text("Select Review Periods").click()
        page.wait_for_timeout(3000)
        page.get_by_role("option", name=datadictvalue["C_RVW_PRD"], exact=True).click()

        # Include in performance document
        if datadictvalue["C_INCLD_IN_PRFRMNC_DCMNT"] == "Yes":
            if not page.get_by_text("Include in performance document").is_checked():
                page.get_by_text("Include in performance document").click()
                page.wait_for_timeout(1000)

        # # Check-in content
        # Performance goals
        if datadictvalue["C_PRFRMNC_GOALS"] == "Yes":
            if not page.get_by_text("Performance goals").is_checked():
                page.get_by_text("Performance goals").click()
                page.wait_for_timeout(1000)
                if datadictvalue["C_ADD_DFLT_DSCSSN_TPCS_FOR_PRFRMNC_GOALS"] == "Yes":
                    if not page.get_by_text("Add default discussion topics for performance goals").is_checked():
                        page.get_by_text("Add default discussion topics for performance goals").click()
                        page.wait_for_timeout(1000)

        # Development goals
        if datadictvalue["C_DVLPMNT_GOALS"] == "Yes":
            if not page.get_by_text("Development goals").is_checked():
                page.get_by_text("Development goals").click()
                page.wait_for_timeout(1000)
                if datadictvalue["C_ADD_DFLT_DSCSSN_TPCS_FOR_DVLPMNT_GOALS"] == "Yes":
                    if not page.get_by_text("Add default discussion topics for development goals").is_checked():
                        page.get_by_text("Add default discussion topics for development goals").click()
                        page.wait_for_timeout(1000)

        # Questionnaire
        if datadictvalue["C_QSTNNR"] == "Yes":
            if not page.get_by_text("Questionnaire").is_checked():
                page.get_by_text("Questionnaire").click()
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Questionnaire for worker role", exact=True).click()
                page.wait_for_timeout(1000)
                page.get_by_role("gridcell", name=datadictvalue["C_QSTNNR_FOR_WRKR_ROLE"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Questionnaire for manager role", exact=True).click()
                page.wait_for_timeout(1000)
                page.get_by_role("gridcell", name=datadictvalue["C_QSTNNR_FOR_MNGR_ROLE"], exact=True).click()

        # General discussion topics
        if datadictvalue["C_GNRL_DSCSSN_TPCS"] == "Yes":
            if not page.get_by_text("General discussion topics").is_checked():
                page.get_by_text("General discussion topics").click()
                page.wait_for_timeout(3000)

        # # Anytime Feedback
        # if datadictvalue["C_CIT_AF"] != "Yes":
        #     if not page.get_by_text("Anytime Feedback").is_checked():
        #         page.get_by_text("Anytime Feedback").click()
        #         page.wait_for_timeout(3000)
        #
        # # Requested Feedback
        # if datadictvalue["C_CIT_RF"] != "Yes":
        #     if not page.get_by_text("Requested Feedback").is_checked():
        #         page.get_by_text("Requested Feedback").click()
        #         page.wait_for_timeout(3000)

        # # Eligibility profiles

        # Add Eligibility Profile
        page.get_by_label("Add Eligibility Profile").click()
        page.wait_for_timeout(3000)
        if datadictvalue["C_ELGBLTY_PRFL"] != '':
            page.get_by_role("combobox", name="Eligibility profiles").click()
            page.get_by_role("combobox", name="Eligibility profiles").type(datadictvalue["C_ELGBLTY_PRFL"])
            page.get_by_role("combobox", name="Eligibility profiles").press("Tab")
            page.wait_for_timeout(5000)
        if datadictvalue["C_RQRD"] =='Yes':
            page.get_by_label("Required").get_by_label("").check()
            page.wait_for_timeout(5000)

        # Submit the Record (SUBMIT)
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Submit").click()

        page.wait_for_timeout(3000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Check-in Template")).to_be_visible()
            print("Check-in Template Saved Successfully")
            datadictvalue["RowStatus"] = "Check-in Template Submitted Successfully"
        except Exception as e:
            print("Check-in Template not saved")
            datadictvalue["RowStatus"] = "Check-in Template not submitted"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, CHECK_IN_TEMPLATE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, CHECK_IN_TEMPLATE, PRCS_DIR_PATH + PERF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PERF_CONFIG_WRKBK, CHECK_IN_TEMPLATE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0] + "_" + CHECK_IN_TEMPLATE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
