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
    page.wait_for_timeout(5000)

    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Checklist Templates")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Checklist Templates", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)

        # Name
        page.get_by_label("Name", exact=True).clear()
        page.get_by_label("Name", exact=True).type(datadictvalue["C_OB_NAME"])

        # Checklist Code
        page.get_by_label("Checklist Code").click()
        page.wait_for_timeout(3000)
        page.get_by_label("Checklist Code").clear()
        page.get_by_label("Checklist Code").type(datadictvalue["C_OB_CHCKLST_CODE"])

        # Country
        page.get_by_label("Country").clear()
        page.get_by_label("Country").type(datadictvalue["C_OB_CNTRY"])

        # Category
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Category").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OB_CTGRY"]).click()

        # Clicking on Ok Button
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(5000)

        # Action Name
        page.get_by_role("combobox", name="Status").click()
        page.get_by_text("Active", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_title("Search: Action Name").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Action Name").type(datadictvalue["C_OB_ACTN_NAME"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.locator("(//span[text()='Action Name']//following::span[text()='"+datadictvalue["C_OB_ACTN_NAME"]+"'])[1]").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        # Saving and closing the Record
        page.get_by_role("button", name="Save and Close").click()

        page.wait_for_timeout(3000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Checklist Templates")).to_be_visible()
            print("Checklists for Preboarding & Onboarding Saved Successfully")
            datadictvalue["RowStatus"] = "Checklists for Preboarding & Onboarding Saved Successfully"
        except Exception as e:
            print("Checklists for Preboarding & Onboardings not saved")
            datadictvalue["RowStatus"] = "Checklists for Preboarding & Onboarding not added"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + ONBOARDING_CONFIG_WRKBK, CHECKLIST_STEP):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + ONBOARDING_CONFIG_WRKBK, CHECKLIST_STEP,PRCS_DIR_PATH + ONBOARDING_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + ONBOARDING_CONFIG_WRKBK, CHECKLIST_STEP)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", ONBOARDING_CONFIG_WRKBK)[0] + "_" + CHECKLIST_STEP)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", ONBOARDING_CONFIG_WRKBK)[0] + "_" + CHECKLIST_STEP + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




