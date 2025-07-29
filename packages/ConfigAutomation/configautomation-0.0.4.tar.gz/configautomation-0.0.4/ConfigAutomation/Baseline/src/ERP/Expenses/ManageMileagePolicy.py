from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
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
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Policies By Expense Category")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Policies By Expense Category").click()


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Create Mileage Policy

        page.get_by_title("Create Policy").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text("Mileage", exact=True).click()
        page.wait_for_timeout(5000)
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Country").select_option(datadictvalue["C_CNTRY"])

        if datadictvalue["C_MLTPL_CRRNCY"] == 'Yes':
            page.get_by_text("Multiple currencies").click()
        elif datadictvalue["C_MLTPL_CRRNCY"] == 'No':
            page.get_by_text("Single currency").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Currency", exact=True).select_option(datadictvalue["C_SNGL_CRRNCY"])
            page.wait_for_timeout(1000)
            page.get_by_label("Unit of Measure").select_option(datadictvalue["C_UNIT_OF_MSR"])

        # Mileage Eligibility Rules
        if datadictvalue["C_STNDRD_MLG_DDCTN"] == 'Yes':
            page.get_by_label("Distance Deduction").fill(datadictvalue["C_DSTNC_DDCTN"])
        if datadictvalue["C_MNMM_DSTNC_FOR_MLG_ELGBLTY"] == 'Yes':
            page.get_by_text("Minimum distance for mileage").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Minimum Distance", exact=True).fill(str(datadictvalue["C_MNMM_DSTNC"]))

        # Mileage Rate Determinants
        if datadictvalue["C_ROLE"] == 'Yes' :
            page.get_by_text("Role", exact=True).click()
            page.get_by_label("Role Type").select_option(datadictvalue["C_ROLE_TYPE"])

        # Location
        if datadictvalue["C_LCTN"] == 'Yes ':
            page.get_by_text("Location", exact=True).click()
            if datadictvalue["C_GGRPHCL_LCTNS"] == 'Yes' :
                page.get_by_text("Geographical locations").click()
            if datadictvalue["C_ZONE"] == 'Yes':
                page.get_by_text("Zone", exact=True).click()

        #Distance Threshold
        if datadictvalue["C_THRSHLD_PRD"] == 'Yes' :
            page.get_by_text("Distance threshold").click()
            if datadictvalue["CC_BY_TRIP_BY_PRD"] == 'By trip' :
                page.get_by_text("By trip", exact=True).click()
            if datadictvalue["CC_BY_TRIP_BY_PRD"] == 'By period' :
                page.get_by_text("By trip", exact=True).click()

        #Vehicle Category , Vehicle Type , Fuel Type
        if datadictvalue["C_VHCL_CTGRY"] == 'Yes':
            page.get_by_role("cell", name="Vehicle Category", exact=True).click()
            page.locator("//label[text()='Vehicle Category']//following::select[1]").select_option(datadictvalue("C_VHCL_SRC"))
        if datadictvalue["C_VHCL_TYPE"] == 'Yes':
            page.get_by_role("cell", name="Vehicle Type", exact=True).locator("label").click()
            page.locator("//label[text()='Vehicle Type']//following::select[1]").select_option(datadictvalue["C_VHCL_TYPE_SRC"])
        if datadictvalue["C_FUEL_TYPE"] == 'Yes' :
            page.get_by_role("cell", name="Fuel Type", exact=True).locator("label").click()
            page.locator("//label[text()='Fuel Type']//following::select[1]").select_option(datadictvalue["C_FUEL_TYPE_SRC"])

        #Add on Rates
        if datadictvalue["C_ENBL_PSSNGR_RATE"] == 'Yes':
            page.get_by_text("Enable passenger rate").click()

        if datadictvalue["C_CPTR_PSSNGR_NAME"] == 'Yes':
            page.get_by_text("Capture passenger name").click()

        if datadictvalue["C_CLCLT_PSSNGR_RATE_BY_DSTNC_TRVLD_BY_PSSNGR"] == 'Yes':
            page.get_by_text("Calculate passenger rate by").click()

        if datadictvalue["C_RSTRCT_NMBR_OF_PSSNGRS_RMBRSD"] == 'Yes':
            page.get_by_text("Restrict number of passengers").click()
            page.get_by_label("Maximum Number of Passengers").fill(datadictvalue["C_MXMM_NMBR_OF_PSSNGRS"])

        if datadictvalue["C_ENBL_CMPNY_SPCFC_RATES"] == 'Yes':
            page.get_by_role("cell", name="Enable company-specific rates", exact=True).click()
            page.get_by_label("Rate Type").select_option(datadictvalue["C_RATE_TYPE"])
        # page.get_by_role("button", name="Cancel").click()
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)

        # Create Rates
        if datadictvalue["C_RATE"] != '':
            page.get_by_role("button", name="Create Rates").click()
            page.wait_for_timeout(2000)
            page.get_by_role("table", name='Edit Rates').get_by_role("row").nth(0).get_by_label("Mileage Rate", exact=True).fill(str(datadictvalue["C_RATE"]))
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar Start Date Select Date", exact=True).locator("input").nth(0).fill(datadictvalue["C_START_DATE"].strftime("%m/%d/%Y"))
            page.get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_START_DATE"].strftime("%m/%d/%Y"))
            if datadictvalue["C_END_DATE"] != '':
                page.get_by_placeholder("m/d/yy").nth(0).fill(datadictvalue["C_END_DATE"].strftime("%m/%d/%Y"))
            page.wait_for_timeout(1000)
            page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(2000)

        page.get_by_role("button", name="Save and Close").click()


        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        #Validation

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Expense Mileage Policy Saved Successfully")

        except Exception as e:
            print("Expense Mileage Policy not Saved")



        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, MILEAGE_POLICY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, MILEAGE_POLICY, PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, MILEAGE_POLICY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[0] + "_" + MILEAGE_POLICY)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + MILEAGE_POLICY + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))