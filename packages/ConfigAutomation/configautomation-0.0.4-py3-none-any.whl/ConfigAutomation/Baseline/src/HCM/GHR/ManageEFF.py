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
    page.get_by_role("textbox").fill("Manage Extensible Flexfields")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Extensible Flexfields").first.click()

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        page.wait_for_timeout(3000)
        if datadictvalue["C_CNTXT_DSPLY_NAME"] != PrevName:
            if i > 0:

                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(2000)

                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(2000)

                page.locator("//a[@title='Expand']//following::span[1]").click()
                page.wait_for_timeout(5000)
                page.get_by_role("button", name="Select and Add").click()
                page.wait_for_timeout(3000)
                page.locator("//div[text()='Select and Add: Contexts']//following::label[text()='Name']//following::input[1]").clear()
                page.locator("//div[text()='Select and Add: Contexts']//following::label[text()='Name']//following::input[1]").type(PrevName)
                page.get_by_role("button", name="Search", exact=True).click()
                page.wait_for_timeout(3000)
                page.get_by_text(PrevName).first.click()
                page.get_by_role("button", name="Apply").click()
                page.get_by_role("button", name="OK").click()

                page.wait_for_timeout(3000)

                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(2000)
                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("Extensible FlexField Saved")
                    datadict[i - 1]["RowStatus"] = "Extensible FlexField Saved"
                except Exception as e:
                    print("Unable to save Extensible FlexField")
                    datadict[i - 1]["RowStatus"] = "Unable to save Extensible FlexField"

                page.wait_for_timeout(3000)
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_FLXFLD_NAME"])
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Search", exact=True).click()

            page.get_by_role("cell", name=datadictvalue["C_FLXFLD_NAME"], exact=True).click()
            page.get_by_role("button", name="Edit").click()
            page.wait_for_timeout(2000)

            page.get_by_role("button", name="Manage Contexts").click()
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Display Name").click()
            page.get_by_label("Display Name").fill(datadictvalue["C_CNTXT_DSPLY_NAME"])
            page.get_by_label("Behavior").click()
            page.get_by_label("Behavior").select_option(datadictvalue["C_BHVR"])
            page.get_by_label("Code", exact=True).clear()
            page.get_by_label("Code", exact=True).type(datadictvalue["C_CNTXT_CODE"])
            page.get_by_label("API name").click()
            page.wait_for_timeout(2000)
            # page.get_by_label("API name").type(datadictvalue["C_CONTXT_API_NAME"])

            page.get_by_role("button", name="Create").nth(1).click()
            page.get_by_label("FlexfieldUsageCode").click()
            page.get_by_label("FlexfieldUsageCode").select_option(datadictvalue["C_CNTXT_USAGE_NAME"])
            page.get_by_role("button", name="Save", exact=True).click()
            page.wait_for_timeout(2000)

            PrevName = datadictvalue["C_CNTXT_DSPLY_NAME"]

        page.get_by_role("button", name="Create").first.click()
        page.wait_for_timeout(3000)
        page.get_by_label("Name", exact=True).click()
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
        page.get_by_label("Description", exact=True).click()
        page.get_by_label("Description", exact=True).fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Data Type").select_option(datadictvalue["C_DATA_TYPE"])
        page.get_by_title("Search: Table Column").click()
        page.get_by_role("cell", name=datadictvalue["C_TABLE_CLMN"], exact=True).click()
        page.wait_for_timeout(5000)

        page.get_by_label("Value Set").fill(datadictvalue["C_VALUE_SET"])
        page.get_by_label("Range Type").select_option(datadictvalue["C_RANGE_TYPE"])

        if datadictvalue["C_DFLT_TYPE"] == 'Constant':
            page.get_by_label("Default Type").click()
            page.get_by_label("Default Type").select_option(datadictvalue["C_DFLT_TYPE"])
            page.get_by_label("Default Value").fill(datadictvalue["C_DFLT_VALUE"])

        if datadictvalue["C_RQRD"] == 'Yes':
            page.get_by_text("Required").check()

        elif datadictvalue["C_RQRD"] == 'No' or '':
            page.get_by_text("Required").uncheck()


        page.get_by_label("Prompt").fill(datadictvalue["C_PRMPT"])
        page.get_by_label("Display Type").select_option(datadictvalue["C_DSPLY_TYPE"])

        page.get_by_label("Display Size").click()
        page.get_by_label("Display Size").fill(str(datadictvalue["C_DSPLY_SIZE"]))
        page.get_by_label("Display Height").click()
        page.get_by_label("Display Height").fill(str(datadictvalue["C_DSPLY_HGHT"]))
        page.get_by_label("Definition Help Text").click()
        page.get_by_label("Definition Help Text").fill(datadictvalue["C_DFNTN_HELP_TEXT"])
        page.get_by_label("Instruction Help Text").click()
        page.get_by_label("Instruction Help Text").fill(datadictvalue["C_INSTRCTN_HELP_TEXT"])

        if datadictvalue["C_DSPLY_TYPE"] == 'Check Box':
            page.get_by_label("Checked Value", exact=True).fill(datadictvalue["C_CHCKD_VALUE"])
            page.get_by_label("Unchecked Value").click()
            page.get_by_label("Unchecked Value").fill(datadictvalue["C_UNCHCKD-VALUE"])

        if datadictvalue["C_READ_ONLY"] == 'Yes':
            page.get_by_text("Read-only").check()

        elif datadictvalue["C_READ_ONLY"] == 'No' or '':
            page.get_by_text("Read-only").uncheck()

        if datadictvalue["C_BI_ENBLD"] == 'Yes':
            page.get_by_text("BI Enabled").click()

        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        page.pause()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1
        if i == rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)

            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)

            page.locator("//a[@title='Expand']//following::span[1]").click()
            page.wait_for_timeout(5000)
            page.get_by_role("button", name="Select and Add").click()
            page.wait_for_timeout(3000)
            page.locator("//div[text()='Select and Add: Contexts']//following::label[text()='Name']//following::input[1]").clear()
            page.locator("//div[text()='Select and Add: Contexts']//following::label[text()='Name']//following::input[1]").type(datadictvalue["C_CNTXT_DSPLY_NAME"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_CNTXT_DSPLY_NAME"]).first.click()
            page.get_by_role("button", name="Apply").click()
            page.get_by_role("button", name="OK").click()

            page.wait_for_timeout(3000)
    
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Done").click()

    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Extensible FlexFields Saved Successfully")
        datadictvalue["RowStatus"] = "Extensible FlexField are added successfully"

    except Exception as e:
        print("Extensible FlexFields not saved")
        datadictvalue["RowStatus"] = "Extensible FlexField not added"

    page.wait_for_timeout(2000)
    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_EFF):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_EFF, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_EFF)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + MANAGE_EFF)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + MANAGE_EFF + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
