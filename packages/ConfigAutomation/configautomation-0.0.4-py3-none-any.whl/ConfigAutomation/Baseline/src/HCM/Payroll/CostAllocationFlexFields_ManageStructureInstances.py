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
    page.get_by_role("button", name="Manage Structure Instances").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)

        # Enter Structure Instance Code
        page.get_by_label("Structure Instance Code").clear()
        page.get_by_label("Structure Instance Code").type(datadictvalue["C_STRCTR_INSTNCS_CODE"])
        page.get_by_label("API name").click()
        page.wait_for_timeout(2000)

        # Enter Name
        page.get_by_label("Name", exact=True).type(datadictvalue["C_STRCTR_INSTNCS_NAME"])

        # Enter Description
        page.get_by_label("Description").type(datadictvalue["C_STRCTR_INSTNCS_DSCRPTN"])

        # Selecting Enabled option
        if datadictvalue["C_STRCTR_INSTNCS_ENBLD"]=="Yes":
            page.get_by_text("Enabled").check()
        elif datadictvalue["C_STRCTR_INSTNCS_ENBLD"]=="No":
            page.get_by_text("Enabled").uncheck()

        # Selecting Dynamic combination creation
        if datadictvalue["C_STRCTR_INSTNCS_CMBNTN_CRTN"]=="Yes":
            page.get_by_text("Dynamic combination creation").check()
        elif datadictvalue["C_STRCTR_INSTNCS_CMBNTN_CRTN"]=="No":
            page.get_by_text("Dynamic combination creation").uncheck()

        # Selecting Structure Name
        # page.get_by_role("cell", name="Structure Name", exact=True).get_by_label("Structure Name").select_option(datadictvalue["C_STRCTR_INSTNCS_STRCTR_NAME"])
        page.get_by_label("Structure Name").select_option(datadictvalue["C_STRCTR_INSTNCS_STRCTR_NAME"])

        # Saving the Record
        page.get_by_role("button", name="Save and Close").click()

        page.wait_for_timeout(3000)
        try:
            expect(page.get_by_role("heading", name="Manage Key Flexfield Structure Instances")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Manage Structure Instances Created Successfully")
            datadictvalue["RowStatus"] = "Manage Structure Instances Saved"
        except Exception as e:
            print("Unable to Create Manage Structure Instances")
            datadictvalue["RowStatus"] = "Unable to Create Manage Structure Instances"
        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + COST_ALLOCATION_FLEX_FIELDS, MANAGE_STRUCTURE_INST):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + COST_ALLOCATION_FLEX_FIELDS, MANAGE_STRUCTURE_INST,PRCS_DIR_PATH + COST_ALLOCATION_FLEX_FIELDS)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + COST_ALLOCATION_FLEX_FIELDS, MANAGE_STRUCTURE_INST)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", COST_ALLOCATION_FLEX_FIELDS)[0] + "_" + MANAGE_STRUCTURE_INST)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", COST_ALLOCATION_FLEX_FIELDS)[0] + "_" + MANAGE_STRUCTURE_INST + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


