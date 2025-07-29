from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill("CURTIS.FEITTY")
    page.get_by_placeholder("Password").fill("j2#sr#3D")
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("My Client Groups", exact=True).click()
    page.get_by_role("link", name="Learning").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Courses").click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)

        # Title
        page.get_by_label("Title",exact=True).clear()
        page.get_by_label("Title",exact=True).type(datadictvalue["C_TITLE"])

        # Syllabus
        page.get_by_label("Editor editing area: main").click()
        page.get_by_label("Editor editing area: main").type(datadictvalue["C_SYLLBS"])

        # Short Description
        page.get_by_label("Short Description").clear()
        page.get_by_label("Short Description").type(datadictvalue["C_SHORT_DSCRPTN"])

        # Publish Start Date
        if datadictvalue["C_PBLSH_START_DATE"]!='':
            page.locator("//label[text()='Publish Start Date']//following::input[1]").clear()
            page.locator("//label[text()='Publish Start Date']//following::input[1]").type(str(datadictvalue["C_PBLSH_START_DATE"]))

        # Publish End Date
        if datadictvalue["C_PBLSH_END_DATE"] != '':
            page.locator("//label[text()='Publish End Date']//following::input[1]").clear()
            page.locator("//label[text()='Publish End Date']//following::input[1]").type(str(datadictvalue["C_PBLSH_END_DATE"]))

        # Minimum Expected Effort
        if datadictvalue["C_MNMM_EXPCTD_HOURS"]!='':
            page.get_by_label("Minimum Expected Effort").clear()
            page.get_by_label("Minimum Expected Effort").type(str(datadictvalue["C_MNMM_EXPCTD_HOURS"]))

        # Maximum Expected Effort
        if datadictvalue["C_MXMM_EXPCTD_HOURS"]!='':
            page.get_by_label("Maximum Expected Effort").clear()
            page.get_by_label("Maximum Expected Effort").type(str(datadictvalue["C_MXMM_EXPCTD_HOURS"]))

        # Currency
        if datadictvalue["C_CRRNCY"]!='':
            page.locator("//label[text()='Currency']//following::input[1]").click()
            page.get_by_text(datadictvalue["C_CRRNCY"]).click()

        # Minimum Price
        if datadictvalue["C_MNMM_PRICE"]!='':
            page.get_by_label("Minimum Price").clear()
            page.get_by_label("Minimum Price").type(str(datadictvalue["C_MNMM_PRICE"]))

        # Maximum Price
        if datadictvalue["C_MXMM_PRICE"]!='':
            page.get_by_label("Maximum Price").clear()
            page.get_by_label("Maximum Price").type(str(datadictvalue["C_MXMM_PRICE"]))

        # Branding Image
        with page.expect_file_chooser() as fc_info:
            # page.get_by_role("img", name="Drag files here or click to").nth(2).click(force=True)
            page.locator("//label[text()='Branding Image']//following::span[text()='Drag files here or click to add attachment'][1]").click(force=True)
            page.wait_for_timeout(3000)
        file_chooser = fc_info.value
        file_chooser.set_files("attachment/Sample.jpg")
        page.wait_for_timeout(5000)

        # Trailer
        with page.expect_file_chooser() as fc_info:
            # page.get_by_role("img", name="Drag files here or click to").nth(3).click(force=True)
            page.locator("//label[text()='Trailer']//following::span[text()='Drag files here or click to add attachment'][1]").click(force=True)
            page.wait_for_timeout(3000)
        file_chooser = fc_info.value
        file_chooser.set_files("attachment/Video_test.mp4")
        page.wait_for_timeout(5000)

        # Override conversation system setup configuration
        if datadictvalue["C_OVRRD_CNVRSTN_SYSTM_SETUP_CNFGRTN"]!='':
            if datadictvalue["C_OVRRD_CNVRSTN_SYSTM_SETUP_CNFGRTN"]=='Yes':
                page.get_by_text("Override conversation system setup configuration",exact=True).check()
            if datadictvalue["C_OVRRD_CNVRSTN_SYSTM_SETUP_CNFGRTN"]=='No':
                page.get_by_text("Override conversation system setup configuration",exact=True).uncheck()

            page.wait_for_timeout(2000)

            if datadictvalue["C_ENBL_CNVRSTN_FOR_SELF_SRVC_USERS_ON_THE_CTLG_PAGE"] != '':
                if datadictvalue["C_ENBL_CNVRSTN_FOR_SELF_SRVC_USERS_ON_THE_CTLG_PAGE"] == 'Yes':
                    page.get_by_text("Enable conversations for self service users on the catalog page", exact=True).check()
                if datadictvalue["C_ENBL_CNVRSTN_FOR_SELF_SRVC_USERS_ON_THE_CTLG_PAGE"] == 'No':
                    page.get_by_text("Enable conversations for self service users on the catalog page", exact=True).uncheck()

        # Learning Item Additional Attributes
        if page.get_by_title("Search: Topic").is_visible():
            page.get_by_title("Search: Topic").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Translated Value").clear()
            page.get_by_label("Translated Value").type(datadictvalue["C_TOPIC"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TOPIC"]).click()
            page.get_by_role("button", name="OK").click()

        # Click on Save button
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(5000)

        # Click on Prerequisite link - New workbook below commanded column names are not available
        # if datadictvalue["C_LCNS_OR_CRTFCT_ONE"]!='':
        #
        #     page.get_by_role("link", name="Prerequisites").click()
        #     page.wait_for_timeout(5000)
        #
        #     # Adding Licenses and Certifications
        #     page.get_by_role("link", name="Add Content").click()
        #     page.get_by_role("cell", name="Licenses and Certifications", exact=True).click()
        #
        #     # Click on Add button
        #     page.get_by_role("link", name="Add", exact=True).click()
        #     # Adding License
        #     page.get_by_title("Search: License or Certificate").click()
        #     page.get_by_role("link", name="Search...").click()
        #     page.get_by_label("Name").clear()
        #     page.get_by_label("Name").type(datadictvalue["C_LCNS_OR_CRTFCT_ONE"])
        #     page.get_by_role("button", name="Search", exact=True).click()
        #     page.wait_for_timeout(3000)
        #     page.get_by_text(datadictvalue["C_LCNS_OR_CRTFCT_ONE"],exact=True).click()
        #     page.get_by_role("button", name="OK").click()
        #     page.wait_for_timeout(3000)
        #     if datadictvalue["C_RQRD_ONE"]!='':
        #         if datadictvalue["C_RQRD_ONE"]=='Yes':
        #             page.locator("//span[text()='Required']//following::label[2]").check()
        #         if datadictvalue["C_RQRD_ONE"]=='No':
        #             page.locator("//span[text()='Required']//following::label[2]").uncheck()
        #
        #     # Click on Save button
        #     page.get_by_role("button", name="Save", exact=True).click()
        #     page.wait_for_timeout(5000)
        #
        #     # Learning OutComes
        #     page.get_by_role("link", name="Learning Outcomes").click()
        #     page.wait_for_timeout(2000)
        #     page.get_by_role("link", name="Add Content").click()
        #     page.get_by_role("cell", name="Licenses and Certifications", exact=True).click()
        #     page.get_by_role("link", name="Add", exact=True).click()
        #
        #     ### License or Certificate
        #     page.get_by_title("Search: License or Certificate").click()
        #     page.get_by_role("link", name="Search...").click()
        #     page.get_by_label("Name").clear()
        #     page.get_by_label("Name").type(datadictvalue["C_LCNSE_OR_CRTFCTE_TWO"])
        #     page.get_by_role("button", name="Search", exact=True).click()
        #     page.wait_for_timeout(3000)
        #     page.get_by_text(datadictvalue["C_LCNSE_OR_CRTFCTE_TWO"]).click()
        #     page.get_by_role("button", name="OK").click()
        #     page.wait_for_timeout(2000)
        #     ### Certificate No
        #     page.get_by_label("CERTIFICATION_NUMBER").clear()
        #     page.get_by_label("CERTIFICATION_NUMBER").type(str(datadictvalue["C_CRFCT_NMBR"]))
        #
        #     ### Issue Date
        #     page.get_by_role("cell",name="m/d/yy Press down arrow to access Calendar ISSUE_DATE Select Date").get_by_placeholder("m/d/yy").clear()
        #     page.get_by_role("cell",name="m/d/yy Press down arrow to access Calendar ISSUE_DATE Select Date").get_by_placeholder("m/d/yy").type(datadictvalue["C_ISSUE_DATE"])
        #
        #     ### Expiration Date
        #     page.get_by_role("cell",name="m/d/yy Press down arrow to access Calendar EXPIRATION_DATE Select Date").get_by_placeholder("m/d/yy").click()
        #     page.get_by_role("cell",name="m/d/yy Press down arrow to access Calendar EXPIRATION_DATE Select Date").get_by_placeholder("m/d/yy").type(datadictvalue["C_EXPRTN_DATE"])
        #
        #     ### Renewal Required
        #     if datadictvalue["C_RNWL_RQRD"]!='':
        #         if datadictvalue["C_RNWL_RQRD"]=='Yes':
        #             page.get_by_role("combobox", name="No").click()
        #             page.get_by_text(datadictvalue["C_RNWL_RQRD"]).click()
        #         if datadictvalue["C_RNWL_RQRD"]=='No':
        #             page.get_by_role("combobox", name="No").click()
        #             page.get_by_text(datadictvalue["C_RNWL_RQRD"]).click()
        #
        #     # Click on Save button
        #     page.get_by_role("button", name="Save", exact=True).click()
        #     page.wait_for_timeout(5000)

        # Default Offering Attributes
        page.get_by_role("link", name="Default Offering Attributes").click()
        page.wait_for_timeout(2000)

        if datadictvalue["C_FCLTTR_TYPE"]!='':

            ### Facilitator type : Instructor
            if datadictvalue["C_FCLTTR_TYPE"]=='Instructor':
                page.get_by_role("combobox", name="Facilitator Type").click()
                page.get_by_text(datadictvalue["C_FCLTTR_TYPE"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_title("Search: Primary Instructor").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Name", exact=True).type(datadictvalue["C_PRMRY_INSTRCTR_NAME"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.wait_for_timeout(3000)
                page.get_by_role("cell", name=datadictvalue["C_PRMRY_INSTRCTR_NAME"], exact=True).locator("span").click()
                page.get_by_role("button", name="OK").click()

            ### Facilitator type : Training Supplier
            if datadictvalue["C_FCLTTR_TYPE"] == 'Training Supplier':
                page.get_by_role("combobox", name="Facilitator Type").click()
                page.get_by_text(datadictvalue["C_FCLTTR_TYPE"], exact=True).click()
                page.get_by_title("Search: Training Supplier Name").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Name", exact=True).type(datadictvalue["C_TRNNG_SPPLR_NAME"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.wait_for_timeout(3000)
                page.get_by_role("cell", name=datadictvalue["C_TRNNG_SPPLR_NAME"], exact=True).locator("span").click()
                page.get_by_role("button", name="OK").click()

                ### Currency
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Currency").click()
                page.get_by_text(datadictvalue["C_CRRNCY_ONE"], exact=True).click()

                ### Add Items
                page.get_by_role("button", name="Add Line Item").click()
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Line Item").click()
                page.get_by_text(datadictvalue["C_LINE_ITEM"],exact=True).click()
                page.get_by_role("textbox").clear()
                page.get_by_role("textbox").type(str(datadictvalue["C_PRICE"]))
                if datadictvalue["C_RQRD_TWO"]=='Yes':
                    page.locator("//h1[text()='Payment']//preceding::label[2]").check()
                if datadictvalue["C_RQRD_TWO"] =='No':
                    page.locator("//h1[text()='Payment']//preceding::label[2]").check()

            # Payment
            ### Payment Type
            if datadictvalue["C_PYMNT_TYPE"]=='No Payment':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Payment Type").click()
                page.get_by_text(datadictvalue["C_PYMNT_TYPE"]).click()

            if datadictvalue["C_PYMNT_TYPE"]=='Manual Payment':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Payment Type").click()
                page.get_by_text(datadictvalue["C_PYMNT_TYPE"]).click()
                page.wait_for_timeout(2000)

                # Require purchase order information
                if datadictvalue["C_RQR_PRCHS_ORDER_INFRM"]!='':
                    if datadictvalue["C_RQR_PRCHS_ORDER_INFRM"]=='Yes':
                        page.locator("//span[text()='Require purchase order information']//preceding::label[1]").check()
                    if datadictvalue["C_RQR_PRCHS_ORDER_INFRM"]=='No':
                        page.locator("//span[text()='Require purchase order information']//preceding::label[1]").uncheck()

                # Enable refunds on withdrawal from instructor-led and blended offerings
                if datadictvalue["C_RFNDS_ON_WTHDRWL"]!='':
                    if datadictvalue["C_RFNDS_ON_WTHDRWL"]=='No':
                        page.locator("//span[text()='Enable refunds on withdrawal from instructor-led and blended offerings']//preceding::label[1]").uncheck()
                    if datadictvalue["C_RFNDS_ON_WTHDRWL"]=='Yes':
                        page.locator("//span[text()='Enable refunds on withdrawal from instructor-led and blended offerings']//preceding::label[1]").check()
                        page.wait_for_timeout(3000)
                        page.locator("//span[text()='Days before offering starts to get a full refund']//following::input[1]").clear()
                        page.locator("//span[text()='Days before offering starts to get a full refund']//following::input[1]").type(str(datadictvalue["C_DAYS_BFR_OFFRNG_RFND"]))

                # Enable refunds on withdrawal from self-paced offerings
                if datadictvalue["C_RFNDS_ON_WTHDRWL_FROM_SELF_PACED_OFFRNGS"]!='':
                    if datadictvalue["C_RFNDS_ON_WTHDRWL_FROM_SELF_PACED_OFFRNGS"]=='No':
                        page.locator("//span[text()='Enable refunds on withdrawal from self-paced offerings']//preceding::label[1]").uncheck()
                    if datadictvalue["C_RFNDS_ON_WTHDRWL_FROM_SELF_PACED_OFFRNGS"]=='Yes':
                        page.locator("//span[text()='Enable refunds on withdrawal from self-paced offerings']//preceding::label[1]").check()
                        page.wait_for_timeout(3000)
                        page.locator("//span[text()='Maximum number of days after assignment start date']//following::input[1]").clear()
                        page.locator("//span[text()='Maximum number of days after assignment start date']//following::input[1]").type(str(datadictvalue["C_MXMM_NMBR_OF_DAYS_AFTER_ASSGNMNT_START_DATE"]))

            # Capacity Rules
            if datadictvalue["C_CPCTY_RULES"]!='':
                page.locator("label").filter(has_text="Capacity Rules").click()
                page.wait_for_timeout(2000)

                page.locator("//label[text()='Minimum Capacity']//following::input[1]").clear()
                page.locator("//label[text()='Minimum Capacity']//following::input[1]").type(str(datadictvalue["C_MNMM_CPCTY"]))

                page.locator("//label[text()='Maximum Capacity']//following::input[1]").clear()
                page.locator("//label[text()='Maximum Capacity']//following::input[1]").type(str(datadictvalue["C_MXMM_CPCTY"]))

                if datadictvalue["C_ALLOW_JNNG_THE_WTLST_FROM_SELF_SRVC"]!='':
                    if datadictvalue["C_ALLOW_JNNG_THE_WTLST_FROM_SELF_SRVC"] == 'Yes':
                        page.get_by_text("Allow joining the waitlist").check()
                    if datadictvalue["C_ALLOW_JNNG_THE_WTLST_FROM_SELF_SRVC"] == 'No':
                        page.get_by_text("Allow joining the waitlist").uncheck()

            # Click on Save button
            page.get_by_role("button", name="Save", exact=True).click()
            page.wait_for_timeout(5000)

        # Communities
        page.get_by_role("link", name="Communities").click()

        # Click on Save button
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(5000)

        # Default Assignment Rules
        page.get_by_role("link", name="Default Assignment Rules").click()

        if datadictvalue["C_INTL_ASSGNMNT_STTS"]=='Active':
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Initial Assignment Status']//following::input[1]").click()
            page.get_by_text(datadictvalue["C_INTL_ASSGNMNT_STTS"]).click()
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Validity Period Starts']//following::input[1]").click()
            page.get_by_text(datadictvalue["C_VLDTY_PRD_STRTS"], exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Validity Period Expires']//following::input[1]").click()
            page.get_by_text(datadictvalue["C_VLDTY_PRD_EXPRS"]).click()

        if datadictvalue["C_INTL_ASSGNMNT_STTS"]=='Bypass Completed':
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Initial Assignment Status']//following::input[1]").click()
            page.get_by_text(datadictvalue["C_INTL_ASSGNMNT_STTS"]).click()

            # Reason for Completion
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="DefaultInitialReasonCode").click()
            page.get_by_text(datadictvalue["C_RSN_FOR_CMPLTN"]).click()

            # Completion Date
            page.get_by_role("textbox", name="m/d/yy").click()
            page.get_by_role("textbox", name="m/d/yy").type(datadictvalue["C_CMPLTN_DATE"])

            # Actual Effort
            page.locator("//label[text()='Actual Effort']//following::input[1]").clear()
            page.locator("//label[text()='Actual Effort']//following::input[1]").type(str(datadictvalue["C_ACTL_EFFRT"]))

            # Actual Score
            page.locator("//label[text()='Actual Score']//following::input[1]").clear()
            page.locator("//label[text()='Actual Score']//following::input[1]").type(str(datadictvalue["C_ACTL_SCORE"]))

            # Validity Period Starts
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Validity Period Starts']//following::input[1]").click()
            page.get_by_text(datadictvalue["C_VLDTY_PRD_STRTS"], exact=True).click()

            # Validity Period Expires
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Validity Period Expires']//following::input[1]").click()
            page.get_by_text(datadictvalue["C_VLDTY_PRD_EXPRS"]).click()

            if datadictvalue["C_VLDTY_PRD_EXPRS"] == 'Expires on date':
                # Validity Period Expires Date
                page.get_by_role("row", name="m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").click()
                page.get_by_role("row", name="m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").type(datadictvalue["C_VLDTY_PRD_EXPRS_DATE"])

                # Valid Until the Selected Date, Every
                page.wait_for_timeout(2000)
                page.get_by_role("row",name="Expires on date m/d/yy Press down arrow to access Calendar Select Date Valid Until the Selected Date, Every",exact=True).get_by_role("combobox").nth(1).click()
                page.get_by_text(datadictvalue["C_VALID_UNTIL_THE_SLCTD_DATE_EVERY"], exact=True).click()

            if datadictvalue["C_VLDTY_PRD_EXPRS"] == 'Expires in years':
                # Validity for
                page.wait_for_timeout(2000)
                page.get_by_role("combobox").nth(3).click()
                page.get_by_text(datadictvalue["C_VALID_UNTIL_THE_SLCTD_DATE_EVERY"], exact=True).click()

            # Renewal Options
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Renewal Options']//following::input[1]").click()
            page.get_by_text(datadictvalue["C_RNWL_OPTNS"], exact=True).click()

            if datadictvalue["C_RNWL_OPTNS"] == 'Start next renewal after due date of prior assignment':
                # Renewal Period
                page.locator("// label[text() = 'Days After Due Date'] // preceding::input[1]").clear()
                page.locator("// label[text() = 'Days After Due Date'] // preceding::input[1]").type(
                    datadictvalue["C_RNWL_PRD"])

            if datadictvalue["C_RNWL_OPTNS"] == 'Start next renewal before validity of prior assignment ends':
                # Renewal Period
                page.locator("// label[text() = 'Days Before Validity Period Ends'] // preceding::input[1]").clear()
                page.locator("// label[text() = 'Days Before Validity Period Ends'] // preceding::input[1]").type(datadictvalue["C_RNWL_PRD"])

        if datadictvalue["C_INTL_ASSGNMNT_STTS"]=='Pending Fulfillment':
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Initial Assignment Status']//following::input[1]").click()
            page.get_by_text(datadictvalue["C_INTL_ASSGNMNT_STTS"]).click()

            # Validity Period Starts
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Validity Period Starts']//following::input[1]").click()
            page.get_by_text(datadictvalue["C_VLDTY_PRD_STRTS"], exact=True).click()

            # Validity Period Expires
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Validity Period Expires']//following::input[1]").click()
            page.get_by_text(datadictvalue["C_VLDTY_PRD_EXPRS"]).click()

            if datadictvalue["C_VLDTY_PRD_EXPRS"] == 'Expires on date':

                # Validity Period Expires Date
                page.get_by_role("row", name="m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").click()
                page.get_by_role("row", name="m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").type(datadictvalue["C_VLDTY_PRD_EXPRS_DATE"])

                # Valid Until the Selected Date, Every
                page.wait_for_timeout(2000)
                page.get_by_role("row",name="Expires on date m/d/yy Press down arrow to access Calendar Select Date Valid Until the Selected Date, Every",exact=True).get_by_role("combobox").nth(1).click()
                page.get_by_text(datadictvalue["C_VALID_UNTIL_THE_SLCTD_DATE_EVERY"], exact=True).click()

            if datadictvalue["C_VLDTY_PRD_EXPRS"] == 'Expires in years':

                # Validity for
                page.wait_for_timeout(2000)
                page.get_by_role("combobox").nth(3).click()
                page.get_by_text(datadictvalue["C_VALID_UNTIL_THE_SLCTD_DATE_EVERY"], exact=True).click()

            # Renewal Options
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Renewal Options']//following::input[1]").click()
            page.get_by_text(datadictvalue["C_RNWL_OPTNS"], exact=True).click()

            if datadictvalue["C_RNWL_OPTNS"]=='Start next renewal after due date of prior assignment':

                # Renewal Period
                page.locator("// label[text() = 'Days After Due Date'] // preceding::input[1]").clear()
                page.locator("// label[text() = 'Days After Due Date'] // preceding::input[1]").type(datadictvalue["C_RNWL_PRD"])

            if datadictvalue["C_RNWL_OPTNS"]=='Start next renewal before validity of prior assignment ends':

                # Renewal Period
                page.locator("// label[text() = 'Days Before Validity Period Ends'] // preceding::input[1]").clear()
                page.locator("// label[text() = 'Days Before Validity Period Ends'] // preceding::input[1]").type(str(datadictvalue["C_RNWL_PRD"]))

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        if page.get_by_role("link", name="Done").is_visible():
            page.get_by_role("link", name="Done").click()
        page.wait_for_timeout(3000)
        if page.get_by_role("link", name="Back").is_visible():
            page.get_by_role("link", name="Back").click()
            page.wait_for_timeout(3000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Courses")).to_be_visible()
            print("Course Saved Successfully")
            datadictvalue["RowStatus"] = "Course Saved Successfully"
        except Exception as e:
            print("Course not saved")
            datadictvalue["RowStatus"] = "Course not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, LA_COURSE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, LA_COURSE,PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK, LA_COURSE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[0] + "_" + LA_COURSE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))