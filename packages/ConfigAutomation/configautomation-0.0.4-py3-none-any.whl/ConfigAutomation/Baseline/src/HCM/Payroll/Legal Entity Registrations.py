from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *

def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(40000)
    page.get_by_role("link", name="Tasks").click()
    page.get_by_role("link", name="Manage Implementation Projects").click()
    page.get_by_label("Name").click()
    page.get_by_label("Name").type("HCM Implementation Project")
    page.get_by_role("button", name="Search", exact=True).click()
    page.wait_for_timeout(2000)
    # page.get_by_role("button", name="Done").click()
    page.get_by_role("cell", name="HCM Implementation Project", exact=True).click()
    page.get_by_role("button", name="Edit").click()
    page.wait_for_timeout(4000)
    page.get_by_role("cell", name="Expand Task ListWorkforce Deployment", exact=True).get_by_role("link").click()
    page.wait_for_timeout(1000)
    page.get_by_role("cell", name="Expand Task List*Define Common Applications Configuration for Human Capital Management", exact=True).get_by_role("link").click()
    page.wait_for_timeout(1000)
    page.get_by_role("cell", name="Expand Task List*Define Enterprise Structures for Human Capital Management", exact=True).get_by_role("link").click()
    page.wait_for_timeout(1000)
    page.get_by_role("cell", name="Expand Iterative Task List*Define Legal Entities for Human Capital Management", exact=True).get_by_role("link").click()
    page.wait_for_timeout(1000)

    page.pause()


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        print(i)
        page.locator("//span[text()='Manage Legal Entity Registrations']//following::a[@title='Go to Task']").first.click()
        # page.locator("//span[text()='Manage Legal Reporting Unit Registrations']//following::a[2]").first.click()
        # page.get_by_label("Legal Entity").click()
        # page.get_by_label("Legal Entity").select_option("Select and Add")
        # page.wait_for_timeout(2000)
        # page.get_by_role("button", name="Apply and Go to Task").click()
        # page.wait_for_timeout(3000)
        # page.get_by_label("Expand Search").click()
        # page.get_by_label("Name").fill(datadictvalue["C_LEGAL_ENTTY_NAME"])
        # page.locator("[id=\"__af_Z_window\"]").get_by_role("button", name="Search", exact=True).click()
        # page.wait_for_timeout(3000)
        # page.locator("[id=\"__af_Z_window\"]").get_by_role("cell", name=datadictvalue["C_LEGAL_ENTTY_NAME"],exact=True).click()
        # page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(7000)

        if page.get_by_role("cell", name=datadictvalue["C_JRSDCTN"], exact=True).is_visible():
            page.get_by_role("button", name="Done").click()
            print(datadictvalue["C_JRSDCTN"] + "Already present in Application")
            page.wait_for_timeout(5000)
        else:
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)
            page.get_by_title("Search: Jurisdiction").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Name", exact=True).click()
            page.get_by_label("Name", exact=True).type(datadictvalue["C_JRSDCTN"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_JRSDCTN"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(1000)
            # page.get_by_title("Search: Registered Address").click()
            # page.get_by_role("link", name="Search...").click()
            # page.get_by_label("Address Line").click()
            # page.get_by_label("Address Line").type(datadictvalue["C_RGSTRD_ADDRSS"])
            # page.get_by_role("button", name="Search", exact=True).click()
            # page.wait_for_timeout(2000)
            # page.locator("//tr[@_afrrk='0']").nth(1).click()
            # #page.get_by_role("option", name=datadictvalue["C_RGSTRD_ADDRSS"]).click()
            # page.wait_for_timeout(1000)
            # page.get_by_role("button", name="OK").click()

            page.get_by_label("Registered Address").clear()
            page.get_by_label("Registered Address").type(datadictvalue["C_RGSTRD_ADDRSS"],delay=100)
            page.wait_for_timeout(1000)
            page.get_by_role("option", name=datadictvalue["C_RGSTRD_ADDRSS"],exact=True).click()
            page.wait_for_timeout(1000)
            page.get_by_label("Registered Name").click()
            page.get_by_label("Registered Name").type(datadictvalue["C_RGSTRD_NAME"])

            #page.get_by_label("Alternate Name")
            if page.get_by_label("EIN or TIN").is_visible():
                if datadictvalue["C_EIN_TIN"] != "N/A":
                    page.get_by_label("EIN or TIN").click()
                    page.get_by_label("EIN or TIN").type(datadictvalue["C_EIN_TIN"])
            if datadictvalue["C_RGSTRTN_NMBR"] != "N/A":
                page.get_by_label("Registration Number").click()
                page.get_by_label("Registration Number").type(datadictvalue["C_RGSTRTN_NMBR"])
            page.wait_for_timeout(1000)
            # page.get_by_label("Place of Registration")
            # page.get_by_label("Issuing Legal Authority")
            # page.get_by_placeholder("mm/dd/yyyy")
            # page.get_by_placeholder("mm/dd/yyyy").nth(1)

            #page.get_by_role("button", name="Cancel", exact=True).click()
            #page.get_by_role("button", name="Save", exact=True).click()
            #page.wait_for_timeout(5000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(5000)
            if page.get_by_text("Confirmation").is_visible():
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(5000)

        i = i + 1

        try:
            expect(page.locator("//span[text()='Manage Legal Entity Registrations']//following::a[@title='Go to Task']").first).to_be_visible()
            print("Added Legal Entity Registration Saved Successfully")
            datadictvalue["RowStatus"] = "Added Legal Entity Registration"
        except Exception as e:
            print("Unable to save Legal Entity Registration")
            datadictvalue["RowStatus"] = "Unable to Add Legal Entity Registration"



    OraSignOut(page, context, browser, videodir)
    return datadict



print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, MANAGE_LEGAL_ENTITY_REGISTRATION):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_CONFIG_WRKBK, MANAGE_LEGAL_ENTITY_REGISTRATION, PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_CONFIG_WRKBK, MANAGE_LEGAL_ENTITY_REGISTRATION)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + MANAGE_LEGAL_ENTITY_REGISTRATION)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_CONFIG_WRKBK)[0] + "_" + MANAGE_LEGAL_ENTITY_REGISTRATION + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

