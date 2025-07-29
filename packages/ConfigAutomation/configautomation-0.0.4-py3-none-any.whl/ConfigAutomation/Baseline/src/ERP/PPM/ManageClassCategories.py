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
    page.get_by_role("textbox").fill("Manage Project Class Categories")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Project Class Categories").click()
    page.wait_for_timeout(3000)

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        if datadictvalue["C_NAME"] != PrevName:

        # Create Class Category
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            # page.get_by_role("row", name="*From Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"])
            page.locator("//label[text()='From Date']//following::input[1]").fill(datadictvalue["C_FROM_DATE"])
            if datadictvalue["C_TO_DATE"]!='':
                page.locator("//label[text()='To Date']//following::input[1]").fill(datadictvalue["C_TO_DATE"])
                # page.get_by_role("row", name="To Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"])
                # page.get_by_placeholder("mm-dd-yyyy").nth(1).fill(datadictvalue["C_TO_DATE"])
            if datadictvalue["C_ASSGN_TO_ALL_PRJCTS"] == 'Yes':
                if not page.get_by_role("cell", name="Assign to all projects", exact=True).is_checked():
                    page.get_by_role("cell", name="Assign to all projects", exact=True).click()
                    if datadictvalue["C_AVLBL_AS_ACCNTNG_SRC"] == 'Yes':
                        page.get_by_text("Available as accounting source").click()

            if datadictvalue["C_ASSGN_TO_ALL_PRJCT_TYPES"] == 'Yes':
                page.get_by_text("Assign to all project types").click()

            if datadictvalue["C_ONE_CLSS_CODE_PER_PRJCT"] == 'Yes':
                page.get_by_text("One class code per project").click()

            if datadictvalue["C_ENTR_CLSS_CODES_PRCNT"] == 'Yes':
                page.get_by_text("Enter class codes percent").click()
                if datadictvalue["C_TTL_PRCNT_MUST_EQL_100"] == 'Yes':
                    # page.get_by_role("cell", name="Total percent must equal").nth(4).click()
                    page.get_by_text("Total percent must equal").click()
            PrevName = datadictvalue["C_NAME"]

        j = 0
        while j < rowcount:

            datadictvalue = datadict[j]

            if PrevName == datadictvalue["C_NAME"]:
                if datadictvalue["C_CC_NAME"] != "":
                    page.wait_for_timeout(2000)

            # Additional Information
            # Class Codes
                page.get_by_role("link", name="Class Codes").click()
                page.wait_for_timeout(1000)
                page.get_by_role("button", name="Add Row").first.click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Expand Name Class Code").get_by_label("Name").fill(datadictvalue["C_CC_NAME"])
                page.get_by_label("Class Code Description").fill(datadictvalue["C_CLASS_CODE_DSCRPTN"])
                page.locator("//span[text()='To Date']//following::input[contains(@placeholder,'m/d/yy')][1]").fill(datadictvalue["C_CC_FROM_DATE"])
                if datadictvalue["C_CC_TO_DATE"] != '':
                    # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date").get_by_placeholder("m/d/yy").fill(datadictvalue["C_CC_TO_DATE"])
                    page.locator("//span[text()='To Date']//following::input[contains(@placeholder,'m/d/yy')][2]')]").fill(datadictvalue["C_CC_TO_DATE"])
                #Assigned Sets
                page.get_by_role("button", name="Add Row").nth(1).click()
                page.wait_for_timeout(1000)
                page.get_by_role("table", name="Assigned Sets").locator("a").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Code", exact=True).fill(datadictvalue["C_SET_CODE"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.get_by_role("cell", name=datadictvalue["C_SET_CODE"], exact=True).click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)
                # Project Type
                page.get_by_role("link", name="Project Types").click()
                page.wait_for_timeout(2000)
                if datadictvalue["C_PRJCT_TYPE"] != '':
                    page.get_by_role("button", name="Add Row").click()
                    page.wait_for_timeout(2000)
                    page.get_by_role("combobox").fill(datadictvalue["C_PRJCT_TYPE"])
                    if datadictvalue["C_PT_TYPE_ASSGN_TO_ALL_PRJCTS"] == 'Yes' :
                        if not page.get_by_role("table", name="Project Types").locator("label").is_checked():
                            page.get_by_role("table", name="Project Types").locator("label").click()
                    if datadictvalue["C_PT_TYPE_ASSGN_TO_ALL_PRJCTS"] == 'No' :
                        if page.get_by_role("table", name="Project Types").locator("label").is_checked():
                            page.get_by_role("table", name="Project Types").locator("label").click()
                j = j + 1
            page.wait_for_timeout(2000)
            i = i + 1
            # Save and Close
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"



        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Done").click()
        # page.get_by_role("button", name="Save and Close").click()

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Class Category Saved Successfully")
            # datadictvalue["RowStatus"] = "Burden Cost Bases are added successfully"

        except Exception as e:
            print("Class Category Bases not saved")
            # datadictvalue["RowStatus"] = "Burden Cost Bases are not added"

        OraSignOut(page, context, browser, videodir)
        return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, MGE_CLASS_CTG):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, MGE_CLASS_CTG, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, MGE_CLASS_CTG)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + MGE_CLASS_CTG)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + MGE_CLASS_CTG + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))