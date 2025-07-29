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
    page.get_by_role("link", name="Programs", exact=True).click()
    page.wait_for_timeout(5000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        print(i)

        page.get_by_label("Program Name").click()
        page.get_by_label("Program Name").fill("")
        page.get_by_label("Program Name").type(datadictvalue["C_PRGRM"])
        page.get_by_placeholder("mm-dd-yyyy").first.click()
        page.wait_for_timeout(1000)
        page.get_by_placeholder("mm-dd-yyyy").first.fill("")
        page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_EFFCTV_START_DATE"])
        page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(6000)


        if page.get_by_role("link", name=datadictvalue["C_PRGRM"], exact=True).is_visible():
            page.get_by_role("link", name=datadictvalue["C_PRGRM"], exact=True).click()
            page.wait_for_timeout(6000)

            if not page.locator("span").filter(has_text=re.compile(rf"^{datadictvalue['C_PLAN_TYPE']}")).first.is_visible():
                page.get_by_placeholder("mm-dd-yyyy").first.click()
                page.get_by_placeholder("mm-dd-yyyy").first.fill("")
                page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_EFFCTV_START_DATE"])
                page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
                page.wait_for_timeout(2000)
                if page.get_by_role("button", name="Yes").is_visible():
                    page.get_by_role("button", name="Yes").click()
                page.wait_for_timeout(4000)

                # Select and Add Plan Type
                page.get_by_role("button", name="Select and Add Plan Type").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Sequence").click()
                page.get_by_label("Sequence").type(str(datadictvalue["C_SEQ"]))
                page.wait_for_timeout(1000)
                page.get_by_role("combobox", name="Plan Type").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLAN_TYPE"], exact=True).click()
                page.wait_for_timeout(1000)
                page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Status").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_STTS_PLAN_TYPE"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(5000)
                print("Selected Newly added Plan type , then add Plan")
            else:
                print("Plan type is already present")

            #if not page.locator("span").filter(has_text=re.compile(rf"^{datadictvalue['C_PLAN']}")).is_visible():
            if page.locator("//span[text()='" + datadictvalue["C_PLAN_TYPE"] + "']//preceding::a[@title='Expand'][1]").is_visible():
                page.locator("//span[text()='" + datadictvalue["C_PLAN_TYPE"] + "']//preceding::a[@title='Expand'][1]").click()
                print("Expanded Plan Type")
                page.wait_for_timeout(5000)
                page.locator("span").filter(has_text=re.compile(rf"^{datadictvalue['C_PLAN_TYPE']}")).first.click()
                page.wait_for_timeout(2000)

            else:
                print("Already Plan Type got Expanded")

            if not page.locator("//span[text()='" + datadictvalue["C_PLAN_TYPE"] + "']//following::span[text()='" + datadictvalue["C_PLAN"] + "']").first.is_visible():
                
                page.get_by_placeholder("mm-dd-yyyy").first.click()
                page.get_by_placeholder("mm-dd-yyyy").first.fill("")
                page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_EFFCTV_START_DATE"])
                page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
                page.wait_for_timeout(2000)
                if page.get_by_role("button", name="Yes").is_visible():
                    page.get_by_role("button", name="Yes").click()
                page.wait_for_timeout(4000)

                #page.get_by_role("cell", name="Plan Type DSAT Dental V1", exact=True).locator("div")
                page.locator("span").filter(has_text=re.compile(rf"^{datadictvalue['C_PLAN_TYPE']}")).first.click()
                print("Plan type is available , So adding Plan")
                page.wait_for_timeout(5000)
                print("Adding Plan Type_" + datadictvalue["C_PLAN_TYPE"] +"to Plan_" + datadictvalue["C_PLAN"])
               
                # Select and Add Plan
                page.get_by_role("button", name="Select and Add Plan", exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("textbox", name="Sequence").click()
                page.get_by_role("textbox", name="Sequence").type(str(datadictvalue["C_SEQ_PLAN"]))
                page.wait_for_timeout(1000)
                page.get_by_role("combobox", name="Plan").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLAN"]).click()
                page.wait_for_timeout(1000)
                page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Status").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_STTS_PLAN"], exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(5000)
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(6000)
                print("Added Plan")
            else:
                print("Plan is already present")
                page.get_by_role("button", name="Cancel").click()
                page.wait_for_timeout(6000)

        else:
            page.get_by_role("button", name="Create", exact=True).click()
            page.wait_for_timeout(5000)
            page.get_by_placeholder("mm-dd-yyyy").first.click()
            page.get_by_placeholder("mm-dd-yyyy").first.fill("")
            page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_EFFCTV_START_DATE"])
            page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
            page.wait_for_timeout(2000)
            if page.get_by_role("button", name="Yes").is_visible():
                page.get_by_role("button", name="Yes").click()
            page.wait_for_timeout(4000)
            page.get_by_label("Program Name").click()
            page.get_by_label("Program Name").type(datadictvalue["C_PRGRM"])
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Program Type").click()
            page.get_by_text(datadictvalue["C_PRGRM_TYPE"], exact=True).click()
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Status").click()
            page.get_by_text(datadictvalue["C_STTS_PRG"], exact=True).click()
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Communicated Rate Frequency").click()
            page.get_by_text(datadictvalue["C_CMMNCTD_RATE_FRQNCY"], exact=True).click()
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Defined Rate Frequency").click()
            page.get_by_text(datadictvalue["C_DFND_RATE_FRQNCY"]).first.click()
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Rate Level").click()
            page.get_by_text(datadictvalue["C_RATE_LEVEL"]).click()
            page.wait_for_timeout(1000)
            page.get_by_title("Default Program Currency").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(1000)
            page.get_by_label("Currency Name").click()
            page.get_by_label("Currency Name").fill("")
            page.get_by_label("Currency Name").type(datadictvalue["C_DFLT_PRGRM_CRRNCY"])
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DFLT_PRGRM_CRRNCY"]).click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="Dependent Designation Level").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DPNDNT_DSGNTN_LEVEL"]).first.click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_ENBL_UNRSTRCTD_ERLLMNT"] == "Yes":
                if not page.get_by_text("Enable unrestricted enrollment").is_checked():
                    page.get_by_text("Enable unrestricted enrollment").click()
            page.wait_for_timeout(3000)

            # page.get_by_label("Short Name").click()
            # page.get_by_label("Short Code").click()
            # page.get_by_label("Interactive Voice Response Code").click()
            # page.get_by_label("Subject to Imputed Income").click()
            # page.locator("[id=\"__af_Z_window\"]").get_by_text("Dependent").click()
            # page.get_by_placeholder("mm-dd-yyyy").nth(1).fill("")
            # page.get_by_placeholder("mm-dd-yyyy").nth(1).type(datadictvalue["C_START_DATE"])
            # page.get_by_placeholder("mm-dd-yyyy").nth(1).press("Tab")
            # page.get_by_label("Web Address").click()

            # Year periods
            page.get_by_role("button", name="Select and Add").first.click()
            page.wait_for_timeout(4000)
            if page.get_by_role("button", name="Move all items to: Selected").is_visible():
                page.get_by_role("button", name="Move all items to: Selected").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(4000)

            #Select and Add Plan Type
            page.get_by_role("button", name="Select and Add Plan Type").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Sequence").click()
            page.get_by_label("Sequence").type(str(datadictvalue["C_SEQ"]))
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Plan Type").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLAN_TYPE"], exact=True).click()
            page.wait_for_timeout(1000)
            page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Status").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_STTS_PLAN_TYPE"], exact=True).click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(4000)
            page.locator("span").filter(has_text=re.compile(rf"^{datadictvalue['C_PLAN_TYPE']}")).click()
            page.wait_for_timeout(3000)

            # Select and Add Plan
            page.get_by_role("button", name="Select and Add Plan", exact=True).click()
            page.wait_for_timeout(2000)
            page.get_by_role("textbox", name="Sequence").click()
            page.get_by_role("textbox", name="Sequence").type(str(datadictvalue["C_SEQ_PLAN"]))
            page.wait_for_timeout(1000)
            page.get_by_role("combobox", name="Plan").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PLAN"]).click()
            page.wait_for_timeout(1000)
            page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Status").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_STTS_PLAN"], exact=True).click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(5000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(6000)

        
        i = i + 1

        

        try:
            expect(page.get_by_label("Program Name")).to_be_visible()
            print("Added Program-Basic Details Saved Successfully")
            datadictvalue["RowStatus"] = "Added Program-Basic Details"
        except Exception as e:
            print("Unable to save Program-Basic Details")
            datadictvalue["RowStatus"] = "Unable to Add Program-Basic Details"

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BASIC_PROGRAM_DETAILS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BASIC_PROGRAM_DETAILS,
                             PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, BASIC_PROGRAM_DETAILS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BASIC_PROGRAM_DETAILS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[
            0] + "_" + BASIC_PROGRAM_DETAILS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


