from playwright.sync_api import Playwright, sync_playwright
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *


CONFIGNAME = "ManageIntercompanyCustomerSupplierAssociation"


def configure(playwright: Playwright, rowcount, datadict) -> dict:
    browser, context, page = OpenBrowser(playwright, False, CONFIGNAME)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Intercompany Customer Supplier Association")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Intercompany Customer Supplier Association", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="Add Row").click()
        page.wait_for_timeout(3000)
        page.locator(".xwn").first.click()
        page.get_by_label("Legal Entity Name").click()
        page.get_by_label("Legal Entity Name").fill(datadictvalue["C_LEGAL_ENTITY_NAME"])
        page.get_by_role("option", name=datadictvalue["C_LEGAL_ENTITY_NAME"]).click()
        page.get_by_label("Intercompany Organization", exact=True).type(datadictvalue["C_INTRCMPNY_ORGNZTON"])
        page.get_by_role("option", name=datadictvalue["C_INTRCMPNY_ORGNZTON"]).click()
        page.get_by_label("Customer Name").type(datadictvalue["C_CSTMER_NAME"])
        page.get_by_role("option", name=datadictvalue["C_CSTMER_NAME"]).click()
        page.wait_for_timeout(2000)
        page.get_by_label("Supplier Name").type(datadictvalue["C_SUPPLIER_NAME"])
        page.get_by_role("option", name=datadictvalue["C_SUPPLIER_NAME"]).click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(3000)
        if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
            page.locator("//div[text()='Confirmation']//following::button[1]").click()

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        if i == rowcount:
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)
            if page.locator("//div[text()='Confirmation']//following::button[1]").is_visible():
                page.locator("//div[text()='Confirmation']//following::button[1]").click()



    OraSignOut(page, context, browser, CONFIGNAME)
    return datadict


# ****** Execution Starts Here ******
rows, cols, datadictwrkbk = ImportWrkbk(GL_WORKBOOK, IC_SUPPLIER_ASSOCIATION,
                                        [0,1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,17],
                                        12)
with sync_playwright() as pw:
    output = configure(pw, rows, datadictwrkbk)
write_status(output, "results/" + CONFIGNAME + "_LoadResults_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")


# ImportWrkbk1(GL_WORKBOOK, IC_SUPPLIER_ASSOCIATION)
