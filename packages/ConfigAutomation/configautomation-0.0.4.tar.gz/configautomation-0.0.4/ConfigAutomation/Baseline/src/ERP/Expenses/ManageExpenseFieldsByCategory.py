from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("Manage Expense Fields By Category")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Manage Expense Fields By Category").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        #Accomodations

        page.get_by_role("link", name="Accommodations").click()
        page.wait_for_timeout(2000)
        if page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).is_visible():
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_ACCMDTNS_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).fill(datadictvalue["C_ACCMDTNS_BSNSS_UNIT"])
            page.get_by_role("table", name="This table contains column headers corresponding to the data body table below").locator("input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        if datadictvalue["C_ENBL_FLDS_FOR_ACCMDTNS"] == 'Yes':
            page.get_by_role("cell", name=datadictvalue["C_ACCMDTNS_BSNSS_UNIT"]).locator("label").first.check()
        if datadictvalue["C_ENBL_FLDS_FOR_ACCMDTNS"] == 'No':
            page.get_by_role("cell", name=datadictvalue["C_ACCMDTNS_BSNSS_UNIT"]).locator("label").first.uncheck()
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name=datadictvalue["C_ACCMDTNS_BSNSS_UNIT"]).get_by_label("Merchant").select_option(datadictvalue["C_ACCMDTNS_MRCHNT_NAME"])
        page.get_by_role("cell", name=datadictvalue["C_ACCMDTNS_BSNSS_UNIT"]).get_by_label("Checkout Date").select_option(datadictvalue["C_CHCKT_DATE"])

        #Airfare
        page.get_by_role("link", name="Airfare").click()
        page.wait_for_timeout(2000)
        if page.get_by_role("table",name="This table contains column headers corresponding to the data body table below").locator(
            "input").nth(0).is_visible():
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_AIR_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table",name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_AIR_BSNSS_UNIT"])
            page.get_by_role("table",name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        if datadictvalue["C_ENBL_FLDS_FOR_ARFR"] == 'Yes':
            page.get_by_role("cell", name=datadictvalue["C_AIR_BSNSS_UNIT"]).locator("label").first.check()
        if datadictvalue["C_ENBL_FLDS_FOR_ARFR"] == 'No':
            page.get_by_role("cell", name=datadictvalue["C_AIR_BSNSS_UNIT"]).locator("label").first.uncheck()
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name=datadictvalue["C_AIR_BSNSS_UNIT"]).get_by_label("Merchant").select_option(
            datadictvalue["C_AIR_MRCHNT_NAME"])
        page.get_by_role("cell", name=datadictvalue["C_AIR_BSNSS_UNIT"]).get_by_label("Flight Type").select_option(
            datadictvalue["C_FLGHT_TYPE"])
        page.get_by_role("cell", name=datadictvalue["C_AIR_BSNSS_UNIT"]).get_by_label("Flight Class").select_option(
            datadictvalue["C_FLGHT_CLASS"])
        page.get_by_role("cell", name=datadictvalue["C_AIR_BSNSS_UNIT"]).get_by_label("Ticket Number").select_option(
            datadictvalue["C_TCKT_NAME"])
        page.get_by_role("cell", name=datadictvalue["C_AIR_BSNSS_UNIT"]).get_by_label("Departure City").select_option(
            datadictvalue["C_DPRTR_CITY"])
        page.get_by_role("cell", name=datadictvalue["C_AIR_BSNSS_UNIT"]).get_by_label("Arrival City").select_option(
            datadictvalue["C_ARRVL_CITY"])
        page.get_by_role("cell", name=datadictvalue["C_AIR_BSNSS_UNIT"]).get_by_label("Agency").select_option(
            datadictvalue["C_AGNCY"])
        page.get_by_role("cell", name=datadictvalue["C_AIR_BSNSS_UNIT"]).get_by_label("Passenger").select_option(
            datadictvalue["C_PSSNGR"])

        #Car Rental

        page.get_by_role("link", name="Car Rental").click()
        page.wait_for_timeout(2000)
        if page.get_by_role("table",
                            name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).is_visible():
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_CAR_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_CAR_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        if datadictvalue["C_ENBL_FLDS_FOR_CAR_RNTL"] == 'Yes':
            page.get_by_role("cell", name=datadictvalue["C_CAR_BSNSS_UNIT"]).locator("label").first.check()
        if datadictvalue["C_ENBL_FLDS_FOR_CAR_RNTL"] == 'No':
            page.get_by_role("cell", name=datadictvalue["C_CAR_BSNSS_UNIT"]).locator("label").first.uncheck()
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name=datadictvalue["C_CAR_BSNSS_UNIT"]).get_by_label("Merchant").select_option(
            datadictvalue["C_CAR_MRCHNT_NAME"])
        page.get_by_role("cell", name=datadictvalue["C_CAR_BSNSS_UNIT"]).get_by_label("Agency").select_option(
            datadictvalue["C_CAR_AGNCY"])

        #Entertainment

        page.get_by_role("link", name="Entertainment").click()
        page.wait_for_timeout(2000)
        if page.get_by_role("table",
                            name="This table contains column headers corresponding to the data body table below").locator(
            "input").nth(0).is_visible():
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_ENT_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_ENT_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        if datadictvalue["C_ENBL_FLDS_FOR_ENTRTNMNT"] == 'Yes':
            page.get_by_role("cell", name=datadictvalue["C_ENT_BSNSS_UNIT"]).locator("label").first.check()
        if datadictvalue["C_ENBL_FLDS_FOR_ENTRTNMNT"] == 'No':
            page.get_by_role("cell", name=datadictvalue["C_ENT_BSNSS_UNIT"]).locator("label").first.uncheck()
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name=datadictvalue["C_ENT_BSNSS_UNIT"]).get_by_label("Merchant").select_option(
            datadictvalue["C_ENT_MRCHNT_NAME"])

        # Meals

        page.get_by_role("link", name="Meals").click()
        page.wait_for_timeout(2000)
        if page.get_by_role("table",
                            name="This table contains column headers corresponding to the data body table below").locator(
            "input").nth(0).is_visible():
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_MEALS_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_MEALS_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        if datadictvalue["C_ENBL_FLDS_FOR_MEALS"] == 'Yes':
            page.get_by_role("cell", name=datadictvalue["C_MEALS_BSNSS_UNIT"]).locator("label").first.check()
        if datadictvalue["C_ENBL_FLDS_FOR_MEALS"] == 'No':
            page.get_by_role("cell", name=datadictvalue["C_MEALS_BSNSS_UNIT"]).locator("label").first.uncheck()
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name=datadictvalue["C_MEALS_BSNSS_UNIT"]).get_by_label("Merchant").select_option(
            datadictvalue["C_MEALS_MRCHNT_NAME"])

        # Mileage

        page.get_by_role("link", name="Mileage").click()
        page.wait_for_timeout(2000)
        if page.get_by_role("table",
                            name="This table contains column headers corresponding to the data body table below").locator(
            "input").nth(0).is_visible():
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_MLG_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_MLG_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        if datadictvalue["C_ENBL_FLDS_FOR_MLG"] == 'Yes':
            page.get_by_role("cell", name=datadictvalue["C_MLG_BSNSS_UNIT"]).locator("label").first.check()
        if datadictvalue["C_ENBL_FLDS_FOR_MLG"] == 'No':
            page.get_by_role("cell", name=datadictvalue["C_MLG_BSNSS_UNIT"]).locator("label").first.uncheck()
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name=datadictvalue["C_MLG_BSNSS_UNIT"]).get_by_label("Starting Location").select_option(
            datadictvalue["C_STRTNG_LCTN"])
        page.get_by_role("cell", name=datadictvalue["C_MLG_BSNSS_UNIT"]).get_by_label("Destination").select_option(
            datadictvalue["C_DSTNTN"])
        page.get_by_role("cell", name=datadictvalue["C_MLG_BSNSS_UNIT"]).get_by_label("License Plate Number").select_option(
            datadictvalue["C_LCNS_PLATE_NMBR"])
        page.get_by_role("cell", name=datadictvalue["C_MLG_BSNSS_UNIT"]).get_by_label("Starting Odometer Reading").select_option(
            datadictvalue["C_STRTNG_ODMTR_RDNG"])
        page.get_by_role("cell", name=datadictvalue["C_MLG_BSNSS_UNIT"]).get_by_label("Ending Odometer Reading").select_option(
            datadictvalue["C_ENDNG_ODMTR_RDNG"])

        # Miscellaneous

        page.get_by_role("link", name="Miscellaneous").click()
        page.wait_for_timeout(2000)
        if page.get_by_role("table",
                            name="This table contains column headers corresponding to the data body table below").locator(
            "input").nth(0).is_visible():
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_MSC_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        else:
            page.get_by_role("button", name="Query By Example").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).fill(datadictvalue["C_MSC_BSNSS_UNIT"])
            page.get_by_role("table",
                             name="This table contains column headers corresponding to the data body table below").locator(
                "input").nth(0).press("Enter")
            page.wait_for_timeout(2000)
        if datadictvalue["C_ENBL_FLDS_FOR_MSCLLNS"] == 'Yes':
            page.get_by_role("cell", name=datadictvalue["C_MSC_BSNSS_UNIT"]).locator("label").first.check()
        if datadictvalue["C_ENBL_FLDS_FOR_MSCLLNS"] == 'No':
            page.get_by_role("cell", name=datadictvalue["C_MSC_BSNSS_UNIT"]).locator("label").first.uncheck()
        page.wait_for_timeout(3000)
        page.get_by_role("cell", name=datadictvalue["C_MSC_BSNSS_UNIT"]).get_by_label("Merchant").select_option(
            datadictvalue["C_MSC_MRCHNT_NAME"])

        # Save the data

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(5000)
        if page.get_by_role("button", name="Yes").is_visible():
            page.get_by_role("button", name="Yes").click()
        if page.get_by_role("button", name="OK").is_visible():
            page.get_by_role("button", name="OK").click()

        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Expense Fields by Category Saved Successfully")
            datadictvalue["RowStatus"] = "Expense Fields by Category are added successfully"

        except Exception as e:
            print("Expense Fields by Category not saved")
            datadictvalue["RowStatus"] = "Expense Fields by Category are not added"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, EXP_FIELDS_BY_CATEGORY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, EXP_FIELDS_BY_CATEGORY, PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, EXP_FIELDS_BY_CATEGORY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[0] + "_" + EXP_FIELDS_BY_CATEGORY)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + EXP_FIELDS_BY_CATEGORY + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))