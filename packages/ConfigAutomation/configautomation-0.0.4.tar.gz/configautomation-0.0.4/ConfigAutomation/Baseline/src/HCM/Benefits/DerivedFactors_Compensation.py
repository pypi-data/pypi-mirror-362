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

    # Navigate to Derived Factors page
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Benefits Administration", exact=True).click()
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Derived Factors").click()
    page.get_by_role("link", name="Compensation", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(3000)
        # Entering Name
        #page.pause()
        # page.get_by_role("row", name="*Name", exact=True).get_by_label("Name").type(datadictvalue["C_NAME"])
        page.locator(
            "//div[text()='Create Derived Factor Compensation']//following::label[text()='Name']//following::input[1]").type(datadictvalue["C_NAME"])
        page.wait_for_timeout(2000)
        # Selecting Units of Measure
        if datadictvalue["C_UNIT_MSR"] != "":
            # page.get_by_role("row", name="*Unit of Measure", exact=True).get_by_role("combobox").click()
            # page.wait_for_timeout(2000)
            # page.get_by_role("listbox").get_by_text(datadictvalue["C_UNIT_MSR"], exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Unit of Measure").click()
            page.wait_for_timeout(2000)
            page.get_by_role("listbox").get_by_text(datadictvalue["C_UNIT_MSR"], exact=True).click()



        # Selecting Source
        if datadictvalue["C_SRC"] != "":
            page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Source").click()
            page.wait_for_timeout(2000)
            page.get_by_role("listbox").get_by_text(datadictvalue["C_SRC"], exact=True).click()
            page.wait_for_timeout(3000)

        # Selecting Stated Salary
        if datadictvalue["C_STATED_SALARY"] != "":
            page.get_by_role("combobox", name="Stated Salary").click()
            page.wait_for_timeout(2000)
            page.get_by_role("listbox").get_by_text(datadictvalue["C_STATED_SALARY"], exact=True).click()

        # Entering Greater than or Equal to Compensation
        if datadictvalue["C_GRTR_THAN_OR_EQUAL_CMPNSTN"] != "":
            page.get_by_label("Greater than or Equal to Compensation").clear()
            page.get_by_label("Greater than or Equal to Compensation").type(str(datadictvalue["C_GRTR_THAN_OR_EQUAL_CMPNSTN"]))

        # Entering Less Than Compensation
        if datadictvalue["C_LESS_THAN_CMPNSTN"] != "":
            page.get_by_label("Less Than Compensation").clear()
            page.get_by_label("Less Than Compensation").type(str(datadictvalue["C_LESS_THAN_CMPNSTN"]))

        # Selecting Determination RuleDerived Factor Compensation Created Successfully
        # Derived Factor Compensation Created Successfully
        if datadictvalue["C_DTRMNTN_RULE"] != "":
            page.get_by_role("combobox", name="Determination Rule").click()
            page.wait_for_timeout(2000)
            page.get_by_role("listbox").get_by_text(datadictvalue["C_DTRMNTN_RULE"], exact=True).click()

        # Selecting Rounding Rule
        if datadictvalue["C_RNDNG_RULE"] != "":
            page.get_by_role("combobox", name="Rounding Rule").click()
            page.wait_for_timeout(2000)
            page.get_by_role("listbox").get_by_text(datadictvalue["C_RNDNG_RULE"], exact=True).click()

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("heading", name="Derived Factors")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Derived Factor Compensation Created Successfully")
            datadictvalue["RowStatus"] = "Derived Factor Compensation Created Successfully"
        except Exception as e:
            print("Unable to Create Derived Factor Compensation")
            datadictvalue["RowStatus"] = "Unable to Save Derived Factor Compensation"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, DERIVEDFACTORS_COMPENSATION):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, DERIVEDFACTORS_COMPENSATION,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, DERIVEDFACTORS_COMPENSATION)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + DERIVEDFACTORS_COMPENSATION)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + DERIVEDFACTORS_COMPENSATION + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


