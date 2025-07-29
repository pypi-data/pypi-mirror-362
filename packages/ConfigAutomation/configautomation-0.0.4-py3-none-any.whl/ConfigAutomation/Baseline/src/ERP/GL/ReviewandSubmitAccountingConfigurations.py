from playwright.sync_api import Playwright, sync_playwright
from ConfigAutomation.Baseline.src.ConfigFileNames import *
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
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="Offering", exact=True).click()
    page.get_by_text("Financials", exact=True).click()
    page.wait_for_timeout(2000)

    i = 0

    while i < rowcount:
        page.wait_for_timeout(3000)
        datadictvalue = datadict[i]

        # Navigating to respective option in Legal Search field and searching
        page.get_by_text("General Ledger").click()
        page.wait_for_timeout(2000)
        page.get_by_role("link", name="Review and Submit Accounting").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(5000)
        Pid = page.locator("//label[contains(text(),'has been submitted.')]").text_content()
        print(Pid)
        Pid1 = Pid.split()
        print(Pid1[5])
        ProcessID = Pid1[5]
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(1000)
        page.get_by_role("link", name="Navigator").click()
        page.get_by_title("Tools", exact=True).click()
        page.get_by_role("link", name="Scheduled Processes").click()
        page.wait_for_timeout(4000)
        page.get_by_label("Expand Search").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Process ID").click()
        page.get_by_label("Process ID").clear()
        page.get_by_label("Process ID").fill(ProcessID)
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(1000)
        status = "Succeeded"
        statusUI = page.locator("//span[text()=" + ProcessID + "]//following::span[1]").text_content()
        print("Process From UI:", statusUI)
        # Refresh untill process get succeeded
        while (statusUI != status):
            if statusUI == "Succeeded" or statusUI == "Warning" or statusUI == "Error":
                print("IF status:", status)
                break
            else:
                page.wait_for_timeout(5000)
                page.get_by_role("button", name="Refresh").click()
                statuselse = page.locator("//span[text()=" + ProcessID + "]//following::span[1]").text_content()
                print("ELSE status :", statuselse)
                if statuselse == status or statuselse == "Warning" or statuselse == "Error":
                    print(" Else IF :", statuselse)
                    break
        page.wait_for_timeout(3000)

        page.locator("//a[@title=\"Settings and Actions\"]").click()
        page.get_by_role("link", name="Setup and Maintenance").click()
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Offering", exact=True).click()
        page.get_by_text("Financials", exact=True).click()
        page.wait_for_timeout(2000)

        # Navigating to respective option in Legal Search field and searching
        page.get_by_text("General Ledger").click()
        page.get_by_role("link", name="Manage Primary Ledgers").click()
        page.wait_for_timeout(5000)
        page.get_by_role("cell", name=datadictvalue["C_NAME"]).nth(1).click()
        if page.get_by_role("cell", name=datadictvalue["C_NAME"]).get_by_role("cell", name="Confirmed", exact=True).is_visible():
            print("Cube is created for the Ledger")
        else:
            print("Cube is not created")

        page.get_by_role("button", name="Done").click()

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, LEDGER):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GL_WORKBOOK, LEDGER, PRCS_DIR_PATH + GL_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GL_WORKBOOK, LEDGER)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + LEDGER)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GL_WORKBOOK)[0] + "_" + LEDGER + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))