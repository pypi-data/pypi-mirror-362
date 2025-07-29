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
        print("Print i =" + str(i))

        if datadictvalue["C_PRGRM"] != "":
            page.get_by_label("Program Name").click()
            page.get_by_label("Program Name").fill("")
            page.get_by_label("Program Name").type(datadictvalue["C_PRGRM"])
            page.get_by_placeholder("mm-dd-yyyy").first.click()
            page.wait_for_timeout(1000)
            page.get_by_placeholder("mm-dd-yyyy").first.fill("")
            page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_SSSN_EFFCTV_DATE"])
            page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(6000)
            if page.get_by_role("link", name=datadictvalue["C_PRGRM"], exact=True).is_visible():
                page.get_by_role("link", name=datadictvalue["C_PRGRM"], exact=True).click()
                page.wait_for_timeout(6000)

            page.get_by_role("link", name="Designation Requirements").click()
            page.wait_for_timeout(5000)

        else:
            break

        j = 0
        while j < rowcount:
            datadictvalue = datadict[j]
            print("Print j =" + str(j))

            # Find and Select Plan Type
            if datadictvalue["C_PLAN_TYPE"] != "":
                k = 1
                while k > 0:

                    if page.get_by_text(datadictvalue["C_PLAN_TYPE"], exact=True).is_visible():
                        print("Plan Type" + datadictvalue["C_PLAN_TYPE"])
                        page.get_by_text(datadictvalue["C_PLAN_TYPE"], exact=True).click()
                        break

                    else:
                        page.wait_for_timeout(3000)
                        print("Scrolling")
                        #page.locator("//div[contains(@id,':0:t1::scroller')]").first.click()
                        page.locator("//table[@summary='Plan Types in Program']").first.click()
                        page.mouse.wheel(0, 500)
                        #page.mouse.move(0, 100)
                        #page.keyboard.press("ArrowDown")


                    k = k + 1

            page.wait_for_timeout(8000)
            if datadictvalue["C_PLAN_TYPE"] != "":
                page.keyboard.press("Space")
                #if not page.locator("//span[text()='" + datadictvalue["C_PLAN_TYPE"] + "']//following::img[@title='Yes']").first.is_visible():
                # General Dependent Action Item
                page.get_by_role("link", name="General", exact=True).first.click()
                page.wait_for_timeout(5000)
                if datadictvalue["C_ACTN_ITEM_GC"] != "":
                #if not page.locator("//span[text()='" + datadictvalue["C_PLAN_TYPE"] + "']//following::img[@title='Yes']").first.is_visible():
                #if not page.get_by_text(datadictvalue["C_ACTION_ITEM"]).first.is_visible():
                    page.wait_for_timeout(4000)
                    # page.pause()
                    page.get_by_role("link", name="Actions", exact=True).click()
                    # page.locator(".xmm").first.click()
                    page.wait_for_timeout(1000)
                    page.locator("[id=\"__af_Z_window\"]").get_by_text("Correct").click()
                    page.wait_for_timeout(2000)

                    page.get_by_role("combobox", name="Dependent Coverage Start Date").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DPNDNT_CVRG_START_DATE_GC"]).click()
                    page.wait_for_timeout(1000)
                    page.get_by_role("combobox", name="Previous Dependent Coverage End Date").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRVS_DPNDNT_CVRG_END_DATE_GC"]).click()
                    page.wait_for_timeout(3000)

                    page.get_by_role("button", name="Select and Add").first.click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Action Item").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ACTN_ITEM_GC"]).click()
                    page.wait_for_timeout(1000)
                    page.get_by_role("combobox", name="Due Date").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DUE_DATE_AI"]).click()
                    page.wait_for_timeout(1000)
                    if datadictvalue["C_SSPND_ENRLLMNT"] != "":
                        if not page.get_by_role("row", name="Suspend enrollment", exact=True).locator("label").is_checked():
                            page.get_by_role("row", name="Suspend enrollment", exact=True).locator("label").click()
                    page.wait_for_timeout(1000)
                    if datadictvalue["C_RQRD_GC"] != "":
                        if not page.get_by_role("row", name="Required", exact=True).locator("label").is_checked():
                            page.get_by_role("row", name="Required", exact=True).locator("label").click()
                    page.wait_for_timeout(1000)
                    page.get_by_role("button", name="OK").first.click()
                    page.wait_for_timeout(5000)

                # Add Life Event
                if datadictvalue["C_LIFE_EVENT_NAME"] != "":
                    print("Life Event - " + datadictvalue["C_LIFE_EVENT_NAME"])
                    # page.pause()
                    # page.get_by_role("link", name="Life Event").click()
                    page.locator("//div[contains(@id,'AP1:r1:0:sdi2::ti')]").click()
                    page.wait_for_timeout(5000)
                    #Open Drop Down and Check whether the Life EVent already exists
                    page.locator("//a[contains(@id,':0:navList1::drop')]").click()
                    page.wait_for_timeout(2000)
                    if page.get_by_text(datadictvalue["C_LIFE_EVENT_NAME"]).first.is_visible():
                        page.get_by_text(datadictvalue["C_LIFE_EVENT_NAME"]).first.click()
                        page.wait_for_timeout(5000)

                    else:
                        page.get_by_role("button", name="Add Life Event").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("listitem", name=datadictvalue["C_LIFE_EVENT_NAME"]).click()
                        page.wait_for_timeout(1000)
                        page.get_by_role("button", name="OK").click()
                        page.wait_for_timeout(5000)

                        # Coverage
                        if datadictvalue["C_CHNG_DPNDNT_CVRG_RULE"] != "":
                            page.get_by_role("combobox", name="Change Dependent Coverage Rule").click()
                            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CHNG_DPNDNT_CVRG_RULE"]).click()
                            page.wait_for_timeout(5000)
                        if datadictvalue["C_DPNDNT_CVRG_START_DATE"] != "":
                            page.get_by_role("combobox", name="Dependent Coverage Start Date").click()
                            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DPNDNT_CVRG_START_DATE"]).click()
                            page.wait_for_timeout(3000)
                        if datadictvalue["C_PRVS_DPNDNT_CVRG_END_DATE"] != "":
                            page.get_by_role("combobox", name="Previous Dependent Coverage End Date").click()
                            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRVS_DPNDNT_CVRG_END_DATE"]).click()
                            page.wait_for_timeout(3000)


                        # Certification
                        if datadictvalue["C_ACTN_ITEM_CRTFCTN"] != "":
                            # page.pause()
                            # page.get_by_role("link", name="Actions", exact=True).nth(1).click()
                            page.locator(".xmm").first.click()
                            page.wait_for_timeout(1000)
                            page.get_by_role("cell", name="Create", exact=True).click()
                            page.wait_for_timeout(5000)
                            ActionItem = page.locator("//label[text()='Action Item']//following::span[1]").text_content()
                            print(ActionItem)
                            if datadictvalue["C_CERT_DUE_DATE"] != "":
                                page.get_by_role("combobox", name="Due Date", exact=True).click()
                                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CERT_DUE_DATE"]).click()
                                page.wait_for_timeout(1000)
                            if datadictvalue["C_SSPND_ENRLLMNT_CRTFCTN"] != "":
                                if not page.get_by_role("row", name="Suspend enrollment", exact=True).locator(
                                        "label").is_checked():
                                    page.get_by_role("row", name="Suspend enrollment", exact=True).locator("label").click()
                            page.wait_for_timeout(1000)
                            if datadictvalue["C_RQRD_CRTFCTN"] != "":
                                if not page.get_by_role("row", name="Required", exact=True).locator("label").is_checked():
                                    page.get_by_role("row", name="Required", exact=True).locator("label").click()
                            page.wait_for_timeout(3000)

                # Certification Type
                if datadictvalue["C_CRTFCTN_TYPE"] != "":
                    print("Life Event - " + datadictvalue["C_LIFE_EVENT_NAME"])
                    # page.get_by_role("link", name="Life Event").click()
                    page.locator("//div[contains(@id,'AP1:r1:0:sdi2::ti')]").click()
                    page.wait_for_timeout(5000)

                    page.get_by_role("button", name="Select and Add").first.click()
                    page.wait_for_timeout(2000)
                    page.get_by_role("combobox", name="Certification Type").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CRTFCTN_TYPE"], exact=True).click()
                    page.wait_for_timeout(1000)
                    page.get_by_role("combobox", name="Relationship Type").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RLTNSHP_TYPE"], exact=True).click()
                    page.wait_for_timeout(1000)

                    if datadictvalue["C_DTRMNTN_FRML"] != "":
                        page.get_by_role("combobox", name="Determination Formula").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DTRMNTN_FRML"]).click()
                        page.wait_for_timeout(1000)
                    if datadictvalue["C_RQRD_RLTNSHP"] != "":
                        if not page.locator("[id=\"__af_Z_window\"]").get_by_text("Required").is_checked():
                            page.locator("[id=\"__af_Z_window\"]").get_by_text("Required").click()
                    page.wait_for_timeout(2000)
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(6000)

                # Add Eligibility
                if datadictvalue["C_ELGBLTY_PRFL"] != "":
                    page.get_by_role("link", name="Eligibility", exact=True).click()
                    page.wait_for_timeout(5000)
                    page.get_by_role("button", name="Select and Add").first.click()
                    page.wait_for_timeout(2000)
                    page.get_by_role("combobox", name="Eligibility Profile").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ELGBLTY_PRFL"]).click()
                    page.wait_for_timeout(1000)
                    # page.get_by_role("combobox", name="Eligibility Formula").click()
                    # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RQRD_ELGBLTY"]).click()
                    # page.wait_for_timeout(1000)
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(6000)

                page.get_by_role("button", name="Save", exact=True).click()
                # page.pause()
                page.wait_for_timeout(10000)
                # page.get_by_text(datadictvalue["C_PLAN_TYPE"], exact=True).first.click()
                #page.get_by_text(datadictvalue["C_PLAN_TYPE"], exact=True).click()
                # page.wait_for_timeout(5000)

                try:
                    expect(page.locator("//span[text()='" + datadictvalue["C_PLAN_TYPE"] + "']//following::img[@title='Yes']").first).to_be_visible()
                    print("Added Benefit Program-Designation to Plan Type Successfully")
                    datadictvalue["RowStatus"] = "Added Benefit Program-Designation to Plan Type"
                except Exception as e:
                            print("Unable to Add Benefit Program-Designation to Plan Type")
                            datadictvalue["RowStatus"] = "Unable to Add Benefit Program-Designation to Plan Type"
            else:
                print("Already configured Benefit Program-Designation For Plan type" + datadictvalue["C_PLAN_TYPE"])
                try:
                    expect(page.locator("//span[text()='" + datadictvalue["C_PLAN_TYPE"] + "']//following::img[@title='Yes']").first).to_be_visible()
                    print("Added Benefit Program-Designation to Plan Type Successfully")
                    datadictvalue["RowStatus"] = "Added Benefit Program-Designation to Plan Type"
                except Exception as e:
                        print("Unable to Add Benefit Program-Designation to Plan Type")
                        datadictvalue["RowStatus"] = "Unable to Add Benefit Program-Designation to Plan Type"

            j = j + 1


        page.get_by_role("button", name="Save and Close").click()
        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict

print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_PROGRAM_DESIGNATION):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_PROGRAM_DESIGNATION,
                             PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_PROGRAM_DESIGNATION)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_PROGRAM_DESIGNATION)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[
            0] + "_" + BENEFIT_PROGRAM_DESIGNATION + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

