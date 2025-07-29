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
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Common Lookups")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.get_by_role("link", name="Manage Common Lookups").click()
        page.get_by_label("Meaning").click()
        page.get_by_label("Meaning").type(datadictvalue["C_LKP_TYPE"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(5000)

        #Checking Look up type is present already If yes create Look up code
        if page.get_by_text(datadictvalue["C_LKP_TYPE"], exact=True).first.is_visible():
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="New").nth(1).click()
            page.wait_for_timeout(3000)
            page.get_by_label("Lookup Code", exact=True).type(datadictvalue["C_LKP_CODE"])
            page.get_by_label("Display Sequence").first.type(str(datadictvalue["C_DSPLY_SQNC"]))
            if datadictvalue["C_ENBLD"] == "Yes":
                if not page.locator("input[type='checkbox']").first.is_checked():
                    page.locator("input[type='checkbox']").first.click()
            page.get_by_role("table", name='selected lookup type').get_by_role("row").first.get_by_role("cell",name="Start Date").locator("input").first.click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_START_DATE"] != '':
                page.get_by_role("table", name='selected lookup type').get_by_role("row").first.get_by_role("cell",name="Start Date").locator("input").first.type(datadictvalue["C_START_DATE"].strftime('%m/%d/%y'))
                page.get_by_role("table", name='selected lookup type').get_by_role("row").first.get_by_role("cell",name="End Date").locator("input").first.click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_END_DATE"] != '':
                page.get_by_role("table", name='selected lookup type').get_by_role("row").first.get_by_role("cell",name="End Date").locator("input").first.type(datadictvalue["C_END_DATE"].strftime('%m/%d/%y'))
            page.get_by_label("Meaning").nth(2).type(datadictvalue["C_LKP_CODE_MNNG"])
            page.get_by_label("Description").nth(2).click()
            page.get_by_label("Description").nth(2).type(datadictvalue["C_LKP_CODE_DSCRPTN"])
            page.get_by_label("Tag").first.type(datadictvalue["C_TAG"])
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            #page.get_by_role("button", name="Cancel").click()
            page.wait_for_timeout(5000)
            try:
                expect(page.get_by_role("link", name="Manage Common Lookups")).to_be_visible()
                print("Added Common Lookup Code Saved Successfully")
                datadictvalue["RowStatus"] = "Added Common Lookup Code"
            except Exception as e:
                print("Unable to save Common Lookup Code")
                datadictvalue["RowStatus"] = "Unable to Add Common Lookup Code"
            print("Row Added - ", str(i))
            datadictvalue["RowStatus"] = "Added Common Lookup Code Successfully"
        #If Look up Type not present already create Look up Type and Look up Code
        else:
            #Create Look up Type
            page.get_by_role("button", name="New").first.click()
            page.get_by_label("Lookup Type").nth(1).click()
            page.get_by_label("Lookup Type").nth(1).type(datadictvalue["C_LKP_TYPE"])
            page.get_by_label("Meaning").nth(1).click()
            page.get_by_label("Meaning").nth(1).type(datadictvalue["C_LKP_TYPE_MNNG"])
            page.get_by_label("Description").nth(1).click()
            page.get_by_label("Description").nth(1).type(datadictvalue["C_LKP_TYPE_DSCRPTN"])
            page.get_by_label("Module").nth(1).click()
            page.get_by_label("Module").nth(1).type(datadictvalue["C_MDL"])
            page.get_by_role("button", name="Save", exact=True).click()
            page.wait_for_timeout(7000)
            # page.pause()
            #Create Look up Code
            # if page.get_by_label("Expand : Lookup Codes").is_visible():
            page.locator("//a[contains(@title,'Expand')]").nth(1).click()
            page.get_by_role("button", name="New").nth(1).click()
            page.wait_for_timeout(3000)
            page.get_by_label("Lookup Code", exact=True).type(datadictvalue["C_LKP_CODE"])
            page.get_by_label("Display Sequence").first.type(str(datadictvalue["C_DSPLY_SQNC"]))
            if datadictvalue["C_ENBLD"] == "Yes":
                if not page.locator("input[type='checkbox']").first.is_checked():
                    page.locator("input[type='checkbox']").first.click()
            page.get_by_role("table", name='selected lookup type').get_by_role("row").first.get_by_role("cell", name="Start Date").locator("input").first.click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_START_DATE"]!='':
                page.get_by_role("table", name='selected lookup type').get_by_role("row").first.get_by_role("cell", name="Start Date").locator("input").first.type(datadictvalue["C_START_DATE"].strftime('%m/%d/%y'))
                page.get_by_role("table", name='selected lookup type').get_by_role("row").first.get_by_role("cell", name="End Date").locator("input").first.click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_END_DATE"]!='':
                page.get_by_role("table", name='selected lookup type').get_by_role("row").first.get_by_role("cell", name="End Date").locator("input").first.type(datadictvalue["C_END_DATE"].strftime('%m/%d/%y'))
            page.get_by_label("Meaning").nth(2).type(datadictvalue["C_LKP_CODE_MNNG"])
            page.get_by_label("Description").nth(2).click()
            page.get_by_label("Description").nth(2).type(datadictvalue["C_LKP_CODE_DSCRPTN"])
            page.get_by_label("Tag").first.type(datadictvalue["C_TAG"])
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            # page.get_by_role("button", name="Cancel").click()
            page.wait_for_timeout(5000)
            try:
                expect(page.get_by_role("link", name="Manage Common Lookups Type")).to_be_visible()
                print("Added Common Lookup Type Saved Successfully")
                datadictvalue["RowStatus"] = "Added Common Lookup Type and code"
            except Exception as e:
                print("Unable to save Common Lookup Type")
                datadictvalue["RowStatus"] = "Unable to Add Common Lookup Type and code"
            print("Row Added - ", str(i))
            datadictvalue["RowStatus"] = "Added Common Lookup Type Successfully"
        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_COMMON_LOOKUP):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_COMMON_LOOKUP, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_COMMON_LOOKUP)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0]+ "_" + MANAGE_COMMON_LOOKUP)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + MANAGE_COMMON_LOOKUP + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

