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

        # Secondary Classification as Regular
        if datadictvalue["C_SCNDRY_CLSSFCTN"]=='Regular':
            page.get_by_role("combobox", name="Secondary Classification").click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_SCNDRY_CLSSFCTN"], exact=True).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_CTGRY"]=='Time Card':
                page.get_by_role("combobox", name="Category").click()
                page.wait_for_timeout(3000)
                page.get_by_text(datadictvalue["C_CTGRY"], exact=True).click()
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

                # Selecting Duration
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="What is the earliest entry").click()
                page.get_by_text(datadictvalue["C_ERLST_ENTRY_DATE"]).click()
                page.get_by_role("combobox", name="What is the latest entry date").click()
                page.get_by_text(datadictvalue["C_LTST_ENTRY_DATE"]).click()

                # Selecting Process and pay element separately or with other earnings elements?
                if datadictvalue["C_PRCSS_PAY"] == 'Process and pay with other earnings':
                    page.locator("label").filter(has_text="Process and pay with other").click()

                elif datadictvalue["C_PRCSS_PAY"] == 'Process separately, but pay with other earnings':
                    page.locator("label").filter(has_text="Process separately, but pay with other earnings").click()
                else:
                    page.locator("label").filter(has_text="Process separately and pay separately").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Calculation Rules
                ### Selecting Conversion Rule as Hours
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Hours':
                    page.get_by_text("Hours").first.click()

                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"]=='Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                    if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()

                ### Selecting Conversion Rule as Other Units
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Other Units':
                    page.get_by_text("Other Units").first.click()

                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"] == 'Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                ### Selecting Conversion Rule as Hours
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Days':
                    page.get_by_text("Days").first.click()

                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(
                        datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"] == 'Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

        # Secondary Classification as Regular Not Worked
        if datadictvalue["C_SCNDRY_CLSSFCTN"]=='Regular Not Worked':
            page.get_by_role("combobox", name="Secondary Classification").click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_SCNDRY_CLSSFCTN"], exact=True).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_CTGRY"]=='Time Card':
                page.get_by_role("combobox", name="Category").click()
                page.wait_for_timeout(3000)
                page.get_by_text(datadictvalue["C_CTGRY"], exact=True).click()
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

                # Selecting Duration
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="What is the earliest entry").click()
                page.get_by_text(datadictvalue["C_ERLST_ENTRY_DATE"]).click()
                page.get_by_role("combobox", name="What is the latest entry date").click()
                page.get_by_text(datadictvalue["C_LTST_ENTRY_DATE"]).click()

                # Selecting Process and pay element separately or with other earnings elements?
                if datadictvalue["C_PRCSS_PAY"] == 'Process and pay with other earnings':
                    page.locator("label").filter(has_text="Process and pay with other").click()

                elif datadictvalue["C_PRCSS_PAY"] == 'Process separately, but pay with other earnings':
                    page.locator("label").filter(has_text="Process separately, but pay with other earnings").click()
                else:
                    page.locator("label").filter(has_text="Process separately and pay separately").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Calculation Rules
                ### Selecting Conversion Rule as Hours
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Hours':
                    page.get_by_text("Hours").first.click()

                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"]=='Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                    if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()

                ### Selecting Conversion Rule as Other Units
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Other Units':
                    page.get_by_text("Other Units").first.click()

                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"] == 'Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                ### Selecting Conversion Rule as Hours
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Days':
                    page.get_by_text("Days").first.click()

                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(
                        datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"] == 'Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

        # Secondary Classification as Overtime
        if datadictvalue["C_SCNDRY_CLSSFCTN"] == 'Overtime':
            page.get_by_role("combobox", name="Secondary Classification").click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_SCNDRY_CLSSFCTN"], exact=True).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_CTGRY"] == 'Time Card':
                page.get_by_role("combobox", name="Category").click()
                page.wait_for_timeout(3000)
                page.get_by_text(datadictvalue["C_CTGRY"], exact=True).click()
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

                # Selecting Duration
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="What is the earliest entry").click()
                page.get_by_text(datadictvalue["C_ERLST_ENTRY_DATE"]).click()
                page.get_by_role("combobox", name="What is the latest entry date").click()
                page.get_by_text(datadictvalue["C_LTST_ENTRY_DATE"]).click()

                # Selecting Process and pay element separately or with other earnings elements?
                if datadictvalue["C_PRCSS_PAY"] == 'Process and pay with other earnings':
                    page.locator("label").filter(has_text="Process and pay with other").click()

                elif datadictvalue["C_PRCSS_PAY"] == 'Process separately, but pay with other earnings':
                    page.locator("label").filter(
                        has_text="Process separately, but pay with other earnings").click()
                else:
                    page.locator("label").filter(has_text="Process separately and pay separately").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Calculation Rules
                ## Selecting Conversion Rule as Hours
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Hours':
                    page.get_by_text("Hours").first.click()

                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(
                        datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"] == 'Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                    if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()

                # Selecting Conversion Rule as Other Units
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Other Units':
                    page.get_by_text("Other Units").first.click()

                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"] == 'Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                ### Selecting Conversion Rule as Hours
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Days':
                    page.get_by_text("Days").first.click()

                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(
                        datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"] == 'Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

        # Secondary Classification as Premium
        if datadictvalue["C_SCNDRY_CLSSFCTN"]=='Premium':
            page.get_by_role("combobox", name="Secondary Classification").click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_SCNDRY_CLSSFCTN"], exact=True).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_CTGRY"]=='Time Card':
                page.get_by_role("combobox", name="Category").click()
                page.wait_for_timeout(3000)
                page.get_by_text(datadictvalue["C_CTGRY"], exact=True).click()
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

                # Selecting Duration
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="What is the earliest entry").click()
                page.get_by_text(datadictvalue["C_ERLST_ENTRY_DATE"]).click()
                page.get_by_role("combobox", name="What is the latest entry date").click()
                page.get_by_text(datadictvalue["C_LTST_ENTRY_DATE"]).click()

                # Selecting Process and pay element separately or with other earnings elements?
                if datadictvalue["C_PRCSS_PAY"] == 'Process and pay with other earnings':
                    page.locator("label").filter(has_text="Process and pay with other").click()

                elif datadictvalue["C_PRCSS_PAY"] == 'Process separately, but pay with other earnings':
                    page.locator("label").filter(has_text="Process separately, but pay with other earnings").click()
                else:
                    page.locator("label").filter(has_text="Process separately and pay separately").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Calculation Rules
                ### Selecting Conversion Rule as Hours
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Hours':
                    page.get_by_text("Hours").first.click()

                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(
                        datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"] == 'Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

        # Secondary Classification as Shift
        if datadictvalue["C_SCNDRY_CLSSFCTN"]=='Shift':
            page.get_by_role("combobox", name="Secondary Classification").click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_SCNDRY_CLSSFCTN"], exact=True).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_CTGRY"]=='Time Card':
                page.get_by_role("combobox", name="Category").click()
                page.wait_for_timeout(3000)
                page.get_by_text(datadictvalue["C_CTGRY"], exact=True).click()
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

                # Selecting Duration
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="What is the earliest entry").click()
                page.get_by_text(datadictvalue["C_ERLST_ENTRY_DATE"]).click()
                page.get_by_role("combobox", name="What is the latest entry date").click()
                page.get_by_text(datadictvalue["C_LTST_ENTRY_DATE"]).click()

                # Selecting Process and pay element separately or with other earnings elements?
                if datadictvalue["C_PRCSS_PAY"] == 'Process and pay with other earnings':
                    page.locator("label").filter(has_text="Process and pay with other").click()

                elif datadictvalue["C_PRCSS_PAY"] == 'Process separately, but pay with other earnings':
                    page.locator("label").filter(has_text="Process separately, but pay with other earnings").click()
                else:
                    page.locator("label").filter(has_text="Process separately and pay separately").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Calculation Rules
                ### Selecting Conversion Rule as Hours
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Hours':
                    page.get_by_text("Hours").first.click()

                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"]=='Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                    if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()

                ### Selecting Conversion Rule as Other Units
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Other Units':
                    page.get_by_text("Other Units").first.click()

                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"] == 'Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                ### Selecting Conversion Rule as Hours
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Days':
                    page.get_by_text("Days").first.click()

                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(
                        datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"] == 'Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()
                    if datadictvalue["C_ELMNT_HOURS_FLSA"]!='N/A':
                        if datadictvalue["C_ELMNT_HOURS_FLSA"]=='Yes':
                            page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                        else:
                            page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()

        # Secondary Classification as Tips Regular
        if datadictvalue["C_SCNDRY_CLSSFCTN"]=='Tips Regular':
            page.get_by_role("combobox", name="Secondary Classification").click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_SCNDRY_CLSSFCTN"], exact=True).click()
            page.wait_for_timeout(2000)
            if datadictvalue["C_CTGRY"]=='Time Card':
                page.get_by_role("combobox", name="Category").click()
                page.wait_for_timeout(3000)
                page.get_by_text(datadictvalue["C_CTGRY"], exact=True).click()
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

                # Selecting Duration
                page.wait_for_timeout(2000)
                page.get_by_role("combobox", name="What is the earliest entry").click()
                page.get_by_text(datadictvalue["C_ERLST_ENTRY_DATE"]).click()
                page.get_by_role("combobox", name="What is the latest entry date").click()
                page.get_by_text(datadictvalue["C_LTST_ENTRY_DATE"]).click()

                # Selecting Process and pay element separately or with other earnings elements?
                if datadictvalue["C_PRCSS_PAY"] == 'Process and pay with other earnings':
                    page.locator("label").filter(has_text="Process and pay with other").click()

                elif datadictvalue["C_PRCSS_PAY"] == 'Process separately, but pay with other earnings':
                    page.locator("label").filter(has_text="Process separately, but pay with other earnings").click()
                else:
                    page.locator("label").filter(has_text="Process separately and pay separately").click()

                ## Clicking on Next button
                page.get_by_role("button", name="Next").click()
                page.wait_for_timeout(3000)

                # Calculation Rules
                ### Selecting Conversion Rule as Hours
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Hours':
                    page.get_by_text("Hours").first.click()

                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"]=='Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                    if datadictvalue["C_ELMNT_HOURS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//following::label[text()='No'][1]").click()

                ### Selecting Conversion Rule as Other Units
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Other Units':
                    page.get_by_text("Other Units").first.click()

                    page.wait_for_timeout(3000)
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"] == 'Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

                ### Selecting Conversion Rule as Hours
                if datadictvalue["C_CLCLTN_UNITS_RPRTNG"] == 'Days':
                    page.get_by_text("Days").first.click()

                    page.wait_for_timeout(3000)
                    page.get_by_role("combobox", name="Work Units Conversion Rule").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(
                        datadictvalue["C_WORK_UNITS_CNVRSN_RULE"]).click()
                    if datadictvalue["C_ELMNT_DFULT_RATE_DFNTN"] == 'Yes':
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='Yes'][1]").click()
                        page.wait_for_timeout(3000)
                        page.get_by_role("combobox", name="Rate Name").click()
                        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_RATE_NAME"]).click()
                    else:
                        page.locator("//label[text()='Does this element have a default rate definition?']//following::label[text()='No'][1]").click()

                    # Overtime Rules
                    if datadictvalue["C_ELMNT_ERNNGS_FLSA"] == 'Yes':
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='Yes'][1]").click()
                    else:
                        page.locator("//label[text()='Should this element be included in the hours calculation of the overtime base rate?']//preceding::label[text()='No'][1]").click()

        # Moving to Next Page
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(3000)
        # Saving the Record
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(40000)
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
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_ELEMENTS_CONFIG_WRKBK, TIME_LABOUR):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PAYROLL_ELEMENTS_CONFIG_WRKBK, TIME_LABOUR,PRCS_DIR_PATH + PAYROLL_ELEMENTS_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PAYROLL_ELEMENTS_CONFIG_WRKBK, TIME_LABOUR)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PAYROLL_ELEMENTS_CONFIG_WRKBK)[0] + "_" + TIME_LABOUR)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PAYROLL_ELEMENTS_CONFIG_WRKBK)[0] + "_" + TIME_LABOUR + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

