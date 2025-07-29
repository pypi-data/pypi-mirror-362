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
    page.get_by_role("link", name="Configure Plan Type Grouping").click()
    page.wait_for_timeout(5000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        if datadictvalue["C_PLAN_TYPE"] != "":
            page.get_by_role("cell", name=datadictvalue["C_PLAN_TYPE"], exact=True).click()
            page.wait_for_timeout(4000)

            if datadictvalue["C_DSPLY"] == "Yes":
                if not page.get_by_role("cell", name="Enrollment Display Name").locator("label").nth(1).is_checked():
                    page.get_by_role("cell", name="Enrollment Display Name").locator("label").nth(1).click()
                    page.wait_for_timeout(2000)

            page.get_by_role("cell", name="Enrollment Display Name").get_by_role("link").first.click()
            page.wait_for_timeout(3000)

        else:
            page.get_by_role("cell", name="Enrollment Display Name").get_by_role("link").first.click()
            page.wait_for_timeout(3000)

        if datadictvalue["C_CLMN_NUM"] == 1:
            print(datadictvalue["C_CLMN_NUM"])
            page.get_by_label("Column").nth(0).click()
            page.get_by_label("Column").nth(0).fill("")
            page.get_by_label("Column").nth(0).type(datadictvalue["C_DSPLY_NAME"])
            page.get_by_label("Column").nth(0).click()

            if datadictvalue["C_DSPLY_RATE"] == "Yes":
                if page.get_by_role("row", name="Column 1").locator("label").nth(1).is_enabled():
                    if not page.get_by_role("row", name="Column 1").locator("label").nth(1).is_checked():
                        page.get_by_role("row", name="Column 1").locator("label").nth(1).click()

        if datadictvalue["C_CLMN_NUM"] == 2:
            print(datadictvalue["C_CLMN_NUM"])
            page.get_by_label("Column").nth(1).click()
            page.get_by_label("Column").nth(1).fill("")
            page.get_by_label("Column").nth(1).type(datadictvalue["C_DSPLY_NAME"])
            page.get_by_label("Column").nth(1).click()

            if datadictvalue["C_DSPLY_RATE"] == "Yes":
                if page.get_by_role("row", name="Column 2").locator("label").nth(1).is_enabled():
                    if not page.get_by_role("row", name="Column 2").locator("label").nth(1).is_checked():
                        page.get_by_role("row", name="Column 2").locator("label").nth(1).click()

        if datadictvalue["C_CLMN_NUM"] == 3:
            print(datadictvalue["C_CLMN_NUM"])
            page.get_by_label("Column").nth(2).click()
            page.get_by_label("Column").nth(2).fill("")
            page.get_by_label("Column").nth(2).type(datadictvalue["C_DSPLY_NAME"])
            page.get_by_label("Column").nth(2).click()

            if datadictvalue["C_DSPLY_RATE"] == "Yes":
                if page.get_by_role("row", name="Column 3").locator("label").nth(1).is_enabled():
                    if not page.get_by_role("row", name="Column 3").locator("label").nth(1).is_checked():
                        page.get_by_role("row", name="Column 3").locator("label").nth(1).click()

        if datadictvalue["C_CLMN_NUM"] == 4:
            print(datadictvalue["C_CLMN_NUM"])
            page.get_by_label("Column").nth(3).click()
            page.get_by_label("Column").nth(3).fill("")
            page.get_by_label("Column").nth(3).type(datadictvalue["C_DSPLY_NAME"])
            page.get_by_label("Column").nth(3).click()

            if datadictvalue["C_DSPLY_RATE"] == "Yes":
                if page.get_by_role("row", name="Column 4").locator("label").nth(1).is_enabled():
                    if not page.get_by_role("row", name="Column 4").locator("label").nth(1).is_checked():
                        page.get_by_role("row", name="Column 4").locator("label").nth(1).click()

        page.wait_for_timeout(1000)
        page.get_by_role("button", name="OK").click()
        print(i)
        page.wait_for_timeout(4000)
        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Plan Grouping")).to_be_visible()
            print("Added Plan Grouping Saved Successfully")
            datadictvalue["RowStatus"] = "Added Plan Grouping"
        except Exception as e:
            print("Unable to save Plan Grouping")
            datadictvalue["RowStatus"] = "Unable to Add Plan Grouping"


    page.get_by_role("button", name="Save").click()
    page.wait_for_timeout(6000)

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, CONFIG_PLANTYPE_GROUPING_DISPLAY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, CONFIG_PLANTYPE_GROUPING_DISPLAY,
                             PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, CONFIG_PLANTYPE_GROUPING_DISPLAY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[
            0] + "_" + CONFIG_PLANTYPE_GROUPING_DISPLAY + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


