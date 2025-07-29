from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *
def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox").type("Manage extensible flexfield")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Extensible Flexfields").first.click()
    page.wait_for_timeout(4000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.get_by_label("Flexfield Code").click()
        page.get_by_label("Flexfield Code").fill("")
        page.get_by_label("Flexfield Code").type(datadictvalue["C_FLXFLD_CODE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.get_by_text(datadictvalue["C_FLXFLD_CODE"]).click()
        page.get_by_role("button", name="Edit").click()
        page.wait_for_timeout(2000)

        if datadictvalue["C_ATTBTS"] == "N/A":
            page.get_by_role("link", name="Expand").first.click()
            #Cick on display name
            page.get_by_text("Person Extra Information", exact=True).click()

        else:
            #Expand Display Name
            page.get_by_role("link", name="Expand").first.click()
            page.wait_for_timeout(3000)
            #Click on Attribute name
            page.get_by_text(datadictvalue["C_ATTBTS"], exact=True).click()
            page.wait_for_timeout(5000)

        #page.get_by_role("cell", name="Expand Organization", exact=True)
        #page.get_by_text("Person Extra Information", exact=True).click()
        page.get_by_role("button", name="Manage Contexts").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create").first.click()
        page.wait_for_timeout(5000)
        page.get_by_label("Display Name").first.click()
        page.get_by_label("Display Name").first.type(datadictvalue["C_CONTXT_DISPLY_NAME"])
        page.get_by_label("Display Name").first.press("Tab")
        page.wait_for_timeout(2000)
        #page.get_by_label("Code").first.click()
        #page.get_by_label("API name").click()
        #page.get_by_label("Description").click()
        page.get_by_label("Behavior").click()
        page.get_by_label("Behavior").select_option(datadictvalue["C_BHVR"])
        page.get_by_label("Instruction Help Text").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Create").nth(1).click()
        page.wait_for_timeout(2000)
        page.get_by_label("FlexfieldUsageCode").click()
        page.wait_for_timeout(1000)
        page.get_by_label("FlexfieldUsageCode").select_option(datadictvalue["C_CNTXT_USAGE_NAME"])
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(5000)

        #Adding Segement to the FlexFields
        if page.get_by_role("button", name="Create").first.is_visible():
            page.get_by_role("button", name="Create").first.click()
        page.wait_for_timeout(5000)
        page.get_by_label("Name").first.click()
        page.get_by_label("Name").first.type(datadictvalue["C_NAME"])
        page.get_by_label("Name").first.press("Tab")
        page.wait_for_timeout(2000)

        page.get_by_label("Data Type").click()
        page.get_by_label("Data Type").select_option(datadictvalue["C_DATA_TYPE"])
        page.get_by_label("Value Set").click()
        page.get_by_label("Value Set").type(datadictvalue["C_VALUE_SET"])
        page.get_by_label("Value Set").press("Tab")

        if datadictvalue["C_DFLT_TYPE"] != "N/A":
            page.get_by_label("Default Type").click()
            page.get_by_label("Default Type").select_option(datadictvalue["C_DFLT_TYPE"])
            page.get_by_label("Default Value").click()
            page.get_by_label("Default Value").type(datadictvalue["C_DFLT_VALUE"])
        page.get_by_label("Prompt").click()
        page.get_by_label("Prompt").fill("")
        page.get_by_label("Prompt").type(datadictvalue["C_PROMPT"])
        page.get_by_label("Display Type").click()
        page.get_by_label("Display Type").select_option(datadictvalue["C_DSPLY_TYPE"])
        page.get_by_label("Display Size").click()
        page.get_by_label("Display Size").type(str(datadictvalue["C_DSPLY_SIZE"]))
        page.get_by_label("Display Height").click()
        page.get_by_label("Display Height").type(str(datadictvalue["C_DSPLY_HEIGHT"]))
        if datadictvalue["C_RQRD"] == "Yes":
            if not page.get_by_text("Required").is_checked():
                page.get_by_text("Required").click()
        if datadictvalue["C_RQRD"] == "Yes":
            if not page.get_by_text("Read-only").is_checked():
                page.get_by_text("Read-only").click()
        if datadictvalue["C_RQRD"] == "Yes":
            if not page.get_by_text("BI Enabled").is_checked():
                page.get_by_text("BI Enabled").click()
        page.pause()
        page.get_by_role("button", name="Save", exact=True).click()
        page.get_by_role("button", name="Save and Close").click()

        try:
            expect(page.get_by_role("link", name="Manage Business Unit", exact=True).first.click()).to_be_visible()
            print("Added Flexfield Segment Saved Successfully")
            datadictvalue["RowStatus"] = "Added Flexfield Segment"
        except Exception as e:
            print("Unable to save Flexfield Segment")
            datadictvalue["RowStatus"] = "Unable to Add Flexfield Segment"
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Added Flexfield Segment Successfully"
        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_EFF):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_EFF, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_EFF)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + MANAGE_EFF + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
