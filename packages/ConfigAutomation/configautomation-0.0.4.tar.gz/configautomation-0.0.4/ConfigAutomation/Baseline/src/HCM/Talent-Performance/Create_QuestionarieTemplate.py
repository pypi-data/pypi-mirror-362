from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("My Client Groups", exact=True).click()
    page.get_by_role("link", name="Performance").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Questionnaire Templates").click()
    page.wait_for_timeout(3000)

    PrevQuesTemplate = ''

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        if datadictvalue["C_NAME"] != PrevQuesTemplate:
            if i > 0:
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)
                # Added line 28 - 32 for Setonhill project testing

            # Clicking on Create button
            page.get_by_role("button", name="Create").first.click()
            page.wait_for_timeout(3000)

            # Select Subscriber
            page.get_by_role("combobox", name="Subscriber").click()
            page.get_by_text(datadictvalue["C_SBCRBR"]).click()
            page.wait_for_timeout(3000)

            # Score Questionary
            if datadictvalue["C_SCORE_QSTNNR"] != '':
                if datadictvalue["C_SCORE_QSTNNR"] == "No":
                    page.get_by_text("Score Questionnaire").uncheck()
                if datadictvalue["C_SCORE_QSTNNR"] == "Yes":
                    page.get_by_text("C_SCORE_QSTNNR").check()
                    page.wait_for_timeout(3000)
            # Overall Score Calculation Rule
                    if datadictvalue["C_OVRLL_SCORE_CLCLTN_RULE"] != '' or "N/A":
                        page.get_by_role("combobox", name="Overall Score Calculation Rule").click()
                        page.get_by_text(datadictvalue["C_OVRLL_SCORE_CLCLTN_RULE"]).click()
                        page.wait_for_timeout(3000)
            # Name
            page.get_by_label("Name").clear()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.wait_for_timeout(3000)

            # Status
            page.get_by_role("combobox", name="Status").click()
            page.get_by_text(datadictvalue["C_STTS"], exact=True).click()
            page.wait_for_timeout(3000)

            # Privacy
            page.get_by_role("combobox", name="Privacy").click()
            page.get_by_text(datadictvalue["C_PRVCY"], exact=True).click()
            page.wait_for_timeout(3000)

            # Owner
            if datadictvalue["C_OWNER"] != '':
                page.get_by_label("Owner").click()
                page.get_by_label("Owner").fill(datadictvalue["C_QSTN_OWNR"])
                page.wait_for_timeout(3000)

            # Description
            if datadictvalue["C_DSCRPTN"] != '':
                page.get_by_label("Description").click()
                page.get_by_label("Description").fill(str(datadictvalue["C_DSCRPTN"]))
                page.wait_for_timeout(2000)

            # Allow changes to instructions
            if datadictvalue["C_ALLOW_CHNGS_TO_INSTRCTNS"] != '':
                if datadictvalue["C_ALLOW_CHNGS_TO_INSTRCTNS"] == 'Yes':
                    page.get_by_text("Allow changes to instructions").check()
                    page.wait_for_timeout(2000)
                if datadictvalue["C_ALLOW_CHNGS_TO_INSTRCTNS"] == 'No':
                    page.get_by_text("Allow changes to instructions").uncheck()
                    page.wait_for_timeout(2000)

            # Clicking on Next button
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(5000)

            # Checking allow additional Question check box
            if datadictvalue["C_ALLOW_ADDTNL_QSTNS"] == 'Yes':
                page.get_by_role("cell", name="1 Vertical Question Order").locator("label").first.check()
                page.wait_for_timeout(2000)
            if datadictvalue["C_ALLOW_ADDTNL_QSTNS"] == 'No':
                page.get_by_role("cell", name="1 Vertical Question Order").locator("label").first.uncheck()
                page.wait_for_timeout(2000)

            # Question Order
            if datadictvalue["C_QSTN_ORDER"] != '' or "N/A":
                page.get_by_label("Question Order").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_QSTN_ORDER"]).click()
                page.wait_for_timeout(2000)

            # Response Order
            if datadictvalue["C_RSPNS_ORDER"] != '' or "N/A":
                page.get_by_label("Response Order").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RSPNS_ORDER"]).click()
                page.wait_for_timeout(2000)

            # Required
            if datadictvalue["C_RQRD"] == 'Yes':
                page.get_by_role("cell", name="1 Vertical Question Order").locator("label").nth(3).check()
                page.wait_for_timeout(2000)
            if datadictvalue["C_RQRD"] == 'No':
                page.get_by_role("cell", name="1 Vertical Question Order").locator("label").nth(3).uncheck()
                page.wait_for_timeout(2000)

            page.wait_for_timeout(3000)
            PrevQuesTemplate = datadictvalue["C_NAME"]

        # Questions
        page.get_by_role("button", name="Add").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Keywords").clear()
        page.get_by_label("Keywords").fill(datadictvalue["C_QSTN_TEXT"])
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_text(str(datadictvalue["C_QSTN_TEXT"])).first.click()
        # page.locator("//span[contains(text(),'"+datadictvalue["C_QSTN_TEXT"]+"')]").first.click(force=True)
        # Commented line 136 for Setonhill project testing
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"
        page.wait_for_timeout(2000)

        i = i + 1

    # Click on Save and Close
    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="OK").click()
    page.wait_for_timeout(2000)

    try:
        expect(page.get_by_role("heading", name="Questionnaire Templates")).to_be_visible()
        print("Questionnarie Templates Saved Successfully")
        datadictvalue["RowStatus"] = "Questionnarie Templates Saved Successfully"
    except Exception as e:
        print("Questionnarie Templates not saved")
        datadictvalue["RowStatus"] = "Questionnarie Templates not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, QUES_TEMPLATES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, QUES_TEMPLATES, PRCS_DIR_PATH + PERF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PERF_CONFIG_WRKBK, QUES_TEMPLATES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0] + "_" + QUES_TEMPLATES +
                     "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
