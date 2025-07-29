from playwright.sync_api import Playwright, sync_playwright
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *

CONFIGNAME = "ManagePersonNameStyles"


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
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Person Name Styles")
    page.get_by_role("textbox").press("Enter")

    # Navigating to Manage Person Name Styles page & Entering the data
    page.get_by_role("link", name="Manage Person Name Styles", exact=True).click()
    page.wait_for_timeout(5000)

    prevCountry = ""
    r = 0
    while r < rowcount:
        datadictvalue = datadict[r]
        page.wait_for_timeout(10000)

        if prevCountry != datadictvalue["C_CNTRY"]:

            if r > 0:
                page.get_by_role("button", name="Save").click()
                page.wait_for_timeout(2000)
                datadict[r - 1]["RowStatus"] = "Person Name Style Saved"

            page.get_by_placeholder("Search by country").click()
            page.get_by_placeholder("Search by country").type(datadictvalue["C_CNTRY"])
            page.get_by_role("button", name="Search by country").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Country").locator("a").click()
            page.wait_for_timeout(5000)

        # Enter the country name style definition
        # Get the locator of the display sequence
        href = page.locator("//input[contains(@id,'person-name-styles-table-input-text')]").evaluate_all("(AllLocs, LocValue) => checkLocAttrValue (AllLocs, LocValue); function checkLocAttrValue (AllLocs, LocValue) { for(let n=0; n < AllLocs.length; n++) { if (document.getElementById(AllLocs[n].attributes[7].value).value == LocValue) { return AllLocs[n].attributes[7].value} } } ", datadictvalue["C_NAME_CMPNNT"])
        # print("Evaluated for - ", datadictvalue["C_NAME_CMPNNT"] + " - " + str(href))

        if str(href) != "None":
            # Find the row index num from the locator

            FindRowIdxNum = re.findall(r'\d+', str(href))
            #print("Evaluated for - ", datadictvalue["C_NAME_CMPNNT"] + " - " + str(href) + "; Index - " + FindRowIdxNum[0])

            # Update all the parameters based on the spreadsheet
            page.locator("[id=\"person-name-styles-table-input-number-" + str(FindRowIdxNum[0]) + "\\|input\"]").dblclick()
            page.locator("[id=\"person-name-styles-table-input-number-" + str(FindRowIdxNum[0]) + "\\|input\"]").fill(str(datadictvalue["C_DSPLY_SQNC"]))  # Display Sequence

            page.locator("[id=\"person-name-styles-table-display-name-input-text-" + str(FindRowIdxNum[0]) + "\\|input\"]").dblclick()
            page.locator("[id=\"person-name-styles-table-display-name-input-text-" + str(FindRowIdxNum[0]) + "\\|input\"]").fill(datadictvalue["C_DSPLY_NAME"])  # Display Name

            if page.locator("input[name=\"person-name-styles-table-checkboxset-" + str(FindRowIdxNum[0]) + "\"]").is_enabled():
                page.locator("input[name=\"person-name-styles-table-checkboxset-" + str(FindRowIdxNum[0]) + "\"]").dblclick()

                if datadictvalue["C_RQRD"] == "Y":
                    page.locator("input[name=\"person-name-styles-table-checkboxset-" + str(FindRowIdxNum[0]) + "\"]").check()  # Required
                if datadictvalue["C_RQRD"] == "N" or '':
                    page.locator("input[name=\"person-name-styles-table-checkboxset-" + str(FindRowIdxNum[0]) + "\"]").uncheck()  # Required

            page.locator("[id=\"person-name-styles-table-lookup-input-text-" + str(FindRowIdxNum[0]) + "\\|input\"]").dblclick()
            page.locator("[id=\"person-name-styles-table-lookup-input-text-" + str(FindRowIdxNum[0]) + "\\|input\"]").fill(datadictvalue["C_NAME_CMPNNT_LKP"])  # Name Component Lookup
        else:
            # Component Provided is not existing. Add a new value
            page.get_by_label("Add").click()
            page.wait_for_timeout(2000)

            page.locator("[id=\"person-name-styles-table-input-number-0\\|input\"]").dblclick()
            page.locator("[id=\"person-name-styles-table-input-number-0\\|input\"]").fill(str(datadictvalue["C_DSPLY_SQNC"]))  # Display Sequence

            page.get_by_role("combobox", name="Select a value").dblclick()
            page.get_by_role("combobox", name="Select a value").type(datadictvalue["C_NAME_CMPNNT"])
            page.get_by_role("combobox", name="Select a value").press("Tab")
            # page.get_by_text(datadictvalue["C_NAME_CMPNNT"],exact=True).click()

            page.locator("[id=\"person-name-styles-table-display-name-input-text-0\\|input\"]").dblclick()
            page.locator("[id=\"person-name-styles-table-display-name-input-text-0\\|input\"]").fill(datadictvalue["C_DSPLY_NAME"])  # Display Name

            page.locator("input[name=\"person-name-styles-table-checkboxset-0\"]").dblclick()
            if datadictvalue["C_RQRD"] == "Y":
                page.locator("input[name=\"person-name-styles-table-checkboxset-0\"]").check()  # Required
            else:
                page.locator("input[name=\"person-name-styles-table-checkboxset-0\"]").uncheck()  # Required

            page.locator("[id=\"person-name-styles-table-lookup-input-text-0\\|input\"]").dblclick()
            page.locator("[id=\"person-name-styles-table-lookup-input-text-0\\|input\"]").fill(datadictvalue["C_NAME_CMPNNT_LKP"])  # Name Component Lookup

            page.get_by_role("button", name="Save").click()

        datadict[r]["RowStatus"] = "Person Name Style Updated"
        prevCountry = datadictvalue["C_CNTRY"]
        r = r + 1

    # Final Row Save
    if r == rowcount:
        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(2000)
        datadict[r - 1]["RowStatus"] = "Person Name Style Saved"

    page.wait_for_timeout(2000)
    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_PRSN_NM_STYL):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_PRSN_NM_STYL, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_PRSN_NM_STYL)
    if rows > 1:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + MANAGE_PRSN_NM_STYL)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[
            0] + "_" + MANAGE_PRSN_NM_STYL + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
