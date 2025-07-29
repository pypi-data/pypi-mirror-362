import pandas as pd
from playwright.sync_api import Page, Browser, BrowserContext
from datetime import datetime
import re
from ConfigAutomation.Baseline.src.ConfigFileNames import *

# Environment and Credentials
# BASEURL = "https://fa-eqhh-dev6-saasfademo1.ds-fa.oraclepdemos.com"
BASEURL = "https://faulkner-iccjjb-test.fa.ocs.oraclecloud.com/"
# BASEURL = "https://setonhill-ibtwjb-test.fa.ocs.oraclecloud.com/"
IMPLUSRID = "dharmendra.mirapakayala@drivestream.com"
IMPLUSRPWD = "G9ltJ0Z5B2scS3H6"



def ImportWrkbk(WrkbkName: str, SheetName: str):
    df = pd.read_excel(WrkbkName, sheet_name=SheetName, na_filter=False, dtype='object')
    rows, cols = df.shape
    if rows > 0:
        datadict = df.to_dict('index')
        print("Total Number of Data Rows Present in the formatted sheet - ", rows)
        # print("Worksheet Output - ", datadict)
        return rows, cols, datadict


def write_status(inputdict: dict, ResultsFile: str):
    df1 = pd.DataFrame(inputdict).T
    df1.to_excel(ResultsFile)


def OpenBrowser(playwright, HeadlessMode: bool, videodir: str) -> tuple[Browser, BrowserContext, Page]:
    browser = playwright.chromium.launch(headless=HeadlessMode, timeout=30000)
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81"
    context = browser.new_context(user_agent=ua, record_video_dir=videodir + "/",
                                  record_video_size={'width': 1300, 'height': 710})
    page = context.new_page()
    return browser, context, page


def OraSignOut(page: Page, context, browser, videodir):
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Sign Out").click()
    page.get_by_role("button", name="Confirm").click()
    context.close()
    page.video.save_as(videodir + "/" + "SuccessVideo_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".webm")
    page.video.delete()
    browser.close()


def CheckWrkbkForProcessing(WrkbkName: str, SheetName: str) -> bool:
    # The function has been overriden to return True always because the
    # execution sequence picks up from A_TemplateDetails tab in the config
    # workbook
    return True

    # df = pd.read_excel(WrkbkName, sheet_name="A_TemplateDetails", na_filter=False, dtype='object', header=None)
    # rows, cols = df.shape
    # datadict = df.to_dict('index')
    #
    # # Initializations
    # r = 0
    # while r < rows:
    #     # Check if sheet name is mentioned in A_TemplateDetails Tab in the A_SheetNames row
    #     if datadict[r][0] == "A_SheetNames":
    #         print("Checking in Template details > Sheet Names if sheet is mentioned")
    #         if SheetName in datadict[r][1]:
    #             print("Sheet Name is mentioned in A_Template Details. Proceeding to process..")
    #             return True
    #         else:
    #             print("Sheet Name not mentioned in A_Template Details. Processing will be skipped")
    #             return False
    #     r = r + 1


def GetSheetNames(WrkbkName: str) -> list:
    df = pd.read_excel(WrkbkName, sheet_name="A_TemplateDetails", na_filter=False, dtype='object', header=None)
    rows, cols = df.shape
    datadict = df.to_dict('index')
    print("Total Number of Rows Present in the A_TemplateDetails sheet - ", rows)

    # Initializations
    r = 0
    while r < rows:
        # Check if sheet name is mentioned in A_TemplateDetails Tab in the A_SheetNames row
        if datadict[r][0] == "A_SheetNames":
            SheetNames = datadict[r][1].split(",")
            NoOfSheets = len(SheetNames)
            print("Total Number of sheets taken for configuration - ", NoOfSheets)
            return SheetNames
        r = r + 1


def CreateWrkbkForProcessing(SrcWrkbkName: str, SheetName: str, TrgtWrkbkName: str):
    df = pd.read_excel(SrcWrkbkName, sheet_name=SheetName, na_filter=False, dtype='object', header=None)
    rows, cols = df.shape
    datadict = df.to_dict('index')
    print("Total Number of Rows Present in the Source worksheet - ", rows)
    # print("Worksheet Output - ", datadict)

    # Initializations
    r = 0
    datadictnew = {}
    StartRow = 0

    while r < rows:
        # If current row is more than startrow index, write the row to the new dictionary
        if StartRow > 0 and (r == StartRow - 1 or r > StartRow - 1):
            print("Writing Data Row - ", r)
            datadictnew[r] = datadict[r]
            r = r + 1
            continue

        # Check for the header row, if found write the row to the new dictionary
        # Also update to remove any text after flower braces { on the header row
        if datadict[r][0] == "A_RawDataTableColumn":
            print("Header Row Found")
            datadictnew[r] = datadict[r]
            datadictnew[r].update((key, re.split("{", val)[0].strip()) for key, val in datadictnew[r].items())
            r = r + 1
            continue

        # Check for start row, if yes get the row number
        if "A_StartRow" in datadict[r][0]:
            FindRowNum = re.findall(r'\d+', datadict[r][0])
            StartRow = int(FindRowNum[0])
            print("Start Row Found - ", StartRow)
            r = StartRow - 1
            continue

        # Increment for next iteration
        r = r + 1
    df1 = pd.DataFrame(datadictnew).T
    df1.to_excel(TrgtWrkbkName, sheet_name=SheetName, header=False, index=False)

def SingleSignONwithUserPwd(page: Page):
    page.get_by_role("button", name="Company Single Sign-On").click()
    page.wait_for_timeout(10000)
    page.locator("//div[text()='Sign in']//following::input[1]").clear()
    page.locator("//div[text()='Sign in']//following::input[1]").type(IMPLUSRID)
    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(10000)
    # page.locator("//div[text()='Enter password']//following::input[1]").clear()
    page.get_by_placeholder("Password").clear()
    page.get_by_placeholder("Password").type(IMPLUSRPWD)
    # page.locator("//div[text()='Enter password']//following::input[1]").type(IMPLUSRPWD)
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_timeout(10000)
    if page.get_by_role("button", name="Yes").is_visible():
        page.get_by_role("button", name="Yes").click()
    page.wait_for_timeout(40000)

def SigninwithIDCS(page: Page):
    page.get_by_role("textbox", name="User Name").click()
    page.get_by_role("textbox", name="User Name").fill(IMPLUSRID)
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)
    if page.get_by_role("button", name="Yes").is_visible():
        page.get_by_role("button", name="Yes").click()
    page.wait_for_timeout(20000)

