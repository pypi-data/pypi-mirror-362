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
        page.wait_for_timeout(4000)

        page.get_by_label("Add", exact=True).click()
        page.wait_for_timeout(5000)

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
        page.get_by_role("combobox", name="Contact").click()
        page.get_by_role("combobox", name="Contact").fill("Adam Land")
        page.get_by_text("Adam Land").click()
        page.wait_for_timeout(3000)

        # Training Supplier
        if datadictvalue["C_TRNNG_SPPLR"] != '':
            page.get_by_role("combobox", name="Training Supplier").click()
            page.get_by_role("combobox", name="Training Supplier").fill(datadictvalue["C_TRNNG_SPPLR"])
            page.get_by_text(datadictvalue["C_TRNNG_SPPLR"]).click()
            page.wait_for_timeout(3000)

        # Context Segment
        if datadictvalue["C_CNTXT_SEG"] != '':
            page.get_by_role("combobox", name="Context Segment").click()
            page.get_by_role("combobox", name="Context Segment").fill(datadictvalue["C_CNTXT_SEG"])
            page.get_by_text(datadictvalue["C_CNTXT_SEG"]).click()
            page.wait_for_timeout(3000)

        # Location
        if datadictvalue["C_LCTN_DTLS"] != '':
            page.get_by_role("combobox", name="Location").click()
            page.get_by_role("combobox", name="Location").fill(datadictvalue["C_LCTN_DTLS"])
            page.get_by_text(datadictvalue["C_LCTN_DTLS"]).click()
            page.wait_for_timeout(3000)

        # Visible To
        if datadictvalue["C_VSBL_TO"] != '':
            page.get_by_role("combobox", name="Visible To").click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_VSBL_TO"]).click()
            page.wait_for_timeout(3000)

        # if datadictvalue["C_PDF_FILE"] != '':
        #     with page.expect_file_chooser() as fc_info:
        #         page.locator("//a[text()='Drag and drop a PDF file here or browse for a PDF file to upload.']").click()
        #     file_chooser = fc_info.value
        #     file_chooser.set_files("attachment/Fire-Drills-Procedures.pdf")
        #     page.wait_for_timeout(15000)

        # Add URL
        if datadictvalue["C_URL"] != '':
            page.get_by_role("textbox", name="URL").click()
            page.get_by_role("textbox", name="URL").fill(datadictvalue["C_URL"])
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Add URL").click()
            page.wait_for_timeout(3000)

        page.pause()

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
