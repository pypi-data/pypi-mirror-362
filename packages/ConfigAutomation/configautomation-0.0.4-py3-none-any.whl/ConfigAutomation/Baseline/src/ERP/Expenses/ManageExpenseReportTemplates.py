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
    page.get_by_role("textbox").fill("Manage Expense Report Templates")
    page.get_by_role("textbox").press("Enter")
    page.get_by_role("link", name="Manage Expense Report Templates", exact=True).click()

    PrevName = ''
    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(2000)

        if datadictvalue["C_NAME"] != PrevName:
            # Save the prev type data if the row contains a new type
            if i > 0:
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Save and Close").click()
                if page.get_by_role("button", name="Yes").is_visible():
                    page.get_by_role("button", name="Yes").click()
                try:
                    expect(page.get_by_role("button", name="Done")).to_be_visible()
                    print("Expense report template Saved successfully")
                    datadict[i - 1]["RowStatus"] = "Expense report template Saved successfully"
                except Exception as e:
                    print("Unable to save Expense report template")
                    datadict[i - 1]["RowStatus"] = "Unable to save Expense report template"

                page.wait_for_timeout(5000)
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(2000)
            page.get_by_role("link", name="Expense Types").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Name", exact=True).click()
            page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])
            page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])
            page.get_by_label("Business Unit").clear()
            page.get_by_label("Business Unit").type(datadictvalue["C_BSNSS_UNIT"])
            page.get_by_role("option", name=datadictvalue["C_BSNSS_UNIT"]).click()
            page.locator("//input[contains(@id,'StartDate')]").first.clear()
            page.locator("//input[contains(@id,'StartDate')]").first.fill(datadictvalue["C_EFFCTV_START_DATE"].strftime("%m/%d/%Y"))
            if datadictvalue["C_EFFCTV_END_DATE"] != '':
                page.locator("//input[contains(@id,'EndDate')]").first.fill(datadictvalue["C_EFFCTV_END_DATE"].strftime("%m/%d/%Y"))
            PrevName = datadictvalue["C_NAME"]
            page.wait_for_timeout(4000)

        #Add the Expense Types
        page.get_by_role("link", name="Expense Types").click()
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_EXP_TYPE_NAME"])
        page.get_by_label("Description").fill(datadictvalue["C_EXP_TYPE_DSCRPTN"])
        page.get_by_label("Category", exact=True).select_option(datadictvalue["C_CTGRY"])
        if datadictvalue["C_TAX_CLSSFCTN_CODE"] !='':
            page.get_by_label("Tax Classification Code").type(datadictvalue["C_TAX_CLSSFCTN_CODE"])
            page.get_by_role("option", name=datadictvalue["C_TAX_CLSSFCTN_CODE"]).click()
        if datadictvalue["C_TAX_PRDCT_CTGRY"] != '':
            page.get_by_label("Tax Product Category").type(datadictvalue["C_TAX_PRDCT_CTGRY"])
            page.get_by_role("option", name=datadictvalue["C_TAX_PRDCT_CTGRY"]).click()
        page.locator("//input[contains(@id,'StartDate')]").first.clear()
        page.locator("//input[contains(@id,'StartDate')]").first.fill(datadictvalue["C_EXP_TYPE_EFFCTV_START_DATE"].strftime("%m/%d/%Y"))
        if datadictvalue["C_EXP_TYPE_EFFCTV_END_DATE"] != '':
            page.locator("//input[contains(@id,'EndDate')]").first.fill(datadictvalue["C_EXP_TYPE_EFFCTV_END_DATE"].strftime("%m/%d/%Y"))
        page.locator("//label[contains(text(),'Account')]//following::a[contains(@title,'Search:')]").click()
        # page.get_by_title("Search: DSAT_Account").click()
        page.get_by_role("link", name="Search...").click()
        page.get_by_label("Value").fill(str(datadictvalue["C_NTRL_ACCNT"]))
        page.get_by_role("button", name="Search", exact=True).click()
        page.get_by_role("cell", name=str(datadictvalue["C_NTRL_ACCNT"]), exact=True).locator("span").click()
        page.get_by_role("button", name="OK").click()
        if datadictvalue["C_THIS_EXPNS_TYPE_USED_IN_ITMZTN_ONLY"] == 'Yes':
            page.get_by_text("This expense type used in").check()
        if datadictvalue["C_THIS_EXPNS_TYPE_USED_IN_ITMZTN_ONLY"] == 'No':
            page.get_by_text("This expense type used in").uncheck()
        page.wait_for_timeout(4000)

        #Itemization

        #Itemization will be enabled if atleast one expense type is added to the template

        if datadictvalue["C_ITMZTN"] != 'Disabled' or '':
            # if i > 0 and page.get_by_label("Itemization", exact=True).is_enabled():
            page.wait_for_timeout(2000)
            page.get_by_role("link", name="Itemization").click()
            page.get_by_label("Itemization", exact=True).select_option(datadictvalue["C_ITMZTN"])
            page.wait_for_timeout(2000)
            if datadictvalue["C_INCLD"] == 'Yes':
                page.locator("//span[text()='"+datadictvalue["C_ITEM_EXPNS_TYPE"]+"']//following::label[contains(@id, 'chkItemize')]").check()
            if datadictvalue["C_INCLD"] == 'No' or '':
                page.locator("//span[text()='"+datadictvalue["C_ITEM_EXPNS_TYPE"]+"']//following::label[contains(@id, 'chkItemize')]").uncheck()

        #Project Expenditure Type
        if datadictvalue["C_ENBL_PRJCTS"] =='Yes':
            page.get_by_role("link", name="Project Expenditure Type").click()
            page.get_by_text("Enable projects").check()
            page.wait_for_timeout(5000)
            page.get_by_title("Default Project Expenditure").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Expenditure Type", exact=True).fill(datadictvalue["C_DFLT_PRJCT_EXPNDTR_TYPE"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_DFLT_PRJCT_EXPNDTR_TYPE"], exact=True).locator("span").click()
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(1000)
            if datadictvalue["C_RQR_RCPTS_FOR_PRJCT_EXPNSS"] == 'Yes':
                page.get_by_text("Require receipts for project").check()
            if datadictvalue["C_RQR_RCPTS_FOR_PRJCT_EXPNSS"] == 'No':
                page.get_by_text("Require receipts for project").uncheck()
            if datadictvalue["C_PRJCT_UNIT"] != '':
                page.get_by_role("button", name="Add Row").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Project Unit").click()
                page.get_by_label("Project Unit").select_option(datadictvalue["C_PRJCT_UNIT"])
                page.wait_for_timeout(4000)
                page.get_by_title("Project Expenditure Type", exact=True).click()
                page.get_by_role("link", name="Search...").click()
                page.get_by_label("Expenditure Type", exact=True).fill(datadictvalue["C_PRJCT_EXPNDTR_TYPE"])
                page.get_by_role("button", name="Search", exact=True).click()
                page.get_by_role("cell", name=datadictvalue["C_PRJCT_EXPNDTR_TYPE"], exact=True).locator("span").click()
                page.get_by_role("button", name="OK").click()

        #Receipt Requirement
        page.wait_for_timeout(2000)
        page.get_by_role("link", name="Receipt Requirement").click()
        if page.locator("//label[text()='Require Receipts for Cash Expense Lines']//following::label[text()='"+datadictvalue["C_RQR_RCPTS_FOR_CASH_EXPNS_LINES"]+"'][1]").is_visible():
            page.locator("//label[text()='Require Receipts for Cash Expense Lines']//following::label[text()='"+datadictvalue["C_RQR_RCPTS_FOR_CASH_EXPNS_LINES"]+"'][1]").click()
        if page.locator("//label[text()='Require Receipts for Corporate Card Expense Lines']//following::label[text()='"+datadictvalue["C_RQR_RCPTS_FOR_CRPRT_CARD_EXPNS_LINES"]+"'][1]").is_visible():
            page.locator("//label[text()='Require Receipts for Corporate Card Expense Lines']//following::label[text()='"+datadictvalue["C_RQR_RCPTS_FOR_CRPRT_CARD_EXPNS_LINES"]+"'][1]").click()
        if page.get_by_label("Apply Receipt Requirement").is_visible():
            page.get_by_label("Apply Receipt Requirement").select_option(datadictvalue["C_APPLY_RCPT_RQRMNT_RULES_TO_NGTV_EXPNS_LINES"])
        if page.get_by_label("Display receipt missing").is_visible():
            page.get_by_label("Display receipt missing").select_option(datadictvalue["C_DSPLY_RCPT_MSSNG_PLCY_WRNNG_TO_USER"])
        if datadictvalue["C_SPPRTNG_DCMNTS_RQRD"] == 'Yes':
            page.get_by_text("Supporting documents required").check()
            page.wait_for_timeout(3000)
            if page.get_by_label("Display missing documents").is_enabled():
                page.get_by_label("Display missing documents").select_option(datadictvalue["C_DSPLY_MSSNG_DCMNTS_PLCY_WRNNG_TO_USER"])

        # Expense Fields
        page.wait_for_timeout(2000)
        page.get_by_role("link", name="Expense Fields").click()
        page.get_by_label("Description").nth(1).select_option(datadictvalue["C_EXP_DSCRPTN"])
        if page.get_by_label("Expense Location").is_visible():
            page.get_by_label("Expense Location").select_option(datadictvalue["C_EXP_EXPNS_LCTN"])
        if page.get_by_label("Number of Days").is_visible():
            page.get_by_label("Number of Days").select_option(datadictvalue["C_EXP_NMBR_OF_DAYS"])
        if page.get_by_label("Merchant Name").is_visible():
            page.get_by_label("Merchant Name").select_option(datadictvalue["C_EXP_MRCHNT_NAME"])

        #Policies
        #Expense Policy
        page.get_by_role("link", name="Policies").click()
        page.wait_for_timeout(5000)
        if page.get_by_role("heading", name="Expense Policy").is_visible() and page.locator("//div[@title='Expense Policy']//following::img[@title='Add Row'][1]").is_enabled():
            page.locator("//div[@title='Expense Policy']//following::img[@title='Add Row'][1]").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Policy Name").click()
            page.get_by_label("Policy Name").select_option(datadictvalue["C_EXP_PLCY_NAME"])
            page.wait_for_timeout(1000)
            page.get_by_role("cell", name="Press down arrow to access Calendar Start Date Select Date",
                             exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_PLCY_START_DATE"].strftime("%m/%d/%Y"))
            page.wait_for_timeout(1000)
            page.get_by_role("heading", name="Expense Policy").click()
            page.wait_for_timeout(3000)
            if datadictvalue["C_PLCY_END_DATE"] != '':
                page.get_by_role("cell", name="Press down arrow to access Calendar End Date Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_PLCY_END_DATE"].strftime("%m/%d/%Y"))

        #Attendees policy
        page.wait_for_timeout(2000)
        if page.get_by_role("heading", name="Attendees Policy").is_visible() and page.locator("//div[@title='Attendees Policy']//following::img[@title='Add Row'][1]").is_enabled():
            page.locator("//div[@title='Attendees Policy']//following::img[@title='Add Row'][1]").click()
            page.wait_for_timeout(2000)
            page.locator("//div[@title='Attendees Policy']//following::select").click()
            page.locator("//div[@title='Attendees Policy']//following::select").select_option(datadictvalue["C_ATT_PLCY_NAME"])
            page.wait_for_timeout(1000)
            page.locator("//div[@title='Attendees Policy']//following::input[contains(@id,'Start')][1]").fill(datadictvalue["C_ATT_START_DATE"].strftime("%m/%d/%Y"))
            page.get_by_role("heading", name="Attendees Policy").click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_ATT_END_DATE"] != '':
                page.locator("//div[@title='Attendees Policy']//following::input[contains(@id,'End')][1]").fill(datadictvalue["C_ATT_END_DATE"].strftime("%m/%d/%Y"))

        # Preferred Agency
        page.wait_for_timeout(2000)
        if page.get_by_role("heading", name="Preferred Agency").is_visible() and page.locator("//div[@title='Preferred Agency']//following::img[@title='Add Row'][1]").is_enabled():
            page.locator("//div[@title='Preferred Agency']//following::img[@title='Add Row'][1]").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Preferred Agency List").select_option(datadictvalue["C_PRFRRD_AGNCY_LIST"])
            page.locator("//div[@title='Preferred Agency']//following::input[contains(@id,'Start')][1]").fill(datadictvalue["C_AGNCY_START_DATE"].strftime("%m/%d/%Y"))
            page.wait_for_timeout(1000)
            page.get_by_role("heading", name="Preferred Agency").click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_MRCHNT_END_DATE"] != '':
                page.locator("//div[@title='Preferred Agency']//following::input[contains(@id,'End')][1]").fill(datadictvalue["C_AGNCY_END_DATE"].strftime("%m/%d/%Y"))
            page.get_by_role("table", name="Preferred Agency").get_by_label("Policy Enforcement").click()
            page.wait_for_timeout(1000)
            page.get_by_role("table", name="Preferred Agency").get_by_label("Policy Enforcement").select_option(datadictvalue["C_AGNCY_PLCY_ENFRCMNT"])
            page.wait_for_timeout(2000)
            if datadictvalue["C_AGNCY_DSPLY_WRNNG_TO_USER"] == 'Yes' and datadictvalue[
                "C_AGNCY_PLCY_ENFRCMNT"] == 'Policy violation warning':
                page.get_by_role("table", name="Preferred Agency").locator("label").nth(4).check()
            if datadictvalue["C_AGNCY_DSPLY_WRNNG_TO_USER"] == 'No' and datadictvalue[
                "C_AGNCY_PLCY_ENFRCMNT"] == 'Policy violation warning':
                page.get_by_role("table", name="Preferred Agency").locator("label").nth(4).uncheck()

            # Preferred Merchant
            page.wait_for_timeout(2000)
            if page.get_by_role("heading", name="Preferred Merchant").is_visible() and page.locator("//div[@title='Preferred Merchant']//following::img[@title='Add Row'][1]").is_enabled():
                page.locator("//div[@title='Preferred Merchant']//following::img[@title='Add Row'][1]").click()
                page.wait_for_timeout(2000)
                page.get_by_label("Preferred Merchant List").select_option(datadictvalue["C_PRFRRD_MRCHNT_LIST"])
                page.get_by_role("table", name="Preferred Merchant").get_by_role("cell",name="Press down arrow to access Calendar Start Date Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_MRCHNT_START_DATE"].strftime("%m/%d/%Y"))
                page.get_by_role("heading", name="Preferred Merchant").click()
                page.wait_for_timeout(2000)
                if datadictvalue["C_MRCHNT_END_DATE"] != '':
                    page.get_by_role("table", name="Preferred Merchant").get_by_role("cell",name="Press down arrow to access Calendar End Date Select Date",exact=True).get_by_placeholder("m/d/yy").fill(datadictvalue["C_MRCHNT_END_DATE"].strftime("%m/%d/%Y"))
                page.get_by_role("table", name="Preferred Merchant").get_by_label("Policy Enforcement").click()
                page.wait_for_timeout(2000)
                page.get_by_role("table", name="Preferred Merchant").get_by_label("Policy Enforcement").select_option(datadictvalue["C_PLCY_ENFRCMNT"])
                page.wait_for_timeout(2000)
                if datadictvalue["C_DSPLY_WRNNG_TO_USER"] == 'Yes' and datadictvalue[
                    "C_PLCY_ENFRCMNT"] == 'Policy violation warning':
                    page.get_by_role("table", name="Preferred Merchant").locator("label").nth(4).check()
                if datadictvalue["C_DSPLY_WRNNG_TO_USER"] == 'No' and datadictvalue[
                    "C_PLCY_ENFRCMNT"] == 'Policy violation warning':
                    page.get_by_role("table", name="Preferred Merchant").locator("label").nth(4).uncheck()
                page.wait_for_timeout(5000)

        #Passenger
        # if datadictvalue["C_ENFRC_PSSNGR_NAME_TO_MATCH_NAME_ON_EXPNS_RPRT"] == 'Yes':
        #     page.get_by_label("Enforce passenger name to match name on expense report").check()
        # if datadictvalue["C_ENFRC_PSSNGR_NAME_TO_MATCH_NAME_ON_EXPNS_RPRT"] == 'No':
        #     page.get_by_label("Enforce passenger name to match name on expense report", exact=True).uncheck()

        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(4000)

        #Enable the set as default if it is required in the template level

        if datadictvalue["C_SET_AS_DFLT"] == 'Yes':
            page.get_by_text("Set as default").check()
        if datadictvalue["C_SET_AS_DFLT"] == 'No':
            page.get_by_text("Set as default").uncheck()

        #Card Expense Type mapping
        page.get_by_role("link", name="Card Expense Type Mapping").click()
        page.wait_for_timeout(1000)
        if datadictvalue["C_ENBL_CRPRT_CARD_MPPNG"] == 'Yes':
            page.get_by_text("Enable corporate card mapping").check()
            page.wait_for_timeout(2000)
            page.get_by_label("Default Expense Type").select_option(datadictvalue["C_DFLT_EXPNS_TYPE"])
            if datadictvalue["C_CARD_EXPNS_TYPE"]!= '' and datadictvalue["C_EXPNS_TYPE"] != '':
                page.get_by_role("row", name=datadictvalue["C_CARD_EXPNS_TYPE"]).get_by_label("Expense Type",exact=True).select_option(datadictvalue["C_EXPNS_TYPE"])
            if datadictvalue["C_ATMTC_ITMZTN"] == 'Yes':
                page.get_by_role("row", name=datadictvalue["C_CARD_EXPNS_TYPE"]).locator("label").nth(1).check()
                page.wait_for_timeout(2000)
                page.get_by_role("row", name=datadictvalue["C_CARD_EXPNS_TYPE"]).get_by_label("Expense Type",
                                                                                      exact=True).select_option(datadictvalue["C_DFLT_ITMZTN_EXPNS_TYPE"])
            if datadictvalue["C_ATMTC_ITMZTN"] == 'No':
                page.get_by_role("row", name=datadictvalue["C_CARD_EXPNS_TYPE"]).locator("label").nth(1).uncheck()
        if datadictvalue["C_ENBL_CRPRT_CARD_MPPNG"] == 'No':
            page.get_by_text("Enable corporate card mapping").uncheck()

        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(4000)

        #Receipt Requirement

        page.get_by_role("link", name="Receipt Requirement").click()
        if datadictvalue["C_RQR_RCPTS_FOR_CASH_EXPNS_LINES_ABOVE_SPCFD_AMNT"] == 'Yes':
            page.get_by_text("Require receipts for cash expense lines above specified amount").check()
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Require receipts for cash expense lines above specified amount']//following::input[1]").fill(str(datadictvalue["C_RCPT_CASH_AMNT"]))
        if datadictvalue["C_RQR_RCPTS_FOR_CASH_EXPNS_LINES_ABOVE_SPCFD_AMNT"] == 'No':
            page.get_by_text("Require receipts for cash expense lines above specified amount").uncheck()
        if datadictvalue["C_RQR_RCPTS_FOR_CRPRT_CARD_EXPNS_LINES_ABOVE_SPCFD_AMNT"] == 'Yes':
            page.get_by_text("Require receipts for corporate card expense lines above specified amount").check()
            page.wait_for_timeout(2000)
            page.locator("//label[text()='Require receipts for corporate card expense lines above specified amount']//following::input[1]").fill(str(datadictvalue["C_RCPT_CARD_AMNT"]))
        if datadictvalue["C_RQR_RCPTS_FOR_CRPRT_CARD_EXPNS_LINES_ABOVE_SPCFD_AMNT"] == 'No':
            page.get_by_text("Require receipts for corporate card expense lines above specified amount").uncheck()
        if datadictvalue["C_APPLY_RCPT_RQRMNT_RULES_TO_NGTV_EXPNS_LINES_1"] == 'Yes':
            page.get_by_text("Apply receipt requirement rules to negative expense lines").check()
        if datadictvalue["C_APPLY_RCPT_RQRMNT_RULES_TO_NGTV_EXPNS_LINES_1"] == 'No':
            page.get_by_text("Apply receipt requirement rules to negative expense lines").uncheck()
        if datadictvalue["C_ALLOW_USERS_TO_INDCT_THAT_RCPTS_ARE_MSSNG"] == 'Yes':
            page.get_by_text("Allow users to indicate that receipts are missing").check()
            page.wait_for_timeout(2000)
            if datadictvalue["C_DSPLY_MSSNG_RCPT_WRNNG_TO_USERS"] == 'Yes':
                page.get_by_text("Display missing receipt warning to users").check()
            if datadictvalue["C_DSPLY_MSSNG_RCPT_WRNNG_TO_USERS"] == 'No':
                page.get_by_text("Display missing receipt warning to users").uncheck()
        if datadictvalue["C_ALLOW_USERS_TO_INDCT_THAT_RCPTS_ARE_MSSNG"] == 'No':
            page.get_by_text("Allow users to indicate that receipts are missing").uncheck()

        # Expense Fields
        page.get_by_role("link", name="Expense Fields").click()
        page.get_by_label("Description").nth(1).select_option(datadictvalue["C_EXP_FLDS_DSCRPTN"])
        if page.get_by_label("Expense Location").is_visible():
            page.get_by_label("Expense Location").select_option(datadictvalue["C_EXP_FLDS_EXPNS_LCTN"])
        page.wait_for_timeout(2000)
        if page.get_by_label("Number of Days").is_visible():
            # page.get_by_label("Number of Days").click()
            page.get_by_label("Number of Days").select_option(datadictvalue["C_EXP_FLDS_NMBR_OF_DAYS"])
        if page.get_by_label("Merchant Name").is_visible():
            page.get_by_label("Merchant Name").select_option(datadictvalue["C_EXP_FLDS_MRCHNT_NAME"])

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Row Added"

        i = i + 1

        # Do the save of the last expense template before signing out
        if i == rowcount:
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            if page.get_by_role("button", name="Yes").is_visible():
                page.get_by_role("button", name="Yes").click()

        try:
            expect(page.get_by_role("button", name="Done")).to_be_visible()
            print("Expense report template Saved successfully")
            datadict[i - 1]["RowStatus"] = "Expense report template Saved successfully"
        except Exception as e:
            print("Unable to save Expense report template")
            datadict[i - 1]["RowStatus"] = "Unable to save Expense report template"

    page.wait_for_timeout(2000)
    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, EXP_TEMP):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + EXP_WORKBOOK, EXP_TEMP, PRCS_DIR_PATH + EXP_WORKBOOK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + EXP_WORKBOOK, EXP_TEMP)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,
                               VIDEO_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[0] + "_" + EXP_TEMP)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", EXP_WORKBOOK)[
            0] + "_" + EXP_TEMP + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


