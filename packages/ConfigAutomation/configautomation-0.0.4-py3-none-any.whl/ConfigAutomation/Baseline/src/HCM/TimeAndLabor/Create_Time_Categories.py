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
    page.wait_for_timeout(3000)

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Time Categories")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Time Categories", exact=True).click()
    page.wait_for_timeout(2000)

    PrevCat = ''

    i = 0

    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        if datadictvalue["C_NAME"] != PrevCat:
            if i > 0:
                page.wait_for_timeout(5000)
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(3000)
                if page.get_by_role("button", name="OK").is_visible():
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(3000)
                page.wait_for_timeout(2000)

            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(4000)

            # Name
            page.get_by_label("Name", exact=True).click()
            page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
            page.wait_for_timeout(2000)

            # Description
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(2000)

            # Track Usage
            if datadictvalue["C_TRACK_USAGE"] == 'Yes':
                page.get_by_text("Yes", exact=True).click()
                page.wait_for_timeout(3000)
                if page.get_by_role("button", name="OK").is_visible():
                    page.wait_for_timeout(2000)
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(2000)
            if datadictvalue["C_TRACK_USAGE"] == 'No':
                page.get_by_text("No", exact=True).click()
                page.wait_for_timeout(2000)

            # Unit of Measure
            page.get_by_role("combobox", name="Unit of Measure").click()
            page.get_by_text(datadictvalue["C_UNIT_OF_MSR"], exact=True).click()
            page.wait_for_timeout(3000)

            PrevCat = datadictvalue["C_NAME"]
        page.wait_for_timeout(3000)
        # page.pause()

        # Add Category Conditions
        if datadictvalue["C_TRACK_USAGE"] == 'Yes':
            page.locator("(// span[text() = 'Time Attribute'] // following::td)[5]").dblclick()
            page.wait_for_timeout(9000)
        if datadictvalue["C_TRACK_USAGE"] == 'No':
            page.locator("//table[@summary='Category Conditions']//following::tr[@_afrrk="+str(i)+"]").dblclick()
            page.wait_for_timeout(9000)
        # page.wait_for_timeout(9000)

        # Time Attribute
        page.wait_for_timeout(4000)
        # page.locator("//a[@title='Value']").click()
        # page.locator("//a[@title='Value']").click()
        page.get_by_role("cell", name="Time Attribute Value Autocompletes on TAB", exact=True).locator("a").click()
        page.wait_for_timeout(3000)
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(2000)
        page.locator("//div[text()='Search and Select : Time Attribute']//following::label[text()='Name']//following::input[1]").click()
        page.wait_for_timeout(2000)
        page.locator("//div[text()='Search and Select : Time Attribute']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_TIME_ATTRBT"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TIME_ATTRBT"], exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # Value Type
        page.get_by_role("combobox", name="Value Type").click()
        page.wait_for_timeout(3000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VALUE_TYPE"]).click()
        page.wait_for_timeout(3000)

        # Value
        if datadictvalue["C_VALUE"] != 'N/A':
            page.get_by_role("cell", name="Value Autocompletes on TAB", exact=True).locator("a").click()
            page.wait_for_timeout(3000)
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_role("textbox", name="Value").click()
            page.get_by_role("textbox", name="Value").fill(str(datadictvalue["C_VALUE"]))
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(str(datadictvalue["C_VALUE"])).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)

        # Operator
        if datadictvalue["C_OPRTR"] != 'N/A':
            if page.get_by_role("combobox", name="Operator").is_visible():
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Operator").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OPRTR"], exact=True).click()
                page.wait_for_timeout(3000)
            else:
                page.get_by_role("button", name="Add", exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Operator").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OPRTR"], exact=True).click()
                page.wait_for_timeout(3000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Save and Close
        if i == rowcount:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
            if page.get_by_role("button", name="OK").is_visible():
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)
            page.wait_for_timeout(2000)

        try:
            expect(page.get_by_role("heading", name="Time Categories")).to_be_visible()
            # expect(page.get_by_role("button", name="OK")).to_be_visible()
            print("TIME_CATEGORIES Saved Successfully")
            datadictvalue["RowStatus"] = "Added TIME_CATEGORIES"
        except Exception as e:
            print("Unable to save TIME_CATEGORIES")
            datadictvalue["RowStatus"] = "Unable to Add TIME_CATEGORIES"

    page.wait_for_timeout(3000)
    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, TIME_CATEGORIES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, TIME_CATEGORIES, PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, TIME_CATEGORIES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0] + "_" + TIME_CATEGORIES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0] + "_" + TIME_CATEGORIES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
