from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)

    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    # Navigate to Derived Factors page
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Benefits Administration", exact=True).click()
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Derived Factors").click()
    page.get_by_role("link", name="Age", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(3000)
        # Entering Name
        page.locator("//h1 [text()='Definition']//following::input[1]").type(datadictvalue["C_NAME"])
        # Selecting Units
        if datadictvalue["C_UNITS"]!="":
            page.get_by_role("combobox", name="Units").click()
            page.wait_for_timeout(2000)
            page.get_by_role("listbox").get_by_text(datadictvalue["C_UNITS"], exact=True).click()
            page.wait_for_timeout(2000)
        # Selecting Age to Use
        if datadictvalue["C_AGE_TO_USE"]!="":
            page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Age to Use").click()
            # page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_AGE_TO_USE"], exact=True).click()

        # Selecting Calculation Formula
        if datadictvalue["C_CLCLTN_FRML"]!="":
            page.get_by_role("combobox", name="Calculation Formula").click()
            page.wait_for_timeout(2000)
            page.get_by_role("listbox").get_by_text(datadictvalue["C_CLCLTN_FRML"], exact=True).click()

        # Entering Greater than or Equal to Age
        if datadictvalue["C_GRTR_THAN_OR_EQUAL_TO_AGE"]!="":
            page.get_by_label("Greater than or Equal to Age").clear()
            page.get_by_label("Greater than or Equal to Age").type(str(datadictvalue["C_GRTR_THAN_OR_EQUAL_TO_AGE"]))

        # Entering Less Than Age
        if datadictvalue["C_LESS_THAN_AGE"] != "":
            page.get_by_label("Less Than Age").clear()
            page.get_by_label("Less Than Age").type(str(datadictvalue["C_LESS_THAN_AGE"]))

        # Selecting Determination Rule
        if datadictvalue["C_DTRMNTN_RULE"] != "":
            page.get_by_role("combobox", name="Determination Rule").click()
            page.wait_for_timeout(2000)
            #page.get_by_role("listbox").get_by_text(datadictvalue["C_DTRMNTN_RULE"], exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DTRMNTN_RULE"], exact=True).click()

        # Selecting Rounding Rule
        if datadictvalue["C_RNDNG_RULE"] != "":
            page.get_by_role("combobox", name="Rounding Rule").click()
            page.wait_for_timeout(2000)
            page.get_by_role("listbox").get_by_text(datadictvalue["C_RNDNG_RULE"], exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        # context.tracing.stop(path="trace.zip")
        try:
            expect(page.get_by_role("heading", name="Derived Factors")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Derived Factor Age Created Successfully")
            datadictvalue["RowStatus"] = "Derived Factor Age Created Successfully"
        except Exception as e:
            print("Unable to Create Derived Factor Age")
            datadictvalue["RowStatus"] = "Unable to Save Derived Factor Age"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, DERIVEDFACTORS_AGE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, DERIVEDFACTORS_AGE,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, DERIVEDFACTORS_AGE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + DERIVEDFACTORS_AGE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + DERIVEDFACTORS_AGE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


