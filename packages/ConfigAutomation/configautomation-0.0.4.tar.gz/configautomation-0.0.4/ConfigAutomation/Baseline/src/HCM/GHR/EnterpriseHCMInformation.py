from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)

    page.get_by_role("textbox").fill("Manage Enterprise HCM Information")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Enterprise HCM Information").click()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Edit", exact=True).click()
    page.get_by_text("Correct",exact=True).click()
    page.wait_for_timeout(4000)

    i =0
    datadictvalue = datadict[i]
    #Enterprise Description
    if page.locator("//label[text()='Effective Start Date']//following::input[1]").is_enabled():
        page.locator("//label[text()='Effective Start Date']//following::input[1]").click()
        page.locator("//label[text()='Effective Start Date']//following::input[1]").fill("")
        page.locator("//label[text()='Effective Start Date']//following::input[1]").fill(datadictvalue["C_EFFCTV_START_DATE"])
    page.get_by_label("Name", exact=True).click()
    page.get_by_label("Name", exact=True).fill("")
    page.get_by_label("Name", exact=True).type(datadictvalue["C_ENTRPRS_NAME"])
    page.get_by_role("combobox", name="Status").click()
    page.get_by_text(datadictvalue["C_STTS"], exact=True).click()
    page.get_by_role("combobox", name="Location", exact=True).click()
    page.get_by_role("combobox", name="Location", exact=True).type(datadictvalue["C_E_LCTN"])
    page.get_by_role("option", name=datadictvalue["C_E_LCTN"]).click()
    #page.get_by_role("combobox", name="Location", exact=True).press("Enter")

    #Work Day Information
    page.get_by_label("Work Start Time").fill("")
    page.get_by_label("Work Start Time").type(str(datadictvalue["C_WORK_START_TIME"]))
    page.get_by_label("Work End Time").fill("")
    page.get_by_label("Work End Time").type(str(datadictvalue["C_WORK_END_TIME"]))
    page.get_by_label("Standard Working Hours", exact=True).click()
    page.get_by_label("Standard Working Hours", exact=True).fill("")
    page.get_by_label("Standard Working Hours", exact=True).type(str(datadictvalue["C_STNDRD_WRKNG_HOURS"]))
    page.wait_for_timeout(1000)
    page.get_by_label("Standard Working Hours Frequency").click()
    page.get_by_label("Standard Working Hours Frequency").fill("")
    page.get_by_label("Standard Working Hours Frequency").type(datadictvalue["C_STNDRD_WRKNG_HOURS_FRQNCY"])
    page.get_by_label("Standard Working Hours Frequency").press("Enter")

    #Enterprise Information
    page.get_by_label("Worker Number Generation").click()
    page.get_by_label("Worker Number Generation").fill("")
    page.get_by_label("Worker Number Generation").type(datadictvalue["C_WRKR_NMBR_GNRTN"])
    page.get_by_label("Worker Number Generation").press("Enter")
    page.get_by_label("Employment Model").click()
    page.get_by_label("Employment Model").fill("")
    page.get_by_label("Employment Model").type(datadictvalue["C_EMPLMNT_MODEL"])
    page.get_by_label("Employment Model").press("Enter")
    page.get_by_label("Allow Employment Terms").click()
    page.get_by_label("Allow Employment Terms").fill("")
    page.get_by_label("Allow Employment Terms").type(datadictvalue["C_ALLOW_EMPLYMNT_TERMS_OVRRD_AT_ASGNMNT"])
    page.get_by_label("Allow Employment Terms").press("Enter")
    page.get_by_label("People Group Flexfield").click()
    page.get_by_label("People Group Flexfield").fill("")
    page.get_by_label("People Group Flexfield").type(datadictvalue["C_PPL_GROUP_FLXFLD_STRCTR"])
    page.get_by_label("People Group Flexfield").press("Enter")
    page.get_by_label("Salary Level").click()
    page.get_by_label("Salary Level").fill("")
    page.get_by_label("Salary Level").type(datadictvalue["C_SLRY_LEVEL"])
    page.get_by_label("Salary Level").press("Enter")
    page.get_by_label("Global Person Name Language").click()
    page.get_by_label("Global Person Name Language").fill("")
    page.get_by_label("Global Person Name Language").type(datadictvalue["C_GLBL_PRSN_NAME_LNGG"])
    page.get_by_label("Global Person Name Language").press("Enter")
    page.get_by_label("Person Number Generation").click()
    page.get_by_label("Person Number Generation").fill("")
    page.get_by_label("Person Number Generation").type(datadictvalue["C_PRSN_NMBR_GNRTN_MTHD"])
    page.get_by_label("Person Number Generation").press("Enter")
    page.get_by_label("Initial Person Number").click()
    page.get_by_label("Initial Person Number").fill("")
    page.get_by_label("Initial Person Number").type(str(datadictvalue["C_INTL_PRSN_NMBR"]))
    page.get_by_label("Initial Person Number").press("Enter")
    page.get_by_label("Person Creation Duplicate").click()
    page.get_by_label("Person Creation Duplicate").fill("")
    page.get_by_label("Person Creation Duplicate").type(datadictvalue["C_PRSN_CRTN_DPLCT_CHECK"])
    page.get_by_label("Person Creation Duplicate").press("Enter")

    #Position Synchronization Configuration
    if datadictvalue["C_ENBL_PSTN_SYNCHRNZTN"] == "Yes":
        if not page.locator("//label[text()='Enable Position Synchronization']//following::label[1]").is_checked():
            page.locator("//label[text()='Enable Position Synchronization']//following::label[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_ENBL_PSTN_SYNCHRNZTN"] == "No":
        if page.locator("//label[text()='Enable Position Synchronization']//following::label[1]").is_checked():
            page.locator("//label[text()='Enable Position Synchronization']//following::label[1]").click()
            page.wait_for_timeout(1000)

    # page.get_by_role("row", name="Manager", exact=True).locator("a").click()
    page.locator("(//label[text()='Manager']//following::input[1])[1]").click()
    page.get_by_text(datadictvalue["C_MNGR"], exact=True).click()

    if datadictvalue["C_DPRTMNT"] == "Yes":
        if not page.locator("//label[text()='Department']//following::label[1]").is_checked():
            page.locator("//label[text()='Department']//following::label[1]").click()
            page.wait_for_timeout(1000)
    elif datadictvalue["C_DPRTMNT"] == "No":
        if page.locator("//label[text()='Department']//following::label[1]").is_checked():
            page.locator("//label[text()='Department']//following::label[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_JOB"] == "Yes":
        if not page.locator("(//label[text()='Job']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Job']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_JOB"] == "No":
        if page.locator("(//label[text()='Job']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Job']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_P_LCTN"] == "Yes":
        if not page.locator("(//label[text()='Location']//following::label[1])[2]").is_checked():
            page.locator("//(label[text()='Location']//following::label[1])[2]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_P_LCTN"] == "No":
        if page.locator("(//label[text()='Location']//following::label[1])[2]").is_checked():
            page.locator("(//label[text()='Location']//following::label[1])[2]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_GRADE_LDDR"] == "Yes":
        if not page.locator("(//label[text()='Grade Ladder']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Grade Ladder']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_GRADE_LDDR"] == "No":
        if page.locator("(//label[text()='Grade Ladder']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Grade Ladder']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_GRADE"] == "Yes":
        if not page.locator("(//label[text()='Grade']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Grade']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_GRADE"] == "No":
        if page.locator("(//label[text()='Grade']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Grade']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_PRBTN"] == "Yes":
        if not page.locator("(//label[text()='Probation Period']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Probation Period']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_PRBTN"] == "No":
        if page.locator("(//label[text()='Probation Period']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Probation Period']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)


    if datadictvalue["C_ALLOW_OVRDD_AT_ASGNMNT"] == "Yes":
        if not page.locator("(//label[text()='Allow Override at Assignment']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Allow Override at Assignment']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_ALLOW_OVRDD_AT_ASGNMNT"] == "No":
        if page.locator("(//label[text()='Allow Override at Assignment']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Allow Override at Assignment']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_RGLR_TEMP"] == "Yes":
        if not page.locator("(//label[text()='Regular or Temporary']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Regular or Temporary']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_RGLR_TEMP"] == "No":
        if page.locator("(//label[text()='Regular or Temporary']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Regular or Temporary']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_FULL_TIME_PART_TIME"] == "Yes":
        if not page.locator("(//label[text()='Full Time or Part Time']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Full Time or Part Time']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_FULL_TIME_PART_TIME"] == "No":
        if page.locator("(//label[text()='Full Time or Part Time']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Full Time or Part Time']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_ASSGMNT_CTGRY"] == "Yes":
        if not page.locator("(//label[text()='Assignment Category']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Assignment Category']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_ASSGMNT_CTGRY"] == "No":
        if page.locator("(//label[text()='Assignment Category']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Assignment Category']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_FTE_WRKNG_HOURS"] == "Yes":
        if not page.locator("(//label[text()='FTE and Working Hours']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='FTE and Working Hours']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_FTE_WRKNG_HOURS"] == "No":
        if page.locator("(//label[text()='FTE and Working Hours']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='FTE and Working Hours']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_START_TIME_END_TIME"] == "Yes":
        if not page.locator("(//label[text()='Start Time and End Time']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Start Time and End Time']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_START_TIME_END_TIME"] == "No":
        if page.locator("(//label[text()='Start Time and End Time']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Start Time and End Time']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_UNION_CLLCTV_AGRNMT_BRGNG_UNIT"] == "Yes":
        if not page.locator("(//label[text()='Union, Bargaining Unit and Collective Agreement']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Union, Bargaining Unit and Collective Agreement']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_UNION_CLLCTV_AGRNMT_BRGNG_UNIT"] == "No":
        if page.locator("(//label[text()='Union, Bargaining Unit and Collective Agreement']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Union, Bargaining Unit and Collective Agreement']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_SYNC_MPPD_FLXFLDS"] == "Yes":
        if not page.locator("(//label[text()='Synchronize Mapped Flexfields']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Synchronize Mapped Flexfields']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_SYNC_MPPD_FLXFLDS"] == "No":
        if page.locator("(//label[text()='Synchronize Mapped Flexfields']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Synchronize Mapped Flexfields']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)

    if datadictvalue["C_ACTN_RSN"] == "Yes":
        if not page.locator("(//label[text()='Action Reason']//following::label[1])[2]").is_checked():
            page.locator("(//label[text()='Action Reason']//following::label[1])[2]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_ACTN_RSN"] == "No":
        if page.locator("(//label[text()='Action Reason']//following::label[1])[2]").is_checked():
            page.locator("(//label[text()='Action Reason']//following::label[1])[2]").click()
            page.wait_for_timeout(1000)

    #Position Hierarchy Configuration
    if datadictvalue["C_USE_PSTN_HRCHY"] == "Yes":
        if not page.locator("(//label[text()='Use HCM Position Hierarchy']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Use HCM Position Hierarchy']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)
    if datadictvalue["C_USE_PSTN_HRCHY"] == "No":
        if page.locator("(//label[text()='Use HCM Position Hierarchy']//following::label[1])[1]").is_checked():
            page.locator("(//label[text()='Use HCM Position Hierarchy']//following::label[1])[1]").click()
            page.wait_for_timeout(1000)

    #Position Incumbent Validation
    # page.locator("tr").filter(has_text=re.compile(r"^Apply Incumbent Validation$")).get_by_role("rowgroup").locator("label").nth(1).click()
    # page.wait_for_timeout(1000)

    #Employment Configuration Options
    page.locator("(//label[text()='Guided Flows: Future-Dated Records Validation']//following::input[1])[1]").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FTR_DATED_RCRDS_VLDTN_FOR_GD_FLOWS"]).click()
    page.wait_for_timeout(1000)
    page.locator("(//label[text()='Validation For Existing Subordinates Termination']//following::input[1])[1]").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VLDTN_FOR_EXSTNG_SBRDNTS_TRMNTN"]).click()
    page.get_by_label("Employment: Approver Region Collapsed").click()
    page.get_by_label("Employment: Approver Region Collapsed").fill("")
    page.get_by_label("Employment: Approver Region Collapsed").type(datadictvalue["C_APPRVR_RGN_CLLPSD"])
    page.get_by_label("Employment: Approver Region Collapsed").press("Enter")
    page.get_by_label("Default Enterprise Seniority Date").click()
    page.get_by_label("Default Enterprise Seniority Date").fill("")
    page.get_by_label("Default Enterprise Seniority Date").type(datadictvalue["C_DFLT_ENTRPRS_SNRTY_DATE"])
    page.get_by_label("Default Enterprise Seniority Date").press("Enter")
    page.get_by_label("Recruiting Integration").click()
    page.get_by_label("Recruiting Integration").fill("")
    page.get_by_label("Recruiting Integration").type(datadictvalue["C_RCRTNG_INTGRTN"])
    page.get_by_label("Recruiting Integration").press("Enter")
    page.get_by_label("Convert pending workers").click()
    page.get_by_label("Convert Pending Workers").fill("")
    page.get_by_label("Convert Pending Workers").type(datadictvalue["C_ATMTCLLY_CNVRT_PNDNG_WRKRS"])
    page.get_by_label("Convert Pending Workers").press("Enter")

    #Position Hierarchy Configuration
    #page.locator("tr").filter(has_text=re.compile(r"^Use HCM Position Hierarchy$")).get_by_role("rowgroup").locator("label").click()
    #page.locator("tr").filter(has_text=re.compile(r"^Use Position Trees$")).get_by_role("rowgroup").locator("label").click()

    #Workforce Structures Configuration
    page.get_by_label("Position Code Generation").click()
    page.get_by_label("Position Code Generation").fill("")
    page.get_by_label("Position Code Generation").type(datadictvalue["C_PSTN_CODE_GNRTN_MTHD"])
    page.get_by_label("Position Code Generation").press("Enter")
    if datadictvalue["C_INTL_PSTN_CODE"]!="N/A":
        page.get_by_label("Initial Position Code").click()
        page.get_by_label("Initial Position Code").fill("")
        page.get_by_label("Initial Position Code").type(str(datadictvalue["C_INTL_PSTN_CODE"]))
    page.wait_for_timeout(1000)
    #get_by_role("cell", name="Position Code Generation Method Position Code Generation Method Search:").locator("a").nth(1)
    #page.get_by_role("cell", name="Position Code Generation Method Position Code Generation Method Search:").get_by_label("Guided Flows: Future-Dated")
    page.locator("(//label[text()='Position Code Generation Method']//following::input[1])[1]").clear()
    page.locator("(//label[text()='Position Code Generation Method']//following::input[1])[1]").click()
    page.locator("(//label[text()='Position Code Generation Method']//following::input[1])[1]").type(datadictvalue["C_PSTN_CODE_GNRTN_MTHD"])
    # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PSTN_CODE_GNRTN_MTHD"]).click()
    if datadictvalue["C_JOB_CODE_GNRTN_MTHD"] != "N/A":
        page.get_by_label("Job Code Generation Method").click()
        page.get_by_label("Job Code Generation Method").clear()
        page.get_by_label("Job Code Generation Method").type(datadictvalue["C_JOB_CODE_GNRTN_MTHD"])
        page.get_by_label("Job Code Generation Method").press("Enter")
    if datadictvalue["C_INTL_JOB_CODE"] != "N/A":
        page.get_by_label("Initial Job Code").click()
        page.get_by_label("Initial Job Code").clear()
        page.get_by_label("Initial Job Code").type(datadictvalue["C_INTL_JOB_CODE"])
        page.get_by_label("Initial Job Code").press("Enter")
    if datadictvalue["C_FTR_DATED_RCRDS_VLDTN"] != "N/A":
        page.locator("td").filter(has_text="Position Code Generation MethodPosition Code Generation MethodAutocompletes on").get_by_label("Guided Flows: Future-Dated").click()
        page.locator("td").filter(has_text="Position Code Generation MethodPosition Code Generation MethodAutocompletes on").get_by_label("Guided Flows: Future-Dated").clear()
        page.locator("td").filter(has_text="Position Code Generation MethodPosition Code Generation MethodAutocompletes on").get_by_label("Guided Flows: Future-Dated").type(datadictvalue["C_FTR_DATED_RCRDS_VLDTN"])
        page.locator("td").filter(has_text="Position Code Generation MethodPosition Code Generation MethodAutocompletes on").press("Enter")
    if datadictvalue["C_DFLT_LCTN_CNTRY"] != "N/A":
        page.get_by_label("Default Location Country").click()
        page.get_by_label("Default Location Country").clear()
        page.get_by_label("Default Location Country").type(datadictvalue["C_DFLT_LCTN_CNTRY"])
        page.get_by_label("Default Location Country").press("Enter")
    if datadictvalue["C_DFLT_EVLTN_SYSTM"] != "N/A":
        page.get_by_label("Default Evaluation System").click()
        page.get_by_text("Custom").click()
    if datadictvalue["C_DFLT_EFFCTV_START_DATE"] != "N/A":
        page.locator("//label[text()='Default Effective Start Date']//following::input[1]").first.click()
        page.locator("//label[text()='Default Effective Start Date']//following::input[1]").first.fill("")
        #page.get_by_placeholder("m/d/yy").nth(1).type("")

    #Workforce Structures Minimum Search Characters
    page.get_by_label("Organization").clear()
    page.get_by_label("Organization").type(str(datadictvalue["C_ORGNZTN_MNM_SRCH_CHRCTRS"]))
    page.get_by_label("Grade").nth(2).clear()
    page.get_by_label("Grade").nth(2).type(str(datadictvalue["C_GRADE_MNM_SRCH_CHRCTRS"]))
    page.get_by_role("textbox", name="Grade Ladder").clear()
    page.get_by_role("textbox", name="Grade Ladder").type(str(datadictvalue["C_GRADE_LDDR_MNM_SRCH_CHRCTRS"]))
    page.get_by_label("Grade Rate").clear()
    page.get_by_label("Grade Rate").type(str(datadictvalue["C_GRADE_RATE_MNM_SRCH_CHRCTRS"]))
    page.get_by_label("Job").nth(3).clear()
    page.get_by_label("Job").nth(3).type(str(datadictvalue["C_JOB_MNM_SRCH_CHRCTRS"]))
    page.get_by_label("Job Family").clear()
    page.get_by_label("Job Family").type(str(datadictvalue["C_JOB_FMLY_MNM_SRCH_CHRCTRS"]))
    page.get_by_label("Location").nth(3).clear()
    page.get_by_label("Location").nth(3).type(str(datadictvalue["C_LCTN_MNM_SRCH_CHRCTRS"]))
    page.locator("//label[text()='Position']//following::input[1]").first.clear()
    page.locator("//label[text()='Position']//following::input[1]").first.type(str(datadictvalue["C_PSTN_MNM_SRCH_CHRCTRS"]))

    #Transaction Console Information
    #page.locator("tr").filter(has_text=re.compile(r"^Enable Transaction Security$")).get_by_role("rowgroup").locator("label").click()
    page.get_by_role("button", name="Review").click()
    page.wait_for_timeout(20000)
    page.get_by_title("Submit").click()
    page.wait_for_timeout(10000)
    if page.get_by_role("button", name="Yes").is_visible():
        page.get_by_role("button", name="Yes").click()
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(5000)
    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Added Enterprise HCM Info Saved Successfully")
        datadictvalue["RowStatus"] = "Added Enterprise HCM Info and code"
    except Exception as e:
        print("Unable to save Enterprise HCM Info")
        datadictvalue["RowStatus"] = "Unable to Add Enterprise HCM Info and code"
    print("Row Added - ", str(i))
    datadictvalue["RowStatus"] = "Added Enterprise HCM Info Successfully"


    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, ENTERPRISE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, ENTERPRISE, PRCS_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, ENTERPRISE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_ENTSTRUCT_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_ENTSTRUCT_CONFIG_WRKBK)[0] + "_" + ENTERPRISE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
