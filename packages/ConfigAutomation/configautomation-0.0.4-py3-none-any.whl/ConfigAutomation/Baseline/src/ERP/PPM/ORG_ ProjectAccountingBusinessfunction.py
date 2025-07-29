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
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Offering").click()
    page.get_by_text("Project Financial Management", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox").fill("Configure Project Accounting Business Function")
    page.get_by_role("textbox").press("Enter")
    page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name="Configure Project Accounting Business Function", exact=True).get_by_role("link").click()
    page.wait_for_timeout(2000)
    page.locator("//a[text()='Configure Project Accounting Business Function']//following::a[1]").first.click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_label("Business Unit", exact=True).select_option("Select and Add")
        page.get_by_role("button", name="Apply and Go to Task").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("table", name='Business Units').get_by_role("cell", name=datadictvalue["C_NAME"],exact=True).click()
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)

        ##Tree name##
        page.get_by_title("Search: Tree Name").first.click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(4000)
        page.get_by_label("Hierarchy").fill(datadictvalue["C_PRJCT_TSK_OWNNG_ORGNZTN_TREE_NAME"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        page.locator("//span[text()='Hierarchy']//following::span[text()='" + datadictvalue["C_PRJCT_TSK_OWNNG_ORGNZTN_TREE_NAME"] + "'][1]").click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_title(datadictvalue["C_PRJCT_TSK_OWNNG_ORGNZTN_TREE_NAME"],exact=True).click()
        page.get_by_role("button", name="OK").click()

        ##Tree Version name##
        page.get_by_title("Search: Tree Version Name").first.click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(4000)
        page.get_by_label("Version", exact=True).fill(datadictvalue["C_PRJCT_TSK_OWNNG_ORGNZTN_TREE_VRSN_NAME"])
        page.get_by_role("button", name="Search", exact=True).click()
        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRJCT_TSK_OWNNG_ORGNZTN_TREE_VRSN_NAME"]).click()
        page.locator("//div[text()='Search and Select: Tree Version Name']//following::span[text()='"+datadictvalue["C_PRJCT_TSK_OWNNG_ORGNZTN_TREE_VRSN_NAME"]+"']").first.click()
        page.get_by_role("button", name="OK").click()

        ##Organization##
        page.get_by_title("Search: Organization").first.click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(4000)
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_PRJCT_TSK_OWNNG_ORGNZTN"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRJCT_TSK_OWNNG_ORGNZTN"]).click()
        page.get_by_role("button", name="OK").click()

        if datadictvalue["C_USE_DFFRNT_DTLS_FOR_PRJCT_EXPNDTR_ORGNZTN"] == 'Yes':
            if not page.get_by_text("Use different details for").is_checked():
                page.get_by_text("Use different details for").click()
                # Project Expenditure Organization
                page.get_by_role("cell",
                                 name="*Tree Name Search: Tree Name Autocompletes on TAB *Tree Version Name Search: Tree Version Name Autocompletes on TAB *Organization Search: Organization Autocompletes on TAB",
                                 exact=True).get_by_label("Tree Name").fill(datadictvalue["C_TREE_NAME"])
                page.get_by_role("cell",
                                 name="*Tree Name Search: Tree Name Autocompletes on TAB *Tree Version Name Search: Tree Version Name Autocompletes on TAB *Organization Search: Organization Autocompletes on TAB",
                                 exact=True).get_by_label("Tree Version Name").fill(datadictvalue["C_TREE_VRSN_NAME"])
                page.get_by_role("cell",
                                 name="*Tree Name Search: Tree Name Autocompletes on TAB *Tree Version Name Search: Tree Version Name Autocompletes on TAB *Organization Search: Organization Autocompletes on TAB",
                                 exact=True).get_by_label("Organization").fill(datadictvalue["C_ORGNZTN"])

        elif datadictvalue["C_USE_DFFRNT_DTLS_FOR_PRJCT_EXPNDTR_ORGNZTN"] == 'No':
            if page.get_by_text("Use different details for").is_checked():
                page.get_by_text("Use different details for").click()

        # Accounting Period
        if datadictvalue["C_USE_DFFRNT_ACCNTNG_AND_PRJCT_ACCNTNG_PRDS"] == 'Yes':
            if not page.get_by_text("Use different accounting and").is_checked():
                page.get_by_text("Use different accounting and").click()
                page.get_by_label("Project Accounting Calendar").select_option(datadictvalue["C_PRJCT_ACCNTNG_CLNDR"])

        elif datadictvalue["C_USE_DFFRNT_ACCNTNG_AND_PRJCT_ACCNTNG_PRDS"] == 'No':
            if page.get_by_text("Use different accounting and").is_checked():
                page.get_by_text("Use different accounting and").click()

        # Costing Currency Conversion
        page.get_by_label("Rate Type").fill(datadictvalue["C_CSTNG_CRRNCY_CNVRSN_RATE_TYPE"])
        page.get_by_label("Date Type").select_option(datadictvalue["C_CSTNG_CRRNCY_CNVRSN_DATE_TYPE"])
        page.get_by_label("Expenditure Cycle Start Day").select_option(datadictvalue["C_EXPNDTR_CYCLE_STRT_DAY"])
        page.get_by_label("Default Asset Book").select_option(datadictvalue["C_DFLT_ASST_BOOK"])

        if datadictvalue["C_ENBL_RTRMNT_PRCSSNG"] == 'Yes':
            if not page.get_by_text("Enable retirement processing").is_checked():
                page.get_by_text("Enable retirement processing").click()
        elif datadictvalue["C_ENBL_RTRMNT_PRCSSNG"] == 'No':
            if page.get_by_text("Enable retirement processing").is_checked():
                page.get_by_text("Enable retirement processing").click()

        # Advanced

        page.get_by_role("link", name="Advanced").click()
        page.wait_for_timeout(5000)
        # Transfer Price Currency Conversion
        page.get_by_label("Date Type").select_option(datadictvalue["C_DATE_TYPE"])
        page.wait_for_timeout(2000)
        page.get_by_label("Rate Type").click()
        page.get_by_label("Rate Type").select_option(datadictvalue["C_RATE_TYPE"])

        # Cross-Charge Transactions Within Legal Entity
        page.get_by_label("Processing Method Within").select_option(datadictvalue["C_PRCSSNG_MTHD_WTHN_BSNSS_UNIT"])
        page.get_by_label("Processing Method Between").select_option(datadictvalue["C_PRCSSNG_MTHD_BTWN_BSNSS_UNTS"])
        if datadictvalue["C_RCVR_BSNSS_UNIT"] != '':
            page.get_by_role("button", name="Add Row").click()
            page.get_by_label("RecvrBuId").select_option(datadictvalue["C_RCVR_BSNSS_UNIT"])
            if datadictvalue["C_PRCSS_FOR_BRRWD_AND_LENT"] == 'Yes':
                # page.get_by_role("row", name="Expand RecvrBuId").locator("label").nth(1).check()
                page.locator("// table[ @ summary = 'Cross-Charge Options'] // following::input[ @ type = 'checkbox'] // following::label").check()

        # Project Units
        page.get_by_label("Project Units").click()
        page.get_by_text("University US Project Unit").click()
        page.get_by_role("button", name="Move selected items to:").click()
        # page.pause()

        # page.get_by_role("button", name="Cancel").click()
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        try:
            expect(page.get_by_text("Search Tasks")).to_be_visible()
            # page.get_by_role("button", name="OK").click()
            print("Project Accounting BU Function Saved Successfully")
            datadictvalue["RowStatus"] = "Project Accounting BU Function added successfully"

        except Exception as e:
            print("Project Accounting BU Function not saved")
            datadictvalue["RowStatus"] = "Project Accounting BU Function are not added"

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"
        # Repeating the loop
        i = i + 1



    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_ACC_BU_FN):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_ACC_BU_FN,
                             PRCS_DIR_PATH + PPM_ORG_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_ORG_CONFIG_WRKBK, PRJ_ACC_BU_FN)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_ORG_CONFIG_WRKBK)[0] + "_" + PRJ_ACC_BU_FN)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_ORG_CONFIG_WRKBK)[
            0] + "_" + PRJ_ACC_BU_FN + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
