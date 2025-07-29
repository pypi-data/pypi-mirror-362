from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *



def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    global datadictvalue
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(5000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Environment, Health and Safety Incident Completion Dates")
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(1000)
    page.get_by_role("link", name="Manage Environment, Health and Safety Incident Completion Dates", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        if datadictvalue["C_TRGT"] == "Inspection Target Approval Date":
            page.locator("//span[text()='Inspection Target Approval Date']//following::input[1]").clear()
            page.locator("//span[text()='Inspection Target Approval Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(3000)
        #elif datadictvalue["C_TRGT"] != "Inspection Target Approval Date":
            #page.locator("//span[text()='Inspection Target Approval Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Inspection Target Completion Date":
            page.locator("//span[text()='Inspection Target Completion Date']//following::input[1]").clear()
            page.locator("//span[text()='Inspection Target Completion Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(3000)
        #elif datadictvalue["C_TRGT"] != "Inspection Target Completion Date":
            #page.locator("//span[text()='Inspection Target Completion Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Inspection Target Review Date":
            page.locator("//span[text()='Inspection Target Review Date']//following::input[1]").clear()
            page.locator("//span[text()='Inspection Target Review Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(3000)
        #elif datadictvalue["C_TRGT"] != "Inspection Target Review Date":
            #page.locator("//span[text()='Inspection Target Review Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Inspection Action Target Preapproval Date":
            page.locator("//span[text()='Inspection Action Target Preapproval Date']//following::input[1]").clear()
            page.locator("//span[text()='Inspection Action Target Preapproval Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(3000)
        #elif datadictvalue["C_TRGT"] != "Inspection Action Target Preapproval Date":
            #page.locator("//span[text()='Inspection Action Target Preapproval Date']//following::input[1]").press("Tab")


        if datadictvalue["C_TRGT"] == "Inspection Action Target Approval Date":
            page.locator("//span[text()='Inspection Action Target Approval Date']//following::input[1]").clear()
            page.locator("//span[text()='Inspection Action Target Approval Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(3000)
        #elif datadictvalue["C_TRGT"] != "Inspection Action Target Approval Date":
            #page.locator("//span[text()='Inspection Action Target Approval Date']//following::input[1]").press("Tab")


        if datadictvalue["C_TRGT"] == "Inspection Action Target Completion Date":
            page.locator("//span[text()='Inspection Action Target Completion Date']//following::input[1]").clear()
            page.locator("//span[text()='Inspection Action Target Completion Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(3000)
        #elif datadictvalue["C_TRGT"] != "Inspection Action Target Completion Date":
            #page.locator("//span[text()='Inspection Action Target Completion Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Inspection Action Target Review Date":
            page.locator("//span[text()='Inspection Action Target Review Date']//following::input[1]").clear()
            page.locator("//span[text()='Inspection Action Target Review Date']//following::input[1]").type(
                str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(3000)
        #elif datadictvalue["C_TRGT"] != "Inspection Action Target Review Date":
            #page.locator("//span[text()='Inspection Action Target Review Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Action Target Approval Date":
            page.locator("//span[text()='Action Target Approval Date']//following::input[1]").clear()
            page.locator("//span[text()='Action Target Approval Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            page.wait_for_timeout(3000)
        #elif datadictvalue["C_TRGT"] != "Action Target Approval Date":
            #page.locator("//span[text()='Action Target Approval Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Action Target Completion Date":
            page.locator("//span[text()='Action Target Completion Date']//following::input[1]").clear()
            page.locator("//span[text()='Action Target Completion Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(3000)
        #elif datadictvalue["C_TRGT"] != "Action Target Completion Date":
            #page.locator("//span[text()='Action Target Completion Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Action Target Review Date":
            page.locator("//span[text()='Action Target Review Date']//following::input[1]").clear()
            page.locator("//span[text()='Action Target Review Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(3000)
        #elif datadictvalue["C_TRGT"] != "Action Target Review Date":
            #page.locator("//span[text()='Action Target Review Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Action Target Preapproval Date":
            page.locator("//span[text()='Action Target Preapproval Date']//following::input[1]").clear()
            page.locator("//span[text()='Action Target Preapproval Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(3000)
        #elif datadictvalue["C_TRGT"] != "Action Target Preapproval Date":
            #page.locator("//span[text()='Action Target Preapproval Date']//following::input[1]").press("Tab")


        if datadictvalue["C_TRGT"] == "Incident Target Approval Date":
            page.locator("//span[text()='Incident Target Approval Date']//following::input[1]").clear()
            page.locator("//span[text()='Incident Target Approval Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(3000)
        #elif datadictvalue["C_TRGT"] != "Incident Target Approval Date":
            #page.locator("//span[text()='Incident Target Approval Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Incident Target Completion Date":
            page.locator("//span[text()='Incident Target Completion Date']//following::input[1]").clear()
            page.locator("//span[text()='Incident Target Completion Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
        #elif datadictvalue["C_TRGT"] != "Incident Target Completion Date":
            #page.locator("//span[text()='Incident Target Completion Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Incident Target Review Date":
            page.locator("//span[text()='Incident Target Review Date']//following::input[1]").clear()
            page.locator("//span[text()='Incident Target Review Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
        #elif datadictvalue["C_TRGT"] != "Incident Target Review Date":
            #page.locator("//span[text()='Incident Target Review Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Investigation Target Approval Date":
            page.locator("//span[text()='Investigation Target Approval Date']//following::input[1]").clear()
            page.locator("//span[text()='Investigation Target Approval Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(4000)
        #elif datadictvalue["C_TRGT"] != "Investigation Target Approval Date":
            #page.locator("//span[text()='Investigation Target Approval Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Investigation Target Review Date":
            page.locator("//span[text()='Investigation Target Review Date']//following::input[1]").clear()
            page.locator("//span[text()='Investigation Target Review Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(4000)
        #elif datadictvalue["C_TRGT"] != "Investigation Target Review Date":
            #page.locator("//span[text()='Investigation Target Review Date']//following::input[1]").press("Tab")

        page.mouse.wheel(0,100)

        if datadictvalue["C_TRGT"] == "Investigation Target Preapproval Date":
            page.locator("//span[text()='Investigation Target Preapproval Date']//following::input[1]").clear()
            page.locator("//span[text()='Investigation Target Preapproval Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(4000)
        #elif datadictvalue["C_TRGT"] != "Investigation Target Preapproval Date":
            #page.locator("//span[text()='Investigation Target Preapproval Date']//following::input[1]").press("Tab")


        if datadictvalue["C_TRGT"] == "Investigation Target Completion Date":
            page.locator("//span[text()='Investigation Target Completion Date']//following::input[1]").clear()
            page.locator("//span[text()='Investigation Target Completion Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(4000)
        #elif datadictvalue["C_TRGT"] != "Investigation Target Completion Date":
            #page.locator("//span[text()='Investigation Target Completion Date']//following::input[1]").press("Tab")

        if datadictvalue["C_TRGT"] == "Incident Event Target Completion Date":
            page.locator("//span[text()='Incident Event Target Completion Date']//following::input[1]").clear()
            page.locator("//span[text()='Incident Event Target Completion Date']//following::input[1]").type(str(datadictvalue["C_CLNT_VLS"]))
            #page.wait_for_timeout(4000)
        #elif datadictvalue["C_TRGT"] != "Incident Event Target Completion Date":
            #page.locator("//span[text()='Incident Event Target Completion Date']//following::input[1]").press("Tab")


        i = i + 1

    # Save and Close
    page.get_by_role("button", name="Save and Close").click()
    page.wait_for_timeout(3000)

    try:
        expect(page.get_by_role("heading", name="Search")).to_be_visible()
        print("Target Dates Saved Successfully")
        datadictvalue["RowStatus"] = "Target Dates Saved Successfully"
    except Exception as e:
        print("Target Dates not saved")
        datadictvalue["RowStatus"] = "Target Dates not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HEAL_SAF_CONFIG_WRKBK, TARGET_DATE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HEAL_SAF_CONFIG_WRKBK, TARGET_DATE, PRCS_DIR_PATH + HEAL_SAF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HEAL_SAF_CONFIG_WRKBK, TARGET_DATE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", HEAL_SAF_CONFIG_WRKBK)[0] + "_" + TARGET_DATE)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", HEAL_SAF_CONFIG_WRKBK)[0] + "_" + TARGET_DATE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
