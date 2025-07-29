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
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Manage Bank Branches")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Bank Branches", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(2000)

        # Enter Bank Info
        page.get_by_label("Bank", exact=True).click()
        page.get_by_label("Bank", exact=True).fill(datadictvalue["C_BANK"])
        # page.get_by_label("Bank", exact=True).fill("AN Bank")
        page.get_by_label("Bank", exact=True).press("Tab")
        page.wait_for_timeout(3000)
        page.get_by_label("Branch Name", exact=True).fill(datadictvalue["C_BRNCH_NAME"])
        page.wait_for_timeout(1000)
        page.get_by_label("Alternate Branch Name").fill(datadictvalue["C_ALTRNT_BRNCH_NAME"])
        page.wait_for_timeout(1000)
        page.get_by_label("Routing Number").fill(str(datadictvalue["C_RTNG_TRNST_NMBR"]))
        page.wait_for_timeout(1000)
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.wait_for_timeout(1000)
        page.get_by_label("BIC Code").fill(str(datadictvalue["C_BIC_CODE"]))
        page.wait_for_timeout(1000)
        page.get_by_label("Branch Number Type").select_option(datadictvalue["C_BRNCH_NMBR_TYPE"])
        page.wait_for_timeout(1000)
        page.get_by_label("Bank Branch Type").select_option(datadictvalue["C_BANK_BRNCH_TYPE"])
        page.wait_for_timeout(1000)
        page.get_by_label("EDI ID Number").fill(str(datadictvalue["C_EDI_ID_NMBR"]))
        page.wait_for_timeout(1000)
        # page.get_by_label("EFT Number").fill()
        page.get_by_label("EDI Location").fill(datadictvalue["C_EDI_LCTN"])
        page.wait_for_timeout(1000)
        page.get_by_label("RFC Identifier").select_option(str(datadictvalue["C_RFC_IDNTFR"]))
        page.wait_for_timeout(3000)

        # Address
        if datadictvalue["C_ADDRSS_LINE_1"] != '':
            page.get_by_label("Expand Addresses").click()
            page.get_by_role("button", name="Create").click()
            page.get_by_role("cell", name="Create Address Country *").get_by_label("Country", exact=True).select_option(datadictvalue["C_ADDRSS_CNTRY"])
            page.wait_for_timeout(1000)
            page.get_by_label("Address Line 1").click()
            page.get_by_label("Address Line 1").fill(datadictvalue["C_ADDRSS_LINE_1"])
            page.get_by_label("Address Line 2").fill(datadictvalue["C_ADDRSS_LINE_2"])
            page.get_by_label("Address Line 3").fill(datadictvalue["C_ADDRSS_LINE_3"])
            page.get_by_title("Postal Code").click()
            page.wait_for_timeout(1000)
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Postal Code").fill(str(datadictvalue["C_PSTL_CODE"]))
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(1000)
            page.locator("//span[text()='Postal Code']//following::span[contains(text(),'"+str(datadictvalue["C_PSTL_CODE"])+"')]").nth(0).click()
            page.get_by_role("button", name="OK").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_label("City").clear()
            page.get_by_label("City").fill(datadictvalue["C_CITY"])
            page.get_by_label("State").clear()
            page.get_by_label("State").fill(datadictvalue["C_STATE"])
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_ADDRSS_LINE_1"]).click()
            if datadictvalue["C_ADDRSS_PRMRY"] == 'Yes':
                page.get_by_role("button", name="Set Primary").click()
                page.wait_for_timeout(1000)

        # Create Bank Contact
        if datadictvalue["C_PHONE"] and datadictvalue["C_EMAIL"] and datadictvalue["C_FIRST_NAME"] != '':
            page.get_by_label("Expand Contacts").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Create").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_label("First Name").fill(datadictvalue["C_FIRST_NAME"])
            page.get_by_label("Middle Name").fill(datadictvalue["C_MDDL_NAME"])
            page.get_by_label("Last Name").fill(datadictvalue["C_LAST_NAME"])
            page.get_by_label("Comments").fill(datadictvalue["C_CMMNTS"])

            # Add Phone Numbers
            if datadictvalue["C_PHONE"] != '':
                page.get_by_role("button", name="Add Row").first.click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name='Contact Points').locator("select").select_option(datadictvalue["C_PRPS"])
                page.get_by_role("cell", name="Phone Country Code").get_by_label("Phone Country Code").fill(str(datadictvalue["C_PHONE_CNTRY_CODE"]))
                page.get_by_label("Area Code").fill(str(datadictvalue["C_AREA_CODE"]))
                page.get_by_label("Phone", exact=True).fill(str(datadictvalue["C_PHONE"]))
                page.get_by_label("Extension").fill(str(datadictvalue["C_EXTNSN"]))
                page.wait_for_timeout(2000)
                if datadictvalue["C_PHONE_PRMRY"] == 'Yes':
                    page.get_by_role("button", name="Set Primary").first.click()

            # Add Addresses
            if datadictvalue["C_CNTCT_ADDRSS_LINE_1"] != '':
                if page.get_by_role("cell", name="Addresses This table contains column headers corresponding to the data body table below Addresses No data to display. Columns Hidden 2 Address date range : Current", exact=True).get_by_role("button").first.is_visible():
                    page.get_by_role("cell", name="Addresses This table contains column headers corresponding to the data body table below Addresses No data to display. Columns Hidden 2 Address date range : Current", exact=True).get_by_role("button").first.click()
                page.get_by_role("button", name="Create").click()
                page.wait_for_timeout(2000)
                page.get_by_role("cell", name="Create Address Country *").get_by_label("Country", exact=True).select_option(datadictvalue["C_CNTCT_CNTRY"])
                page.get_by_label("Address Line 1").click()
                page.get_by_label("Address Line 1").fill(datadictvalue["C_CNTCT_ADDRSS_LINE_1"])
                page.get_by_label("Address Line 2").fill(datadictvalue["C_CNTCT_ADDRSS_LINE_2"])
                # page.get_by_label("Address Line 3").fill(datadictvalue["C_ADDRSS_LINE_2"])
                page.get_by_title("Postal Code").click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_role("textbox", name="Postal Code").fill(str(datadictvalue["C_CNTCT_PSTL_CODE"]))
                page.get_by_role("button", name="Search", exact=True).click()
                page.locator("//span[text()='Postal Code']//following::span[contains(text(),'" + str(datadictvalue["C_CNTCT_PSTL_CODE"]) + "')]").nth(0).click()
                page.get_by_role("button", name="OK").nth(2).click()
                page.wait_for_timeout(2000)
                page.get_by_label("City").clear()
                page.get_by_label("City").fill(datadictvalue["C_CNTCT_CITY"])
                page.get_by_label("State").clear()
                page.get_by_label("State").fill(datadictvalue["C_CNTCT_STATE"])
                page.get_by_role("button", name="OK").nth(1).click()
                page.wait_for_timeout(3000)
                # page.get_by_text(datadictvalue["C_CNTCT_ADDRSS_LINE_1"]).click()
                # if page.get_by_role("link", name="Close").is_visible():
                #     page.get_by_role("link", name="Close").click()
                # if page.get_by_role("cell",name="Addresses This table contains column headers corresponding to the data body table below Addresses No data to display. Columns Hidden 2 Address date range : Current",
                #                     exact=True).get_by_role("button").first.is_visible():
                #     page.get_by_role("cell",name="Addresses This table contains column headers corresponding to the data body table below Addresses No data to display. Columns Hidden 2 Address date range : Current",
                #                      exact=True).get_by_role("button").first.click()
                # if datadictvalue["C_CNTCT_ADDRSS_PRMRY"] == 'Yes':
                #     page.get_by_role("row", name="Set Primary", exact=True).get_by_role("button").click()

            # Add Email
            if datadictvalue["C_EMAIL"] != '':
                page.get_by_role("button", name="Add Row").nth(1).click()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name="Expand Email Email").get_by_role("cell").nth(3).locator("select").select_option(datadictvalue["C_MAIL_PRPS"])
                page.get_by_label("Email").fill(datadictvalue["C_EMAIL"])
                if datadictvalue["C_MAIL_PRMRY"] == 'Yes':
                    page.get_by_role("button", name="Set Primary").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="OK").click()

        # Save the data
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        if page.get_by_role("button", name="Yes").is_visible():
            page.get_by_role("button", name="Yes").click()
        page.wait_for_timeout(2000)
        if page.get_by_role("button", name="OK").is_visible():
            page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Done").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Bank Branches Saved Successfully")
            datadictvalue["RowStatus"] = "Bank Branches are added successfully"

        except Exception as e:
            print("Bank Branches not saved")
            datadictvalue["RowStatus"] = "Bank Branches are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, BANK_BRANCHES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + CM_WORKBOOK, BANK_BRANCHES, PRCS_DIR_PATH + CM_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + CM_WORKBOOK, BANK_BRANCHES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0] + "_" + BANK_BRANCHES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", CM_WORKBOOK)[0] + "_" + BANK_BRANCHES + "_Results_" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
