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

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(40000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Cost Allocation Key Flexfield")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Cost Allocation Key Flexfield", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Manage Structures").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        if i==0:
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Structure Code").clear()
            page.get_by_label("Structure Code").type(datadictvalue["C_STRCTR_CODE"])
            page.get_by_label("Name").clear()
            page.get_by_label("Name").type(datadictvalue["C_KEY_NAME"])
            page.get_by_label("Description").clear()
            page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])
            page.get_by_label("Delimiter").select_option(datadictvalue["C_DLMTR"])
            page.get_by_role("button", name="Save", exact=True).click()

        if i>=0:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)

            # Entering Segment Code
            page.get_by_label("Segment Code").type(datadictvalue["C_SGMNT_CODE"])
            page.get_by_label("API Name").click()

            # Entering Name
            page.get_by_label("Name", exact=True).type(datadictvalue["C_STRCTR_CODE_NAME"])

            # Entering Description
            page.get_by_label("Description").fill(datadictvalue["C_STRCTR_CODE_DSCRPTN"])

            # Entering Sequence Number
            page.get_by_label("Sequence Number").type(str(datadictvalue["C_STRCTR_CODE_SQNC_NMBR"]))

            # Entering Prompt Value
            page.get_by_label("Prompt", exact=True).type(datadictvalue["C_PRMPT"])

            # Entering Short Propmt
            page.get_by_label("Short Prompt").fill(datadictvalue["C_SHRT_PRMPT"])

            # Selecting Enabled or not
            page.get_by_text("Enabled").check()

            # Entering Display Width
            page.get_by_label("Display Width").type(str(datadictvalue["C_DSPLY_WDTH"]))

            # Select Column Name
            page.get_by_title("Search: Column Name").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.locator("//div[text()='Search and Select: Column Name']//following::label[text()='Name']//following::input[1]").type(datadictvalue["C_CLMN_NAME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CLMN_NAME"], exact=True).click()
            page.get_by_role("button", name="OK").click()

            # Selecting Default Value Set Fund
            page.get_by_title("Search: Default Value Set Code").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.locator("//div[text()='Search and Select: Default Value Set Code']//following::label[text()='Value Set Code']//following::input[1]").type(datadictvalue["C_DFLT_VALUE_SET_CODE"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_DFLT_VALUE_SET_CODE"]).first.click()
            page.get_by_role("button", name="OK").click()

            # Select Segment Labels
            if datadictvalue["C_SLCTD_LBLS_OFFST"]!='N/A':
                page.get_by_role("option", name=datadictvalue["C_SLCTD_LBLS_OFFST"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Move selected items to:").click()
            if datadictvalue["C_SLCTD_LBLS_DPRTMNT"]!='N/A':
                page.get_by_role("option", name=datadictvalue["C_SLCTD_LBLS_DPRTMNT"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Move selected items to:").click()
            if datadictvalue["C_SLCTD_LBLS_PYRLL"]!='N/A':
                page.get_by_role("option", name=datadictvalue["C_SLCTD_LBLS_PYRLL"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Move selected items to:").click()
            if datadictvalue["C_SLCTD_LBLS_ELMNT_ENTRY"] != 'N/A':
                page.get_by_role("option", name=datadictvalue["C_SLCTD_LBLS_ELMNT_ENTRY"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Move selected items to:").click()
            if datadictvalue["C_SLCTD_LBLS_ELMNT"] != 'N/A':
                page.get_by_role("option", name=datadictvalue["C_SLCTD_LBLS_ELMNT"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Move selected items to:").click()
            if datadictvalue["C_SLCTD_LBLS_JOB"] != 'N/A':
                page.get_by_role("option", name=datadictvalue["C_SLCTD_LBLS_JOB"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Move selected items to:").click()
            if datadictvalue["C_SLCTD_LBLS_PRSN"] != 'N/A':
                page.get_by_role("option", name=datadictvalue["C_SLCTD_LBLS_PRSN"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Move selected items to:").click()
            if datadictvalue["C_SLCTD_LBLS_PRSN_ELMNT"] != 'N/A':
                page.get_by_role("option", name=datadictvalue["C_SLCTD_LBLS_PRSN_ELMNT"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Move selected items to:").click()
            if datadictvalue["C_SLCTD_LBLS_PSTN"] != 'N/A':
                page.get_by_role("option", name=datadictvalue["C_SLCTD_LBLS_PSTN"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Move selected items to:").click()

            page.get_by_role("button", name="Save and Close").click()
            # page.get_by_role("button", name="Cancel").click()
            page.wait_for_timeout(3000)

        i = i + 1

        if i == rowcount:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            # page.get_by_role("button", name="Cancel").click()
            page.wait_for_timeout(3000)

    try:
        expect(page.get_by_role("heading", name="Manage Key Flexfield")).to_be_visible()
        page.wait_for_timeout(3000)
        print("Manage Structures Created Successfully")
        datadictvalue["RowStatus"] = "Manage Structures Saved"
    except Exception as e:
        print("Unable to Create Manage Structures")
        datadictvalue["RowStatus"] = "Unable to Create Manage Structures"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + COST_ALLOCATION_FLEX_FIELDS, MANAGE_STRUCTURE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + COST_ALLOCATION_FLEX_FIELDS, MANAGE_STRUCTURE,PRCS_DIR_PATH + COST_ALLOCATION_FLEX_FIELDS)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + COST_ALLOCATION_FLEX_FIELDS, MANAGE_STRUCTURE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", COST_ALLOCATION_FLEX_FIELDS)[0] + "_" + MANAGE_STRUCTURE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", COST_ALLOCATION_FLEX_FIELDS)[0] + "_" + MANAGE_STRUCTURE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

