from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    #Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    #Navigate to Object Group
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="My Client Groups").click()
    page.get_by_role("link", name="Payroll").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Object Groups").click()
    page.wait_for_timeout(2000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        # Select Legislative data group
        page.get_by_role("combobox", name="Legislative Data Group").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTV_DATA_GROUP"], exact=True).click()
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(2000)

        # Create Object Group
        page.get_by_role("button", name="Create").click()

        #Fill name
        page.locator("//div[text()='Create Object Group']//following::label[text()='Name']//following::input[1]").clear()
        page.locator("//div[text()='Create Object Group']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_NAME"])

        #Select type as Deduction Card Group
        page.locator("//div[text()='Create Object Group']//following::label[text()='Legislative Data Group']//following::input[1]").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TYPE"]).click()
        page.wait_for_timeout(3000)

        #Select Static or Dynamic
        if datadictvalue["C_STTC_DYNMC"] == 'Dynamic':
            page.locator("[id=\"__af_Z_window\"]").get_by_text("Dynamic", exact=True).click()
        else:
            page.locator("[id=\"__af_Z_window\"]").get_by_text("Static", exact=True).click()

        #Select Continue to enter more details
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(5000)

        #Select Start Date
        page.locator("//label[text()='Start Date']//following::input[1]").clear()
        page.locator("//label[text()='Start Date']//following::input[1]").fill(datadictvalue["C_START_DATE"])

        #Select End Date
        page.locator("//label[text()='End Date']//following::input[1]").clear()
        page.locator("//label[text()='End Date']//following::input[1]").fill(datadictvalue["C_END_DATE"])

        #Enter Description
        page.get_by_label("Description").clear()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        #Select value for Payroll Process
        if datadictvalue["C_OBJCT_PYRLL_PRCSS"] != 'N/A' or '':
            page.get_by_role("cell", name="Payroll Process Value").get_by_role("link").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Object Group Parameters").click()
            page.get_by_label("Object Group Parameters").fill(datadictvalue["C_OBJCT_PYRLL_PRCSS"])
            page.get_by_role("button", name="Search").click()
            page.get_by_text(datadictvalue["C_OBJCT_PYRLL_PRCSS"]).nth(0).click()
            page.wait_for_timeout(2000)

        #Select value for Tax Reporting Unit
        if datadictvalue["C_OBJCT_TAX_RPRTNG_UNIT"] != 'N/A' or '':
            page.get_by_role("cell", name="Tax Reporting Unit Value").get_by_role("link").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Object Group Parameters").click()
            page.get_by_label("Object Group Parameters").fill(datadictvalue["C_OBJCT_TAX_RPRTNG_UNIT"])
            page.get_by_role("button", name="Search").click()
            page.get_by_text(datadictvalue["C_OBJCT_TAX_RPRTNG_UNIT"]).nth(0).click()
            page.wait_for_timeout(2000)


        #Select value for Payroll Statutory Unit
        if datadictvalue["C_OBJCT_PYRLL_STTTRY_UNIT"] != 'N/A' or '':
            page.get_by_role("cell", name="Payroll Statutory Unit Value").get_by_role("link").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Object Group Parameters").click()
            page.get_by_label("Object Group Parameters").fill(datadictvalue["C_OBJCT_PYRLL_STTTRY_UNIT"])
            page.get_by_role("button", name="Search").click()
            page.get_by_text(datadictvalue["C_OBJCT_PYRLL_STTTRY_UNIT"]).nth(0).click()
            page.wait_for_timeout(2000)


        #Select value for Tax Code Suffix
        if datadictvalue["C_OBJCT_TAX_CODE_SFFX"] != 'N/A' or '':
            page.get_by_role("cell", name="Tax Code Suffix Value").get_by_role("link").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Object Group Parameters").click()
            page.get_by_label("Object Group Parameters").fill(datadictvalue["C_OBJCT_TAX_CODE_SFFX"])
            page.get_by_role("button", name="Search").click()
            page.get_by_role("link", name=str(datadictvalue["C_OBJCT_TAX_CODE_SFFX"]), exact=True).click()
            page.wait_for_timeout(2000)

        #Select value for Component Flexfield Context
        if datadictvalue["C_OBJCT_CMPNNT_FLXFLD_CNTXT"] != 'N/A' or '':
            page.get_by_role("cell", name="Component Flexfield Context Value").get_by_role("link").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Object Group Parameters").click()
            page.get_by_label("Object Group Parameters").fill(datadictvalue["C_OBJCT_CMPNNT_FLXFLD_CNTXT"])
            page.get_by_role("button", name="Search").click()
            page.get_by_role("link", name=datadictvalue["C_OBJCT_CMPNNT_FLXFLD_CNTXT"]).click()
            page.wait_for_timeout(2000)

        #Select value for Card Component Definition
        if datadictvalue["C_OBJCT_CMPNNT_DFNTN"] != 'N/A' or '':
            page.get_by_role("cell", name="Card Component Definition Value").get_by_role("link").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Object Group Parameters").click()
            page.get_by_label("Object Group Parameters").fill(datadictvalue["C_OBJCT_CMPNNT_DFNTN"])
            page.get_by_role("button", name="Search").click()
            page.get_by_role("link", name=datadictvalue["C_OBJCT_CMPNNT_DFNTN"]).click()
            page.wait_for_timeout(2000)

        #Add Deduction Card Component
        if datadictvalue["C_DDCTN_CARD_CMPNNT_RULES"] != 'N/A' or '':
            page.get_by_role("button", name="Add").first.click()
            page.wait_for_timeout(1000)
            page.get_by_role("table", name="Deduction Card Component Rules").locator("a").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Formula Name").click()
            page.get_by_label("Formula Name").fill(datadictvalue["C_DDCTN_CARD_CMPNNT_RULES"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(1000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DDCTN_CARD_CMPNNT_RULES"]).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        #Add Deduction Component Detail
        if datadictvalue["C_DDCTN_CMPNNT_DTL_RULES"] != 'N/A' or '':
            page.get_by_role("button", name="Add").nth(1).click()
            page.wait_for_timeout(1000)
            page.get_by_role("table", name="Deduction Component Detail").locator("a").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Formula Name").click()
            page.get_by_label("Formula Name").fill(datadictvalue["C_DDCTN_CMPNNT_DTL_RULES"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(1000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DDCTN_CMPNNT_DTL_RULES"]).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        #Add Pension Component Detail
        if datadictvalue["C_PNSN_CMPNNT_DTL_RULES"] != 'N/A' or '':
            page.get_by_role("button", name="Add").nth(2).click()
            page.wait_for_timeout(1000)
            page.get_by_role("table", name="Pension Component Detail Rules").locator("a").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Formula Name").click()
            page.get_by_label("Formula Name").fill(datadictvalue["C_PNSN_CMPNNT_DTL_RULES"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(1000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PNSN_CMPNNT_DTL_RULES"]).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        #Go to Next page to enter more details
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(2000)

        #Deduction Card Component
        if datadictvalue["C_DDCTN_DSPLY_VALUE"] != 'N/A' or '':
            page.get_by_role("button", name="Add").first.click()
            page.wait_for_timeout(2000)
            page.get_by_role("table", name="Deduction Card Component").get_by_role("link").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_Name_On"])
            page.get_by_role("button", name="Search").click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name=datadictvalue["C_DDCTN_DSPLY_VALUE"]).click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Inclusion Status").click()
            page.get_by_text(datadictvalue["C_DDCTN_INCLSN_STTS"]).click()

        #Deduction Component Detail
        if datadictvalue["C_DDCTN_CMPNNT_DSPLY_VALUE"] != 'N/A' or '':
            page.get_by_role("button", name="Add").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_role("table", name="Deduction Component Detail").get_by_role("link").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_Name_Tw"])
            page.get_by_role("button", name="Search").click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name=datadictvalue["C_DDCTN_CMPNNT_DSPLY_VALUE"]).click()
            page.get_by_role("table", name="Deduction Component Detail").get_by_role("combobox").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DDCTN_CMPNNT_INCLSN_STTS"]).click()

        #Pension Component Detail
        if datadictvalue["C_PNSN_CMPNNT_DSPLY_VALUE"] != 'N/A' or '':
            page.get_by_role("button", name="Add").nth(2).click()
            page.wait_for_timeout(2000)
            page.get_by_role("table", name="Pension Component Detail").get_by_role("link").click()
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_Name_Th"])
            page.get_by_role("button", name="Search").click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name=datadictvalue["C_PNSN_CMPNNT_DSPLY_VALUE"]).click()
            page.get_by_role("table", name="Pension Component Detail").get_by_role("combobox").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PNSN_INCLSN_STTS"]).click()

        #Submit to create an object
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(1000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

    # Validation
    try:
        expect(page.get_by_role("heading", name="Object Groups")).to_be_visible()
        print("Object Group Created Successfully")

    except Exception as e:
        print("Object Group Creation UnSuccessfull")

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_DED):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_DED, PRCS_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_DED)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_OBJ_GRP_CONFIG_WRKBK)[0] + "_" +DST_OBJ_GRP_DED)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_OBJ_GRP_CONFIG_WRKBK)[0] + "_" +DST_OBJ_GRP_DED + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))