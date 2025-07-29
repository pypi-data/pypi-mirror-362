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
    page.get_by_role("link", name="User-Defined Criteria").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(3000)

        # Name
        if datadictvalue["C_NAME"]!='':
            page.locator("//div[text()='Create User-Defined Criteria']//following::input[1]").clear()
            page.locator("//div[text()='Create User-Defined Criteria']//following::input[1]").type(datadictvalue["C_NAME"])

        # Short Code
        if datadictvalue["C_SHORT_CODE"]!='':
            page.get_by_label("Short Code").clear()
            page.get_by_label("Short Code").type(datadictvalue["C_SHORT_CODE"])

        # Description
        if datadictvalue["C_DSCRPTN"]!='':
            page.get_by_label("Description").clear()
            page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])

        # Table
        if datadictvalue["C_TABLE"]!='':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Table").click()
            page.get_by_text(datadictvalue["C_TABLE"],exact=True).click()

        # Lookup
        if datadictvalue["C_LKP"]!='':
            page.get_by_title("Sea&rch").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_label("LookupType").clear()
            page.get_by_label("LookupType").type(datadictvalue["C_LKP"])
            page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_LKP"],exact=True).click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="OK").click()

        # Column
        if datadictvalue["C_CLMN"]!='':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Column").click()
            page.get_by_text(datadictvalue["C_CLMN"],exact=True).click()
            page.wait_for_timeout(2000)

        # Enable Range Validation
        if datadictvalue["C_ENBL_RANGE_VLDTN"]== "X":
            page.get_by_text("Enable range validation").check()
            page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(6000)

        try:
            expect(page.get_by_role("heading", name="User-Defined Criteria")).to_be_visible()
            page.wait_for_timeout(3000)
            print("User Defined Criteria Created Successfully")
            datadictvalue["RowStatus"] = "User Defined Criteria Created Successfully"
        except Exception as e:
            print("Unable to Create User Defined Criteria")
            datadictvalue["RowStatus"] = "Unable to Save User Defined Criteria"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, USR_DEF_CRITERIA):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, USR_DEF_CRITERIA,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, USR_DEF_CRITERIA)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + USR_DEF_CRITERIA)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + USR_DEF_CRITERIA + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




