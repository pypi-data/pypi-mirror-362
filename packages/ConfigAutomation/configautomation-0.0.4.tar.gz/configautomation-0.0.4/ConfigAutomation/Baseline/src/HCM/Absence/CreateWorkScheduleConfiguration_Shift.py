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

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(40000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Work Shifts")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Work Shifts", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        # Create Shift with Time Shift
        if datadictvalue["C_CRT_SHIFT"]=='Create Time Shift':
            #page.get_by_role("cell", name="Create Shift", exact=True).locator("a").click()
            #page.get_by_role("link", name="Create Time Shift").click()
            page.get_by_title("Create Shift").nth(2).click()
            page.get_by_role("link", name="Create Time Shift").click()
            page.wait_for_timeout(3000)

            # Name
            page.get_by_label("Name").clear()
            page.get_by_label("Name").type(datadictvalue["C_NAME"])

            # Description
            page.get_by_label("Description").clear()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

            # Code
            if datadictvalue["C_CODE"]!='N/A':
                page.get_by_label("Code").clear()
                page.get_by_label("Code").type(datadictvalue["C_CODE"])

            # Start Time
            if datadictvalue["C_START_TIME"]!="N/A":
                page.get_by_label("Start Time").clear()
                page.get_by_label("Start Time").type(datadictvalue["C_START_TIME"])

            # Duration
            if datadictvalue["C_DRTN"]!='N/A':
                page.get_by_label("Duration", exact=True).type(str(datadictvalue["C_DRTN"]))
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Duration Unit").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DRTN_UOM"], exact=True).click()

            # Category
            if datadictvalue["C_CTGRY"]!='N/A':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Category").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CTGRY"], exact=True).click()

            # Shift Details
            ### Shift details with Flexible
            if datadictvalue["C_SHIFT_DTL_TYPE"]=='Flexible':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="ShiftDtlTypeTransient").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SHIFT_DTL_TYPE"],exact=True).click()
                page.wait_for_timeout(5000)

                # Adding row in Shift details
                page.get_by_role("button", name="Add Row").click()
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Name").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SHIFT_DTLS_NAME"], exact=True).click()

                # Shift Details Day
                page.get_by_label("Day").clear()
                page.get_by_label("Day").type(str(datadictvalue["C_SHIFT_DTLS_DAY"]))

                # Shift Details Start Time
                page.locator("//span[text()='Day']//following::input[4]").clear()
                page.locator("//span[text()='Day']//following::input[4]").type(datadictvalue["C_SHIFT_DTLS_START_TIME"])

                # Shift Details Duration
                page.get_by_role("table", name="Shift Details").get_by_label("Duration", exact=True).clear()
                page.get_by_role("table", name="Shift Details").get_by_label("Duration", exact=True).type(str(datadictvalue["C_SHIFT_DTLS_DRTN"]))

                # Shift Details Duration Unit
                page.wait_for_timeout(2000)
                page.get_by_label("Duration Unit", exact=True).nth(2).click()
                page.get_by_role("listbox").get_by_text(datadictvalue["C_SHIFT_DTLS_DRTN_UNIT"]).click()

                # Shift Details Minimum Break Minutes
                page.get_by_label("Minimum Break Minutes").clear()
                page.get_by_label("Minimum Break Minutes").type(str(datadictvalue["C_SHIFT_DTLS_MNMM_BRK_MNTS"]))

                # Shift Details Maximum Break Minutes
                page.get_by_label("Maximum Break Minutes").clear()
                page.get_by_label("Maximum Break Minutes").type(str(datadictvalue["C_SHIFT_DTLS_MXMM_BRK_MNTS"]))

                # Shift Details Core Work
                if datadictvalue["C_SHIFT_DTLS_CORE_WORK"]!='N/A':
                    page.get_by_label("Core Work").clear()
                    page.get_by_label("Core Work").fill(datadictvalue["C_SHIFT_DTLS_CORE_WORK"])

            ### Shift details with Punch
            if datadictvalue["C_SHIFT_DTL_TYPE"]=='Punch':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="ShiftDtlTypeTransient").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SHIFT_DTL_TYPE"],exact=True).click()
                page.wait_for_timeout(5000)

                # Adding row in Shift details
                page.get_by_role("button", name="Add Row").click()
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Name").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SHIFT_DTLS_NAME"], exact=True).click()

                # Shift Details Day
                if datadictvalue["C_SHIFT_DTLS_DAY"]!='N/A':
                    page.get_by_label("Day").clear()
                    page.get_by_label("Day").type(datadictvalue["C_SHIFT_DTLS_DAY"])

                # Shift Details Start Time
                page.locator("//span[text()='Day']//following::input[4]").clear()
                page.locator("//span[text()='Day']//following::input[4]").type(datadictvalue["C_SHIFT_DTLS_START_TIME"])

                # Shift Details Duration
                page.get_by_role("table", name="Shift Details").get_by_label("Duration", exact=True).clear()
                page.get_by_role("table", name="Shift Details").get_by_label("Duration", exact=True).type(str(datadictvalue["C_SHIFT_DTLS_DRTN"]))

                # Shift Details Duration Unit
                page.wait_for_timeout(2000)
                page.get_by_label("Duration Unit", exact=True).nth(2).click()
                page.get_by_role("listbox").get_by_text(datadictvalue["C_SHIFT_DTLS_DRTN_UNIT"]).click()

                # Shift Details Minimum Break Minutes
                page.get_by_label("Minimum Break Minutes").clear()
                page.get_by_label("Minimum Break Minutes").type(str(datadictvalue["C_SHIFT_DTLS_MNMM_BRK_MNTS"]))

                # Shift Details Maximum Break Minutes
                page.get_by_label("Maximum Break Minutes").clear()
                page.get_by_label("Maximum Break Minutes").type(str(datadictvalue["C_SHIFT_DTLS_MXMM_BRK_MNTS"]))

                # Shift Details Core Work
                if datadictvalue["C_SHIFT_DTLS_CORE_WORK"]!='N/A':
                    page.get_by_label("Core Work").clear()
                    page.get_by_label("Core Work").fill(datadictvalue["C_SHIFT_DTLS_CORE_WORK"])

            ### Shift details with None
            if datadictvalue["C_SHIFT_DTL_TYPE"] == 'None':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="ShiftDtlTypeTransient").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SHIFT_DTL_TYPE"],exact=True).click()

            page.get_by_role("button", name="Save and Close").click()

        # Create Shift with Duration shift
        if datadictvalue["C_CRT_SHIFT"] == 'Create Duration Shift':
            #page.get_by_role("cell", name="Create Shift", exact=True).locator("a").click()
            page.get_by_title("Create Shift").nth(2).click()
            page.get_by_role("link", name="Create Duration Shift").click()
            page.wait_for_timeout(3000)

            # Name
            page.get_by_label("Name").clear()
            page.get_by_label("Name").type(datadictvalue["C_NAME"])

            # Description
            page.get_by_label("Description").clear()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

            # Code
            if datadictvalue["C_CODE"] != 'N/A':
                page.get_by_label("Code").clear()
                page.get_by_label("Code").type(datadictvalue["C_CODE"])

            # Duration
            if datadictvalue["C_DRTN"] != 'N/A':
                page.get_by_label("Duration", exact=True).type(str(datadictvalue["C_DRTN"]))
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Duration Unit").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DRTN_UOM"], exact=True).click()

            # Category
            if datadictvalue["C_CTGRY"] != 'N/A':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Category").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CTGRY"], exact=True).click()

            # Period Type
            if datadictvalue["C_PRD_TYPE"] != 'N/A':
                page.wait_for_timeout(2000)
                #page.get_by_role("row", name="*Period Type", exact=True).get_by_role("combobox").click()
                page.locator("//div[text()='Create Duration Shift']//following::input[9]").click()
                #page.get_by_text(datadictvalue["C_PRD_TYPE"], exact=True).click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRD_TYPE"], exact=True).click()

            page.get_by_role("button", name="Save and Close").click()

        # Create Shift with Elapsed shift
        if datadictvalue["C_CRT_SHIFT"] == 'Create Elapsed Shift':
            #page.get_by_role("cell", name="Create Shift", exact=True).locator("a").click()
            page.get_by_title("Create Shift").nth(2).click()
            page.get_by_role("link", name="Create Elapsed Shift").click()

            page.wait_for_timeout(3000)

            # Name
            page.get_by_label("Name").clear()
            page.get_by_label("Name").type(datadictvalue["C_NAME"])

            # Description
            page.get_by_label("Description").clear()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

            # Code
            if datadictvalue["C_CODE"] != 'N/A':
                page.get_by_label("Code").clear()
                page.get_by_label("Code").type(datadictvalue["C_CODE"])

            # Duration
            if datadictvalue["C_DRTN"] != 'N/A':
                page.get_by_label("Duration", exact=True).type(str(datadictvalue["C_DRTN"]))
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Duration Unit").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DRTN_UOM"], exact=True).click()

            # Category
            if datadictvalue["C_CTGRY"] != 'N/A':
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Category").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CTGRY"], exact=True).click()

            page.get_by_role("button", name="Save and Close").click()

        page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("heading", name="Work Shifts")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Work Schedule Configuration Shits  Created Successfully")
            datadictvalue["RowStatus"] = "Created Work Schedule Configuration Shits Successfully"
        except Exception as e:
            print("Unable to Save Work Schedule Configuration Shits")
            datadictvalue["RowStatus"] = "Unable to Save Work Schedule Configuration Shits"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + WORK_SCH_CONFIG, WORK_SHIFTS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + WORK_SCH_CONFIG, WORK_SHIFTS,PRCS_DIR_PATH + WORK_SCH_CONFIG)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + WORK_SCH_CONFIG, WORK_SHIFTS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", WORK_SCH_CONFIG)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", WORK_SCH_CONFIG)[0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))



