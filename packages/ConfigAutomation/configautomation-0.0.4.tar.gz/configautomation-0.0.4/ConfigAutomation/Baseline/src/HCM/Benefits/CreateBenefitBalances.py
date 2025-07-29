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

    # Navigate to Benefit Balance page
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Benefits Administration", exact=True).click()
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Benefit Balances").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(3000)


        # Effective Date
        if datadictvalue["C_EFFCTV_DATE"]!='':
            page.get_by_role("cell",name="Create Benefit Balance Close *Effective Date m/d/yy Press down arrow to access").get_by_placeholder("m/d/yy").clear()
            page.get_by_role("cell",name="Create Benefit Balance Close *Effective Date m/d/yy Press down arrow to access").get_by_placeholder("m/d/yy").type(str(datadictvalue["C_EFFCTV_DATE"]))

        # Benefit Balance
        if datadictvalue["C_BNFT_BLNC"]!='':
            page.get_by_role("row", name="*Benefit Balance", exact=True).get_by_label("Benefit Balance").clear()
            page.get_by_role("row", name="*Benefit Balance", exact=True).get_by_label("Benefit Balance").type(datadictvalue["C_BNFT_BLNC"])

        # Description
        if datadictvalue["C_DSCRPTN"]!='':
            page.get_by_role("row", name="Description", exact=True).get_by_label("Description").clear()
            page.get_by_role("row", name="Description", exact=True).get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        # Legal Employer
        if datadictvalue["C_LEGAL_EMPLYR"]!='':
            page.get_by_title("Search: Legal Employer").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Name").clear()
            page.get_by_label("Name").type(datadictvalue["C_LEGAL_EMPLYR"])
            page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search",exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_LEGAL_EMPLYR"],exact=True).click()
            page.get_by_role("button", name="OK").click()

        # Currency
        if datadictvalue["C_CRRCNCY"]!='':
            page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Currency").click()
            # page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Currency").type(datadictvalue["C_CRRCNCY"])
            page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Currency").click()
            # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CRRCNCY"],exact=True).click()

        # Balance Usage
        if datadictvalue["C_BLNC_USAGE"]!='':
            page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Balance Usage").click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_BLNC_USAGE"]).click()

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)
        try:
            expect(page.get_by_role("heading", name="Benefit Balances")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Benefit Balances Created Successfully")
            datadictvalue["RowStatus"] = "Benefit Balances Created Successfully"
        except Exception as e:
            print("Unable to Create Benefit Balances")
            datadictvalue["RowStatus"] = "Unable to Save Benefit Balances"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_BALANCES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_BALANCES,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_BALANCES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_BALANCES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_BALANCES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




