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
    page.wait_for_timeout(3000)

    # Navigate to Setup and Maintenance
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Settings and Actions").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(4000)
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(4000)
    page.get_by_label("", exact=True).fill("Absence Certifications")
    page.get_by_label("", exact=True).click()
    page.get_by_role("button", name="Search").click()
    page.get_by_role("link", name="Absence Certifications").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        # Effective Start
        if datadictvalue["C_EFCTV_START_DATE"] != '':
            page.get_by_placeholder("m/d/yy").click()
            page.get_by_placeholder("m/d/yy").clear()
            page.wait_for_timeout(2000)
            page.get_by_placeholder("m/d/yy").fill(datadictvalue["C_EFCTV_START_DATE"])
            page.get_by_placeholder("m/d/yy").press("Tab")
            page.wait_for_timeout(2000)
            page.get_by_text("Warning").click()
            page.get_by_role("button", name="Yes").click()

        # Classification
        page.get_by_role("combobox", name="Classification").click()
        page.wait_for_timeout(2000)
        page.get_by_text(datadictvalue["C_CLSSFCTN"], exact=True).click()

        # Legislation
        page.get_by_role("combobox", name="Legislation").click()
        page.wait_for_timeout(5000)
        page.get_by_text(datadictvalue["C_LGSLTN"], exact=True).click()

        # Name
        #page.get_by_role("cell", name="*Name", exact=True).locator("label").click()
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(2000)

        # Description
        if datadictvalue["C_DSCRPTN"] != '':
            #page.get_by_role("row", name="Description Description", exact=True).locator("span").click()
            page.get_by_label("Description").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        # Status
        page.get_by_role("combobox", name="Status").click()
        page.wait_for_timeout(2000)
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

        # Absence Record Update Rule
        page.get_by_role("combobox", name="Absence Record Update Rule").click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_RCRD_UPDT_RULE"])
        page.wait_for_timeout(2000)

        # Trigger
        #page.get_by_role("heading", name="Creation").click()
        page.get_by_role("combobox", name="Trigger").click()
        page.wait_for_timeout(2000)
        page.get_by_text(datadictvalue["C_TRGGR"], exact=True).click()

        if datadictvalue["C_CNFRMD_CRTD"] == "Yes":
            if not page.get_by_text("Mark as confirmed when created", exact=True).is_checked():
                page.get_by_text("Mark as confirmed when created", exact=True).click()


        # Eligibility Profile
        page.wait_for_timeout(3000)
        if page.get_by_role("combobox", name="Eligibility Profile").is_visible():
            page.get_by_role("combobox", name="Eligibility Profile").click()
            page.wait_for_timeout(4000)
            page.get_by_text(datadictvalue["C_ELGBTY_PRFL"]).click()

        # Due Date Rule (Passage of Due Date)
        if datadictvalue["C_DUE_DATE_RULE"] != '':
            page.get_by_role("combobox", name="Due Date Rule").click()
            page.wait_for_timeout(5000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DUE_DATE_RULE"]).click()
            #page.get_by_text(datadictvalue["C_DUE_DATE_RULE"])
        # Reference Date
        #if datadictvalue["C_RFRNC_DATE"] != '':
            #page.get_by_role("cell", name="Reference Date").nth(1).click()
        if page.get_by_role("combobox", name="Reference Date").is_visible():
            page.get_by_role("combobox", name="Reference Date").click()
            page.wait_for_timeout(4000)
            page.get_by_text(datadictvalue["C_RFRNC_DATE"], exact=True).click()
            # Duration
        page.wait_for_timeout(3000)
        if page.get_by_label("Duration").is_visible():
            page.get_by_label("Duration").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Duration").fill(str(datadictvalue["C_DRTN"]))
        # UOM
        if page.get_by_role("combobox", name="UOM").is_visible():
            #page.get_by_role("cell", name="UOM").nth(1).click()
            page.get_by_role("combobox", name="UOM").click()
            page.wait_for_timeout(4000)
            page.get_by_text(datadictvalue["C_PDD_UOM"]).click()

        # Reason Rule (Confirmation)
        if datadictvalue["C_RSN_RULE"] != '':
            #page.get_by_role("cell", name="Reason Rule Reasons Absence").get_by_role("combobox").click()
            page.locator("//h1[text()='Confirmation']//following::input[1]").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RSN_RULE"]).click()
            #page.get_by_role("cell", name="Reason Rule", exact=True).nth(1).select_option(datadictvalue["C_RESON_RULE"])
            page.wait_for_timeout(3000)
            #page.get_by_text(datadictvalue["C_RESON_RULE"])
        # Reasons
        if page.get_by_label("Reasons").first.is_visible():
            page.get_by_label("Reasons").first.click()
            #page.get_by_role("cell", name="Reasons").nth(1).click()
            #page.get_by_text("Reasons").first.click()
            page.wait_for_timeout(3000)
            page.get_by_label(datadictvalue["C_RSNS"]).click()
            page.wait_for_timeout(1000)
            page.get_by_label("Reasons").first.press("Tab")
            #page.get_by_label("Reasons").fill(datadictvalue["C_RESONS"]).press("Tab")
            page.wait_for_timeout(3000)
        # Absence Record Update
        if page.get_by_role("combobox", name="Absence Record Update", exact=True).nth(1).is_visible():
            page.get_by_role("combobox", name="Absence Record Update", exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_ABSNC_RCRD_UPDT"]).click()

        # Expiration Rule (Expiration)
        if datadictvalue["C_E_EXPRTN_RULE"] != '':
            page.get_by_role("combobox", name="Expiration Rule").click()
            page.wait_for_timeout(3000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_E_EXPRTN_RULE"]).click()
        # Reference Date
        if page.get_by_label("Reference Date").nth(2).is_visible():
            #page.get_by_role("combobox", name="Reference Date").click()
            page.get_by_label("Reference Date").nth(2).click()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_E_RFRNC_DATE"], exact=True).click()
        # Duration
        page.wait_for_timeout(3000)
        if page.get_by_label("Duration").nth(1).is_visible():
            page.get_by_label("Duration").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_E_DRTN"], exact=True).click()
        # UOM
        if page.get_by_role("combobox", name="UOM").nth(1).is_visible():
            page.get_by_role("combobox", name="UOM").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_E_UOM"], exact=True).click()

        # Reason Rule
        if datadictvalue["C_V_RSN_RULE"] != '':
            #page.get_by_role("heading", name="Void").click()
            #page.get_by_text("Reason Rule").nth(1).click()
            page.locator("//h1[text()='Void']//following::input[1]").click()
            #page.get_by_role("cell", name="Reason Rule Reasons", exact=True).get_by_role("combobox").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_V_RSN_RULE"]).click()
            page.wait_for_timeout(3000)
        # Reasons
        #if datadictvalue["C_V_RSN"] != '':
            #page.get_by_text("Reasons").nth(1).click()
            page.locator("//h1[text()='Void']//following::input[3]").click()
            #page.get_by_role("cell", name="Reason Rule Reasons", exact=True).get_by_label("Reasons").click()
            #page.get_by_role("cell", name="Reason Rule Reasons", exact=True).get_by_label("Reasons").click()
            page.wait_for_timeout(3000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_V_RSN"]).click()
            #page.get_by_label("Reasons").fill(datadictvalue["C_V_RESONS"]).click()
            page.wait_for_timeout(1000)
            page.locator("//h1[text()='Void']//following::input[3]").press("Tab")
            page.wait_for_timeout(2000)

        # Save and Close
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        # Submit
        try:
            expect(page.get_by_role("heading", name="Absence Certifications")).to_be_visible()
            page.wait_for_timeout(4000)
            print("Absence Certifications Created Successfully")
            datadictvalue["RowStatus"] = "Created Absence Certifications Successfully"
        except Exception as e:
            print("Unable to Save Absence Certifications")
            datadictvalue["RowStatus"] = "Unable to Save Absence Certifications"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_CERTIFICATIONS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_CERTIFICATIONS,
                             PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_CERTIFICATIONS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[
            0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
