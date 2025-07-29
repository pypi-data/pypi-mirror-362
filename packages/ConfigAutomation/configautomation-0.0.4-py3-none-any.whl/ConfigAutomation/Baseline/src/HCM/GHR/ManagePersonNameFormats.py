from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *
import re

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
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Person Name Formats")
    page.get_by_role("textbox").press("Enter")



    # Navigating to Manage Address Formats page & Entering the data
    page.get_by_role("link", name="Manage Person Name Formats", exact=True).click()
    page.wait_for_timeout(5000)
    
    PrevPrsnFrmt=""
    r = 0
    while r < rowcount:

        datadictvalue = datadict[r]
        page.wait_for_timeout(5000)

        # This worksheet will contain multiple rows for one Name Format setup.
        # Hence, checking if the next row is same as earlier to determine if we are working
        # with the same Format or a new one
        if datadictvalue["C_FRMT_TYPE"] != PrevPrsnFrmt:

            #Save the prev record data if the row contains a name Format
            if r > 0:
                page.wait_for_timeout(5000)
                page.get_by_role("button", name="Submit").click()
                try:
                    expect(page.get_by_role("heading", name="Name Formats")).to_be_visible()
                    print("Person format Saved")
                    datadict[r - 1]["RowStatus"] = "Person format Saved"
                except Exception as e:
                    print("Unable to save Person format")
                    datadict[r - 1]["RowStatus"] = "Unable to save Person format"
                
            #Reset the counter to identify rows correctly for child levels
            i = 0
            page.wait_for_timeout(5000)
            page.get_by_placeholder("Search by type, country, or").click()
            page.get_by_placeholder("Search by type, country, or").type(datadictvalue["C_FRMT_TYPE"])
            # page.get_by_role("button", name="Suggested Filter Label: Scope").click()
            page.locator("(//div[text()='Scope'])[1]").click()
            page.get_by_label("Global").click()
            page.wait_for_timeout(3000)
            page.locator("#pill-UserFormatChoice-popup_layer_overlay").click()
            page.wait_for_timeout(5000)
            page.locator("#edit-record-link").click()
            page.wait_for_timeout(5000)
            count = page.locator("//span[text()='Delete']").count()
            print(count)
            j = 0
            while j < count:
                page.locator("//span[text()='Delete']").first.click()
                print("Row deleted Successfully")
                j = j + 1
            PrevPrsnFrmt = datadictvalue["C_FRMT_TYPE"]


        #Add Components
        page.get_by_label("Add").click()
        page.wait_for_timeout(3000)
        if datadictvalue["C_CMPNNT_1"] != "":
            page.get_by_role("combobox", name="Component 1").click()
            page.get_by_role("combobox", name="Component 1").type(datadictvalue["C_CMPNNT_1"])
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_CMPNNT_1"]).first.click()
        if datadictvalue["C_CMPNNT_2"] != "":
            page.get_by_role("combobox", name="Component 2").click()
            page.get_by_role("combobox", name="Component 2").type(datadictvalue["C_CMPNNT_2"])
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_CMPNNT_2"]).first.click()
        if datadictvalue["C_CMPNNT_3"] != "":
            page.get_by_role("combobox", name="Component 3").click()
            page.get_by_role("combobox", name="Component 3").type(datadictvalue["C_CMPNNT_3"])
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_CMPNNT_3"],exact=True).first.click()
        if datadictvalue["C_CMPNNT_4"] != "":
            page.get_by_role("combobox", name="Component 4").click()
            page.get_by_role("combobox", name="Component 4").type(datadictvalue["C_CMPNNT_4"])
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_CMPNNT_4"],exact=True).first.click()
        if datadictvalue["C_CMPNNT_5"] != "":
            page.get_by_role("combobox", name="Component 5").click()
            page.get_by_role("combobox", name="Component 5").type(datadictvalue["C_CMPNNT_5"])
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_CMPNNT_5"],exact=True).first.click()
        if datadictvalue["C_CMPNNT_6"] != "":
            page.get_by_role("combobox", name="Component 6").click()
            page.get_by_role("combobox", name="Component 6").type(datadictvalue["C_CMPNNT_6"])
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_CMPNNT_6"],exact=True).first.click()
        page.get_by_role("row",name="Component 1 Component 2 Component 3 Component 4 Component 5 Component 6 Replace Condition",exact=True).get_by_label("Submit").click()

        print("Row Added - ", str(r))
        datadictvalue["RowStatus"] = "Row Added"
        i = i + 1
        r = r + 1

        #Do the save of the last before signing out
    if r == rowcount:
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Submit").click()
        try:
            expect(page.get_by_role("heading", name="Name Formats")).to_be_visible()
            print("Person format Saved")
            datadict[r - 1]["RowStatus"] = "Person format Saved"
        except Exception as e:
            print("Unable to save Person format")
            datadict[r - 1]["RowStatus"] = "Unable to save Person format"

    page.wait_for_timeout(2000)
    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_PRSN_FORMATS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_PRSN_FORMATS, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_PRSN_FORMATS)
    if rows > 1:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0]+ "_" + MANAGE_PRSN_FORMATS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + MANAGE_PRSN_FORMATS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))