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
    page.get_by_role("button", name="Offering").click()
    page.get_by_text("Financials", exact=True).click()
    page.wait_for_timeout(2000)

    # Navigating to respective option in Legal Search field and searching
    page.get_by_text("Legal Structures").first.click()
    page.locator("//a[text()='Manage Legal Entity Registrations']//following::a[1]").click()
    page.wait_for_timeout(3000)
    page.get_by_label("Legal Entity", exact=True).select_option("Select and Add")
    page.get_by_role("button", name="Apply and Go to Task").click()
    page.get_by_label("Expand Search").click()
    page.wait_for_timeout(3000)

    # Looping the values based on excel rows
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        # Navigating to Manage Legal Entity Registrations page & Entering the data
        page.get_by_label("Name").fill(datadictvalue["C_LEGAL_ENTTY"])
        page.locator("//label[text()='Name']//following::button[text()='Search']").click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name=datadictvalue["C_LEGAL_ENTTY"], exact=True).click()
        page.get_by_role("button", name="Save and Close").click()
        page.get_by_role("button", name="Edit").click()
        page.get_by_label("Registered Name").clear()
        page.get_by_label("Registered Name").fill(datadictvalue["C_RGSTED_NAME"])
        if page.get_by_label("EIN or TIN").is_visible():
            page.get_by_label("EIN or TIN").clear()
            page.get_by_label("EIN or TIN").fill(datadictvalue["C_LEGAL_ENTTY_RGSTRTN_NMBR"])
        page.get_by_label("Alternate Name").fill(datadictvalue["C_ALTRNT_NAME"])
        page.get_by_label("Place of Registration").fill(datadictvalue["C_PLACE_OF_RGSTRTN"])
        page.get_by_label("Issuing Legal Authority").type(datadictvalue["C_ISSNG_LEGAL_ATHRTY"])
        page.locator("//label[text()='Start Date']//following::input[1]").nth(0).fill(datadictvalue["C_START_DATE"])
        page.locator("//label[text()='End Date']//following::input[1]").nth(0).fill(datadictvalue["C_END_DATE"])

        # Saving and closing the record
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)


        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Setup: Financials")).to_be_visible()
            print("Legal entity registration completed successfully")
            datadictvalue["RowStatus"] = "Successfully Added Legal Entity Registration"

        except Exception as e:
            print("Unable to save the Legal entity Registration")
            datadictvalue["RowStatus"] = "Unable to save the Legal entity Registration"

    # Signout from the application
    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, LEGAL_ENTITY_REG):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, LEGAL_ENTITY_REG, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, LEGAL_ENTITY_REG)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + LEGAL_ENTITY_REG)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + LEGAL_ENTITY_REG + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))