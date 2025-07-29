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
    page.wait_for_timeout(1000)
    page.get_by_role("textbox").fill("Manage Parse Rule Sets")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Parse Rule Sets", exact=True).click()

    PrevName = ''

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)

        if datadictvalue["C_NAME"] != PrevName:
            # Save the prev type data if the row contains a new type
            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(2000)
                if page.get_by_role("button", name="Yes").is_visible():
                    page.get_by_role("button", name="Yes").click()
                page.wait_for_timeout(2000)
                if page.get_by_role("button", name="OK").is_visible():
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(2000)
                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("Parse Rule Sets Saved")
                    datadict[i - 1]["RowStatus"] = "Parse Rule Sets Saved"
                except Exception as e:
                    print("Unable to save Parse Rule Sets")
                    datadict[i - 1]["RowStatus"] = "Unable to save Parse Rule Sets"
                page.wait_for_timeout(1000)

            # Create
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)

            # Name
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])

            # Description
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

            # Active
            if datadictvalue["C_ACTV"] == "Yes":
                page.locator("//label[text()='Active']").check()
                # page.get_by_role("row", name="Active", exact=True).locator("label").check()
            if datadictvalue["C_ACTV"] == "No":
                page.locator("//label[text()='Active']").uncheck()
                # page.get_by_role("row", name="Active", exact=True).locator("label").uncheck()
            PrevName = datadictvalue["C_NAME"]

        # Parse Rules
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(3000)

        # Active
        if datadictvalue["C_RULES_ACTV"] == 'Yes':
            page.locator("//span[text()='Active']//following::input[1]").check()
            # page.get_by_role("table", name="Parse Rules").get_by_role("row").nth(0).locator("label").first.check()
        if datadictvalue["C_RULES_ACTV"] == 'No':
            page.locator("//span[text()='Active']//following::input[1]").uncheck()
            # page.get_by_role("table", name="Parse Rules").get_by_role("row").nth(0).locator("label").first.uncheck()

        # Transaction Code
        page.get_by_label("Transaction Code").nth(0).click()
        page.get_by_label("Transaction Code").nth(0).fill(str(datadictvalue["C_TRNSCTN_CODE"]))

        # Source Field
        page.get_by_label("Source Field").nth(0).type(datadictvalue["C_SRC_FIELD"])
        page.get_by_role("option", name=datadictvalue["C_SRC_FIELD"]).click()

        # Target Field
        page.get_by_label("Target Field").nth(0).type(datadictvalue["C_TRGT_FIELD"])
        page.get_by_role("option", name=datadictvalue["C_TRGT_FIELD"]).click()

        # Rule
        page.get_by_label("Rule").nth(0).fill(datadictvalue["C_RULE"])

        # Overwrite
        if datadictvalue["C_OVRWRT"] == 'Yes':
            page.get_by_role("table", name="Parse Rules").get_by_role("row").nth(0).locator("label").nth(5).check()
        if datadictvalue["C_OVRWRT"] == 'No':
            page.get_by_role("table", name="Parse Rules").get_by_role("row").nth(0).locator("label").nth(5).uncheck()
            page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        if i == rowcount:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)

            if page.get_by_role("button", name="Yes").is_visible():
                page.get_by_role("button", name="Yes").click()
                page.wait_for_timeout(2000)

            if page.get_by_role("button", name="OK").is_visible():
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Parse Rule Sets Saved Successfully")
            datadictvalue["RowStatus"] = "Parse Rule Sets are added successfully"

        except Exception as e:
            print("Parse Rule Sets not saved")
            datadictvalue["RowStatus"] = "Parse Rule Sets are not added"

    page.wait_for_timeout(2000)
    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, PARSE_RULE_SETS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, PARSE_RULE_SETS, PRCS_DIR_PATH + CM_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + CM_WORKBOOK, PARSE_RULE_SETS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0] + "_" + PARSE_RULE_SETS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0] + "_" + PARSE_RULE_SETS +
                     "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
