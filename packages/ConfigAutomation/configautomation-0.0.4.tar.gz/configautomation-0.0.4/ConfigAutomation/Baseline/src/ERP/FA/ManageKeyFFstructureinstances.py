from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *



def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    # Login to the instances
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    # Navigation to Manage Asset Books
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Fixed Assets Key Flexfields")
    page.get_by_role("button", name="Search").click()

    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Fixed Assets Key Flexfields").click()
    page.wait_for_timeout(3000)
    # Search for FA Key FlexFields
    page.get_by_role("button", name="Search", exact=True).click()

    PreValue = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        if datadictvalue["C_NAME"] != PreValue:

            # Manage Structures (Select the KK FF Name )
            if datadictvalue["C_KEY_FLXFLD_NAME"] == 'Asset Key Flexfield':
                page.get_by_role("cell", name="Asset Key Flexfield", exact=True).click()
            if datadictvalue["C_KEY_FLXFLD_NAME"] == 'Category Flexfield':
                page.get_by_role("cell", name="Category Flexfield", exact=True).click()
            if datadictvalue["C_KEY_FLXFLD_NAME"] == 'Location Flexfield':
                page.get_by_role("cell", name="Location Flexfield", exact=True).click()

            page.get_by_role("button", name="Manage Structure Instances").click()
            page.wait_for_timeout(2000)
        # Create Structure Instance
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        page.get_by_label("Structure Instance Code").fill(datadictvalue["C_VALUE_SET_CODE"])
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_DSCRP"])

        if datadictvalue["C_ENBLD2"] == 'Yes':
            if not page.get_by_text("Enabled", exact=True).is_checked():
                page.get_by_text("Enabled", exact=True).click()
        elif datadictvalue["C_ENBLD2"] == 'No':
            if page.get_by_text("Enabled", exact=True).is_checked():
                page.get_by_text("Enabled", exact=True).click()

        if datadictvalue["C_SHRTHND_ALIAS_ENBLD"] == 'Yes':
            if not page.get_by_text("Shorthand alias enabled").click().is_checked():
                page.get_by_text("Shorthand alias enabled").click().click()
        elif datadictvalue["C_SHRTHND_ALIAS_ENBLD"] == 'No':
            if page.get_by_text("Shorthand alias enabled").click().is_checked():
                page.get_by_text("Shorthand alias enabled").click().click()

        page.get_by_label("Structure Name").select_option(datadictvalue["C_NAME"])
        page.get_by_role("button", name="Save", exact=True).click()

        # page.get_by_role("button", name="Done").click()
        page.wait_for_timeout(3000)

        j = 0
        while j < rowcount:
            datadictvalue = datadict[j]
            page.get_by_role("cell", name=datadictvalue["C_SGMNT_CODE"], exact=True).first.click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Edit", exact=True).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_RQRD"] == 'Yes':
                if not page.get_by_role("row", name="Required", exact=True).locator("label").is_checked():
                    page.get_by_role("row", name="Required", exact=True).locator("label").click()
            elif datadictvalue["C_RQRD"] == 'No':
                if page.get_by_role("row", name="Required", exact=True).locator("label").is_checked():
                    page.get_by_role("row", name="Required", exact=True).locator("label").click()
            if datadictvalue["C_DSPLYD"] == 'Yes':
                if not page.get_by_role("row", name="Displayed", exact=True).locator("label").is_checked():
                    page.get_by_role("row", name="Displayed", exact=True).locator("label").click()
            elif datadictvalue["C_DSPLYD"] == 'No':
                if page.get_by_role("row", name="Displayed", exact=True).locator("label").is_checked():
                    page.get_by_role("row", name="Displayed", exact=True).locator("label").click()
            if datadictvalue["C_BI_ENBD"] == 'Yes':
                if not page.get_by_role("row", name="BI enabled", exact=True).locator("label").is_checked():
                    page.get_by_role("row", name="BI enabled", exact=True).locator("label").click()
            if datadictvalue["C_BI_ENBD"] == 'No':
                if page.get_by_role("row", name="BI enabled", exact=True).locator("label").is_checked():
                    page.get_by_role("row", name="BI enabled", exact=True).locator("label").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Query Required").click()
            page.get_by_label("Query Required").select_option(datadictvalue["C_QUERY_RQRD"])
            # page.get_by_label("Query Required").press("Tab")
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="OK").click()
            print("Row Added - ", str(j))
            j = j + 1

        datadictvalue["RowStatus"] = "Successfully Created Structure Instances"
        page.wait_for_timeout(2000)



        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Done").click()
        i = i + 1

        page.wait_for_timeout(5000)


        #Deployment


        page.get_by_role("cell", name="Asset Key Flexfield", exact=True).click()
        page.get_by_role("button", name="Deploy Flexfield").click()
        page.wait_for_timeout(8000)
        try:
            expect(page.get_by_text("KEY# : Confirmation")).to_be_visible()
            page.get_by_role("button", name="OK").click()
            print("Asset Key Field Deployed Successfully")

        except Exception as e:
            print("Asset Key Field Deployed  not Saved")

        page.get_by_role("cell", name="Category Flexfield", exact=True).click()
        page.get_by_role("button", name="Deploy Flexfield").click()
        page.wait_for_timeout(8000)

        try:
            expect(page.get_by_text("CAT# : Confirmation")).to_be_visible()
            page.get_by_role("button", name="OK").click()
            print("Category Key Field Deployed Successfully")

        except Exception as e:
            print("Category Key Field Deployed  not Saved")

        page.get_by_role("cell", name="Location Flexfield", exact=True).click()
        page.get_by_role("button", name="Deploy Flexfield").click()
        page.wait_for_timeout(8000)

        try:
            expect(page.get_by_text("LOC# : Confirmation")).to_be_visible()
            page.get_by_role("button", name="OK").click()
            print("Location Key Field Deployed Successfully")

        except Exception as e:
            print("Location Key Field Deployed  not Saved")

        page.wait_for_timeout(5000)




    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_FA_KEYFF):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + FA_WORKBOOK, MANAGE_FA_KEYFF, PRCS_DIR_PATH + FA_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + FA_WORKBOOK, MANAGE_FA_KEYFF)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[0] + "_" + MANAGE_FA_KEYFF)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", FA_WORKBOOK)[
            0] + "_" + MANAGE_FA_KEYFF + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))