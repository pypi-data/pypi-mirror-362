from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Conversion Rate Types")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Conversion Rate Types", exact=True).click()
    # page.pause()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(4000)
        page.get_by_role("cell", name="Name", exact=True).nth(1).get_by_label("Name").click()
        page.get_by_role("cell", name="Name", exact=True).nth(1).get_by_label("Name").type(datadictvalue["C_NAME"])
        page.get_by_role("cell", name="Description", exact=True).nth(1).get_by_label("Description").click()
        page.get_by_role("cell", name="Description", exact=True).nth(1).get_by_label("Description").type(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(2000)


        if datadictvalue["C_ENFRC_INVRS_RLTNSHP"] == 'Yes':
            page.wait_for_timeout(2000)
            if not page.locator("//span[text()='Enforce Inverse Relationship']//following::label[contains(@id,'Label0')][1]").is_checked():
                page.locator("//span[text()='Enforce Inverse Relationship']//following::label[contains(@id,'Label0')][1]").click()
        #
        elif datadictvalue["C_ENFRC_INVRS_RLTNSHP"] == 'No':
            if page.locator("//span[text()='Enforce Inverse Relationship']//following::label[contains(@id,'Label0')][1]").is_checked():
                page.locator("//span[text()='Enforce Inverse Relationship']//following::label[contains(@id,'Label0')][1]").click()
        page.wait_for_timeout(2000)
        #
        if datadictvalue["C_ENBL_CROSS_RATES"] == 'Yes':
            page.wait_for_timeout(2000)
            if not page.locator("//span[text()='Enable Cross Rates']//following::label[contains(@id,'Label0')][2]").is_checked():
                page.locator("//span[text()='Enable Cross Rates']//following::label[contains(@id,'Label0')][2]").click()

        elif datadictvalue["C_ENBL_CROSS_RATES"] == 'No':
            if page.locator("//span[text()='Enable Cross Rates']//following::label[contains(@id,'Label0')][2]").is_checked():
                page.locator("//span[text()='Enable Cross Rates']//following::label[contains(@id,'Label0')][2]").click()
        page.wait_for_timeout(3000)


        if datadictvalue["C_ALLOW_CROSS_RATES_OVRRD"] == 'Yes':
            page.wait_for_timeout(2000)
            if not page.locator("//span[text()='Allow Cross Rates Override']//following::label[contains(@id,'Label0')][3]").is_checked():
                page.locator("//span[text()='Allow Cross Rates Override']//following::label[contains(@id,'Label0')][3]").click()
                page.locator("//span[text()='Cross Rate Pivot Currency']//following::select[1]").select_option("0")

        elif datadictvalue["C_ALLOW_CROSS_RATES_OVRRD"] == 'No':
            if page.locator("//span[text()='Allow Cross Rates Override']//following::label[contains(@id,'Label0')][3]").is_checked():
                page.locator("//span[text()='Allow Cross Rates Override']//following::label[contains(@id,'Label0')][3]").click()
                page.locator("//span[text()='Cross Rate Pivot Currency']//following::select[1]").select_option("0")
            page.wait_for_timeout(2000)

            if datadictvalue["C_DFLT_RATE_TYPE"] == 'Yes':
                page.get_by_label("Actions").locator("div").click()
                page.get_by_text("Change Default Rate Type").click()
        page.wait_for_timeout(2000)
        i = i + 1

    page.get_by_role("button", name="Save", exact=True).click()
    page.wait_for_timeout(4000)

    page.get_by_role("button", name="Save and Close").click()

    # Validation
    try:
        expect(page.get_by_role("heading", name="Search")).to_be_visible()
        print("Managed Conversion Rates Successfully")
        datadictvalue["RowStatus"] = "Conversion Rates Saved"
    except Exception as e:
        print("Managed Conversion Rates UnSuccessfully")
        datadictvalue["RowStatus"] = "Conversion Rates not Saved"

    print("Row Added - ", str(i))


    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, MANAGE_CONV_RATES_TYPES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, MANAGE_CONV_RATES_TYPES, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, MANAGE_CONV_RATES_TYPES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + MANAGE_CONV_RATES_TYPES)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[
                0] + "_" + MANAGE_CONV_RATES_TYPES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))