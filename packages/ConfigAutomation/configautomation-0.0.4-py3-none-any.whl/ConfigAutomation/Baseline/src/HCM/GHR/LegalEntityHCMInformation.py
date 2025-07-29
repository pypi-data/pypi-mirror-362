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
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(2000)

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Legal Entity HCM Information")
    page.get_by_role("textbox").press("Enter")
    # Looping the values based on excel rows
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        # Navigating to Manage Legal Entity HCM Information page & Entering the data
        page.get_by_role("link", name="Manage Legal Entity HCM Information", exact=True).click()
        page.get_by_label("Legal Entity Name").type(datadictvalue["C_LEGAL_ENTTY_NAME"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("link", name=datadictvalue["C_LEGAL_ENTTY_NAME"]).click()
        page.get_by_title("Edit").click()
        page.get_by_text("Correct").click()

        # Work Day Information
        page.get_by_label("Work Start Time").clear()
        page.get_by_label("Work Start Time").type(str(datadictvalue["C_WORK_START_TIME"]))
        page.get_by_label("Work End Time").clear()
        page.get_by_label("Work End Time").type(str(datadictvalue["C_WORK_END_TIME"]))
        page.get_by_label("Standard Working Hours", exact=True).click()
        page.get_by_label("Standard Working Hours", exact=True).clear()
        page.get_by_label("Standard Working Hours", exact=True).type(str(datadictvalue["C_STNDRD_WRKNG_HOURS"]))
        page.wait_for_timeout(1000)
        page.get_by_label("Standard Working Hours Frequency").click()
        page.get_by_label("Standard Working Hours Frequency").clear()
        page.get_by_label("Standard Working Hours Frequency").type(datadictvalue["C_STNDRD_WRKNG_HOURS_FRQNCY"])
        page.get_by_label("Standard Working Hours Frequency").press("Enter")
        # page.get_by_label("Standard Annual Working Duration", exact=True).click()
        # page.get_by_label("Standard Annual Working Duration", exact=True).fill("")
        # page.get_by_label("Standard Annual Working Duration", exact=True).type(str(datadictvalue["C_STNDRD_ANNUAL_WRKING_DRTN"]))
        # page.wait_for_timeout(1000)
        # page.get_by_label("Annual Working Duration Unit").click()
        # page.get_by_label("Annual Working Duration Unit").fill("")
        # page.get_by_label("Annual Working Duration Unit").type(datadictvalue["C_ANNUAL_WRKNG_DRTN_UNITS"])
        # page.get_by_label("Annual Working Duration Unit").press("Enter")

        # Enterprise Information
        page.get_by_label("Salary Level").click()
        page.get_by_label("Salary Level").clear()
        page.get_by_label("Salary Level").type(datadictvalue["C_SLRY_LEVEL"])
        page.get_by_label("Salary Level").press("Enter")
        page.get_by_label("Worker Number Generation").click()
        page.get_by_label("Worker Number Generation").clear()
        page.get_by_label("Worker Number Generation").type(datadictvalue["C_WRKR_NMBR_GNRTN"])
        page.get_by_label("Worker Number Generation").press("Enter")
        page.get_by_label("Allow Employment Terms").click()
        page.get_by_label("Allow Employment Terms").clear()
        page.get_by_label("Allow Employment Terms").type(datadictvalue["C_ALLOW_EMPLYMNT_TERMS_OVRRD_AT_ASGNMNT"])
        page.get_by_label("Allow Employment Terms").press("Enter")
        page.get_by_label("People Group Flexfield").click()
        page.get_by_label("People Group Flexfield").clear()
        page.get_by_label("People Group Flexfield").type(datadictvalue["C_PPL_GROUP_FLEX_FIELD"])
        page.get_by_label("People Group Flexfield").press("Enter")
        # page.get_by_label("Minimum Working Age").click()
        # page.get_by_label("Minimum Working Age").fill("")
        # page.get_by_label("Minimum Working Age").type(datadictvalue["C_MIN_WRKNG_AGE"])
        # page.get_by_label("Minimum Retirement Age").click()
        # page.get_by_label("Minimum Retirement Age").fill("")
        # page.get_by_label("Minimum Retirement Age").type(datadictvalue["C_MIN_RTRMNT_AGE"])
        # page.get_by_label("Maximum Retirement Age").click()
        # page.get_by_label("Maximum Retirement Age").fill("")
        # page.get_by_label("Maximum Retirement Age").type(datadictvalue["C_MAX_RTRMNT_AGE"])
        # page.get_by_label("Maximum Age of a Minor").click()
        # page.get_by_label("Maximum Age of a Minor").fill("")
        # page.get_by_label("Maximum Age of a Minor").type(datadictvalue["C_MAX_AGE_OF_MINOR"])
        page.get_by_label("Employment Model").click()
        page.get_by_label("Employment Model").clear()
        page.get_by_label("Employment Model").type(str(datadictvalue["C_EMP_MODEL"]))
        page.get_by_label("Employment Model").press("Enter")
        #page.get_by_role("button", name="Cancel").click()
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(5000)
        if page.get_by_text("Warning").is_visible():
            page.get_by_role("button", name="Yes").click()
        page.wait_for_timeout(5000)
        if page.get_by_text("Confirmation").is_visible():
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(5000)
        # updating the row status & repeating the data depends on availability of data in Excel
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            page.get_by_role("button", name="Done").click()
            print("Added LegalEntity HCM Info Saved Successfully")
            datadictvalue["RowStatus"] = "Added LegalEntity HCM Info and code"
        except Exception as e:
            print("Unable to save LegalEntity HCM Info")
            datadictvalue["RowStatus"] = "Unable to Add LegalEntity HCM Info and code"
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Added LegalEntity HCM Info Successfully"
        i = i + 1

    # Signout from the application
    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, LEGAL_ENTITY_HCM_INFORMATION):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, LEGAL_ENTITY_HCM_INFORMATION, PRCS_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK, LEGAL_ENTITY_HCM_INFORMATION)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_ENTSTRUCT_CONFIG_WRKBK)[0] + "_" + LEGAL_ENTITY_HCM_INFORMATION)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_ENTSTRUCT_CONFIG_WRKBK)[0]+ "_" + LEGAL_ENTITY_HCM_INFORMATION + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))