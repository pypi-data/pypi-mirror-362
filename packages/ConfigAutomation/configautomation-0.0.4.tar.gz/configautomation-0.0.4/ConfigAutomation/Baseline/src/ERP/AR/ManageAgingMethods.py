from playwright.sync_api import Playwright, sync_playwright
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(5000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Aging Methods")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Aging Methods", exact=True).click()


    i = 0

    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        if i == 0:
            page.get_by_role("button", name="Add Row").first.click()
            page.wait_for_timeout(4000)
            page.get_by_role("row", name="Aging Method Name").get_by_label("Aging Method Name").nth(0).fill(datadictvalue["C_AGING_MTHD_NAME"])
            page.get_by_role("row", name="Aging Method Name").get_by_label("Aging Type").nth(0).select_option(datadictvalue["C_AGING_TYPE"])
            page.get_by_role("row", name="Aging Method Name").get_by_label("Enabled").nth(0).select_option(datadictvalue["C_ENBLD"])
            page.get_by_role("row", name="Aging Method Name").get_by_label("Aging Method Set").nth(0).select_option(datadictvalue["C_AGING_MTHD_SET"])
            page.get_by_role("row", name="Aging Method Description").get_by_label("Aging Method Description").nth(0).fill(datadictvalue["C_AGING_MTHD_DSCRPTN"])
            page.get_by_role("button", name="Save", exact=True).click()

            page.wait_for_timeout(2000)
            page.get_by_text("Current").click()

        if i > 0:
            j = i + 1
            # print("J value:", j)
            # print("Aging days to:",datadictvalue["C_AGING_DAYS_TO"])
            if datadictvalue["C_AGING_DAYS_TO"] != 9999:
                page.get_by_role("button", name="Add Row").nth(1).click()
                page.wait_for_timeout(3000)
                page.get_by_role("cell", name="Aging Days From").nth(j).get_by_label("Aging Days From").clear()
                page.get_by_role("cell", name="Aging Days From").nth(j).get_by_label("Aging Days From").fill(str(datadictvalue["C_AGING_DAYS_FROM"]))
                page.get_by_role("cell", name="Aging Days To").nth(j).get_by_label("Aging Days To").clear()
                page.get_by_role("cell", name="Aging Days To").nth(j).get_by_label("Aging Days To").fill(str(datadictvalue["C_AGING_DAYS_TO"]))
                page.get_by_role("cell", name="Aging Bucket Heading").get_by_label("Aging Bucket Heading", exact=True).nth(i).clear()
                page.get_by_role("cell", name="Aging Bucket Heading").get_by_label("Aging Bucket Heading", exact=True).nth(i).fill(datadictvalue["C_AGING_BCKT_HDNG"])
                page.wait_for_timeout(4000)

            if datadictvalue["C_AGING_DAYS_TO"] == 9999:
                page.get_by_role("cell", name="Aging Days From").nth(j).get_by_label("Aging Days From").clear()
                page.get_by_role("cell", name="Aging Days From").nth(j).get_by_label("Aging Days From").fill(str(datadictvalue["C_AGING_DAYS_FROM"]))
                if page.get_by_role("cell", name="Aging Days To").nth(j).get_by_label("Aging Days To").is_enabled():
                    page.get_by_role("cell", name="Aging Days To").nth(j).get_by_label("Aging Days To").fill(str(datadictvalue["C_AGING_DAYS_TO"]))
                page.get_by_role("cell", name="Aging Bucket Heading").get_by_label("Aging Bucket Heading", exact=True).nth(i).clear()
                page.get_by_role("cell", name="Aging Bucket Heading").get_by_label("Aging Bucket Heading", exact=True).nth(i).fill(datadictvalue["C_AGING_BCKT_HDNG"])

        i = i + 1

    page.get_by_role("button", name="Save and Close").click()



    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, AR_AGING_METHODS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, AR_AGING_METHODS, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, AR_AGING_METHODS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + AR_AGING_METHODS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + AR_AGING_METHODS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))