from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Navigator").click()
    page.wait_for_timeout(6000)
    page.get_by_title("Tools", exact=True).click()
    page.get_by_role("link", name="Alerts Composer").click()
    page.wait_for_timeout(10000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Add
        page.locator("//a[@title='Add']").click()
        page.get_by_text("Resource Alert").click()

        # Enabled
        page.get_by_role("combobox", name="Enabled").click()
        page.get_by_text(datadictvalue["C_ENBLD"]).click()
        page.wait_for_timeout(3000)

        # Alert Name
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_ALERT_NAME"])
        page.wait_for_timeout(3000)

        # Description
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(3000)

        # Resource
        page.get_by_role("combobox", name="Resource").click()
        page.get_by_text(datadictvalue["C_RSRC"], exact=True).click()
        page.wait_for_timeout(3000)

        # Filters
        if datadictvalue["C_F_RSRC"] != '':
            page.get_by_role("link", name="Filters").click()
            page.get_by_role("button", name="Add Filter").click()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Resource").click()
            page.get_by_text(datadictvalue["C_F_RSRC"], exact=True).click()
            page.wait_for_timeout(3000)
        # Add Expression
            page.get_by_role("button", name="Add Expression").click()
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_F_NAME"])
            page.wait_for_timeout(3000)
            page.get_by_label("Expression").click()
            page.get_by_label("Expression").fill(datadictvalue["C_F_EXPRSSN"])
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Apply").click()
            page.wait_for_timeout(3000)

        # Templates
        if datadictvalue["C_T_NAME"] != '':
            page.get_by_role("link", name="Templates").click()
            page.get_by_role("button", name="Add Template").click()
            page.wait_for_timeout(3000)
            page.get_by_role("cell", name="Name Preview Translation").get_by_label("Name").click()
            page.get_by_role("cell", name="Name Preview Translation").get_by_label("Name").fill(datadictvalue["C_T_NAME"])
            page.wait_for_timeout(3000)
            if datadictvalue["C_T_DFLT_LNGG"] != '':
                page.get_by_role("combobox", name="Default Language").click()
                page.get_by_text(datadictvalue["C_T_DFLT_LNGG"], exact=True).click()
                page.wait_for_timeout(3000)
            if datadictvalue["C_T_ENBLD"] != '':
                page.get_by_role("combobox", name="Enabled").click()
                page.get_by_text(datadictvalue["C_T_ENBLD"], exact=True).click()
                page.wait_for_timeout(3000)
            if datadictvalue["C_T_EDIT"] != '':
                page.get_by_title("Edit").nth(3).click()
                page.wait_for_timeout(3000)
                page.get_by_text(datadictvalue["C_T_EDIT"],exact=True).click()
                page.wait_for_timeout(3000)
            # Recipient
                if datadictvalue["C_T_CMMNCTN_MTHD"] != '':
                    page.get_by_role("button", name="Add Recipient").click()
                    page.get_by_role("combobox", name="Communication Method").click()
                    page.get_by_text(datadictvalue["C_T_CMMNCTN_MTHD"], exact=True).click()
                    page.wait_for_timeout(3000)
                    page.get_by_label("Expression").click()
                    page.get_by_label("Expression").fill(datadictvalue["C_T_EXPRSN"])
                    page.wait_for_timeout(3000)
            # Format - Text
                if datadictvalue["C_M_FRMT"] == "Text":
                    page.get_by_role("combobox", name="Format").click()
                    page.get_by_text(datadictvalue["C_M_FRMT"], exact=True).click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_M_SBJCT"] != '':
                        page.get_by_label("Subject").click()
                        page.get_by_label("Subject").fill(datadictvalue["C_M_SBJCT"])
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_M_GROUP_BY"] != '':
                        page.get_by_label("Group By").click()
                        page.get_by_label("Group By").fill(datadictvalue["C_M_GROUP_BY"])
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_M_MSSG_TEXT"] != '':
                        page.get_by_label("Message Text").click()
                        page.get_by_label("Message Text").fill(datadictvalue["C_M_MSSG_TEXT"])
                        page.wait_for_timeout(3000)
                # Format - HTML
                elif datadictvalue["C_M_FRMT"] == "HTML":
                    page.get_by_role("combobox", name="Format").click()
                    page.get_by_text(datadictvalue["C_M_FRMT"], exact=True).click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_M_SBJCT"] != '':
                        page.get_by_label("Subject").click()
                        page.get_by_label("Subject").fill(datadictvalue["C_M_SBJCT"])
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_M_GROUP_BY"] != '':
                        page.get_by_label("Group By").click()
                        page.get_by_label("Group By").fill(datadictvalue["C_M_GROUP_BY"])
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_M_MSSG_TEXT"] != '':
                        page.frame_locator("[id=\"_FOpt1\\:_UISpageCust\"] iframe").locator("body").click()
                        page.frame_locator("[id=\"_FOpt1\\:_UISpageCust\"] iframe").locator("body").fill(datadictvalue["C_M_MSSG_TEXT"])
                        page.wait_for_timeout(3000)
                page.get_by_role("button", name="Apply").click()
                page.wait_for_timeout(3000)

        # Run Options
        if datadictvalue["C_R_ATMTCLLY_RUN"] != '':
            page.get_by_role("link", name="Run Options").click()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Automatically Run").click()
            page.get_by_text(datadictvalue["C_R_ATMTCLLY_RUN"], exact=True).click()
            page.wait_for_timeout(3000)
        if datadictvalue["C_R_MXMM_MSSGS"] != '':
            page.get_by_label("Maximum Messages").click()
            page.get_by_label("Maximum Messages").fill(datadictvalue["C_R_MXMM_MSSGS"])
            page.wait_for_timeout(3000)
        if datadictvalue["C_R_STOP_DPLCT_MSSGS"] != "No":
            page.get_by_role("combobox", name="Stop Duplicate Messages").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_R_STOP_DPLCT_MSSGS"]).click()
            page.wait_for_timeout(3000)
            page.get_by_label("For").click()
            page.get_by_label("For").fill(str(datadictvalue["C_R_FOR"]))
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="KeepFreqType").click()
            page.get_by_text(datadictvalue["C_R_FRQNCY"], exact=True).click()
            page.wait_for_timeout(3000)
        if datadictvalue["C_R_LOG_ACTVTY_HSTRY"] != '':
            page.get_by_role("combobox", name="Log Activity History").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_R_LOG_ACTVTY_HSTRY"], exact=True).click()
            page.wait_for_timeout(3000)
        if datadictvalue["C_R_SMLT_RUN"] != '':
            page.get_by_role("combobox", name="Simulate Run").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_R_SMLT_RUN"], exact=True).click()
            page.wait_for_timeout(3000)

        # Save and Close
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Save and Close").click()

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Alerts")).to_be_visible()
            print("Alerts Saved Successfully")
            datadictvalue["RowStatus"] = "Alerts Saved Successfully"
        except Exception as e:
            print("Alerts not saved")
            datadictvalue["RowStatus"] = "Alerts not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HEAL_SAF_CONFIG_WRKBK, ENABLE_DELIVERED_ALERTS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HEAL_SAF_CONFIG_WRKBK, ENABLE_DELIVERED_ALERTS, PRCS_DIR_PATH + HEAL_SAF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HEAL_SAF_CONFIG_WRKBK, ENABLE_DELIVERED_ALERTS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", HEAL_SAF_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", HEAL_SAF_CONFIG_WRKBK)[0] + "_" + ENABLE_DELIVERED_ALERTS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
