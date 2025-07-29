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
    page.wait_for_timeout(5000)

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(5000)
    page.get_by_role("textbox").fill("Manage Project Templates")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Project Templates", exact=True).click()

    # Create Project Statuses
    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        if datadictvalue["C_NAME"] != PrevName:
            if i > 0:
                page.get_by_role("button", name="Done").click()
                page.wait_for_timeout(2000)
                page.get_by_title("Save").click()
                page.wait_for_timeout(2000)
                # page.get_by_role("cell", name="Save and Close", exact=True).click()
                page.get_by_text("Save and Close").click()
                page.wait_for_timeout(2000)
            ###Created for Testing###
            # page.get_by_label("Template Name").fill(datadictvalue["C_NAME"])
            # page.get_by_role("button", name="Search", exact=True).click()
            # page.get_by_role("button", name="Edit").click()
    ###-------------------------------------###
            page.get_by_role("button", name="Create Template", exact=True).click()
            page.wait_for_timeout(4000)
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.wait_for_timeout(2000)
            page.get_by_label("Number").click()
            page.get_by_label("Number").fill(datadictvalue["C_NMBR"])
            page.wait_for_timeout(2000)

            page.get_by_title("Search: Business Unit").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Business Unit").click()
            page.get_by_role("textbox", name="Business Unit").fill(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("button", name="Search", exact=True).click()
            # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BSNSS_UNIT"], exact=True).click()
            page.locator("//div[text()='Search and Select: Business Unit']//following::span[text()='"+datadictvalue["C_BSNSS_UNIT"]+"']").click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)
            page.get_by_title("Search: Project Unit").click()
            page.get_by_role("link", name="Search...").click()
            # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").click()
            # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").fill(str(datadictvalue["C_PRJCT_UNIT"]))
            page.locator("//div[text()='Search and Select: Project Unit']//following::label[text()='Name']//following::input[1]").click()
            page.locator("//div[text()='Search and Select: Project Unit']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_PRJCT_UNIT"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRJCT_UNIT"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)
            page.get_by_title("Search: Organization").click()
            page.get_by_role("link", name="Search...").click()
            # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").click()
            # # page.get_by_role("textbox", name="Name").click()
            # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").fill(str(datadictvalue["C_ORGNZTN"]))
            page.locator("//div[text()='Search and Select: Organization']//following::label[text()='Name']//following::input[1]").click()
            page.locator("//div[text()='Search and Select: Organization']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_ORGNZTN"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ORGNZTN"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

            page.get_by_title("Search: Legal Entity").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Legal Entity").click()
            page.get_by_role("textbox", name="Legal Entity").fill(str(datadictvalue["C_LEGAL_ENTTY"]))
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LEGAL_ENTTY"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(2000)

            page.get_by_title("Search: Project Type").click()
            page.get_by_role("link", name="Search...").click()
            # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").click()
            # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").fill(str(datadictvalue["C_PRJCT_TYPE"]))
            page.locator("//div[text()='Search and Select: Project Type']//following::label[text()='Name']//following::input[1]").click()
            page.locator("//div[text()='Search and Select: Project Type']//following::label[text()='Name']//following::input[1]").fill(str(datadictvalue["C_PRJCT_TYPE"]))
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRJCT_TYPE"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

            page.get_by_label("Initial Project Status").click()
            page.get_by_label("Initial Project Status").select_option(datadictvalue["C_INTL_PRJCT_STTS"])
            page.wait_for_timeout(2000)

            # Entering From & To Date
            # page.get_by_role("row", name="From Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"])
            page.locator("//label[text()='From Date']//following::input[1]").nth(0).fill(datadictvalue["C_FROM_DATE"])

            if datadictvalue["C_TO_DATE"] != '':
                # page.get_by_role("row", name="To Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"])
                page.locator("//label[text()='To Date']//following::input[1]").nth(0).fill(datadictvalue["C_TO_DATE"])
            page.wait_for_timeout(2000)

            # Enable Sponsor Project
            # if datadictvalue["C_SPNSRD_PRJCT"] == 'Yes':
            #     page.get_by_role("cell", name="Sponsored Project").check()
            #     page.wait_for_timeout(2000)
            page.get_by_role("button", name="Save and Continue").click()
            page.wait_for_timeout(2000)
    ###-------------------------------------###
            #####Basic Information Update#####

            page.wait_for_timeout(2000)
            page.get_by_role("link", name="Go to Project Setup Options").click()
            page.wait_for_timeout(2000)
            #- page.get_by_role("link", name="Basic Information").click()
            #- page.get_by_role("row", name="Collapse Basic Information Basic Information Edit", exact=True).get_by_role("button").nth(1).click()
            page.locator("//h1[text()='Basic Information']//following::button[@title='Edit']").first.click()
            page.wait_for_timeout(2000)
            page.get_by_label("Priority").select_option(datadictvalue["C_PRRTY"])
            page.wait_for_timeout(2000)
            page.get_by_label("Outline Display Level").fill(str(datadictvalue["C_OTLN_DSPLY_LEVEL"]))
            page.wait_for_timeout(2000)

            # page.get_by_role("cell", name="Cascade Option", exact=True).nth(1).click()
            page.get_by_label("Cascade Option").click()
            page.locator("//label[text()='Cascade Option']//following::select[1]").select_option(datadictvalue["C_CSCD_OPTN"])
            page.wait_for_timeout(2000)
            if datadictvalue["C_WORK_TYPE"] !='':
                page.get_by_role("cell", name="Work Type", exact=True).click()
                page.get_by_label("Work Type").select_option(datadictvalue["C_WORK_TYPE"])
                page.wait_for_timeout(2000)

            # Entering Start Date
            if datadictvalue["C_START_DATE"] != '':
                #- page.get_by_role("row", name="*Start Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_START_DATE"])
                page.locator("//label[text()='Start Date']//following::input[1]").nth(1).fill(datadictvalue["C_START_DATE"])

            if page.locator("//label[text()='Planned Start Date']//following::input[1]").nth(1).is_visible():
                if datadictvalue["C_PLNND_START_DATE"] != '':
                    page.locator("//label[text()='Planned Start Date']//following::input[1]").nth(1).fill(datadictvalue["C_PLNND_START_DATE"])
            page.wait_for_timeout(2000)

            if datadictvalue["C_PLNNNG_PRJCT"] == 'Yes':
                #- page.get_by_role("cell", name="Planning project", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text("Planning project").check()
                page.wait_for_timeout(2000)

            if datadictvalue["C_WORK_TYPE"] !='':
                page.get_by_role("cell", name="Work Type", exact=True).click()
                page.get_by_label("Work Type").select_option(datadictvalue["C_WORK_TYPE"])
                page.wait_for_timeout(2000)
            if datadictvalue["C_SRVC_TYPE"] != '':
                page.get_by_role("cell", name="Service Type", exact=True).nth(2).click()
                page.get_by_label("Service Type").select_option(datadictvalue["C_SRVC_TYPE"])
                page.wait_for_timeout(2000)

            # Entering Finish Date
            if datadictvalue["C_FNSH_DATE"] != '':
                #- page.get_by_role("row", name="*Finish Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FNSH_DATE"])
                page.locator("(//label[text()='Finish Date'])[2]//following::input[1]").fill(datadictvalue["C_FNSH_DATE"])
            if page.locator("(//label[text()='Planned Finish Date'])[2]//following::input[1]").is_visible():
                if datadictvalue["C_PLNND_FNSH_DATE"] != '':
                    page.locator("(//label[text()='Planned Finish Date'])[2]//following::input[1]").fill(datadictvalue["C_PLNND_FNSH_DATE"])
                    page.wait_for_timeout(2000)

            if datadictvalue["C_ENBL_BDGTRY_CNTRL"] == 'Yes':
                page.locator("//label[text() = 'Enable budgetary control']").check()
                page.wait_for_timeout(2000)
                if page.get_by_role("button", name="Yes").is_visible():
                    page.get_by_role("button", name="Yes").click()
            if datadictvalue["C_ENBL_BDGTRY_CNTRL"] == 'No':
                page.locator("//label[text() = 'Enable budgetary control']").uncheck()
                page.wait_for_timeout(2000)

            # # Save the data
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)

            ###Add Project Plan Type before adding Project Plan###
            #####Project Plan Type#####
            page.get_by_text("Add", exact=True).click()
            page.wait_for_timeout(2000)

            #Adding Project Plan Type
            page.get_by_title("Search: Name").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Name").click()
            page.get_by_role("textbox", name="Name").fill(datadictvalue["C_PRJCT_PLAN_TYPE"])
            page.get_by_role("button", name="Search", exact=True).click()
            #- page.get_by_role("cell", name=datadictvalue["C_PRJCT_PLAN_TYPE"], exact=True).locator("span").click()
            page.get_by_role("cell", name=datadictvalue["C_PRJCT_PLAN_TYPE"]).nth(1).click()
            # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRJCT_PLAN_TYPE"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            # page.wait_for_timeout(2000)

            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)

            #####TEAM MEMBERS#####
            if datadictvalue["C_RSRC"] != '':
                # page.get_by_role("row", name="Collapse Team Members Team Members Edit", exact=True).locator("button").click()
                page.locator("//div[@title='Team Members']//following::button[text()='Edit'][1]").click()
                page.get_by_role("button", name="Add Resource").click()

                    #Adding Resources
                page.get_by_title("Search: Resource").click()
                page.get_by_role("link", name="Search...").click()
                # page.get_by_role("textbox", name="Name").click()
                # page.get_by_role("textbox", name="Name").fill(datadictvalue["C_RSRC"])
                page.get_by_label("Name").click()
                page.get_by_label("Name").fill(datadictvalue["C_RSRC"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RSRC"], exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)

                page.get_by_role("combobox", name="Project Role").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRJCT_ROLE"], exact=True).click()
                page.wait_for_timeout(2000)
                if datadictvalue["C_TRACK_TIME"] == 'Yes':
                    page.get_by_role("cell", name="Track Time", exact=True).locator("label").check()
                page.wait_for_timeout(2000)
                if datadictvalue["C_EFFRT"] != '':
                    #- page.get_by_role("cell", name="Hours").nth(3).fill(str(datadictvalue["C_EFFRT"]))
                    page.locator("//div[text()='Add Project Resource']//following::label[text()='Effort']//following::input[1]").fill(str(datadictvalue["C_EFFRT"]))
                if datadictvalue["C_ALLCTN"] != '':
                    #-page.get_by_role("cell", name="%").nth(3).fill(str(datadictvalue["C_ALLCTN"]))
                    page.locator("//div[text()='Add Project Resource']//following::label[text()='Allocation']//following::input[1]").fill(str(datadictvalue["C_ALLCTN"]))
                # Save and close the Add Resource tab
                page.get_by_title("Save and Close").click()
                # Save and close the Resource tab
                # page.get_by_role("cell", name="Save and Close", exact=True).locator("div").click()
                page.get_by_role("button", name="Save", exact=True).click()
                page.get_by_role("button", name="Save and Close").click()

            #####Project Customers#####
            if datadictvalue["C_PC_NAME"] != '':
                page.get_by_role("button", name="Add Row").first.click()
                page.wait_for_timeout(3000)

                page.get_by_label("Name").fill(datadictvalue["C_PC_NAME"])
                page.get_by_label("Name").press("Tab")
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(3000)

            #####Partner Organizations#####
            if datadictvalue["C_PO_NAME"] != '':
                page.get_by_role("button", name="Add").nth(1).click()
                page.wait_for_timeout(3000)

                page.get_by_label("Name").fill(datadictvalue["C_PO_NAME"])
                page.get_by_label("Name").press("Tab")
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(2000)

            #####Supplier Organizations#####
            if datadictvalue["C_SO_NAME"] != '':
                page.get_by_role("button", name="Add").nth(2).click()
                page.wait_for_timeout(2000)

                page.get_by_label("Name").fill(datadictvalue["C_SO_NAME"])
                page.get_by_label("Name").press("Tab")
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(2000)

            #####Project Classifications#####
            if datadictvalue["C_CLASS_CTGRY"] != '':
                page.get_by_role("row", name="Collapse Project Classifications Project Classifications Help Edit",exact=True).locator("button").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Add").click()
                page.get_by_label("Class Category").click()
                page.get_by_label("Class Category").select_option(datadictvalue["C_CLASS_CTGRY"])
                page.wait_for_timeout(3000)

                # Adding Class Code
                # page.get_by_title("Search: Class Code").click()
                # page.get_by_role("link", name="Search...").click()
                # page.get_by_role("textbox", name="Name").click()
                # page.get_by_role("textbox", name="Name").fill(datadictvalue["C_CLASS_CODE"])
                # page.get_by_role("button", name="Search", exact=True).click()
                # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CLASS_CODE"], exact=True).click()
                # page.get_by_text(datadictvalue["C_CLASS_CODE"]).nth(1).click()
                # page.page.get_by_role("button", name="OK").click()
                page.get_by_label("Class Code").fill(datadictvalue["C_CLASS_CODE"])
                page.wait_for_timeout(2000)
                page.get_by_label("Class Code").press("Tab")
                page.wait_for_timeout(2000)
                if datadictvalue["C_PRCNT"] !='':
                    page.get_by_label("Percent").fill(str(datadictvalue["C_PRCNT"]))
                page.get_by_role("button", name="Save and Close").click()

            #####Resource Breakdown Structures#####
            if datadictvalue["C_RBS_NAME"] != '':
                page.locator("//div[@title='Resource Breakdown Structures']//following::img[contains(@id,'icon')][1]").click()
                page.wait_for_timeout(3000)

                    #Adding RBS
                # page.get_by_title("Search: Name").click()
                # page.get_by_role("link", name="Search...").click()
                # page.get_by_role("textbox", name="Name").click()
                page.locator("//div[text()='Add Resource Breakdown Structure']//following::input[1]").click()
                page.locator("//div[text()='Add Resource Breakdown Structure']//following::input[1]").type(datadictvalue["C_RBS_NAME"])
                page.wait_for_timeout(2000)
                page.get_by_role("option", name=datadictvalue["C_RBS_NAME"]).click()
                page.wait_for_timeout(2000)
                # page.get_by_role("button", name="Search", exact=True).click()
                # page.pause()
                # page.get_by_role("cell", name=datadictvalue["C_RBS_NAME"], exact=True).locator("span").click()
                # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RBS_NAME"], exact=True).click()
                # page.get_by_role("button", name="OK").click()
                # page.get_by_label("Name").fill(datadictvalue["C_RBS_NAME"])
                # page.wait_for_timeout(2000)
                # page.get_by_label("Name").press("Tab")
                # page.get_by_role("row", name="*Usage", exact=True).get_by_label("Usage").select_option(datadictvalue["C_USG"])
                page.locator("// div[text() = 'Add Resource Breakdown Structure'] // following::label[text() = 'Usage'][3]").select_option(datadictvalue["C_USG"])
                page.get_by_role("button", name="Save and Close").click()

            #####Update Project Plan Types if required#####(Row 273-340:Till Additional Information)
            ### As discussed with Engg Team, there is a seperate task for Project Plan Types and all the updates will be handled in the Manage Project Plan Types task"
            ### So, if needed we can uncommand and use it for future reference
            # #page.get_by_role("row", name="Replace Edit", exact=True).get_by_role("button").nth(1).click()

            # if datadictvalue["C_ENBL_PLNNNG_IN_MLTPL_TRNSCTN_CRRNCS"] == 'Yes':
            #     page.get_by_text("Enable planning in multiple").click()
            # if datadictvalue["C_SCHDL_USING_THIRD_PARTY_SFTWR"] == 'Yes':
            #     page.get_by_text("Schedule using third-party").click()
            #
            # #\Plan Settings/#
            # page.get_by_role("link", name="Plan Settings").click()
            # if datadictvalue["C_ENBL_CSTS_FOR_PRJCT_PLAN"] == 'Yes':
            #     page.get_by_text("Enable costs for project plan").click()
            # if datadictvalue["C_SET_UNPLNND_SSGNMNTS_AS_PLNND_SSGNMNTS"] == 'Yes':
            #     page.get_by_text("Set unplanned assignments as").click()
            # page.get_by_label("Calendar Type").select_option(datadictvalue["C_CLNDR_TYPE"])
            # page.get_by_label("Rate Derivation Date Type").select_option(datadictvalue["C_RATE_DRVTN_DATE_TYPE"])
            # page.wait_for_timeout(3000)
            #
            # # \Task Settings/#
            # page.get_by_role("link", name="Task Settings").click()
            # if datadictvalue["C_USE_TASK_PLNND_DATES_AS_TASK_ASSGNMNT_DATES"] == 'Yes':
            #     page.get_by_text("Use task planned dates as").click()
            # if datadictvalue["C_SYNCHRNZ_TASK_TRNSCTN_DATES_WTH_PLNND_DATES"] == 'Yes':
            #     page.get_by_text("Synchronize task transaction").click()
            # if datadictvalue["C_ATMTCLLY_ROLL_UP_TASK_PLNND_DATES"] == 'Yes':
            #     page.get_by_text("Automatically roll up task").click()
            # page.get_by_label("Date Adjustment Buffer in Days").fill(str(datadictvalue["C_DATE_ADJSTMNT_BFFR_IN_DAYS"]))
            # page.wait_for_timeout(3000)
            #
            # # \Currency Settings/#
            # page.get_by_role("link", name="Currency Settings").click()
            # page.wait_for_timeout(2000)
            #
            # # \Rate Settings/#
            # page.get_by_role("link", name="Rate Settings").click()
            # page.wait_for_timeout(2000)
            #
            # # \Progress Settings/#
            # page.get_by_role("link", name="Progress Settings").click()
            # page.get_by_label("Physical Percent Complete Calculation Method").select_option(
            #     datadictvalue["C_PHYSCL_PRCNT_CMPLT_CLCLTN_MTHD"])
            # page.get_by_label("ETC Method").select_option(datadictvalue["C_ETC_MTHD"])
            # if datadictvalue["C_ALLW_NGTV_ETC_CLCLTN"] == 'Yes':
            #     page.get_by_text("Allow negative ETC calculation").click()
            # if datadictvalue["C_UPDT_PLNND_QNTTY_WITH_EAC_QNTTY"] == 'Yes':
            #     page.get_by_text("Update planned quantity with").click()
            # if datadictvalue["C_ATMTCLLY_GNRT_FRCST_VRSN"] == 'Yes':
            #     page.get_by_text("Automatically generate").click()
            # page.get_by_label("Primary Physical Percent").select_option(datadictvalue["C_PRMRY_PHYSCL_PRCNT_CMPLT_BASIS"])
            # page.wait_for_timeout(3000)C_PP_PLNND_START_DATE
            #
            # # \Budget Generation Options/#
            # page.get_by_role("link", name="Budget Generation Options").click()
            # if datadictvalue["C_GNRT_BDGT_VRSN_WHEN_STTNG_BSLN_FOR_PRJCT_PLAN"] == 'Yes':
            #     page.get_by_text("Generate budget version when").click()
            # page.get_by_label("Financial Plan Type").click()
            # page.get_by_label("Financial Plan Type").select_option(datadictvalue["C_FNNCL_PLAN_TYPE"])
            # if datadictvalue["C_ATMTCLLY_DSGNT_BDGT_VRSN_AS_BSLN"] == 'Yes':
            #     page.get_by_text("Automatically designate").click()
            # page.wait_for_timeout(2000)
            #
            # # \Additional Information/#
            # page.get_by_role("link", name="Additional Information").click()
            # page.wait_for_timeout(2000)
            # page.get_by_role("button", name="Save and Close").click()
            ##########Financial & Reporting tab fields as not required as confirmed by Engg team##########
            page.wait_for_timeout(4000)
            PrevName = datadictvalue["C_NAME"]
            print("Name:", PrevName)

        #####Project Plan#####
        page.locator("// div[ @ title = 'Project Plan'] // following::div[ @ title = 'Edit']").first.click()
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Create Task").click()
        page.wait_for_timeout(2000)
        #- page.get_by_role("cell", name="Subtask", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text("Subtask").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Task Number", exact=True)
        page.get_by_label("Task Number", exact=True).fill(str(datadictvalue["C_TASK_NMBR"]))
        page.wait_for_timeout(2000)
        page.get_by_label("Task Name").click()
        page.get_by_label("Task Name").fill(datadictvalue["C_TASK_NAME"])
        page.wait_for_timeout(2000)

        # Entering planned Date
        page.locator("(//a[@title='Select Date']//preceding::input[@placeholder='m/d/yy'])[1]").click()
        page.locator("(//a[@title='Select Date']//preceding::input[@placeholder='m/d/yy'])[1]").fill(datadictvalue["C_PP_PLNND_START_DATE"])
        page.locator("(//a[@title='Select Date']//preceding::input[@placeholder='m/d/yy'])[2]").click()
        page.locator("(//a[@title='Select Date']//preceding::input[@placeholder='m/d/yy'])[2]").clear()
        page.locator("(//a[@title='Select Date']//preceding::input[@placeholder='m/d/yy'])[2]").fill(datadictvalue["C_PP_PLNND_FNSH_DATE"])
        page.locator("(//a[@title='Select Date']//preceding::input[@placeholder='m/d/yy'])[2]").press("Tab")
        page.wait_for_timeout(2000)

        # #Below fields were autopopulated, if needed we can uncommand and use it for future ref
        # #C_TASK_MNGR
        # #C_TRNSCTN_CNTRLS
        # #C_TRNSCTN_STRT_DATE
        # #C_TRNSCTN_FNSH_DATE
        # #C_ADDTNL_INFRMTN
        # #C_TASK
        if datadictvalue["C_BLBLE"] == 'Yes':
            page.locator("//table[@summary='Manage Project Plan']//following::input[@type='checkbox']//following::label").nth(0).click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_CHRGBL"] == 'Yes':
            page.locator("//table[@summary='Manage Project Plan']//following::input[@type='checkbox']//following::label").nth(1).click()
        page.wait_for_timeout(2000)
        # #Below columns were not editable
        # #C_CRTCL
        # #C_MLSTN

        if datadictvalue["C_RCV_INTRCMPNY_AND_INTRPRJCT_INVCS"] == 'Yes':
            page.locator("//table[@summary='Manage Project Plan']//following::input[@type='checkbox']//following::label").nth(4).click()
            page.wait_for_timeout(2000)
        if datadictvalue["C_PP_SRVC_TYPE"] != '':
            page.get_by_label("Service Type").select_option(datadictvalue["C_PP_SRVC_TYPE"])
            page.wait_for_timeout(2000)
        if datadictvalue["C_WRK_TYPE"] != '':
            page.get_by_label("Work Type").select_option(datadictvalue["C_WRK_TYPE"])
            page.wait_for_timeout(2000)
        if datadictvalue["C_PP_SRVC_TYPE"] != '':
            page.get_by_label("Physical Percent Complete").select_option(datadictvalue["C_PP_SRVC_TYPE"])
            page.wait_for_timeout(2000)
        if datadictvalue["C_PLNND"] != '':
            page.get_by_label("Planned", exact=True).fill(str(datadictvalue["C_PLNND"]))
            #C_ITD_ACTL
            page.wait_for_timeout(2000)
        if datadictvalue["C_PLNND_IN_PRJCT_CRRNCY"] != '':
            page.get_by_label("Planned in Project Currency", exact=True).fill(str(datadictvalue["C_PLNND_IN_PRJCT_CRRNCY"]))
            #C_ITD_ACTL_IN_PRJCT_CRRNCY_SD
            page.wait_for_timeout(2000)

        #Save and close the task details tab
        page.get_by_role("button", name="Save and Close", exact=True).click()

        #####In Future if needed, we need to add other tabs like Partner Organizations, Supplier Organizations columns in the loop#####

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        if i == rowcount:
            page.get_by_role("button", name="Done").click()
            page.wait_for_timeout(2000)
            page.get_by_title("Save").click()
            page.wait_for_timeout(2000)
            # page.get_by_role("cell", name="Save and Close", exact=True).click()
            page.get_by_text("Save and Close").click()
            page.wait_for_timeout(2000)

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Project Templates Saved Successfully")
            datadictvalue["RowStatus"] = "Project Templates  are added successfully"

        except Exception as e:
            print("Project Statuses not saved")
            datadictvalue["RowStatus"] = "Project Templates  are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJ_TMPLT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJ_TMPLT, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJ_TMPLT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + PRJ_TMPLT)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + PRJ_TMPLT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))