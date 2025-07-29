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
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox").type("Payroll Definitions")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Payroll Definitions").first.click()
    page.wait_for_timeout(4000)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(4000)

        # US Legislative Data Group
        page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Legislative Data Group").click()
        page.get_by_text(datadictvalue["C_LGSLTV_DATA_GROUP"], exact=True).nth(1).click()
        page.locator("(//label[text()='Effective As-of Date']//following::input[1])[2]").click()
        page.locator("(//label[text()='Effective As-of Date']//following::input[1])[2]").fill("")
        page.locator("(//label[text()='Effective As-of Date']//following::input[1])[2]").type(datadictvalue["C_EFFCTV_DATE"])
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(4000)

        # Basic Details
        page.get_by_label("Name", exact=True).click()
        page.get_by_label("Name", exact=True).type(datadictvalue["C_NAME"])
        page.get_by_label("Reporting Name").click()
        page.get_by_label("Reporting Name").type(datadictvalue["C_RPRTNG_NAME"])
        page.wait_for_timeout(2000)
        page.get_by_label("Consolidation Group").click()
        page.get_by_label("Consolidation Group").type(datadictvalue["C_CNSLDTN_GROUP"])
        page.get_by_label("Consolidation Group").press("Enter")
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Period Type").click()
        page.get_by_text(datadictvalue["C_PRD_TYPE"], exact=True).click()

        if datadictvalue["C_LDGR"]!='':
            page.get_by_title("Search and Select: Ledger").click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//div[text()='Search and Select: Ledger']//following::label[text()='Name']//following::input[1]").clear()
            page.locator("//div[text()='Search and Select: Ledger']//following::label[text()='Name']//following::input[1]").type(datadictvalue["C_LDGR"])

            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LDGR"]).click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(1000)
        page.get_by_placeholder("mm-dd-yyyy").click()
        page.get_by_placeholder("mm-dd-yyyy").type(datadictvalue["C_FIRST_PRD_END_DATE"])
        page.wait_for_timeout(1000)
        page.get_by_label("Default Payment Method").click()
        page.get_by_label("Default Payment Method").type(datadictvalue["C_DFLT_PYMNT_MTHD"])
        page.get_by_label("Default Payment Method").press("Enter")
        page.wait_for_timeout(2000)


        # Calculation default Values
        if page.get_by_label("Expand Calculation Default").is_visible():
            page.get_by_label("Expand Calculation Default").click()
            page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Context Segment").click()
        page.get_by_text(datadictvalue["C_CNTXT_SGMNT"],exact=True).click()
        if datadictvalue["C_PRC_VALUE_ITRTV_PRTX_DDCTN"]!='N/A':
            page.get_by_label("Precision Value for Iterative").type(str(datadictvalue["C_PRC_VALUE_ITRTV_PRTX_DDCTN"]))
        if datadictvalue["C_FLSA_OVRTM_PRD_OVRRD"]!='N/A':
            page.get_by_label("FLSA Overtime Period Override").type(datadictvalue["C_FLSA_OVRTM_PRD_OVRRD"])
        if datadictvalue["C_PRMM_CLCLTN_RATE"]!='N/A':
            page.get_by_label("Premium Calculation Rate").type(datadictvalue["C_PRMM_CLCLTN_RATE"])
        if datadictvalue["C_USE_INFRMTN_HOURS_FROM"]!='N/A':
            page.get_by_label("Use Information Hours From").type(datadictvalue["C_USE_INFRMTN_HOURS_FROM"])
        if datadictvalue["C_THRSHLD_BASIS"]!='N/A':
            page.get_by_label("Threshold Basis").type(datadictvalue["C_THRSHLD_BASIS"])

        #Additional Info
        page.get_by_role("button", name="New").click()
        page.wait_for_timeout(2000)
        page.get_by_title("Search and Select: Organization Payment Method").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Organization Payment Method Name").click()
        page.get_by_label("Organization Payment Method Name").type(datadictvalue["C_ORGNZTN_PYMNT_MTHD"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ORGNZTN_PYMNT_MTHD"]).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(3000)

        #Offset Details
        page.get_by_label("Number of Years").clear()
        page.get_by_label("Number of Years").type(str(datadictvalue["C_NMBR_YEARS"]))
        page.wait_for_timeout(1000)

        page.get_by_role("cell", name="Planned Submission Date").get_by_label("Falls").clear()
        page.get_by_role("cell", name="Planned Submission Date").get_by_label("Falls").type(str(datadictvalue["C_PLNND_FALL"]))
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Cutoff Date").get_by_label("Falls").clear()
        page.get_by_role("cell", name="Cutoff Date").get_by_label("Falls").type(str(datadictvalue["C_CTFF_FALL"]))
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Payslip Availability Date").get_by_label("Falls").clear()
        page.get_by_role("cell", name="Payslip Availability Date").get_by_label("Falls").type(str(datadictvalue["C_PYSLP_FALL"]))
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Payroll Run Date").get_by_label("Falls").clear()
        page.get_by_role("cell", name="Payroll Run Date").get_by_label("Falls").type(str(datadictvalue["C_PYRLL_FALL"]))
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Date Earned").get_by_label("Falls").clear()
        page.get_by_role("cell", name="Date Earned").get_by_label("Falls").type(str(datadictvalue["C_DATE_ERND_FALL"]))
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Date Paid").get_by_label("Falls").clear()
        page.get_by_role("cell", name="Date Paid").get_by_label("Falls").type(str(datadictvalue["C_DATE_PAID_FALL"]))
        page.wait_for_timeout(1000)

        #Offset
        page.get_by_role("cell", name="Planned Submission Date").get_by_label("Offset").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLNND_OFFST"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Cutoff Date").get_by_label("Offset").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CTFF_OFFST"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Payslip Availability Date").get_by_label("Offset").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYSLP_OFFST"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Payroll Run Date").get_by_label("Offset").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYRLL_OFFST"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name=" Date Earned").get_by_label("Offset").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DATE_ERND_OFFST"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name=" Date Paid").get_by_label("Offset").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DATE_PAID_OFFST"]).click()
        page.wait_for_timeout(1000)

        #Base Date
        page.get_by_role("cell", name="Planned Submission Date").get_by_label("Base Date").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLNND_BASE_DATE"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Cutoff Date").get_by_label("Base Date").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CTFF_BASE_DATE"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Payslip Availability Date").get_by_label("Base Date").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYSLP_BASE_DATE"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Payroll Run Date").get_by_label("Base Date").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYRLL_BASE_DATE"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Date Earned").get_by_label("Base Date").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DATE_ERND_BASE_DATE"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("cell", name="Date Paid").get_by_label("Base Date").first.click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DATE_PAID_BASE_DATE"]).click()
        page.wait_for_timeout(1000)

        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(8000)
        page.get_by_role("heading", name="Create Payroll: Payroll Calendar").is_visible()
        print("Create Payroll: Payroll Calendar")
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(8000)
        page.get_by_role("heading", name="Create Payroll: Costing of Payroll").is_visible()
        print("Create Payroll: Costing of Payroll")
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(8000)
        page.get_by_role("heading", name="Create Payroll: Payroll Review").is_visible()
        print("Create Payroll: Payroll Review")
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Submit").click()
        print("Submitted")
        page.wait_for_timeout(20000)


        try:
            expect(page.get_by_role("heading", name="Payroll Definitions")).to_be_visible()
            print("Added Payroll Definitions Saved Successfully")
            datadictvalue["RowStatus"] = "Added Payroll Definitions"
        except Exception as e:
            print("Unable to save Payroll Definitions")
            datadictvalue["RowStatus"] = "Unable to Add Payroll Definitions"
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Added Payroll Definitions Successfully"
        i = i + 1



    OraSignOut(page, context, browser, videodir)
    return datadict

print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, PAYROLL_DEFINITIONS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, PAYROLL_DEFINITIONS, PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK, PAYROLL_DEFINITIONS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + PAYROLL_DEFINITIONS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + PAYROLL_DEFINITIONS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

