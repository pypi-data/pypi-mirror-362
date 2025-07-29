from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.ConfigFileNames import *
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)

    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Transmission Configurations")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Transmission Configurations", exact=True).click()
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_label("Select Protocol").click()
        page.get_by_label("Select Protocol").select_option(datadictvalue["C_PRTCL_SLCTD"])
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)
        page.get_by_label("Configuration", exact=True).fill(datadictvalue["C_CNFGRTN"])
        page.get_by_label("Tunneling Configuration").select_option(datadictvalue["C_TNNLNG_CNFGRTN"])
        page.locator("//label[text()='From Date']//following::input[1]").fill(datadictvalue["C_FROM_DATE"])
        page.locator("//label[text()='To Date']//following::input[1]").fill(datadictvalue["C_TO_DATE"])

        if datadictvalue["C_PRTCL_SLCTD"] == 'Secure File Transfer Protocol for Static File Names':

                page.get_by_role("cell", name="*FTP Server IP Address Character Value").get_by_label("Value").fill(datadictvalue["C_FTP_SRVR_IP_ADDRSS"])
                page.get_by_role("cell", name="FTP Server Port Number Number").get_by_label("Value").fill(str(datadictvalue["C_FTP_SRVR_PORT_NMBR"]))
                page.get_by_role("cell", name="*FTP Account User Name Character Value").get_by_label("Value").fill(datadictvalue["C_FTP_ACCNT_USER_NAME"])
                page.get_by_role("cell", name="FTP Account Password Character Value").get_by_label("Value").fill(datadictvalue["C_FTP_CCNT_PSSWRD"])
                page.get_by_role("cell", name="Sent File Name Character Value").get_by_label("Value").fill(datadictvalue["C_SENT_FILE_NAME"])
                page.get_by_role("cell",name="PGP Public Encryption Key Character Value Value Autocompletes on TAB").get_by_label("Value").fill(datadictvalue["C_PGP_PBLC_ENCRYPTN_KEY"])
                page.get_by_role("cell",name="PGP Private Signing Key Character Value Value Autocompletes on TAB").get_by_label("Value").fill(datadictvalue["C_PGP_PRVT_SGNNG_KEY"])

        if datadictvalue["C_PRTCL_SLCTD"] == 'Secure File Transfer Retrieval Protocol for Static File Names':
                page.get_by_role("cell", name="*SFTP Server Name Character").get_by_label("Value").fill(datadictvalue["C_FTP_SRVR_IP_ADDRSS"])
                page.get_by_role("cell", name="SFTP Server Port Number Number Value").get_by_label("Value").fill(str(datadictvalue["C_FTP_SRVR_PORT_NMBR"]))
                page.get_by_role("cell", name="*SFTP Account User Name Character Value").get_by_label("Value").fill(datadictvalue["C_FTP_ACCNT_USER_NAME"])
                page.get_by_role("cell", name="*Local File Directory Character Value").get_by_label("Value").fill(datadictvalue["C_LCL_FILE_DRCTRY"])
                page.get_by_role("cell", name="*Remote File Name Character").get_by_label("Value").fill(datadictvalue["C_RMT_FILE_NAME"])
                page.get_by_role("cell", name="SFTP Account Password Character Value").get_by_label("Value").fill(datadictvalue["C_FTP_CCNT_PSSWRD"])

        page.get_by_role("cell", name="*Remote File Directory Character Value").get_by_label("Value").fill(datadictvalue["C_RMT_FILE_DRCTRY"])
        page.get_by_role("cell",name="Client Private Key File Character Value Value Autocompletes on TAB").get_by_label("Value").fill(datadictvalue["C_CLNT_PRVT_KEY_FILE"])
        page.get_by_role("cell", name="Client Private Key Password Character Value").get_by_label("Value").fill(datadictvalue["C_CLNT_PRVT_KEY_PSSWRD"])
        page.get_by_role("cell", name="Keep Local File Character").get_by_label("Value").fill(datadictvalue["C_KEEP_LCL_FILE"])
        page.get_by_role("cell", name="UNIX Permission Mask for Remote File Character Value").get_by_label("Value").fill(datadictvalue["C_UNIX_PRMSSN_MASK_FOR_RMT_FILE"])
        page.get_by_role("button", name="Save and Close").click()
        #Validation

        try:
            expect(page.locator("//div[text()='Confirmation']//following::button[1]")).to_be_visible()
            page.locator("//div[text()='Confirmation']//following::button[1]").click()
            print("Row Saved Successfully")
            datadictvalue["RowStatus"] = "Configuration Saved Successfully"
        except Exception as e:
            print("Saved UnSuccessfully")
            datadictvalue["RowStatus"] = "Configuration Saved UnSuccessfully"

        i = i + 1


    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, TRANSMISSION_CONFIG):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, TRANSMISSION_CONFIG, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, TRANSMISSION_CONFIG)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + TRANSMISSION_CONFIG)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
                0] + "_" +TRANSMISSION_CONFIG + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))