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
    page.get_by_role("link", name="Home", exact=True).click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="My Client Groups").click()
    page.get_by_role("link", name="Payroll").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Object Groups").click()
    page.wait_for_timeout(4000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        # Select Legislative data group
        page.get_by_role("combobox", name="Legislative Data Group").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTV_DATA_GROUP"], exact=True).click()
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)

        # Create Object Group
        page.get_by_role("button", name="Create").click()

        # Fill name
        page.locator("//div[text()='Create Object Group']//following::label[text()='Name']//following::input[1]").clear()
        page.locator("//div[text()='Create Object Group']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_NAME"])

        # Select type as Deduction Card Group
        page.locator("//div[text()='Create Object Group']//following::label[text()='Legislative Data Group']//following::input[1]").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
        page.wait_for_timeout(3000)

        # Select Continue to enter more details
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(5000)

        # Select Start Date
        page.locator("//label[text()='Start Date']//following::input[1]").clear()
        page.locator("//label[text()='Start Date']//following::input[1]").fill(datadictvalue["C_START_DATE"])

        # Select End Date
        page.locator("//label[text()='End Date']//following::input[1]").clear()
        page.locator("//label[text()='End Date']//following::input[1]").fill(datadictvalue["C_END_DATE"])

        # Enter Description
        page.get_by_label("Description").clear()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(2000)

        #Enter ObjectGroup
        page.get_by_role("link", name="Value").click()
        page.get_by_label("Object Group Parameters").click()
        page.get_by_label("Object Group Parameters").fill(datadictvalue["C_OBJCT_USG_TYPE"])
        page.get_by_role("button", name="Search").click()
        page.get_by_role("link", name=datadictvalue["C_OBJCT_USG_TYPE"]).click()
        page.get_by_role("button", name="Next").click()
        if datadictvalue["C_ELMNT_CLSSFCTN_DSPLY_VALUE"] != 'N/A':
            page.get_by_role("button", name="Add").first.click()
            page.get_by_role("link", name="Value").click()
            page.get_by_role("textbox", name="Element Classification Name").click()
            page.get_by_role("textbox", name="Element Classification Name").type(datadictvalue["C_ELMNT_CLSSFCTN_DSPLY_VALUE"])
            page.get_by_role("button", name="Search").click()
            page.get_by_role("link", name=datadictvalue["C_ELMNT_CLSSFCTN_DSPLY_VALUE"]).click()
            page.wait_for_timeout(3000)
        if datadictvalue["C_ELMNT_DSPLY_VALUE"] != 'N/A':
            page.get_by_role("button", name="Add").nth(1).click()
            page.wait_for_timeout(3000)
            page.get_by_role("cell", name="Value Include Inclusion").get_by_role("link").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Element Name").click()
            page.get_by_label("Element Name").fill(datadictvalue["C_ELMNT_DSPLY_VALUE"])
            page.get_by_role("button", name="Search").click()
            page.get_by_role("link", name=datadictvalue["C_ELMNT_DSPLY_VALUE"]).click()
            page.get_by_role("combobox", name="Inclusion Status").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ELMNT_INCLSN_STTS"], exact=True).click()
            page.wait_for_timeout(3000)

        #page.get_by_role("button", name="Cancel").click()
        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(5000)

        i = i + 1
        # Validation
        try:
            expect(page.get_by_role("heading", name="Object Groups")).to_be_visible()
            print("Object Group Elements Created Successfully")

        except Exception as e:
            print("Object Group Creation Elements UnSuccessfull")


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_ELE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_ELE, PRCS_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_ELE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_OBJ_GRP_CONFIG_WRKBK)[0] + "_" +DST_OBJ_GRP_ELE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_OBJ_GRP_CONFIG_WRKBK)[0] + "_" +DST_OBJ_GRP_ELE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))