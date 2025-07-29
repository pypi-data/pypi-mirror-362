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
    page.wait_for_timeout(20000)


    # Navigate to Security Console
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Tools", exact=True).click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Security Console").click()
    page.wait_for_timeout(10000)

    # Entering respective option in global Search field and searching
    if page.get_by_role("button", name="OK").is_visible():
        page.get_by_role("button", name="OK").click()
    page.get_by_role("link", name="Roles Roles").click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Create Role").click()
        page.wait_for_timeout(2000)

        # Role Name
        page.get_by_label("Role Name",exact=True).clear()
        page.get_by_label("Role Name", exact=True).type(datadictvalue["C_ROLE_NAME"])
        page.wait_for_timeout(3000)

        # Role Code
        page.get_by_label("Role Code",exact=True).clear()
        page.get_by_label("Role Code",exact=True).type(datadictvalue["C_ROLE_CODE"])
        page.wait_for_timeout(3000)

        # Role Category
        page.get_by_role("combobox", name="Role Category").click()
        page.get_by_role("combobox", name="Role Category").type(datadictvalue["C_ROLE_CATEGORY"])
        page.wait_for_timeout(3000)

        # Description
        if datadictvalue["C_DSCPT"]!='':
            page.get_by_label("Description").clear()
            page.get_by_label("Description").type(datadictvalue["C_DSCPT"])

        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Summary Step: Not Visited Step").click()
        page.wait_for_timeout(5000)

        # Save and Close
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)
        if page.get_by_role("button", name="OK").is_visible():
            page.get_by_role("button", name="OK").click()
        try:
            expect(page.get_by_role("heading", name="Roles")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Segment Roles Created Successfully")
            datadictvalue["RowStatus"] = "Created Segment Roles Successfully"
        except Exception as e:
            print("Unable to Save Segment Roles")
            datadictvalue["RowStatus"] = "Unable to Save Segment Roles"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + SECURITY_OBJ_GRP_CONFIG_WRKBK, SEG_ROLE_OBJ_GRP):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + SECURITY_OBJ_GRP_CONFIG_WRKBK, SEG_ROLE_OBJ_GRP,PRCS_DIR_PATH + SECURITY_OBJ_GRP_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + SECURITY_OBJ_GRP_CONFIG_WRKBK, SEG_ROLE_OBJ_GRP)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", SECURITY_OBJ_GRP_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", SECURITY_OBJ_GRP_CONFIG_WRKBK)[0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


