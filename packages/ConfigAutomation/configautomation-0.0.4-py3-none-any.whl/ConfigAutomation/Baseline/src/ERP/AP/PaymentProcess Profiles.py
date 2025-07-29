from playwright.sync_api import Playwright, sync_playwright, expect
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
    page.get_by_role("textbox").fill("Manage Payment Process Profiles")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Payment Process Profiles", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(15000)
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.get_by_label("Code").click()
        page.get_by_label("Code").fill(datadictvalue["C_CODE"])
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
        page.locator("//label[text()='From Date']//following::input[1]").fill(datadictvalue["C_FROM_DATE"].strftime("%m/%d/%Y"))
        page.locator("//label[text()='To Date']//following::input[1]").fill(datadictvalue["C_TO_DATE"])
        page.get_by_label("Payment File Format").click()
        page.get_by_label("Payment File Format").type(datadictvalue["C_PYMNT_FILE_FRMT"])
        page.get_by_role("option", name=datadictvalue["C_PYMNT_FILE_FRMT"]).click()

        if datadictvalue["C_PRCSSNG_TYPE"] == 'Electronic':
            page.get_by_label("Processing Type").select_option(datadictvalue["C_PRCSSNG_TYPE"])
            page.get_by_label("Default Payment Document").select_option(datadictvalue["C_DFLT_PYMNT_DCMNT"])
            if datadictvalue["C_ALLOW_MNL_STTNG_OF_PYMNT_CNFRMTN"] == 'Yes':
                page.get_by_text("Allow manual setting of").check()


        if datadictvalue["C_PRCSSNG_TYPE"] == 'Printed':
            page.get_by_label("Processing Type").select_option(datadictvalue["C_PRCSSNG_TYPE"])
            page.get_by_label("Default Payment Document").select_option(datadictvalue["C_DFLT_PYMNT_DCMNT"])
            if datadictvalue["C_PYMNT_FILE"] == 'Send to file':
                page.get_by_text("Send to file").click()
            if datadictvalue["C_PYMNT_FILE"] == 'Send to printer':
                page.get_by_text("Send to printer")
            if datadictvalue["C_ATMTCLLY_PRINT_AFTR_FRMTTNG"] == 'Yes':
                page.get_by_text("Automatically print after").click()


        #Useage Rates
        page.get_by_role("link", name="Usage Rules").click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_PYMNT_MTHDS"] == 'All':
            page.get_by_text("All", exact=True).first.click()
        if datadictvalue["C_PYMNT_MTHDS"] == 'Specify':
            page.get_by_text("Specify").first.get_by_text("Specify").first.click()
            page.get_by_role("button", name="Add Row").first.click()
            page.get_by_title("Search: Payment Methods").first.click()
            page.get_by_title("Search: Payment Methods").click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//label[text()='Name']//following::input[contains(@id,'value10')][1]").fill(datadictvalue["C_SPCFY_PYMNT_MTHD"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_SPCFY_PYMNT_MTHD"],exact=True).click()
            # page.get_by_text(datadictvalue["C_SPCFY_PYMNT_MTHD"], exact=True).click()
            page.get_by_role("button", name="OK").click()

        #dis amount
        if datadictvalue["C_DSBRSMNT_BANK_ACCNTS"] == 'All':
            page.get_by_text("All", exact=True).nth(1).click()

            # page.get_by_text("All", exact=True).first.click()
        if datadictvalue["C_DSBRSMNT_BANK_ACCNTS"] == 'Specify':
            page.get_by_text("Specify").first.get_by_text("Specify").nth(1).click()

        #BU

        if datadictvalue["C_BSNSS_UNITS"] == 'All':
            page.get_by_text("All", exact=True).nth(2).click()
        if datadictvalue["C_BSNSS_UNITS"] == 'Specify':
            page.get_by_text("Specify").nth(2).click()

        #curriences

        if datadictvalue["C_CRRNCS"] == 'All':
            page.get_by_text("All", exact=True).nth(3).click()
        if datadictvalue["C_CRRNCS"] == 'Specify':
            page.get_by_text("Specify").nth(3).click()


       #Payment System
        page.get_by_role("link", name="Payment System").click()

        page.wait_for_timeout(2000)
        page.get_by_label("Payment System", exact=True).click()

        if datadictvalue["C_PYMNT_SYSTM"] != '':
            page.get_by_label("Payment System", exact=True).select_option(datadictvalue["C_PYMNT_SYSTM"])
            page.wait_for_timeout(5000)
            if datadictvalue["C_ATMTCLLY_TRNSMT_FILE_AFTR_FRMTTNG"] == 'Yes':
                page.get_by_text("Automatically transmit").check()


        #Payment
        page.get_by_role("link", name="Payment", exact=True).click()
        page.wait_for_timeout(2000)
        if datadictvalue["C_UNQ_RMTTNC_DNTFR"] == 'Yes':
            page.get_by_text("Unique remittance identifier").click()
        if datadictvalue["C_RMTTNC_MSSG"] == 'Yes':
            page.get_by_text("Remittance message").click()
        if datadictvalue["C_DUE_DATE"] == 'Yes':
            page.get_by_text("Due date").click()

        if datadictvalue["C_BANK_CHRG_BRR"] == 'Yes':
            page.get_by_text("Bank charge bearer").click()
        if datadictvalue["C_DCMNT_GRPNG_RULES_PYMNT_RSN"] == 'Yes':
            page.get_by_text("Payment reason").click()
        if datadictvalue["C_PYMNT_STTLMNT_PRRTY"] == 'Yes':
            page.get_by_text("Settlement priority").click()
        if datadictvalue["C_PYMNT_DLVRY_CHNNL"] == 'Yes':
            page.get_by_text("Delivery channel").click()
        if datadictvalue["C_PYMNT_LTMT_DBTR"] == 'Yes':
            page.get_by_text("Ultimate Debtor").click()
        page.get_by_label("Maximum Documents per Payment").click()
        page.get_by_label("Maximum Documents per Payment").fill(datadictvalue["C_MXMM_DCMNTS_PER_PYMN"])

        #Payment File

        page.get_by_role("link", name="Payment File").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Payment File Accompanying").select_option(datadictvalue["C_PYMNT_FILE_ACCMPNYNG_LTTR_FRMT"])
        page.get_by_label("Outbound Payment File Prefix").click()
        page.get_by_label("Outbound Payment File Prefix").fill(datadictvalue["C_OTBND_PYMNT_FILE_PRFX"])
        page.get_by_label("Outbound Payment File Extension").fill(datadictvalue["C_OTBND_PYMNT_FILE_EXTNSN"])

        if datadictvalue["C_GROUP_BY_BSNSS_UNIT"] == 'Yes':
            page.get_by_text("Group by Business Unit").click()
        if datadictvalue["C_FIRST_PARTY_LEGAL_ENTTY"] == 'Yes':
            page.get_by_text("First party legal entity").click()
        if datadictvalue["C_PYMNT_DATE"] == 'Yes':
            page.get_by_text("Payment date").click()
        if datadictvalue["C_PYMNT_FNCTN"] == 'Yes':
            page.get_by_text("Payment function").click()
        if datadictvalue["C_PYMNT_GRPNG_RULES_PYMNT_RSN"] == 'Yes':
            page.get_by_text("Payment reason").click()
        if datadictvalue["C_PYMNT_PRCSS_RQST"] == 'Yes':
            page.get_by_text("Payment process request").click()
        if datadictvalue["C_BLLS_PYBL"] == 'Yes':
            page.get_by_text("Bills payable").click()
        if datadictvalue["C_RFC_DNTFR"] == 'Yes':
            page.get_by_text("Regional Financial Center").click()
        page.get_by_label("Batch Booking").select_option(datadictvalue["C_BATCH_BKNG"])
        page.get_by_label("Service Level").click()
        page.get_by_label("Service Level").select_option(datadictvalue["C_SRVC_LEVEL"])
        page.get_by_label("Delivery Channel").click()
        page.get_by_label("Delivery Channel").fill(datadictvalue["C_DLVRY_CHNNL"])
        page.get_by_label("Currency", exact=True).click()
        page.get_by_label("Currency", exact=True).select_option(datadictvalue["C_PYMNT_CRRNCY"])
        page.get_by_label("Number of Payments").click()
        page.get_by_label("Number of Payments").fill(datadictvalue["C_NMBR_OF_PYMNTS"])
        if datadictvalue["C_CNVRSN_RATE_TYPE"] != '':
            page.get_by_title("Search: Conversion Rate Type").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_role("textbox", name="Conversion Rate Type").click()
            page.get_by_role("textbox", name="Conversion Rate Type").fill(datadictvalue["C_CNVRSN_RATE_TYPE"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_CNVRSN_RATE_TYPE"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            # page.get_by_title("Search: Conversion Rate Type").click()
            # page.get_by_text(datadictvalue["C_CNVRSN_RATE_TYPE"], exact=True).click()
            # page.get_by_role("cell", name=datadictvalue["C_CNVRSN_RATE_TYPE"], exact=True).click()

        #Bank Instructions
        page.get_by_label("First sort").click()
        page.get_by_label("First sort").select_option(datadictvalue["C_FIRST_SORT"])
        page.get_by_label("Second sort").click()
        page.get_by_label("Second sort").select_option(datadictvalue["C_SCND_SORT"])
        page.get_by_label("Third sort").click()
        page.get_by_label("Third sort").select_option(datadictvalue["C_THIRD_SORT"])

        page.get_by_label("Bank Instruction 1").select_option(datadictvalue["C_BANK_INSTRCTN_1"])
        page.get_by_label("Bank Instruction 2").select_option(datadictvalue["C_BANK_INSTRCTN_2"])
        page.get_by_label("Bank Instruction Details").fill(datadictvalue["C_BANK_INSTRCTN_DTLS"])
        page.get_by_label("Payment Text Message 1").fill(datadictvalue["C_PYMNT_TEXT_MSSG_1"])
        page.get_by_label("Payment Text Message 2").fill(datadictvalue["C_PYMNT_TEXT_MSSG_2"])

        #Grouping

        if datadictvalue["C_GRP_PYMNT_DATE"] == 'Yes':
            page.get_by_text("Payment Date").click()
        if datadictvalue["C_DSBRSMNT_BANK_ACCNT"] == 'Yes':
            page.get_by_text("Disbursement Bank Account").click()
        if datadictvalue["C_LTMT_DBTR"] == 'Yes':
            page.get_by_text("Ultimate Debtor").click()
        if datadictvalue["C_SRVC_LEVEL_AND_DLVRY_CHNNL"] == 'Yes':
            page.get_by_text("Service Level and Delivery").click()
        if datadictvalue["C_CTGRY_PRPS"] == 'Yes':
            page.get_by_text("Category Purpose").click()
        if datadictvalue["C_STTLMNT_PRRTY"] == 'Yes':
            page.get_by_text("Settlement Priority").click()
        if datadictvalue["C_CHRG_BRR"] == 'Yes':
            page.get_by_text("Charge Bearer").click()
        #Reporting

        page.get_by_role("link", name="Reporting").click()
        page.wait_for_timeout(2000)
        #Payment File Register

        page.locator("//h1[text()='Payment File Register']//following::select[1]").click()
        page.locator("//h1[text()='Payment File Register']//following::select[1]").select_option(datadictvalue["C_PYMNT_FILE_RGSTR_FRMT"])
        if datadictvalue["C_ATMTCLLY_SBMT_WHEN_PYMNTS_ARE_CNFRMD"] == 'Yes':
            page.get_by_text("Automatically submit when").first.check()
        # Positive Pay
        page.locator("//h1[text()='Positive Pay']//following::select[1]").select_option(datadictvalue["C_PSTV_PAY_FRMT"])
        page.get_by_label("File Extension").fill(datadictvalue["C_FILE_EXTNSN"])
        page.get_by_label("File Prefix").fill(datadictvalue["C_FILE_PRFX"])
        if datadictvalue["C_ATMTCLLY_TRNSMT_FILE"] == 'Yes':
            page.get_by_text("Automatically transmit file").click()
        page.locator("//h1[text()='Separate Remittance Advice']//following::select[1]").click()
        page.locator("//h1[text()='Separate Remittance Advice']//following::select[1]").select_option(datadictvalue["C_SPRT_RMTTNCE_FRMT"])
        if datadictvalue["C_ATMTCLLY_SBMT_WHN_PYMNTS_R_CNFRMD"] == 'Yes':
            page.get_by_text("Automatically submit when").nth(1).check()
        if datadictvalue["C_ALLOW_MLTPL_CPS_FOR_PYMNT_FILE"] == 'Yes':
            page.get_by_text("Allow multiple copies for").check()

        page.get_by_label("Condition").select_option(datadictvalue["C_CNDTN"])
        page.get_by_label("Delivery Method", exact=True).select_option(datadictvalue["C_DLVRY_MTHD"])
        page.get_by_label("Reporting Option").select_option(datadictvalue["C_RPRTNG_OPTN"])

        # Save and Close
        page.get_by_role("button", name="Save and Close").click()


        try:
            expect(page.get_by_role("button", name="OK")).to_be_visible()
            page.get_by_role("button", name="OK").click()
            print("Row Saved Successfully")
            datadictvalue["RowStatus"] = "Saved Successfully"
        except Exception as e:
            print("Row Saved UnSuccessfully")
            datadictvalue["RowStatus"] = "UnSuccessfull"


        i = i + 1
        page.wait_for_timeout(3000)
    page.get_by_role("button", name="Done").click()

    try:
        expect(page.get_by_role("heading", name="Search")).to_be_visible()
        print("Saved Successfully")
        datadictvalue["RowStatus"] = "Saved Successfully"
    except Exception as e:
        print("Saved UnSuccessfully")
        datadictvalue["RowStatus"] = "UnSuccessfull"

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYMENT_PROCESS_PROFILES):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AP_WORKBOOK, PAYMENT_PROCESS_PROFILES, PRCS_DIR_PATH + AP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AP_WORKBOOK, PAYMENT_PROCESS_PROFILES)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[0] + "_" + PAYMENT_PROCESS_PROFILES)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AP_WORKBOOK)[
                0] + "_" +PAYMENT_PROCESS_PROFILES + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))