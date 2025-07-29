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
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Configure Seniority Dates")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(3000)


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)
        page.get_by_role("link", name="Configure Seniority Dates", exact=True).click()
        # Selecting Seniority Data rule set
        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(3000)
        if page.get_by_role("row", name="Active Seniority Rule Name").get_by_label("Active").first.is_visible():
            page.get_by_role("row", name="Active Seniority Rule Name").get_by_label("Active").first.click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ACTV"]).click()
        if page.get_by_role("combobox", name="Seniority Rule Name").first.is_visible():
            page.get_by_role("combobox", name="Seniority Rule Name").first.click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SNRTY_RULE_NAME"]).click()
        if page.get_by_role("combobox", name="Attribute").first.is_visible():
            page.get_by_role("combobox", name="Attribute").first.click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ATTRBT"]).click()
        if page.get_by_role("combobox", name="Level").first.is_visible():
            page.get_by_role("combobox", name="Level").first.click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LEVEL"]).click()
        if page.get_by_role("combobox", name="Cumulative").first.is_visible():
            page.get_by_role("combobox", name="Cumulative").first.click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CMLTV"]).click()
        if page.get_by_role("combobox", name="Allow Edit").first.is_visible():
            page.get_by_role("combobox", name="Allow Edit").first.click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ALLOW_EDIT"]).click()
        if page.get_by_role("combobox", name="Display in Guided Flows").first.is_visible():
            page.get_by_role("combobox", name="Display in Guided Flows").first.click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSPLY_IN_GDD_FLOWS"]).click()
        if page.get_by_role("combobox", name="Override Seniority Basis").first.is_visible():
            page.get_by_role("combobox", name="Override Seniority Basis").first.click()
            page.wait_for_timeout(2000)
            page.locator('[id="__af_Z_window"]').get_by_text(datadictvalue["C_OVRRD_SNRTY_BASIS"],exact=True).click()
        if datadictvalue["C_WRKR_TYPE"] !='':
            if page.get_by_role("cell", name="Worker Type").nth(1).locator("a").is_visible():
                page.get_by_role("cell", name="Worker Type").nth(1).locator("a").click()
                page.wait_for_timeout(2000)
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WRKR_TYPE"]).check()
                # page.get_by_role("checkbox", name=datadictvalue["C_WRKR_TYPE"], exact=True).check()

        if datadictvalue["C_OVRRD_SNRTY_BASIS"]!='Days':
            if datadictvalue["C_USE_FRML_FOR_HRS_CNVRSN"]!='N/A' or '':
                if datadictvalue["C_USE_FRML_FOR_HRS_CNVRSN"] == 'Yes':
                    page.get_by_text("Use Formula for Hours").check()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_HRS_CNVRSN_FRMLA"]!='N/A' or '':
                        page.get_by_label("Hours Conversion Formula").click()
                        page.get_by_label("Hours Conversion Formula").type(datadictvalue["C_HRS_CNVRSN_FRMLA"])
                        page.get_by_label("Hours Conversion Formula").press("Tab")
                if datadictvalue["C_USE_FRML_FOR_HRS_CNVRSN"] == 'No':
                    page.get_by_text("Use Formula for Hours").uncheck()

            if datadictvalue["C_HRS_IN_A_DAY"] != 'N/A' or '':
                page.get_by_label("Hours in a Day").clear()
                page.get_by_label("Hours in a Day").type(datadictvalue["C_HRS_IN_A_DAY"])

            if datadictvalue["C_HRS_IN_A_MONTH"] != 'N/A' or '':
                page.get_by_label("Hours in a Month").clear()
                page.get_by_label("Hours in a Month").type(datadictvalue["C_HRS_IN_A_MONTH"])

            if datadictvalue["C_HRS_IN_A_YEAR"] != 'N/A' or '':
                page.get_by_label("Hours in a Year").clear()
                page.get_by_label("Hours in a Year").type(datadictvalue["C_HRS_IN_A_YEAR"])


        # Saving the Record
        page.get_by_role("button", name="Save").click()
        page.get_by_role("button", name="Yes").click()
        page.wait_for_timeout(3000)
        if page.get_by_text("Confirmation").is_visible():
            page.get_by_role("link", name="Close").click()
            page.wait_for_timeout(2000)
        page.get_by_role("link", name="Back").click()
        page.wait_for_timeout(3000)
        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Seniority Rule Saved Successfully")
            datadictvalue["RowStatus"] = "Seniority Rule Saved"
        except Exception as e:
            print("Unable to save Seniority Rule")
            datadictvalue["RowStatus"] = "Unable to save Seniority Rule"

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Seniority Rule Added Successfully"
        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict

#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, SENIORITY_DATE_RULES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, SENIORITY_DATE_RULES, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, SENIORITY_DATE_RULES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0]+ "_" + SENIORITY_DATE_RULES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + SENIORITY_DATE_RULES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
