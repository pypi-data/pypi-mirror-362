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

    # Navigate to Derived Factors page
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Benefits Administration", exact=True).click()
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Self-Service Configuration").click()


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Self-Service Effective Date
        if datadictvalue["C_SELF_SRVC_EFFCTV_DATE_TO_USE"]!='':
            page.get_by_placeholder("m/d/yy").clear()
            page.get_by_placeholder("m/d/yy").type(datadictvalue["C_SELF_SRVC_EFFCTV_DATE_TO_USE"])

        # Display Primary Care Physician
        if datadictvalue["C_DSPLY_PRMRY_CARE_PHYSCN"]=="No":
            page.get_by_text("Display Primary Care Physician").uncheck()
        elif datadictvalue["C_DSPLY_PRMRY_CARE_PHYSCN"]=="Yes":
            page.get_by_text("Display Primary Care Physician").check()

        # Unrestricted Processing Enablement
        if datadictvalue["C_UNRSTRCTD_PRCSSNG_ENBLMNT"]=='':
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Unrestricted Processing").click()

        # Display warning to review contacts before enrollment
        if datadictvalue["C_DSPLY_WRNNG_TO_RVW_CNTCT_BFR_ENRLLMNT"]=='Yes':
            page.get_by_text("Display warning to review").check()
            page.wait_for_timeout(2000)
            page.get_by_label("Frequency in Days").clear()
            page.get_by_label("Frequency in Days").type(str(datadictvalue["C_FRQNCY_IN_DAYS"]))

        # Display future-dated contacts
        if datadictvalue["C_DSPLY_FUTUR_DTD_CNTCT"]=='No':
            page.get_by_text("Display future-dated contacts").uncheck()

        # Dependent and Beneficiary Designation
        ## Display warning to highlight benefit offering before designation
        if datadictvalue["C_DSPLY_WRNNG_TO_HGHLGHT_BNFT_OFFRNG_BFR_DSGNTN"]=='Yes':
            page.get_by_text("Display warning to highlight").check()
        elif datadictvalue["C_DSPLY_WRNNG_TO_HGHLGHT_BNFT_OFFRNG_BFR_DSGNTN"]=='No':
            page.get_by_text("Display warning to highlight").uncheck()

        ## Enforce dependent and beneficiary designation during enrollment
        if datadictvalue["C_ENFRC_DPNDNT_AND_BNFCRY_DSGNTN_DRNG_ENRLLMNT"]=='Yes':
            page.get_by_text("Enforce dependent and").check()
        elif datadictvalue["C_ENFRC_DPNDNT_AND_BNFCRY_DSGNTN_DRNG_ENRLLMNT"]=='No':
            page.get_by_text("Enforce dependent and").uncheck()

        ## Allow new contacts to be added as eligible dependents
        if datadictvalue["C_ALLOW_NEW_CNTCTS_TO_BE_ADD_AS_ELGBL_DPNDTS"]=='Yes':
            page.get_by_text("Allow new contacts to be").check()
        elif datadictvalue["C_ALLOW_NEW_CNTCTS_TO_BE_ADD_AS_ELGBL_DPNDTS"]=='No':
            page.get_by_text("Allow new contacts to be").uncheck()

        # Confirmation
        ## Display signature
        if datadictvalue["C_DSPLY_SGNTR"]=='Yes':
            page.get_by_text("Display signature").check()
        elif datadictvalue["C_DSPLY_SGNTR"]=='No':
            page.get_by_text("Display signature").uncheck()

        ## Display enrolled plans on the Confirmation and Summary page in an expanded state
        if datadictvalue["C_DSPLY_ENRLLD_PLNS_ON_THE_CNFRMTN_AND_SMMRY_PAGE_EXPAND_STT"]=='Yes':
            page.get_by_text("Display enrolled plans on the").check()
        elif datadictvalue["C_DSPLY_ENRLLD_PLNS_ON_THE_CNFRMTN_AND_SMMRY_PAGE_EXPAND_STT"]=='No':
            page.get_by_text("Display enrolled plans on the").uncheck()

        ## Display waived enrollments on the Confirmation and Summary page in a separate section
        if datadictvalue["C_DSPLY_WVD_ENRLLMNTS_ON_CNFRMTN_SMMRY_PAGE_SPRT_SCTN"]=='Yes':
            page.get_by_text("Display waived enrollments on").check()
        elif datadictvalue["C_DSPLY_WVD_ENRLLMNTS_ON_CNFRMTN_SMMRY_PAGE_SPRT_SCTN"]=='No':
            page.get_by_text("Display waived enrollments on").uncheck()

        # Enrollment Authorizations
        ## Display Authorization page in Benefits Service Center
        if datadictvalue["DSPLY_ATHRZTN_PAGE_BNFTS_SRVC_CNTR"]=='Yes':
            page.get_by_text("Display Authorization page in").check()
        elif datadictvalue["DSPLY_ATHRZTN_PAGE_BNFTS_SRVC_CNTR"]=='No':
            page.get_by_text("Display Authorization page in").uncheck()

        ## Display authorization text as of life event occurred date
        if datadictvalue["DSPLY_ATHRZTN_TEXT_LIFE_EVENT_OCCRD_DATE"]=='Yes':
            page.get_by_text("Display authorization text as").check()
        elif datadictvalue["DSPLY_ATHRZTN_TEXT_LIFE_EVENT_OCCRD_DATE"]=='No':
            page.get_by_text("Display authorization text as").uncheck()

        # Life Event
        ## Allow administrators to close life event, within enrollment flow, after making elections
        if datadictvalue["C_ALLOW_ADMN_CLOSE_LIFE_ENRLL_FLOW_AFTR_MKNG_ELCTN"]=='Yes':
            page.get_by_text("Allow administrators to close").check()
        elif datadictvalue["C_ALLOW_ADMN_CLOSE_LIFE_ENRLL_FLOW_AFTR_MKNG_ELCTN"]=='No':
            page.get_by_text("Allow administrators to close").uncheck()

        # Pending Actions
        ## Allow employees to declare that they can't provide a certificate
        if datadictvalue["C_ALLOW_EMPLYS_TO_DCLR_THAT_THEY_CANT_PRVDE_CRTFCT"] == 'Yes':
            page.get_by_text("Allow employees to declare").check()
        elif datadictvalue["C_ALLOW_EMPLYS_TO_DCLR_THAT_THEY_CANT_PRVDE_CRTFCT"] == 'No':
            page.get_by_text("Allow employees to declare").uncheck()

        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("heading", name="Self-Service Configuration")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Self Service Configuration Created Successfully")
            datadictvalue["RowStatus"] = "Self Service Configuration Created Successfully"
        except Exception as e:
            print("Unable to Create Self Service Configuration")
            datadictvalue["RowStatus"] = "Unable to Save Self Service Configuration"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, SELF_SER_CONFIG):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, SELF_SER_CONFIG,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, SELF_SER_CONFIG)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + SELF_SER_CONFIG)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + SELF_SER_CONFIG + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




