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
    page.get_by_role("textbox").type("Question Library")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        #Select question Library task
        page.get_by_role("link", name="Question Library", exact=True).click()
        page.wait_for_timeout(2000)

        #select the Subscriber
        page.get_by_role("combobox", name="Subscriber").click()
        page.get_by_text(datadictvalue["C_SBCRBR"]).click()
        page.wait_for_timeout(3000)

        page.get_by_text('Question Library').nth(1).click()
        page.wait_for_timeout(3000)
        if page.get_by_role("cell", name="Expand Question Library").get_by_role("link").is_visible():
            page.get_by_role("cell", name="Expand Question Library").get_by_role("link").click()
        page.wait_for_timeout(3000)

        #Check whether folder is available or new folder to be created
        if page.get_by_text(datadictvalue["C_QSTN_LBRRY"], exact=True).nth(0).is_visible():
            page.get_by_text(datadictvalue["C_QSTN_LBRRY"], exact=True).nth(0).click()
            page.wait_for_timeout(2000)
        else:
            # Create Question Library
            page.get_by_role("button", name="Create").first.click()
            page.get_by_role("textbox", name="Folder").click()
            page.get_by_role("textbox", name="Folder").fill(datadictvalue["C_QSTN_LBRRY"])
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)
            #Selecting Question Library
            page.get_by_text(datadictvalue["C_QSTN_LBRRY"], exact=True).click()
            page.wait_for_timeout(2000)

        #Adding QUESTIONS
        page.locator("a").filter(has_text="Create").click()

        #Question Code
        page.get_by_label("Question Code", exact=True).click()
        page.get_by_label("Question Code", exact=True).clear()
        page.get_by_label("Question Code", exact=True).fill(datadictvalue["C_QSTN_CODE"])

        #Status
        page.get_by_role("combobox", name="Status").click()
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

        #Privacy
        page.get_by_role("combobox", name="Privacy").click()
        page.get_by_text(datadictvalue["C_PRVCY"], exact=True).click()

        #Question Text
        page.get_by_label("Question Text").click()
        page.get_by_label("Question Text").fill(datadictvalue["C_QSTN_TEXT"])

        #Question Type
        page.get_by_role("combobox", name="Question Type").click()
        page.get_by_text(datadictvalue["C_QSTN_TYPE"], exact=True).click()
        page.wait_for_timeout(2000)

        #Score Question
        if page.get_by_text("Score Question").is_visible():
            if datadictvalue["C_SCORE_QSTN"] == 'Yes':
                page.get_by_text("Score Question").check()
            if datadictvalue["C_SCORE_QSTN"] == 'No' or '':
                page.get_by_text("Score Question").uncheck()

        #Question Classification
        page.get_by_role("combobox", name="Question Classification").click()
        page.get_by_text(datadictvalue["C_QSTN_CLSSFCTN"],exact=True).click()

        #Candidate Type
        page.get_by_role("combobox", name="Candidate Types").click()
        page.get_by_text(datadictvalue["C_CNDDT_TYPES"]).click()

        #Response Type
        page.get_by_role("combobox", name="Response Type").click()
        page.wait_for_timeout(1000)
        page.get_by_text(datadictvalue["C_RSPNS_TYPE"]).click()
        page.wait_for_timeout(1000)
        if page.locator("//input[@title='Plain Text Box']").is_visible():
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Save and Close").click()
            page.get_by_role("button", name="OK").click()
            page.locator("//div[@title='Questions']//preceding::a[1]").click()
            page.wait_for_timeout(2000)
        else:
            #Response Order
            page.get_by_role("combobox", name="Response Order").click()
            page.get_by_text(datadictvalue["C_RSPNS_ORDER"]).click()

            #Add Response
            if datadictvalue["C_SHORT_DSCRPTN_ONE"] != '':
                page.get_by_role("button", name="Add").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name='Summary').get_by_role("row").nth(0).locator("input").nth(1).click()
                page.get_by_role("table", name='Summary').get_by_role("row").nth(0).locator("input").nth(1).fill(str(datadictvalue["C_SHORT_DSCRPTN_ONE"]))

            if datadictvalue["C_SHORT_DSCRPTN_TWO"] != '':
                page.get_by_role("button", name="Add").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name='Summary').get_by_role("row").nth(1).locator("input").nth(1).click()
                page.get_by_role("table", name='Summary').get_by_role("row").nth(1).locator("input").nth(1).fill(str(datadictvalue["C_SHORT_DSCRPTN_TWO"]))

            if datadictvalue["C_SHORT_DSCRPTN_THREE"] != '':
                page.get_by_role("button", name="Add").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name='Summary').get_by_role("row").nth(2).locator("input").nth(1).click()
                page.get_by_role("table", name='Summary').get_by_role("row").nth(2).locator("input").nth(1).fill(str(datadictvalue["C_SHORT_DSCRPTN_THREE"]))

            if datadictvalue["C_SHORT_DSCRPTN_FOUR"] != '':
                page.get_by_role("button", name="Add").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name='Summary').get_by_role("row").nth(3).locator("input").nth(1).click()
                page.get_by_role("table", name='Summary').get_by_role("row").nth(3).locator("input").nth(1).fill(str(datadictvalue["C_SHORT_DSCRPTN_FOUR"]))

            if datadictvalue["C_SHORT_DSCRPTN_FIVE"] != '':
                page.get_by_role("button", name="Add").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name='Summary').get_by_role("row").nth(4).locator("input").nth(1).click()
                page.get_by_role("table", name='Summary').get_by_role("row").nth(4).locator("input").nth(1).fill(str(datadictvalue["C_SHORT_DSCRPTN_FIVE"]))
            page.get_by_role("button", name="Save and Close").click()
            page.get_by_role("button", name="OK").click()

            page.locator("//div[@title='Questions']//preceding::a[1]").click()
            page.wait_for_timeout(2000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Search")).to_be_visible()
            print("questions Saved Successfully")
            datadictvalue["RowStatus"] = "Added questions"
        except Exception as e:
            print("Unable to save questions")
            datadictvalue["RowStatus"] = "Unable to Add questions"

    OraSignOut(page, context, browser, videodir)
    return datadict

print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + Recruiting_CONFIG_WRKBK, QUESTION_LIBRARY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + Recruiting_CONFIG_WRKBK, QUESTION_LIBRARY,
                             PRCS_DIR_PATH + Recruiting_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + Recruiting_CONFIG_WRKBK, QUESTION_LIBRARY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", Recruiting_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", Recruiting_CONFIG_WRKBK)[0] + "_" + QUESTION_LIBRARY + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
