from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(3000)
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(5000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Common Lookups")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Common Lookups", exact=True).click()

    # Search - Lookup Type
    page.get_by_label("Lookup Type", exact=True).click()
    page.get_by_label("Lookup Type", exact=True).fill("ORA_HNS_INCIDENT_EVENT")
    page.wait_for_timeout(3000)
    page.get_by_label("Meaning").click()
    page.get_by_label("Meaning").fill("Incident Event")
    page.wait_for_timeout(3000)
    page.get_by_label("Description").click()
    page.get_by_label("Description").fill("A label used to categorize an incident into subtypes.")
    page.wait_for_timeout(3000)
    page.get_by_label("Module").click()
    page.get_by_label("Module").fill("Environment, Health and Safety Incidents")
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Search", exact=True).click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Add - New Lookup
        page.get_by_role("button", name="New").nth(1).click()
        page.wait_for_timeout(5000)

        # Create - New Lookup Code
        page.locator("//span[text()='Lookup Code']//following::input[1]").fill(datadictvalue["C_LKP_CODE"])
        page.wait_for_timeout(3000)

        # Display Sequence
        page.locator("//span[text()='Display Sequence']//following::input[2]").type(str(datadictvalue["C_DSPLY_SQNC"]))
        page.wait_for_timeout(3000)

        # Enabled
        if datadictvalue["C_ENBLD"] != '':
            if datadictvalue["C_ENBLD"] == "Yes":
                page.locator("//span[text()='Enabled']//following::label[3]").check()
                page.wait_for_timeout(3000)
            if datadictvalue["C_ENBLD"] == "No":
                page.locator("//span[text()='Enabled']//following::label[3]").uncheck()
                page.wait_for_timeout(3000)

        # Start Date
        if datadictvalue["C_START_DATE"] != '':
            page.locator("//span[text()='Start Date']//following::input[contains(@placeholder,'m/d/yy')][1]").clear()
            page.locator("//span[text()='Start Date']//following::input[contains(@placeholder,'m/d/yy')][1]").fill(
                str(datadictvalue["C_START_DATE"]))
            page.wait_for_timeout(3000)

        # End Date
        if datadictvalue["C_END_DATE"] != '':
            page.locator("//span[text()='End Date']//following::input[contains(@placeholder,'m/d/yy')][2]").clear()
            page.locator("//span[text()='End Date']//following::input[contains(@placeholder,'m/d/yy')][2]").fill(
                str(datadictvalue["C_END_DATE"]))
            page.wait_for_timeout(3000)

        # Meaning
        if datadictvalue["C_L_MNNG"] != '':
            page.locator(
                "//div[contains(@title,'Lookup Codes')]//following::input[contains(@placeholder,'m/d/yy')][2]//following::input[2]").click()
            page.locator(
                "//div[contains(@title,'Lookup Codes')]//following::input[contains(@placeholder,'m/d/yy')][2]//following::input[2]").fill(datadictvalue["C_L_MNNG"])
            page.wait_for_timeout(3000)

        # Description
        if datadictvalue["C_L_DSCRPTN"] != '':
            page.locator(
                "//div[contains(@title,'Lookup Codes')]//following::input[contains(@placeholder,'m/d/yy')][2]//following::input[3]").click()
            page.locator(
                "//div[contains(@title,'Lookup Codes')]//following::input[contains(@placeholder,'m/d/yy')][2]//following::input[3]").fill(datadictvalue["C_L_DSCRPTN"])
            page.wait_for_timeout(3000)

        # Tag
        if datadictvalue["C_TAG"] != '':
            page.locator(
                "//div[contains(@title,'Lookup Codes')]//following::input[contains(@placeholder,'m/d/yy')][2]//following::input[4]").click()
            page.locator(
                "//div[contains(@title,'Lookup Codes')]//following::input[contains(@placeholder,'m/d/yy')][2]//following::input[4]").fill(datadictvalue["C_TAG"])
            page.wait_for_timeout(3000)

        i = i + 1
        # Save and Close
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Save and Close").click()



    try:
        expect(page.get_by_role("heading", name="Search")).to_be_visible()
        print("Incident Event Lookup Saved Successfully")
        datadictvalue["RowStatus"] = "Incident Event Lookup Saved Successfully"
    except Exception as e:
        print("Incident Event Lookup not saved")
        datadictvalue["RowStatus"] = "Incident Event lookup not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HEAL_SAF_CONFIG_WRKBK, INCIDENT_EVENTS_LOOKUPS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HEAL_SAF_CONFIG_WRKBK, INCIDENT_EVENTS_LOOKUPS, PRCS_DIR_PATH + HEAL_SAF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HEAL_SAF_CONFIG_WRKBK, INCIDENT_EVENTS_LOOKUPS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", HEAL_SAF_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", HEAL_SAF_CONFIG_WRKBK)[0] + "_" + INCIDENT_EVENTS_LOOKUPS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
