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
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Manage Project Types")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Project Types", exact=True).click()

    #Create Planning and Billing Resource Breakdown Structures
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Name").click()
        page.get_by_role("textbox", name="Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(1000)

        # Entering Set
        if datadictvalue["C_SET"] != '':
            page.get_by_title("Search: Set").click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//div[text()='Search and Select: Set']//following::label[text()='Name']//following::input[1]").click()
            page.locator("//div[text()='Search and Select: Set']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_SET"])
            # page.get_by_role("cell", name="Name Name Name Code Code Code").get_by_label("Name").click()
            # page.get_by_role("cell", name="Name Name Name Code Code Code").get_by_label("Name").fill(datadictvalue["C_SET"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SET"]).click()
            page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(1000)

        # Entering From & To Date
        # page.get_by_role("row", name="*From Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"])
        page.locator("//label[text()='From Date']//following::input[1]").nth(0).fill(datadictvalue["C_FROM_DATE"])
        if datadictvalue["C_TO_DATE"] != '':
           # page.get_by_role("row", name="To Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"])
           page.locator("//label[text()='To Date']//following::input[1]").nth(0).fill(datadictvalue["C_TO_DATE"].strftime('%m/%d/%y'))
        page.wait_for_timeout(2000)

        # Enter Work type
        if datadictvalue["C_WORK_TYPE"] !='':
            page.get_by_label("Work Type").select_option(datadictvalue["C_WORK_TYPE"])
        page.wait_for_timeout(2000)

        #Enable & Disable project options

        if datadictvalue["C_ENBL_BRDNNG"] == 'Yes':
            page.get_by_text("Enable burdening").check()
        if datadictvalue["C_ENBL_BRDNNG"] == 'No' or '':
            page.get_by_text("Enable burdening").uncheck()
        page.wait_for_timeout(1000)
        if datadictvalue["C_ENBL_BLLNG"] == 'Yes':
            page.get_by_text("Enable billing").check()
        if datadictvalue["C_ENBL_BLLNG"] == 'No' or '':
            page.get_by_text("Enable billing").uncheck()
        page.wait_for_timeout(1000)
        if datadictvalue["C_ENBL_CPTLZTN"] == 'Yes':
            page.get_by_text("Enable capitalization").check()
        if datadictvalue["C_ENBL_CPTLZTN"] == 'No' or '':
            page.get_by_text("Enable capitalization").uncheck()
        page.wait_for_timeout(1000)
        if datadictvalue["C_ENBL_SPNSRD_PRJCTS"] == 'Yes':
            page.get_by_text("Enable sponsored projects").check()
        if datadictvalue["C_ENBL_SPNSRD_PRJCTS"] == 'No' or '':
            page.get_by_text("Enable sponsored projects").uncheck()
        page.wait_for_timeout(2000)

        #Burdening Options

        if datadictvalue["C_ENBL_BRDNNG"] == 'Yes':
            page.get_by_role("link", name="Burdening Options").click()
            page.get_by_label("Default Cost Burden Schedule").select_option(datadictvalue["C_DFLT_COST_BRDN_SCHDL"])
            page.wait_for_timeout(2000)

            if datadictvalue["C_ALLOW_COST_BRDN_SCHDL_CHNG_FOR_PRJCTS_AND_TASKS"] == 'Yes':
                page.get_by_text("Allow cost burden schedule").check()
            if datadictvalue["C_ALLOW_COST_BRDN_SCHDL_CHNG_FOR_PRJCTS_AND_TASKS"] == 'No' or '':
                page.get_by_text("Allow cost burden schedule").uncheck()
            page.wait_for_timeout(1000)

            if datadictvalue["C_INCLD_BRDN_COST_ON_SAME_EXPNDTR_ITEM"] == 'Yes':
                page.get_by_text("Include burden cost on same").check()
            if datadictvalue["C_INCLD_BRDN_COST_ON_SAME_EXPNDTR_ITEM"] == 'No' or '':
                page.get_by_text("Include burden cost on same").uncheck()
            page.wait_for_timeout(1000)

            if datadictvalue["C_CRT_EXPNDTR_ITEMS_FOR_BRDN_COST_CMPNNTS"] == 'Yes':
                page.get_by_text("Create expenditure items for").check()
            if datadictvalue["C_CRT_EXPNDTR_ITEMS_FOR_BRDN_COST_CMPNNTS"] == 'No' or '':
                page.get_by_text("Create expenditure items for").uncheck()
            page.wait_for_timeout(1000)

        #Entering Project Name & Task Name

        if datadictvalue["C_CRT_EXPNDTR_ITEMS_FOR_BRDN_COST_CMPNNTS"] == 'Yes':
            page.get_by_title("Search: Project Name").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("cell", name="**Name Name Name **Number").get_by_label("Name").click()
            page.get_by_role("cell", name="**Name Name Name **Number").get_by_label("Name").fill(datadictvalue["C_PRJCT_NAME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_text(datadictvalue["C_PRJCT_NAME"]).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)
            #Task Name
            page.get_by_title("Search: Task Name").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Task Name").click()
            page.get_by_role("textbox", name="Task Name").fill(datadictvalue["C_TASK_NAME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TASK_NAME"]).click()
            page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        #ENable & Disable fields
        if datadictvalue["C_CRT_SPRT_EXPNDTR_ITEM_FOR_BRDN_COST"] == 'Yes':
            page.get_by_text("Create separate expenditure").check()
        if datadictvalue["C_CRT_SPRT_EXPNDTR_ITEM_FOR_BRDN_COST"] == 'No' or '':
            page.get_by_text("Create separate expenditure").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_CRT_BRDN_COST_ACCNTNG_JRNL_ENTRS"] == 'Yes':
            page.get_by_text("Create burden cost accounting").check()
        if datadictvalue["C_CRT_BRDN_COST_ACCNTNG_JRNL_ENTRS"] == 'No' or '':
            page.get_by_text("Create burden cost accounting").uncheck()
        page.wait_for_timeout(2000)
        if datadictvalue["C_CRT_BRDND_COST_ACCNTNG_JRNL_ENTRS"] == 'Yes':
            page.get_by_text("Create burdened cost").check()
        if datadictvalue["C_CRT_BRDND_COST_ACCNTNG_JRNL_ENTRS"] == 'No' or '':
            page.get_by_text("Create burdened cost").uncheck()
        page.wait_for_timeout(2000)

        #Next Tab
        if datadictvalue["C_ENBL_CPTLZTN"] == 'Yes':
            page.get_by_role("link", name="Capitalization Options").click()
            page.wait_for_timeout(2000)

            page.get_by_label("Cost Type").select_option(datadictvalue["C_COST_TYPE"])
            page.wait_for_timeout(2000)
            page.get_by_label("Asset Line Grouping Method").select_option(datadictvalue["C_ASSET_LINE_GRPNG_MTHD"])
            page.wait_for_timeout(2000)
            page.get_by_label("Asset Cost Allocation Method").select_option(datadictvalue["C_ASSET_COST_ALLCTN_MTHD"])
            page.wait_for_timeout(2000)
            page.get_by_label("Event Processing Method").select_option(datadictvalue["C_EVENT_PRCSSNG_MTHD"])
            page.wait_for_timeout(2000)

            if datadictvalue["C_RQR_CMPLT_ASSET_DFNTN"] == 'Yes':
                page.get_by_text("Require complete asset").check()
            if datadictvalue["C_RQR_CMPLT_ASSET_DFNTN"] == 'No' or '':
                page.get_by_text("Require complete asset").uncheck()
            page.wait_for_timeout(2000)
            if datadictvalue["C_USE_GRPNG_MTHD_FOR_SPPLR_INVCS"] == 'Yes':
                page.get_by_text("Use grouping method for").check()
            if datadictvalue["C_USE_GRPNG_MTHD_FOR_SPPLR_INVCS"] == 'No' or '':
                page.get_by_text("Use grouping method for").uncheck()
            page.wait_for_timeout(2000)

            if datadictvalue["C_EXPRT_SPPLR_INVCS_TO_ORCL_FSN_ASSTS"] == 'As merged additions':
                page.get_by_text("As merged additions").check()
                if datadictvalue["C_EXPRT_SPPLR_INVCS_TO_ORCL_FSN_ASSTS"] == 'As new additions':
                    page.get_by_text("As new additions").check()

            page.wait_for_timeout(2000)

            page.get_by_label("Default Capitalized Interest").select_option(datadictvalue["C_DFLT_CPTLZD_INTRST_RATE_SCHDL"])
            page.wait_for_timeout(2000)

            if datadictvalue["C_ALLOW_OVRRD"] == 'Yes':
                page.get_by_text("Allow override").check()
            if datadictvalue["C_ALLOW_OVRRD"] == 'No':
                page.get_by_text("Allow override").uncheck()
            page.wait_for_timeout(2000)

        #Next tab Classifications
        page.get_by_role("link", name="Classifications").click()
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Class Category").select_option(datadictvalue["C_CLASS_CTGRY"])
        page.get_by_label("Class Category").press("Tab")
        page.wait_for_timeout(2000)

        if datadictvalue["C_ASSGN_TO_ALL_PRJCTS"] == 'Yes':
            # page.get_by_role("cell", name="Class Category Agency").locator("label").nth(1).check()
            page.locator("//table[@summary='Classifications']//following::input[@type='checkbox']//following::label").check()
        page.get_by_role("link", name="Capitalization Options").click()
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save", exact=True).click()
        page.get_by_role("button", name="Save and Close").click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1



    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Project Types Saved Successfully")
        datadictvalue["RowStatus"] = "Project Types are added successfully"

    except Exception as e:
        print("Project Types not saved")
        datadictvalue["RowStatus"] = "Project Types are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJ_TYPS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJ_TYPS, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PRJ_TYPS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + PRJ_TYPS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + PRJ_TYPS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
