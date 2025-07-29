from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *



def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill("Curtis.feitty")
    page.get_by_placeholder("Password").fill("j2#sr#3D")
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("My Client Groups", exact=True).click()
    page.get_by_role("link", name="Learning").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Offerings").click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Searching Course Name
        page.get_by_label("Offering Title", exact=True).type(datadictvalue["C_OFFRNG_TITLE"])
        page.get_by_placeholder("m/d/yy").clear()
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.get_by_role("link", name=datadictvalue["C_OFFRNG_TITLE"]).click()
        page.wait_for_timeout(5000)
        page.get_by_role("link", name="Activities Activities").click()

        # For Adding Section details
        page.locator("//div[@title='Overview']//following::span[text()='Add']").first.click()
        page.wait_for_timeout(2000)
        page.get_by_text("Add Section").click()

        # Section Title
        page.get_by_label("Section Title").clear()
        page.get_by_label("Section Title").type(datadictvalue["C_SCTN_TITLE"])

        # Description
        page.get_by_label("Editor editing area: main").click()
        page.get_by_label("Editor editing area: main").type(datadictvalue["C_DSCRPTN"])

        # Defined By
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Defined By").click()
        page.get_by_text(datadictvalue["C_DFND_BY"], exact=True).click()

        if datadictvalue["C_DFND_BY"]=='Section':
            # No.of Activities to Complete
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Number of Activities to").click()
            page.get_by_text(datadictvalue["C_NMBR_OF_ACTVTS_TO_CMPLT"], exact=True).click()

        # Learner can Access Section
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Learner Can Access Section").click()
        page.get_by_text(datadictvalue["C_LRNR_CAN_ACCSS_SCTN"],exact=True).click()

        # Section
        if datadictvalue["C_LRNR_CAN_ACCSS_SCTN"]!='':
            if datadictvalue["C_LRNR_CAN_ACCSS_SCTN"]=='After completing specific section':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Section", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SCTN"]).click()


        # Place Section After
        if datadictvalue["C_PLACE_SCTN_AFTER"]!='':
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Place Section After").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLACE_SCTN_AFTER"]).click()

        # Saving Section details
        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(3000)

        # For Adding Instructor Led Activity
        page.locator("//div[@title='Overview']//following::span[text()='Add']").first.click()
        page.wait_for_timeout(2000)
        page.get_by_text("Add Instructor-Led Activity").click()
        page.wait_for_timeout(5000)

        # Title
        page.get_by_label("Title").clear()
        page.get_by_label("Title").type(datadictvalue["C_TITLE_ONE"])

        # List Description
        if datadictvalue["C_LIST_DSCRPTN"]!='':
            page.get_by_label("List Description").clear()
            page.get_by_label("List Description").type(datadictvalue["C_LIST_DSCRPTN"])

        # Detailed Description
        page.get_by_label("Editor editing area: main").click()
        page.get_by_label("Editor editing area: main").type(datadictvalue["C_DTLD_DSCRPTN"])

        # Allow person completing the activity to mark themselves complete
        if datadictvalue["C_ALLOW_PRSN_CMPLTNG_THE_ACTVTY_TO_MARK_CMPLT"]!='':
            if datadictvalue["C_ALLOW_PRSN_CMPLTNG_THE_ACTVTY_TO_MARK_CMPLT"]=='Yes':
                page.locator("//span[text()='Allow person completing the activity to mark themselves complete']//preceding::label[1]").check()
            if datadictvalue["C_ALLOW_PRSN_CMPLTNG_THE_ACTVTY_TO_MARK_CMPLT"]=='No':
                page.locator("//span[text()='Allow person completing the activity to mark themselves complete']//preceding::label[1]").uncheck()

        # Expected Effort in Hours
        page.get_by_label("Expected Effort in Hours").clear()
        page.get_by_label("Expected Effort in Hours").type(str(datadictvalue["C_EXPCTD_EFFRT_IN_HOURS"]))

        # Activity Date
        page.get_by_placeholder("m/d/yy").clear()
        page.get_by_placeholder("m/d/yy").type(datadictvalue["C_ACTVTY_DATE"])

        # Time Zone
        page.wait_for_timeout(2000)
        page.locator("//label[text()='Time Zone'][1]//following::a[contains(@id,'drop')]").first.click()
        page.get_by_text(datadictvalue["C_TIME_ZONE"],exact=True).click()

        # Start Time
        page.get_by_label("Start Time").clear()
        page.get_by_label("Start Time").type(datadictvalue["C_START_TIME"])

        # End Time
        page.get_by_label("End Time").clear()
        page.get_by_label("End Time").type(datadictvalue["C_END_TIME"])

        # Repeat
        if datadictvalue["C_RPT"]!='':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Repeat").click()
            page.get_by_text(datadictvalue["C_RPT"], exact=True).click()

        #Delivery Details
        ### Instructors
        page.get_by_role("textbox", name="Instructors").click()
        page.get_by_role("textbox", name="Instructors").fill(datadictvalue["C_INSTRCTRS"])

        # Virtual Classroom Type
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Virtual Classroom Type").click()
        page.get_by_text(datadictvalue["C_VRTL_CLSSRM_TYPE"],exact=True).click()

        if datadictvalue["C_VRTL_CLSSRM_TYPE"]=='Ad hoc virtual classroom':
            page.wait_for_timeout(2000)
            page.get_by_label("Virtual Classroom URL").type(datadictvalue["C_VRTL_CLSSRM_URL"])

        if datadictvalue["C_VRTL_CLSSRM_TYPE"] == 'Named virtual classroom':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Virtual Classroom Type").click()
            page.get_by_role("textbox", name="Virtual Classroom").type(datadictvalue["C_VRTL_CLSSRM"])
            page.get_by_text(datadictvalue["C_VRTL_CLSSRM"], exact=True).click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Product").click()
            page.get_by_text("Meeting", exact=True).click()

        ### Classrooms
        page.get_by_role("textbox", name="Classrooms").clear()
        page.get_by_role("textbox", name="Classrooms").type(datadictvalue["C_CLSSRMS"], delay=50)
        page.get_by_text(datadictvalue["C_CLSSRMS"], exact=True).click()
        page.get_by_role("heading", name="Delivery Details").click()

        # Advanced Rules
        # ### Activity Type
        # page.wait_for_timeout(2000)
        # page.get_by_role("combobox", name="Activity Type").click()
        # page.get_by_text(datadictvalue["C_ACTVTY_TYPE"]).click()

        ### Learner Can Access Activity
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Learner Can Access Activity").click()
        page.get_by_text(datadictvalue["C_LRNR_CAN_ACCSS_ACTVTY"]).click()

        # Attachments are visible to administrators
        with page.expect_file_chooser() as fc_info:
            page.locator("//label[text()='Attachments are visible to administrators']//following::span[text()='Drag files here or click to add attachment'][1]").click(force=True)
            page.wait_for_timeout(3000)
        file_chooser = fc_info.value
        file_chooser.set_files("attachment/Sample.jpg")
        page.wait_for_timeout(5000)

        # Attachments are visible to administrators and enrollees
        with page.expect_file_chooser() as fc_info:
            page.locator("//label[text()='Attachments are visible to administrators and enrollees']//following::span[text()='Drag files here or click to add attachment'][1]").click(force=True)
            page.wait_for_timeout(3000)
        file_chooser = fc_info.value
        file_chooser.set_files("attachment/Sample.jpg")
        page.wait_for_timeout(5000)

        # Adhoc Resources
        page.get_by_role("button", name="Add").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Name").clear()
        page.get_by_label("Name").type(datadictvalue["C_NAME"])
        page.get_by_label("Quantity").clear()
        page.get_by_label("Quantity").type(str(datadictvalue["C_QNTTY"]))
        if datadictvalue["C_DSCRPTN_ONE"]!='':
            page.get_by_label("Description", exact=True).type(datadictvalue["C_DSCRPTN_ONE"])
        page.get_by_role("button", name="Save").click()


        # Click on Ok button
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # For Adding Evaluation
        page.locator("//div[@title='Overview']//following::span[text()='Add']").first.click()
        page.wait_for_timeout(2000)
        page.get_by_text("Add Evaluation").click()
        page.wait_for_timeout(5000)

        # Title
        page.get_by_label("Title").clear()
        page.get_by_label("Title").type(datadictvalue["C_TITLE_TWO"])

        # Evaluation Section
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Evaluation Selection").click()
        page.get_by_text(datadictvalue["C_EVLTN_SLCTN"]).click()
        page.wait_for_timeout(2000)

        # Evaluation
        if datadictvalue["C_EVLTN_SLCTN"] == 'Override system default':
            page.get_by_placeholder("Search", exact=True).clear()
            page.get_by_placeholder("Search", exact=True).type(datadictvalue["C_EVLTN"])
            page.get_by_text(datadictvalue["C_EVLTN"], exact=True).click()
            # Required for Completion
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Required for Completion").click()
            page.get_by_text(datadictvalue["C_RQRD_FOR_CMPLTN"], exact=True).click()

        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(3000)
        page.locator("//a[@title='Done']").click()
        page.wait_for_timeout(3000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Offerings")).to_be_visible()
            print("Instructor Led Activity Saved Successfully")
            datadictvalue["RowStatus"] = "Instructor Led Activity Saved Successfully"
        except Exception as e:
            print("Instructor Led Activity not saved")
            datadictvalue["RowStatus"] = "Instructor Led Activity not added"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, INST_LED_ACTIVITY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, INST_LED_ACTIVITY,PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK, INST_LED_ACTIVITY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[0] + "_" + INST_LED_ACTIVITY + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

