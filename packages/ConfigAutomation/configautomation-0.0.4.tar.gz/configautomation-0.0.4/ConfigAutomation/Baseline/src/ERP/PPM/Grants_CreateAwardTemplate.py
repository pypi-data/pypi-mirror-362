from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(5000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Award Templates")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(1000)
    page.get_by_role("link", name="Manage Award Templates", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)
        ##-- page.get_by_role("cell", name="Create Award Template Close *").get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.locator("//div[text()='Create Award Template']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(2000)
        ##-- page.get_by_role("cell", name="Create Award Template Close *").get_by_label("Number").fill(datadictvalue["C_NMBR"])
        page.locator("//div[text()='Create Award Template']//following::label[text()='Number']//following::input[1]").fill(datadictvalue["C_NMBR"])
        page.wait_for_timeout(2000)

        # Select Business Unit
        page.get_by_title("Search: Business Unit").click()
        page.get_by_role("link", name="Search...").click()
        ##-- page.get_by_role("cell", name="*Name Name Name", exact=True).get_by_label("Name").fill(datadictvalue["C_AWARD_BSNSS_UNIT"])
        page.locator("//div[text()='Search and Select: Business Unit']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_AWARD_BSNSS_UNIT"])
        ##-- page.get_by_role("button", name="Search", exact=True).nth(1).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.locator("//div[text()='Search and Select: Business Unit']//following::span[text()='"+datadictvalue["C_AWARD_BSNSS_UNIT"]+"']").click()
        page.wait_for_timeout(2000)
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_AWARD_BSNSS_UNIT"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        ###Legal Entity & Currency will be auto-populated based on the selected Business Unit###
        # Select Primary Sponser
        if datadictvalue["C_PRMRY_SPNSR"] != '':
            page.get_by_title("Search: Primary Sponsor").click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//div[text()='Search and Select: Primary Sponsor']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_PRMRY_SPNSR"])
            ##-- page.get_by_role("cell",name="Search and Select: Primary Sponsor Close This table contains column headers").get_by_label("Name").fill(datadictvalue["C_PRMRY_SPNSR"])
            ##-- page.get_by_role("button", name="Search", exact=True).nth(1).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_PRMRY_SPNSR"], exact=True).locator("span").click()
            # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRMRY_SPNSR"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        # Entering Start & End Date
        page.locator("//label[text()='Start Date']//following::input[1]").nth(1).fill(datadictvalue["C_AWARD_START_DATE"])
        if datadictvalue["C_AWARD_END_DATE"] != '':
            ##-- page.get_by_role("row", name="End Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_AWARD_END_DATE"].strftime("%m/%d/%Y"))
            page.locator("//label[text()='End Date']//following::input[1]").nth(1).fill(datadictvalue["C_AWARD_END_DATE"])

        page.wait_for_timeout(2000)

        # Select Principal Investigator
        if datadictvalue["C_PRNCPL_INVSTGTR"] != '':
            page.get_by_title("Search: Principal Investigator").click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//div[text()='Search and Select: Principal Investigator']//following::label[text()='Name']").fill(datadictvalue["C_PRNCPL_INVSTGTR"])
            ##--page.get_by_role("cell", name="**Name Name Name **Email").get_by_label("Name").fill(datadictvalue["C_PRNCPL_INVSTGTR"])
            page.get_by_role("button", name="Search", exact=True).click()
            ##-- page.get_by_role("button", name="Search", exact=True).nth(1).click()
            # page.get_by_role("cell", name=datadictvalue["C_PRNCPL_INVSTGTR"], exact=True).locator("span").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRNCPL_INVSTGTR"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        # Save & Continue
        page.get_by_role("button", name="Save and Continue").click()
        page.wait_for_timeout(2000)

        #Additioanl updates if required
        if datadictvalue["C_DSCRPTN"] != '':
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(2000)
        if datadictvalue["C_CNTRCT_TYPE"] !='':
            page.get_by_label("Contract Type").select_option(datadictvalue["C_CNTRCT_TYPE"])
            page.wait_for_timeout(2000)

        #####Tab 1#General Tab#####
        page.get_by_role("link", name="General").click()

        # Select Principal Investigator
        page.get_by_title("Search: Organization").click()
        page.get_by_role("link", name="Search...").click()
        page.locator("//div[text()='Search and Select: Organization']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_ORGNZTN"])
        ## --page.get_by_role("cell", name="Name Name Name").get_by_label("Name").fill(datadictvalue["C_ORGNZTN"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ORGNZTN"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        page.get_by_label("Institution").select_option(datadictvalue["C_INSTTTN"])
        page.wait_for_timeout(2000)

        if datadictvalue["C_SPNSR_AWARD_NMBR"] != '':
            page.get_by_label("Sponsor Award Number").click()
            page.get_by_label("Sponsor Award Number").fill(datadictvalue["C_SPNSR_AWARD_NMBR"])
            page.wait_for_timeout(2000)

        if datadictvalue["C_PRPS"] != '':
            page.get_by_label("Purpose").select_option(datadictvalue["C_PRPS"])
            page.wait_for_timeout(2000)
        if datadictvalue["C_TYPE"] != '':
            page.get_by_label("Type", exact=True).select_option(datadictvalue["C_TYPE"])
            page.wait_for_timeout(2000)

        #CFDA Number Listing Number
        if datadictvalue["C_CFDA_NMBR"] != '':
            page.get_by_role("link", name="Manage Assistance Listing").click()
            page.get_by_label("Assistance Listing Numbers").fill(datadictvalue["C_CFDA_NMBR"])
            page.get_by_role("button", name="OK").click()

        #Quick Create Award Options
        if datadictvalue["C_SET_AS_DFLT_AWARD_TMPLT"] == 'Yes':
            if not page.get_by_text("Set as default award template").is_checked():
                page.get_by_text("Set as default award template").click()

        elif datadictvalue["C_SET_AS_DFLT_AWARD_TMPLT"] == 'No' or '':
            if page.get_by_text("Set as default award template").is_checked():
                page.get_by_text("Set as default award template").click()

        if datadictvalue["C_SBMT_CNTRCT_FOR_APPRVL"] == 'Yes':
            if not page.get_by_text("Submit contract for approval").is_checked():
                page.get_by_text("Submit contract for approval").click()

        elif datadictvalue["C_SBMT_CNTRCT_FOR_APPRVL"] == 'No' or '':
            if page.get_by_text("Submit contract for approval").is_checked():
                page.get_by_text("Submit contract for approval").click()

            # Select Project Template
        if datadictvalue["C_PRJCT_TMPLT"] != '':
            page.get_by_title("Search: Project Template").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("cell", name="Template Name").get_by_label("Template Name").fill(datadictvalue["C_PRJCT_TMPLT"])
            page.get_by_role("button", name="Search", exact=True).first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRJCT_TMPLT"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        #Keywords
        if datadictvalue["C_KEY_NAME"] != '':
            page.get_by_role("button", name="New").first.click()
            page.wait_for_timeout(2000)
            page.get_by_title("Search: Name").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("cell", name="Name").get_by_label("Name").fill(datadictvalue["C_KEY_NAME"])
            page.get_by_role("button", name="Search", exact=True).first.click()
            # page.get_by_role("cell", name=datadictvalue["C_KEY_NAME"], exact=True).locator("span").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_KEY_NAME"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        #Select Reference & Type
        if datadictvalue["C_RFRNC_TYPE"] != '':
            page.get_by_role("button", name="New").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_role("table", name="References").get_by_label("Name").fill(datadictvalue["C_RFRNC_TYPE"])
            page.wait_for_timeout(2000)
            page.get_by_label("Value").click()
            page.get_by_label("Value").fill(datadictvalue["C_RFRNC_VALUE"])

        #Attchment fields
        #C_A_TYPE
        #C_FILE_NAME_OR_URL
        #C_TITLE
        #C_DSCRPTN
        #C_ATTCHD_BY
        #C_ATTCHD_DATE

        #Additional Information
        page.get_by_label("Expand Additional Information").click()

        ###Add conflict of interest###
        page.get_by_role("link", name="Add conflict of interest").click()
        page.wait_for_timeout(2000)

        if datadictvalue["C_CMPLNT_WITH_INSTTTN_PLCY"] == 'YES' or 'Yes':
            page.get_by_text("Compliant with institution").click()

        if datadictvalue["C_CMPLNC_RVW_CMPLTD"] == 'YES' or 'Yes':
            page.get_by_text("Compliance review completed").click()

        if datadictvalue["C_APPRVL_DATE"] != '':
            page.locator("//label[text()='Approval Date']//following::input[1]").nth(0).fill(datadictvalue["C_APPRVL_DATE"].strftime("%m/%d/%Y"))
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        ###Add flow-through funds###
        page.get_by_role("link", name="Add flow-through funds").click()
        if datadictvalue["C_SPNSR"]!= '':
            page.get_by_label("Sponsor", exact=True).fill(datadictvalue["C_SPNSR"])

        if datadictvalue["C_RFRNC_AWARD_NAME"] != '':
            page.get_by_label("Reference Award Name").click()
            page.get_by_label("Reference Award Name").fill(datadictvalue["C_RFRNC_AWARD_NAME"])
            page.wait_for_timeout(2000)

        # Entering Start & End Date
        if datadictvalue["C_FTF_START_DATE"] != '':
            page.locator("//label[text()='Start Date']//following::input[1]").nth(1).fill(datadictvalue["C_FTF_START_DATE"].strftime("%m/%d/%Y"))
        if datadictvalue["C_FTF_END_DATE"] != '':
            page.locator("//label[text()='End Date']//following::input[1]").nth(1).fill(datadictvalue["C_FTF_END_DATE"].strftime("%m/%d/%Y"))
        page.wait_for_timeout(2000)

        if datadictvalue["C_AMNT"] != '':
            page.get_by_label("Amount").click()
            page.get_by_label("Amount").fill(str(datadictvalue["C_AMNT"]))
            page.wait_for_timeout(2000)

        if datadictvalue["C_FNDD_BY_FDRL_AGNCY"] == 'YES' or 'Yes':
            page.get_by_text("Funded by federal agency").click()
            page.wait_for_timeout(2000)

        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        ###Intellectual Property###
        page.get_by_role("link", name="Add intellectual property").click()
        page.wait_for_timeout(2000)

        if datadictvalue["C_INTLLCTL_PRPRTY_RPRTD"] == 'YES' or 'Yes':
            page.get_by_text("Intellectual property reported").click()
            page.wait_for_timeout(2000)

        if datadictvalue["C_IP_DSCRPTN"] != '':
            page.get_by_role("cell",name="Edit Intellectual Property Close Intellectual property reported Description OK").get_by_label("Description").fill(datadictvalue["C_IP_DSCRPTN"])
            page.wait_for_timeout(2000)

        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        ###Previous Award###
        page.get_by_role("link", name="Add previous award").click()

        if datadictvalue["C_BSNSS_UNIT"] != '':
            page.get_by_title("Search: Business Unit").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("cell", name="*Name Name Name", exact=True).get_by_label("Name").fill(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("//div[text()='Search and Select: Business Unit']//following::span[text()='" + datadictvalue["C_BSNSS_UNIT"] + "']").click()
            page.wait_for_timeout(2000)
            # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BSNSS_UNIT"], exact=True).click()
            page.get_by_role("button", name="OK").nth(1).click()
            page.wait_for_timeout(2000)

        if datadictvalue["C_PRVS_AWARD_NAME"] != '':
            page.get_by_title("Search: Previous Award Name").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("cell", name="**Name Name Name **Number", exact=True).get_by_label("Name").fill(datadictvalue["C_PRVS_AWARD_NAME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRVS_AWARD_NAME"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        if datadictvalue["C_RNWL_IN_PRGRSS"] == 'YES' or 'Yes':
            page.get_by_text("Renewal in progress").click()
            page.wait_for_timeout(2000)

        if datadictvalue["C_ACCMPLSHMNT_BASED_RNWL"] == 'YES' or 'Yes':
            page.get_by_text("Accomplishment-based renewal").click()
            page.wait_for_timeout(2000)

        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        ##DFF Information if any###
        if datadictvalue["C_ADDTNL_INFRMTN"] != '':
            page.get_by_label("Additional Information", exact=True).fill(datadictvalue["C_ADDTNL_INFRMTN"])
        if datadictvalue["C_FUND_DTLS"] != '':
            page.get_by_label("Fund Details").fill(datadictvalue["C_FUND_DTLS"])
        if datadictvalue["C_AWARD_ADDTNL_DTLS"] != '':
            page.get_by_label("Award Additional Details").select_option(datadictvalue["C_AWARD_ADDTNL_DTLS"])

        #####Tab 2#Financial Tab#####
        page.get_by_role("link", name="Financial").click()

        #General Info#
        page.get_by_title("Search: Burden Schedule").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(2000)
        page.locator("//div[text()='Search and Select: Burden Schedule']//following::label[text()='Name']//following::input[1]").clear()
        page.locator("//div[text()='Search and Select: Burden Schedule']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_BRDN_SCHDL"])
        ##-- page.get_by_role("cell", name="Name Name").nth(2).get_by_label("Name").clear()
        ##-- page.get_by_role("cell", name="Name Name").nth(2).get_by_label("Name").fill(datadictvalue["C_BRDN_SCHDL"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BRDN_SCHDL"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        if datadictvalue["C_EXPNDD_ATHRTY"] == 'YES' or 'Yes':
            page.get_by_text("Expanded authority").click()
            page.wait_for_timeout(2000)

        #Budget Period Definition
        page.get_by_label("Number of Budget Periods").fill(str(datadictvalue["C_NMBR_OF_BDGT_PRDS"]))
        page.wait_for_timeout(2000)
        #Period Frequency is defaulted
        if datadictvalue["C_USER_DFND_PRFX"] != '':
            page.get_by_label("User-Defined Prefix").fill(datadictvalue["C_USER_DFND_PRFX"])
        page.get_by_label("Separator").select_option(datadictvalue["C_SPRTR"])
        page.get_by_label("Format", exact=True).select_option(datadictvalue["C_FRMT"])
        page.wait_for_timeout(2000)
        #C_SMPL_NAME is defaulted based on the seleted Format

        if datadictvalue["C_COST_SHRD_BY_INTRNL_SRC"] == 'Yes' or 'YES':
            page.get_by_text("Cost shared by internal source").check()
        page.wait_for_timeout(2000)
        if datadictvalue["C_COST_SHRD_BY_INTRNL_SRC"] == 'No' or '':
            page.get_by_text("Cost shared by internal source").uncheck()
        page.wait_for_timeout(2000)

        # Organization Credits
        if datadictvalue["C_OC_ORGNZTN"] != '':
            page.get_by_role("button", name="New").click()
            page.wait_for_timeout(2000)
            page.get_by_title("Search: Organization").click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//div[text()='Search and Select: Organization']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_ORGNZTN"])
            ##--page.get_by_role("cell", name="Name Name Name", exact=True).get_by_label("Name").fill(datadictvalue["C_OC_ORGNZTN"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OC_ORGNZTN"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Percentage").fill(str(datadictvalue["C_PRCNTG"]))

        #####Tab 3#Compliance Tab#####
        if datadictvalue["C_TC_CTGRY"]!= '':
            page.get_by_role("link", name="Compliance").click()
            page.wait_for_timeout(2000)
            #Terms and Conditions
            page.get_by_role("button", name="New").first.click()
            page.wait_for_timeout(2000)
            page.get_by_label("Category").select_option(datadictvalue["C_TC_CTGRY"])
            # page.get_by_role("cell", name="Category", exact=True).select_option(datadictvalue["C_TC_CTGRY"])
            page.wait_for_timeout(2000)
            page.get_by_role("cell", name="Name Search: Name").click()
            page.wait_for_timeout(3000)
            #Name
            page.get_by_title("Search: Name").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("cell", name="Name Name Name Description", exact=True).get_by_label("Name").fill(datadictvalue["C_TC_NAME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TC_NAME"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)
            #Description is auto populated based on the selected name
            if datadictvalue["C_OPRTR"] != '':
                page.get_by_label("Operator").select_option(datadictvalue["C_OPRTR"])
            if datadictvalue["C_VALUE"] != '':
                page.get_by_label("Value").fill(datadictvalue["C_VALUE"])

        #Certifications
        if datadictvalue["C_TC_NAME"] != '':
            page.get_by_role("button", name="New").nth(1).click()
            page.get_by_title("Search: Name").nth(1).click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("cell", name="**Name Name Name **", exact=True).get_by_label("Name").fill(datadictvalue["C_TC_NAME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TC_NAME"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

            # Entering Certification Date
            page.locator("//a[@title='Search: Certified By']//preceding::input[3]").first.fill(datadictvalue["C_CRTFCTNS_DATE"].strftime("%m/%d/%Y"))

            if datadictvalue["C_CRTFD_BY"] != '':
                page.get_by_title("Search: Certified By").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_role("cell", name="**Name Name Name **Email", exact=True).get_by_label("Name").fill(datadictvalue["C_CRTFD_BY"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CRTFD_BY"], exact=True).click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)
            page.get_by_label("Status").select_option(datadictvalue["C_STTS"])
            page.wait_for_timeout(2000)

            # Entering Certification Approval Date
            if datadictvalue["C_CRTFCTN_APPRVL_DATE"] != '':
                page.locator("//a[@title='Search: Certified By']//following::input[1]").nth(0).fill(datadictvalue["C_CRTFCTN_APPRVL_DATE"].strftime("%m/%d/%Y"))

            # Entering Certification Expiration Date
            if datadictvalue["C_EXPRTN_DATE"] != '':
                page.locator("//a[@title='Search: Certified By']//following::input[3]").nth(0).fill(datadictvalue["C_EXPRTN_DATE"].strftime("%m/%d/%Y"))

            if datadictvalue["C_EXPDTD_RVW"] == 'YES' or 'Yes':
                page.locator("//table[@summary='Certifications']//following::input[@type='checkbox']//following::label").nth(5).click()

            if datadictvalue["C_FULL_RVW"] == 'YES' or 'Yes':
                page.locator("//table[@summary='Certifications']//following::input[@type='checkbox']//following::label").nth(6).click()

        #####Tab 4#Personnel Tab#####
        if datadictvalue["C_PRSN"] != '':
            page.get_by_role("link", name="Personnel").click()
            page.wait_for_timeout(2000)

            page.get_by_role("button", name="New").click()

            if datadictvalue["C_INTRNL"]== 'YES' or 'Yes':
                page.get_by_role("row", name="Expand Person Search: Person").locator("label").first.click()

            page.get_by_title("Search: Person").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("cell", name="**Name Name Name **Email", exact=True).get_by_label("Name").fill(datadictvalue["C_PRSN"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRSN"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

            #Person Number is defaulted based on the selected person name
            if datadictvalue["C_ROLE"] != '':
                page.get_by_title("Search: Role").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_role("cell", name="Name Name Name Description", exact=True).get_by_label("Name").fill(datadictvalue["C_ROLE"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ROLE"], exact=True).click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)

            # Entering Start & End Date
            page.locator("//a[@title='Search: Role']//following::input[1]").nth(0).fill(datadictvalue["C_P_START_DATE"].strftime("%m/%d/%Y"))
            if datadictvalue["C_END_DATE"] != '':
                page.locator("//a[@title='Search: Role']//following::input[3]").nth(0).fill(datadictvalue["C_END_DATE"].strftime("%m/%d/%Y"))
            page.wait_for_timeout(2000)

            #Email is defaulted based on the selected person.

        page.wait_for_timeout(2000)

        # Save the data
        page.get_by_role("button", name="Save", exact=True).click()

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1

        # Save the data
        page.get_by_role("button", name="Save and Close").click()

        try:
            expect(page.get_by_role("button", name="Actions")).to_be_visible()
            print("Awards Templates saved Successfully")
            datadictvalue["RowStatus"] = "Awards Templates added successfully"

        except Exception as e:
            print("Awards Templates not saved")
            datadictvalue["RowStatus"] = "Awards Templates not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, AWARD_TEMPLATES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, AWARD_TEMPLATES,
                             PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, AWARD_TEMPLATES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[0] + "_" + AWARD_TEMPLATES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[
            0] + "_" + AWARD_TEMPLATES + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))