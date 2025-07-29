from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    #Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    #Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Questionnaires")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Questionnaires", exact=True).click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
    

        # select the Subscriber
        page.get_by_role("combobox", name="Subscriber").click()
        page.get_by_text(datadictvalue["C_SBCRBR"]).click()
        page.wait_for_timeout(3000)

        if page.get_by_text("Questionnaire Library").first.is_visible():
            if page.locator("//span[text()='Questionnaire Library']//preceding::a[@title='Expand']").is_visible():
                page.locator("//span[text()='Questionnaire Library']//preceding::a[@title='Expand']").click()
                page.wait_for_timeout(3000)
                page.get_by_text("Questionnaire Library").first.click()

        # Check whether folder is available or new folder to be created
            if page.get_by_text(datadictvalue["C_QSTNNR_LBRRY"], exact=True).nth(0).is_visible():
                page.get_by_text(datadictvalue["C_QSTNNR_LBRRY"], exact=True).nth(0).click()
                page.wait_for_timeout(2000)
            else:
                # Create Question Library
                page.get_by_role("button", name="Create").first.click()
                page.get_by_role("textbox", name="Folder").click()
                page.get_by_role("textbox", name="Folder").fill(datadictvalue["C_QSTNNR_LBRRY"])
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)
                # Selecting Question Library
                page.get_by_text(datadictvalue["C_QSTNNR_LBRRY"],exact=True).click()
                page.wait_for_timeout(2000)


        #Adding Questionnaires
        page.locator("a").filter(has_text="Create").click()

        #Select Template
        # page.get_by_label("Questionnaire Template ID").click()
        # page.get_by_label("Questionnaire Template ID").fill(datadictvalue["C_QUSTNNR_CODE"])
        # page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        # page.wait_for_timeout(2000)
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_QUSTNNR_CODE"]).click()
        # page.get_by_role("button", name="OK").click()
        # page.wait_for_timeout(2000)

        #Name
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_QSTNNR_TMPLT_NAME"])
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_QSTNNR_TMPLT_NAME"],exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])

        #Status
        page.get_by_role("combobox", name="Status").click()
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

        #Privacy
        page.get_by_role("combobox", name="Privacy").click()
        page.get_by_text(datadictvalue["C_PRVCY"], exact=True).click()

        #Description
        # page.get_by_label("Description").click()
        # page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        #PrevQues = datadictvalue["C_NAME"]

        #Next Page
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(2000)

    #Question verification
    # page.get_by_text(datadictvalue["C_ALLOW_ADDTNL_QSTNS"],exact=True).first.click()
    # page.wait_for_timeout(2000)
    # page.get_by_text(datadictvalue["C_QUSTN_TEXT"]).click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Next Page
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(2000)

        # Click on Save and Close
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="OK").click()

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Questionnaires")).to_be_visible()
            print("Questionnaires Saved Successfully")
            datadictvalue["RowStatus"] = "Added Questionnaires"
        except Exception as e:
            print("Unable to save Questionnaires")
            datadictvalue["RowStatus"] = "Unable to Add Questions"

    OraSignOut(page, context, browser, videodir)
    return datadict



print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + Recruiting_CONFIG_WRKBK, QUESTIONNAIRE_REC):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + Recruiting_CONFIG_WRKBK, QUESTIONNAIRE_REC,PRCS_DIR_PATH + Recruiting_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + Recruiting_CONFIG_WRKBK, QUESTIONNAIRE_REC)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", Recruiting_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", Recruiting_CONFIG_WRKBK)[0] + "_" + QUESTIONNAIRE_REC + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
