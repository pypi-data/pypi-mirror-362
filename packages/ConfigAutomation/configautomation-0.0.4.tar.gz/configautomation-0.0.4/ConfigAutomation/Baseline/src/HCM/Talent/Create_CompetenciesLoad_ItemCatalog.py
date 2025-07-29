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
    page.get_by_role("textbox").type("Item Catalogs")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Item Catalogs", exact=True).click()

    PrevTempName=''

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        if datadictvalue["C_ITEM_CTLG_CTLGNM"] != PrevTempName:

            page.get_by_role("button", name="Add").click()
            page.wait_for_timeout(3000)

            # Template Name
            page.get_by_role("combobox", name="Name").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ITM_CTLG_NM"]).click()

            # Item Catalog Name
            page.get_by_role("cell", name="Create Item Catalog Close *").get_by_label("Item Catalog Name").clear()
            page.get_by_role("cell", name="Create Item Catalog Close *").get_by_label("Item Catalog Name").fill(datadictvalue["C_ITEM_CTLG_CTLGNM"])

            # Saving the Record to enable Add button
            page.get_by_role("button", name="Continue").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Save", exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

            PrevTempName = datadictvalue["C_ITEM_CTLG_CTLGNM"]

        # Clicking on Add button
        page.get_by_role("button", name="Add").click()
        page.wait_for_timeout(3000)

        # Item Name
        page.get_by_label("Name", exact=True).type(datadictvalue["C_ITM_CNTNT_NM"])

        # Clicking on Continue button
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(3000)

        # Item Code
        page.get_by_label("Item Code").click()
        page.get_by_label("Item Code").fill(datadictvalue["C_ITM_CNTNT_CODE"])

        # From Date
        page.get_by_role("row", name="*From Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").clear()
        page.get_by_role("row", name="*From Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").type(datadictvalue["C_ITM_CNTNT_FRMDT"])

        # To Date
        if datadictvalue["C_ITM_CNTNT_TDT"]!='':
            page.get_by_role("row", name="To Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").clear()
            page.get_by_role("row", name="To Date m/d/yy Press down arrow to access Calendar Select Date",exact=True).get_by_placeholder("m/d/yy").type(datadictvalue["C_ITM_CNTNT_TDT"])

        # Rating Model
        page.get_by_title("Select a {ATTRIBUTE_NAME}: Rating Model").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(2000)
        page.get_by_role("cell", name="Name Name Name").get_by_label("Name").type(datadictvalue["C_ITM_CNTNT_RTNGMDL"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.get_by_text(datadictvalue["C_ITM_CNTNT_RTNGMDL"],exact=True).nth(2).click()
        page.get_by_role("button", name="OK").click()

        # Description
        page.get_by_label("Description", exact=True).clear()
        page.get_by_label("Description", exact=True).fill(datadictvalue["C_ITM_CNTNT_DSCPTN"])

        # Competency Alias
        if datadictvalue["C_ITM_CNTNT_CMPTNY ALS"]!='':
            page.get_by_label("Competency Alias").clear()
            page.get_by_label("Competency Alias").fill(datadictvalue["C_ITM_CNTNT_CMPTNY ALS"])

        # Renewal Period Units
        if datadictvalue["C_ITM_CNTNT_PE]RD UNT"]!='':
            page.get_by_title("Select a {ATTRIBUTE_NAME}: Renewal Period Units").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Meaning").clear()
            page.get_by_label("Meaning").type(datadictvalue["C_ITM_CNTNT_PE]RD UNT"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ITM_CNTNT_PE]RD UNT"],exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        # Satisfaction Method
        if datadictvalue["C_ITM_CNTNT_STSF_MTHD"]!='':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Satisfaction Method").click()
            page.get_by_text(datadictvalue["C_ITM_CNTNT_STSF_MTHD"]).click()

        # Category
        if datadictvalue["C_ITM_CNTNT_CTGY"]!='':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Category").click()
            page.get_by_text(datadictvalue["C_ITM_CNTNT_CTGY"]).click()

        # Evaluation Method
        if datadictvalue["C_ITM_CNTNT_EVLTN"]!='':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Evaluation Method").click()
            page.get_by_text(datadictvalue["C_ITM_CNTNT_EVLTN"]).click()

        # Certification Required
        if datadictvalue["C_ITM_CNTNT_CRTFCT"]!='':
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Certification Required").click()
            page.get_by_text(datadictvalue["C_ITM_CNTNT_CRTFCT"], exact=True).click()

        # Renewal Period Frequency
        if datadictvalue["C_ITM_CNTNT_RNPRFRQ"]!='':
            page.get_by_label("Renewal Period Frequency").clear()
            page.get_by_label("Renewal Period Frequency").type(datadictvalue["C_ITM_CNTNT_RNPRFRQ"])

        # Short Description
        if datadictvalue["C_ITM_CNTNT_SHRTDSCPT"]!='':
            page.get_by_label("Short Description").clear()
            page.get_by_label("Short Description").type(datadictvalue["C_ITM_CNTNT_SHRTDSCPT"])

        # Behavioral Indicator
        if datadictvalue["C_ITM_CNTNT_BHVRL"]!='':
            page.get_by_label("Behavioral Indicator").clear()
            page.get_by_label("Behavioral Indicator").fill(datadictvalue["C_ITM_CNTNT_BHVRL"])

        # Long Description
        if datadictvalue["C_ITM_CNTNT_LNGDSCRPT"]!='':
            page.get_by_label("Long Description").clear()
            page.get_by_label("Long Description").type(datadictvalue["C_ITM_CNTNT_LNGDSCRPT"])

        # Save and Close
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Click on Final Save and Close
        if i == rowcount:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)

    try:
        expect(page.get_by_role("heading", name="Item Catalogs")).to_be_visible()
        print("Item Catalog Saved Successfully")
        datadictvalue["RowStatus"] = "Item Catalog Saved Successfully"
    except Exception as e:
        print("Item Catalog not saved")
        datadictvalue["RowStatus"] = "Item Catalog not added"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PROFILE_COMPETENCIES_WRKBK, ITEM_CATALOG):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PROFILE_COMPETENCIES_WRKBK, ITEM_CATALOG,PRCS_DIR_PATH + PROFILE_COMPETENCIES_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PROFILE_COMPETENCIES_WRKBK, ITEM_CATALOG)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", PROFILE_COMPETENCIES_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PROFILE_COMPETENCIES_WRKBK)[0] + "_" + REPEATING_TIME_PERIODS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))