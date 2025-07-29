from playwright.sync_api import Playwright, sync_playwright
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    # Navigation
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Benefits Administration", exact=True).click()
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Programs and Plans").click()
    page.get_by_role("link", name="Plans", exact=True).click()


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        if datadictvalue["C_PLAN_NAME"] != "":

            print(str(i) + "_" + str(rowcount))
            page.get_by_label("Plan Name").click()
            page.get_by_label("Plan Name").type(datadictvalue["C_PLAN_NAME"])
            page.wait_for_timeout(2000)
            page.get_by_placeholder("m/d/yy").first.click()
            page.get_by_placeholder("m/d/yy").first.fill("")
            page.get_by_placeholder("m/d/yy").first.type(datadictvalue["C_EFFCTV _START_DATE"])
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(5000)
            page.get_by_role("link", name=datadictvalue["C_PLAN_NAME"]).click()
            page.wait_for_timeout(5000)
            page.get_by_label("Certifications Step: Not Visited").click()
            page.wait_for_timeout(5000)
            page.get_by_text(datadictvalue["C_PLAN_NAME"], exact=True).click()
            page.wait_for_timeout(4000)
            page.get_by_role("link", name="Life Event").click()
            page.wait_for_timeout(5000)

            j = 0
            while j < rowcount:
                datadictvalue = datadict[j]


                print("Life Event Name" + "-" +datadictvalue["C_LIFE_EVENT_NAME"])
                # page.locator("//a[contains(@id,':0:navList1::drop')]").click()
                # if page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LIFE_EVENT_NAME"]).is_visible():
                #     page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LIFE_EVENT_NAME"]).click()

                if datadictvalue["C_LIFE_EVENT_NAME"] != "":

                    page.get_by_role("button", name="Add Life Event").first.click()
                    page.wait_for_timeout(4000)
                    #if page.get_by_role("listitem", name=datadictvalue["C_LIFE_EVENT_NAME"]).is_visible():
                    page.get_by_role("listitem", name=datadictvalue["C_LIFE_EVENT_NAME"]).click()
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(2000)
                    if datadictvalue["C_SUSPEND_ENROLLMENT"] == "Yes":
                        page.get_by_text("Suspend enrollment").click()

                    if datadictvalue["C_REQUIRED"] == "Yes":
                        page.get_by_text("Required").first.click()

                    page.get_by_role("combobox", name="Due Date", exact=True).click()
                    page.get_by_text(datadictvalue["C_DUE_DATE"]).click()
                    page.wait_for_timeout(2000)

                if datadictvalue["C_CRTFCTN_TYPE"] != "":
                    page.get_by_role("button", name="Select and Add").click()
                    page.wait_for_timeout(2000)
                    page.get_by_role("combobox", name="Certification Type").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CRTFCTN_TYPE"]).click()
                    page.wait_for_timeout(2000)
                    if datadictvalue["C_RQRD"] == "Yes":
                        page.locator("[id=\"__af_Z_window\"]").get_by_text("Required", exact=True).click()
                    page.wait_for_timeout(1000)
                    if datadictvalue["C_DTRMNTN_RULE"] == "Formula":
                        page.get_by_role("combobox", name="Determination Rule").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DTRMNTN_RULE"], exact=True).click()
                        page.wait_for_timeout(5000)
                        page.get_by_role("combobox", name="Determination Formula").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DTRMNTN_FRML"]).click()
                        page.wait_for_timeout(2000)
                        page.get_by_role("button", name="OK").click()
                        page.wait_for_timeout(2000)

                page.get_by_role("button", name="Save", exact=True).click()
                page.wait_for_timeout(4000)

                try:
                    #expect(page.get_by_role("heading", name="Overview")).to_be_visible()
                    page.wait_for_timeout(3000)
                    print("Benefit Plan Certifications Created Successfully")
                    datadictvalue["RowStatus"] = "Benefit Plan Certifications Created Successfully"
                except Exception as e:
                    print("Unable to Create Benefit Plan Certifications")
                    datadictvalue["RowStatus"] = "Unable to Save Benefit Plan Certifications"

                j = j + 1


            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(5000)

        else:
            print("PLAN NAME not provided in Sheet")

        i = i + 1

        # try:
        #     expect(page.get_by_role("heading", name="Overview")).to_be_visible()
        #     page.wait_for_timeout(3000)
        #     print("Benefit Plan Certifications Created Successfully")
        #     datadictvalue["RowStatus"] = "Benefit Plan Certifications Created Successfully"
        # except Exception as e:
        #     print("Unable to Create Benefit Plan Certifications")
        #     datadictvalue["RowStatus"] = "Unable to Save Benefit Plan Certifications"


    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_PRGM_CERT_UPLOAD):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_PRGM_CERT_UPLOAD,
                             PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_PRGM_CERT_UPLOAD)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_PRGM_CERT_UPLOAD)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[
            0] + "_" + BENEFIT_PRGM_CERT_UPLOAD + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


