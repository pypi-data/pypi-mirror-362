from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill("CURTIS.FEITTY")
    page.get_by_placeholder("Password").fill("j2#sr#3D")
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Navigator").click()
    page.wait_for_timeout(3000)
    page.get_by_title("My Client Groups", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Learning").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Content", exact=True).click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(6000)
    #
        # Add
        page.get_by_role("button", name="Add").click()
        page.wait_for_timeout(6000)
        page.get_by_text(datadictvalue["C_ADD_CNTNT_TYPE"]).click()
        page.wait_for_timeout(6000)

        # Title
        if datadictvalue["C_TITLE"] != '':
            page.get_by_label("Title").click()
            page.get_by_label("Title").fill(datadictvalue["C_TITLE"])
            page.wait_for_timeout(2000)

        # Status
        if datadictvalue["C_STTS"] != '':
            page.get_by_role("combobox", name="Status").click()
            page.get_by_text(datadictvalue["C_STTS"], exact=True).click()
            page.wait_for_timeout(2000)

        # Description
        if datadictvalue["C_DSCRPTN"] != '':
            page.get_by_label("Editor editing area: main").click()
            page.get_by_label("Editor editing area: main").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(3000)

        # Start Date
        if datadictvalue["C_START_DATE"] != '':
            page.locator("//label[text()='Start Date']//following::input[1]").clear()
            page.locator("//label[text()='Start Date']//following::input[1]").type(str(datadictvalue["C_START_DATE"]))
            page.wait_for_timeout(3000)

        # End Date
        if datadictvalue["C_END_DATE"] != '':
            page.locator("//label[text()='End Date']//following::input[1]").clear()
            page.locator("//label[text()='End Date']//following::input[1]").type(str(datadictvalue["C_END_DATE"]))
            page.wait_for_timeout(3000)

        # File - Add Online Content/Add Video/Add PDF File
        if datadictvalue["C_ONLN_FILE"] != '':
            with page.expect_file_chooser() as fc_info:
                page.locator(
                    "//a[text()='Drag and drop a file here or browse for SCORM, HACP or AICC content to upload']").click()
            file_chooser = fc_info.value
            file_chooser.set_files("attachment/A-Roadmap-to-Success-scorm.zip")
            page.wait_for_timeout(20000)

        # File - Add Video
        if datadictvalue["C_VIDEO_FILE"] != '':
            with page.expect_file_chooser() as fc_info:
                page.locator("//a[text()='Drag and drop a video here or browse for a video to upload.']").click()
            file_chooser = fc_info.value
            file_chooser.set_files("attachment/Video_test.mp4")
            # file_chooser.set_files("attachment/PROTECT YOUR HEARING! - Hearing conservation safety training video.mp4")
            page.wait_for_timeout(15000)

        # File - Add PDF File
        if datadictvalue["C_PDF_FILE"] != '':
            with page.expect_file_chooser() as fc_info:
                page.locator("//a[text()='Drag and drop a PDF file here or browse for a PDF file to upload.']").click()
            file_chooser = fc_info.value
            file_chooser.set_files("attachment/Fire-Drills-Procedures.pdf")
            page.wait_for_timeout(15000)

        # URL
        if datadictvalue["C_URL"] != '':
            page.get_by_label("URL").click()
            page.get_by_label("URL").fill(datadictvalue["C_URL"])
            page.wait_for_timeout(5000)
            # Mark as complete when learner opens the web link
            if datadictvalue["C_WEB_LINK"] != '':
                if datadictvalue["C_WEB_LINK"] == "Yes":
                    if not page.get_by_text("Mark as complete when learner opens the web link", exact=True).is_checked():
                        page.get_by_text("Mark as complete when learner opens the web link", exact=True).click()
                if datadictvalue["C_WEB_LINK"] == "No":
                    if page.get_by_text("Mark as complete when learner opens the web link", exact=True).is_checked():
                        page.get_by_text("Mark as complete when learner opens the web link", exact=True).click()

        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(5000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Done")).to_be_visible()
            print("Learning Content Saved Successfully")
            datadictvalue["RowStatus"] = "Learning Content Saved Successfully"
        except Exception as e:
            print("Learning Content not saved")
            datadictvalue["RowStatus"] = "Learning Content not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, LEARNING_CONTENT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, LEARNING_CONTENT,
                             PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK, LEARNING_CONTENT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[
            0] + "_" + LEARNING_CONTENT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
