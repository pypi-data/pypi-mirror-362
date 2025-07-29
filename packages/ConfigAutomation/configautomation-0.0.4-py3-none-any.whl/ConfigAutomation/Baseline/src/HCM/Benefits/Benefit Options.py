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
    page.get_by_role("link", name="Benefit Options").click()
    page.wait_for_timeout(5000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]

        #Search for Option Name to confirm Whether it is already Existing in the Application
        page.get_by_label("Option Name").click()
        page.get_by_label("Option Name").fill("")
        page.get_by_label("Option Name").type(datadictvalue["C_OPTN_NAME"])
        page.get_by_placeholder("mm-dd-yyyy").first.fill("")
        page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_EFFCTV_START_DATE"])
        page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(5000)

        #If option name is already available check for plan and Grp Relationship
        if page.get_by_role("link", name=datadictvalue["C_OPTN_NAME"]).is_visible():
            page.get_by_role("link", name=datadictvalue["C_OPTN_NAME"]).click()
            page.wait_for_timeout(5000)

            if datadictvalue["C_PLAN_TYPE"] != "":
                #If Plan Type not available , Add the Plan types
                if not page.get_by_text(datadictvalue["C_PLAN_TYPE"]).is_visible():
                    page.get_by_placeholder("mm-dd-yyyy").first.fill("")
                    page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_EFFCTV_START_DATE"])
                    page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
                    page.wait_for_timeout(4000)
                    if page.get_by_role("button", name="Yes").is_visible():
                        page.get_by_role("button", name="Yes").click()
                    page.wait_for_timeout(4000)
                    if page.get_by_role("link", name=datadictvalue["C_OPTN_NAME"]).is_visible():
                        page.get_by_label("Option Name").click()
                        page.get_by_label("Option Name").fill("")
                        page.get_by_label("Option Name").type(datadictvalue["C_OPTN_NAME"])
                        page.wait_for_timeout(2000)
                page.get_by_role("button", name="Select and Add").click()
                page.wait_for_timeout(3000)


                if datadictvalue["C_PLAN_TYPE"] != "":
                    page.get_by_label("Plan Type Name").click()
                    page.get_by_label("Plan Type Name").type(datadictvalue["C_PLAN_TYPE"])
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(4000)

            # If Group Relationship not available , Add the Group Relationship
            if datadictvalue["C_GROUP_RLTNSHP"] != "":
                if page.get_by_role("cell", name=datadictvalue["C_GROUP_RLTNSHP"], exact=True).is_visible():
                    page.get_by_role("cell", name=datadictvalue["C_GROUP_RLTNSHP"], exact=True).click()
                    page.wait_for_timeout(2000)
                    # Edit Group Relationship
                    page.get_by_title("Edit").nth(2).click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text("Correct").click()
                    page.wait_for_timeout(2000)
                    if datadictvalue["C_GROUP_RLTNSHP"] != "No designees":
                        # Check already existing if not then Add Relationship Type
                        Relationship_Type = page.locator("//span[text()='Relationship Type']//following::input[1]").get_attribute("title")
                        print(Relationship_Type)

                        if datadictvalue["C_RLTNSHP_TYPE"] != Relationship_Type:
                            if page.get_by_role("button", name="Add", exact=True).is_visible():
                                page.get_by_role("button", name="Add", exact=True).click()
                            if page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Create").is_visible():
                                page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Create").click()
                            page.wait_for_timeout(5000)
                            page.get_by_label("Relationship Type").first.click()
                            page.get_by_role("listbox").get_by_text(datadictvalue["C_RLTNSHP_TYPE"], exact=True).click()
                            page.wait_for_timeout(1000)
                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(5000)

                elif not page.get_by_role("cell", name=datadictvalue["C_GROUP_RLTNSHP"], exact=True).is_visible():
                    page.get_by_role("button", name="Create").click()
                    page.wait_for_timeout(2000)
                    page.get_by_role("combobox", name="Group Relationship").click()
                    page.get_by_text(datadictvalue["C_GROUP_RLTNSHP"], exact=True).click()
                    page.wait_for_timeout(1000)
                    page.get_by_role("combobox", name="Designation Type").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSGNTN_TYPE"]).click()
                    page.wait_for_timeout(1000)
                    page.get_by_role("combobox", name="Cover All Eligible").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_COVER_ALL_ELGBL"], exact=True).click()
                    page.wait_for_timeout(1000)
                    page.get_by_label("Minimum").type(str(datadictvalue["C_MNMM"]))
                    page.get_by_label("Maximum").type(str(datadictvalue["C_MXMM"]))
                    page.wait_for_timeout(1000)

                    # Add Relationship Type
                    if datadictvalue["C_RLTNSHP_TYPE"] != "":
                        page.get_by_role("button", name="Add", exact=True).click()
                        page.get_by_role("combobox", name="Relationship Type").click()
                        page.get_by_role("listbox").get_by_text(datadictvalue["C_RLTNSHP_TYPE"], exact=True).click()
                        page.wait_for_timeout(2000)

                    page.get_by_role("button", name="OK").click()
                    page.wait_for_timeout(5000)

                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(6000)

            else:
                print("Group Relationship already attached to the Option")
                page.wait_for_timeout(2000)
                page.get_by_role("button", name="Save and Close").click()
                page.wait_for_timeout(6000)

        #If option Name is not already available in application
        else:
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)

            page.get_by_placeholder("mm-dd-yyyy").first.fill("")
            page.get_by_placeholder("mm-dd-yyyy").first.type(datadictvalue["C_EFFCTV_START_DATE"])
            page.get_by_placeholder("mm-dd-yyyy").first.press("Tab")
            page.wait_for_timeout(4000)
            if page.get_by_role("button", name="Yes").is_visible():
                page.get_by_role("button", name="Yes").click()
            page.wait_for_timeout(4000)

            #Add Option Name Details
            page.get_by_label("Option Name", exact=True).click()
            page.get_by_label("Option Name", exact=True).type(str(datadictvalue["C_OPTN_NAME"]))
            page.get_by_label("Benefits Extract Option Name").click()
            page.get_by_label("Benefits Extract Option Name").type(datadictvalue["C_BNFT_EXTRCT_OPTN_NAME"])
            # page.get_by_label("Short Name").click()
            # page.get_by_label("Short Name").type()
            # page.get_by_label("Short Code").click()
            # page.get_by_label("Short Code").type()
            page.wait_for_timeout(1000)

            if datadictvalue["C_WAIVE_OPTN"] == "Yes":
                if not page.get_by_text("Waive option").is_checked():
                    page.get_by_text("Waive option").click()
                    page.wait_for_timeout(2000)

            #Add Plan Types
            page.get_by_role("button", name="Select and Add").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Plan Type Name").click()
            page.get_by_label("Plan Type Name").type(datadictvalue["C_PLAN_TYPE"])
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(4000)
            # page.get_by_title("Search and Select: Plan Type").click()
            # page.wait_for_timeout(1000)
            # page.get_by_role("link", name="More...").click()
            # page.wait_for_timeout(2000)
            # page.locator("tr").filter(has_text=re.compile(rf"^{datadictvalue['C_PLAN_TYPE']}")).get_by_role("cell").click()
            # page.wait_for_timeout(1000)
            # page.get_by_role("button", name="OK").nth(1).click()
            # page.wait_for_timeout(3000)
            #page.get_by_role("button", name="OK").click()
            #page.wait_for_timeout(4000)

            #Add Group Relationship
            if datadictvalue["C_GROUP_RLTNSHP"] != "":
                page.get_by_role("button", name="Create").click()
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="Group Relationship").click()
                page.get_by_text(datadictvalue["C_GROUP_RLTNSHP"], exact=True).click()
                page.wait_for_timeout(1000)
                page.get_by_role("combobox", name="Designation Type").click()
                page.get_by_text(datadictvalue["C_DSGNTN_TYPE"]).click()
                page.wait_for_timeout(1000)
                page.get_by_role("combobox", name="Cover All Eligible").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_COVER_ALL_ELGBL"], exact=True).click()
                page.wait_for_timeout(1000)
                page.get_by_label("Minimum").type(str(datadictvalue["C_MNMM"]))
                page.get_by_label("Maximum").type(str(datadictvalue["C_MXMM"]))
                page.wait_for_timeout(1000)
                #Add Relationship Type
                if datadictvalue["C_RLTNSHP_TYPE"] != "":
                    page.get_by_role("button", name="Add", exact=True).click()
                    page.get_by_role("combobox", name="Relationship Type").click()
                    page.get_by_role("listbox").get_by_text(datadictvalue["C_RLTNSHP_TYPE"], exact=True).click()
                    #get_by_role("listbox").get_by_text("Spouse", exact=True)
                    page.wait_for_timeout(2000)

                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(5000)

            #page.get_by_role("button", name="Save", exact=True)
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(6000)
        i = i + 1
        print(i)

        try:
            expect(page.get_by_role("heading", name="Benefit Options")).to_be_visible()
            print("Added Benefit Options Saved Successfully")
            datadictvalue["RowStatus"] = "Added Benefit Options"
        except Exception as e:
            print("Unable to save Benefit Options")
            datadictvalue["RowStatus"] = "Unable to Add Benefit Options"

    OraSignOut(page, context, browser, videodir)
    return datadict


print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_OPTIONS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_OPTIONS,
                             PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + BENEFITS_CONFIG_WRKBK, BENEFIT_OPTIONS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[0] + "_" + BENEFIT_OPTIONS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", BENEFITS_CONFIG_WRKBK)[
            0] + "_" + BENEFIT_OPTIONS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


