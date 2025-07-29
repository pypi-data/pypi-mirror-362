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

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Define Time and Labor")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Define Time and Labor", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Time Rule Sets").click()
    page.wait_for_timeout(4000)

    i = 0

    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Search for Rule set
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill("")
        page.wait_for_timeout(1000)
        page.get_by_label("Name").type(datadictvalue["C_NAME"])
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill("")
        page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Rule Set Type").click()
        page.wait_for_timeout(1000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RULE_SET_TYPE"]).click()
        page.get_by_placeholder("m/d/yy").click()
        page.get_by_placeholder("m/d/yy").fill("")
        page.wait_for_timeout(1000)
        page.get_by_placeholder("m/d/yy").type(datadictvalue["C_EFFCTV_START_DATE"])
        page.get_by_placeholder("m/d/yy").press("Tab")
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(6000)

        # if Rule Set is Visible - Click on Visible Rule Set
        if page.get_by_role("link", name=datadictvalue["C_NAME"]).is_visible():
            page.get_by_role("link", name=datadictvalue["C_NAME"]).click()
            print("Rule Set present already")
            page.wait_for_timeout(5000)

            # Check Member Name is already exists
            if page.locator("//span[text()='RULE']//following::span[text()='" + datadictvalue["C_MMBR_NAME"] + "']").is_visible():
                print("Rule Member Name is visible")
            if page.locator("//span[text()='RULE SET']//following::span[text()='" + datadictvalue["C_MMBR_NAME"] + "']").is_visible():
                print("Rule set Member Name is visible")
                page.wait_for_timeout(3000)

            # If no Member Name exists - Create a new sequence for existing Rule Set
            else:
                page.get_by_role("button", name="Edit").click()
                page.wait_for_timeout(2000)
                page.get_by_text("Correct", exact=True).click()
                page.wait_for_timeout(2000)
                if page.get_by_text("You chose to correct the selected record. Your changes will overwrite the existing data. Do you want to continue?").is_visible():
                    page.get_by_role("button", name="Yes").click()
                    page.wait_for_timeout(4000)

                # Create Member Name
                page.get_by_role("button", name="New").click()
                page.wait_for_timeout(4000)
                # Member Type
                membertypecount = page.get_by_role("combobox", name="Member Type").count()
                print("Member Type Count-" + str(membertypecount))
                indexvalue = membertypecount - 1
                print("Index Value-" + str(indexvalue))
                page.get_by_role("combobox", name="Member Type").nth(indexvalue).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MMBR_TYPE"], exact=True).click()
                page.wait_for_timeout(2000)
                # Member Name - Based on Member Type
                if membertypecount == 1 or 2:
                    page.get_by_role("cell", name="Member Type Name Search and").locator("a").nth(membertypecount).click()
                    page.wait_for_timeout(2000)
                if membertypecount > 2:
                    page.get_by_role("cell", name="Member Type Name Search and").locator("a").nth(indexvalue).click()
                    #page.get_by_role("row", name=f"{membertypecount} Member Type Rule Search and select").locator("a").nth(1).click()
                    page.wait_for_timeout(2000)
                page.get_by_role("link", name="Search...").click()
                page.wait_for_timeout(3000)
                page.locator("//td//div[contains(text(),'Search and Select:')]//following::input[@aria-label=' Name']").click()
                page.wait_for_timeout(5000)
                page.locator("//td//div[contains(text(),'Search and Select:')]//following::input[@aria-label=' Name']").type(datadictvalue["C_MMBR_NAME"])
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Search", exact=True).click()
                page.wait_for_timeout(3000)
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MMBR_NAME"]).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(5000)
                # Time Category Condition
                if datadictvalue["C_TIME_CTGRY_CNDTN"] != "N/A":
                    page.wait_for_timeout(2000)
                    page.get_by_role("cell", name="Time Category Condition Search and Select: Autocompletes on TAB", exact=True).locator("a").first.click()
                    page.get_by_role("link", name="Search...").click()
                    page.wait_for_timeout(2000)
                    page.locator("//div[text()='Search and Select: Time Category Condition']//following::input[@aria-label=' Name']").click()
                    page.locator("//div[text()='Search and Select: Time Category Condition']//following::input[@aria-label=' Name']").type(datadictvalue["C_TIME_CTGRY_CNDTN"])
                    page.wait_for_timeout(1000)
                    page.get_by_role("button", name="Search", exact=True).click()
                    page.wait_for_timeout(3000)
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TIME_CTGRY_CNDTN"]).click()
                    page.wait_for_timeout(1000)
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(5000)

            # Save and Close
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)
            if page.get_by_role("button", name="OK").is_visible():
                page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(5000)

        # Create new Rule Set - If Rule Set is not Visible
        else:
            # Create Rule Set
            page.get_by_role("button", name="Create Rule Set").click()
            page.wait_for_timeout(2000)
            page.locator("//div[text()='Create Rule Set']//following::label[text()='Name']//following::input").first.click()
            page.locator("//div[text()='Create Rule Set']//following::label[text()='Name']//following::input").first.fill(datadictvalue["C_NAME"])
            page.wait_for_timeout(2000)

            # Rule Set Type
            page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Rule Set Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RULE_SET_TYPE"]).click()
            page.wait_for_timeout(2000)

            # Effective Start Date
            page.locator("//div[text()='Create Rule Set']//following::label[text()='Effective Start Date']//following::input").first.click()
            page.locator("//div[text()='Create Rule Set']//following::label[text()='Effective Start Date']//following::input").first.fill("")
            page.locator("//div[text()='Create Rule Set']//following::label[text()='Effective Start Date']//following::input").first.type(datadictvalue["C_EFFCTV_START_DATE"])
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_timeout(2000)

            # Create Member Name
            page.wait_for_timeout(4000)
            page.get_by_role("button", name="New").click()
            page.wait_for_timeout(4000)
            # Description
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill("")
            page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(3000)
            # Member Type
            page.get_by_role("combobox", name="Member Type").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MMBR_TYPE"], exact=True).click()
            page.wait_for_timeout(2000)
            # Member Name - Select based on Member Type
            if datadictvalue["C_MMBR_TYPE"] == "Rule":
                page.get_by_title("Search and Select: ").first.click()
                page.wait_for_timeout(2000)
            if datadictvalue["C_MMBR_TYPE"] == "Rule set":
                page.get_by_title("Search and Select: ").nth(1).click()
                page.wait_for_timeout(2000)
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.locator("//div[contains(text(),'Search and Select:')]//following::input[@aria-label=' Name']").click()
            page.locator("//div[contains(text(),'Search and Select:')]//following::input[@aria-label=' Name']").type(datadictvalue["C_MMBR_NAME"])
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MMBR_NAME"]).click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(5000)
            # Time Category Condition
            if datadictvalue["C_TIME_CTGRY_CNDTN"] != "N/A":
                page.get_by_role("cell", name="Time Category Condition Search and Select: Autocompletes on TAB", exact=True).locator("a").click()
                page.get_by_role("link", name="Search...").click()
                page.wait_for_timeout(2000)
                page.locator("//div[text()='Search and Select: Time Category Condition']//following::input[@aria-label=' Name']").click()
                page.locator("//div[text()='Search and Select: Time Category Condition']//following::input[@aria-label=' Name']").type(datadictvalue["C_TIME_CTGRY_CNDTN"])
                page.wait_for_timeout(1000)
                page.get_by_role("button", name="Search", exact=True).click()
                page.wait_for_timeout(3000)
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TIME_CTGRY_CNDTN"]).click()
                page.wait_for_timeout(1000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(5000)

            # Save and Close
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)
            if page.get_by_role("button", name="OK").is_visible():
                page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)

        try:
            expect(page.get_by_role("heading", name="Rule Sets")).to_be_visible()
            print("Manage Time Repository Rule Saved Successfully")
            datadictvalue["RowStatus"] = "Added Manage Time Repository Rule"
        except Exception as e:
            print("Unable to save Manage Time Repository Rule")
            datadictvalue["RowStatus"] = "Unable to Add Manage Time Repository Rule"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, TIME_RULE_SETS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, TIME_RULE_SETS,
                             PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, TIME_RULE_SETS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[
            0] + "_" + TIME_RULE_SETS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
