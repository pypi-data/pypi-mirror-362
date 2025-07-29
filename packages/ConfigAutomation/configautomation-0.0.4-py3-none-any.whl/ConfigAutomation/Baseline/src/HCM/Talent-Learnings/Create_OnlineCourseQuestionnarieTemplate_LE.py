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

    PrevOLQuesTemplate=''

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        if datadictvalue["C_NAME"] != PrevOLQuesTemplate:

            # Clicking on Create button
            page.get_by_role("button", name="Create").click()

            # Select Subscriber
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Subscriber").click()
            page.get_by_text(datadictvalue["C_SBSCBR"]).click()

            # Score Questionary
            if datadictvalue["C_SCORE_QSTNNR"] != '':
                if datadictvalue["C_SCORE_QSTNNR"] == 'Yes':
                    page.get_by_text("Score Questionnaire").check()
                    # Overall Score Calculation Rule
                    page.wait_for_timeout(2000)
                    page.get_by_role("combobox", name="Overall Score Calculation Rule").click()
                    page.get_by_text(datadictvalue["C_OVRLL_SCORE_CLCLTN_RULE"]).click()

                # if datadictvalue["C_SCORE_QSTNNR"] == 'No':
                #     page.get_by_text("C_SCORE_QSTNNR").uncheck()

            # Name
            page.get_by_label("Name").clear()
            page.get_by_label("Name").type(datadictvalue["C_NAME"])

            # Status
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Status").click()
            page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

            # Privacy
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Privacy").click()
            page.get_by_text(datadictvalue["C_PRVCY"], exact=True).click()

            # Owner
            if datadictvalue["C_OWNER"]!='':
                page.get_by_label("Owner").click()
                page.get_by_label("Owner").type(datadictvalue["C_OWNER"])

            # Description
            if datadictvalue["C_DSCRPTN"]!='':
                page.get_by_label("Description").click()
                page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])

            # Allow changes to instructions
            if datadictvalue["C_ALLOW_CHNGS_TO_INSTRCTNS"]!='':
                if datadictvalue["C_ALLOW_CHNGS_TO_INSTRCTNS"] == 'Yes':
                    page.get_by_text("Allow changes to instructions").check()
                if datadictvalue["C_ALLOW_CHNGS_TO_INSTRCTNS"] == 'No':
                    page.get_by_text("Allow changes to instructions").uncheck()

            # Clicking on Next button
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(5000)

            # Section Order
            if datadictvalue["C_SCTN_ORDER"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Section Order").click()
                page.get_by_text(datadictvalue["C_SCTN_ORDER"], exact=True).click()

            # Section Presentation
            if datadictvalue["C_SCTN_PRSNTTN"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Section Presentation").click()
                page.get_by_text(datadictvalue["C_SCTN_PRSNTTN"], exact=True).click()

            page.wait_for_timeout(3000)

            # Allow changes to format options
            if datadictvalue["C_ALLOW_CHNGS_TO_FRMT_OPTNS"]!='':
                if datadictvalue["C_ALLOW_CHNGS_TO_FRMT_OPTNS"] == 'Yes':
                    page.get_by_text("Allow changes to format").check()
                if datadictvalue["C_ALLOW_CHNGS_TO_FRMT_OPTNS"] == 'No':
                    page.get_by_text("Allow changes to format").uncheck()

            # Allow changes to sections
            if datadictvalue["C_ALLOW_CHNGS_TO_SCTNS"]!='':
                if datadictvalue["C_ALLOW_CHNGS_TO_SCTNS"] == 'Yes':
                    page.get_by_text("Allow changes to sections").check()
                if datadictvalue["C_ALLOW_CHNGS_TO_SCTNS"] == 'No':
                    page.get_by_text("Allow changes to sections").uncheck()

            # Allow Response Types
            if datadictvalue["C_ALLWD_RSPNS_TYPES"]!='':
                page.get_by_label("Allowed Response Types").click()
                page.get_by_text(datadictvalue["C_ALLWD_RSPNS_TYPES"], exact=True).check()

            # Checking allow additional Question check box
            page.get_by_role("heading", name="Sections").click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_ALLOW_ADDTNL_QSTNS"] == 'Yes':
                page.locator("//div[@title='Sections']//following::label[1]").first.check()
            if datadictvalue["C_ALLOW_ADDTNL_QSTNS"] == 'No':
                page.locator("//div[@title='Sections']//following::label[1]").first.uncheck()

            # Question Order
            page.wait_for_timeout(2000)
            page.get_by_label("Question Order").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_QSTN_ORDER"]).click()

            # Response Order
            page.wait_for_timeout(2000)
            page.get_by_label("Response Order").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RSPNS_ORDER"]).click()

            # Required
            if datadictvalue["C_RQRD"] == 'Yes':
                page.locator("//div[@title='Sections']//following::label[4]").check()
            if datadictvalue["C_RQRD"] == 'No':
                page.locator("//div[@title='Sections']//following::label[4]").uncheck()

            page.wait_for_timeout(3000)

            PrevOLQuesTemplate = datadictvalue["C_NAME"]

        # Questions
        page.get_by_role("button", name="Add").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Keywords").clear()
        page.get_by_label("Keywords").type(datadictvalue["C_QSTN_TEXT"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.locator("//span[contains(text(),'"+datadictvalue["C_QSTN_TEXT"]+"')]").first.click(force=True)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)


        i = i + 1

        # Click on Save and Close
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="OK").click()

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
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, OLC_QUES_TEMPLATE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, OLC_QUES_TEMPLATE, PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK, OLC_QUES_TEMPLATE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[0] + "_" + OLC_QUES_TEMPLATE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

