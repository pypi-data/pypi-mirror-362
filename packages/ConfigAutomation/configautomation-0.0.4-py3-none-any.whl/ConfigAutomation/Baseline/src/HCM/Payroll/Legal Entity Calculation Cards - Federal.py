from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.get_by_role("link", name="Manage Implementation Projects").click()
    page.get_by_label("Name").click()
    page.get_by_label("Name").type("HCM Implementation Project")
    page.get_by_role("button", name="Search", exact=True).click()
    page.wait_for_timeout(2000)
    # page.get_by_role("button", name="Done").click()
    page.get_by_role("cell", name="HCM Implementation Project", exact=True).click()
    page.get_by_role("button", name="Edit").click()
    page.wait_for_timeout(4000)
    page.get_by_role("cell", name="Expand Task ListWorkforce Deployment", exact=True).get_by_role("link").click()
    page.wait_for_timeout(1000)
    page.get_by_role("cell", name="Expand Task List*Define Common Applications Configuration for Human Capital Management", exact=True).get_by_role("link").click()
    page.wait_for_timeout(1000)
    page.get_by_role("cell", name="Expand Task List*Define Enterprise Structures for Human Capital Management", exact=True).get_by_role("link").click()
    page.wait_for_timeout(1000)
    page.get_by_role("cell", name="Expand Iterative Task List*Define Legal Entities for Human Capital Management", exact=True).get_by_role("link").click()
    page.wait_for_timeout(1000)
    page.locator("//span[text()='Legal Entity Calculation Cards']//following::a[@title='Go to Task']").first.click()
    page.wait_for_timeout(7000)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        page.get_by_placeholder("m/d/yy").nth(1).click()
        page.get_by_placeholder("m/d/yy").nth(1).fill("")
        page.get_by_placeholder("m/d/yy").nth(1).type(datadictvalue["C_EFFCTV_DATE"])
        page.get_by_label("Name", exact=True).click()
        page.get_by_label("Name", exact=True).type(datadictvalue["C_NAME"])
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(15000)
        page.get_by_role("link", name="Federal").click()
        page.wait_for_timeout(10000)

        #Federal Income Tax
        page.get_by_role("cell", name="Federal Income Tax", exact=True).click()
        page.wait_for_timeout(5000)
        page.get_by_role("cell", name="Expand").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Supplemental Tax Calculation").click()
        page.get_by_label("Supplemental Tax Calculation").type(datadictvalue["C_SPPLMNTL_TAX"])
        page.get_by_label("Supplemental Tax Calculation").press("Tab")
        page.get_by_label("Tax Withholding Rules").click()
        page.get_by_label("Tax Withholding Rules").type(datadictvalue["C_TAX_WTHHLDNG_RULE"])
        page.get_by_label("Tax Withholding Rules").press("Tab")
        page.get_by_label("Enable Period-to-Date Tax").click()
        page.get_by_label("Enable Period-to-Date Tax").type(datadictvalue["C_ENBL_PROD_DATE_TAX"])
        page.get_by_label("Enable Period-to-Date Tax").press("Tab")
        page.wait_for_timeout(2000)
        if datadictvalue["C_FIT_DSPLY_VALUE"] != "":
            page.get_by_role("link", name="Enterable Calculation Values").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Create").nth(2).click()
            page.get_by_label("Display Value").click()
            page.get_by_label("Display Value").type(datadictvalue["C_FIT_DSPLY_VALUE"])
            page.get_by_label("Display Value").press("Tab")
            page.get_by_role("combobox", name="Value", exact=True).click()
            page.get_by_text(datadictvalue["C_FIT_VALUE_TYPE"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        #Medicare
        page.get_by_role("cell", name="Medicare", exact=True).click()
        page.wait_for_timeout(5000)
        page.get_by_role("cell", name="Expand").click()
        page.wait_for_timeout(2000)
        page.get_by_title("Search: Self Adjustment Method").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Value").click()
        page.get_by_label("Value").type(datadictvalue["C_MDCR_SELF_ADJSTMNT"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MDCR_SELF_ADJSTMNT"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        # Federal Unemployment
        page.get_by_role("cell", name="Federal Unemployment", exact=True).click()
        page.wait_for_timeout(5000)
        page.get_by_role("cell", name="Expand").click()
        page.wait_for_timeout(2000)
        page.get_by_title("Search: Employer Self Adjustment Method").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Value").click()
        page.get_by_label("Value").type(datadictvalue["C_FU_EMPLYR_SELF_ADJSTMNT"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FU_EMPLYR_SELF_ADJSTMNT"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        #Social Security
        page.get_by_role("cell", name="Social Security", exact=True).click()
        page.wait_for_timeout(5000)
        page.get_by_role("cell", name="Expand").click()
        page.wait_for_timeout(2000)
        page.get_by_title("Search: Self Adjustment Method").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Value").click()
        page.get_by_label("Value").type(datadictvalue["C_SCL_SCRTY_SELF_ADJSTMNT"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SCL_SCRTY_SELF_ADJSTMNT"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(4000)
        # page.get_by_role("button", name="Save", exact=True).click()
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)
        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Payroll Statutory Unit")).to_be_visible()
            print("Added Legal Entity Calculation Federal Saved Successfully")
            datadictvalue["RowStatus"] = "Added Legal Entity Calculation Federal"
        except Exception as e:
            print("Unable to save Legal Entity Calculation Federal")
            datadictvalue["RowStatus"] = "Unable to Add Legal Entity Calculation Federal"

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, LEGAL_ENTITY_CALCULATION_FEDERA):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, LEGAL_ENTITY_CALCULATION_FEDERA, PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK, LEGAL_ENTITY_CALCULATION_FEDERA)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + LEGAL_ENTITY_CALCULATION_FEDERA)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + LEGAL_ENTITY_CALCULATION_FEDERA + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
