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
        if datadictvalue["C_STTC_DYNMC"] == 'Static':
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_STTC_DYNMC"], exact=True).click()
            if datadictvalue["C_ADVNCD_OPTNS"] == 'Yes':
                page.get_by_text("Advanced Options").check()
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Continue").click()
                page.wait_for_timeout(2000)
            if datadictvalue["C_ADVNCD_OPTNS"] == 'Yes':
                #if not page.get_by_text("Advanced Options").is_checked():
                page.get_by_text("Advanced Options").check()
            if datadictvalue["C_ADVNCD_OPTNS"] == 'No':
                #if page.get_by_text("Advanced Options").is_checked():
                page.get_by_text("Advanced Options").uncheck()
                page.wait_for_timeout(3000)

            #Select Continue to enter more details
                page.get_by_role("button", name="Continue").click()
                page.wait_for_timeout(2000)

        #Select Start Date
            page.locator("//label[text()='Start Date']//following::input[1]").clear()
            page.locator("//label[text()='Start Date']//following::input[1]").fill(datadictvalue["C_START_DATE"])

        #Select End Date
            page.locator("//label[text()='End Date']//following::input[1]").clear()
            page.locator("//label[text()='End Date']//following::input[1]").fill(datadictvalue["C_END_DATE"])

        #Enter Description
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(3000)

            if datadictvalue["C_OBJCT_PYRLL_NAME"] == 'N/A' or '':
                page.get_by_role("button", name="Next").click()

            #Select value for Payroll Process
            elif datadictvalue["C_OBJCT_PYRLL_NAME"] != 'N/A' or '':
                page.get_by_role("link", name="Value").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Object Group Parameters").click()
                page.get_by_label("Object Group Parameters").fill(datadictvalue["C_OBJCT_PYRLL_NAME"])
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name=datadictvalue["C_OBJCT_PYRLL_NAME"], exact=True).click()
                page.get_by_role("button", name="Next").click()

             #Select value for Payroll Definition
            if datadictvalue["C_PYRLL_DFNTN_PYRLL"] != 'N/A' or '':
                page.locator("//h1[text()='Payroll Definition']//following::img[@title='Add'][1]").click()
                page.wait_for_timeout(2000)
                page.get_by_role("link", name="Value").click()
                page.get_by_label("Payroll", exact=True).click()
                page.get_by_label("Payroll", exact=True).fill(datadictvalue["C_PYRLL_DFNTN_PYRLL"])
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name=datadictvalue["C_PYRLL_DFNTN_PYRLL"]).click()
                page.wait_for_timeout(2000)

            # Select value for Payroll Statutory Unit
            if datadictvalue["C_PYRLL_STTTRY_UNIT"] != 'N/A' or '':
                page.locator("//h1[text()='Payroll Statutory Unit']//following::img[@title='Add'][1]").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name="Payroll Statutory Unit").get_by_role("link").click()
                page.get_by_label("Payroll Statutory Unit", exact=True).click()
                page.get_by_label("Payroll Statutory Unit", exact=True).fill(datadictvalue["C_PYRLL_STTTRY_UNIT"])
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name=datadictvalue["C_PYRLL_STTTRY_UNIT"]).click()
                page.wait_for_timeout(2000)

            # Select value for Tax Reporting Unit
            if datadictvalue["C_TAX_RPRTNG_UNIT"] != 'N/A' or '':
                page.locator("//h1[text()='Tax Reporting Unit']//following::img[@title='Add'][1]").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name="Tax Reporting Unit").get_by_role("link").click()
                page.get_by_label("Tax Reporting Unit", exact=True).click()
                page.get_by_label("Tax Reporting Unit", exact=True).fill(datadictvalue["C_TAX_RPRTNG_UNIT"])
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name=datadictvalue["C_TAX_RPRTNG_UNIT"]).click()
                page.wait_for_timeout(2000)

            # Select value for Payroll Relationship
            if datadictvalue["C_PYRLL_RLTNSHP_NMBR"] != 'N/A' or '':
                page.locator("//h1[text()='Payroll Relationship']//following::img[@title='Add'][1]").click()
                page.wait_for_timeout(4000)
                page.get_by_role("table", name="Payroll Relationship").get_by_role("link").click()
                page.wait_for_timeout(3000)
                page.get_by_label("Payroll Relationship Number").click()
                page.wait_for_timeout(3000)
                page.get_by_label("Payroll Relationship Number").type(str(datadictvalue["C_PYRLL_RLTNSHP_NMBR"]))
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name=datadictvalue["C_PYRLL_RLTNSHP_NMBR"]).click()
                page.locator("//div[@title='Payroll Relationship']//following::input[@value='Include']").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYRLL_RLTNSHP_INCLSN_STTS"]).click()
                page.wait_for_timeout(2000)


            # Select value for Payroll Term
            if datadictvalue["C_EMPLYMNT_TRMS_NMBR"] != 'N/A' or '':
                page.locator("//h1[text()='Payroll Term Rules']//following::img[@title='Add'][1]").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name="Payroll Term").get_by_role("link").click()
                page.get_by_label("Employment Terms Number").click()
                page.get_by_label("Employment Terms Number").fill(datadictvalue["C_EMPLYMNT_TRMS_NMBR"])
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name=datadictvalue["C_EMPLYMNT_TRMS_NMBR"]).click()
                page.wait_for_timeout(2000)


            # Select value for Payroll Assignment
            if datadictvalue["C_PYRLL_ASSGMNT_NMBR"] != 'N/A' or '':
                page.locator("//h1[text()='Payroll Assignment']//following::img[@title='Add'][1]").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name="Payroll Assignment").get_by_role("link").click()
                page.get_by_label("Assignment Number").click()
                page.get_by_label("Assignment Number").fill(datadictvalue["C_PYRLL_ASSGMNT_NMBR"])
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name=datadictvalue["C_PYRLL_ASSGMNT_NMBR"]).click()
                page.locator("//div[@title='Payroll Term']//following::input[@value='Include']").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYRLL_ASSGMNT_NMBR_INCLSN_STTS"]).click()
                page.wait_for_timeout(2000)

        # Select Static or Dynamic
        if datadictvalue["C_STTC_DYNMC"] == 'Dynamic':
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_STTC_DYNMC"], exact=True).click()
            if datadictvalue["C_ADVNCD_OPTNS"] == 'Yes':
                page.get_by_text("Advanced Options").check()
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Continue").click()
                page.wait_for_timeout(2000)
            if datadictvalue["C_ADVNCD_OPTNS"] == 'Yes':
                # if not page.get_by_text("Advanced Options").is_checked():
                page.get_by_text("Advanced Options").check()
            if datadictvalue["C_ADVNCD_OPTNS"] == 'No':
                # if page.get_by_text("Advanced Options").is_checked():
                page.get_by_text("Advanced Options").uncheck()
                page.wait_for_timeout(3000)

            # Select Continue to enter more details
                page.get_by_role("button", name="Continue").click()
                page.wait_for_timeout(2000)

            # Select Start Date
            page.locator("//label[text()='Start Date']//following::input[1]").click()
            page.locator("//label[text()='Start Date']//following::input[1]").fill(datadictvalue["C_START_DATE"])

            # Select End Date
            page.locator("//label[text()='End Date']//following::input[1]").clear()
            page.locator("//label[text()='End Date']//following::input[1]").fill(datadictvalue["C_END_DATE"])

            # Enter Description
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(4000)

            # Select value for Object Parameter
            if datadictvalue["C_OBJCT_PYRLL_NAME"] != 'N/A' or '':
                page.get_by_role("link", name="Value").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Object Group Parameters").click()
                page.get_by_label("Object Group Parameters").fill(datadictvalue["C_OBJCT_PYRLL_NAME"])
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name=datadictvalue["C_OBJCT_PYRLL_NAME"], exact=True).click()
                page.wait_for_timeout(3000)

            # Select value for Payroll Relationship Rules
            if datadictvalue["C_PYRLL_RLTNSHP_RULES"] != 'N/A' or '':
                page.locator("//h1[text()='Payroll Relationship Rules']//following::img[@title='Add'][1]").click()
                page.locator("//div[@title='Payroll Relationship Rules']//following::input[@role='combobox']").click()
                page.wait_for_timeout(3000)
                page.get_by_role("cell", name="Search Autocompletes on TAB").locator("a").click()
                page.get_by_role("link", name="Search...").click()
                #page.get_by_role("table", name="Payroll Relationship Rules").get_by_role("link").click()
                page.get_by_label("Formula Name").click()
                page.get_by_label("Formula Name").fill(datadictvalue["C_PYRLL_RLTNSHP_RULES"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYRLL_RLTNSHP_RULES"]).click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Next").click()

            #Select value for Payroll Term Rules
            if datadictvalue["C_PYRLL_TERM_RULES"] != 'N/A' or '':
                page.locator("//h1[text()='Payroll Term Rules']//following::img[@title='Add'][1]").click()
                page.wait_for_timeout(2000)
                page.locator("//div[@title='Payroll Term Rules']//following::input[@role='combobox']").click()
                page.get_by_role("table", name="Payroll Term Rules").locator("a").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Formula Name").click()
                page.get_by_label("Formula Name").fill(datadictvalue["C_PYRLL_TERM_RULES"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYRLL_TERM_RULES"]).click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Next").click()

            # Select value for Payroll Assignment Rules
            if datadictvalue["C_PYRLL_ASSGNMNT_RULES"] != 'N/A' or '':
                page.locator("//h1[text()='Payroll Assignment Rules']//following::img[@title='Add'][1]").click()
                page.wait_for_timeout(2000)
                page.locator("//div[@title='Payroll Assignment Rules']//following::input[@role='combobox']").click()
                page.get_by_role("table", name="Payroll Assignment Rules").locator("a").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Formula Name").click()
                page.get_by_label("Formula Name").fill(datadictvalue["C_PYRLL_ASSGNMNT_RULES"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PYRLL_ASSGNMNT_RULES"]).click()
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Next").click()

        # Select value for Payroll Statutory Unit
            if datadictvalue["C_PYRLL_STTTRY_UNIT"] != 'N/A' or '':
                page.locator("//h1[text()='Payroll Statutory Unit']//following::img[@title='Add'][1]").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name="Payroll Statutory Unit").get_by_role("link").click()
                page.get_by_label("Payroll Statutory Unit", exact=True).click()
                page.get_by_label("Payroll Statutory Unit", exact=True).fill(datadictvalue["C_PYRLL_STTTRY_UNIT"])
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name=datadictvalue["C_PYRLL_STTTRY_UNIT"]).click()
                page.wait_for_timeout(2000)

            # Select value for Tax Reporting Unit
            if datadictvalue["C_TAX_RPRTNG_UNIT"] != 'N/A' or '':
                page.locator("//h1[text()='Tax Reporting Unit']//following::img[@title='Add'][1]").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name="Tax Reporting Unit").get_by_role("link").click()
                page.get_by_label("Tax Reporting Unit", exact=True).click()
                page.get_by_label("Tax Reporting Unit", exact=True).fill(datadictvalue["C_TAX_RPRTNG_UNIT"])
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name=datadictvalue["C_TAX_RPRTNG_UNIT"]).click()
                page.wait_for_timeout(2000)

            # Select value for Payroll Term
            if datadictvalue["C_EMPLYMNT_TRMS_NMBR"] != 'N/A' or '':
                page.locator("//h1[text()='Payroll Term']//following::img[@title='Add'][1]").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name="Payroll Term").get_by_role("link").click()
                page.get_by_label("Employment Terms Number").click()
                page.get_by_label("Employment Terms Number").fill(datadictvalue["C_EMPLYMNT_TRMS_NMBR"])
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name=datadictvalue["C_EMPLYMNT_TRMS_NMBR"]).click()
                page.locator("//div[@title='Payroll Term']//following::input[@value='Include']").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_EMPLYMNT_TRMS_INCLSN_STTS"]).click()
                page.wait_for_timeout(2000)

            # Select value for Payroll Assignment
            if datadictvalue["C_PYRLL_ASSGMNT_NMBR"] != 'N/A' or '':
                page.locator("//h1[text()='Payroll Assignment']//following::img[@title='Add'][1]").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name="Payroll Assignment").get_by_role("link").click()
                page.get_by_label("Assignment Number").click()
                page.get_by_label("Assignment Number").fill(datadictvalue["C_PYRLL_ASSGMNT_NMBR"])
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name=datadictvalue["C_PYRLL_ASSGMNT_NMBR"]).click()
                page.wait_for_timeout(2000)

        #page.get_by_role("button", name="Cancel").click()
        page.get_by_role("button", name="Save").click()
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(2000)

        i = i + 1
        # Validation
        try:
            expect(page.get_by_role("heading", name="Object Groups")).to_be_visible()
            print("Object Group Elements Created Successfully")

        except Exception as e:
            print("Object Group Creation Elements UnSuccessfull")


    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_PAY_R):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_PAY_R, PRCS_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_OBJ_GRP_CONFIG_WRKBK, DST_OBJ_GRP_PAY_R)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_OBJ_GRP_CONFIG_WRKBK)[0] + "_" +DST_OBJ_GRP_PAY_R )
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_OBJ_GRP_CONFIG_WRKBK)[0] + "_" +DST_OBJ_GRP_PAY_R + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))