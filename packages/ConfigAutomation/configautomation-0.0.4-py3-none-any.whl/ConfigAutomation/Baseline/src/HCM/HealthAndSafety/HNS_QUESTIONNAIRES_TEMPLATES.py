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
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Questionnaire Templates")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Questionnaire Templates", exact=True).click()
    page.wait_for_timeout(2000)

    PrevHNSQTEMP = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        if datadictvalue["C_NAME"] != PrevHNSQTEMP:

            # Create Questionnaire Templates
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(5000)

            # Questionnaire Template ID
            # page.get_by_label("Questionnaire Template ID").click()
            # page.get_by_label("Questionnaire Template ID").clear()
            # page.get_by_label("Questionnaire Template ID").fill(datadictvalue["C_QSTNNR_TMPLT_ID"])

            # Score Questionnaire
            if datadictvalue["C_SCORE_QSTNNR"] == 'Yes':
                page.get_by_text("Score Questionnaire").check()
            if datadictvalue["C_SCORE_QSTNNR"] == 'No' or '':
                page.get_by_text("Score Questionnaire").uncheck()

            # Name
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])

            # Subscriber
            page.get_by_role("combobox", name="Subscriber").click()
            page.get_by_text(datadictvalue["C_SBSCRBR"]).click()

            # Status
            page.get_by_role("combobox", name="Status").click()
            page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

            # Privacy
            page.get_by_role("combobox", name="Privacy").click()
            page.get_by_text(datadictvalue["C_PRVCY"], exact=True).click()

            # Description
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

            # Allow Changes to instructions
            if datadictvalue["C_ALLOW_CHNGS_TO_INSTRCTNS"] == 'Yes':
                page.get_by_text("Allow changes to instructions").check()
            if datadictvalue["C_ALLOW_CHNGS_TO_INSTRCTNS"] == 'No' or '':
                page.get_by_text("Allow changes to instructions").uncheck()

            # Next Page
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(3000)

            # Score Questionnaire
            if datadictvalue["C_SCORE_QSTNNR_CNTNTS"] == "Yes":
                page.get_by_text("Score Questionnaire").check()
            if datadictvalue["C_SCORE_QSTNNR_CNTNTS"] == "No":
                page.get_by_text("Score Questionnaire").uncheck()

            # Section Order
            page.get_by_role("combobox", name="Section Order").click()
            page.get_by_text(datadictvalue["C_SCTN_ORDER"], exact=True).click()

            # Section Presentation
            page.get_by_role("combobox", name="Section Presentation").click()
            page.get_by_text(datadictvalue["C_SCTN_PRSNTTN"], exact=True).click()

            # Allow Changes to format options
            if datadictvalue["C_ALLOW_CHNGS_TO_FRMT_OPTNS"] == 'Yes':
                page.get_by_text("Allow changes to format").click()

            if datadictvalue["C_ALLOW_CHNGS_TO_FRMT_OPTNS"] == 'No' or '':
                page.get_by_text("Allow changes to format").click()

            # Allow changes to sections
            if datadictvalue["C_ALLOW_CHNGS_TO_SCTNS"] == 'Yes':
                page.get_by_text("Allow changes to sections").check()
            if datadictvalue["C_ALLOW_CHNGS_TO_SCTNS"] == 'No' or '':
                page.get_by_text("Allow changes to sections").uncheck()

            # Allowed Response type
            page.get_by_label("Allowed Response Types").click()
            if datadictvalue["C_ALLWD_RSPNS_TYPES"] == 'Yes':
                if datadictvalue["C_ALLWD_RSPNS_TYPES"] == 'All':
                    page.get_by_label("All", exact=True).check()
            if datadictvalue["C_ALLWD_RSPNS_TYPES"] == 'No' or '':
                page.get_by_label("All", exact=True).uncheck()

            # Allow Additional Questions
            if datadictvalue["C_ALLOW_ADDTNL_QSTNS"] == 'Yes':
                page.locator(
                    "//span[text()='" + str(datadictvalue["C_TITLE"]) + "']//following::label[1]").first.check()

            # Question Order
            page.locator("//span[text()='" + str(datadictvalue[
                                                     "C_TITLE"]) + "']//following::input[@role='combobox'][1]").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_QSTN_ORDER"]).click()

            # Response Order
            page.locator("//span[text()='" + str(datadictvalue[
                                                     "C_TITLE"]) + "']//following::input[@role='combobox'][2]").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RSPNS_ORDER"]).click()

            # Required checkbox
            if datadictvalue["C_RQRD"] == 'Yes':
                page.locator(
                    "//span[text()='" + str(datadictvalue["C_TITLE"]) + "']//following::label[4]").first.check()
            if datadictvalue["C_RQRD"] == 'No' or '':
                page.locator(
                    "//span[text()='" + str(datadictvalue["C_TITLE"]) + "']//following::label[4]").first.uncheck()

            page.wait_for_timeout(2000)

            PrevHNSQTEMP = datadictvalue["C_NAME"]

        # Add Questions
        page.get_by_role("button", name="Add").click()
        page.get_by_label("Keywords").clear()
        page.wait_for_timeout(1000)
        page.get_by_label("Keywords").fill(datadictvalue["C_QSTN_TEXT"])
        page.get_by_label("Folder").clear()
        page.wait_for_timeout(1000)
        page.get_by_label("Folder").fill(datadictvalue["C_FLDR"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(1000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FLDR"]).click()

        # page.get_by_text(datadictvalue["C_QUSTN_TEXT"]).click()

        page.wait_for_timeout(1000)
        page.get_by_role("button", name="OK").click()

        i = i + 1

    # Next Page
    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(2000)
    # Click on Save and Close
    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="OK").click()

    try:
        expect(page.get_by_role("heading", name="Questionnaire Templates")).to_be_visible()
        print("Questionnaire Templates Saved Successfully")
        datadictvalue["RowStatus"] = "Added Questionnaire Templates"
    except Exception as e:
        print("Unable to save Questionnaire Templates")
        datadictvalue["RowStatus"] = "Unable to Add Questionnaire Templates"

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HEAL_SAF_CONFIG_WRKBK, QUESTIONNAIRES_TEMPLATES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HEAL_SAF_CONFIG_WRKBK, QUESTIONNAIRES_TEMPLATES,
                             PRCS_DIR_PATH + HEAL_SAF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HEAL_SAF_CONFIG_WRKBK, QUESTIONNAIRES_TEMPLATES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", HEAL_SAF_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", HEAL_SAF_CONFIG_WRKBK)[
            0] + "_" + QUESTIONNAIRES_TEMPLATES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
