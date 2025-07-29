from playwright.sync_api import Playwright, sync_playwright
from ConfigAutomation.Baseline.src.utils import *

CONFIGNAME = "Sample_CreateLegalEntity"

def configure(playwright: Playwright, rowcount, datadict) -> dict:
    browser, context, page = OpenBrowser(playwright, False, CONFIGNAME)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Legal Entity")
    page.get_by_role("textbox").press("Enter")

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)
        page.get_by_role("link", name="Manage Legal Entity", exact=True).click()
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["Name"])
        page.get_by_label("Legal Entity Identifier").click()
        page.get_by_label("Legal Entity Identifier").fill(datadictvalue["Legal Entity Identifier"])
        page.get_by_role("row", name="Start Date mm/dd/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("mm/dd/yy").click()
        page.get_by_role("row", name="Start Date mm/dd/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("mm/dd/yy").fill(datadictvalue[" Effective Start Date"])
        page.get_by_label("Legal Address").click()
        if datadictvalue["Legal Address"] != "":
            page.get_by_label("Legal Address").type(datadictvalue["Legal Address"], delay=50)
            page.get_by_role("option", name=datadictvalue["Legal Address"]).click()
        page.get_by_label("EIN or TIN").click()
        page.get_by_label("EIN or TIN").fill(datadictvalue["EIN/TIN"])
        page.get_by_label("Legal Reporting Unit").click()
        page.get_by_label("Legal Reporting Unit").fill(datadictvalue["Legal Reporting Unit Registration Number"])
        if datadictvalue["Payroll statutory Unit"] == "Yes":
            page.get_by_text("Payroll statutory unit", exact=True).check()
        if datadictvalue["Legal Employer"] == "Yes":
            page.get_by_text("Legal employer").check()
        page.get_by_role("button", name="Cancel").click()
        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"
        i = i + 1

    OraSignOut(page, context, browser, CONFIGNAME)
    return datadict


#****** Execution Starts Here ******
rows, cols, datadictwrkbk = ImportWrkbk(ENTERPRISE_STRUCTURES_WRKBK, ENTERPRISE_STRUCTURES_SHEET, 35)
with sync_playwright() as pw:
    output = configure(pw, rows, datadictwrkbk)
write_status(output, "results/" + CONFIGNAME + "_LoadResults_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
