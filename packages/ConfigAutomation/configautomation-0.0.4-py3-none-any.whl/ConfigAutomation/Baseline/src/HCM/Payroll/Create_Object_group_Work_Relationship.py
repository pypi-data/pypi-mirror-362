from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    #Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    #Navigate to Object Group
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="My Client Groups").click()
    page.get_by_role("link", name="Payroll").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Object Groups").click()
    page.wait_for_timeout(2000)

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

        #Fill name
        page.locator("//div[text()='Create Object Group']//following::label[text()='Name']//following::input[1]").clear()
        page.locator("//div[text()='Create Object Group']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_NAME"])

        #Select type as Deduction Card Group
        page.locator("//div[text()='Create Object Group']//following::label[text()='Legislative Data Group']//following::input[1]").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
        page.wait_for_timeout(3000)

        #Select Static or Dynamic
        if datadictvalue["C_STTC_DYNMC"] == 'Dynamic':
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_STTC_DYNMC"], exact=True).click()
        else:
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_STTC_DYNMC"], exact=True).click()
        page.wait_for_timeout(2000)

        #Select Continue to enter more details
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(2000)

        # Select Start Date
        page.locator("//label[text()='Start Date']//following::input[1]").clear()
        page.locator("//label[text()='Start Date']//following::input[1]").fill(datadictvalue["C_START_DATE"])

        # Select End Date
        page.locator("//label[text()='End Date']//following::input[1]").clear()
        page.locator("//label[text()='End Date']//following::input[1]").fill(datadictvalue["C_END_DATE"])

        #Enter Description
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        #Go to Next page to enter more details
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(2000)

        #HR Worker Relationship
        if datadictvalue["C_HR_WRKR_NMBR"] != 'N/A' or '':
            page.get_by_role("button", name="Add").first.click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name="Value").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Worker Number").click()
            page.get_by_label("Worker Number").fill(str(datadictvalue["C_HR_WRKR_NMBR"]))
            page.get_by_role("button", name="Search").click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name=str(datadictvalue["C_HR_WRKR_NMBR"])).click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Inclusion Status").click()
            page.get_by_text(datadictvalue["C_HR_INCLSN_STTS"]).click()

        #HR Terms
        if datadictvalue["C_EMPLYMNT_TERMS_NMBR"] != 'N/A' or '':
            page.get_by_role("button", name="Add").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name="Value").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Employment Terms Number").click()
            page.get_by_label("Employment Terms Number").fill(datadictvalue["C_EMPLYMNT_TERMS_NMBR"])
            page.get_by_role("button", name="Search").click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name=datadictvalue["C_EMPLYMNT_TERMS_NMBR"]).click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Inclusion Status").click()
            page.get_by_text(datadictvalue["C_HR_TERMS_INCLSN_STTS"]).click()

        #HR Assignment
        if datadictvalue["C_HR_ASSGNMNT_NMBR"] != 'N/A' or '':
            page.get_by_role("button", name="Add").nth(2).click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name="Value").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Assignment Number").click()
            page.get_by_label("Assignment Number").fill(datadictvalue["C_HR_ASSGNMNT_NMBR"])
            page.get_by_role("button", name="Search").click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name=datadictvalue["C_HR_ASSGNMNT_NMBR"]).click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Inclusion Status").click()
            page.get_by_text(datadictvalue["C_HR_ASSGNMNT_INCLSN_STTS"]).click()

        #Submit to create an object
        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(3000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

    # Validation
    try:
        expect(page.get_by_role("heading", name="Object Groups")).to_be_visible()
        print("Object Group Created Successfully")

    except Exception as e:
        print("Object Group Creation UnSuccessfull")

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_WRK_REL):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_WRK_REL, PRCS_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_WRK_REL)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_OBJ_GRP_CONFIG_WRKBK)[0] + "_" +DST_OBJ_GRP_WRK_REL)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_OBJ_GRP_CONFIG_WRKBK)[0] + "_" +DST_OBJ_GRP_WRK_REL + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))