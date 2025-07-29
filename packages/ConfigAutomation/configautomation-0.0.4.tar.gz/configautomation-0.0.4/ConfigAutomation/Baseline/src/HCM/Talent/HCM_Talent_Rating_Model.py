from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *
import re

def configure(playwright: Playwright, rowcount, datadict, videodir):
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("My Client Groups", exact=True).click()
    page.get_by_role("link", name="Performance").click()
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Profile Rating Models").click()

    PrevRtngMdl=""
    r = 0
    while r < rowcount:

        datadictvalue = datadict[r]
        page.wait_for_timeout(2000)

        # This worksheet will contain multiple rows for one single rating model setup.
        # Hence, checking if the next row is same as earlier to determine if we are working
        # with the same model or a new one
        if datadictvalue["C_CODE"] != PrevRtngMdl:

            #Save the prev model data if the row contains a new rating model
            if r > 0:
                page.wait_for_timeout(5000)
                page.get_by_role("button", name="Cancel").click()
                try:
                    expect(page.get_by_role("heading", name="Search Results")).to_be_visible()
                    print("Rating Model Saved")
                    datadict[r - 1]["RowStatus"] = "Rating Model Saved"
                except Exception as e:
                    print("Unable to save rating model")
                    datadict[r - 1]["RowStatus"] = "Unable to save rating model"

            #Reset the counter to identify rows correctly for child levels
            i = 0
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Code").click()
            page.get_by_label("Code").fill(datadictvalue["C_CODE"])
            page.get_by_label("Name").fill(datadictvalue["C_NAME"])
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.get_by_role("row", name="*From Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").clear()
            page.get_by_role("row", name="*From Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_FROM_DATE"])
            page.get_by_role("row", name="To Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_TO_DATE"])
            page.get_by_label("Distribution Threshold").click()
            page.get_by_label("Distribution Threshold").fill(datadictvalue["C_DSTRBTN_THRSHLD"])
            PrevRtngMdl = datadictvalue["C_CODE"]


        #Add Rating Level
        page.get_by_role("link", name="Rating Levels").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Add").click()
        page.wait_for_timeout(2000)
        page.get_by_role("table", name='Rating Levels').get_by_role("row").nth(i).get_by_role("cell", name='Rating Level', exact=True).locator("input").click()
        page.get_by_role("table", name='Rating Levels').get_by_role("row").nth(i).get_by_role("cell", name='Rating Level', exact=True).locator("input").fill(str(datadictvalue["C_RTNG_LEVEL_CODE"]))
        page.get_by_role("table", name='Rating Levels').get_by_role("row").nth(i).get_by_role("cell", name='Name', exact=True).locator("input").fill(datadictvalue["C_RTNG_LEVEL_NAME"])
        page.get_by_role("table", name='Rating Levels').get_by_role("row").nth(i).get_by_role("cell", name='Description', exact=True).locator("input").fill(datadictvalue["C_RTNG_LEVEL_DSCRPTN"])
        page.get_by_role("table", name='Rating Levels').get_by_role("row").nth(i).get_by_role("cell", name='Short Description', exact=True).locator("input").fill(datadictvalue["C_SHORT_DSCRPTN"])
        page.get_by_role("table", name='Rating Levels').get_by_role("row").nth(i).get_by_role("cell", name='Star Rating', exact=True).locator("input").click()
        page.get_by_role("table", name='Rating Levels').get_by_role("row").nth(i).get_by_role("cell", name='Star Rating', exact=True).locator("input").fill(datadictvalue["C_STAR_RTNG"])
        page.get_by_role("table", name='Rating Levels').get_by_role("row").nth(i).get_by_role("cell", name='Numeric Rating', exact=True).locator("input").fill(str(datadictvalue["C_NMR_RTNG"]))
        page.wait_for_timeout(1000)
        page.get_by_role("table", name='Rating Levels').get_by_role("row").nth(i).get_by_role("combobox", name='Career Strength or Development', exact=True).type(datadictvalue["C_CRR_STRNGTH_DVLPMNT"])

        #Add Review Points
        page.get_by_role("link", name="Review Points").click()
        page.wait_for_timeout(2000)
        page.get_by_role("cell", name="Review Points", exact=True).locator("input").nth(i).fill(str(datadictvalue["C_RVW_PNTS"]))
        page.get_by_role("cell", name="From Points", exact=True).locator("input").nth(i).fill(str(datadictvalue["C_FROM_PNTS"]))
        page.get_by_role("cell", name="To Points", exact=True).locator("input").nth(i).fill(str(datadictvalue["C_TO_PNTS"]))
        page.wait_for_timeout(2000)

        #Rating Categories
        page.get_by_role("link", name="Rating Categories").click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_CTGRY_NAME"] !="":
            page.get_by_role("button", name="Add").click()
            page.wait_for_timeout(2000)
            page.get_by_role("cell", name="Category Name", exact=True).locator("input").nth(0).click()
            page.get_by_role("cell", name="Category Name", exact=True).locator("input").nth(0).fill(datadictvalue["C_CTGRY_NAME"])
            page.get_by_role("cell", name="Category Description", exact=True).locator("input").nth(0).fill(datadictvalue["C_CTGRY_DSCRPTN"])
            page.get_by_role("cell", name="Lower Boundary", exact=True).locator("input").nth(0).fill(str(datadictvalue["C_LOWER_BNDRY"]))
            page.get_by_role("cell", name="Upper Boundary", exact=True).locator("input").nth(0).fill(str(datadictvalue["C_UPPER_BNDRY"]))

        #Distributions
        page.get_by_role("link", name="Distributions").click()
        page.wait_for_timeout(2000)
        page.get_by_role("cell", name='Minimum Distribution', exact=True).locator("input").nth(i).fill(str(datadictvalue["C_MIN_DSTRBTN"]))
        page.get_by_role("cell", name='Maximum Distribution', exact=True).locator("input").nth(i).fill(str(datadictvalue["C_MAX_DSTRBTN"]))

        print("Row Added - ", str(r))
        datadictvalue["RowStatus"] = "Row Added"
        i = i + 1
        r = r + 1

        #Do the save of the last rating model before signing out
        if r == rowcount:
            page.wait_for_timeout(5000)
            page.get_by_role("button", name="Cancel").click()
            try:
                expect(page.get_by_role("heading", name="Search Results")).to_be_visible()
                print("Rating Model Saved")
                datadictvalue["RowStatus"] = "Rating Model Saved"
            except Exception as e:
                print("Unable to save rating model")
                datadictvalue["RowStatus"] = "Unable to save rating model"

    page.wait_for_timeout(2000)
    OraSignOut(page, context, browser, videodir)
    return datadict


#****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, RATING_MODEL_SHEET_NAME):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, RATING_MODEL_SHEET_NAME, PRCS_DIR_PATH + PERF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PERF_CONFIG_WRKBK, RATING_MODEL_SHEET_NAME)
    if rows > 1:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0] + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))