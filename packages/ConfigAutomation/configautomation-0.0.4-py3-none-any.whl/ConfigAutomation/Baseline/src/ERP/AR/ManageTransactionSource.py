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
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("Manage Transaction Sources")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Manage Transaction Sources", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Create").click()

        #Transaction source set
        page.get_by_role("button", name="Search", exact=True).click()
        page.get_by_title("Search: Transaction Source Set").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Reference Data Set Name").click()
        page.get_by_label("Reference Data Set Name").fill(datadictvalue["C_TRNSCTN_SRC_SET"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("cell", name=datadictvalue["C_TRNSCTN_SRC_SET"], exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        if datadictvalue["C_LEGAL_ENTTY"] != "":
            page.get_by_title("Search: Legal Entity").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Legal Entity Name").click()
            page.get_by_label("Legal Entity Name").fill(datadictvalue["C_LEGAL_ENTTY"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_LEGAL_ENTTY"], exact=True).click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(2000)

        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(2000)
        page.get_by_label("Description").click()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        page.get_by_label("Type", exact=True).select_option(datadictvalue["C_TYPE"])
        page.wait_for_timeout(2000)

        page.locator("//label[text()='From Date']//following::input[1]").click()
        page.locator("//label[text()='From Date']//following::input[1]").fill(datadictvalue["C_FROM_DATE"].strftime('%m/%d/%y'))

        if datadictvalue["C_TO_DATE"] != "":
            page.locator("//label[text()='To Date']//following::input[1]").click()
            page.locator("//label[text()='To Date']//following::input[1]").fill(datadictvalue["C_TO_DATE"].strftime('%m/%d/%y'))
            page.wait_for_timeout(2000)

        if datadictvalue["C_ATMTC_TRNSCTN_NMBRNG"] == 'Yes':
            if not page.get_by_text("Automatic transaction").is_checked():
                page.get_by_text("Automatic transaction").click()
        if datadictvalue["C_ATMTC_TRNSCTN_NMBRNG"] == 'No':
            if page.get_by_text("Automatic transaction").is_checked():
                page.get_by_text("Automatic transaction").click()

        page.get_by_label("Last Transaction Number").click()
        page.get_by_label("Last Transaction Number").fill(str(datadictvalue["C_LAST_TRNSCTN_NMBR"]))

        if datadictvalue["C_RCPT_HNDLNG_FOR_CRDTS"] != "":
            page.get_by_label("Receipt Handling for Credits").select_option(datadictvalue["C_RCPT_HNDLNG_FOR_CRDTS"])

        if datadictvalue["C_COPY_DCMNT_NMBR_TO_TRNSCTN_NMBR"] == "Yes":
            page.get_by_text("Copy document number to").click()

        if datadictvalue["C_ALLOW_DPLCT_TRNSCTN_NMBRS"] == "Yes":
            page.get_by_text("Allow duplicate transaction numbers").click()

        if datadictvalue["C_COPY_TRNSCTN_INFRMTN_FLXFLD_TO_CRDT_MEMO"] == "Yes":
            page.get_by_text("Copy transaction information flexfield to credit memo").click()

        page.get_by_text("Control transaction completion").click()

        if datadictvalue["C_RFRNC_FIELD_DFLT_VALUE"] != "":
            page.get_by_label("Reference Field Default Value").select_option(datadictvalue["C_RFRNC_FIELD_DFLT_VALUE"])

        if datadictvalue["C_STDRD_TRNSCTN_TYPE"] != "":
            page.get_by_title("Search: Standard Transaction").click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//div[text()='Search and Select: Standard Transaction Type']//following::label[text()='Name']//following::input[1]").click()
            page.locator("//div[text()='Search and Select: Standard Transaction Type']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_STDRD_TRNSCTN_TYPE"])
            page.locator("//div[text()='Search and Select: Standard Transaction Type']//following::label[text()='Name']//following::input[1]").press("Enter")
            page.get_by_role("cell", name=datadictvalue["C_STDRD_TRNSCTN_TYPE"]).nth(3).click()
            page.get_by_role("button", name="OK").click()

        if datadictvalue["C_CRDT_TRNSCTN_SRC"] != "":
            page.get_by_title("Search: Credit Transaction").click()
            page.get_by_role("link", name="Search...").click()
            page.locator("//div[text()='Search and Select: Credit Transaction Source']//following::label[text()='Name']//following::input[1]").click()
            page.locator("//div[text()='Search and Select: Credit Transaction Source']//following::label[text()='Name']//following::input[1]").fill(datadictvalue["C_CRDT_TRNSCTN_SRC"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_CRDT_TRNSCTN_SRC"], exact=True).click()
            page.get_by_role("button", name="OK").click()

        if datadictvalue["C_RGNL_INFRMTN"] != "":
            page.get_by_label("Regional Information").select_option(datadictvalue["C_RGNL_INFRMTN"])

        if datadictvalue["C_TYPE"] == "Imported":
            page.get_by_label("Invalid Line").click()
            page.get_by_label("Invalid Line").select_option(datadictvalue["C_INVLD_LINE"])

            page.get_by_label("Accounting Date in a Closed").click()
            page.get_by_label("Accounting Date in a Closed").select_option(datadictvalue["C_ACCNTNG_DATE_IN_A_CLSD_PRD"])

            page.get_by_label("Grouping Rule").fill(datadictvalue["C_GRPNG_RULE"])

            if datadictvalue["C_CRT_CLRNG"] == "Yes":
                page.get_by_text("Create clearing").click()

            if datadictvalue["C_ALLOW_SALES_CRDTS"] == 'Yes':
                if not page.get_by_text("Automatic transaction").is_checked():
                    page.get_by_text("Allow sales credits").click()
            if datadictvalue["C_ALLOW_SALES_CRDTS"] == 'No':
                if page.get_by_text("Allow sales credits").is_checked():
                    page.get_by_text("Allow sales credits").click()

            if datadictvalue["C_SLSPRSN"] !='':
                page.get_by_role("group", name="Salesperson").get_by_text(datadictvalue["C_SLSPRSN"], exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_SALES_CRDT_TYPE"] != '':
                page.get_by_role("group", name="Sales credit type").get_by_text(datadictvalue["C_SALES_CRDT_TYPE"], exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_SALES_CRDT"] != '':
                page.get_by_role("group", name="Sales credit").get_by_text(datadictvalue["C_SALES_CRDT"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_BILL_TO_CSTMR"] != '':
                page.get_by_role("group", name="Bill-to customer").get_by_text(datadictvalue["C_BILL_TO_CSTMR"], exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_BILL_TO_ADDRSS"] != '':
                page.get_by_role("group", name="Bill-to Address").get_by_text(datadictvalue["C_BILL_TO_ADDRSS"], exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_BILL_TO_CNTCT"] != '':
                page.get_by_role("group", name="Bill-to Contact").get_by_text(datadictvalue["C_BILL_TO_CNTCT"], exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_SHIP_TO_CSTMR"] != '':
                page.get_by_role("group", name="Ship-to Customer").get_by_text(datadictvalue["C_SHIP_TO_CSTMR"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_SHIP_TO_ADDRSS"] != '':
                page.get_by_role("group", name="Ship-to Address").get_by_text(datadictvalue["C_SHIP_TO_ADDRSS"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_SHIP_TO_CNTCT"] != '':
                page.get_by_role("group", name="Ship-to Contact").get_by_text(datadictvalue["C_SHIP_TO_CNTCT"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_SOLD_TO_CSTMR"] != '':
                page.get_by_role("group", name="Sold-to Customer").get_by_text(datadictvalue["C_SOLD_TO_CSTMR"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_PYMNT_MTHD_RULE"] != '':
                page.get_by_role("group", name="Payment Method Rule").get_by_text(datadictvalue["C_PYMNT_MTHD_RULE"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_CSTMR_BANK_ACCNT"] != '':
                page.get_by_role("group", name="Customer Bank Account").get_by_text(datadictvalue["C_CSTMR_BANK_ACCNT"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_INVCNG_RULE"] != '':
                page.get_by_role("group", name="Invoicing Rule").get_by_text(datadictvalue["C_INVCNG_RULE"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_RVN_SCHDLNG_RULE"] != '':
                page.get_by_role("group", name="Rule").get_by_text(datadictvalue["C_RULE"], exact=True).nth(2)
                page.wait_for_timeout(1000)
            if datadictvalue["C_ACCNTNG_FLXFLD"] != '':
                page.get_by_role("group", name="Accounting Flexfield").get_by_text(datadictvalue["C_ACCNTNG_FLXFLD"], exact=True).click()
                page.wait_for_timeout(1000)

            if datadictvalue["C_DRV_DATE"] == "Yes":
                page.get_by_text("Derive date").click()
            if datadictvalue["C_PYMNT_TERMS"] != '':
                page.get_by_role("group", name="Payment Terms").get_by_text(datadictvalue["C_PYMNT_TERMS"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_RVN_ACCNT_ALLCTN"] != '':
                page.get_by_role("group", name="Revenue Account Allocation").get_by_text(datadictvalue["C_RVN_ACCNT_ALLCTN"], exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_TRNSCTN_TYPE"] != '':
                page.get_by_role("group", name="Transaction Type").get_by_text(datadictvalue["C_TRNSCTN_TYPE"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_BILL_TO_CNTCT"] != '':
                page.get_by_role("group", name="Memo Reason").get_by_text(datadictvalue["C_MEMO_RSN"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_MEMO_RSN"] != '':
                page.get_by_role("group", name="Memo Line Rule").get_by_text(datadictvalue["C_MEMO_LINE_RULE"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_INVNTRY_ITEM"] != '':
                page.get_by_role("group", name="Inventory item").get_by_text(datadictvalue["C_INVNTRY_ITEM"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_UNIT_OF_MSR"] != '':
                page.get_by_role("group", name="Unit of Measure").get_by_text(datadictvalue["C_UNIT_OF_MSR"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_FOB_POINT"] != '':
                page.get_by_role("group", name="FOB Point").get_by_text(datadictvalue["C_FOB_POINT"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_FRGHT_CRRR"] != '':
                page.get_by_role("group", name="Freight Carrier").get_by_text(datadictvalue["C_FRGHT_CRRR"],exact=True).click()
                page.wait_for_timeout(1000)
            if datadictvalue["C_RLTD_DCMNT"] != '':
                page.get_by_role("group", name="Related Document").get_by_text(datadictvalue["C_RLTD_DCMNT"],exact=True).click()
                page.wait_for_timeout(1000)

        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Save and Close").click()

        # Repeating the loop
        i = i + 1

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Manage Transaction Sources Saved Successfully")
            datadictvalue["RowStatus"] = "Manage Transaction Sources are added successfully"

        except Exception as e:
            print("Manage Transaction Sources not saved")
            datadictvalue["RowStatus"] = "Manage Transaction Sources are not added"

        OraSignOut(page, context, browser, videodir)
        return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, TRANS_SOURCE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + AR_WORKBOOK, TRANS_SOURCE, PRCS_DIR_PATH + AR_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + AR_WORKBOOK, TRANS_SOURCE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + TRANS_SOURCE)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", AR_WORKBOOK)[0] + "_" + TRANS_SOURCE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))