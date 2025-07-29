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
    page.get_by_role("link", name="Questionnaires").click()
    page.wait_for_timeout(3000)

    PrevLAQuestionarie=''

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        if datadictvalue["C_QSTNNR_LBBRY"] != PrevLAQuestionarie:

            # Subscriber
            page.wait_for_timeout(5000)
            page.get_by_role("combobox", name="Subscriber").click()
            page.get_by_text(datadictvalue["C_SBCRBR"],exact=True).click()
            page.wait_for_timeout(3000)


            # Click on Create Folder button
            page.get_by_role("cell", name="Expand Questionnaire Library").locator("span").nth(1).click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Create").first.click()
            page.get_by_role("textbox", name="Folder").type(datadictvalue["C_QSTNNR_LBBRY"])
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_QSTNNR_LBBRY"], exact=True).click(force=True)
            page.wait_for_timeout(5000)

            PrevLAQuestionarie = datadictvalue["C_QSTNNR_LBBRY"]

        #Clicking on Questionnarie create button
        page.locator("a").filter(has_text="Create").click()
        page.wait_for_timeout(3000)

        # Questionnarie Template Name
        page.get_by_label("Name").clear()
        page.get_by_label("Name").type(datadictvalue["C_NAME"])
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.get_by_text(datadictvalue["C_NAME"]).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # Questionnarie Name
        page.get_by_label("Name").clear()
        page.wait_for_timeout(2000)
        page.get_by_label("Name").type(datadictvalue["C_NAME_ONE"])

        # Status
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Status").click()
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

        # Privacy
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Privacy").click()
        page.get_by_text(datadictvalue["C_PRVCY"], exact=True).click()

        # Owner Name
        if datadictvalue["C_OWNER"] != '':
            page.get_by_label("Owner").click()
            page.get_by_label("Owner").type(datadictvalue["C_OWNER"])

        # Description
        if datadictvalue["C_DSCRPTN"]!='':
            page.get_by_label("Description").clear()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        # Clicking on Next button
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(3000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Click on Save and Close for Task
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="OK").click()

        try:
            expect(page.get_by_role("heading", name="Questionnaires")).to_be_visible()
            print("Questionnaries Saved Successfully")
            datadictvalue["RowStatus"] = "Questionnaries Saved Successfully"
        except Exception as e:
            print("Questionnaries not saved")
            datadictvalue["RowStatus"] = "Questionnaries not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, LA_QUESTIONNARIE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, LA_QUESTIONNARIE, PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK, LA_QUESTIONNARIE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[0] + "_" + LA_QUESTIONNARIE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




