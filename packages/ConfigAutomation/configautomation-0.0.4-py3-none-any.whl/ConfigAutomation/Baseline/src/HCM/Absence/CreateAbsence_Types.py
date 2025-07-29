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
    page.wait_for_timeout(40000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Absence Types")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Absence Types", exact=True).click()

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        if datadictvalue["C_ABSNC_PLAN"] != PrevName:
            if i > 0:
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(4000)

            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)

            # Entering Effective As-of Date
            page.get_by_role("cell", name="Create Absence Type *").get_by_placeholder("m/d/yy").clear()
            page.get_by_role("cell", name="Create Absence Type *").get_by_placeholder("m/d/yy").type(datadictvalue["C_EFCTV_DATE"])

            # Legislation
            page.wait_for_timeout(2000)
            page.get_by_title("United States").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTN"], exact=True).click()


            # Pattern
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Pattern").click()
            page.get_by_text(datadictvalue["C_PTTRN"]).click()

            page.get_by_role("button", name="Continue").click()
            page.wait_for_timeout(5000)

            # Name
            page.get_by_label("Name").clear()
            page.get_by_label("Name").type(datadictvalue["C_NAME"])

            # UOM
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="UOM").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MEASR"]).click()

            # Legislative Data Group
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Legislative Data Group").click()
            page.get_by_text(datadictvalue["C_LGSLTVE_DTGRP"],exact=True).click()

            # Status
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Status").click()
            page.get_by_text(datadictvalue["C_STTUS"], exact=True).click()

            # Event Type
            if datadictvalue["C_EVNT_TYPE"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Event Type").click()
                page.get_by_text(datadictvalue["C_EVNT_TYPE"], exact=True).click()

            # Legislative Grouping Code
            if datadictvalue["C_LGSLTV_GRPNG_CODE"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Legislative Grouping Code").click()
                page.get_by_text(datadictvalue["C_LGSLTV_GRPNG_CODE"], exact=True).click()

            # Minimum Duration Alert
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Minimum Duration Alert").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MNMUM_DRTON_ALERT"]).click()

            # Maximum Duration Alert
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Maximum Duration Alert").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_MXMUM_DRTON_ALERT"]).click()

            # Partial Day Rule
            if datadictvalue["C_PTTRN"]!='Childbirth or Placement':
                if datadictvalue["C_MEASR"] == 'Hours':
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Partial Day Rule").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRTAL_DAY_RULE"]).click()

            # Schedule Hierarchy Start Point
            if datadictvalue["C_SCHDL_START_POINT"]!='':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Schedule Hierarchy Start Point").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SCHDL_START_POINT"]).click()

            # Enable employee updates
            if datadictvalue["C_ENBLE_EMPLY_UPDTES"]=='Yes':
                page.get_by_text("Enable employee updates").check()
            elif datadictvalue["C_ENBLE_EMPLY_UPDTES"]=='No':
                page.get_by_text("Enable employee updates").uncheck()

            # Enable manager updates
            if datadictvalue["C_ENBLE_MNGER_UPDTES"]=='Yes':
                page.get_by_text("Enable manager updates").check()
            elif datadictvalue["C_ENBLE_MNGER_UPDTES"]=='No':
                page.get_by_text("Enable manager updates").uncheck()

            # Enable administrative updates
            if datadictvalue["C_ENBLE_ADMIN_UPDTES"]=='Yes':
                page.get_by_text("Enable administrative updates").check()
            elif datadictvalue["C_ENBLE_ADMIN_UPDTES"]=='No':
                page.get_by_text("Enable administrative updates").uncheck()

            # Lock if completed for employee
            if datadictvalue["C_LOCK_CMPLT_EMPLY"]=='Yes':
                page.get_by_text("Lock if completed for employee").check()
            elif datadictvalue["C_LOCK_CMPLT_EMPLY"]=='No':
                page.get_by_text("Lock if completed for employee").uncheck()

            # Enable for time card entry
            if datadictvalue["C_MEASR"] == 'Hours':
                # if datadictvalue["C_ENBLE_TIME_CARD_ENTRY"]!='':
                    page.wait_for_timeout(4000)
                    page.get_by_role("combobox", name="Enable for time card entry").click()
                    page.get_by_text(datadictvalue["C_ENBLE_TIME_CARD_ENTRY"]).click()

            # Clicking on Plans and Reasons
            page.get_by_role("link", name="Plans and Reasons").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Select and Add").first.click()
            page.get_by_title("Search: Plan").click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Name").clear()
            page.get_by_label("Name").type(datadictvalue["C_ABSNC_PLAN"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.locator("//button[text()='Search']//following::span[4]").click()
            page.get_by_role("button", name="OK").nth(1).click()
            page.wait_for_timeout(3000)

            # Priority
            page.get_by_label("Priority").clear()
            page.get_by_label("Priority").type(datadictvalue["C_PRIORITY"])
            page.locator("//button[@accesskey='K']").click()
            # page.get_by_role("button", name="OK").click()
            # page.get_by_title("button", name="OK").click()

            page.wait_for_timeout(4000)
            PrevName = datadictvalue["C_ABSNC_PLAN"]
            print("Name:", PrevName)

        # Clicking on Plans and Reasons
        if datadictvalue["C_REASON"] != 'None' or '':
            page.get_by_role("button", name="Select and Add").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Reason", exact=True).click()
            page.get_by_text(datadictvalue["C_REASON"], exact=True).click()
            page.get_by_role("button", name="OK").click()

        i = i + 1

    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(2000)
    try:
        expect(page.get_by_role("heading", name="Absence Types")).to_be_visible()
        page.wait_for_timeout(3000)
        print("Absence Types Created Successfully")
        datadictvalue["RowStatus"] = "Created Absence Types Successfully"
    except Exception as e:
        print("Unable to Save Absence Types")
        datadictvalue["RowStatus"] = "Unable to Save Absence Types"


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_TYPES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_TYPES,PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_TYPES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))



