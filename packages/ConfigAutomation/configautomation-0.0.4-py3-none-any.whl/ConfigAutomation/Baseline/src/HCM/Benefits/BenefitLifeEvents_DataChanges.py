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

    # Navigate to BenefitLifeEvents-DataChnages page
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Benefits Administration", exact=True).click()
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Benefit Life Events").click()
    page.get_by_role("link", name="Data Changes").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(3000)
        print(datadictvalue["C_NAME"])
        page.locator("//div[text()='Create Person Change']//following::input[1]").click()
        page.locator("//div[text()='Create Person Change']//following::input[1]").type(datadictvalue["C_NAME"])
        #page.get_by_role("cell", name="Create Person Change *Name *").get_by_label("Name", exact=True).click()
        #page.get_by_role("cell", name="Create Person Change *Name *").get_by_label("Name", exact=True).type(datadictvalue["C_NAME"])
        page.get_by_role("combobox", name="Table Name").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TABLE_NAME"]).click()
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Column Name").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CLMN_NAME"], exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Old Value").click()
        page.get_by_role("listbox").get_by_text(datadictvalue["C_OLD_VALUE"], exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="New Value").click()
        page.get_by_role("listbox").get_by_text(datadictvalue["C_NEW_VALUE"], exact=True).click()
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        try:
            expect(page.get_by_role("heading", name="Search Results")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Life Event Data Changed Successfully")
            datadictvalue["RowStatus"] = "Data Changed Successfully"
        except Exception as e:
            print("Unable to Save Life Event Data Changes")
            datadictvalue["RowStatus"] = "Unable to Save Life Event Data Changes"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, LIFEEVENTS_DATACHANGES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, LIFEEVENTS_DATACHANGES,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, LIFEEVENTS_DATACHANGES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + LIFEEVENTS_DATACHANGES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[
            0] + "_" + LIFEEVENTS_DATACHANGES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

