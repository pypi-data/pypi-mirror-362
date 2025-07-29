from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("My Client Groups", exact=True).click()
    page.get_by_role("link", name="Performance").click()
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Performance Template Sections").click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(4000)

        # Click on Create Button
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)

    # Section Details
        # Name
        page.get_by_label("Name", exact=True).click()
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(3000)

        # Description
        if datadictvalue["C_DSCRPTN"] != "":
            page.get_by_label("Description", exact=True).click()
            page.get_by_label("Description", exact=True).type(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(3000)

        # Comments
        if datadictvalue["C_CMMNTS"] != "":
            page.get_by_label("Comments", exact=True).click()
            page.get_by_label("Comments", exact=True).type(datadictvalue["C_CMMNTS"])
            page.wait_for_timeout(3000)

        # From Date
        page.locator("//label[text()='From Date']//following::input[1]").click()
        page.locator("//label[text()='From Date']//following::input[1]").fill(str(datadictvalue["C_FROM_DATE"]))
        page.wait_for_timeout(3000)

        # To Date
        page.locator("//label[text()='To Date']//following::input[1]").click()
        page.locator("//label[text()='To Date']//following::input[1]").fill(str(datadictvalue["C_TO_DATE"]))
        page.wait_for_timeout(3000)

        # Status
        page.get_by_role("combobox", name="Status").click()
        page.wait_for_timeout(2000)
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()
        page.wait_for_timeout(3000)

    # Section Processing
        # Section Type
        if datadictvalue["C_SCTN_TYPE"] != "":
            page.get_by_role("combobox", name="Section Type").click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_SCTN_TYPE"], exact=True).click()
            page.wait_for_timeout(7000)

        # Competencies Section Name
        if datadictvalue["C_CMPTNCS_SCTN_NAME"] != "":
            page.get_by_role("combobox", name="Competencies Section Name").click()
            page.get_by_text(datadictvalue["C_CMPTNCS_SCTN_NAME"], exact=True).click()
            page.wait_for_timeout(2000)

        # Evaluation Type
        if datadictvalue["C_PTS_EV_TY"] != "":
            page.get_by_role("combobox", name="Evaluation Type").click()
            page.get_by_text(datadictvalue["C_PTS_EV_TY"]).click()
            page.wait_for_timeout(2000)

    # Ratings
        # Section Rating Model
        if datadictvalue["C_SCTN_RTNG_MODEL"] != "":
            page.get_by_role("combobox", name="Section Rating Model").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SCTN_RTNG_MODEL"], exact=True).click()
            page.wait_for_timeout(2000)

        # Calculation Rule for Section
        if datadictvalue["C_CLCLTN_RULE_FOR_SCTN"] != "":
            page.get_by_role("combobox", name="Calculation Rule for Section").click()
            page.get_by_text(datadictvalue["C_CLCLTN_RULE_FOR_SCTN"]).click()
            page.wait_for_timeout(2000)

        # Decimal Places
        if datadictvalue["C_DCML_PLCS"] != "":
            page.get_by_role("combobox", name="Decimal Places").click()
            page.get_by_text(datadictvalue["C_DCML_PLCS"]).click()
            page.wait_for_timeout(2000)

        # Mapping Metric
        if datadictvalue["C_MPPNG_MTRC"] != "":
            page.pause()
            page.get_by_role("combobox", name="Mapping Metric").click()
            page.get_by_text(datadictvalue["C_MPPNG_MTRC"]).click()
            page.wait_for_timeout(2000)

        # Fast Formula Rule
        if datadictvalue["C_FAST_FRML_RULE"] != "":
            page.get_by_role("combobox", name="Fast Formula Rule").click()
            page.get_by_text(datadictvalue["C_FAST_FRML_RULE"]).click()
            page.wait_for_timeout(2000)

        # Decimal Rounding Rule
        if datadictvalue["C_DCML_RNDNG_RULE"] != "":
            page.get_by_role("combobox", name="Decimal Rounding Rule").click()
            page.get_by_text(datadictvalue["C_DCML_RNDNG_RULE"]).click()
            page.wait_for_timeout(2000)

        # Mapping Method
        if datadictvalue["C_MPPNG_MTHD"] != "":
            page.get_by_role("combobox", name="Mapping Method").click()
            page.get_by_text(datadictvalue["C_MPPNG_MTHD"]).click()
            page.wait_for_timeout(2000)

        # Use section weights in calculation
        if datadictvalue["C_USE_SCTN_WGHTS_IN_CLCLTN"] != "":
            if datadictvalue["C_USE_SCTN_WGHTS_IN_CLCLTN"] == 'Yes':
                page.get_by_text("Use section weights in calculation").check()
            if datadictvalue["C_USE_SCTN_WGHTS_IN_CLCLTN"] == 'No':
                page.get_by_text("Use section weights in calculation").uncheck()
            page.wait_for_timeout(2000)

        # Enable Manual Section Rating
        if datadictvalue["C_ENBL_MNL_SCTN_RTNG"] != "":
            if datadictvalue["C_ENBL_MNL_SCTN_RTNG"] == 'Yes':
                page.get_by_text("Enable manual section rating").check()

            if datadictvalue["C_ENBL_MNL_SCTN_RTNG"] == 'No':
                page.get_by_text("Enable manual section rating").uncheck()
            page.wait_for_timeout(2000)

        # Require Manager Justification if Manual and Calculated Ratings Are Different
        if datadictvalue["C_RQR_MNGR_JSTFCTN_IF_MNL_AND_CLCLTD_RTNGS_ARE_DFFRNT"] != "No":
            if not page.get_by_text("Require Manager Justification if Manual and Calculated Ratings Are Different").is_checked():
                page.get_by_text("Require Manager Justification if Manual and Calculated Ratings Are Different", exact=True).click()
                page.wait_for_timeout(2000)

    # Section Processing - Comments
        # Enable Section Comments
        if datadictvalue["C_ENBL_SCTN_CMMNTS"] != "":
            if datadictvalue["C_ENBL_SCTN_CMMNTS"] == 'Yes':
                page.get_by_text("Enable Section Comments").check()
            if datadictvalue["C_ENBL_SCTN_CMMNTS"] == 'No':
                page.get_by_text("Enable Section Comments").uncheck()
            page.wait_for_timeout(3000)

    # Weighting
        # Weight Section
        if datadictvalue["C_WGHT_SCTN"] != "":
            if datadictvalue["C_WGHT_SCTN"] == 'Yes':
                page.get_by_text("Weight Section").check()
                page.wait_for_timeout(2000)
            if datadictvalue["C_WGHT_SCTN"] == 'No':
                page.get_by_text("Weight Section").uncheck()
                page.wait_for_timeout(2000)

        # Section Weight
        if datadictvalue["C_SCTN_WGHT"] != "":
            if datadictvalue["C_SCTN_WGHT"] != "No":
                page.get_by_role("cell", name="Section Weight", exact=True).locator("label").click()
                page.get_by_label("Section Weight", exact=True).fill(str(datadictvalue["C_SCTN_WGHT"]))
                page.wait_for_timeout(2000)

        # Section Minimum Weight
        if datadictvalue["C_SCTN_MNMM_WGHT"] != "":
            if datadictvalue["C_SCTN_MNMM_WGHT"] != "No":
                page.get_by_role("cell", name="Section Minimum Weight", exact=True).locator("label").click()
                page.get_by_label("Section Minimum Weight", exact=True).fill(str(datadictvalue["C_SCTN_MNMM_WGHT"]))
                page.wait_for_timeout(2000)

    # Item Processing
        # Enable Items
        if datadictvalue["C_ENBL_ITEMS"] != "":
            if datadictvalue["C_ENBL_ITEMS"] == 'Yes':
                page.get_by_text("Enable Items").check()
            if datadictvalue["C_ENBL_ITEMS"] == 'No':
                page.get_by_text("Enable Items").uncheck()
            page.wait_for_timeout(2000)

    # Ratings and Calculations
        # Rate Items
        if datadictvalue["C_RATE_ITEMS"] != "":
            if datadictvalue["C_RATE_ITEMS"] == 'Yes':
                page.get_by_text("Rate Items").check()
            if datadictvalue["C_RATE_ITEMS"] == 'No':
                page.get_by_text("Rate Items").uncheck()
            page.wait_for_timeout(2000)

        # Rating Type
            if datadictvalue["C_RTNG_TYPE"] != "":
                page.get_by_role("combobox", name="Rating Type").click()
                page.wait_for_timeout(4000)
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RTNG_TYPE"], exact=True).click()
                page.wait_for_timeout(4000)

        # Use Section Rating model for Performance Rating
        if datadictvalue["C_USE_SCTN_RTNG_MODEL_FOR_PRFMNC_RTNG"] != "":
            if datadictvalue["C_USE_SCTN_RTNG_MODEL_FOR_PRFMNC_RTNG"] == 'Yes':
                page.get_by_text("Use Section Rating model for Performance Rating").check()
        if datadictvalue["C_USE_SCTN_RTNG_MODEL_FOR_PRFMNC_RTNG"] == 'No':
            page.get_by_text("Use Section Rating model for Performance Rating").uncheck()
            # # Performance Rating Model
            # if datadictvalue["C_PRFRMNC_RTNG_MODEL"] != "":
            #     page.get_by_role("combobox", name="Performance Rating Model").click()
            #     page.wait_for_timeout(4000)
            #     page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRFRMNC_RTNG_MODEL"],exact=True).click()
            #     page.wait_for_timeout(2000)
            # Performance Rating Model
            if datadictvalue["C_PRFRMNC_RTNG_MODEL"] != "":
                page.get_by_role("combobox", name="Performance Rating Model").click()
                page.wait_for_timeout(4000)
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRFRMNC_RTNG_MODEL"], exact=True).click()
                page.wait_for_timeout(2000)
            # Item Calculation
        if datadictvalue["C_ITEM_CLCLTN"] != "":
            page.get_by_role("combobox", name="Item Calculation").click()
            page.get_by_text(datadictvalue["C_ITEM_CLCLTN"]).click()
            page.wait_for_timeout(2000)


    # Item Processing - Comments
        # Enable Item Comments
        if datadictvalue["C_ENBL_ITEM_CMMNTS"] != "":
            if datadictvalue["C_ENBL_ITEM_CMMNTS"] == 'Yes':
                page.get_by_text("Enable Item Comments").check()
            if datadictvalue["C_ENBL_ITEM_CMMNTS"] == 'No':
                page.get_by_text("Enable Item Comments").uncheck()
            page.wait_for_timeout(2000)

    # Properties
        # Minimum Weight
        if datadictvalue["C_SCTN_MNMM_WGHT"] != "":
            if datadictvalue["C_SCTN_MNMM_WGHT"] == 'Yes':
                page.get_by_text("Minimum Weight", exact=True).check()
            if datadictvalue["C_SCTN_MNMM_WGHT"] == 'No':
                page.get_by_text("Minimum Weight", exact=True).uncheck()
            page.wait_for_timeout(2000)

        # Weight
        if datadictvalue["C_WGHT"] != "":
            if datadictvalue["C_WGHT"] == 'Yes':
                page.get_by_text("Weight", exact=True).check()
            if datadictvalue["C_WGHT"] == 'No':
                page.get_by_text("Weight", exact=True).uncheck()
            page.wait_for_timeout(2000)

        # Required
        if datadictvalue["C_RQRD"] != "":
            if datadictvalue["C_RQRD"] == 'Yes':
                page.get_by_text("Required").check()
            page.wait_for_timeout(2000)

    # Content
        # Populate with competencies using profile
        if datadictvalue["C_PPLT_WITH_CMPTNCS_USING_PRFL"] != "":
            if datadictvalue["C_PPLT_WITH_CMPTNCS_USING_PRFL"] == 'Yes':
                page.get_by_text("Required").check()
            page.wait_for_timeout(2000)

        # Profile Type
        if datadictvalue["C_PRFL_TYPE"] != "":
            page.get_by_role("combobox", name="Profile Type").click()
            page.get_by_text(datadictvalue["C_PRFL_TYPE"]).click()
            page.wait_for_timeout(2000)

        # Populate with Worker Performance Goals
        if datadictvalue["C_PPLT_WITH_WRKR_PRFRMNC_GOALS"] != "":
            if datadictvalue["C_PPLT_WITH_WRKR_PRFRMNC_GOALS"] == 'Yes':
                page.get_by_text("Populate with Worker Performance Goals").check()
            if datadictvalue["C_PPLT_WITH_WRKR_PRFRMNC_GOALS"] == 'No':
                page.get_by_text("Populate with Worker Performance Goals").uncheck()
            page.wait_for_timeout(2000)

        # Use specific content items
        if datadictvalue["C_USE_SPCFC_CNTNT_ITEMS"] != "":
            if datadictvalue["C_USE_SPCFC_CNTNT_ITEMS"] == 'Yes':
                page.get_by_text("Use specific content items").check()
            page.wait_for_timeout(2000)
        page.pause()
        # Save and Close the Record (Save and Close)
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Performance Template Sections")).to_be_visible()
            print("Performance Template Sections Saved Successfully")
            datadictvalue["RowStatus"] = "Performance Template Sections Submitted Successfully"
        except Exception as e:
            print("Performance Template Sections not saved")
            datadictvalue["RowStatus"] = "Performance Template Sections not submitted"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, PERFORMANCE_TEMPLATE_SECTION):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, PERFORMANCE_TEMPLATE_SECTION, PRCS_DIR_PATH + PERF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PERF_CONFIG_WRKBK, PERFORMANCE_TEMPLATE_SECTION)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0] + "_" + PERFORMANCE_TEMPLATE_SECTION)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0] + "_" + PERFORMANCE_TEMPLATE_SECTION + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
