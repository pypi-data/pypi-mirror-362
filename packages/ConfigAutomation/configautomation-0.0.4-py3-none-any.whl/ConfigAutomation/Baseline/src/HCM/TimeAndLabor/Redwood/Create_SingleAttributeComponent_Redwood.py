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
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(20000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Time Entry Layout Components")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Time Entry Layout Components", exact=True).click()
    page.wait_for_timeout(2000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        # Selecting Single Attribute Time Card
        page.locator("[id=\"__af_Z_window\"]").get_by_text("Single attribute time card").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # Name
        page.get_by_label("Name", exact=True).clear()
        page.get_by_label("Name", exact=True).type(str(datadictvalue["C_NAME"]))
        page.wait_for_timeout(1000)

        # Description
        page.get_by_label("Description").clear()
        page.get_by_label("Description").type(str(datadictvalue["C_DSCRPTN"]))
        page.wait_for_timeout(1000)

        # Selecting Time Attribute
        page.get_by_label("Time Attribute").click()
        page.get_by_label("Time Attribute").fill(datadictvalue["C_TIME_ATTRBT"])
        page.get_by_label("Time Attribute").press("Tab")
        page.wait_for_timeout(3000)

        # Filtered Data Source for Time Entry
        page.get_by_label("Filtered Data Source for Time Entry").click()
        page.get_by_title("Search and Select: Filtered Data Source for Time Entry").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(3000)
        page.locator("//div[text()='Search and Select: Filtered Data Source for Time Entry']//following::input[@aria-label=' Name']").click()
        page.locator("//div[text()='Search and Select: Filtered Data Source for Time Entry']//following::input[@aria-label=' Name']").fill(datadictvalue["C_FLTRD_DATA_SRC_FOR_TIME_ENTRY"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name=datadictvalue["C_FLTRD_DATA_SRC_FOR_TIME_ENTRY"], exact=True).click()
        # page.get_by_role("cell", name=datadictvalue["C_FLTRD_DATA_SURCE_FOR_TIME_ENTRY"], exact=True).locator("span").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # Add Filters
        if datadictvalue["C_FLTER_VRBL_PRN"] != '' or "N/A":
            page.get_by_role("button", name="Add Filters").click()

        # Adding Filter 1
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="TclayfldAttributeChar10").click()
            page.get_by_role("listbox").get_by_text(datadictvalue["C_FLTER_VRBL_PRN"], exact=True).click()
            page.get_by_title("Filter Input Attribute").first.click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//div[text()='Search and Select: Time Attributes']//following::input[@aria-label=' Name']").click()
            page.locator("//div[text()='Search and Select: Time Attributes']//following::input[@aria-label=' Name']").fill(datadictvalue["C_FLTR_INPUT_ATTRBT_PRN"])
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.locator("(//span[text()='"+datadictvalue["C_FLTR_INPUT_ATTRBT_PRN"]+"'])[2]").click()
            page.get_by_role("button", name="OK").nth(1).click()
            page.wait_for_timeout(3000)

        # Adding Filter 2
            page.get_by_role("combobox", name="TclayfldAttributeChar11").click()
            page.get_by_role("listbox").get_by_text(datadictvalue["C_FLTR_VRBL_STRT_DATE"], exact=True).click()
            page.get_by_title("Filter Input Attribute").nth(1).click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.locator("//div[text()='Search and Select: Time Attributes']//following::input[@aria-label=' Name']").click()
            page.locator("//div[text()='Search and Select: Time Attributes']//following::input[@aria-label=' Name']").fill(datadictvalue["C_FLTR_INPUT_ATTRBT_START_TIME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.locator("//span[text()='" + datadictvalue["C_FLTR_INPUT_ATTRBT_START_TIME"] + "']").click()
            page.get_by_role("button", name="OK").nth(1).click()

        # Adding Filter 3
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="TclayfldAttributeChar12").click()
            page.get_by_role("listbox").get_by_text(datadictvalue["C_FLTR_VRBL_STOP_DATE"], exact=True).click()
            page.get_by_title("Filter Input Attribute").nth(2).click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.locator("//div[text()='Search and Select: Time Attributes']//following::input[@aria-label=' Name']").click()
            page.locator("//div[text()='Search and Select: Time Attributes']//following::input[@aria-label=' Name']").fill(datadictvalue["C_FLTR_INPUT_ATTRBT_STOP_TIME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.locator("//span[text()='" + datadictvalue["C_FLTR_INPUT_ATTRBT_STOP_TIME"] + "']").click()
            page.get_by_role("button", name="OK").nth(1).click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="OK").first.click()

        # UnFiltered Data Source for Time Entry
        page.get_by_label("Unfiltered Data Source for Setup Tasks").click()
        page.get_by_title("Search and Select: Unfiltered Data Source for Setup Tasks").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(3000)
        page.locator("//div[text()='Search and Select: Unfiltered Data Source for Setup Tasks']//following::input[@aria-label=' Name']").click()
        page.locator("//div[text()='Search and Select: Unfiltered Data Source for Setup Tasks']//following::input[@aria-label=' Name']").fill(datadictvalue["C_UNFLTRD_DATA_SRC_FOR_SETUP_TASKS"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_UNFLTRD_DATA_SRC_FOR_SETUP_TASKS"]).click()
        # page.get_by_role("cell", name=datadictvalue["C_UNFLTRD_DATA_SRC_FOR_SETUP_TASKS"], exact=True).locator("span").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # Default Values - Population method for New Entry
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Population Method for New").click()
        page.get_by_text(datadictvalue["C_PPLTN_MTHD_FOR_NEW_ENTRY"]).click()

        # Function
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Function").click()
        page.wait_for_timeout(2000)
        page.get_by_text("Based on primary assignment").click()

        # Display Properties
        # Display Type
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Display Type").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSPLY_TYPE"]).click()

        # Display Name
        page.wait_for_timeout(3000)
        page.get_by_label("Display Name").clear()
        page.get_by_label("Display Name").type(datadictvalue["C_DSPLY_NAME"])
        page.wait_for_timeout(2000)

        # Enable override on layouts
        if datadictvalue["C_ENBLE_OVRRD_ON_LYTS"] == "Yes":
            page.get_by_text("Enable override on layouts").check()
        if datadictvalue["C_ENBLE_OVRRD_ON_LYTS"] == "No":
            page.get_by_text("Enable override on layouts").uncheck()

        # Required on the Time Card
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Required on the Time Card").click()
        page.get_by_text(datadictvalue["C_RQRD_ON_THE_TIME_CARD"]).click()
        page.wait_for_timeout(3000)

        # Clicking on Next button
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        try:
            expect(page.get_by_role("heading", name="Time Entry Layout Components")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Time Entry - Single Attribute Component Created Successfully")
            datadictvalue["RowStatus"] = "Created Time Entry - Single Attribute Component Successfully"
        except Exception as e:
            print("Unable to Save Time Entry - Single Attribute Component")
            datadictvalue["RowStatus"] = "Unable to Save Time Entry - Single Attribute Component"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, SINGLE_ATTRIBUTE_COMPONENTS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, SINGLE_ATTRIBUTE_COMPONENTS, PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, SINGLE_ATTRIBUTE_COMPONENTS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0])
        write_status(output,
                     RESULTS_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0] + "_Results_" + datetime.now().strftime(
                         "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
