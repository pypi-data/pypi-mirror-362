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
    page.wait_for_timeout(3000)
    page.locator("//a[@title=\"Settings and Actions\"]").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.wait_for_timeout(20000)
    page.get_by_role("link", name="Tasks").click()
    page.locator("[id=\"__af_Z_window\"]").get_by_role("link", name="Search").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").type("Time Entry Layout Components")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Time Entry Layout Components", exact=True).click()
    page.wait_for_timeout(2000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        # Create
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(2000)

        # Selecting Multiple attribute time card field
        page.locator("[id=\"__af_Z_window\"]").get_by_text("Multiple attribute time card field").click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # Name
        page.get_by_label("Name", exact=True).clear()
        page.get_by_label("Name", exact=True).fill(datadictvalue["C_NAME"])

        # Description
        page.get_by_label("Description").clear()
        page.get_by_label("Description").fill(datadictvalue["C_DSCRPTN"])

        # Add Time Attribute - Attribute Display Sequence
        if datadictvalue["C_ATTRBT_DSPLY_SQNC"] != '':
            page.get_by_role("button", name="Add Time Attribute").click()
            page.get_by_label("Attribute Display Sequence").click()
            page.get_by_label("Attribute Display Sequence").fill(str(datadictvalue["C_ATTRBT_DSPLY_SQNC"]))
            page.wait_for_timeout(3000)

            # Time Attribute
            if datadictvalue["C_ATTRBT_TIME_ATTRBT"] != '':
                page.get_by_label("Time Attribute").click()
                page.get_by_label("Time Attribute").fill(datadictvalue["C_ATTRBT_TIME_ATTRBT"])
                page.wait_for_timeout(3000)

            # Unfiltered Data Source for Setup Tasks
            if datadictvalue["C_ATTRBT_UNFLTRD_DATA_SRC"] != '':
                page.get_by_label("Unfiltered Data Source for Setup Tasks").click()
                page.get_by_title("Search: Unfiltered Data Source for Setup Tasks").click()
                page.get_by_text(datadictvalue["C_ATTRBT_UNFLTRD_DATA_SRC"]).click()
                page.wait_for_timeout(3000)

            # Filtered Data Source for Time Entry
            if datadictvalue["C_ATTRBT_FLTRD_DATA_SRC"] != '':
                page.get_by_label("Filtered Data Source for Time Entry").click()
                page.get_by_label("Filtered Data Source for Time Entry").fill(datadictvalue["C_ATTRBT_FLTRD_DATA_SRC"])
                page.get_by_label("Filtered Data Source for Time Entry").press("Tab")
                page.wait_for_timeout(3000)

            # Required for attribute definition structure
            if datadictvalue["C_ATTRBT_RQRD_ATTRBT_STRCTR"] == "No":
                page.get_by_text("Required for attribute definition structure").uncheck()
                page.wait_for_timeout(3000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # C_DSPLY_SEQ_1
        # Display Value
        if (str(datadictvalue["C_DSPLY_SEQ_1"])) == "1":
            page.get_by_role("cell", name="1 Display Value").get_by_label("Display Value").click()
            page.get_by_role("cell", name="1 Display Value").get_by_label("Display Value").fill(datadictvalue["C_DSPLY_VAL_1"])
            page.wait_for_timeout(3000)
        # Absence Management Type
        if datadictvalue["C_ABS_MGMT_TYPE_1"] != "N/A":
            page.get_by_role("cell", name="1 Display Value").get_by_label("Absence Management Type").click()
            page.get_by_role("cell", name="1 Display Value").get_by_label("Absence Management Type").fill(datadictvalue["C_ABS_MGMT_TYPE_1"])
            page.wait_for_timeout(3000)
        # Payroll Time Types
        if datadictvalue["C_PYRL_TIME_TYPE_1"] != "N/A":
            page.get_by_role("cell", name="1 Display Value").get_by_label("Payroll Time Type").click()
            page.get_by_role("cell", name="1 Display Value").get_by_label("Payroll Time Type").fill(datadictvalue["C_PYRL_TIME_TYPE_1"])
            # page.get_by_role("cell", name="1 Display Value").get_by_label("Payroll Time Type").press("Tab")
            page.wait_for_timeout(8000)
        # Enable Cost Override for Payroll Time Type
        if datadictvalue["C_COST_OVRRD_1"] == "Yes":
            page.wait_for_timeout(6000)
            # expect(page.get_by_label("Enable Cost Override for Payroll Time Type")).to_be_checked()
            page.get_by_text("Enable Cost Override for Payroll Time Type").check()
            page.wait_for_timeout(3000)
        # Enabled
        if datadictvalue["C_ENABLE_1"] == "No":
            page.get_by_role("cell", name="1 Display Value").locator("label").nth(1).uncheck()
            # page.get_by_text("Enabled").uncheck()
            page.wait_for_timeout(3000)
        # Worker Allowed Action
        if datadictvalue["C_WRK_ALWD_ACT_1"] != '':
            page.get_by_role("combobox", name="Worker Allowed Action").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WRK_ALWD_ACT_1"]).click()
            page.wait_for_timeout(3000)
        # Line Manager Allowed Action
        if datadictvalue["C_LIN_MGR_ALWD_ACT_1"] != '':
            page.get_by_role("combobox", name="Line Manager Allowed Action").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LIN_MGR_ALWD_ACT_1"]).click()
            page.wait_for_timeout(3000)
        # Time and Labor Manager Allowed Action
        if datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_1"] != '':
            page.get_by_role("combobox", name="Time and Labor Manager Allowed Action").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_1"]).click()
            page.wait_for_timeout(3000)

        # C_DSPLY_SEQ_2
        # Display Value
        if (str(datadictvalue["C_DSPLY_SEQ_2"])) == "2":
            page.get_by_role("button", name="Add Row Below").click()
            page.wait_for_timeout(5000)
            page.get_by_role("cell", name="2 Display Value").get_by_label("Display Value").click()
            page.get_by_role("cell", name="2 Display Value").get_by_label("Display Value").fill(datadictvalue["C_DSPLY_VAL_2"])
            page.wait_for_timeout(3000)
        # Absence Management Type
        if datadictvalue["C_ABS_MGMT_TYPE_2"] != "N/A":
            page.get_by_role("cell", name="2 Display Value").get_by_label("Absence Management Type").click()
            page.get_by_role("cell", name="2 Display Value").get_by_label("Absence Management Type").fill(datadictvalue["C_ABS_MGMT_TYPE_2"])
            page.wait_for_timeout(3000)
        # Payroll Time Type
        if datadictvalue["C_PYRL_TIME_TYPE_2"] != "N/A":
            page.get_by_role("cell", name="2 Display Value").get_by_label("Payroll Time Type").click()
            page.get_by_role("cell", name="2 Display Value").get_by_label("Payroll Time Type").fill(datadictvalue["C_PYRL_TIME_TYPE_2"])
            page.wait_for_timeout(3000)
        # Enable Cost Override for Payroll Time Type
        if datadictvalue["C_COST_OVRRD_2"] == "Yes":
            page.get_by_text("Enable Cost Override for Payroll Time Type").check()
            page.wait_for_timeout(3000)
        # Enabled
        if datadictvalue["C_ENABLE_2"] == "No":
            page.get_by_text("Enabled").uncheck()
            page.wait_for_timeout(3000)
        # Worker Allowed Action
        if datadictvalue["C_WRK_ALWD_ACT_2"] != '':
            page.get_by_role("cell", name="2 Display Value").get_by_label("Worker Allowed Action").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WRK_ALWD_ACT_2"]).click()
            page.wait_for_timeout(3000)
        # Line Manager Allowed Action
        if datadictvalue["C_LIN_MGR_ALWD_ACT_2"] != '':
            page.get_by_role("cell", name="2 Display Value").get_by_label("Line Manager Allowed Action").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LIN_MGR_ALWD_ACT_2"]).click()
            page.wait_for_timeout(3000)
        # Time and Labor Manager Allowed Action
        if datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_2"] != '':
            page.get_by_role("cell", name="2 Display Value").get_by_label("Time and Labor Manager Allowed Action").first.click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_2"]).click()
            page.wait_for_timeout(3000)

        # C_DSPLY_SEQ_3
        # Display Value
        if (str(datadictvalue["C_DSPLY_SEQ_3"])) == "3":
            page.get_by_role("button", name="Add Row Below").click()
            page.wait_for_timeout(1000)
            page.get_by_role("cell", name="3 Display Value").get_by_label("Display Value").click()
            page.get_by_role("cell", name="3 Display Value").get_by_label("Display Value").fill(datadictvalue["C_DSPLY_VAL_3"])
            page.wait_for_timeout(3000)
        # Absence Management Type
            if datadictvalue["C_ABS_MGMT_TYPE_3"] != "N/A":
                page.get_by_role("cell", name="3 Display Value").get_by_label("Absence Management Type").click()
                page.get_by_role("cell", name="3 Display Value").get_by_label("Absence Management Type").fill(datadictvalue["C_ABS_MGMT_TYPE_3"])
                page.wait_for_timeout(3000)
        # Payroll Time Type
            if datadictvalue["C_PYRL_TIME_TYPE_3"] != "N/A":
                page.get_by_role("cell", name="3 Display Value").get_by_label("Payroll Time Type").click()
                page.get_by_role("cell", name="3 Display Value").get_by_label("Payroll Time Type").fill(datadictvalue["C_PYRL_TIME_TYPE_3"])
                page.wait_for_timeout(3000)
            # Enable Cost Override for Payroll Time Type
            if datadictvalue["C_COST_OVRRD_3"] == "Yes":
                page.get_by_text("Enable Cost Override for Payroll Time Type").check()
                page.wait_for_timeout(3000)
            # Enabled
            if datadictvalue["C_ENABLE_3"] == "No":
                page.get_by_text("Enabled").uncheck()
                page.wait_for_timeout(3000)
            # Worker Allowed Action
            if datadictvalue["C_WRK_ALWD_ACT_3"] != '':
                page.get_by_role("cell", name="3 Display Value").get_by_label("Worker Allowed Action").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WRK_ALWD_ACT_3"]).click()
                page.wait_for_timeout(3000)
            # Line Manager Allowed Action
            if datadictvalue["C_LIN_MGR_ALWD_ACT_3"] != '':
                page.get_by_role("cell", name="3 Display Value").get_by_label("Line Manager Allowed Action").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LIN_MGR_ALWD_ACT_3"]).click()
                page.wait_for_timeout(3000)
            # Time and Labor Manager Allowed Action
            if datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_3"] != '':
                page.get_by_role("cell", name="3 Display Value").get_by_label("Time and Labor Manager Allowed Action").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_3"]).click()
                page.wait_for_timeout(3000)

        # C_DSPLY_SEQ_4
        # Display Value
        if (str(datadictvalue["C_DSPLY_SEQ_4"])) == "4":
            page.get_by_role("button", name="Add Row Below").click()
            page.wait_for_timeout(1000)
            page.get_by_role("cell", name="4 Display Value").get_by_label("Display Value").click()
            page.get_by_role("cell", name="4 Display Value").get_by_label("Display Value").fill(datadictvalue["C_DSPLY_VAL_4"])
            page.wait_for_timeout(3000)
        # Absence Management Type
            if datadictvalue["C_ABS_MGMT_TYPE_4"] != "N/A":
                page.get_by_role("cell", name="4 Display Value").get_by_label("Absence Management Type").click()
                page.get_by_role("cell", name="4 Display Value").get_by_label("Absence Management Type").fill(datadictvalue["C_ABS_MGMT_TYPE_4"])
                page.wait_for_timeout(3000)
        # Payroll Time Type
            if datadictvalue["C_PYRL_TIME_TYPE_4"] != "N/A":
                page.get_by_role("cell", name="4 Display Value").get_by_label("Payroll Time Type").click()
                page.get_by_role("cell", name="4 Display Value").get_by_label("Payroll Time Type").fill(datadictvalue["C_PYRL_TIME_TYPE_4"])
                page.wait_for_timeout(3000)
        # Enable Cost Override for Payroll Time Type
            if datadictvalue["C_COST_OVRRD_4"] == "Yes":
                page.get_by_text("Enable Cost Override for Payroll Time Type").check()
                page.wait_for_timeout(3000)
        # Enabled
            if datadictvalue["C_ENABLE_4"] == "No":
                page.get_by_text("Enabled").uncheck()
                page.wait_for_timeout(3000)
        # Worker Allowed Action
            if datadictvalue["C_WRK_ALWD_ACT_4"] != '':
                page.get_by_role("cell", name="4 Display Value").get_by_label("Worker Allowed Action").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WRK_ALWD_ACT_4"]).click()
                page.wait_for_timeout(3000)
        # Line Manager Allowed Action
            if datadictvalue["C_LIN_MGR_ALWD_ACT_4"] != '':
                page.get_by_role("cell", name="4 Display Value").get_by_label("Line Manager Allowed Action").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LIN_MGR_ALWD_ACT_4"]).click()
                page.wait_for_timeout(3000)
        # Time and Labor Manager Allowed Action
            if datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_4"] != '':
                page.get_by_role("cell", name="4 Display Value").get_by_label("Time and Labor Manager Allowed Action").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_4"]).click()
                page.wait_for_timeout(3000)

        # C_DSPLY_SEQ_5
        # Display Value
        if (str(datadictvalue["C_DSPLY_SEQ_5"])) == "5":
            page.get_by_role("button", name="Add Row Below").click()
            page.wait_for_timeout(1000)
            page.get_by_role("cell", name="5 Display Value").get_by_label("Display Value").click()
            page.get_by_role("cell", name="5 Display Value").get_by_label("Display Value").fill(datadictvalue["C_DSPLY_VAL_5"])
            page.wait_for_timeout(3000)
        # Absence Management Type
            if datadictvalue["C_ABS_MGMT_TYPE_5"] != "N/A":
                page.get_by_role("cell", name="5 Display Value").get_by_label("Absence Management Type").click()
                page.get_by_role("cell", name="5 Display Value").get_by_label("Absence Management Type").fill(datadictvalue["C_ABS_MGMT_TYPE_5"])
                page.wait_for_timeout(3000)
        # Payroll Time Type
            if datadictvalue["C_PYRL_TIME_TYPE_5"] != "N/A":
                page.get_by_role("cell", name="5 Display Value").get_by_label("Payroll Time Type").click()
                page.get_by_role("cell", name="5 Display Value").get_by_label("Payroll Time Type").fill(datadictvalue["C_PYRL_TIME_TYPE_5"])
                page.wait_for_timeout(3000)
        # Enable Cost Override for Payroll Time Type
            if datadictvalue["C_COST_OVRRD_5"] == "Yes":
                page.get_by_text("Enable Cost Override for Payroll Time Type").check()
                page.wait_for_timeout(3000)
        # Enabled
            if datadictvalue["C_ENABLE_5"] == "No":
                page.get_by_text("Enabled").uncheck()
                page.wait_for_timeout(3000)
        # Worker Allowed Action
            if datadictvalue["C_WRK_ALWD_ACT_5"] != '':
                page.get_by_role("cell", name="5 Display Value").get_by_label("Worker Allowed Action").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WRK_ALWD_ACT_5"]).click()
                page.wait_for_timeout(3000)
        # Line Manager Allowed Action
            if datadictvalue["C_LIN_MGR_ALWD_ACT_5"] != '':
                page.get_by_role("cell", name="5 Display Value").get_by_label("Line Manager Allowed Action").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LIN_MGR_ALWD_ACT_5"]).click()
                page.wait_for_timeout(3000)
        # Time and Labor Manager Allowed Action
            if datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_5"] != '':
                page.get_by_role("cell", name="5 Display Value").get_by_label("Time and Labor Manager Allowed Action").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_5"]).click()
                page.wait_for_timeout(3000)

        # C_DSPLY_SEQ_6
        # Display Value
        if (str(datadictvalue["C_DSPLY_SEQ_6"])) == "6":
            page.get_by_role("button", name="Add Row Below").click()
            page.wait_for_timeout(1000)
            page.get_by_role("cell", name="6 Display Value").get_by_label("Display Value").click()
            page.get_by_role("cell", name="6 Display Value").get_by_label("Display Value").fill(datadictvalue["C_DSPLY_VAL_6"])
            page.wait_for_timeout(3000)
        # Absence Management Type
            if datadictvalue["C_ABS_MGMT_TYPE_6"] != "N/A":
                page.get_by_role("cell", name="6 Display Value").get_by_label("Absence Management Type").click()
                page.get_by_role("cell", name="6 Display Value").get_by_label("Absence Management Type").fill(datadictvalue["C_ABS_MGMT_TYPE_6"])
                page.wait_for_timeout(3000)
        # Payroll Time Type
            if datadictvalue["C_PYRL_TIME_TYPE_6"] != "N/A":
                page.get_by_role("cell", name="6 Display Value").get_by_label("Payroll Time Type").click()
                page.get_by_role("cell", name="6 Display Value").get_by_label("Payroll Time Type").fill(datadictvalue["C_PYRL_TIME_TYPE_6"])
                page.wait_for_timeout(3000)
        # Enable Cost Override for Payroll Time Type
            if datadictvalue["C_COST_OVRRD_6"] == "Yes":
                page.get_by_text("Enable Cost Override for Payroll Time Type").check()
                page.wait_for_timeout(3000)
        # Enabled
            if datadictvalue["C_ENABLE_6"] == "No":
                page.get_by_text("Enabled").uncheck()
                page.wait_for_timeout(3000)
        # Worker Allowed Action
            if datadictvalue["C_WRK_ALWD_ACT_6"] != '':
                page.get_by_role("cell", name="6 Display Value").get_by_label("Worker Allowed Action").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WRK_ALWD_ACT_6"]).click()
                page.wait_for_timeout(3000)
        # Line Manager Allowed Action
            if datadictvalue["C_LIN_MGR_ALWD_ACT_6"] != '':
                page.get_by_role("cell", name="6 Display Value").get_by_label("Line Manager Allowed Action").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LIN_MGR_ALWD_ACT_6"]).click()
                page.wait_for_timeout(3000)
        # Time and Labor Manager Allowed Action
            if datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_6"] != '':
                page.get_by_role("cell", name="6 Display Value").get_by_label("Time and Labor Manager Allowed Action").first.click()
                page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_6"]).click()
                page.wait_for_timeout(3000)

        # C_DSPLY_SEQ_7
        # Display Value
            if (str(datadictvalue["C_DSPLY_SEQ_7"])) == "7":
                page.get_by_role("button", name="Add Row Below").click()
                page.wait_for_timeout(1000)
                page.get_by_role("cell", name="7 Display Value").get_by_label("Display Value").click()
                page.get_by_role("cell", name="7 Display Value").get_by_label("Display Value").fill(datadictvalue["C_DSPLY_VAL_7"])
                page.wait_for_timeout(3000)
            # Absence Management Type
                if datadictvalue["C_ABS_MGMT_TYPE_7"] != '':
                    page.get_by_role("cell", name="7 Display Value").get_by_label("Absence Management Type").click()
                    page.get_by_role("cell", name="7 Display Value").get_by_label("Absence Management Type").fill(datadictvalue["C_ABS_MGMT_TYPE_7"])
                    page.wait_for_timeout(3000)
            # Payroll Time Type
                if datadictvalue["C_PYRL_TIME_TYPE_7"] != '':
                    page.get_by_role("cell", name="7 Display Value").get_by_label("Payroll Time Type").click()
                    page.get_by_role("cell", name="7 Display Value").get_by_label("Payroll Time Type").fill(datadictvalue["C_PYRL_TIME_TYPE_7"])
                    page.wait_for_timeout(3000)
            # Enable Cost Override for Payroll Time Type
                if datadictvalue["C_COST_OVRRD_7"] == "Yes":
                    page.get_by_text("Enable Cost Override for Payroll Time Type").check()
                    page.wait_for_timeout(3000)
            # Enabled
                if datadictvalue["C_ENABLE_7"] == "No":
                    page.get_by_text("Enabled").uncheck()
                    page.wait_for_timeout(3000)
            # Worker Allowed Action
                if datadictvalue["C_WRK_ALWD_ACT_7"] != '':
                    page.get_by_role("cell", name="7 Display Value").get_by_label("Worker Allowed Action").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_WRK_ALWD_ACT_7"]).click()
                    page.wait_for_timeout(3000)
            # Line Manager Allowed Action
                if datadictvalue["C_LIN_MGR_ALWD_ACT_7"] != '':
                    page.get_by_role("cell", name="7 Display Value").get_by_label("Line Manager Allowed Action").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_LIN_MGR_ALWD_ACT_7"]).click()
                    page.wait_for_timeout(3000)
            # Time and Labor Manager Allowed Action
                if datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_7"] != '':
                    page.get_by_role("cell", name="7 Display Value").get_by_label("Time and Labor Manager Allowed Action").first.click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TIME_A_LAB_MGR_ALWD_ACT_7"]).click()
                    page.wait_for_timeout(3000)

        # Filter Variable
        if datadictvalue["C_FLTR_VRBL"] != '':
            page.get_by_role("button", name="Add Filters").click()
            page.wait_for_timeout(3000)
            page.get_by_text("Filter Variable").click()
            page.get_by_role("combobox", name="TclayfldAttributeChar10").click()
            page.get_by_role("listbox").get_by_text(datadictvalue["C_FLTR_VRBL"]).click()
            page.wait_for_timeout(3000)

        # Filter Input Attribute
        if datadictvalue["C_FLTR_INPUT_ATTRBT"] != '':
            page.get_by_title("Filter Input Attribute").first.click()
            page.get_by_text(datadictvalue["C_FLTR_INPUT_ATTRBT"], exact=True).click()
            page.wait_for_timeout(3000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # Population Method for New Entry
        if datadictvalue["C_DV_PPLTN_MTHOD_FOR_NEW_ENTRY"] != '':
            page.get_by_role("combobox", name="Population Method for New Entry").click()
            page.get_by_text(datadictvalue["C_DV_PPLTN_MTHOD_FOR_NEW_ENTRY"], exact=True).click()
            page.wait_for_timeout(3000)
            # Specific Display Value
            if datadictvalue["C_SPCFC_DSPLY_VALUE"] != '':
                page.get_by_role("combobox", name="Specific Display Value").click()
                page.get_by_text(datadictvalue["C_SPCFC_DSPLY_VALUE"], exact=True).click()
                page.wait_for_timeout(3000)
            # Function
            if datadictvalue["C_DF_FUNCTION"] != '':
                page.get_by_role("combobox", name="Function").click()
                page.get_by_role("row", name="*Function", exact=True).locator("a")
                page.get_by_text(datadictvalue["C_DF_FUNCTION"], exact=True).click()
                page.wait_for_timeout(3000)

        # Display Type
        if datadictvalue["C_DSPLY_TYPE"] != '':
            page.get_by_role("combobox", name="Display Type").click()
            page.get_by_text(datadictvalue["C_DSPLY_TYPE"], exact=True).click()
            page.wait_for_timeout(3000)

        # Display Name
        if datadictvalue["C_DSPLY_NAME"] != '':
            page.get_by_label("Display Name", exact=True).clear()
            page.get_by_label("Display Name", exact=True).type(datadictvalue["C_DSPLY_NAME"])
            page.wait_for_timeout(3000)

        # Enable override on layouts
        if datadictvalue["C_ENBLE_OVRRD_ON_LYOUTS"] == "No":
            page.get_by_text("Enable override on layouts").uncheck()
            page.wait_for_timeout(3000)

        # C_RQRD_ON_THE_TIME_CARD
        if datadictvalue["C_RQRD_ON_THE_TIME_CARD"] != '':
            page.get_by_role("combobox", name="Required on the Time Card").click()
            page.get_by_text(datadictvalue["C_RQRD_ON_THE_TIME_CARD"], exact=True).click()
            page.wait_for_timeout(3000)

        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(3000)

        # C_DFD_NAME
        if (str(datadictvalue["C_DFD_NAME"])) != '':
            page.get_by_role("button", name="Create").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(str(datadictvalue["C_DFD_NAME"]))
            page.wait_for_timeout(3000)

        # C_INDPNDNT_TIME_ATTRBT
        if datadictvalue["C_INDPNDNT_TIME_ATTRBT"] != '':
            page.get_by_role("combobox", name="Independent Time Attribute").click()
            page.get_by_text(datadictvalue["C_INDPNDNT_TIME_ATTRBT"]).click()
            page.wait_for_timeout(3000)

        # C_DPNDNT_TIME_ATTRBTE
            if datadictvalue["C_DPNDNT_TIME_ATTRBTE"] != '':
                page.get_by_label("Dependent Time Attribute", exact=True).click()
                page.get_by_label("Dependent Time Attribute", exact=True).fill(datadictvalue["C_DPNDNT_TIME_ATTRBTE"])
                page.wait_for_timeout(3000)

        # C_DSCPTN
        if datadictvalue["C_DSCPTN"] != '':
            page.get_by_label("Description").click()
            page.get_by_label("Description").fill(datadictvalue["C_DSCPTN"])
            page.wait_for_timeout(3000)

        # C_AVLBLTY_ALL_INDPNDNT_VALUES
        if datadictvalue["C_AVLBLTY_ALL_INDPNDNT_VALUES"] == "For all independent time attribute values":
            page.get_by_text("For all independent time attribute values").click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Yes").click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)
        if datadictvalue["C_AVLBLTY_ALL_INDPNDNT_VALUES"] == "For specific independent time attribute values":
            page.get_by_text("For specific independent time attribute values").click()
            page.wait_for_timeout(3000)
        # C_AVLBLTY_INDPNDNT_VALUES
            if datadictvalue["C_AVLBLTY_INDPNDNT_VALUES"] != '':
                page.get_by_role("combobox", name="TclayfldValue").click()
                page.get_by_text(datadictvalue["C_AVLBLTY_INDPNDNT_VALUES"]).click()
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)

        # C_TA_FLTRD_SRC_TIME_ENTRY
        if datadictvalue["C_TA_FLTRD_SRC_TIME_ENTRY"] != '':
            page.get_by_label("Filtered Data Source for Time Entry").click()
            page.get_by_title("Search and Select: Filtered Data Source for Time Entry").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(3000)
            page.get_by_role("cell", name="*Name Name Name").get_by_label("Name").click()
            page.get_by_role("cell", name="*Name Name Name").get_by_label("Name").fill(datadictvalue["C_TA_FLTRD_SRC_TIME_ENTRY"])
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.get_by_role("cell", name=datadictvalue["C_TA_FLTRD_SRC_TIME_ENTRY"], exact=True).locator("span").click()
            page.get_by_role("cell", name=datadictvalue["C_TA_FLTRD_SRC_TIME_ENTRY"], exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)

            # Filter Variable
            if datadictvalue["C_FLTR_VRBL_1"] != '':
                page.get_by_role("button", name="Add Filters").click()
                page.wait_for_timeout(3000)
                page.get_by_text("Filter Variable").click()
                page.get_by_role("combobox", name="TclayfldAttributeChar10").click()
                page.wait_for_timeout(3000)
                page.get_by_role("listbox").get_by_text(datadictvalue["C_FLTR_VRBL_1"]).click()
                page.wait_for_timeout(3000)
            # Filter Input Attribute
            if datadictvalue["C_FLTR_INPUT_ATTRBT_1"] != '':
                page.get_by_title("Filter Input Attribute").first.click()
                page.get_by_role("link", name="Search...").click()
                page.wait_for_timeout(3000)
                page.get_by_role("combobox", name="Search Results Level").click()
                page.get_by_text("Detailed").click()
                page.get_by_role("cell", name="Search Results Level Search").get_by_label("Name").click()
                page.get_by_role("cell", name="Search Results Level Search").get_by_label("Name").fill(datadictvalue["C_FLTR_INPUT_ATTRBT_1"])
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="Search", exact=True).click()
                page.get_by_text(datadictvalue["C_FLTR_INPUT_ATTRBT_1"], exact=True).click()
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="OK").nth(1).click()
                page.wait_for_timeout(3000)
                page.get_by_role("button", name="OK").click()
                page.wait_for_timeout(3000)

        # C_TA_UNFILTRD_SRC_STP_TASK
        if datadictvalue["C_TA_UNFILTRD_SRC_STP_TASK"] != '':
            page.get_by_label("Unfiltered Data Source for Setup Tasks").click()
            page.get_by_title("Search and Select: Unfiltered Data Source for Setup Tasks").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(3000)
            page.get_by_role("cell", name="*Name Name Name").get_by_label("Name").fill(datadictvalue["C_TA_UNFILTRD_SRC_STP_TASK"])
            page.get_by_role("cell", name="*Name Name Name").get_by_label("Name").click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TA_UNFILTRD_SRC_STP_TASK"]).click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="OK").click()
            page.wait_for_timeout(3000)

        # C_GP_PPLTN_MTHOD_FOR_NEW_ENTRY
        if datadictvalue["C_GP_PPLTN_MTHOD_FOR_NEW_ENTRY"] != '':
            page.get_by_role("combobox", name="Population Method for New Entry").click()
            page.get_by_text(datadictvalue["C_GP_PPLTN_MTHOD_FOR_NEW_ENTRY"]).click()
            page.wait_for_timeout(4000)
            # C_GP_SPCFC_DSPLY_VALUE
            if datadictvalue["C_GP_SPCFC_DSPLY_VALUE"] != '':
                page.get_by_role("combobox", name="Specific Display Value").click()
                page.get_by_label("Specific Display Value").fill(datadictvalue["C_GP_SPCFC_DSPLY_VALUE"])
                page.wait_for_timeout(3000)
            # C_DF_FUNCTION
            if datadictvalue["C_GP_FUNCTION"] != '':
                page.get_by_role("combobox", name="Function").click()
                page.get_by_role("row", name="Function", exact=True).locator("a")
                page.get_by_text(datadictvalue["C_GP_FUNCTION"]).click()
                page.wait_for_timeout(3000)

        # C_GP_DSPLY_TYPE
        if datadictvalue["C_GP_DSPLY_TYPE"] != '':
            page.get_by_role("combobox", name="Display Type").click()
            page.get_by_text(datadictvalue["C_GP_DSPLY_TYPE"]).click()
            page.wait_for_timeout(3000)

        # C_GP_DSPLY_NAME
        if datadictvalue["C_GP_DSPLY_NAME"] != '':
            page.get_by_label("Display Name").click()
            page.get_by_label("Display Name").clear()
            page.get_by_label("Display Name").fill(datadictvalue["C_GP_DSPLY_NAME"])
            page.wait_for_timeout(3000)

        # C_GP_ENBLE_OVRRD_ON_LYOUTS
        if datadictvalue["C_GP_ENBLE_OVRRD_ON_LYOUTS"] == "No":
            page.get_by_text("Enable override on layouts").uncheck()
            page.wait_for_timeout(3000)
        if datadictvalue["C_GP_ENBLE_OVRRD_ON_LYOUTS"] == "Yes":
            page.get_by_text("Enable override on layouts").check()

        # C_GP_RQRD_ON_THE_TIME_CARD
        if datadictvalue["C_GP_RQRD_ON_THE_TIME_CARD"] != '':
            page.get_by_role("combobox", name="Required on the Time Card").click()
            page.get_by_text(datadictvalue["C_GP_RQRD_ON_THE_TIME_CARD"], exact=True).click()
            page.wait_for_timeout(3000)

        # Clicking on Next button
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(5000)
        page.get_by_role("button", name="Cancel").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Yes").click()
        page.wait_for_timeout(2000)

        try:
            expect(page.get_by_role("heading", name="Time Entry Layout Components")).to_be_visible()
            page.wait_for_timeout(3000)
            print("Time Entry - Multiple Attribute Component Created Successfully")
            datadictvalue["RowStatus"] = "Created Time Entry - Multiple Attribute Component Successfully"
        except Exception as e:
            print("Unable to Save Time Entry - Multiple Attribute Component")
            datadictvalue["RowStatus"] = "Unable to Save Time Entry - Multiples Attribute Component"

        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, MULTIPLE_ATTRIBUTE_COMPONENT):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, MULTIPLE_ATTRIBUTE_COMPONENT, PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK, MULTIPLE_ATTRIBUTE_COMPONENT)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0])
        write_status(output,
                     RESULTS_DIR_PATH + re.split(".xlsx", HCM_TIME_AND_LABOR_WRKBK)[0] + "_Results_" + datetime.now().strftime(
                         "%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
