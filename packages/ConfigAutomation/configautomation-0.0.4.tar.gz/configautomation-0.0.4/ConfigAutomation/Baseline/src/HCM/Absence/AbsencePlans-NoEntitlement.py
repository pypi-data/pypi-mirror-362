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

    #Navigation
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Navigator").click()
    page.wait_for_timeout(2000)
    page.get_by_title("My Client Groups", exact=True).click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Absences", exact=True).click()
    page.wait_for_timeout(5000)

    #Search and Select Absence Plan
    page.get_by_placeholder("Search for tasks").click()
    page.get_by_placeholder("Search for tasks").type("Absence Plans")
    page.get_by_role("link", name="Search for tasks").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Absence Plans").click()
    page.wait_for_timeout(4000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        # Create Absence Plan
        page.get_by_role("button", name="Create").click()
        page.locator("//div[text()='Create Absence Plan']//following::input[1]").click()
        page.locator("//div[text()='Create Absence Plan']//following::input[1]").fill("")
        page.locator("//div[text()='Create Absence Plan']//following::input[1]").type(datadictvalue["C_EFCTV_DATE"])
        page.wait_for_timeout(1000)
        page.locator("//div[text()='Create Absence Plan']//following::label[text()='Legislation']//following::input[1]").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTN"], exact=True).click()
        page.locator("//div[text()='Create Absence Plan']//following::label[text()='Plan Type']//following::input[1]").click()
        page.wait_for_timeout(1000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLAN_TYPE"], exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Continue").click()


        #General Attribute
        page.get_by_label("Plan", exact=True).click()
        page.get_by_label("Plan", exact=True).type(datadictvalue["C_PLAN"])
        page.get_by_role("combobox", name="Plan UOM").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLAN_UOM"], exact=True).click()

        if datadictvalue["C_ALTNTV_SCHDL_CTGRY"] != "":
            page.get_by_role("combobox", name="Alternative Schedule Category").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ALTNTV_SCHDL_CTGRY"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_LGSLTV_GRPNG_CODE"] != "N/A":
            page.get_by_role("combobox", name="Legislative Grouping Code").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTV_GRPNG_CODE"])
            page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Legislative Data Group").click()
        page.get_by_text(datadictvalue["C_LGSLTV_DATA_GRP"], exact=True).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Status").click()
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()
        page.wait_for_timeout(2000)

        # Plan Term
        if datadictvalue["C_TYPE"] == "Calendar year":
            page.get_by_role("combobox", name="Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
            page.wait_for_timeout(1000)
            page.locator("//label[text()='Calendar']//following::input[1]").click()
            page.locator("//label[text()='Calendar']//following::input[1]").type(datadictvalue["C_CLNDR"])
            page.wait_for_timeout(1000)

        if datadictvalue["C_TYPE"] == "Anniversary year":
            page.get_by_role("combobox", name="Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Anniversary Event Rule").click()
            page.get_by_text(datadictvalue["C_ANNVRSRY_EVENT_RULE"], exact=True).click()
            page.wait_for_timeout(1000)

        #Participation
        page.get_by_role("link", name="Participation").click()
        page.wait_for_timeout(4000)
        page.get_by_role("combobox", name="Enrollment Start Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ENRLMT_START_RULE"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Enrollment End Rule").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ENRLMT_END_RULE"]).click()
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Select and Add").first.click()
        page.wait_for_timeout(2000)
        page.get_by_label("Sequence", exact=True).click()
        page.get_by_label("Sequence", exact=True).type(str(datadictvalue["C_ELGBLTY_SQNC"]))
        page.wait_for_timeout(1000)
        page.get_by_title("Search: Eligibility Profile").click()
        page.wait_for_timeout(1000)
        page.get_by_role("link", name="Search...").click()
        page.get_by_role("button", name="Advanced").click()
        page.wait_for_timeout(1000)
        page.get_by_label("Name").nth(1).click()
        page.get_by_label("Name").nth(1).fill("")
        page.get_by_label("Name").nth(1).type(datadictvalue["C_ELGBTY_PROFL"])
        page.wait_for_timeout(2000)
        page.get_by_label("Status Operator").click()
        page.get_by_role("listbox").get_by_text("Is not blank").click()
        page.wait_for_timeout(4000)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)
        page.locator("//div[text()='Search and Select: Eligibility Profile']//following::tr//following::td//following::span[text()='" + datadictvalue["C_ELGBTY_PROFL"] + "']").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="OK").first.click()
        page.wait_for_timeout(2000)
        page.get_by_title("Save and Close").click()
        page.wait_for_timeout(4000)

        #Entries and Balances

        #Adjustments and Transfers
        page.get_by_role("link", name="Entries and Balances").click()
        page.wait_for_timeout(4000)
        if datadictvalue["C_OTHER_ADJSTMNTS"] !="No":
            if not page.get_by_text("Other adjustments").first.is_checked():
                page.get_by_text("Other adjustments").first.click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_OTHER_ADJSTMNT_RSNS"] != "N/A" or "None":
                page.get_by_label("Other Adjustment Reasons").click()
                page.get_by_label(datadictvalue["C_OTHER_ADJSTMNT_RSNS"]).click()
                page.wait_for_timeout(1000)
                page.get_by_label("Other Adjustment Reasons").click()
                page.wait_for_timeout(1000)

        #Rates
        if datadictvalue["C_ABSNC_PYMNT_RULE"]!="N/A":
            if datadictvalue["C_ABSNC_PYMNT_RULE"] == "Rate definition" or "Unpaid":
                page.get_by_role("combobox", name="Absence Payment Rate Rule").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_PYMNT_RULE"]).click()
                page.wait_for_timeout(3000)
                if datadictvalue["C_ABSNC_PYMNT_RATE"] !="N/A":
                    page.get_by_role("combobox", name="Rate Name").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_PYMNT_RATE"]).click()
                    page.wait_for_timeout(3000)

        if datadictvalue["C_TRNFR_ABSNC_PYMNT"] == "Yes":
            page.get_by_text("Transfer absence payment information for payroll processing").first.check()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Element").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYRLL_ELMNT"]).click()
            page.wait_for_timeout(1000)

        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(10000)

        try:
            expect(page.get_by_role("heading", name="Absence Plans")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Absence Plans - No Entitlement Configured Successfully" + datadictvalue["C_PLAN"])
            datadictvalue["RowStatus"] = "Created Absence Plans - No Entitlement Successfully" + datadictvalue["C_PLAN"]
        except Exception as e:
            print("Unable to Save Absence Plans - No Entitlement Configuration" + datadictvalue["C_PLAN"])
            datadictvalue["RowStatus"] = "Unable to Save Absence Plans - No Entitlement Configuration" + datadictvalue["C_PLAN"]

        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_PLANS_NO_ENTITLEMENT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_PLANS_NO_ENTITLEMENT,PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + ABSENCE_CONFIG_WRKBK, ABSENCE_PLANS_NO_ENTITLEMENT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", ABSENCE_CONFIG_WRKBK)[0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




