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
    page.wait_for_timeout(20000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Salary Basis")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Salary Basis", exact=True).first.click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Name").type(datadictvalue["C_NAME"])
        page.get_by_label("Code").clear()
        page.get_by_label("Code").type(datadictvalue["C_CODE"])
        page.get_by_role("combobox", name="Salary Basis Type").click()
        page.wait_for_timeout(2000)
        page.get_by_text(datadictvalue["C_SLRY_BASIS_TYPE"]).click()
        page.get_by_role("combobox", name="Frequency").click()
        page.get_by_text(datadictvalue["C_FRQNCY"], exact=True).click()
        page.get_by_label("Legislative Data Group").type(datadictvalue["C_LGSLTV_DATA_GROUP"])
        page.get_by_label("Annualization Factor").clear()
        page.get_by_label("Annualization Factor").type(str(datadictvalue["C_ANNLZTN_FCTR"]))
        page.get_by_title("Search and Select: Payroll").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("textbox", name="Payroll Element").type(datadictvalue["C_PYRLL_ELMNT"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYRLL_ELMNT"], exact=True).click()
        page.get_by_role("button",name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Input Value").click()
        page.get_by_label("Input Value").type(datadictvalue["C_INPUT_VALUE"])
        page.get_by_role("link", name="Salary Ranges").click()
        page.wait_for_timeout(3000)
        page.get_by_label("Grade Rate", exact=True).type(datadictvalue["C_A_GRADE_RATE"])
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        try:
            expect(page.get_by_role("heading", name="Salary Basis")).to_be_visible()
            print("Salary Basis Saved Successfully")
            datadictvalue["RowStatus"] = "Salary Basis Saved"
        except Exception as e:
            print("Unable to Save Salary Basis")
            datadictvalue["RowStatus"] = "Unable to Save Salary Basis"

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Salary Basis Added Successfully"
        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, SALARY_BASIS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, SALARY_BASIS, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, SALARY_BASIS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0]+ "_" + SALARY_BASIS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + SALARY_BASIS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))