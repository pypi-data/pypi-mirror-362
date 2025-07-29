from playwright.sync_api import Playwright, sync_playwright
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    # Navigate to Document Upload page
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Benefits Administration", exact=True).click()
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Programs and Plans").click()
    page.get_by_role("link", name="Programs", exact=True).click()

    i = 0
    while i < rowcount:

        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        if i == 0:
            # Enter Program Name
            page.get_by_label("Program Name").clear()
            page.get_by_label("Program Name").type(datadictvalue["C_PRGRM_NAME"])

            # Enter Effective As-of Date
            page.get_by_placeholder("mm-dd-yyyy").clear()
            page.get_by_placeholder("mm-dd-yyyy").type(datadictvalue["C_EFFCTV_START_DATE"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(5000)

            # Clicking on Respective Program
            page.get_by_role("link", name=datadictvalue["C_PRGRM_NAME"]).click()
            page.wait_for_timeout(5000)

            # Clicking on Document Upload hyperlink in Program page
            page.get_by_label("Document Uploads Step: Not").click()
            page.wait_for_timeout(5000)
            page.get_by_placeholder("mm-dd-yyyy").clear()
            page.get_by_placeholder("mm-dd-yyyy").type(datadictvalue["C_EFFCTV_START_DATE"])
            page.wait_for_timeout(3000)

        if i>=0:

            page.get_by_role("button", name="Select and Add", exact=True).click()
            page.wait_for_timeout(3000)

            # Start Date
            page.locator("//label[text()='Start Date']//following::input[1]").clear()
            page.locator("//label[text()='Start Date']//following::input[1]").type(datadictvalue["C_START_DATE"])

            # End Date
            page.locator("//label[text()='End Date']//following::input[1]").clear()
            page.locator("//label[text()='End Date']//following::input[1]").type(datadictvalue["C_END_DATE"])

            # Certification Type
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Certification Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CRTFCTN_TYPE"], exact=True).click()

            # Validity Rule
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Validity Rule").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_VLDTY_RULE"], exact=True).click()

            # Click on Ok Button
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        i = i + 1

        # Click on Save & Save and Close button
        #page.get_by_role("button", name="Save", exact=True).click()
        try:
            page.get_by_role("button", name="Save", exact=True).click()
            #expect().to_be_visible()
            page.wait_for_timeout(3000)
            print("Documents Uploaded Successfully")
            datadictvalue["RowStatus"] = "Documents Uploaded Successfully"
        except Exception as e:
            print("Unable to Upload Documents")
            datadictvalue["RowStatus"] = "Unable to Upload Documents"

    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(2000)


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_PRGM_DOC_UPLOAD):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_PRGM_DOC_UPLOAD,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_PRGM_DOC_UPLOAD)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_PRGM_DOC_UPLOAD)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_PRGM_DOC_UPLOAD + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))





