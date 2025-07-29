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
    page.get_by_role("textbox").type("Enterprise Recruiting and Candidate Experience Information")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Enterprise Recruiting and Candidate Experience Information", exact=True).click()
    page.wait_for_timeout(2000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        #Recruiting Management
        #Edit
        page.get_by_role("button", name="Edit").first.click()
        page.wait_for_timeout(2000)

        #Requisition Number Generation Method
        page.get_by_role("combobox", name="Requisition Number Generation").click()
        page.get_by_text(datadictvalue["C_RQSTN_NMBR_GNRTN_MTHD"], exact=True).click()

        #Requisition Number Starting Value
        page.get_by_label("Requisition Number Starting").click()
        page.get_by_label("Requisition Number Starting").clear()
        page.get_by_label("Requisition Number Starting").fill(str(datadictvalue["C_RQSTN_NMBR_STRTNG_VALUE"]))

        #Maximum Number of Unverified Job Applications
        page.get_by_label("Maximum Number of Unverified").click()
        page.get_by_label("Maximum Number of Unverified").clear()
        page.get_by_label("Maximum Number of Unverified").fill(str(datadictvalue["C_MXMM_NMBR_OF_UVRFD_JOB_APPLCTNS"]))

        #Checkbox
        if datadictvalue["C_ALLOW_WTHDRWN_CANDDT_TO_RPPLY"] == 'Yes':
            page.locator("tr").filter(has_text="Allow Withdrawn Candidate to").locator("label").nth(1).check()
        if datadictvalue["C_ALLOW_WTHDRWN_CANDDT_TO_RPPLY"] == 'No' or '':
            page.locator("tr").filter(has_text="Allow Withdrawn Candidate to").locator("label").nth(1).uncheck()
        if datadictvalue["C_CNTNGNT_WRKR_IS_EXTRNL_CANDDT"] == 'Yes':
            page.locator("tr").filter(has_text="Contingent Worker Is External").locator("label").nth(1).check()
        if datadictvalue["C_CNTNGNT_WRKR_IS_EXTRNL_CANDDT"] == 'No' or '':
            page.locator("tr").filter(has_text="Contingent Worker Is External").locator("label").nth(1).uncheck()
        if datadictvalue["C_PRFLL_INFRMTN_IN_CNDDT_APPLCTNS"] == 'Yes':
            page.locator("tr").filter(has_text="Prefill Legislative").locator("label").nth(1).check()
        if datadictvalue["C_PRFLL_INFRMTN_IN_CNDDT_APPLCTNS"] == 'No' or '':
            page.locator("tr").filter(has_text="Prefill Legislative").locator("label").nth(1).uncheck()
        if datadictvalue["C_PRFLL_PRSCRNNG_QUSTNS_IN_EXTRNL_CNDDT_APPLCTNS"] == 'Yes':
            page.locator("tr").filter(has_text="Prefill Prescreening").locator("label").nth(1).check()
        if datadictvalue["C_PRFLL_PRSCRNNG_QUSTNS_IN_EXTRNL_CNDDT_APPLCTNS"] == 'No' or '':
            page.locator("tr").filter(has_text="Prefill Prescreening").locator("label").nth(1).uncheck()

        page.get_by_role("button", name="Save").click()

        #Candidate Experience
        page.locator("//h2[text()='Candidate Experience']//following::img[1]").click()
        page.wait_for_timeout(2000)
        page.locator("//div[@title='Candidate Experience']//following::div[@title='Edit']").first.click()
        page.wait_for_timeout(2000)


        if datadictvalue["C_KEEP_ME_SGND_IN_FOR_EXTRNL_CNDDTS"] == 'Yes':
            page.locator("tr").filter(has_text="Keep Me Signed in for External Candidates").locator("label").nth(1).check()
        if datadictvalue["C_KEEP_ME_SGND_IN_FOR_EXTRNL_CNDDTS"] == 'No' or '':
            page.locator("tr").filter(has_text="Keep Me Signed in for External Candidates").locator("label").nth(1).uncheck()

        if datadictvalue["C_CNDDT_ATCNFRMTN"] == 'Yes':
            if not page.locator("tr").filter(has_text="Candidate Autoconfirmation").locator("label").nth(1).check():
                page.locator("tr").filter(has_text="Candidate Autoconfirmation").locator("label").nth(1).check()
        if datadictvalue["C_CNDDT_ATCNFRMTN"] == 'No' or '':
            page.locator("tr").filter(has_text="Candidate Autoconfirmation").locator("label").nth(1).uncheck()

        if datadictvalue["C_CNDDT_LAST_NAME_VRFCTN_AND_PHONE_NMBR_RQST"] == 'Yes':
            #page.get_by_role("row", name="Candidate Last Name Verification and Phone Number Request", exact=True).locator("label").nth(1).check()
            page.locator("tr").filter(has_text="Verify Last Name and Allow Phone Number Claims").locator("label").nth(1).check()
        # if datadictvalue["C_CNDDT_LAST_NAME_VRFCTN_AND_PHONE_NMBR_RQST"] == 'No':
        #     #page.get_by_role("row", name="Candidate Last Name Verification and Phone Number Request", exact=True).locator("label").nth(1).uncheck()
        #     page.get_by_role("row", name="Verify Last Name and Allow Phone Number Claims", exact=True).locator("label").nth(1).uncheck()
        if datadictvalue["C_CRR_SITE_SRCH_IN_RQSTN_DSCRPTN"] == 'Yes':
            page.locator("tr").filter(has_text="Career Site Search in Requisition Description").locator("label").nth(1).check()
        if datadictvalue["C_CRR_SITE_SRCH_IN_RQSTN_DSCRPTN"] == 'No' or '':
            page.locator("tr").filter(has_text="Career Site Search in Requisition Description").locator("label").nth(1).uncheck()

        if datadictvalue["C_AUTO_CRRCT_IN_KYWRD_SRCH"] == 'Yes':
            page.locator("tr").filter(has_text="Auto Correct in Keyword Search").locator("label").nth(1).check()
        if datadictvalue["C_AUTO_CRRCT_IN_KYWRD_SRCH"] == 'No' or '':
            page.locator("tr").filter(has_text="Auto Correct in Keyword Search").locator("label").nth(1).uncheck()

        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(2000)

        #Talent Community
        page.locator("//h2[text()='Candidate Pools']//following::img[1]").click()
        page.wait_for_timeout(2000)
        page.locator("//div[@title='Candidate Pools']//following::div[@title='Edit']").first.click()
        page.wait_for_timeout(2000)


        #Active check box
        if datadictvalue["C_ACTV"] == 'Yes':
            page.locator("tr").filter(has_text="Active").locator("label").nth(1).check()
        if datadictvalue["C_ACTV"] == 'No' or '':
            page.locator("tr").filter(has_text="Active").locator("label").nth(1).uncheck()

        #Fields displayed to external candidates when they join a talent community
        page.get_by_role("combobox", name="Fields displayed to external").click()
        page.get_by_text(datadictvalue["C_FLDS_DSPLYD_TO_EXTRNL_CNDDTS_WHEN_THEY_JOIN_A_TLNT_CMMNTY"], exact=True).click()

        #Global Talent Community Pool Visible check box
        if datadictvalue["C_GLBL_TLNT_CMMNTY_POOL_VSBL"] == 'Yes':
            page.locator("tr").filter(has_text="Global Talent Community Pool Visible").locator("label").first.check()
        if datadictvalue["C_GLBL_TLNT_CMMNTY_POOL_VSBL"] == 'No' or '':
            page.locator("tr").filter(has_text="Global Talent Community Pool Visible").locator("label").first.uncheck()

        #Send Job Alert
        page.get_by_role("combobox", name="Send Job Alert Every").click()
        page.get_by_text(str(datadictvalue["C_SEND_JOB_ALERT_EVERY"]), exact=True).click()

        #Save
        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(2000)

        #offer
        page.locator("//h2[text()='Offer']//following::img[1]").click()
        page.wait_for_timeout(2000)
        page.locator("//div[@title='Offer']//following::div[@title='Edit']").first.click()
        page.wait_for_timeout(2000)


        if datadictvalue["C_DWNLD_OFFER_LTTR_WITH_RSLVD_TKNS"] == 'Yes':
            page.locator("tr").filter(has_text="Download Offer Letter with").locator("label").nth(1).check()
        if datadictvalue["C_DWNLD_OFFER_LTTR_WITH_RSLVD_TKNS"] == 'No' or '':
            page.locator("tr").filter(has_text="Download Offer Letter with").locator("label").nth(1).uncheck()

        if datadictvalue["C_WTHDRW_CNDDTS_JOB_APPLCTNS_WHEN_THEY_MOVE_TO_HR_PHASE"] == 'Yes':
            page.locator("tr").filter(has_text="Withdraw candidates from all").locator("label").nth(1).check()
        if datadictvalue["C_WTHDRW_CNDDTS_JOB_APPLCTNS_WHEN_THEY_MOVE_TO_HR_PHASE"] == 'No' or '':
            page.locator("tr").filter(has_text="Withdraw candidates from all").locator("label").nth(1).uncheck()

        if datadictvalue["C_RMV_CNDDTS_FROM_CNDDTE_POOLS_WHEN_THEY_MOVE_TO_HR_PHASE"] == 'Yes':
            page.locator("tr").filter(has_text="Remove candidates from").locator("label").nth(1).check()
        if datadictvalue["C_RMV_CNDDTS_FROM_CNDDTE_POOLS_WHEN_THEY_MOVE_TO_HR_PHASE"] == 'No' or '':
            page.locator("tr").filter(has_text="Remove candidates from").locator("label").nth(1).uncheck()


        page.get_by_label("After Reaching the Final").click()
        page.get_by_label("After Reaching the Final").clear()
        page.get_by_label("After Reaching the Final").fill(str(datadictvalue["C_AFTER_RCHNG_THE_FINAL_SCCSSFL_STTE"]))

        page.get_by_label("After Reaching Any Final").click()
        page.get_by_label("After Reaching Any Final").clear()
        page.get_by_label("After Reaching Any Final").fill(str(datadictvalue["C_AFTER_RCHNG_ANY_FINAL_UNSCCSSFL_STTE"]))

        if datadictvalue["C_RQSTN_CLLBRTRS_ADDD_TO_OFFRS"] == 'All':
            page.get_by_label("All").check()

        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(2000)

        #Move to HR
        page.locator("//h2[text()='Move to HR']//following::img[1]").click()
        page.wait_for_timeout(2000)
        page.locator("//div[@title='Move to HR']//following::div[@title='Edit']").first.click()
        page.wait_for_timeout(2000)


        page.get_by_text(datadictvalue["C_DPLCT_CHECK_IN_MOVE_TO_HR"]).click()
        page.get_by_text(datadictvalue["C_INCLD_AS_PTNTL_DPLCTS"]).click()

        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(2000)


        #Campaigns
        page.locator("//h2[text()='Campaigns']//following::img[1]").click()
        page.wait_for_timeout(2000)
        page.locator("//div[@title='Campaigns']//following::div[@title='Edit']").first.click()
        page.wait_for_timeout(2000)

        page.get_by_label("Email Maximum Retry Count").click()
        page.get_by_label("Email Maximum Retry Count").clear()
        page.get_by_label("Email Maximum Retry Count").fill(str(datadictvalue["C_EMAIL_MXMM_RTRY_COUNT"]))

        if datadictvalue["C_DONT_SEND_EMLS_TO_CNDDTS_FLGGD_AS_DONT_HIRE"] == 'Yes':
            page.locator("tr").filter(has_text="Don't send emails to candidates flagged as don't hire").locator("label").nth(1).check()
        if datadictvalue["C_DONT_SEND_EMLS_TO_CNDDTS_FLGGD_AS_DONT_HIRE"] == 'No' or '':
            page.locator("tr").filter(has_text="Don't send emails to candidates flagged as don't hire").locator("label").nth(1).uncheck()

        if datadictvalue["C_ENBL_DO_NOT_SEND_RULE"] == 'Yes':
            page.locator("tr").filter(has_text=re.compile(r"^Enable Do Not Send Rule$")).locator("label").nth(1).check()
        if datadictvalue["C_ENBL_DO_NOT_SEND_RULE"] == 'No' or '':
            page.locator("tr").filter(has_text=re.compile(r"^Enable Do Not Send Rule$")).locator("label").nth(1).uncheck()


        page.get_by_role("combobox", name="week").click()
        page.get_by_text(datadictvalue["C_DONT_SEND_EMLS_TO_MMBRS_WHO_ALRDY_RCVD_EMLS_IN_LAST_PRD"]).click()

        if datadictvalue["C_ENB_RICH_TEXT_EDTR_IN_EMAIL_DSGNR"] == 'Yes':
            page.locator("tr").filter(has_text="Don't send emails to audience").locator("label").nth(2).check()
        if datadictvalue["C_ENB_RICH_TEXT_EDTR_IN_EMAIL_DSGNR"] == 'No' or '':
            page.locator("tr").filter(has_text="Don't send emails to audience").locator("label").nth(2).uncheck()


        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(2000)

        #Agency Hiring
        page.locator("//h2[text()='Agency Hiring']//following::img[1]").click()
        page.wait_for_timeout(2000)
        page.locator("//div[@title='Agency Hiring']//following::div[@title='Edit']").first.click()
        page.wait_for_timeout(2000)

        if datadictvalue["C_HIDE_CNDDTE_DATA"] == 'Yes':
            page.locator("tr").filter(has_text="Hide Candidate Data").locator("label").nth(1).check()
        page.wait_for_timeout(2000)
        if datadictvalue["C_HIDE_CNDDTE_DATA"] == 'No' or '':
            page.locator("tr").filter(has_text="Hide Candidate Data").locator("label").nth(1).uncheck()
        page.wait_for_timeout(2000)

        if datadictvalue["C_REC_ALLOW_INTRNL_CNDDTE_SRCH"] == 'Yes':
            page.locator("tr").filter(has_text="Allow Internal Candidate").locator("label").nth(1).check()
        if datadictvalue["C_REC_ALLOW_INTRNL_CNDDTE_SRCH"] == 'No' or '':
            page.locator("tr").filter(has_text="Allow Internal Candidate").locator("label").nth(1).uncheck()

        if datadictvalue["C_ENBL_AGENT_ACTNS"] == 'Yes':
            page.locator("tr").filter(has_text="Enable Agent Actions").locator("label").nth(1).check()
        if datadictvalue["C_ENBL_AGENT_ACTNS"] == 'No' or '':
            page.locator("tr").filter(has_text="Enable Agent Actions").locator("label").nth(1).uncheck()


        page.get_by_role("combobox", name="Agent User Category").click()
        page.get_by_text(datadictvalue["C_AGENT_USER_CTGRY"]).click()

        page.get_by_role("combobox", name="Agent Role").click()
        page.get_by_text(datadictvalue["C_AGENT_ROLE"]).click()


        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(2000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Enterprise Recruiting and")).to_be_visible()
            print("Enterprise Recruiting and Candidate Experience Information Saved Successfully")
            datadictvalue["RowStatus"] = "Added Enterprise Recruiting and Candidate Experience Information"
        except Exception as e:
            print("Unable to save Enterprise Recruiting and Candidate Experience Information")
            datadictvalue["RowStatus"] = "Unable to Add Enterprise Recruiting and Candidate Experience Information"

    OraSignOut(page, context, browser, videodir)
    return datadict

print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + Recruiting_CONFIG_WRKBK, RECRUITING_MANAGEMENT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + Recruiting_CONFIG_WRKBK, RECRUITING_MANAGEMENT,PRCS_DIR_PATH + Recruiting_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + Recruiting_CONFIG_WRKBK, RECRUITING_MANAGEMENT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", Recruiting_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", Recruiting_CONFIG_WRKBK)[0] + "_" + RECRUITING_MANAGEMENT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
