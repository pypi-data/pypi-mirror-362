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

    #Navigation
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Navigator").click()
    page.wait_for_timeout(2000)
    page.get_by_title("My Client Groups", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Absences").click()
    page.wait_for_timeout(5000)

    #Search and Select Absence Plan
    page.get_by_placeholder("Search for tasks").click()
    page.get_by_placeholder("Search for tasks").type("Absence Plans")
    page.get_by_role("link", name="Search for tasks").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Absence Plans").click()
    page.wait_for_timeout(4000)

    #Search using Absence Plan Name
    #page.get_by_placeholder("m/d/yy").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        print(i)
        # Create Absence Plan
        page.get_by_role("button", name="Create").click()
        page.get_by_role("cell", name="Create Absence Plan *").get_by_placeholder("m/d/yy").click()
        page.get_by_role("cell", name="Create Absence Plan *").get_by_placeholder("m/d/yy").fill("")
        page.get_by_role("cell", name="Create Absence Plan *").get_by_placeholder("m/d/yy").type(datadictvalue["C_EFFCTV_DATE"])
        page.wait_for_timeout(1000)
        page.get_by_role("row", name="*Legislation", exact=True).locator("a").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTN"], exact=True).click()
        page.get_by_role("row", name="*Plan Type", exact=True).locator("a").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLAN_TYPE"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Continue").click()

        #General Attribute
        page.get_by_label("Plan", exact=True).click()
        page.get_by_label("Plan", exact=True).type(datadictvalue["C_PLAN"])
        page.get_by_label("Description").click()
        page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])
        page.get_by_role("combobox", name="Plan UOM").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLAN_UOM"])
        if datadictvalue["C_ALTNTV_SCHDL_CTGRY"] != "N/A":
            page.get_by_role("combobox", name="Alternative Schedule Category").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ALTNTV_SCHDL_CTGRY"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_LGSLTV_GRPNG_CODE"] != "N/A":
            page.get_by_role("combobox", name="Legislative Grouping Code").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTV_GRPNG_CODE"])
            page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Legislative Data Group").click()
        page.get_by_text(datadictvalue["C_LGSLTV_DTGRP"], exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Status").click()
        page.get_by_text(datadictvalue["C_STTUS"], exact=True).click()
        if datadictvalue["C_CNCRRT_ETLMNT"] !="":
            if not page.get_by_text("Enable concurrent entitlement").is_checked():
                page.get_by_text("Enable concurrent entitlement", exact=True).click()
                page.wait_for_timeout(1000)
        if datadictvalue["C_CNVRSN_FRML"] != "N/A":
            page.get_by_role("combobox", name="Conversion Formula").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CNVRSN_FRML"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_PLAN_CTGRY"] != "N/A":
            page.get_by_role("combobox", name="Plan Category").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLAN_CTGRY"])
            page.wait_for_timeout(1000)

        #Plan Term
        if datadictvalue["C_TYPE"] == "Calendar year":
            page.get_by_role("combobox", name="Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
            page.wait_for_timeout(1000)
            page.get_by_placeholder("m/d/yy").first.click()
            page.get_by_placeholder("m/d/yy").first.type(datadictvalue["C_CLNDR"])
            page.wait_for_timeout(1000)

        if datadictvalue["C_TYPE"] == "Anniversary year":
            page.get_by_role("combobox", name="Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Anniversary Event Rule").click()
            page.get_by_text(datadictvalue["C_ANVRSR_EVENT_RULE"], exact=True).click()
            page.wait_for_timeout(1000)

        #Balance Display
        page.get_by_role("combobox", name="Worker Balance Display").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WRKR_BLNC_DSPLY"])
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Manager Balance Display").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MNGR_BLNC_DSPLY"])
        page.wait_for_timeout(1000)

        #Legislative Information
        if datadictvalue["C_LGSLTV_INFRMTN_CNTXT_SGMNT"] != "N/A":
            page.get_by_role("combobox", name="Context Segment").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTV_INFRMTN_CNTXT_SGMNT"]).click()
            page.wait_for_timeout(4000)
        if datadictvalue["C_VCTN_PLAN_CRRNT_YEAR"] != "N/A":
            page.get_by_label("Vacation Plan Current Year").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VCTN_PLAN_CRRNT_YEAR"]).click()
            page.wait_for_timeout(1000)
        if datadictvalue["C_VCTN_PLAN_PRVS_YEAR"] != "N/A":
            page.get_by_label("Vacation Plan Previous Year").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VCTN_PLAN_PRVS_YEAR"]).click()
            page.wait_for_timeout(1000)
        if datadictvalue["C_ENTTLMNT_SNRTY_DAYS"] != "N/A":
            page.get_by_title("Search: Entitlement to Seniority Days").click()
            page.get_by_role("cell", name=datadictvalue["C_ENTTLMNT_SNRTY_DAYS"], exact=True).click()
            page.wait_for_timeout(1000)

        #Descriptive Information
        if datadictvalue["C_DSCRPTV_INFRMTN_CNTXT_SGMNT"] != "N/A":
            page.get_by_role("combobox", name="Context Segment").nth(1).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRPTV_INFRMTN_CNTXT_SGMNT"]).click()


        #Participation
        page.get_by_role("link", name="Participation").click()
        page.wait_for_timeout(4000)
        page.get_by_role("combobox", name="Enrollment Start Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ENRLMT_START_RULE"]).click()
        page.wait_for_timeout(1000)
        if datadictvalue["C_WTNG_PRD"] != "N/A":
            page.get_by_label("Waiting Period").first.click()
            page.get_by_label("Waiting Period").first.type(str(datadictvalue["C_WTNG_PRD"]))
            page.get_by_label("Waiting Period").first.press("Tab")
            page.wait_for_timeout(4000)
        if datadictvalue["C_WTNG_PRD_UOM"] != "N/A":
            page.get_by_label("Waiting Period").nth(1).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WTNG_PRD_UOM"]).click()
            page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Enrollment End Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ENRLMT_END_RULE"]).click()
        page.wait_for_timeout(2000)

        if page.get_by_text("Transfer positive balance").is_visible():
            if datadictvalue["C_ELGBLTY_TRNSFR_BLNCE"] != "No":
                if not page.get_by_text("Transfer positive balance").is_checked():
                    page.get_by_text("Transfer positive balance").click()
                    page.wait_for_timeout(1000)
            if datadictvalue["C_ELGBLTY_DSBRS_BLNCE"] != "No":
                if not page.get_by_text("Disburse positive balance").first.is_checked():
                    page.get_by_text("Disburse positive balance").first.click()
                    page.wait_for_timeout(1000)
            if datadictvalue["C_ELGBLTY_RCVOR_BLNCE"] != "No":
                if not page.get_by_text("Recover negative balance").first.is_checked():
                    page.get_by_text("Recover negative balance").first.click()
                    page.wait_for_timeout(1000)
            if datadictvalue["C_EMPLYN_TRMNTN_DSBRS"] != "No":
                if not page.get_by_text("Disburse positive balance").nth(1).is_checked():
                    page.get_by_text("Disburse positive balance").nth(1).click()
                    page.wait_for_timeout(1000)
            if datadictvalue["C_EMPLYN_TRMNTN_RCVOR"] != "No":
                if not page.get_by_text("Recover negative balance").nth(1).is_checked():
                    page.get_by_text("Recover negative balance").nth(1).click()
                    page.wait_for_timeout(1000)
        elif page.get_by_label("Expand On Loss of Plan").click():
            if datadictvalue["C_ELGBLTY_TRNSFR_BLNCE"] != "No":
                if not page.get_by_text("Transfer positive balance").is_checked():
                    page.get_by_text("Transfer positive balance").click()
                    page.wait_for_timeout(1000)
            if datadictvalue["C_ELGBLTY_DSBRS_BLNCE"] != "No":
                if not page.get_by_text("Disburse positive balance").first.is_checked():
                    page.get_by_text("Disburse positive balance").first.click()
                    page.wait_for_timeout(1000)
            if datadictvalue["C_ELGBLTY_RCVOR_BLNCE"] != "No":
                if not page.get_by_text("Recover negative balance").first.is_checked():
                    page.get_by_text("Recover negative balance").first.click()
                    page.wait_for_timeout(1000)
        if page.get_by_text("Disburse positive balance").nth(1).is_visible():
            if datadictvalue["C_EMPLYN_TRMNTN_DSBRS"] != "No":
                if not page.get_by_text("Disburse positive balance").nth(1).is_checked():
                    page.get_by_text("Disburse positive balance").nth(1).click()
                    page.wait_for_timeout(1000)
            if datadictvalue["C_EMPLYN_TRMNTN_RCVOR"] != "No":
                if not page.get_by_text("Recover negative balance").nth(1).is_checked():
                    page.get_by_text("Recover negative balance").nth(1).click()
                    page.wait_for_timeout(1000)
        elif page.get_by_label("Expand On Termination").click():
            if datadictvalue["C_EMPLYN_TRMNTN_DSBRS"] != "No":
                if not page.get_by_text("Disburse positive balance").nth(1).is_checked():
                    page.get_by_text("Disburse positive balance").nth(1).click()
                    page.wait_for_timeout(1000)
            if datadictvalue["C_EMPLYN_TRMNTN_RCVOR"] != "No":
                if not page.get_by_text("Recover negative balance").nth(1).is_checked():
                    page.get_by_text("Recover negative balance").nth(1).click()
                    page.wait_for_timeout(1000)

        #Transfer Rules
        # page.get_by_role("combobox", name="Limit Rule").click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TRNSFR_RULES_LMT_RULE"]).click()
        # page.get_by_label("Limit", exact=True).click()
        # page.get_by_label("Limit", exact=True).fill("")
        # page.get_by_label("Limit", exact=True).type(datadictvalue["C_TRNSFR_RULES_LIMIT"])
        # page.get_by_role("combobox", name="Limit Formula").click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TRNSFR_RULES_LIMIT_FRML"]).click()
        # page.get_by_role("combobox", name="Limit Proration Rule").click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TRNSFR_RULES_LIMIT_PRRTN_RULE"]).click()
        # page.get_by_role("combobox", name="Limit Proration Formula").click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TRNSFR_RULES_LIMIT_PRRTN_FRML"]).click()
        # page.get_by_role("combobox", name="Target Plan Formula").click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TRNSFR_RULES_TRGT_PLAN_FRML"]).click()
        # if datadictvalue["C_EMPLYN_TRMNTN_RCVOR"] != "No":
        #     if not page.get_by_text("Allow Prior Balance Reinstatement").first.is_checked():
        #         page.get_by_text("Allow Prior Balance Reinstatement").first.click()
        #         page.wait_for_timeout(2000)

        page.get_by_role("button", name="Select and Add").first.click()
        page.wait_for_timeout(2000)
        page.get_by_label("Sequence", exact=True).click()
        page.get_by_label("Sequence", exact=True).type(str(datadictvalue["C_ELGBLTY_SQNC"]))
        page.wait_for_timeout(1000)
        page.get_by_title("Search: Eligibility Profile").click()
        page.wait_for_timeout(2000)
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("button", name="Advanced").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Name").nth(1).click()
        page.get_by_label("Name").nth(1).fill("")
        page.get_by_label("Name").nth(1).type(datadictvalue["C_ELGBTY_PROFL"])
        page.wait_for_timeout(2000)
        page.get_by_label("Status Operator").click()
        page.get_by_role("listbox").get_by_text("Is not blank").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.locator("//div[text()='Search and Select: Eligibility Profile']//following::tr//following::td//following::span[text()='" + datadictvalue["C_ELGBTY_PROFL"] + "']").click()
        #page.get_by_text(datadictvalue["C_ELGBTY_PROFL"]).nth(1).click()
        #page.locator("tr").filter(has_text=re.compile(rf"^{datadictvalue['C_ELGBTY_PROFL']}")).get_by_role("cell").click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="OK").first.click()
        page.wait_for_timeout(1000)
        if datadictvalue["C_ELGBLTY_RQRD"] != "No":
            if not page.get_by_role("row", name="Required", exact=True).locator("label").nth(1).is_checked():
                page.get_by_role("row", name="Required", exact=True).locator("label").nth(1).click()
        page.wait_for_timeout(1000)
        page.get_by_title("Save and Close").click()
        page.wait_for_timeout(2000)

        #Accruals
        page.get_by_role("link", name="Accruals").click()
        page.wait_for_timeout(4000)
        if datadictvalue["C_ACCRL_DFNTN"] == "Matrix":
            page.get_by_text("Matrix", exact=True).click()
        if datadictvalue["C_ACCRL_FRML"] == "Formula":
            page.get_by_role("group").get_by_text("Formula").click()
            page.get_by_role("combobox", name="Accrual Formula").click()

        page.get_by_role("combobox", name="Partial Accrual Period Proration Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRTL_ACCRL_PRRTN_RULE"]).click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_VSTNG_RULE"] != "N/A":
            page.get_by_role("combobox", name="Vesting Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VSTNG_RULE"]).click()
            page.wait_for_timeout(2000)
        if datadictvalue["C_ACCRL_DRTN"] != "N/A":
            page.get_by_label("Duration", exact=True).click()
            page.get_by_label("Duration", exact=True).type(str(datadictvalue["C_ACCRL_DRTN"]))
            page.wait_for_timeout(1000)
        if datadictvalue["C_ACCRL_UOM"] != "N/A":
            page.get_by_role("combobox", name="UOM").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ACCRL_UOM"]).click()
            page.wait_for_timeout(1000)
        page.get_by_label("Payment Percentage", exact=True).click()
        page.get_by_label("Payment Percentage", exact=True).fill("")
        page.get_by_label("Payment Percentage", exact=True).type(str(datadictvalue["C_PYMNT_PRCNTGE"]))
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Accrual Method").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ACCRL_MTHOD"]).click()
        page.wait_for_timeout(1000)
        if datadictvalue["C_ACCRE_ON"] !="N/A":
            page.get_by_role("combobox", name="Accrue On").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ACCRE_ON"]).click()
            page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Accrual Proration Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ACCRL_PRRTN_RULE"]).click()
        page.wait_for_timeout(1000)
        if datadictvalue["C_ACCRL_PRRTN_FRMLA"] != "N/A":
            page.get_by_role("combobox", name="Accrual Proration Formula").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ACCRL_PRRTN_FRMLA"]).click()
            page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Rounding Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RNDNG_RILE"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Balance Frequency Source").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BLNCE_FRQNC_SRCE"]).click()
        page.wait_for_timeout(1000)
        if datadictvalue["C_BLNCE_FRQNC_SRCE"] == "Repeating period":
            if datadictvalue["C_RPTNG_PRD"] !="N/A":
                page.get_by_label("Repeating Period").click()
                page.get_by_label("Repeating Period").type(datadictvalue["C_RPTNG_PRD"])
                page.get_by_label("Repeating Period").press("Tab")
                page.wait_for_timeout(1000)

        #Plan Limits
        page.get_by_role("combobox", name="Ceiling Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CLNIN_RULE"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Annual Accrual Limit Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ANNUL_CCRUL_LMTRULE"]).click()
        page.wait_for_timeout(1000)
        if datadictvalue["C_ALLOW_NGTVE_BLNCE"] !="None":
            if not page.get_by_text("Allow negative balance").first.is_checked():
                page.get_by_text("Allow negative balance").first.click()
                page.wait_for_timeout(2000)

        #Year End Processing
        page.get_by_role("combobox", name="Rollover Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_YEAR_END_RLLVR_RULE"]).click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_YEAR_END_RLLVR_LIMIT"] !="N/A":
            page.get_by_label("Rollover Limit", exact=True).click()
            page.get_by_label("Rollover Limit", exact=True).fill("")
            page.get_by_label("Rollover Limit", exact=True).type(str(datadictvalue["C_YEAR_END_RLLVR_LIMIT"]))
            page.wait_for_timeout(1000)
        if datadictvalue["C_YEAR_END_LIMIT_PRRTN_RULE"] != "N/A":
            page.get_by_role("combobox", name="Limit Proration Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_YEAR_END_LIMIT_PRRTN_RULE"]).click()
            page.wait_for_timeout(1000)
        if datadictvalue["C_YEAR_END_RLLVR_TRGT_PLAN"] != "N/A":
            page.get_by_role("combobox", name="Rollover Target Plan").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_YEAR_END_RLLVR_TRGT_PLAN"]).click()
            page.wait_for_timeout(1000)
        if datadictvalue["C_YEAR_END_CNVRSN_FCTR"] != "N/A":
            page.get_by_label("Conversion Factor", exact=True).click()
            page.get_by_label("Conversion Factor", exact=True).fill("")
            page.get_by_label("Conversion Factor", exact=True).type(str(datadictvalue["C_YEAR_END_CNVRSN_FCTR"]))
            page.wait_for_timeout(1000)

        page.get_by_role("combobox", name="Carryover Limit Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_YEAR_END_CRRYVR_RULE"]).click()
        page.wait_for_timeout(4000)

        if datadictvalue["C_YEAR_END_CRRYVR_LMIT"] != "N/A":
            if page.get_by_label("Carryover Limit", exact=True).is_visible():
                page.get_by_label("Carryover Limit", exact=True).click()
                page.get_by_label("Carryover Limit", exact=True).fill("")
                page.get_by_label("Carryover Limit", exact=True).type(str(datadictvalue["C_YEAR_END_CRRYVR_LMIT"]))

        if datadictvalue["C_CRRYVR_PRRTN_RULE"] != "N/A":
            page.get_by_role("combobox", name="Carryover Proration Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CRRYVR_PRRTN_RULE"]).click()
            page.wait_for_timeout(4000)

        if datadictvalue["C_CRRYVR_PRRTN_FRML"] != "N/A":
            if page.get_by_role("combobox", name="Carryover Proration Formula").is_visible():
                page.get_by_role("combobox", name="Carryover Proration Formula").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CRRYVR_PRRTN_FRML"]).click()

        if datadictvalue["C_CRRYVRS_EXPR_SPCFC_TIME"] =="Yes":
            if not page.get_by_text("Carryovers expire after specific time").first.is_checked():
                page.get_by_text("Carryovers expire after specific time").first.click()
                page.wait_for_timeout(4000)

        if datadictvalue["C_EXPRTN_PRD"] != "N/A":
            page.get_by_label("Expiration Period Duration").first.click()
            page.get_by_label("Expiration Period Duration").first.fill("")
            page.get_by_label("Expiration Period Duration").first.type(str(datadictvalue["C_EXPRTN_PRD"]))
            page.get_by_label("Expiration Period Duration").first.press("Tab")
            page.wait_for_timeout(2000)
        if datadictvalue["C_EXPRTN_PRD_UOM"] != "N/A":
            page.get_by_label("Expiration Period UOM").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_EXPRTN_PRD_UOM"]).click()
            page.wait_for_timeout(1000)
        if datadictvalue["C_POST_RLLVR_DSBRS_BLNC"] == "Yes":
            if not page.get_by_text("Disburse remaining balance").first.is_checked():
                page.get_by_text("Disburse remaining balance").first.click()
                page.wait_for_timeout(4000)

        #Accural Matrix
        page.get_by_role("button", name="Create").first.click()
        page.wait_for_timeout(4000)
        page.get_by_label("Sequence", exact=True).click()
        page.get_by_label("Sequence", exact=True).type(str(datadictvalue["C_ACCRL_SQNC"]))
        page.wait_for_timeout(1000)
        page.get_by_role("link", name="Expression Builder").click()
        page.wait_for_timeout(3000)
        page.locator("//div[text()='Expression:']//following::textarea[1]").click()
        page.locator("//div[text()='Expression:']//following::textarea[1]").type(str(datadictvalue["C_ACCRL_EXPRSSN_BLDR"]))
        page.get_by_role("button", name="OK").first.click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_ACCRL_ACCRL_RATE"] != "N/A":
            page.get_by_label("Accrual Rate").click()
            page.get_by_label("Accrual Rate").type(datadictvalue["C_ACCRL_ACCRL_RATE"])
            page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Accrual Formula").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ACCRL_MTRIX"]).click()
        page.wait_for_timeout(1000)

        #Entries and Balances

        #Adjustments and Transfers
        page.get_by_role("link", name="Entries and Balances").click()
        page.wait_for_timeout(4000)
        if datadictvalue["C_ENBLE_TRNSF"] !="No":
            if not page.get_by_text("Enable transfers").first.is_checked():
                page.get_by_text("Enable transfers").first.click()
                page.wait_for_timeout(1000)
        if datadictvalue["C_ENBLE_DJSTMNT"] !="No":
            if not page.get_by_text("Enable adjustments").first.is_checked():
                page.get_by_text("Enable adjustments").first.click()
                page.wait_for_timeout(3000)
        if datadictvalue["C_ADJSTMNT_RSNS"] !="":
            page.get_by_role("cell", name="Adjustment Reasons", exact=True).locator("a").click()
            page.get_by_label(datadictvalue["C_ADJSTMNT_RSNS"]).click()
            page.wait_for_timeout(1000)
            page.get_by_role("cell", name="Adjustment Reasons", exact=True).locator("a").click()
            page.wait_for_timeout(1000)

        #Elective Disbursements
        if datadictvalue["C_BNFTS_INTGRTN"] != "No":
            if not page.get_by_text("Enable benefits integration").first.is_checked():
                page.get_by_text("Enable benefits integration").first.click()
                page.wait_for_timeout(1000)
        if datadictvalue["C_MARK_PNDNG"] != "N/A":
            if not page.get_by_text("Mark as pending").first.is_checked():
                page.get_by_text("Mark as pending").first.click()
                page.wait_for_timeout(3000)
        if datadictvalue["C_ELCTN_DATE_RULE"] != "N/A":
            page.get_by_role("combobox", name="Election Date Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ELCTN_DATE_RULE"]).click()
            page.wait_for_timeout(1000)
        if datadictvalue["C_ELCTV_PYMNT_PRCNTG"] != "N/A":
            page.get_by_label("Default Payment Percentage").first.click()
            page.get_by_label("Default Payment Percentage").first.type()
            page.wait_for_timeout(1000)
        if datadictvalue["C_EVLTN_FRML"] != "N/A":
            page.get_by_role("combobox", name="Evaluation Formula").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_EVLTN_FRML"]).click()
            page.wait_for_timeout(1000)

        #Year End Disbursements
        if datadictvalue["C_PYMNT_PRCNTG"] != "N/A":
            page.get_by_label("Default Payment Percentage").nth(1).click()
            page.get_by_label("Default Payment Percentage").first.type(str(datadictvalue["C_PYMNT_PRCNTG"]))
            page.wait_for_timeout(1000)

        #Discretionary Disbursements
        if datadictvalue["C_DSCRTNRY_ENBL_ADMNSTRTR"] == "Yes":
            if not page.get_by_text("Enable for administrator").first.is_checked():
                page.get_by_text("Enable for administrator").first.check()
                page.wait_for_timeout(1000)
        if datadictvalue["C_DSCRTNRY_ENBL_MNGR"] == "Yes":
            if not page.get_by_text("Enable for manager").first.is_checked():
                page.get_by_text("Enable for manager").first.click()
                page.wait_for_timeout(1000)
        if datadictvalue["C_DSCRTNRY_ENBL_WRKR"] == "Yes":
            if not page.get_by_text("Enable for worker").first.is_checked():
                page.get_by_text("Enable for worker").first.click()
                page.wait_for_timeout(1000)

        if datadictvalue["C_DSCRTNRY_RULE"] == "Flat amount":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Disbursement Rule").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_RULE"]).click()
            page.wait_for_timeout(3000)
            page.get_by_label("Minimum", exact=True).first.click()
            page.get_by_label("Minimum", exact=True).first.type(str(datadictvalue["C_DSCRTNRY_MNMM"]))
            page.wait_for_timeout(1000)
            page.get_by_label("Maximum", exact=True).first.click()
            page.get_by_label("Maximum", exact=True).first.type(str(datadictvalue["C_DSCRTNRY_MXMM"]))
            page.wait_for_timeout(1000)
            page.get_by_role("row", name="Increment Hours", exact=True).get_by_label("Increment").first.click()
            page.wait_for_timeout(1000)
            page.get_by_role("row", name="Increment Hours", exact=True).get_by_label("Increment").first.fill("")
            page.get_by_role("row", name="Increment Hours", exact=True).get_by_label("Increment").first.type(str(datadictvalue["C_DSCRTNRY_INCRMNT"]))
            page.wait_for_timeout(1000)

        elif datadictvalue["C_DSCRTNRY_RULE"] == "Formula":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Disbursement Rule").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_RULE"]).click()
            page.wait_for_timeout(3000)
            if datadictvalue["C_DSCRTNRY_FRML"] != "N/A":
                page.get_by_role("combobox", name="Formula").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_FRML"]).click()
                page.wait_for_timeout(1000)
        page.keyboard.press("Space")

        #Donation
        if datadictvalue["C_ENBL_ADMNSTRTR"] == "Yes":
            if not page.get_by_text("Enable for administrator").nth(1).is_checked():
                page.get_by_text("Enable for administrator").nth(1).check()
                page.wait_for_timeout(1000)
                #page.locator("//label[text()='Enable for administrator']//preceding::input[@type='checkbox'][1]").first.click()
                #page.get_by_label("Enable for administrator").first.check()
        if datadictvalue["C_ENBL_MNGR"] == "Yes":
            if not page.get_by_text("Enable for manager").nth(1).is_checked():
                page.get_by_text("Enable for manager").nth(1).click()
                page.wait_for_timeout(1000)
        if datadictvalue["C_ENBL_WRKR"] == "Yes":
            if not page.get_by_text("Enable for worker").nth(1).is_checked():
                page.get_by_text("Enable for worker").nth(1).click()
                page.wait_for_timeout(1000)

        if datadictvalue["C_DNTN_RULE"] == "Flat amount":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Donation Rule").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DNTN_RULE"]).click()
            page.wait_for_timeout(3000)
            page.get_by_label("Minimum", exact=True).nth(1).click()
            page.get_by_label("Minimum", exact=True).nth(1).type(str(datadictvalue["C_DNTN_MNMM"]))
            page.wait_for_timeout(1000)
            page.get_by_label("Maximum", exact=True).nth(1).click()
            page.get_by_label("Maximum", exact=True).nth(1).type(str(datadictvalue["C_DNTN_MXMM"]))
            page.wait_for_timeout(1000)
            page.get_by_role("cell", name="Increment Increment", exact=True).get_by_label("Increment").click()
            page.wait_for_timeout(1000)
            page.get_by_role("cell", name="Increment Increment", exact=True).get_by_label("Increment").fill("")
            page.get_by_role("cell", name="Increment Increment", exact=True).get_by_label("Increment").type(str(datadictvalue["C_DNTN_INCRMNT"]))
            page.wait_for_timeout(1000)

        elif datadictvalue["C_DNTN_RULE"] == "Formula":
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Donation Rule").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DNTN_RULE"]).click()
            page.wait_for_timeout(3000)
            if datadictvalue["C_DNTN_FRML"] != "N/A":
                page.get_by_role("combobox", name="Formula").nth(1).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DNTN_FRML"]).click()
                page.wait_for_timeout(1000)

        #Rates
        if datadictvalue["C_ABSNC_PYMNT_RULE"] != "":
            page.get_by_role("combobox", name="Absence Payment Rate Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_PYMNT_RULE"]).click()
            page.wait_for_timeout(3000)
            if datadictvalue["C_ABSNC_PYMNT_RULE"] != "Formula" or "Unpaid":
                if datadictvalue["C_ABSNC_PYMNT_RATE_NAME"] !="N/A":
                    page.locator("//label[text()='Absence Payment Rate Rule']//following::label[text()='Rate Name']//following::input[1]").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_PYMNT_RATE_NAME"]).click()
                    page.wait_for_timeout(2000)
            if datadictvalue["C_ABSNC_PYMNT_RULE"] == "Formula":
                if datadictvalue["C_ABSNC_PYMNT_FRML"] != "N/A":
                    page.locator("//label[text()='Absence Payment Rate Rule']//following::label[text()='Formula']//following::input[1]").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_PYMNT_FRML"]).click()
                    page.wait_for_timeout(2000)

        if datadictvalue["C_FINAL_DSBRSMNT_RATE_RULE"] == "Rate definition" or "Unpaid":
            page.get_by_role("combobox", name="Final Disbursement Rate Rule	").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FINAL_DSBRSMNT_RATE_RULE"]).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_FINAL_DSBRSMNT_RATE_RULE"] != "Formula" or "Unpaid":
                if datadictvalue["C_FINAL_DSBRSMNT_DFND_RATE"] != "N/A":
                    page.locator("//label[text()='Final Disbursement Rate Rule']//following::label[text()='Defined Rate']//following::input[1]").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FINAL_DSBRSMNT_DFND_RATE"]).click()
                    page.wait_for_timeout(2000)
            if datadictvalue["C_FINAL_DSBRSMNT_FRML"] == "Formula":
                if datadictvalue["C_FINAL_DSBRSMNT_FRML"] != "N/A":
                    page.locator("//label[text()='Final Disbursement Rate Rule']//following::label[text()='Formula']//following::input[1]").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FINAL_DSBRSMNT_FRML"]).click()
                    page.wait_for_timeout(2000)

        if datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE_RULE"] == "Rate definition" or "Unpaid":
            page.get_by_role("combobox", name="Discretionary Disbursement Rate Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE_RULE"]).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE_RULE"] != "Formula" or "Unpaid":
                if datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE_NAME"] != "N/A":
                    page.locator("//label[text()='Discretionary Disbursement Rate Rule']//following::label[text()='Rate Name']//following::input[1]").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE_NAME"]).click()
                    page.wait_for_timeout(2000)
            if datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE_RULE"] == "Formula":
                if datadictvalue["C_DSCRTNRY_DSBRSMNT_FRML"] != "N/A":
                    page.locator("//label[text()='Discretionary Disbursement Rate Rule']//following::label[text()='Formula']//following::input[1]").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_DSBRSMNT_FRML"]).click()
                    page.wait_for_timeout(2000)

        if datadictvalue["C_LBLTY_RATE_RULE"] == "Rate definition" or "Unpaid":
            page.get_by_role("combobox", name="Liability Rate Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LBLTY_RATE_RULE"]).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_LBLTY_RATE_RULE"] != "Formula" or "Unpaid":
                if datadictvalue["C_LBLTY_RATE_NAME"] != "N/A":
                    page.locator("//label[text()='Liability Rate Rule']//following::label[text()='Rate Name']//following::input[1]").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LBLTY_RATE_NAME"]).click()
                    page.wait_for_timeout(2000)
            if datadictvalue["C_LBLTY_RATE_RULE"] == "Formula":
                if datadictvalue["C_LBLTY_FRML"] != "N/A":
                    page.locator("//label[text()='Liability Rate Rule']//following::label[text()='Formula']//following::input[1]").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LBLTY_FRML"]).click()
                    page.wait_for_timeout(2000)

        #Payroll Integration
        if datadictvalue["C_PYRLL_INTGRTN"] == "Yes":
            if not page.get_by_text("Transfer absence payment information for payroll processing").first.is_checked():
                page.get_by_text("Transfer absence payment information for payroll processing").first.click()
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Element").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYRLL_ELMNT"]).click()
                page.wait_for_timeout(1000)

        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(10000)

        try:
            expect(page.get_by_role("heading", name="Absence Plans")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Absence Plans - Accrual Configured Successfully"+ datadictvalue["C_PLAN"])
            datadictvalue["RowStatus"] = "Created Absence Plans - Accrual Successfully" + datadictvalue["C_PLAN"]
        except Exception as e:
            print("Unable to Save Absence Plans - Accrual Configuration" + datadictvalue["C_PLAN"])
            datadictvalue["RowStatus"] = "Unable to Save Absence Plans - Accrual Configuration" + datadictvalue["C_PLAN"]

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_PLANS_ACCRUAL):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_PLANS_ACCRUAL,PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_PLANS_ACCRUAL)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




