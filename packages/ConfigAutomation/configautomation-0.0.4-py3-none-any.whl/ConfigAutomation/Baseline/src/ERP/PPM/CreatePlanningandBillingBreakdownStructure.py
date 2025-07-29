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
    page.get_by_role("textbox").fill("Manage Planning and Billing Resource Breakdown Structures")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Planning and Billing Resource Breakdown Structures", exact=True).click()

    #Create Planning and Billing Resource Breakdown Structures
    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        if datadictvalue["C_NAME"] != PrevName:
            # Save the prev type data if the row contains a new type
            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_title("Save", exact=True).click()
                page.get_by_role("button", name="Save and Close").click()
                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("Resource Breakdown Structure Saved")
                    datadict[i - 1]["RowStatus"] = "Resource Breakdown Structure Saved"
                except Exception as e:
                    print("Unable to save Resource Breakdown Structure")
                    datadict[i - 1]["RowStatus"] = "Unable to save Resource Breakdown Structure"

                page.wait_for_timeout(3000)
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)
            page.get_by_role("textbox", name="Name").click()
            page.get_by_role("textbox", name="Name").fill(datadictvalue["C_NAME"])
            page.wait_for_timeout(1000)

            page.get_by_role("textbox", name="Description").click()
            page.get_by_role("textbox", name="Description").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(2000)

            #Entering Project Unit
            page.get_by_title("Search: Project Unit").click()
            page.get_by_role("link", name="Search...").click()
            page.locator("// div[text() = 'Search and Select: Project Unit'] // following::label[text() = 'Name'] // following::input[1]").click()
            page.locator("// div[text() = 'Search and Select: Project Unit'] // following::label[text() = 'Name'] // following::input[1]").fill(datadictvalue["C_PRJCT_UNIT"])
            # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").click()
            # page.get_by_role("cell", name="Name Name Name").get_by_label("Name").fill(datadictvalue["C_PRJCT_UNIT"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRJCT_UNIT"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

            # Enable or Disable Information
            if datadictvalue["C_ALLW_RSRC_CHNGS_TO_PRJCT_LEVEL"] == 'Yes':
                page.get_by_text("Allow resource changes at").check()
            page.wait_for_timeout(2000)

            if datadictvalue["C_ATMTCLLY_ADD_RSRCS_ON_INCRRNG_CTL_MNTS"] == 'Yes':
                page.get_by_text("Automatically add resources").check()
            page.wait_for_timeout(2000)

            # Entering Job Set
            if datadictvalue["C_JOB_SET"]!='':
                page.get_by_title("Search: Job Set").first.click()
                page.get_by_role("link", name="Search...").click()
                # page.get_by_role("cell", name="Code Code Code Name Name Name").get_by_label("Name").click()
                # page.get_by_role("cell", name="Code Code Code Name Name Name").get_by_label("Name").fill(datadictvalue["C_JOB_SET"])
                page.get_by_label("Code").click()
                page.get_by_label("Code").fill(datadictvalue["C_JOB_SET"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_JOB_SET"]).nth(1).click()
                page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

            # Entering From & To Date
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date",exact=True).get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_FROM_DATE"])
            # page.get_by_role("row", name="*From Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"])
            page.locator("//label[text()='From Date']//following::input[1]").first.fill(datadictvalue["C_FROM_DATE"])

            if datadictvalue["C_TO_DATE"] != '':
                # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date",exact=True).get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_TO_DATE"])
                # page.get_by_role("row", name="To Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"])
                page.locator("//label[text()='To Date']//following::input[1]").first.fill(datadictvalue["C_TO_DATE"].strftime('%m/%d/%y'))
            page.wait_for_timeout(2000)
            PrevName = datadictvalue["C_NAME"]

            # Next Tab Select Resource Formats
            page.get_by_role("button", name="Next").click()

            if datadictvalue["C_EVNT_TYPE"] == 'Yes':
                page.get_by_role("row", name="Expand Event Type Event Type").locator("label").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_EXPNDTR_CTGRY"] == 'Yes':
                page.get_by_role("row", name="Expand Expenditure Category").locator("label").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_EXPNDTR_TYPE"] == 'Yes':
                page.get_by_role("row", name="Expand Expenditure Type").locator("label").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_INVNTRY_ITEM"] == 'Yes':
                page.get_by_role("row", name="Expand Inventory Item").locator("label").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_ITEM_CTGRY"] == 'Yes':
                page.get_by_role("row", name="Expand Item Category Item").locator("label").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_JOB"] == 'Yes':
                page.get_by_role("row", name="Expand Job Job").locator("label").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_NAMED_PRSN"] == 'Yes':
                page.get_by_role("row", name="Expand Named Person Named").locator("label").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_ORGNZTN"] == 'Yes':
                page.get_by_role("row", name="Expand Organization").locator("label").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_PRJCT_NNLBR_RSRC"] == 'Yes':
                page.get_by_role("row", name="Expand Project Nonlabor").locator("label").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_RSRC_CLASS"] == 'Yes':
                page.get_by_role("row", name="Expand Resource Class").locator("label").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_RVN_CTGRY"] == 'Yes':
                page.get_by_role("row", name="Expand Revenue Category").locator("label").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_SPPLR"] == 'Yes':
                page.get_by_role("row", name="Expand Supplier Supplier").locator("label").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_SYSTM_PRSN_TYPE"] == 'Yes':
                page.get_by_role("row", name="Expand System Person Type").locator("label").click()
            page.wait_for_timeout(2000)

            #Add Resources Tab
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(2000)


            #Enter Name
        page.get_by_role("button", name="Add").click()
        page.get_by_label("Resource", exact=True).click()
        page.get_by_label("Resource", exact=True).fill(datadictvalue["C_PR_NAME"])
        page.wait_for_timeout(2000)


        # Add Expenditure Category
        page.get_by_title("Search: Expenditure Category").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_RC_EXPNDTR_CTGRY"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RC_EXPNDTR_CTGRY"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # Enter Resource Class
        page.get_by_label("Resource Class").select_option(datadictvalue["C_RC_RSRC_CLASS"])
        page.wait_for_timeout(2000)

        # Enter Spread Curve
        page.get_by_label("Spread Curve").select_option(datadictvalue["C_SPRD_CRV"])
        page.wait_for_timeout(2000)

        # Save and close the data
        page.get_by_role("button", name="Save", exact=True).click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1

        if i==rowcount:
            page.get_by_title("Save", exact=True).click()
            page.get_by_text("Save and Close").click()

            # Done
            page.get_by_role("button", name="Done").click()

            try:
                expect(page.get_by_role("button", name="Actions", exact=True)).to_be_visible()
                print("Planning Resource Breakdown Structure Saved Successfully")
                datadictvalue["RowStatus"] = "Planning Resource Breakdown Structures are added successfully"

            except Exception as e:
                print("Planning Resource Breakdown Structure not saved")
                datadictvalue["RowStatus"] = "Planning Resource Breakdown Structures are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PLN_BLN_BRK_STR):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PLN_BLN_BRK_STR, PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_PFC_CONFIG_WRKBK, PLN_BLN_BRK_STR)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[0] + "_" + PLN_BLN_BRK_STR)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_PFC_CONFIG_WRKBK)[
            0] + "_" + PLN_BLN_BRK_STR + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))