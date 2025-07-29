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

        if datadictvalue["C_PRGRM"] != "":
            page.get_by_label("Program Name").click()
            page.get_by_label("Program Name").fill("")
            page.get_by_label("Program Name").type(datadictvalue["C_PRGRM"])
            page.get_by_placeholder("mm-dd-yyyy").first.click()
            page.wait_for_timeout(1000)
            page.get_by_placeholder("mm-dd-yyyy").first.fill("")
            page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_EFFCTV_DATE"])
            page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(6000)
            if page.get_by_role("link", name=datadictvalue["C_PRGRM"], exact=True).is_visible():
                page.get_by_role("link", name=datadictvalue["C_PRGRM"], exact=True).click()
                page.wait_for_timeout(6000)

            page.get_by_role("link", name="Enrollment").click()
            page.wait_for_timeout(5000)

            # Click on Program Name
            page.get_by_text(datadictvalue["C_PRGRM"], exact=True).click()
            page.wait_for_timeout(3000)

        else:
            break

        # j = 34
        # while j < rowcount:
        #     datadictvalue = datadict[j]
        #     print(j)
        j = 0
        while j < rowcount:
            datadictvalue = datadict[j]
            print(j)

            # Depending on the datasheet select either Plan Type or Plan Name
            #if we select Plan Type
            if datadictvalue["C_PLAN_TYPE"] != "":
                k = 1
                while k > 0:

                    if page.locator("//span[text()='" + datadictvalue["C_PLAN_TYPE"] + "']//following::span[text()='Plan Type']").first.is_visible():
                        print("Plan Type" +"-"+ datadictvalue["C_PLAN_TYPE"])
                        page.locator("//span[text()='" + datadictvalue["C_PLAN_TYPE"] + "']//following::span[text()='Plan Type']").first.click()
                        break
                    else:
                        #page.locator("//table[@summary='Program Enrollment Requirements']").nth(1).click()
                        #page.wait_for_timeout(2000)
                        page.mouse.wheel(0, 200)
                        #page.locator("//div[contains(@id,'scroller')]").first.click()
                        page.wait_for_timeout(2000)

                    k = k + 1

                if not page.locator("//span[text()='" + datadictvalue["C_PLAN_TYPE"] + "']//following::span[text()='Plan Type']//following::img[@title='Yes']").first.is_visible():
                    page.wait_for_timeout(4000)
                    page.get_by_role("link", name="Actions", exact=True).click()
                    page.wait_for_timeout(1000)
                    page.locator("[id=\"__af_Z_window\"]").get_by_text("Correct").click()
                    page.wait_for_timeout(2000)
                    if datadictvalue["C_ENRLLMNT_MTHD"] != "":
                        page.get_by_role("combobox", name="Enrollment Method").click()
                        # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ENRLLMNT_MTHD"], exact=True).click()
                        page.get_by_text(datadictvalue["C_ENRLLMNT_MTHD"], exact=True).click()

                    page.get_by_role("combobox", name="Enrollment Rule", exact=True).click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ENRLLMNT_RULE"]).click()
                    page.get_by_role("combobox", name="Default Enrollment Rule", exact=True).click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DFLT_ENRLLMNT_RULE"]).click()
                    if datadictvalue["C_INTRM_RULE"] != "":
                        page.get_by_role("combobox", name="Interim Rule", exact=True).click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_INTRM_RULE"]).click()
                    if datadictvalue["C_UNSSPND_ENRLLMNT_RULE"] != "":
                        page.get_by_role("combobox", name="Unsuspend Enrollment Rule", exact=True).click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_UNSSPND_ENRLLMNT_RULE"]).click()
                    if datadictvalue["C_UNSSPND_RATE_RULE"] != "":
                        page.get_by_role("combobox", name="Unsuspend Rate Rule", exact=True).click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_UNSSPND_RATE_RULE"]).click()
                    if datadictvalue["C_NO_MNMM"] != "":
                        if not page.get_by_text("No minimum").is_checked():
                            page.get_by_text("No minimum").click()
                    if datadictvalue["C_NO_MXMM"] != "":
                        if not page.get_by_text("No maximum").is_checked():
                            page.get_by_text("No maximum").click()
                    page.wait_for_timeout(2000)
                    page.get_by_role("button", name="Save", exact=True).click()
                    page.wait_for_timeout(10000)

                    try:
                        expect(page.locator("//span[text()='" + datadictvalue["C_PLAN_TYPE"] + "']//following::span[text()='Plan Type']//following::img[@title='Yes']").first).to_be_visible()
                        print("Added Program-Enrollment to Plan Type Successfully")
                        datadictvalue["RowStatus"] = "Added Program-Enrollment to Plan Type"
                    except Exception as e:
                        print("Unable to Add Program-Enrollment to Plan Type")
                        datadictvalue["RowStatus"] = "Unable to Add Program-Enrollment to Plan Type"
                else:
                    print("Plan type Already Enrolled")
                    try:
                        expect(page.locator("//span[text()='" + datadictvalue["C_PLAN_TYPE"] + "']//following::span[text()='Plan Type']//following::img[@title='Yes']").first).to_be_visible()
                        print("Added Program-Enrollment to Plan Type Successfully")
                        datadictvalue["RowStatus"] = "Added Program-Enrollment to Plan Type"
                    except Exception as e:
                        print("Unable to Add Program-Enrollment to Plan Type")
                        datadictvalue["RowStatus"] = "Unable to Add Program-Enrollment to Plan Type"
            else:
                print("Plan Type not provided in datasheet")

            #if we select Plan
            if datadictvalue["C_PLAN"] != "":
                k = j + 1
                while k > 0:

                    if page.locator("//span[text()='" + datadictvalue["C_PLAN"] + "']//following::span[text()='Plan']").first.is_visible():
                        print("Plan Name" +"-"+ datadictvalue["C_PLAN"])
                        page.locator("//span[text()='" + datadictvalue["C_PLAN"] + "']//following::span[text()='Plan']").first.click()
                        break
                    else:
                        #page.locator("//table[@summary='Program Enrollment Requirements']").first.click()
                        #page.wait_for_timeout(2000)
                        page.mouse.wheel(0, 200)
                        page.wait_for_timeout(2000)
                        #page.locator("//div[contains(@id,'scroller')]").first.click()

                    k = k + 1

                if not page.locator("//span[text()='" + datadictvalue["C_PLAN"] + "']//following::span[text()='Plan']//following::img[@title='Yes']").first.is_visible():

                    if datadictvalue["C_ENRLLMNT_MTHD"] != "":

                        page.wait_for_timeout(4000)
                        page.get_by_role("link", name="Actions", exact=True).click()
                        page.wait_for_timeout(1000)
                        page.locator("[id=\"__af_Z_window\"]").get_by_text("Correct").click()
                        page.wait_for_timeout(2000)
                        page.get_by_role("combobox", name="Enrollment Method").click()
                        page.get_by_text(datadictvalue["C_ENRLLMNT_MTHD"], exact=True).click()
                        page.wait_for_timeout(1000)
                        page.get_by_role("button", name="Save", exact=True).click()
                        page.wait_for_timeout(10000)

                    if datadictvalue["C_ASSGN_ON_DFLT"] != "":

                        page.wait_for_timeout(4000)
                        page.get_by_role("link", name="Actions", exact=True).click()
                        page.wait_for_timeout(1000)
                        page.locator("[id=\"__af_Z_window\"]").get_by_text("Correct").click()
                        page.wait_for_timeout(3000)

                        #if not page.get_by_text("Assign on default").is_checked():
                        page.get_by_text("Assign on default").click()
                        page.wait_for_timeout(2000)

                        page.get_by_role("button", name="Save", exact=True).click()
                        page.wait_for_timeout(10000)

                    if datadictvalue["C_POST_ELCTN_FRML"] != "":
                        page.wait_for_timeout(2000)
                        page.get_by_role("link", name="Actions", exact=True).click()
                        page.wait_for_timeout(1000)
                        page.locator("[id=\"__af_Z_window\"]").get_by_text("Correct").click()
                        page.wait_for_timeout(2000)
                        page.get_by_role("combobox", name="Post Election Formula", exact=True).click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_POST_ELCTN_FRML"]).click()
                        page.wait_for_timeout(1000)
                        page.get_by_role("button", name="Save", exact=True).click()
                        page.wait_for_timeout(10000)

                    try:
                        expect(page.locator("//span[text()='" + datadictvalue["C_PLAN"] + "']//following::span[text()='Plan']//following::img[@title='Yes']").first).to_be_visible()
                        print("Added Program-Enrollment to Plan Successfully")
                        datadictvalue["RowStatus"] = "Added Program-Enrollment to Plan"
                    except Exception as e:
                        print("Unable to Add Program-Enrollment to Plan")
                        datadictvalue["RowStatus"] = "Unable to Add Program-Enrollment to Plan"
                else:
                    print("Plan Already Enrolled")
                    try:
                        expect(page.locator("//span[text()='" + datadictvalue["C_PLAN"] + "']//following::span[text()='Plan']//following::img[@title='Yes']").first).to_be_visible()
                        print("Added Program-Enrollment to Plan Successfully")
                        datadictvalue["RowStatus"] = "Added Program-Enrollment to Plan"
                    except Exception as e:
                        print("Unable to Add Program-Enrollment to Plan")
                        datadictvalue["RowStatus"] = "Unable to Add Program-Enrollment to Plan"
            else:
                print("Plan not provided in datasheet")

            j = j + 1


        page.get_by_role("button", name="Save and Close").click()
        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict



print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_PROGRAM_ENROLLMENT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_PROGRAM_ENROLLMENT,
                             PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_PROGRAM_ENROLLMENT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_PROGRAM_ENROLLMENT)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[
            0] + "_" + BENEFIT_PROGRAM_ENROLLMENT + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

