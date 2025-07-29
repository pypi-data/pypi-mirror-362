from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("HCM Groups")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="HCM Groups").click()
    page.wait_for_timeout(2000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        # Name
        page.get_by_role("textbox", name="Name").clear()
        page.get_by_role("textbox", name="Name").fill(str(datadictvalue["C_NAME"]))
        page.wait_for_timeout(2000)

        # Description
        if datadictvalue["C_DSCRPTN"] != '':
            page.get_by_label("Description").clear()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(3000)

        # Locked
        if datadictvalue["C_LCKD"] != "Yes":
            page.get_by_role("combobox", name="Locked").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LCKD"], exact=True).click()
            page.wait_for_timeout(2000)

        if datadictvalue["C_LCKD"] != "No":
            page.get_by_role("combobox", name="Locked").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LCKD"]).click()
            page.wait_for_timeout(2000)


        # Assignment
        page.get_by_role("combobox", name="Assignment").click()
        page.get_by_text(datadictvalue["C_ASSGNMNT"], exact=True).click()
        page.wait_for_timeout(2000)

        # Include assignments with an HR status of active or suspended
        if datadictvalue["C_HR_STTS_ACTV_SSPNDD"] != '' or "N/A":
            if datadictvalue["C_HR_STTS_ACTV_SSPNDD"] == "Yes":
               page.get_by_text("Include assignments with an HR status of active or suspended", exact=True).check()
            elif datadictvalue["C_HR_STTS_ACTV_SSPNDD"] == "No":
               page.get_by_text("Include assignments with an HR status of active or suspended", exact=True).uncheck()
            page.wait_for_timeout(2000)

        # Include in Refresh All Groups Process
        if datadictvalue["C_INCLD_IN_RFRSH_ALL_GRPS_PRCSS"] != '' or "N/A":
            if datadictvalue["C_INCLD_IN_RFRSH_ALL_GRPS_PRCSS"] == "Yes":
                page.get_by_text("Include in Refresh All Groups Process", exact=True).check()
            elif datadictvalue["C_INCLD_IN_RFRSH_ALL_GRPS_PRCSS"] == "No":
                page.get_by_text("Include in Refresh All Groups Process", exact=True).uncheck()
            page.wait_for_timeout(2000)

        # Evaluation Period
        page.get_by_role("combobox", name="Evaluation Period").click()
        page.get_by_text(datadictvalue["C_EVLTN_PRD"]).click()
        page.wait_for_timeout(2000)

        # Evaluation Criteria - Select Attribute - Full Name
        if datadictvalue["C_ATTRBT"] != "N/A" or '':
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name="Expand").click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ATTRBT"], exact=True).click()
            page.wait_for_timeout(2000)
            # Operator
            page.get_by_role("combobox", name="Operator", exact=True).click()
            page.get_by_text(datadictvalue["C_OPRTR"], exact=True).click()
            page.wait_for_timeout(4000)
            # Value
            page.locator("//label[text()='Value']//following::input[1]").first.click()
            page.locator("//label[text()='Value']//following::input[1]").first.fill(datadictvalue["C_VALUE"])
            page.wait_for_timeout(3000)
            # Logical Operator
            if datadictvalue["C_LGCL_OPRTR"] != "N/A" or '':
                page.get_by_role("combobox", name="Logical Operator").click()
                page.get_by_text(datadictvalue["C_LGCL_OPRTR"], exact=True).click()
                page.wait_for_timeout(2000)

            ## Saving and Closing
            #page.get_by_title("Save and Close").click()
            #page.wait_for_timeout(3000)


        # Include or Exclude Groups
        page.get_by_text("GroupValue SetButton has a popup, press down arrow key to access the popup").click()
        page.wait_for_timeout(6000)

        # Name
        if datadictvalue["C_TYPE"] == 'Group':
            page.get_by_text(datadictvalue["C_TYPE"], exact=True).click()
            page.wait_for_timeout(2000)
            page.get_by_label("Group", exact=True).type(datadictvalue["C_INCLD_EXCLD_NAME"])
            page.wait_for_timeout(3000)
            # Condition
            page.get_by_role("combobox", name="InclFlag").click()
            page.get_by_text(datadictvalue["C_GRPS_CNDTN"], exact=True).click()
            page.wait_for_timeout(3000)

        if datadictvalue["C_TYPE"] == 'Value Set':
            page.get_by_text(datadictvalue["C_TYPE"]).click()
            page.wait_for_timeout(2000)
            page.get_by_label("Value set").type(datadictvalue["C_INCLD_EXCLD_NAME"])
            page.wait_for_timeout(3000)
            # Condition
            page.get_by_role("combobox", name="InclFlag").click()
            page.get_by_text(datadictvalue["C_GRPS_CNDTN"], exact=True).click()
            page.wait_for_timeout(3000)

        # Include or Exclude members - Member Name
        if datadictvalue["C_MMBR_NAME"] != '':
            page.get_by_role("button", name="Add", exact=True).click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name="Search: Person Name").click()
            page.wait_for_timeout(2000)
            page.locator("//div[text()='Search and Select: Person Name']//following::label[text()='Name']//following::input[1]").click()
            page.locator("//div[text()='Search and Select: Person Name']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_MMBR_NAME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_MMBR_NAME"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

            # Condition
            if datadictvalue["C_CNDTN"] != '':
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Person Name Search: Person").get_by_role("combobox").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CNDTN"]).click()
                page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        if page.get_by_role("button", name="OK").is_visible():
            page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="HCM Groups")).to_be_visible()
            print("HCM Groups Saved Successfully")
            datadictvalue["RowStatus"] = "HCM Groups Saved Successfully"
        except Exception as e:
            print("HCM Groups not saved")
            datadictvalue["RowStatus"] = "HCM Groups not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, HCM_GROUPS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, HCM_GROUPS, PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, HCM_GROUPS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0] + "_" + HCM_GROUPS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
