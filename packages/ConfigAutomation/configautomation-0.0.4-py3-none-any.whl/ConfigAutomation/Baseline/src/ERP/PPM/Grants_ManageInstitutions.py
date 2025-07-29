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

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(5000)
    page.get_by_role("textbox").fill("Manage Institutions")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Institutions").click()
    page.wait_for_timeout(3000)
    # page.pause()

    # Create Institutions

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        # Header Details

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Parent Institution").select_option(datadictvalue["C_PRNT_INSTTTN"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.get_by_label("Unique Entity Identifier").fill(str(datadictvalue["C_UNQ_ENTTY_IDNTFR"]))
        page.get_by_label("D-U-N-S Number").fill(str(datadictvalue["C_DUNS_NMBR"]))
        page.get_by_label("NIH IPF Number").fill(str(datadictvalue["C_UNQ_ENTTY_IDNTFR"]))
        page.get_by_label("DHHS Entity Number").fill(str(datadictvalue["C_DHHS_ENTTY_NMBR"]))
        page.wait_for_timeout(2000)
        # Institution General Details -Location
        page.get_by_role("link", name="General Information").click()
        page.get_by_role("button", name="Create").first.click()
        page.wait_for_timeout(2000)
        page.get_by_label("Location", exact=True).type(datadictvalue["C_LCTN"])
        page.get_by_role("option", name=datadictvalue["C_LCTN"]).click()
        # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar From Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"].strftime("%m/%d/%Y"))
        # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar To Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"])
        page.locator("//img[@title='Primary']//following::input[1]").fill(datadictvalue["C_FROM_DATE"])
        if datadictvalue["C_TO_DATE"] !='':
            page.locator("//img[@title='Primary']//following::input[3]").fill(datadictvalue["C_TO_DATE"])
        if datadictvalue["C_AWARD_LCTN"] == 'Yes':
            page.locator("//span[text()='Award Location']//following::label[contains(@id,'Label0')][1]").check()
        if datadictvalue["C_BLLNG_LCTN"] == 'Yes':
            page.locator("//span[text()='Billing Location']//following::label[contains(@id,'Label0')][2]").check()
        page.get_by_label("URL").fill(datadictvalue["C_URL"])
        page.wait_for_timeout(2000)
        # Create References
        if datadictvalue["C_TYPE"] != '':
            page.get_by_role("button", name="Create").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_label("Type").fill(datadictvalue["C_TYPE"])
            page.get_by_label("Value").fill(datadictvalue["C_VALUE"])
            page.get_by_label("Comments").fill(datadictvalue["C_CMMNTS"])
            page.wait_for_timeout(2000)
        # Contacts Details
        page.get_by_role("link", name="Contacts").click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_CRT_CNTCT_PRSN_NAME"] != '':
            page.get_by_role("button", name="Create").first.click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Name").fill(datadictvalue["C_CRT_CNTCT_PRSN_NAME"])
            page.get_by_role("combobox", name="Name").press("Tab")
        # Official Types
            if datadictvalue["C_CRT_OFFCL_TYPES_NAME"] != '':
                page.get_by_role("button", name="Create").nth(1).click()
                page.get_by_role("table", name="Official Types").get_by_label("Name").select_option(datadictvalue["C_CRT_OFFCL_TYPES_NAME"])
            page.wait_for_timeout(2000)
        # Compliance
        page.get_by_role("link", name="Compliance").click()
        if datadictvalue["C_CRT_CRTFCTN_NAME"] != '':
            page.get_by_role("button", name="Create")
            page.get_by_role("combobox", name="Name").nth(0).fill(datadictvalue["C_CRT_CRTFCTN_NAME"])
            if datadictvalue["C_SPNSR"] != '':
                page.get_by_label("Sponsor").fill(datadictvalue["C_SPNSR"])
                page.get_by_label("Sponsor").press("Tab")
            page.wait_for_timeout(2000)
            page.get_by_label("Status").select_option(datadictvalue["C_STTS"])
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar Certification Date Select Date").get_by_placeholder("m/d/yy").fill(datadictvalue["C_CRTFCTN_DATE"])
            # page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar Expiration Date Select Date").get_by_placeholder("m/d/yy").fill(datadictvalue["C_EXPRTNN_DATE"])
            page.locator("//a[@title='Search: Sponsor']//following::input[1]").fill(datadictvalue["C_CRTFCTN_DATE"])
            page.locator("//a[@title='Search: Sponsor']//following::input[3]").fill(datadictvalue["C_EXPRTNN_DATE"])
            page.get_by_label("Reference Number").fill(str(datadictvalue["C_RFRNC_NMBR"]))

        # Audit
        page.get_by_role("link", name="Audits").click()
        if datadictvalue["C_CRT_TYPES_NAME"] != '':
            # Types
            # page.get_by_role("button", name="Create").first.click()
            page.get_by_role("button", name="Create").click()
            page.get_by_role("table", name="Types").get_by_label("Name").select_option(datadictvalue["C_CRT_TYPES_NAME"])
            if datadictvalue["C_PRGRM_CVRG"] != '':
                page.get_by_label("Program Coverage").fill(datadictvalue["C_PRGRM_CVRG"])
                page.get_by_label("Sponsor").fill(datadictvalue["C_CRT_DTLS_SPNSR"])
                page.get_by_label("Auditor").fill(datadictvalue["C_ADTR"])
                page.get_by_label("Report Number").fill(datadictvalue["C_RPRT_NMBR"])
                page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar Start Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_START_DATE"])
                page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar End Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_END_DATE"])
                page.get_by_role("cell", name="m/d/yy Press down arrow to access Calendar Report Date Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_RPRT_DATE"])
                if datadictvalue["C_NMBR"] != '':
                    page.get_by_role("button", name="Create").nth(2).click()
                    page.get_by_label("Resolution Official Name").fill(datadictvalue["C_RSLTN_OFFCL_NAME"])
                    page.get_by_role("table", name="Alerts").get_by_label("Description").fill(datadictvalue["C_CRT_ALRTS_DSCRPTN"])
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        # Repeating the loop
        i = i + 1

    if i == rowcount:
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)


    try:
        expect(page.get_by_role("button", name="Done")).to_be_visible()
        print("Manage Institutions Saved Successfully")
        datadictvalue["RowStatus"] = "Manage Institutions added successfully"

    except Exception as e:
        print("Manage Institutions not saved")
        datadictvalue["RowStatus"] = "Manage Institutions are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, INSTITUTIONS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, INSTITUTIONS,
                             PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK, INSTITUTIONS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[0] + "_" + INSTITUTIONS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PPM_GRNTS_CONFIG_WRKBK)[
            0] + "_" + INSTITUTIONS + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))