from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("My Client Groups", exact=True).click()
    page.get_by_role("link", name="Learning").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Classrooms").click()
    page.wait_for_timeout(3000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_label("Add", exact=True).click()
        page.wait_for_timeout(3000)

        # Title
        page.get_by_label("Name", exact=True).clear()
        page.get_by_label("Name", exact=True).type(datadictvalue["C_TITLE"])

        # Description
        page.get_by_role("textbox", name="Description").clear()
        page.get_by_role("textbox", name="Description").type(datadictvalue["C_DSCRPTN"])

        # Capacity
        page.get_by_label("Seating Capacity").clear()
        page.get_by_label("Seating Capacity").type(str(datadictvalue["C_CPCTY"]))

        # Contact
        # page.locator("//label[text()='Contact']//following::a[1]").click()
        # page.wait_for_timeout(3000)
        # page.get_by_role("button", name="Advanced").click()
        # page.get_by_label("Contact Name Operator").click()
        # page.get_by_text("Equals").click()
        # page.get_by_label("Contact Name", exact=True).clear()
        # page.get_by_label("Contact Name", exact=True).type(datadictvalue["C_CNTCT"])
        # page.get_by_role("button", name="Search", exact=True).click()
        # page.wait_for_timeout(2000)
        # page.get_by_text(datadictvalue["C_CNTCT"],exact=True).click()
        # page.get_by_role("button", name="OK").click()
        if datadictvalue["C_CNTCT"] != '':
            page.get_by_role("combobox", name="Contact").fill(datadictvalue["C_CNTCT"])
            page.get_by_text(datadictvalue["C_CNTCT"], exact=True).click()

        #Training Supplier
        if datadictvalue["C_TRNNG_SPPLR"] != '':
            page.get_by_role("combobox", name="Training Supplier").fill(datadictvalue["C_TRNNG_SPPLR"])
            page.get_by_text(datadictvalue["C_TRNNG_SPPLR"], exact=True).click()

        # Location
        # page.get_by_role("link", name="Select Named Location").click()
        # page.wait_for_timeout(2000)
        # page.get_by_label("Name").clear()
        # page.get_by_label("Name").type(datadictvalue["C_LCTN_DTLS"])
        # page.get_by_role("button", name="Search", exact=True).click()
        # page.wait_for_timeout(2000)
        # page.get_by_text(datadictvalue["C_LCTN_DTLS"],exact=True).first.click()
        # page.get_by_role("button", name="Select").click()
        if datadictvalue["C_LCTN_DTLS"] != '':
            page.get_by_text("Select an existing location").click()
            page.get_by_role("combobox", name="Location").fill(datadictvalue["C_LCTN_DTLS"])
            page.get_by_text(datadictvalue["C_LCTN_DTLS"]).click()
        if datadictvalue[""] == 'Add a new location':
            page.get_by_text("Add a new location").click()
            page.get_by_role("combobox", name="Country").click()
            page.get_by_role("combobox", name="Country").fill("United States")
            page.get_by_text("US United States").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Address Line 1").fill("test")
            page.get_by_label("Address Line 2").fill("test1")
            page.get_by_label("Address Line 3").fill("test2")
            page.locator("//input[contains(@id,'PostalCode')]//following::a[1]").nth(1).click()
            page.get_by_role("combobox", name="ZIP Code").fill("10010")


        # Training Supplier
        # if datadictvalue["C_TRNNG_SPPLR"]!='':
        #     page.get_by_role("link", name="Search: Training Supplier").click()
        #     page.wait_for_timeout(2000)
        #     page.get_by_role("textbox", name="Name").clear()
        #     page.get_by_role("textbox", name="Name").type(datadictvalue["C_TRNNG_SPPLR"])
        #     page.get_by_role("button", name="Search", exact=True).click()
        #     page.wait_for_timeout(2000)
        #     page.get_by_text(datadictvalue["C_TRNNG_SPPLR"], exact=True).first.click()
        #     page.get_by_role("button", name="OK").click()

        # Click on Save and Close button
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Classrooms")).to_be_visible()
            print("Classroom Saved Successfully")
            datadictvalue["RowStatus"] = "Classroom Saved Successfully"
        except Exception as e:
            print("Classroom not saved")
            datadictvalue["RowStatus"] = "Classroom not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, CLASSROOM):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK, CLASSROOM, PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + LEARNINGS_CONFIG_WRKBK, CLASSROOM)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", LEARNINGS_CONFIG_WRKBK)[0] + "_" + CLASSROOM + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))