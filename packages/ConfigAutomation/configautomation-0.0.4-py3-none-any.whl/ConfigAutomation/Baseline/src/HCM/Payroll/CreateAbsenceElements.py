from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    print(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    print(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()

    # Navigate to Setup and Maintenance
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(5000)
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


        # Secondary Classification as Vacation
        if datadictvalue["C_SCNDRY_CLSSFCTN"] == 'Vacation':
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
            page.get_by_placeholder("mm-dd-yyyy").clear()
            page.get_by_placeholder("mm-dd-yyyy").type(datadictvalue["C_EFFCTV_DATE"])

            # Selecting Currency
            page.get_by_role("combobox", name="Input Currency").click()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_INPUT_CRRNCY"],exact=True).click()

            # Selecting Absence Plan details with Hours
            if datadictvalue["C_CLCLTN_UNITS"]=='Hours':
                page.locator("//label[text() = 'What calculation units are used for reporting?']//following::label[text()='Hours']").click()
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                if datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"]=='Accrual Balances':
                    page.locator("//label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"]=='Accrual Balances and Absences':
                    page.locator("//label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances and Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"]=='Qualification Absences':
                    page.locator("//label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Qualification Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"]=='No Entitlement Absences':
                    page.locator("//label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='No Entitlement Absences']").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Absence Payments
                if datadictvalue["C_RDC_ERNNGS"]!='N/A':
                    if datadictvalue["C_RDC_ERNNGS"]=='Reduce regular earnings by absence payment':
                        page.locator("//label[text() = 'How do you want to reduce earnings for employees not requiring a time card?']//following::label[text()='Reduce regular earnings by absence payment']").click()
                    else:
                        page.locator("//label[text() = 'How do you want to reduce earnings for employees not requiring a time card?']//following::label[text()='Select rate to determine absence deduction amount']").click()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_ABSNC_DDCTN_RATE"] != 'N/A':
                        page.get_by_role("combobox",name="Rate to Determine Absence Deduction Amount").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_DDCTN_RATE"]).click()

                if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Regular':
                    page.locator("//label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Regular'][1]").click()
                    page.wait_for_timeout(3000)
                if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Supplemental':
                    page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Supplemental'][1]").click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process and pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").first.click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately, but pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").first.click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately and pay separately':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").first.click()

                if datadictvalue["C_ENBLE_ENTTLMNT_PYMNT"]== 'Yes':
                    page.locator("//label[text() = 'Does this plan enable entitlement payments after termination?']//following::label[text()='Yes'][1]").click()

                if datadictvalue["C_ABSNC_PYMNT_RATE"]!='N/A':
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Which rate should the absence payment calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_PYMNT_RATE"]).click()

                # Selecting Accrual Liability and Balance Payments
                ### Calculate Absence liability?
                if datadictvalue["C_CLCLT_ABSNC_LBLTY"]!='N/A':
                    if datadictvalue["C_CLCLT_ABSNC_LBLTY"] == 'Yes':
                        page.locator("//label[text() = 'Calculate absence liability?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                    else:
                        page.locator("//label[text() = 'Calculate absence liability?']//following::label[text()='No'][1]").click()
                    if datadictvalue["C_LBLTY_RATE"] != 'N/A':
                        page.get_by_role("combobox", name="Which rate should the liability balance calculation use?").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LBLTY_RATE"]).click()

                # Does this plan enable balance payments when enrollment ends?
                if datadictvalue["C_ENBL_BLNC_PYMNT"] != 'N/A':
                    if datadictvalue["C_ENBL_BLNC_PYMNT"]=='Yes':
                        page.locator("//label[text() = 'Does this plan enable balance payments when enrollment ends?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_FINAL_RATE"] != 'N/A':
                        page.get_by_role("combobox", name="Which rate should the final").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FINAL_RATE"]).click()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_PYT_AMNT_TAXED"]=='Regular':
                        page.locator("//label[text() = 'How do you want Payout Amount to be taxed?']//following::label[text()='Regular'][1]").click()
                    if datadictvalue["C_PYT_AMNT_TAXED"] == 'Supplemental':
                        page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Supplemental'][1]").click()
                        page.wait_for_timeout(3000)
                        if datadictvalue["C_AMNT_TAXED_PYMNT_PRCSS_MODE"] == 'Process and pay with other earnings':
                            page.locator("// label[text() = 'Absence Payout Process Mode']//following::label[text()='Process and pay with other earnings']").first.click()
                        elif datadictvalue["C_AMNT_TAXED_PYMNT_PRCSS_MODE"] == 'Process separately, but pay with other earnings':
                            page.locator("// label[text() = 'Absence Payout Process Mode']//following::label[text()='Process separately, but pay with other earnings']").first.click()
                        elif datadictvalue["C_AMNT_TAXED_PYMNT_PRCSS_MODE"] == 'Process separately and pay separately':
                            page.locator("// label[text() = 'Absence Payout Process Mode']//following::label[text()='Process separately and pay separately']").first.click()

                #Does this plan enable partial payment of balance?
                if datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"]=='Yes':
                    page.locator("//label[text() = 'Does this plan enable partial payment of balance?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox",name="Which rate should the discretionary disbursement calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"]).click()

                # How do you want Cash out amount to be taxed?
                if datadictvalue["C_CASH_OUT_AMNT_TAXED"]!='N/A':
                    if datadictvalue["C_CASH_OUT_AMNT_TAXED"]=='Regular':
                        page.locator("//label[text() = 'How do you want Cash out amount to be taxed?']//following::label[text()='Regular'][1]").click()

                # OverTime Rules
                if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()
            # Selecting Absence Plan details with Days
            if datadictvalue["C_CLCLTN_UNITS"] == 'Days':
                page.locator("// label[text() = 'What calculation units are used for reporting?']//following::label[text()='Days']").click()
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                if datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Accrual Balances':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Accrual Balances and Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances and Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Qualification Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Qualification Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'No Entitlement Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='No Entitlement Absences']").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Absence Payments
                if datadictvalue["C_RDC_ERNNGS"]!='N/A':
                    if datadictvalue["C_RDC_ERNNGS"]=='Reduce regular earnings by absence payment':
                        page.locator("//label[text() = 'How do you want to reduce earnings for employees not requiring a time card?']//following::label[text()='Reduce regular earnings by absence payment']").click()
                    else:
                        page.locator("//label[text() = 'How do you want to reduce earnings for employees not requiring a time card?']//following::label[text()='Select rate to determine absence deduction amount']").click()

                if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Regular':
                    page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Regular'][1]").click()
                    page.wait_for_timeout(3000)
                if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Supplemental':
                    page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Supplemental'][1]").click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"]=='Process and pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").first.click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"]=='Process separately, but pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").first.click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"]=='Process separately and pay separately':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").first.click()
                if datadictvalue["C_ENBLE_ENTTLMNT_PYMNT"] == 'Yes':
                    page.locator("// label[text() = 'Does this plan enable entitlement payments after termination?']//following::label[text()='Yes'][1]").click()

                # Selecting Accrual Liability and Balance Payments
                ### Calculate Absence liability?
                if datadictvalue["C_CLCLT_ABSNC_LBLTY"] == 'Yes':
                    page.locator("// label[text() = 'Calculate absence liability?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox",name="Which rate should the liability balance calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LBLTY_RATE"]).click()
                else:
                    page.locator("//label[text() = 'Calculate absence liability?']//following::label[text()='No'][1]").click()
                # Does this plan enable balance payments when enrollment ends?
                if datadictvalue["C_ENBL_BLNC_PYMNT"] == 'Yes':
                    page.locator("// label[text() = 'Does this plan enable balance payments when enrollment ends?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Which rate should the final").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FINAL_RATE"]).click()
                    page.wait_for_timeout(3000)

                if datadictvalue["C_PYT_AMNT_TAXED"] == 'Regular':
                    page.locator("//label[text() = 'How do you want Payout Amount to be taxed?']//following::label[text()='Regular'][1]").click()
                if datadictvalue["C_PYT_AMNT_TAXED"] == 'Supplemental':
                    page.locator("// label[text() = 'How do you want Payout Amount to be taxed?']//following::label[text()='Supplemental'][1]").click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"]=='Process and pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").first.click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"]=='Process separately, but pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").first.click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"]=='Process separately and pay separately':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").first.click()

                # Does this plan enable partial payment of balance?
                if datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"] == 'Yes':
                    page.locator("//label[text() = 'Does this plan enable partial payment of balance?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.locator("//label[text()='Which rate should the absence payment calculation use?']//following::input[1]").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"]).click()

                # How do you want Cash out amount to be taxed?
                if datadictvalue["C_CASH_OUT_AMNT_TAXED"]!='N/A':
                    if datadictvalue["C_CASH_OUT_AMNT_TAXED"] == 'Regular':
                        page.locator("//label[text() = 'How do you want Cash out amount to be taxed?']//following::label[text()='Regular'][1]").click()
                    if datadictvalue["C_CASH_OUT_AMNT_TAXED"] == 'Supplemental':
                        page.locator("// label[text() = 'How do you want Cash out amount to be taxed?']//following::label[text()='Supplemental'][1]").click()
                        page.wait_for_timeout(5000)
                        if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process and pay with other earnings':
                            page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").nth(2).click()
                        elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately, but pay with other earnings':
                            page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").nth(2).click()
                        elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately and pay separately':
                            page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").nth(2).click()

                # OverTime Rules
                if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                if datadictvalue["C_ELMNT_HOURS_FLSA"]!='N/A':
                    if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()

        # Secondary Classification as Sickness
        if datadictvalue["C_SCNDRY_CLSSFCTN"] == 'Sickness':
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
            page.get_by_placeholder("mm-dd-yyyy").clear()
            page.get_by_placeholder("mm-dd-yyyy").type(datadictvalue["C_EFFCTV_DATE"])

            # Selecting Currency
            page.get_by_role("combobox", name="Input Currency").click()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_INPUT_CRRNCY"],exact=True).click()

            # Selecting Absence Plan details
            if datadictvalue["C_CLCLTN_UNITS"]=='Hours':
                page.locator("//label[text() = 'What calculation units are used for reporting?']//following::label[text()='Hours']").click()
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                if datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"]=='Accrual Balances':
                    page.locator("//label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"]=='Accrual Balances and Absences':
                    page.locator("//label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances and Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"]=='Qualification Absences':
                    page.locator("//label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Qualification Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"]=='No Entitlement Absences':
                    page.locator("//label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='No Entitlement Absences']").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Absence Payments
                if datadictvalue["C_RDC_ERNNGS"]!='N/A':
                    if datadictvalue["C_RDC_ERNNGS"]=='Reduce regular earnings by absence payment':
                        page.locator("//label[text() = 'How do you want to reduce earnings for employees not requiring a time card?']//following::label[text()='Reduce regular earnings by absence payment']").click()
                    else:
                        page.locator("//label[text() = 'How do you want to reduce earnings for employees not requiring a time card?']//following::label[text()='Select rate to determine absence deduction amount']").click()

                if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Regular':
                    page.locator("//label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Regular'][1]").click()
                    page.wait_for_timeout(3000)
                if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Supplemental':
                    page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Supplemental'][1]").click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process and pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").first.click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately, but pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").first.click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately and pay separately':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").first.click()

                if datadictvalue["C_ENBLE_ENTTLMNT_PYMNT"] == 'Yes':
                    page.locator("//label[text() = 'Does this plan enable entitlement payments after termination?']//following::label[text()='Yes'][1]").click()

                if datadictvalue["C_ABSNC_PYMNT_RATE"]!='N/A':
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Which rate should the absence payment calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_PYMNT_RATE"]).click()

                # Selecting Accrual Liability and Balance Payments
                ### Calculate Absence liability?
                if datadictvalue["C_CLCLT_ABSNC_LBLTY"] == 'Yes':
                    page.locator("//label[text() = 'Calculate absence liability?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Which rate should the liability balance calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LBLTY_RATE"]).click()
                else:
                    page.locator("//label[text() = 'Calculate absence liability?']//following::label[text()='No'][1]").click()
                # Does this plan enable balance payments when enrollment ends?
                if datadictvalue["C_ENBL_BLNC_PYMNT"]=='Yes':
                    page.locator("//label[text() = 'Does this plan enable balance payments when enrollment ends?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Which rate should the final").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FINAL_RATE"]).click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_PYT_AMNT_TAXED"]=='Regular':
                        page.locator("//label[text() = 'How do you want Payout Amount to be taxed?']//following::label[text()='Regular'][1]").click()
                #Does this plan enable partial payment of balance?
                if datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"]=='Yes':
                    page.locator("//label[text() = 'Does this plan enable partial payment of balance?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox",name="Which rate should the discretionary disbursement calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"]).click()

                # How do you want Cash out amount to be taxed?
                if datadictvalue["C_CASH_OUT_AMNT_TAXED"]=='Regular':
                    page.locator("//label[text() = 'How do you want Cash out amount to be taxed?']//following::label[text()='Regular'][1]").click()

                # OverTime Rules
                if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()
            # Selecting Absence Plan details with Days
            if datadictvalue["C_CLCLTN_UNITS"] == 'Days':
                page.locator("// label[text() = 'What calculation units are used for reporting?']//following::label[text()='Days']").click()
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                if datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Accrual Balances':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Accrual Balances and Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances and Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Qualification Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Qualification Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'No Entitlement Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='No Entitlement Absences']").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Absence Payments
                if datadictvalue["C_RDC_ERNNGS"] == 'Reduce regular earnings by absence payment':
                    page.locator("//label[text() = 'How do you want to reduce earnings for employees not requiring a time card?']//following::label[text()='Reduce regular earnings by absence payment']").click()
                else:
                    page.locator("//label[text() = 'How do you want to reduce earnings for employees not requiring a time card?']//following::label[text()='Select rate to determine absence deduction amount']").click()

                if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Regular':
                    page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Regular'][1]").click()
                    page.wait_for_timeout(3000)
                if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Supplemental':
                    page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Supplemental'][1]").click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process and pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").first.click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately, but pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").first.click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately and pay separately':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").first.click()
                if datadictvalue["C_ENBLE_ENTTLMNT_PYMNT"] == 'Yes':
                    page.locator("// label[text() = 'Does this plan enable entitlement payments after termination?']//following::label[text()='Yes'][1]").click()

                # Selecting Accrual Liability and Balance Payments
                ### Calculate Absence liability?
                if datadictvalue["C_CLCLT_ABSNC_LBLTY"] == 'Yes':
                    page.locator("// label[text() = 'Calculate absence liability?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox",name="Which rate should the liability balance calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LBLTY_RATE"]).click()
                else:
                    page.locator("//label[text() = 'Calculate absence liability?']//following::label[text()='No'][1]").click()
                # Does this plan enable balance payments when enrollment ends?
                if datadictvalue["C_ENBL_BLNC_PYMNT"] == 'Yes':
                    page.locator("// label[text() = 'Does this plan enable balance payments when enrollment ends?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Which rate should the final").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FINAL_RATE"]).click()
                    page.wait_for_timeout(3000)

                if datadictvalue["C_PYT_AMNT_TAXED"] == 'Regular':
                    page.locator("//label[text() = 'How do you want Payout Amount to be taxed?']//following::label[text()='Regular'][1]").click()
                if datadictvalue["C_PYT_AMNT_TAXED"] == 'Supplemental':
                    page.locator("// label[text() = 'How do you want Payout Amount to be taxed?']//following::label[text()='Supplemental'][1]").click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process and pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").nth(1).click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately, but pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").nth(1).click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately and pay separately':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").nth(1).click()

                # Does this plan enable partial payment of balance?
                if datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"] == 'Yes':
                    page.locator("//label[text() = 'Does this plan enable partial payment of balance?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox",name="Which rate should the discretionary disbursement calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"]).click()

                # How do you want Cash out amount to be taxed?
                if datadictvalue["C_CASH_OUT_AMNT_TAXED"] != 'N/A':
                    if datadictvalue["C_CASH_OUT_AMNT_TAXED"] == 'Regular':
                        page.locator("//label[text() = 'How do you want Cash out amount to be taxed?']//following::label[text()='Regular'][1]").click()
                    if datadictvalue["C_CASH_OUT_AMNT_TAXED"] == 'Supplemental':
                        page.locator("// label[text() = 'How do you want Cash out amount to be taxed?']//following::label[text()='Supplemental'][1]").click()
                        page.wait_for_timeout(3000)
                        if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process and pay with other earnings':
                            page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").nth(2).click()
                        elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately, but pay with other earnings':
                            page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").nth(2).click()
                        elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately and pay separately':
                            page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").nth(2).click()

                # OverTime Rules
                if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()

        # Secondary Classification as Other
        if datadictvalue["C_SCNDRY_CLSSFCTN"] == 'Other':
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
            page.get_by_placeholder("mm-dd-yyyy").clear()
            page.get_by_placeholder("mm-dd-yyyy").type(datadictvalue["C_EFFCTV_DATE"])

            # Selecting Currency
            page.get_by_role("combobox", name="Input Currency").click()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_INPUT_CRRNCY"],exact=True).click()

            # Selecting Absence Plan details
            if datadictvalue["C_CLCLTN_UNITS"] == 'Hours':
                page.locator("// label[text() = 'What calculation units are used for reporting?']//following::label[text()='Hours']").click()
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                if datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Accrual Balances':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Accrual Balances and Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances and Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Qualification Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Qualification Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'No Entitlement Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='No Entitlement Absences']").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Absence Payments
                if datadictvalue["C_RDC_ERNNGS"] == 'Reduce regular earnings by absence payment':
                    page.locator("//label[text() = 'How do you want to reduce earnings for employees not requiring a time card?']//following::label[text()='Reduce regular earnings by absence payment']").click()
                else:
                    page.locator("//label[text() = 'How do you want to reduce earnings for employees not requiring a time card?']//following::label[text()='Select rate to determine absence deduction amount']").click()
                    page.wait_for_timeout(3000)
                if datadictvalue["C_ABSNC_DDCTN_RATE"] != 'N/A':
                    page.get_by_role("combobox",name="Rate to Determine Absence Deduction Amount").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_DDCTN_RATE"]).click()

                if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Regular':
                    page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Regular'][1]").click()
                    page.wait_for_timeout(3000)

                if datadictvalue["C_ENBLE_ENTTLMNT_PYMNT"] == 'Yes':
                    page.locator("// label[text() = 'Does this plan enable entitlement payments after termination?']//following::label[text()='Yes'][1]").click()

                if datadictvalue["C_ABSNC_PYMNT_RATE"]!='N/A':
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Which rate should the absence payment calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_PYMNT_RATE"]).click()


                # Selecting Accrual Liability and Balance Payments
                ### Calculate Absence liability?
                if datadictvalue["C_CLCLT_ABSNC_LBLTY"]!='N/A':
                    if datadictvalue["C_CLCLT_ABSNC_LBLTY"] == 'Yes':
                        page.locator("// label[text() = 'Calculate absence liability?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox",name="Which rate should the liability balance calculation use?").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LBLTY_RATE"]).click()
                    else:
                        page.locator("//label[text() = 'Calculate absence liability?']//following::label[text()='No'][1]").click()
                # Does this plan enable balance payments when enrollment ends?
                if datadictvalue["C_ENBL_BLNC_PYMNT"] == 'Yes':
                    page.locator("// label[text() = 'Does this plan enable balance payments when enrollment ends?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Which rate should the final").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FINAL_RATE"]).click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_PYT_AMNT_TAXED"] == 'Regular':
                        page.locator("//label[text() = 'How do you want Payout Amount to be taxed?']//following::label[text()='Regular'][1]").click()
                # Does this plan enable partial payment of balance?
                if datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"] == 'Yes':
                    page.locator("//label[text() = 'Does this plan enable partial payment of balance?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox",
                                     name="Which rate should the discretionary disbursement calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"]).click()

                # How do you want Cash out amount to be taxed?
                if datadictvalue["C_CASH_OUT_AMNT_TAXED"] == 'Regular':
                    page.locator("//label[text() = 'How do you want Cash out amount to be taxed?']//following::label[text()='Regular'][1]").click()

                # OverTime Rules
                if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()
            # Selecting Absence Plan details with Days
            if datadictvalue["C_CLCLTN_UNITS"] == 'Days':
                        page.locator("// label[text() = 'What calculation units are used for reporting?']//following::label[text()='Days']").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(
                            datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                        if datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Accrual Balances':
                            page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances']").click()
                        elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Accrual Balances and Absences':
                            page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances and Absences']").click()
                        elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Qualification Absences':
                            page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Qualification Absences']").click()
                        elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'No Entitlement Absences':
                            page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='No Entitlement Absences']").click()

                        ## Clicking on Next button
                        page.get_by_role("button", name="Next").click()
                        page.wait_for_timeout(3000)

                        # Absence Payments
                        if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Regular':
                            page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Regular'][1]").click()
                            page.wait_for_timeout(3000)
                        if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Supplemental':
                            page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Supplemental'][1]").click()
                            page.wait_for_timeout(3000)
                            if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process and pay with other earnings':
                                page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").first.click()
                            elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately, but pay with other earnings':
                                page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").first.click()
                            elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately and pay separately':
                                page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").first.click()
                        if datadictvalue["C_ENBLE_ENTTLMNT_PYMNT"] == 'Yes':
                            page.locator("// label[text() = 'Does this plan enable entitlement payments after termination?']//following::label[text()='Yes'][1]").click()

                        # Selecting Accrual Liability and Balance Payments
                        ### Calculate Absence liability?
                        if datadictvalue["C_CLCLT_ABSNC_LBLTY"] == 'Yes':
                            page.locator("// label[text() = 'Calculate absence liability?']//following::label[text()='Yes'][1]").click()
                            page.wait_for_timeout(3000)
                            page.get_by_role("combobox",name="Which rate should the liability balance calculation use?").click()
                            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LBLTY_RATE"]).click()
                        else:
                            page.locator("//label[text() = 'Calculate absence liability?']//following::label[text()='No'][1]").click()
                        # Does this plan enable balance payments when enrollment ends?
                        if datadictvalue["C_ENBL_BLNC_PYMNT"] == 'Yes':
                            page.locator("// label[text() = 'Does this plan enable balance payments when enrollment ends?']//following::label[text()='Yes'][1]").click()
                            page.wait_for_timeout(3000)
                            page.get_by_role("combobox", name="Which rate should the final").click()
                            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FINAL_RATE"]).click()
                            page.wait_for_timeout(3000)

                        if datadictvalue["C_PYT_AMNT_TAXED"] == 'Regular':
                            page.locator("//label[text() = 'How do you want Payout Amount to be taxed?']//following::label[text()='Regular'][1]").click()
                        if datadictvalue["C_PYT_AMNT_TAXED"] == 'Supplemental':
                            page.locator("// label[text() = 'How do you want Payout Amount to be taxed?']//following::label[text()='Supplemental'][1]").click()
                            page.wait_for_timeout(3000)
                            if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process and pay with other earnings':
                                page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").nth(1).click()
                            elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately, but pay with other earnings':
                                page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").nth(1).click()
                            elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately and pay separately':
                                page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").nth(1).click()

                        # Does this plan enable partial payment of balance?
                        if datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"] == 'Yes':
                            page.locator("//label[text() = 'Does this plan enable partial payment of balance?']//following::label[text()='Yes'][1]").click()
                            page.wait_for_timeout(3000)
                            page.get_by_role("combobox",name="Which rate should the discretionary disbursement calculation use?").click()
                            page.locator("[id=\"__af_Z_window\"]").get_by_text(
                                datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"]).click()

                        # How do you want Cash out amount to be taxed?
                        if datadictvalue["C_CASH_OUT_AMNT_TAXED"] != 'N/A':
                            if datadictvalue["C_CASH_OUT_AMNT_TAXED"] == 'Regular':
                                page.locator("//label[text() = 'How do you want Cash out amount to be taxed?']//following::label[text()='Regular'][1]").click()
                            if datadictvalue["C_CASH_OUT_AMNT_TAXED"] == 'Supplemental':
                                page.locator("// label[text() = 'How do you want Cash out amount to be taxed?']//following::label[text()='Supplemental'][1]").click()
                                page.wait_for_timeout(3000)
                                if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process and pay with other earnings':
                                    page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").nth(2).click()
                                elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately, but pay with other earnings':
                                    page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").nth(2).click()
                                elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately and pay separately':
                                    page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").nth(2).click()

                        # OverTime Rules
                        if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                            page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                        else:
                            page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                        if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                            page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                        else:
                            page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()

        # Secondary Classification as Maternity
        if datadictvalue["C_SCNDRY_CLSSFCTN"] == 'Maternity':
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
            page.get_by_placeholder("mm-dd-yyyy").clear()
            page.get_by_placeholder("mm-dd-yyyy").type(datadictvalue["C_EFFCTV_DATE"])

            # Selecting Currency
            page.get_by_role("combobox", name="Input Currency").click()
            page.wait_for_timeout(2000)
            page.get_by_text(datadictvalue["C_INPUT_CRRNCY"],exact=True).click()

            # Selecting Absence Plan details
            if datadictvalue["C_CLCLTN_UNITS"] == 'Hours':
                page.locator("// label[text() = 'What calculation units are used for reporting?']//following::label[text()='Hours']").click()
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                if datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Accrual Balances':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Accrual Balances and Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances and Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Qualification Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Qualification Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'No Entitlement Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='No Entitlement Absences']").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Absence Payments
                if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Regular':
                    page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Regular'][1]").click()
                    page.wait_for_timeout(3000)

                if datadictvalue["C_ENBLE_ENTTLMNT_PYMNT"] == 'Yes':
                    page.locator("// label[text() = 'Does this plan enable entitlement payments after termination?']//following::label[text()='Yes'][1]").click()

                if datadictvalue["C_ABSNC_PYMNT_RATE"]!='N/A':
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Which rate should the absence payment calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ABSNC_PYMNT_RATE"]).click()


                # Selecting Accrual Liability and Balance Payments
                ### Calculate Absence liability?
                if datadictvalue["C_CLCLT_ABSNC_LBLTY"]!='N/A':
                    if datadictvalue["C_CLCLT_ABSNC_LBLTY"] == 'Yes':
                        page.locator("// label[text() = 'Calculate absence liability?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox",name="Which rate should the liability balance calculation use?").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LBLTY_RATE"]).click()
                    else:
                        page.locator("//label[text() = 'Calculate absence liability?']//following::label[text()='No'][1]").click()
                # Does this plan enable balance payments when enrollment ends?
                if datadictvalue["C_ENBL_BLNC_PYMNT"] == 'Yes':
                    page.locator("// label[text() = 'Does this plan enable balance payments when enrollment ends?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Which rate should the final").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FINAL_RATE"]).click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_PYT_AMNT_TAXED"] == 'Regular':
                        page.locator("//label[text() = 'How do you want Payout Amount to be taxed?']//following::label[text()='Regular'][1]").click()
                # Does this plan enable partial payment of balance?
                if datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"] == 'Yes':
                    page.locator("//label[text() = 'Does this plan enable partial payment of balance?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox",
                                     name="Which rate should the discretionary disbursement calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"]).click()

                # How do you want Cash out amount to be taxed?
                if datadictvalue["C_CASH_OUT_AMNT_TAXED"] == 'Regular':
                    page.locator("//label[text() = 'How do you want Cash out amount to be taxed?']//following::label[text()='Regular'][1]").click()

                # OverTime Rules
                if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()

            if datadictvalue["C_CLCLTN_UNITS"] == 'Days':
                page.locator("// label[text() = 'What calculation units are used for reporting?']//following::label[text()='Days']").click()
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                if datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Accrual Balances':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Accrual Balances and Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Accrual Balances and Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'Qualification Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='Qualification Absences']").click()
                elif datadictvalue["C_TYPE_OF_ABSNC_INFRMTN"] == 'No Entitlement Absences':
                    page.locator("// label[text() = 'What type of absence information do you want transferred to payroll?']//following::label[text()='No Entitlement Absences']").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Absence Payments
                if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Regular':
                    page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Regular'][1]").click()
                    page.wait_for_timeout(3000)
                if datadictvalue["C_ABSNC_PYMNT_TAXED"] == 'Supplemental':
                    page.locator("// label[text() = 'How do you want Absence Payment to be taxed?']//following::label[text()='Supplemental'][1]").click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"]=='Process and pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").first.click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"]=='Process separately, but pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").first.click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"]=='Process separately and pay separately':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").first.click()
                if datadictvalue["C_ENBLE_ENTTLMNT_PYMNT"] == 'Yes':
                    page.locator("// label[text() = 'Does this plan enable entitlement payments after termination?']//following::label[text()='Yes'][1]").first.click()

                # Selecting Accrual Liability and Balance Payments
                ### Calculate Absence liability?
                if datadictvalue["C_CLCLT_ABSNC_LBLTY"] == 'Yes':
                    page.locator("// label[text() = 'Calculate absence liability?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox",name="Which rate should the liability balance calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LBLTY_RATE"]).click()
                else:
                    page.locator("//label[text() = 'Calculate absence liability?']//following::label[text()='No'][1]").click()
                # Does this plan enable balance payments when enrollment ends?
                if datadictvalue["C_ENBL_BLNC_PYMNT"] == 'Yes':
                    page.locator("// label[text() = 'Does this plan enable balance payments when enrollment ends?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Which rate should the final").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_FINAL_RATE"]).click()
                    page.wait_for_timeout(3000)

                if datadictvalue["C_PYT_AMNT_TAXED"] == 'Regular':
                    page.locator("//label[text() = 'How do you want Payout Amount to be taxed?']//following::label[text()='Regular'][1]").click()
                if datadictvalue["C_PYT_AMNT_TAXED"] == 'Supplemental':
                    page.locator("// label[text() = 'How do you want Payout Amount to be taxed?']//following::label[text()='Supplemental'][1]").click()
                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"]=='Process and pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").nth(1).click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"]=='Process separately, but pay with other earnings':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").nth(1).click()
                    elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"]=='Process separately and pay separately':
                        page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").nth(1).click()

                # Does this plan enable partial payment of balance?
                if datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"] == 'Yes':
                    page.locator("//label[text() = 'Does this plan enable partial payment of balance?']//following::label[text()='Yes'][1]").click()
                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox",name="Which rate should the discretionary disbursement calculation use?").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DSCRTNRY_DSBRSMNT_RATE"]).click()

                # How do you want Cash out amount to be taxed?
                if datadictvalue["C_CASH_OUT_AMNT_TAXED"]!='N/A':
                    if datadictvalue["C_CASH_OUT_AMNT_TAXED"] == 'Regular':
                        page.locator("//label[text() = 'How do you want Cash out amount to be taxed?']//following::label[text()='Regular'][1]").click()
                    if datadictvalue["C_CASH_OUT_AMNT_TAXED"] == 'Supplemental':
                        page.locator("// label[text() = 'How do you want Cash out amount to be taxed?']//following::label[text()='Supplemental'][1]").click()
                        page.wait_for_timeout(3000)
                        if datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process and pay with other earnings':
                            page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process and pay with other earnings']").nth(2).click()
                        elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately, but pay with other earnings':
                            page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately, but pay with other earnings']").nth(2).click()
                        elif datadictvalue["C_ABSNC_PYMNT_PRCSS_MODE"] == 'Process separately and pay separately':
                            page.locator("// label[text() = 'Absence Payment Process Mode']//following::label[text()='Process separately and pay separately']").nth(2).click()

                # OverTime Rules
                if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                else:
                    page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()

        # Moving to Next Page
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(3000)
        # Saving the Record
        page.get_by_role("button", name="Submit").click()
        page.locator("//span[text()='K']").click()
        page.wait_for_timeout(30000)
        #page.locator("//span[text()='K']").click()
        #page.wait_for_timeout(20000)
        if page.locator("//span[text()='K']").is_visible():
            page.locator("//span[text()='K']").click()
            page.wait_for_timeout(5000)

        try:
            expect(page.locator("//h1[text()='Elements']")).to_be_visible()
            #page.wait_for_timeout(4000)
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
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_ELEMENTS_CONFIG_WRKBK, ABSENCE_ELEMENTS):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_ELEMENTS_CONFIG_WRKBK, ABSENCE_ELEMENTS,PRCS_DIR_PATH + PAYROLL_ELEMENTS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_ELEMENTS_CONFIG_WRKBK, ABSENCE_ELEMENTS)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_ELEMENTS_CONFIG_WRKBK)[0] + "_" + ABSENCE_ELEMENTS)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_ELEMENTS_CONFIG_WRKBK)[0] + "_" + ABSENCE_ELEMENTS + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

