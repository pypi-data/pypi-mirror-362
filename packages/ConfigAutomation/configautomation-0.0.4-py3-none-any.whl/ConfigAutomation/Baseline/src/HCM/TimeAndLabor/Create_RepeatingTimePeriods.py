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
    page.wait_for_timeout(5000)

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Define Time and Labor")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Define Time and Labor", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Repeating Time Periods").click()
    page.wait_for_timeout(2000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        # Create
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)

        # Name
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(str(datadictvalue["C_NAME"]))
        page.wait_for_timeout(2000)

        # Description
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(str(datadictvalue["C_DSCRPTN"]))
        page.wait_for_timeout(2000)

        # Period Usage
        if datadictvalue["C_TIME_CARD"] != "N/A":
            if datadictvalue["C_TIME_CARD"] == "Yes":
                page.get_by_text("Time Card", exact=True).check()
            elif datadictvalue["C_TIME_CARD"] == "No" or '':
                page.get_by_text("Time Card", exact=True).uncheck()
            page.wait_for_timeout(3000)

        if datadictvalue["C_APPRVL"] != "N/A":
            if datadictvalue["C_APPRVL"] == "Yes":
                page.get_by_text("Approval", exact=True).check()
            elif datadictvalue["C_APPRVL"] == "No" or '':
                page.get_by_text("Approval", exact=True).uncheck()
            page.wait_for_timeout(3000)

        if datadictvalue["C_ACCRL_PRCSSNG"] != "N/A":
            if datadictvalue["C_ACCRL_PRCSSNG"] == "Yes":
                page.get_by_text("Accrual Processing", exact=True).check()
            elif datadictvalue["C_ACCRL_PRCSSNG"] == "No" or '':
                page.get_by_text("Accrual Processing", exact=True).uncheck()
            page.wait_for_timeout(3000)

        if datadictvalue["C_OVRTM"] != "N/A":
            if datadictvalue["C_OVRTM"] == "Yes":
                page.get_by_text("Overtime", exact=True).check()
            elif datadictvalue["C_OVRTM"] == "No" or '':
                page.get_by_text("Overtime", exact=True).uncheck()
            page.wait_for_timeout(3000)

        if datadictvalue["C_BLNCS"] != "N/A":
            if datadictvalue["C_BLNCS"] == "Yes":
                page.get_by_text("Balances", exact=True).check()
            elif datadictvalue["C_BLNCS"] == "No" or '':
                page.get_by_text("Balances", exact=True).uncheck()
            page.wait_for_timeout(3000)

        page.wait_for_timeout(4000)

        # Period Type - Daily
        if datadictvalue["C_DPT_PRD_TYPE"] == "Daily":
            page.get_by_role("combobox", name="Period Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DPT_PRD_TYPE"], exact=True).click()
            page.wait_for_timeout(3000)

            # Period Length
            if datadictvalue["C_DPT_PRD_LNGTH"] != "N/A":
                page.get_by_role("combobox", name="Period Length").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DPT_PRD_LNGTH"], exact=True).click()
                page.wait_for_timeout(3000)

            # Number of Days
            if datadictvalue["C_NMBR_OF_DAYS"] != "N/A":
                page.get_by_label("Number of Days").click()
                page.get_by_label("Number of Days").fill(str(datadictvalue["C_NMBR_OF_DAYS"]))
                page.wait_for_timeout(3000)

            # Sample Start Date
            if datadictvalue["C_SMPLE_START_DATE"] != "N/A":
                page.locator("//label[text()='Sample Start Date']//following::input[1]").clear()
                page.locator("//label[text()='Sample Start Date']//following::input[1]").fill(str(datadictvalue["C_SMPLE_START_DATE"]))
                page.wait_for_timeout(3000)

        # Period Type - Monthly
        if datadictvalue["C_DPT_PRD_TYPE"] == "Monthly":
            page.get_by_role("combobox", name="Period Type").click()
            # page.get_by_text(datadictvalue["C_DPT_PRD_TYPE"], exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DPT_PRD_TYPE"], exact=True).click()
            page.wait_for_timeout(3000)

            # Period Length
            if datadictvalue["C_MPT_PRD_LNGTH"] != "N/A":
                page.get_by_role("combobox", name="Period Length").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MPT_PRD_LNGTH"], exact=True).click()
                page.wait_for_timeout(3000)

            # Number of Months
            if datadictvalue["C_NMBR_OF_MNTHS"] != "N/A":
                page.get_by_label("Number of Months").click()
                page.get_by_label("Number of Months").fill(str(datadictvalue["C_NMBR_OF_MNTHS"]))
                page.wait_for_timeout(3000)

            # Sample Start Date
            if datadictvalue["C_SMPLE_START_DATE"] != "N/A":
                page.locator("//label[text()='Sample Start Date']//following::input[1]").clear()
                page.locator("//label[text()='Sample Start Date']//following::input[1]").fill(str(datadictvalue["C_SMPLE_START_DATE"]))
                page.wait_for_timeout(3000)

        # Period Type - Semimonthly
        if datadictvalue["C_DPT_PRD_TYPE"] == "Semimonthly":
            page.get_by_role("combobox", name="Period Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DPT_PRD_TYPE"], exact=True).click()
            page.wait_for_timeout(4000)

            # Sample Start Date
            if datadictvalue["C_SMPLE_START_DATE"] != "N/A":
                page.locator("//label[text()='Sample Start Date']//following::input[1]").clear()
                page.locator("//label[text()='Sample Start Date']//following::input[1]").fill(str(datadictvalue["C_SMPLE_START_DATE"]))
                page.wait_for_timeout(3000)

        # Period Type - Weekly
        if datadictvalue["C_DPT_PRD_TYPE"] == "Weekly":
            page.get_by_role("combobox", name="Period Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DPT_PRD_TYPE"], exact=True).click()
            page.wait_for_timeout(3000)

            # Period Length
            if datadictvalue["C_WPT_PERD_LNGTH"] != "N/A":
                page.get_by_role("combobox", name="Period Length").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WPT_PERD_LNGTH"], exact=True).click()
                page.wait_for_timeout(3000)

            # Number of Weeks
            if datadictvalue["C_NMBR_OF_WEEKS"] != "N/A":
                page.get_by_label("Number of Weeks").click()
                page.get_by_label("Number of Weeks").fill(str(datadictvalue["C_NMBR_OF_WEEKS"]))
                page.wait_for_timeout(3000)

            # Sample Start Date
            if datadictvalue["C_SMPLE_START_DATE"] != "N/A":
                page.locator("//label[text()='Sample Start Date']//following::input[1]").clear()
                page.locator("//label[text()='Sample Start Date']//following::input[1]").fill(str(datadictvalue["C_SMPLE_START_DATE"]))
                page.wait_for_timeout(3000)

        # Save and Close
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Repeating Time Periods")).to_be_visible()
            print("Repeating Time Periods Saved Successfully")
            datadictvalue["RowStatus"] = "Added Repeating Time Period"
        except Exception as e:
            print("Unable to save Repeating Time Period")
            datadictvalue["RowStatus"] = "Unable to Add Repeating Time Period"

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, REPEATING_TIME_PERIOD):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, REPEATING_TIME_PERIOD,
                             PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, REPEATING_TIME_PERIOD)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[
            0] + "_" + REPEATING_TIME_PERIOD + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
