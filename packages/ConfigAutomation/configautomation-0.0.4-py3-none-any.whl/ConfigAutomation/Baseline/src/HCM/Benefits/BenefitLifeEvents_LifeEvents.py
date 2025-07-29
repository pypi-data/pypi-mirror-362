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

    # Navigate to BenefitLifeEvents-Life Events page
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Benefits Administration", exact=True).click()
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Benefit Life Events").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(3000)

        # Effective Date
        page.get_by_placeholder("mm-dd-yyyy").clear()
        page.get_by_placeholder("mm-dd-yyyy").type(datadictvalue["C_EFFCTV_START_DATE"])
        page.get_by_placeholder("mm-dd-yyyy").press("Enter")
        page.wait_for_timeout(3000)
        if page.get_by_role("button", name="Yes").is_visible():
            page.get_by_role("button", name="Yes").click()


        # Life Event Name
        if datadictvalue["C_LIFE_EVENT_NAME"]!="":
            page.get_by_label("Name", exact=True).click()
            page.wait_for_timeout(5000)
            page.get_by_label("Name", exact=True).type(datadictvalue["C_LIFE_EVENT_NAME"])
        # Life Event Description
        if datadictvalue["C_DSCRPTN"]!="":
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.wait_for_timeout(2000)
        # Life Event Type
        if datadictvalue["C_LIFE_EVENT_TYPE"]!="":
            page.get_by_role("combobox", name="Type", exact=True).click()
            page.get_by_role("listbox").get_by_text(datadictvalue["C_LIFE_EVENT_TYPE"], exact=True).click()
        # Selecting Global
        if datadictvalue["C_GLBL"]=="Yes":
            page.get_by_text("Global", exact=True).check()
        # Selecting Override
        if datadictvalue["C_OVRRD"]=="Yes":
            page.get_by_text("Override", exact=True).click()
        # Expanding Additional Informaion panel
        if page.get_by_label("Expand Additional Information").is_visible():
            page.get_by_label("Expand Additional Information").click()
        # Selecting Timeliness Evaluation
        if datadictvalue["C_TMLNSS_EVLTN"]!="":
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Timeliness Evaluation").click()
            page.get_by_role("listbox").get_by_text(datadictvalue["C_TMLNSS_EVLTN"], exact=True).click()
            # Selecting Timeliness Days
            page.get_by_label("Timeliness Days").clear()
            page.get_by_label("Timeliness Days").type(str(datadictvalue["C_TMLNSS_DAYS"]))
        # Selecting Self-Assigned
        if datadictvalue["C_SELF_ASSGND"]=="Yes":
            page.get_by_text("Self-Assigned").click()
            page.wait_for_timeout(3000)
            # Entering Life Event Instruction Text
            page.get_by_label("Life Event Instruction Text").type(datadictvalue["C_LIFE_EVENT_INSTRCTN_TEXT"])
        # Selecting Person Change Details
        if datadictvalue["C_PRSN_CHNG"]!="":
            page.get_by_role("link", name="Person Changes", exact=True).click()
            page.get_by_role("button", name="Add", exact=True).click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Person Change").click()
            page.wait_for_timeout(3000)
            page.get_by_role("listbox").get_by_text(datadictvalue["C_PRSN_CHNG"], exact=True).click()
        # Saving and Closing the entry
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        try:
            expect(page.get_by_role("heading", name="Life Events")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Life Event Created Successfully")
            datadictvalue["RowStatus"] = "Created Life Events Successfully"
        except Exception as e:
            print("Unable to Save Life Event")
            datadictvalue["RowStatus"] = "Unable to Save Life Event"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, LIFEEVENTS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, LIFEEVENTS,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, LIFEEVENTS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + LIFEEVENTS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + LIFEEVENTS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
