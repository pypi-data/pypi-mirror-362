from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill("CURTIS.FEITTY")
    page.get_by_placeholder("Password").fill("j2#sr#3D")

    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(8000)
    page.get_by_label("Navigation Tabs").click()
    page.get_by_role("link", name="My Client Groups").click()
    page.wait_for_timeout(8000)
    page.get_by_role("link", name="Learning").click()
    page.wait_for_timeout(8000)
    page.get_by_role("link", name="Offerings").click()
    page.wait_for_timeout(5000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        # Select Course Title
        page.get_by_role("link", name="Create").click()
        page.wait_for_timeout(3000)
        page.get_by_text(datadictvalue["C_OFFRNG_TYPE"]).click()
        page.wait_for_timeout(3000)


        # Course Title Selection and Search Course
        # page.get_by_label("Course Title Operator").click()
        # page.wait_for_timeout(2000)
        # page.locator("//div[@title='Create Offering: Select Course']//following::li[text()='Equals']").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Course Title", exact=True).fill(datadictvalue["C_CRS_TITLE"])
        # page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name="**Publish Start Date", exact=True).locator("label")
        # page.get_by_role("cell", name="**Course Title Course Title").get_by_label("Publish Start Date Operator")
        # page.wait_for_timeout(1000)
        # page.get_by_role("cell", name="**Course Title Course Title").get_by_placeholder("m/d/yy").clear()
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name=datadictvalue["C_CRS_TITLE"], exact=True).click()
        page.get_by_role("button", name="Select").click()
        page.wait_for_timeout(3000)

        # Title
        # page.get_by_label("Offering Title Operator")
        # page.get_by_label("Offering Title", exact=True)
        # page.get_by_label("Course Title Operator")
        # page.get_by_label("Course Title", exact=True)
        page.get_by_label("Title").clear()
        page.get_by_label("Title").fill(datadictvalue["C_TITLE"])
        page.wait_for_timeout(3000)

        # Description
        page.get_by_text("Description").click()
        page.get_by_label("Editor editing area: main").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(3000)

        # Publish Start Date
        if datadictvalue["C_PBLSH_START_DATE"] != '':
            page.locator("//label[text()='Publish Start Date']//following::input[1]").clear()
            page.locator("//label[text()='Publish Start Date']//following::input[1]").type(datadictvalue["C_PBLSH_START_DATE"])
            page.wait_for_timeout(3000)

        # Publish End Date
        if datadictvalue["C_PBLSH_END_DATE"] != '':
            page.locator("//label[text()='Publish End Date']//following::input[1]").clear()
            page.locator("//label[text()='Publish End Date']//following::input[1]").type(str(datadictvalue["C_PBLSH_END_DATE"]))
            page.wait_for_timeout(3000)

        # Offering Start Date
        if page.locator("//label[text()='Offering Start Date']//following::input[1]").is_visible():
            if datadictvalue["C_OFFRNG_START_DATE"] != '':
                page.locator("//label[text()='Offering Start Date']//following::input[1]").clear()
                page.locator("//label[text()='Offering Start Date']//following::input[1]").type(str(datadictvalue["C_OFFRNG_START_DATE"]))
                page.wait_for_timeout(3000)

        # Offering End Date
        if page.locator("//label[text()='Offering End Date']//following::input[1]").is_visible():
            if datadictvalue["C_OFFRNG_END_DATE"] != '':
                page.locator("//label[text()='Offering End Date']//following::input[1]").clear()
                page.locator("//label[text()='Offering End Date']//following::input[1]").type(str(datadictvalue["C_OFFRNG_END_DATE"]))
                page.wait_for_timeout(3000)

        # Primary Classroom
        if page.get_by_label("Primary Classroom").is_visible():
            if datadictvalue["C_PRMRY_CLSSRM"] != '':
                page.get_by_label("Primary Classroom").clear()
                page.get_by_label("Primary Classroom").type(datadictvalue["C_PRMRY_CLSSRM"])
                page.wait_for_timeout(3000)

        # Language
        page.get_by_label("Language").click()
        page.wait_for_timeout(3000)
        page.get_by_text(datadictvalue["C_LNGG"], exact=True).click()

        # Facilitator type: Instructor
        if datadictvalue["C_FCLTTR_TYPE"] == 'Instructor':
            page.get_by_role("combobox", name="Facilitator Type").click()
            page.get_by_text(datadictvalue["C_FCLTTR_TYPE"], exact=True).click()
            page.wait_for_timeout(3000)
        # Primary Instructor
            if datadictvalue["C_PRMRY_INSTRCTR"] != '':
                page.locator("//label[text()='Primary Instructor']//following::input[1]").clear()
                page.locator("//label[text()='Primary Instructor']//following::input[1]").type(datadictvalue["C_PRMRY_INSTRCTR"])
                page.wait_for_timeout(3000)

        # Facilitator type: Training Supplier
        if datadictvalue["C_FCLTTR_TYPE"] == 'Training Supplier' and datadictvalue["C_TRNNG_SPPLR_NAME"] != '':
            page.get_by_role("combobox", name="Facilitator Type").click()
            page.get_by_text(datadictvalue["C_FCLTTR_TYPE"], exact=True).click()
            page.wait_for_timeout(2000)
        # Training Supplier Name
            if datadictvalue["C_TRNNG_SPPLR_NAME"] != '':
                page.locator("//label[text()='Training Supplier Name']//following::input[1]").clear()
                page.locator("//label[text()='Training Supplier Name']//following::input[1]").type(datadictvalue["C_TRNNG_SPPLR_NAME"])
                page.wait_for_timeout(2000)

        # Offering Coordinator (Dafault Value)

        # Override conversation system setup configuration
        if datadictvalue["C_OVRRD_CNVRSTN_SYSTM_SETUP_CNFGRTN"] != '':
            if datadictvalue["C_OVRRD_CNVRSTN_SYSTM_SETUP_CNFGRTN"] == "No":
                page.get_by_text("Override conversation system setup configuration").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_OVRRD_CNVRSTN_SYSTM_SETUP_CNFGRTN"] == "Yes":
                page.get_by_text("Override conversation system setup configuration").check()
                page.wait_for_timeout(3000)
        # Enable conversations for active and completed enrollees on the enrollment page
                if datadictvalue["C_ENBL_CNVRSTN_FOR_ACTV_AND_CMPLTD_ENRLLS_ON_THE_ENRLLMNT_PAGE"] != '':
                    if datadictvalue["C_ENBL_CNVRSTN_FOR_ACTV_AND_CMPLTD_ENRLLS_ON_THE_ENRLLMNT_PAGE"] == "Yes":
                        page.get_by_text("Enable conversations for active and completed enrollees on the enrollment page").check()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_ENBL_CNVRSTN_FOR_ACTV_AND_CMPLTD_ENRLLS_ON_THE_ENRLLMNT_PAGE"] == "No":
                        page.get_by_text("Enable conversations for active and completed enrollees on the enrollment page").uncheck()

    # Capacity Rules
        if datadictvalue["C_CPCTY_RULES"] != '':
            if datadictvalue["C_CPCTY_RULES"] == "Yes":
                page.get_by_role("heading", name="Capacity Rules")
                page.locator("label").filter(has_text="Capacity Rules").check()
            if datadictvalue["C_CPCTY_RULES"] == "No":
                page.get_by_text("Capacity Rules").uncheck()

        # Minimum Capacity
            if datadictvalue["C_MNMM_CPCTY"] != '':
                page.get_by_label("Minimum Capacity").clear()
                page.get_by_label("Minimum Capacity").type(str(datadictvalue["C_MNMM_CPCTY"]))
                page.wait_for_timeout(3000)

        # Maximum Capacity
            if datadictvalue["C_MXMM_CPCTY"] != '':
                page.get_by_label("Maximum Capacity").clear()
                page.get_by_label("Maximum Capacity").type(str(datadictvalue["C_MXMM_CPCTY"]))
                page.wait_for_timeout(3000)

        # Waitlist Mode (Default & Non-Editable Field)

        # Waitlist rules - Allow joining the waitlist from self-service
            if datadictvalue["C_WTLST_RULES"] != '':
                if datadictvalue["C_WTLST_RULES"] == "Yes":
                    page.get_by_text("Allow joining the waitlist from self-service").check()
                    page.wait_for_timeout(3000)
                if datadictvalue["C_WTLST_RULES"] == "No":
                    page.get_by_text("Allow joining the waitlist from self-service").uncheck()
                    page.wait_for_timeout(3000)

    # Enable virtual instructor led activity completion rules
        if page.get_by_text("Enable virtual instructor led activity completion rules.").is_visible():
            if datadictvalue["C_ENBL_VRTL_INSTRCTR_LED_ACTVTY_CMPLTN_RULES"] != '':
                if datadictvalue["C_ENBL_VRTL_INSTRCTR_LED_ACTVTY_CMPLTN_RULES"] == "Yes":
                    page.get_by_text("Enable virtual instructor led activity completion rules.").check()
                if datadictvalue["C_ENBL_VRTL_INSTRCTR_LED_ACTVTY_CMPLTN_RULES"] == "No":
                    page.get_by_text("Enable virtual instructor led activity completion rules.").uncheck()
                    page.wait_for_timeout(3000)

    # Percent of virtual activity duration the learner must participate in to be marked complete.
                if datadictvalue["C_PRCNT_OF_VRTL_ACTVY_DRTN_LRNR"] != '':
                    page.locator("//span[text()='Percent of virtual activity duration the learner must participate in to be marked complete.']//following::input[1]").clear()
                    page.locator("//span[text()='Percent of virtual activity duration the learner must participate in to be marked complete.']//following::input[1]").type(str(datadictvalue["C_PRCNT_OF_VRTL_ACTVY_DRTN_LRNR"]))
                    page.wait_for_timeout(3000)

    # Override Pricing
        if datadictvalue["C_OVRRD_PRCNG"] != '':
            if datadictvalue["C_OVRRD_PRCNG"] == "No":
                page.get_by_text("Override Pricing").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_OVRRD_PRCNG"] == "Yes":
                page.get_by_text("Override Pricing").check()
                page.wait_for_timeout(3000)

            # Currency
                if datadictvalue["C_CRRNCY"] != '':
                    page.get_by_role("combobox", name="Currency", exact=True).click()
                    page.get_by_text(datadictvalue["C_CRRNCY"], exact=True).click()
                    page.wait_for_timeout(3000)

            # Add Line Item - Line Item
                if datadictvalue["C_LINE_ITEM"] != '':
                    page.get_by_role("button", name="Add Line Item").click()
                    page.wait_for_timeout(2000)
                    page.get_by_role("combobox", name="Line Item").click()
                    page.get_by_text(datadictvalue["C_LINE_ITEM"]).click()
                    page.wait_for_timeout(2000)

            # Price
                if datadictvalue["C_PRICE"] != '':
                    page.get_by_role("row", name="Price").nth(1).locator("input").nth(2).clear()
                    page.get_by_role("row", name="Price").nth(1).locator("input").nth(2).type(str(datadictvalue["C_PRICE"]))
                    page.wait_for_timeout(3000)

            # Use to Calculate Catalog Item Price in Self-Service
                    if datadictvalue["C_CLCLT_CTLG_ITEM_PRICE"] != '':
                        if datadictvalue["C_CLCLT_CTLG_ITEM_PRICE"] != "Yes":
                            page.locator("//span[text()='Use to Calculate Catalog Item Price in Self-Service']//following::label[2]").check()
                            page.wait_for_timeout(3000)
                        if datadictvalue["C_CLCLT_CTLG_ITEM_PRICE"] == "No":
                            page.locator("//span[text()='Use to Calculate Catalog Item Price in Self-Service']//following::label[2]").uncheck()

        # Override Payment Type
        if datadictvalue["C_OVRRD_PYMNT_TYPE"] != '':
            if datadictvalue["C_OVRRD_PYMNT_TYPE"] == "Yes":
                page.get_by_text("Override Payment Type").check()
                page.wait_for_timeout(3000)
            if datadictvalue["C_OVRRD_PYMNT_TYPE"] == "No":
                page.get_by_text("Override Payment Type").uncheck()
                page.wait_for_timeout(3000)
        # Payment Type
                if datadictvalue["C_PYMNT_TYPE"] != '':
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Payment Type").click()
                    page.get_by_text(datadictvalue["C_PYMNT_TYPE"]).click()

                #if datadictvalue["C_PYMNT_TYPE"] == 'Manual Payment':
                    #page.wait_for_timeout(2000)
                    #page.get_by_role("combobox", name="Payment Type").click()
                    #page.get_by_text(datadictvalue["C_PYMNT_TYPE"]).click()
                    #page.wait_for_timeout(2000)

        # Require purchase order information
                if datadictvalue["C_RQR_PRCHS_ORDER_INFRMTN"] != '':
                    if datadictvalue["C_RQR_PRCHS_ORDER_INFRMTN"] == "Yes":
                        page.locator("//span[text()='Require purchase order information']//preceding::input[1]").check()
                    if datadictvalue["C_RQR_PRCHS_ORDER_INFRMTN"] == "No":
                        page.locator("//span[text()='Require purchase order information']//preceding::input[1]").uncheck()

        # Enable refunds on withdrawal from instructor-led and blended offerings
                if datadictvalue["C_RFNDS_ON_WTHDRWL_INSTRUCTOR_LED_BLENDED"] != '':
                    if datadictvalue["C_RFNDS_ON_WTHDRWL_INSTRUCTOR_LED_BLENDED"] == "No":
                        page.get_by_role("row", name="Enable refunds on withdrawal from instructor-led and blended offerings", exact=True).locator("label").uncheck()
                    if datadictvalue["C_RFNDS_ON_WTHDRWL_INSTRUCTOR_LED_BLENDED"] == "Yes":
                        page.get_by_role("row", name="Enable refunds on withdrawal from instructor-led and blended offerings", exact=True).locator("label").check()
                        page.wait_for_timeout(3000)
        # Days before offering starts to get a full refund
                    if datadictvalue["C_DAY_BEFORE_OFFERING_START_FULL_REFUND"] != '':
                        page.locator("//span[text()='Days before offering starts to get a full refund']//following::input[1]").clear()
                        page.wait_for_timeout(3000)
                        page.locator("//span[text()='Days before offering starts to get a full refund']//following::input[1]").type(str(datadictvalue["C_DAY_BEFORE_OFFERING_START_FULL_REFUND"]))

        # Enable refunds on withdrawal from self-paced offerings
                if datadictvalue["C_RFNDS_ON_WTHDRWL_FROM_SELF_PACED_OFFRNGS"] != '':
                    if datadictvalue["C_RFNDS_ON_WTHDRWL_FROM_SELF_PACED_OFFRNGS"] == "No":
                        page.get_by_role("row", name="Enable refunds on withdrawal from self-paced offerings", exact=True).locator("label").uncheck()
                    if datadictvalue["C_RFNDS_ON_WTHDRWL_FROM_SELF_PACED_OFFRNGS"] == "Yes":
                        page.get_by_role("row", name="Enable refunds on withdrawal from self-paced offerings", exact=True).locator("label").check()
                        page.wait_for_timeout(3000)
        # Maximum number of days after assignment start date
                    if datadictvalue["C_MXMM_MNBR_OF_DAYS_AFTER_ASSGNMNT_START_DATE"] != '':
                        page.locator("//span[text()='Days before offering starts to get a full refund']//following::input[1]").clear()
                        page.wait_for_timeout(3000)
                        page.locator("//span[text()='Days before offering starts to get a full refund']//following::input[1]").type(str(datadictvalue["C_MXMM_MNBR_OF_DAYS_AFTER_ASSGNMNT_START_DATE"]))

        # Topic
        if datadictvalue["C_TOPIC"] != '':
            page.wait_for_timeout(3000)
            page.get_by_label("Topic").click()
            page.get_by_title("Search: Topic").click()
            page.wait_for_timeout(3000)
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Translated Value").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Translated Value").fill(datadictvalue["C_TOPIC"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TOPIC"]).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(5000)

    # Save and Close (Cancel)
        page.get_by_role("button", name="Save and Close", exact=True).click()
        page.wait_for_timeout(10000)
        if page.locator("//a[@title='Done']").is_visible():
            page.locator("//a[@title='Done']").click()
            page.wait_for_timeout(5000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Offerings")).to_be_visible()
            print("Offerings Saved Successfully")
            datadictvalue["RowStatus"] = "Offerings Saved Successfully"
        except Exception as e:
            print("Offerings not saved")
            datadictvalue["RowStatus"] = "Offerings not added"

    OraSignOut(page, context, browser, videodir)
    return datadict



# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, LEARNING_OFFERINGS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, LEARNING_OFFERINGS,
                             PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK, LEARNING_OFFERINGS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[
            0] + "_" + LEARNING_OFFERINGS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
