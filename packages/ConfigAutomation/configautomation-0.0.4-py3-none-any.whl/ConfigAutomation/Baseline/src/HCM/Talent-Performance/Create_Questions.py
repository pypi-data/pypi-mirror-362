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
    page.get_by_role("link", name="Questions").click()
    page.wait_for_timeout(3000)

    PrevQuesFolder=''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Subscriber
        page.get_by_text('Question Library').nth(0).click()
        page.wait_for_timeout(3000)
        if page.get_by_role("cell", name="Expand Question Library").get_by_role("link").is_visible():
            page.get_by_role("cell", name="Expand Question Library").get_by_role("link").click()
        page.wait_for_timeout(3000)

        # Check whether folder is available or new folder to be created
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
            # Selecting Question Library
            page.get_by_text(datadictvalue["C_QSTN_LBRRY"], exact=True).click()
            page.wait_for_timeout(2000)

        # Click on Create button
        page.locator("a").filter(has_text="Create").click()
        page.wait_for_timeout(5000)

        # Question Code
        # if datadictvalue["C_QSTN_CODE"]!='':
        #     page.get_by_label("Question Code", exact=True).clear()
        #     page.get_by_label("Question Code", exact=True).type(datadictvalue["C_QSTN_CODE"])

        # Status
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Status").click()
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

        # Privacy
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Privacy").click()
        page.get_by_text(datadictvalue["C_PRVCY"], exact=True).click()

        # Owner Name
        if datadictvalue["C_OWNER"]!='':
            page.get_by_label("Owner").click()
            page.get_by_label("Owner").type(datadictvalue["C_OWNER"])

        # Question Text
        page.get_by_label("Question Text").click()
        page.get_by_label("Question Text").type(datadictvalue["C_QSTN_TEXT"])

        # Instructions
        if datadictvalue["C_INSTRCTNS"]!='':
            page.get_by_label("Editor editing area: main").click()
            page.get_by_label("Editor editing area: main").type(datadictvalue["C_INSTRCTNS"])

        # Question type as Text
        if datadictvalue["C_QSTN_TYPE"]=='Text':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Question Type").click()
            page.get_by_text(datadictvalue["C_QSTN_TYPE"],exact=True).click()

            # Display the question conditionally
            if datadictvalue["C_DSPLY_THE_QSTN_CNDTNLLY"]!='':
                if datadictvalue["C_DSPLY_THE_QSTN_CNDTNLLY"]=='Yes':
                    page.get_by_text("Display the question").check()
                if datadictvalue["C_DSPLY_THE_QSTN_CNDTNLLY"]=='No':
                    page.get_by_text("Display the question").uncheck()

                page.wait_for_timeout(2000)
                # Controlling Question Code
                if datadictvalue["C_CNTRLLNG_QSTN_CODE"]!='':
                    page.get_by_label("Controlling Question Code").click()
                    page.get_by_label("Controlling Question Code").type(datadictvalue["C_CNTRLLNG_QSTN_CODE"])
                # Controlling Response
                if datadictvalue["C_CNTRLLNG_RSPNS"]!='':
                    page.wait_for_timeout(2000)
                    page.get_by_role("combobox", name="Controlling Response").click()
                    page.get_by_text(datadictvalue["C_CNTRLLNG_RSPNS"],exact=True).click()

            # Response Type
            if datadictvalue["C_RSPNS_TYPE"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Response Type").click()
                page.get_by_text(datadictvalue["C_RSPNS_TYPE"],exact=True).click()

            # Allow Attachments
            if datadictvalue["C_ALLOW_ATTCHMNTS"]!='':
                if datadictvalue["C_ALLOW_ATTCHMNTS"]=='Yes':
                    page.get_by_text("Allow attachments").check()
                if datadictvalue["C_ALLOW_ATTCHMNTS"]=='No':
                    page.get_by_text("Allow attachments").uncheck()

            # Minimum Length
            if datadictvalue["C_MNMM_LNGTH"]!='':
                page.get_by_label("Minimum Length").click()
                page.get_by_label("Minimum Length").type(datadictvalue["C_MNMM_LNGTH"])

            # Maximum Length
            if datadictvalue["C_MXMM_LNGTH"]!='':
                page.get_by_label("Maximum Length").click()
                page.get_by_label("Maximum Length").type(datadictvalue["C_MXMM_LNGTH"])

        # Question Type as Single Choice
        if datadictvalue["C_QSTN_TYPE"]=='Single Choice':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Question Type").click()
            page.get_by_text(datadictvalue["C_QSTN_TYPE"],exact=True).click()

            # Display the question conditionally
            if datadictvalue["C_DSPLY_THE_QSTN_CNDTNLLY"] != '':
                if datadictvalue["C_DSPLY_THE_QSTN_CNDTNLLY"] == 'Yes':
                    page.get_by_text("Display the question").check()
                if datadictvalue["C_DSPLY_THE_QSTN_CNDTNLLY"] == 'No':
                    page.get_by_text("Display the question").uncheck()

                page.wait_for_timeout(2000)
                # Controlling Question Code
                if datadictvalue["C_CNTRLLNG_QSTN_CODE"] != '':
                    page.get_by_label("Controlling Question Code").click()
                    page.get_by_label("Controlling Question Code").type(datadictvalue["C_CNTRLLNG_QSTN_CODE"])
                # Controlling Response
                if datadictvalue["C_CNTRLLNG_RSPNS"] != '':
                    page.wait_for_timeout(2000)
                    page.get_by_role("combobox", name="Controlling Response").click()
                    page.get_by_text(datadictvalue["C_CNTRLLNG_RSPNS"], exact=True).click()

            # Score Question
            if datadictvalue["C_SCORE_QSTN"]!='':
                if datadictvalue["C_SCORE_QSTN"] == 'Yes':
                    page.get_by_text("Score Question").check()
                if datadictvalue["C_SCORE_QSTN"] == 'No':
                    page.get_by_text("Score Question").uncheck()

            # Response
            ## Response Type
            if datadictvalue["C_RSPNS_TYPE"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Response Type").click()
                page.get_by_text(datadictvalue["C_RSPNS_TYPE"],exact=True).click()

            ## Rating Model
            if datadictvalue["C_RTNG_MODEL"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Rating Model").click()
                page.get_by_text(datadictvalue["C_RTNG_MODEL"],exact=True).first.click()

            ## Response Order
            if datadictvalue["C_RSPNS_ORDER"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Response Order").click()
                page.get_by_text(datadictvalue["C_RSPNS_ORDER"],exact=True).first.click()

            ## Allow Attachments
            if datadictvalue["C_ALLOW_ATTCHMNTS"]!='':
                if datadictvalue["C_ALLOW_ATTCHMNTS"]=='Yes':
                    page.get_by_text("Allow attachments").check()
                if datadictvalue["C_ALLOW_ATTCHMNTS"]=='No':
                    page.get_by_text("Allow attachments").uncheck()

            ## Allow Additional Comments
            if datadictvalue["C_ALLOW_ADDTNL_CMMNTS"]!='':
                if datadictvalue["C_ALLOW_ADDTNL_CMMNTS"]=='Yes':
                    page.get_by_text("Allow Additional Comments").check()
                if datadictvalue["C_ALLOW_ADDTNL_CMMNTS"]=='No':
                    page.get_by_text("Allow Additional Comments").uncheck()

            ## Adding Shot Description
            if datadictvalue["C_SHORT_DSCRPTN_ONE"]!='':
                page.get_by_role("button", name="Add").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:0\\:it9\"]").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:0\\:it9\"]").type(datadictvalue["C_SHORT_DSCRPTN_ONE"])

            if datadictvalue["C_SHORT_DSCRPTN_TWO"]!='':
                page.get_by_role("button", name="Add").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:1\\:it9\"]").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:1\\:it9\"]").type(datadictvalue["C_SHORT_DSCRPTN_TWO"])

            if datadictvalue["C_SHORT_DSCRPTN_THREE"]!='':
                page.get_by_role("button", name="Add").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:2\\:it9\"]").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:2\\:it9\"]").type(datadictvalue["C_SHORT_DSCRPTN_THREE"])

            if datadictvalue["C_SHORT_DSCRPTN_FOUR"]!='':
                page.get_by_role("button", name="Add").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:3\\:it9\"]").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:3\\:it9\"]").type(datadictvalue["C_SHORT_DSCRPTN_FOUR"])

        # Question type as No Response
        if datadictvalue["C_QSTN_TYPE"] == 'No Response':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Question Type").click()
            page.get_by_text(datadictvalue["C_QSTN_TYPE"], exact=True).click()

        # Question Type as Multiple Choice
        if datadictvalue["C_QSTN_TYPE"]=='Multiple Choice':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Question Type").click()
            page.get_by_text(datadictvalue["C_QSTN_TYPE"],exact=True).click()

            # Display the question conditionally
            if datadictvalue["C_DSPLY_THE_QSTN_CNDTNLLY"] != '':
                if datadictvalue["C_DSPLY_THE_QSTN_CNDTNLLY"] == 'Yes':
                    page.get_by_text("Display the question").check()
                if datadictvalue["C_DSPLY_THE_QSTN_CNDTNLLY"] == 'No':
                    page.get_by_text("Display the question").uncheck()

                page.wait_for_timeout(2000)
                # Controlling Question Code
                if datadictvalue["C_CNTRLLNG_QSTN_CODE"] != '':
                    page.get_by_label("Controlling Question Code").click()
                    page.get_by_label("Controlling Question Code").type(datadictvalue["C_CNTRLLNG_QSTN_CODE"])
                # Controlling Response
                if datadictvalue["C_CNTRLLNG_RSPNS"] != '':
                    page.wait_for_timeout(2000)
                    page.get_by_role("combobox", name="Controlling Response").click()
                    page.get_by_text(datadictvalue["C_CNTRLLNG_RSPNS"], exact=True).click()

            # Score Question
            if datadictvalue["C_SCORE_QSTN"]!='':
                if datadictvalue["C_SCORE_QSTN"] == 'Yes':
                    page.get_by_text("Score Question").check()
                if datadictvalue["C_SCORE_QSTN"] == 'No':
                    page.get_by_text("Score Question").uncheck()

            # Response
            ## Response Type
            if datadictvalue["C_RSPNS_TYPE"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Response Type").click()
                page.get_by_text(datadictvalue["C_RSPNS_TYPE"],exact=True).click()

            ## Rating Model
            if datadictvalue["C_RTNG_MODEL"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Rating Model").click()
                page.get_by_text(datadictvalue["C_RTNG_MODEL"],exact=True).first.click()

            ## Response Order
            if datadictvalue["C_RSPNS_ORDER"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Response Order").click()
                page.get_by_text(datadictvalue["C_RSPNS_ORDER"],exact=True).first.click()

            ## Allow Attachments
            if datadictvalue["C_ALLOW_ATTCHMNTS"]!='':
                if datadictvalue["C_ALLOW_ATTCHMNTS"]=='Yes':
                    page.get_by_text("Allow attachments").check()
                if datadictvalue["C_ALLOW_ATTCHMNTS"]=='No':
                    page.get_by_text("Allow attachments").uncheck()

            ## Allow Additional Comments
            if datadictvalue["C_ALLOW_ADDTNL_CMMNTS"]!='':
                if datadictvalue["C_ALLOW_ADDTNL_CMMNTS"]=='Yes':
                    page.get_by_text("Allow Additional Comments").check()
                if datadictvalue["C_ALLOW_ADDTNL_CMMNTS"]=='No':
                    page.get_by_text("Allow Additional Comments").uncheck()

            ## Minimum Number of Selections
            if datadictvalue["C_MNMM_NMBR_OF_SLCTNS"]!='':
                page.get_by_label("Minimum Number of Selections").click()
                page.get_by_label("Minimum Number of Selections").type(datadictvalue["C_MNMM_NMBR_OF_SLCTNS"])

            ## Maximum No.of Selections
            if datadictvalue["C_MXMM_NMBR_OF_SLCTNS"]!='':
                page.get_by_label("Maximum Number of Selections").click()
                page.get_by_label("Maximum Number of Selections").type(datadictvalue["C_MXMM_NMBR_OF_SLCTNS"])

            ## Adding Shot Description
            if datadictvalue["C_SHORT_DSCRPTN_ONE"] != '':
                page.get_by_role("button", name="Add").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:0\\:it9\"]").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:0\\:it9\"]").type(datadictvalue["C_SHORT_DSCRPTN_ONE"])

            if datadictvalue["C_SHORT_DSCRPTN_TWO"] != '':
                page.get_by_role("button", name="Add").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:1\\:it9\"]").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:1\\:it9\"]").type(datadictvalue["C_SHORT_DSCRPTN_TWO"])

            if datadictvalue["C_SHORT_DSCRPTN_THREE"] != '':
                page.get_by_role("button", name="Add").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:2\\:it9\"]").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:2\\:it9\"]").type(datadictvalue["C_SHORT_DSCRPTN_THREE"])

            if datadictvalue["C_SHORT_DSCRPTN_FOUR"] != '':
                page.get_by_role("button", name="Add").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:3\\:it9\"]").click()
                page.locator("input[name=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:AT1\\:_ATp\\:ATt1\\:3\\:it9\"]").type(datadictvalue["C_SHORT_DSCRPTN_FOUR"])

        # Click on Save and Close for Task
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="OK").click()

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Questions")).to_be_visible()
            print("Questions Saved Successfully")
            datadictvalue["RowStatus"] = "Questions Saved Successfully"
        except Exception as e:
            print("Questions not saved")
            datadictvalue["RowStatus"] = "Questions not added"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, QUESTIONS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, QUESTIONS,PRCS_DIR_PATH + PERF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PERF_CONFIG_WRKBK, QUESTIONS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0] + "_" + QUESTIONS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))