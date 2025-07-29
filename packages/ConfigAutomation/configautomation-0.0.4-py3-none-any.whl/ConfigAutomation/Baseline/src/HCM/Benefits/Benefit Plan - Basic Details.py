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
    page.get_by_role("link", name="Plans", exact=True).click()
    page.wait_for_timeout(5000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        page.get_by_label("Plan Name").click()
        page.get_by_label("Plan Name").fill("")
        page.get_by_label("Plan Name").type(datadictvalue["C_PLAN_NAME"])
        page.get_by_placeholder("mm-dd-yyyy").first.fill("")
        page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_SSSN_EFFCTV_DATE"])
        page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(5000)

        if page.get_by_role("link", name=datadictvalue["C_PLAN_NAME"], exact=True).is_visible():

            if datadictvalue["C_OPTN_NAME"] != "":
                page.get_by_role("link", name=datadictvalue["C_PLAN_NAME"], exact=True).click()
                page.wait_for_timeout(5000)
                print(datadictvalue["C_OPTN_NAME"])
                if not page.get_by_role("cell", name=datadictvalue["C_OPTN_NAME"], exact=True).locator("span").nth(1).is_visible():
                    #Add Options
                    page.get_by_role("button", name="Select and Add").nth(1).click()
                    page.wait_for_timeout(2000)
                    page.get_by_title("Option Name").click()
                    page.get_by_role("link", name="More...").click()
                    page.wait_for_timeout(2000)
                    page.locator("//tbody/tr/td/span[text()='" + datadictvalue["C_OPTN_NAME"] + "']").nth(1).click()
                    # page.locator("tbody").filter(has_text=re.compile(r"^\$10001$")).get_by_role("cell")
                    page.wait_for_timeout(1000)
                    page.get_by_role("button", name="OK").nth(1).click()
                    page.wait_for_timeout(1000)
                    page.get_by_label("Sequence").click()
                    page.get_by_label("Sequence").type(str(datadictvalue["C_SEQ"]))
                    page.wait_for_timeout(1000)
                    page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Status").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_STTS_OPT"], exact=True).click()
                    page.wait_for_timeout(1000)
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(3000)
                else:
                    print("Option already exists")
                page.get_by_role("button", name="Save and Close").click()

            else:
                print("Plan name already exists and doesnt have any option to add")

        else:
            page.get_by_role("button", name="Create", exact=True).click()
            page.wait_for_timeout(5000)
            page.get_by_placeholder("mm-dd-yyyy").first.fill("")
            page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_SSSN_EFFCTV_DATE"])
            page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
            page.wait_for_timeout(2000)
            if page.get_by_role("button", name="Yes").is_visible():
                page.get_by_role("button", name="Yes").click()
            page.wait_for_timeout(4000)
            page.get_by_label("Plan Name").click()
            page.get_by_label("Plan Name").type(datadictvalue["C_PLAN_NAME"])
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Plan Type").click()
            page.get_by_text(datadictvalue["C_PLAN_TYPE"], exact=True).first.click()
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Usage").click()
            page.get_by_text(datadictvalue["C_USAGE"], exact=True).click()
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Plan Function").click()
            page.get_by_text(datadictvalue["C_PLAN_FNCTN"]).click()
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Status").click()
            page.get_by_text(datadictvalue["C_STTUS"], exact=True).click()
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Rate Level").click()
            page.get_by_text(datadictvalue["C_RATE_LEVEL"]).click()
            page.wait_for_timeout(1000)

            #if datadictvalue["C_GLOBAL_PLAN"] == "Yes":
            # if page.get_by_role("img", name="checked").is_enabled():
            #     if page.get_by_role("img", name="checked").is_checked():
            #         page.get_by_role("img", name="checked").click()
            # page.wait_for_timeout(1000)
            if datadictvalue["C_ENBL_UNRSTRCTD_ENRLLMNT"] == "Yes":
                if not page.get_by_text("Enable unrestricted enrollment").is_checked():
                    page.get_by_text("Enable unrestricted enrollment").click()

            # page.get_by_label("Short Name").click()
            # page.get_by_label("Short Code").click()
            # page.get_by_label("Interactive Voice Response Code").click()
            # page.get_by_label("Subject to Imputed Income").click()
            # page.locator("[id=\"__af_Z_window\"]").get_by_text("Dependent").click()
            if datadictvalue["C_INCPTN_DATE"] != "":
                page.get_by_placeholder("mm-dd-yyyy").nth(1).fill("")
                page.get_by_placeholder("mm-dd-yyyy").nth(1).type(datadictvalue["C_INCPTN_DATE"])
                page.get_by_placeholder("mm-dd-yyyy").nth(1).press("Tab")
            # page.get_by_label("Web Address").click()
            page.wait_for_timeout(4000)

            #Year periods
            page.get_by_role("button", name="Select and Add").first.click()
            page.wait_for_timeout(4000)
            if page.get_by_role("button", name="Move all items to: Selected").is_visible():
                page.get_by_role("button", name="Move all items to: Selected").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(4000)

            if datadictvalue["C_OPTN_NAME"] != "":
                #Add Options
                page.get_by_role("button", name="Select and Add").nth(1).click()
                page.wait_for_timeout(2000)
                page.get_by_title("Option Name").click()
                page.get_by_role("link", name="More...").click()
                page.wait_for_timeout(2000)
                page.locator("//tbody/tr/td/span[text()='" + datadictvalue["C_OPTN_NAME"] + "']").nth(1).click()
                #page.locator("tbody").filter(has_text=re.compile(r"^\$10001$")).get_by_role("cell")
                #page.locator("tbody").filter(has_text=re.compile(rf"^{datadictvalue['C_OPTN_NAME']}")).get_by_role("cell").click()
                page.wait_for_timeout(1000)
                page.get_by_role("button", name="OK").nth(1).click()
                page.wait_for_timeout(1000)
                page.get_by_label("Sequence").click()
                page.get_by_label("Sequence").type(str(datadictvalue["C_SEQ"]))
                page.wait_for_timeout(1000)
                page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Status").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_STTS_OPT"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(5000)
                #page.get_by_role("button", name="Save", exact=True)
            page.get_by_role("button", name="Save and Close").click()

        page.wait_for_timeout(6000)
        i = i + 1
        print(i)

        try:
            expect(page.get_by_role("link", name="Plans", exact=True)).to_be_visible()
            print("Added Plan-Basic Details Saved Successfully")
            datadictvalue["RowStatus"] = "Added Plan-Basic Details"
        except Exception as e:
            print("Unable to save Plan-Basic Details")
            datadictvalue["RowStatus"] = "Unable to Add Plan-Basic Details"

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BASIC_PLAN_DETAILS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BASIC_PLAN_DETAILS,
                             PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, BASIC_PLAN_DETAILS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BASIC_PLAN_DETAILS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[
            0] + "_" + BASIC_PLAN_DETAILS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


