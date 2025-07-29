from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Navigator").click()
    page.wait_for_timeout(2000)
    page.get_by_title("Benefits Administration", exact=True).click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.get_by_role("link", name="Plan Types", exact=True).click()
    page.wait_for_timeout(4000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)
        page.get_by_placeholder("mm-dd-yyyy").first.fill("")
        page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_EFFCTV_START_DATE"])
        page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
        page.wait_for_timeout(4000)
        if page.get_by_role("button", name="Yes").is_visible():
            page.get_by_role("button", name="Yes").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Plan Type Name", exact=True).click()
        page.get_by_label("Plan Type Name", exact=True).type(datadictvalue["C_PLAN_TYPE"])
        page.get_by_label("Plan Type Name", exact=True).press("Tab")
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Option Type").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OPTN_TYPE"]).click()
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Self-Service Grouping").click()
        if page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SELF_SRVC_GRPNG"], exact=True).is_visible():
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SELF_SRVC_GRPNG"], exact=True).click()
        elif page.get_by_text(datadictvalue["C_SELF_SRVC_GRPNG"], exact=True).is_visible():
            page.get_by_text(datadictvalue["C_SELF_SRVC_GRPNG"], exact=True).click()
        #page.get_by_text(datadictvalue["C_SELF_SRVC_GRPNG"]).first.click()
        page.wait_for_timeout(1000)
        page.get_by_label("Minimum Plan Enrollment").click()
        page.get_by_label("Minimum Plan Enrollment").type(str(datadictvalue["C_MIN_PLAN_ENRLLMNT"]))
        page.get_by_label("Maximum Plan Enrollment").click()
        page.get_by_label("Maximum Plan Enrollment").type(str(datadictvalue["C_MAX_PLAN_ENRLLMNT"]))

        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(6000)
        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Plan Types")).to_be_visible()
            print("Added Plan Types Saved Successfully")
            datadictvalue["RowStatus"] = "Added Plan Types"
        except Exception as e:
            print("Unable to save Plan Types")
            datadictvalue["RowStatus"] = "Unable to Add Plan Types"


    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, PLAN_TYPES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, PLAN_TYPES,
                             PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, PLAN_TYPES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + PLAN_TYPES)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[
            0] + "_" + PLAN_TYPES + "_" + PLAN_TYPES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


