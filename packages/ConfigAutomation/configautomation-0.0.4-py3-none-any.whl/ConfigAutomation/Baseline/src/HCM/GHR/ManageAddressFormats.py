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

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Address Formats")
    page.get_by_role("textbox").press("Enter")

    # Navigating to Manage Address Formats page & Entering the data
    page.get_by_role("link", name="Manage Address Formats", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("combobox", name="Country").click()
    page.get_by_text("United States", exact=True).click()
    page.get_by_role("button", name="Search", exact=True).click()
    page.get_by_role("link", name="United States Postal Address").click()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Edit").click()


    # Looping the values based on excel rows
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        # Entering the Values for Formatting Layout
        page.get_by_label("Line").nth(i).clear()
        page.get_by_label("Line").nth(i).type(str(datadictvalue["C_LINE"]))
        page.get_by_label("Position").nth(i).clear()
        page.get_by_label("Position").nth(i).type(str(datadictvalue["C_PSTN"]))

        if datadictvalue["C_RQRD"] == 'x':
            if datadictvalue["C_ADDRSS_ELMNT"] == 'Address Line 1':
                page.get_by_role("row", name=datadictvalue["C_ADDRSS_ELMNT"]).locator("label").nth(3).check()

            if datadictvalue["C_ADDRSS_ELMNT"] == 'Address Line 2':
                page.get_by_role("row", name="Expand Line Position Prompt Address line 2").locator("label").nth(3).check()

            if datadictvalue["C_ADDRSS_ELMNT"] == 'City':
                page.get_by_role("row", name=datadictvalue["C_ADDRSS_ELMNT"]).locator("label").nth(3).check()

            if datadictvalue["C_ADDRSS_ELMNT"] == 'State':
                page.locator("//span[text()='" + datadictvalue["C_ADDRSS_ELMNT"] + "']//following::label[1]").check()
                page.wait_for_timeout(5000)

            if datadictvalue["C_ADDRSS_ELMNT"] == 'Postal code':
                page.locator("//span[text()='" + datadictvalue["C_ADDRSS_ELMNT"] + "']//following::label[1]").check()

            if datadictvalue["C_ADDRSS_ELMNT"] == 'County':
                page.locator("//input[@title='" + datadictvalue["C_ADDRSS_ELMNT"] + "']//following::label[2]").check()

            if datadictvalue["C_ADDRSS_ELMNT"] == 'Country':
                page.get_by_role("row", name=datadictvalue["C_ADDRSS_ELMNT"]).locator("label").nth(3).check()

        print("Row Added - ", str(i))
        i = i + 1
    page.get_by_role("button", name="Save and Close").click()
    try:
        expect(page.get_by_role("heading", name="Manage Address Formats")).to_be_visible()
        print("Manage Address Format Saved Successfully")
        datadictvalue["RowStatus"] = "Manage Address Format Saved"
    except Exception as e:
        print("Unable to save Manage Address Format")
        datadictvalue["RowStatus"] = "Unable to save Manage Address Format"

    # Signout from the application
    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_ADDRESS_FORMATS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_ADDRESS_FORMATS, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_ADDRESS_FORMATS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0]+ "_" + MANAGE_ADDRESS_FORMATS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + MANAGE_ADDRESS_FORMATS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

