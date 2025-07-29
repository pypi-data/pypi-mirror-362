from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)

    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    # Navigate to Derived Factors page
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("Benefits Administration", exact=True).click()
    page.get_by_role("link", name="Plan Configuration").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Derived Factors").click()
    page.get_by_role("link", name="Age and Service", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)
        print(i)
        page.get_by_role("button", name="Create", exact=True).click()
        page.wait_for_timeout(3000)

        # Entering Name
        page.locator("//div[text()='Create Derived Factor Age and Service']//following::label[text()='Name']//following::input[1]").type(datadictvalue["C_NAME"])

        # Age Factor
        if datadictvalue["C_AGE_FCTR"] != '':
            page.locator("//div[text()='Create Derived Factor Age and Service']//following::label[text()='Age Factor']//following::input[1]").click()
            page.wait_for_timeout(2000)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_AGE_FCTR"]).click(force=True)


            # if page.locator("//li[text()='" + datadictvalue["C_AGE_FCTR"] + "']").nth(1).is_visible():
            #     page.locator("//li[text()='" + datadictvalue["C_AGE_FCTR"] + "'").nth(1).click()
            #     print("Age Factor" + datadictvalue["C_AGE_FCTR"])
                #page.locator("//li[text()='" + datadictvalue["C_AGE_FCTR"] + "']").nth(1).click()
                #break

            # else:
            #     print("Scrolling")
            #     #page.locator("//table[contains(@id,':0:AT1:selectOneChoice')]").click()
            #     page.locator("//ul[@class='x1kw p_AFScroll']").nth(3).click()
            #     page.mouse.wheel(0, 500)
            #     page.wait_for_timeout(2000)


        # Length of Service Factor
        if datadictvalue["C_LNGTH_OF_SRVC_FCTR"] != '':
            page.locator("//div[text()='Create Derived Factor Age and Service']//following::label[text()='Length of Service Factor']//following::input[1]").click()
            page.wait_for_timeout(2000)

            if page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LNGTH_OF_SRVC_FCTR"]).is_visible():
                print("Age Factor" + datadictvalue["C_AGE_FCTR"])
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LNGTH_OF_SRVC_FCTR"]).click()

            # else:
            #     print("Scrolling")
            #     #page.locator("//table[contains(@id,':0:AT1:selectOneChoice')]").click()
            #     #page.locator("//ul[@aria-label='Length of Service Factor']").click()
            #     page.mouse.wheel(0, 500)
            #     page.pause()
            #     page.wait_for_timeout(2000)


        # Greater than or Equal to Age and Service
        if datadictvalue["C_GRTR_THAN_OR_EQUAL_TO_AGE_AND_SRVC"]!='':
            page.get_by_label("Greater than or Equal to Age").clear()
            page.get_by_label("Greater than or Equal to Age").type(str(datadictvalue["C_GRTR_THAN_OR_EQUAL_TO_AGE_AND_SRVC"]))

        # Less Than Age and Service
        if datadictvalue["C_LESS_THAN_AGE_AND_SRVC"] != '':
            page.get_by_label("Less Than Age and Service").click()
            page.get_by_label("Less Than Age and Service").type(str(datadictvalue["C_LESS_THAN_AGE_AND_SRVC"]))

        #context.tracing.stop(path="trace.zip")
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(2000)

        try:
            expect(page.get_by_role("heading", name="Derived Factors")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Derived Factor Age&Service Created Successfully")
            datadictvalue["RowStatus"] = "Derived Factor Age&Service Created Successfully"
        except Exception as e:
            print("Unable to Create Derived Factor Age&Service")
            datadictvalue["RowStatus"] = "Unable to Save Derived Factor Age&Service"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, DERIVEDFACTORS_AGEANDSERVICE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, DERIVEDFACTORS_AGEANDSERVICE,PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, DERIVEDFACTORS_AGEANDSERVICE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + DERIVEDFACTORS_AGEANDSERVICE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + DERIVEDFACTORS_AGEANDSERVICE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
