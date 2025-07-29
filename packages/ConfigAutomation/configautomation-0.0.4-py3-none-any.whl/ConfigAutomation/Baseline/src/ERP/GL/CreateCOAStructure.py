from playwright.sync_api import Playwright, sync_playwright
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
    page.get_by_role("button", name="Offering").click()
    page.get_by_text("Financials", exact=True).click()
    page.get_by_text("Financial Reporting Structures").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Chart of Accounts Structures").click()
    page.get_by_label("Module").click()
    page.get_by_label("Module").type("General ledger")
    page.get_by_label("Module").press("Enter")
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Search", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Manage Structures").click()

    i = 0
    datadictvalue = datadict[i]
    page.get_by_role("button", name="Create").click()
    page.wait_for_timeout(2000)
    page.get_by_label("Structure Code").click()
    page.get_by_label("Structure Code").type(datadictvalue["C_COA_STRCTR_NAME"])
    page.get_by_label("Name").click()
    page.get_by_label("Name").type(datadictvalue["C_COA_STRCTR_NAME"])
    page.get_by_label("Delimiter").click()
    page.get_by_label("Delimiter").select_option(datadictvalue["C_SGMNT_SPRTR"])
    if not page.locator("label").filter(has_text="Enabled").is_checked():
        page.locator("label").filter(has_text="Enabled").click()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(5000)
    page.get_by_label("Name").click()
    page.get_by_label("Name").fill("")
    page.get_by_label("Name").type(datadictvalue["C_COA_STRCTR_NAME"])
    page.get_by_role("button", name="Search", exact=True).click()
    page.get_by_role("button", name="Edit").click()
    page.wait_for_timeout(5000)

    j = 0
    while j < rowcount:
        datadictvalue = datadict[j]
        page.get_by_role("button", name="Create").click()
        page.get_by_label("Segment Code").click()
        page.get_by_label("Segment Code").type(datadictvalue["C_SGMNT"])
        page.get_by_label("Segment Code").press("Tab")
        page.get_by_label("API name").click()
        page.get_by_label("API name").press("Tab")
        page.get_by_label("Name", exact=True).click()
        page.get_by_label("Name", exact=True).type(datadictvalue["C_SGMNT"])
        page.get_by_label("Sequence Number").click()
        page.get_by_label("Sequence Number").type(str(datadictvalue["C_SQNC_NMBR"]))
        page.get_by_label("Prompt", exact=True).click()
        page.get_by_label("Prompt", exact=True).type(datadictvalue["C_SGMNT"])
        page.get_by_label("Short Prompt").click()
        page.get_by_label("Short Prompt").type(datadictvalue["C_SHORT_PRMPT"])
        if not page.get_by_text("Enabled").is_checked():
            page.get_by_text("Enabled").click()
        page.get_by_label("Display Width").click()
        page.get_by_label("Display Width").type(str(datadictvalue["C_DSPLY_WIDTH"]))
        page.get_by_label("Column Name").click()
        page.get_by_label("Column Name").type(datadictvalue["C_SGMNT_CLMN"])
        page.get_by_title("Search: Column Name").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(1000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SGMNT_CLMN"], exact=True).first.click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Default Value Set Code").click()
        page.get_by_label("Default Value Set Code").type(datadictvalue["C_SGMNT"])
        page.get_by_label("Default Value Set Code").press("Enter")
        page.wait_for_timeout(1000)
        print(datadictvalue["C_SGMNT_LABEL"])

        if "Intercompany Segment" == datadictvalue["C_SGMNT_LABEL"]:
            page.get_by_role("option", name=datadictvalue["C_SGMNT_LABEL"]).nth(1).click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Move selected items to:").click()

        elif datadictvalue["C_SGMNT_LABEL"] != "":
            page.get_by_role("option", name=datadictvalue["C_SGMNT_LABEL"]).click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Move selected items to:").click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Save and Close").click()
        print("Row Added - ", str(j))
        datadictvalue["RowStatus"] = "Successfully Created COA Add Structure"
        j = j + 1
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(5000)

    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, CHART_OF_ACCOUNT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, CHART_OF_ACCOUNT, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, CHART_OF_ACCOUNT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + CHART_OF_ACCOUNT)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + CHART_OF_ACCOUNT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))