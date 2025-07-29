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
    page.wait_for_timeout(40000)
    page.get_by_role("link", name="Tasks").click()

    # Entering respective option in global Search field and searching
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Elements")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Elements", exact=True).click()


    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(10000)
        if page.locator("//a[text()='View']//following::div[@role='button'][1]").is_visible():
           page.locator("//a[text()='View']//following::div[@role='button'][1]").click()
        page.get_by_role("link", name="Create").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_role("combobox", name="Legislative Data Group").click()
        page.wait_for_timeout(5000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LGSLTV_DATA_GROUP"], exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("combobox", name="Primary Classification").click()
        page.wait_for_timeout(3000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRMRY_CLSSFCTN"]).click()
        page.wait_for_timeout(2000)


        # Secondary Classification as Benefits Employer Paid
        if datadictvalue["C_SCNDRY_CLSSFCTN"]=='Benefits Employer Paid':
            page.get_by_role("combobox", name="Secondary Classification").click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_SCNDRY_CLSSFCTN"], exact=True).click()
            page.wait_for_timeout(2000)

            page.get_by_role("button", name="Continue").click()
            page.wait_for_timeout(3000)

            # Entering Basic Details
            page.get_by_label("Name", exact=True).type(datadictvalue["C_ELMNT_NAME"])
            page.get_by_label("Reporting Name").type(datadictvalue["C_RPRTNG_NAME"])
            page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])
            page.get_by_placeholder("m/d/yy").clear()
            page.get_by_placeholder("m/d/yy").type(datadictvalue["C_EFCTV_DATE"])

            # Selecting Currency
            page.get_by_role("combobox", name="Input Currency").click()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_INPUT_CRNCY"],exact=True).click()

            # Should every person eligible for the element automatically receive it?
            if datadictvalue["C_ATMTC_ELMNT_ELGBLTY"]!='N/A':
                if datadictvalue["C_ATMTC_ELMNT_ELGBLTY"] == 'Yes':
                    page.locator("// label[text() = 'Should every person eligible for the element automatically receive it?'] // following::label[text() = 'Yes'][1]").click()
                elif datadictvalue["C_ATMTC_ELMNT_ELGBLTY"] == 'No':
                    page.locator("// label[text() = 'Should every person eligible for the element automatically receive it?'] // following::label[text() = 'No'][1]").click()

            page.wait_for_timeout(2000)
            page.get_by_role("combobox", name="What is the earliest entry").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ERLST_ENTRY_DATE"]).click()
            page.get_by_role("combobox", name="What is the latest entry date").click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LTST_ENTRY_DATE"]).click()

            # Standard Rules

            ###At which employment level should this element be attached?
            if datadictvalue["C_EMPLYMNT_LEVEL_ELMNT"]!='N/A':
                if datadictvalue["C_EMPLYMNT_LEVEL_ELMNT"] == 'Assignment Level':
                    page.get_by_text("Assignment Level", exact=True).click()
                elif datadictvalue["C_EMPLYMNT_LEVEL_ELMNT"] == 'Payroll relationship level':
                    page.get_by_text("Payroll relationship level", exact=True).click()
                elif datadictvalue["C_EMPLYMNT_LEVEL_ELMNT"] == 'Term Level':
                    page.get_by_text("Term Level", exact=True).click()

            ### Does this element recur each payroll period, or does it require explicit entry?
            if datadictvalue["C_ELMNT_RCRRNG_NNRCRRNG"]!='N/A':
                if datadictvalue["C_ELMNT_RCRRNG_NNRCRRNG"] == 'Recurring':
                    page.get_by_text("Recurring", exact=True).click()
                elif datadictvalue["C_ELMNT_RCRRNG_NNRCRRNG"] == 'Nonrecurring':
                    page.get_by_text("Nonrecurring", exact=True).click()

            ### Process the element only once in each payroll period?
            if datadictvalue["C_PRCSS_ELMNT_ONLY_ONCE"] != 'N/A':
                if datadictvalue["C_PRCSS_ELMNT_ONLY_ONCE"] == 'Yes':
                    page.locator("//label[text()='Process the element only once in each payroll period?']//following::label[text()='Yes'][1]").click()
                elif datadictvalue["C_PRCSS_ELMNT_ONLY_ONCE"] == 'No':
                    page.locator("//label[text()='Process the element only once in each payroll period?']//following::label[text()='No'][1]").click()

            ### Can a person have more than one entry of this element in a payroll period?
            if datadictvalue["C_MORE_THAN_ONE_ENTRY"] != 'N/A':
                if datadictvalue["C_MORE_THAN_ONE_ENTRY"] == 'Yes':
                    page.locator("//label[text()='Can a person have more than one entry of this element in a payroll period?']//following::label[text()='Yes'][1]").click()
                elif datadictvalue["C_MORE_THAN_ONE_ENTRY"] == 'No':
                    page.locator("//label[text()='Can a person have more than one entry of this element in a payroll period?']//following::label[text()='No'][1]").click()

            # Clicking on Next button
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(3000)

            # Calculation Rules
            ### Based on Fixed amount deductions
            if datadictvalue["C_CLCLTN_RULE"] == 'Fixed amount deduction':
                page.get_by_text("Fixed amount deduction", exact=True).click()

                # Special Rules
                ### Is this element subject to proration?
                if datadictvalue["C_ELMNT_PRRTN"] != 'N/A':
                    if datadictvalue["C_ELMNT_PRRTN"] == 'No':
                        page.locator("//label[text()='Is this element subject to proration?']//following::label[text()='No'][1]").click()
                    elif datadictvalue["C_ELMNT_PRRTN"] == 'Yes':
                        page.locator("//label[text()='Is this element subject to proration?']//following::label[text()='Yes'][1]").click()
                        if datadictvalue["C_PRRTN_GROUP"] != 'N/A':
                            page.wait_for_timeout(3000)
                            page.get_by_role("combobox", name="Proration Group").click()
                            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRRTN_GROUP"]).click()

                #### Is this element subject to retroactive changes?
                if datadictvalue["C_ELMNT_RTRCTV_CHNGS"] != 'N/A':
                    if datadictvalue["C_ELMNT_RTRCTV_CHNGS"] == 'No':
                        page.locator("//label[text()='Is this element subject to retroactive changes?']//following::label[text()='No'][1]").click()
                    elif datadictvalue["C_ELMNT_RTRCTV_CHNGS"] == 'Yes':
                        page.locator("//label[text()='Is this element subject to retroactive changes?']//following::label[text()='Yes'][1]").click()
                        if datadictvalue["C_RETRO_GROUP"] != 'N/A':
                            page.wait_for_timeout(2000)
                            page.get_by_role("combobox", name="Retro Group").click()
                            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RETRO_GROUP"]).click()

                #### How do you want the element to be processed when an employee has zero earnings?
                if datadictvalue["C_PRCSSD_ZERO_ERNNGS"]!='N/A':
                    if datadictvalue["C_PRCSSD_ZERO_ERNNGS"] == 'Process the element':
                        page.locator("//label[text()='How do you want the element to be processed when an employee has zero earnings?']//following::label[text()='Process the element']").click()
                    elif datadictvalue["C_PRCSSD_ZERO_ERNNGS"] == 'Do not process the element':
                        page.locator("//label[text()='How do you want the element to be processed when an employee has zero earnings?']//following::label[text()='Do not process the element']").click()
                    elif datadictvalue["C_PRCSSD_ZERO_ERNNGS"] == 'Process the element with zero amount':
                        page.locator("//label[text()='How do you want the element to be processed when an employee has zero earnings?']//following::label[text()='Process the element with zero amount']").click()

            ### Based on Percentage deduction
            if datadictvalue["C_CLCLTN_RULE"] == 'Percentage deduction':
                page.get_by_text("Percentage deduction", exact=True).click()

                # Special Rules
                ### Is this element subject to proration?
                if datadictvalue["C_ELMNT_PRRTN"] != 'N/A':
                    if datadictvalue["C_ELMNT_PRRTN"] == 'No':
                        page.locator(
                            "//label[text()='Is this element subject to proration?']//following::label[text()='No'][1]").click()
                    elif datadictvalue["C_ELMNT_PRRTN"] == 'Yes':
                        page.locator(
                            "//label[text()='Is this element subject to proration?']//following::label[text()='Yes'][1]").click()
                        if datadictvalue["C_PRRTN_GROUP"] != 'N/A':
                            page.wait_for_timeout(3000)
                            page.get_by_role("combobox", name="Proration Group").click()
                            page.locator("[id=\"__af_Z_window\"]").get_by_text(
                                datadictvalue["C_PRRTN_GROUP"]).click()

                #### Is this element subject to retroactive changes?
                if datadictvalue["C_ELMNT_RTRCTV_CHNGS"] != 'N/A':
                    if datadictvalue["C_ELMNT_RTRCTV_CHNGS"] == 'No':
                        page.locator(
                            "//label[text()='Is this element subject to retroactive changes?']//following::label[text()='No'][1]").click()
                    elif datadictvalue["C_ELMNT_RTRCTV_CHNGS"] == 'Yes':
                        page.locator(
                            "//label[text()='Is this element subject to retroactive changes?']//following::label[text()='Yes'][1]").click()
                        if datadictvalue["C_RETRO_GROUP"] != 'N/A':
                            page.wait_for_timeout(2000)
                            page.get_by_role("combobox", name="Retro Group").click()
                            page.locator("[id=\"__af_Z_window\"]").get_by_text(
                                datadictvalue["C_RETRO_GROUP"]).click()

                #### How do you want the element to be processed when an employee has zero earnings?
                if datadictvalue["C_PRCSSD_ZERO_ERNNGS"] != 'N/A':
                    if datadictvalue["C_PRCSSD_ZERO_ERNNGS"] == 'Process the element':
                        page.locator(
                            "//label[text()='How do you want the element to be processed when an employee has zero earnings?']//following::label[text()='Process the element']").click()
                    elif datadictvalue["C_PRCSSD_ZERO_ERNNGS"] == 'Do not process the element':
                        page.locator(
                            "//label[text()='How do you want the element to be processed when an employee has zero earnings?']//following::label[text()='Do not process the element']").click()
                    elif datadictvalue["C_PRCSSD_ZERO_ERNNGS"] == 'Process the element with zero amount':
                        page.locator(
                            "//label[text()='How do you want the element to be processed when an employee has zero earnings?']//following::label[text()='Process the element with zero amount']").click()

        # Moving to Next Page
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(3000)
        # Saving the Record
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(30000)
        page.locator("//span[text()='K']").click()
        page.wait_for_timeout(20000)
        if page.locator("//span[text()='K']").is_visible():
            page.locator("//span[text()='K']").click()
            page.wait_for_timeout(10000)
        try:
            expect(page.locator("//h1[text()='Elements']")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Element Entry Created Successfully")
            datadictvalue["RowStatus"] = "Element Saved"
        except Exception as e:
            print("Unable to Create the Element Entry")
            datadictvalue["RowStatus"] = "Unable to Create the Element Entry"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + OTHER_DEDUCTIONS, EMPLOYER_LIABILITY):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + OTHER_DEDUCTIONS, EMPLOYER_LIABILITY,PRCS_DIR_PATH + OTHER_DEDUCTIONS)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + OTHER_DEDUCTIONS, EMPLOYER_LIABILITY)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", OTHER_DEDUCTIONS)[0] + "_" + EMPLOYER_LIABILITY)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", OTHER_DEDUCTIONS)[0] + "_" + EMPLOYER_LIABILITY + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))




