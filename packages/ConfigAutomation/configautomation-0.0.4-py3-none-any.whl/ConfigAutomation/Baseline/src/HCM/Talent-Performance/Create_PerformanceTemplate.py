from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("My Client Groups", exact=True).click()
    page.get_by_role("link", name="Performance").click()
    page.wait_for_timeout(10000)
    page.get_by_role("link", name="Performance Templates").click()
    page.wait_for_timeout(5000)

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Click on Create Button
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(3000)

        # Template Type
        page.get_by_role("combobox", name="Template Type").click()
        page.wait_for_timeout(3000)
        page.get_by_text(datadictvalue["C_G_PFM_TMTY"], exact=True).click()

        # Name
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_G_PFM_NM"])
        page.wait_for_timeout(1000)

        # Comments
        page.get_by_label("Comments").click()
        page.get_by_label("Comments").fill(datadictvalue["C_G_PFM_CMMT"])
        page.wait_for_timeout(1000)

        # From Date
        page.get_by_text("From Date").click()
        page.get_by_role("row", name="*From Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").click()
        page.get_by_role("row", name="*From Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").fill(str(datadictvalue["C_G_PFM_FRM_DT"]))
        page.wait_for_timeout(3000)

        # To Date
        page.get_by_text("To Date").click()
        page.get_by_role("row", name="*To Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").click()
        page.get_by_role("row", name="*To Date m/d/yy Press down arrow to access Calendar Select Date", exact=True).get_by_placeholder("m/d/yy").fill(str(datadictvalue["C_G_PFM_T_DT"]))
        page.wait_for_timeout(3000)

        # Status
        page.get_by_role("combobox", name="Status").click()
        page.wait_for_timeout(3000)
        page.get_by_text(datadictvalue["C_G_PFM_STS"], exact=True).click()
        page.wait_for_timeout(3000)

        # Document Type
        page.get_by_label("Document Type").click()
        page.get_by_label("Document Type").fill(datadictvalue["C_G_PFM_DCTY"])
        page.get_by_label("Document Type").press("Enter")
        page.wait_for_timeout(3000)

        # Eligibility Profile
        if datadictvalue["C_G_PFM_ELGP"] != '':
            page.get_by_role("heading", name="Eligibility Profile").click()
            page.get_by_role("button", name="Add Row").click()
            page.wait_for_timeout(3000)
            page.locator("//span[text()='Eligibility Profile']//following::input[1]").clear()
            page.locator("//span[text()='Eligibility Profile']//following::input[1]").type(datadictvalue["C_G_PFM_ELGP"])
            page.wait_for_timeout(3000)

            if datadictvalue["C_G_PFM_RQED"] != '':
                if datadictvalue["C_G_PFM_RQED"] != "Yes":
                    page.locator("//span[text()='Required']//following::label[1]").check()
                    page.wait_for_timeout(3000)
                if datadictvalue["C_G_PFM_RQED"] == "No":
                    page.locator("//span[text()='Required']//following::label[1]").uncheck()
                    page.wait_for_timeout(3000)

        # Participation - Set the minimum number of participants
        if datadictvalue["C_G_PFM_MN_PRTC"] != '':
            if datadictvalue["C_G_PFM_MN_PRTC"] == "No":
                page.get_by_text("Set the minimum number of participants").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_G_PFM_MN_PRTC"] == "Yes":
                page.get_by_text("Set the minimum number of participants").check()
                page.wait_for_timeout(3000)
                if datadictvalue["C_G_PFM_RQ_PRTC"] != '':
                    page.get_by_label("How many participants required in total?").clear()
                    page.get_by_label("How many participants required in total?").type(str(datadictvalue["C_G_PFM_RQ_PRTC"]))
                    page.wait_for_timeout(3000)
                if datadictvalue["C_G_PFM_DFRT"] != '':
                    if datadictvalue["C_G_PFM_DFRT"] == "No":
                        page.get_by_text("Do you want to enforce this?").uncheck()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_G_PFM_DFRT"] == "Yes":
                        page.get_by_text("Do you want to enforce this?").check()
                        page.wait_for_timeout(3000)

        # Participation - Set the maximum number of participants
        if datadictvalue["C_G_PFM_MX_PRTC"] != '':
            if datadictvalue["C_G_PFM_MX_PRTC"] == "No":
                page.get_by_text("Set the maximum number of participants").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_G_PFM_MX_PRTC"] == "Yes":
                page.get_by_text("Set the maximum number of participants").check()
                page.wait_for_timeout(3000)
                if datadictvalue["C_G_PFM_PLLT"] != '':
                    page.get_by_label("How many participants allowed in total?").clear()
                    page.get_by_label("How many participants allowed in total?").type(str(datadictvalue["C_G_PFM_PLLT"]))
                    page.wait_for_timeout(3000)

        # View - Role 1
        if datadictvalue["C_G_PFM_RL_1"] != '':
            page.get_by_role("heading", name="Participation").click()
            page.get_by_role("button", name="Add", exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Role").click()
            # page.get_by_role("combobox", name="Role").nth(1).click()
            # page.get_by_role("table", name="Participation").locator("a").first.click()
            page.get_by_text(datadictvalue["C_G_PFM_RL_1"]).click()
            # page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_G_PFM_RL_1"], exact=True).click()
            page.wait_for_timeout(3000)
            # Maximum Number of Participants Required per Role
            if datadictvalue["C_G_PFM_MX_PRTC_1"] != '':
                expect(page.get_by_label("Maximum Number of Participants Allowed per Role")).to_be_disabled()
                if not page.get_by_label("Maximum Number of Participants Allowed per Role").is_visible():
                    # page.locator("//span[text()='Maximum Number of Participants Allowed per Role']//following::input[3]")
                    page.get_by_label("Maximum Number of Participants Allowed per Role").clear()
                    page.get_by_label("Maximum Number of Participants Allowed per Role").type(str(datadictvalue["C_G_PFM_MX_PRTC_1"]))
                page.wait_for_timeout(3000)
            # Minimum Number of Participants Required per Role
            if datadictvalue["C_G_PFM_N_PRTC_1"] != '':
                expect(page.get_by_label("Minimum Number of Participants Required per Role")).to_be_disabled()
                if not page.get_by_label("Minimum Number of Participants Required per Role").is_visible():
                    # page.locator("//span[text()='Minimum Number of Participants Required per Role']//following::input[4]")
                    page.get_by_label("Minimum Number of Participants Required per Role").clear()
                    page.get_by_label("Minimum Number of Participants Required per Role").type(str(datadictvalue["C_G_PFM_N_PRTC_1"]))
                page.wait_for_timeout(3000)

        # View - Role 2
        if datadictvalue["C_G_PFM_RL_2"] != '':
            page.get_by_role("heading", name="Participation").click()
            page.get_by_role("button", name="Add", exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Role").nth(1).click()
            # page.get_by_role("table", name="Participation").locator("a").nth(1)
            page.wait_for_timeout(3000)
            # page.get_by_text(datadictvalue["C_G_PFM_RL_2"]).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_G_PFM_RL_2"]).click()
            page.wait_for_timeout(3000)
            # Maximum Number of Participants Required per Role
            if datadictvalue["C_G_PFM_MX_PRTC_2"] != '':
                expect(page.get_by_label("Maximum Number of Participants Allowed per Role")).to_be_disabled()
                if not page.get_by_label("Maximum Number of Participants Allowed per Role").is_visible():
                    # page.locator("//span[text()='Maximum Number of Participants Allowed per Role']//following::input[3]")
                    page.get_by_label("Maximum Number of Participants Allowed per Role").clear()
                    page.get_by_label("Maximum Number of Participants Allowed per Role").type(str(datadictvalue["C_G_PFM_MX_PRTC_2"]))
                page.wait_for_timeout(3000)
            # Minimum Number of Participants Required per Role
            if datadictvalue["C_G_PFM_N_PRTC_2"] != '':
                expect(page.get_by_label("Minimum Number of Participants Required per Role")).to_be_disabled()
                if not page.get_by_label("Minimum Number of Participants Required per Role").is_visible():
                    # page.locator("//span[text()='Minimum Number of Participants Required per Role']//following::input[4]")
                    page.get_by_label("Minimum Number of Participants Required per Role").clear()
                    page.get_by_label("Minimum Number of Participants Required per Role").type(str(datadictvalue["C_G_PFM_N_PRTC_2"]))
                page.wait_for_timeout(3000)

        # View - Role 3
        if datadictvalue["C_G_PFM_RL_3"] != '':
            page.get_by_role("button", name="Add", exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Role").nth(2).click()
            # page.get_by_role("table", name="Participation").locator("a").nth(2)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_G_PFM_RL_3"], exact=True).click()
            page.wait_for_timeout(3000)
            # Maximum Number of Participants Required per Role
            if datadictvalue["C_G_PFM_MX_PRTC_3"] != '':
                expect(page.get_by_label("Maximum Number of Participants Allowed per Role")).to_be_disabled()
                if not page.get_by_label("Maximum Number of Participants Allowed per Role").is_visible():
                    # page.locator("//span[text()='Maximum Number of Participants Allowed per Role']//following::input[3]")
                    page.get_by_label("Maximum Number of Participants Allowed per Role").clear()
                    page.get_by_label("Maximum Number of Participants Allowed per Role").type(str(datadictvalue["C_G_PFM_MX_PRTC_3"]))
                page.wait_for_timeout(3000)
            # Minimum Number of Participants Required per Role
            if datadictvalue["C_G_PFM_N_PRTC_3"] != '':
                expect(page.get_by_label("Minimum Number of Participants Required per Role")).to_be_disabled()
                if not page.get_by_label("Minimum Number of Participants Required per Role").is_visible():
                    # page.locator("//span[text()='Minimum Number of Participants Required per Role']//following::input[4]")
                    page.get_by_label("Minimum Number of Participants Required per Role").clear()
                    page.get_by_label("Minimum Number of Participants Required per Role").type(str(datadictvalue["C_G_PFM_N_PRTC_3"]))
                page.wait_for_timeout(3000)
            # # Minimum Number of Participants Required per Role
            # if datadictvalue["C_G_PFM_N_PRTC_3"] != '':
            #     expect(page.get_by_role("cell", name="View Worker and Manager Evaluations by this Role Role Maximum Number of").get_by_label("Minimum Number of")).to_be_disabled()
            #     if not page.get_by_role("cell", name="View Worker and Manager Evaluations by this Role Role Maximum Number of").get_by_label("Minimum Number of").is_visible():
            #         page.get_by_role("cell", name="View Worker and Manager Evaluations by this Role Role Maximum Number of").get_by_label("Minimum Number of").clear()
            #         page.get_by_role("cell", name="View Worker and Manager Evaluations by this Role Role Maximum Number of").get_by_label("Minimum Number of").type(str(datadictvalue["C_G_PFM_N_PRTC_3"]))
            #     page.wait_for_timeout(3000)
            # # Maximum Number of Participants Required per Role
            # if datadictvalue["C_G_PFM_MX_PRTC_3"] != '':
            #     expect(page.get_by_role("cell", name="View Worker and Manager Evaluations by this Role Role Maximum Number of").get_by_label("Maximum Number of")).to_be_disabled()
            #     if not page.get_by_role("cell", name="View Worker and Manager Evaluations by this Role Role Maximum Number of").get_by_label("Maximum Number of").is_visible():
            #         page.get_by_role("cell", name="View Worker and Manager Evaluations by this Role Role Maximum Number of").get_by_label("Maximum Number of").clear()
            #         page.get_by_role("cell", name="View Worker and Manager Evaluations by this Role Role Maximum Number of").get_by_label("Maximum Number of").type(str(datadictvalue["C_G_PFM_MX_PRTC_3"]))
            #     page.wait_for_timeout(3000)

        if datadictvalue["C_G_PFM_RL_4"] == '':
            pass
        # View - Role 4
        else:
            page.get_by_role("button", name="Add", exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Role").nth(3).click()
            # page.get_by_role("table", name="Participation").locator("a").nth(3)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_G_PFM_RL_4"], exact=True).click()
            page.wait_for_timeout(3000)
            # Minimum Number of Participants Required per Role
            if datadictvalue["C_G_PFM_N_PRTC_4"] != '':
                expect(page.get_by_label("Minimum Number of Participants Required per Role")).to_be_disabled()
                if not page.get_by_label("Minimum Number of Participants Required per Role").is_visible():
                    page.get_by_label("Minimum Number of Participants Required per Role").clear()
                    page.get_by_label("Minimum Number of Participants Required per Role").type(str(datadictvalue["C_G_PFM_N_PRTC_4"]))
                page.wait_for_timeout(3000)
            # Maximum Number of Participants Required per Role
            if datadictvalue["C_G_PFM_MX_PRTC_4"] != '':
                expect(page.get_by_label("Maximum Number of Participants Allowed per Role")).to_be_disabled()
                if not page.get_by_label("Maximum Number of Participants Allowed per Role").is_visible():
                    page.get_by_label("Maximum Number of Participants Allowed per Role").clear()
                    page.get_by_label("Maximum Number of Participants Allowed per Role").type(str(datadictvalue["C_G_PFM_MX_PRTC_4"]))
                page.wait_for_timeout(3000)

        # View - Role 5
        if datadictvalue["C_G_PFM_RL_5"] == '':
            pass
        # View - Role 5
        else:
            page.get_by_role("button", name="Add", exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Role").nth(4).click()
            # page.get_by_role("table", name="Participation").locator("a").nth(4)
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_G_PFM_RL_5"], exact=True).click()
            page.wait_for_timeout(3000)
            # Minimum Number of Participants Required per Role
            if datadictvalue["C_G_PFM_N_PRTC_5"] != '':
                expect(page.get_by_label("Minimum Number of Participants Required per Role")).to_be_disabled()
                if not page.get_by_label("Minimum Number of Participants Required per Role").is_visible():
                    page.get_by_label("Minimum Number of Participants Required per Role").clear()
                    page.get_by_label("Minimum Number of Participants Required per Role").type(str(datadictvalue["C_G_PFM_N_PRTC_5"]))
                page.wait_for_timeout(3000)
            # Maximum Number of Participants Required per Role
            if datadictvalue["C_G_PFM_MX_PRTC_5"] != '':
                expect(page.get_by_label("Minimum Number of Participants Required per Role")).to_be_disabled()
                if not page.get_by_label("Minimum Number of Participants Required per Role").is_visible():
                    page.get_by_label("Maximum Number of Participants Allowed per Role").clear()
                    page.get_by_label("Maximum Number of Participants Allowed per Role").type(str(datadictvalue["C_G_PFM_MX_PRTC_5"]))
                page.wait_for_timeout(3000)
        page.get_by_role("button", name="Save", exact=True).click()
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # Process Flow
        if datadictvalue["C_P_PFM_PF"] != '':
            page.get_by_role("link", name="Process").click()
            page.wait_for_timeout(3000)
            page.get_by_label("Process Flow").click()
            page.get_by_title("Search: Process Flow").click()
            page.get_by_role("link", name="Search...").click()
            page.get_by_label("Name").click()
            page.get_by_label("Name").fill(datadictvalue["C_P_PFM_PF"])
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Search", exact=True).click()
            page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_P_PFM_PF"]).click()
            page.get_by_role("button", name="OK").click()
            # page.get_by_label("Process Flow").click()
            # page.get_by_label("Process Flow").fill(datadictvalue["C_P_PFM_PF"])
            # page.wait_for_timeout(1000)
            # page.get_by_label("Process Flow").press("Tab")
            # # page.get_by_role("option", name=datadictvalue["C_PFM_PF"]).click()
            page.wait_for_timeout(3000)

        # Task 1
            if datadictvalue["C_P_PFM_TSK_1"] == "Worker Self-Evaluation":
                # Standard Alert Days
                if datadictvalue["C_P_PFM_SLRT_1"] != '':
                    page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Standard Alert Days").clear()
                    page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Standard Alert Days").fill(str(datadictvalue["C_P_PFM_SLRT_1"]))
                    page.wait_for_timeout(3000)
                # Repeat Standard Alert Until Task Completes
                if datadictvalue["C_P_PFM_RP_LRT_1"] != '':
                    if datadictvalue["C_P_PFM_RP_LRT_1"] == "Yes":
                        page.get_by_role("row", name="Worker Self-Evaluation").locator("label").nth(1).check()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_RP_LRT_1"] == "No":
                        page.get_by_role("row", name="Worker Self-Evaluation").locator("label").nth(1).uncheck()
                        page.wait_for_timeout(3000)
                # Critical Alert Days
                if datadictvalue["C_P_PFM_CRT_LRT_1"] != '':
                    page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Critical Alert Days").click()
                    page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Critical Alert Days").fill(str(datadictvalue["C_P_PFM_CRT_LRT_1"]))
                    page.wait_for_timeout(3000)
                # Repeat Critical Alert Until Task Completes
                if datadictvalue["C_P_PFM_RC_LRT_1"] != '':
                    if datadictvalue["C_P_PFM_RC_LRT_1"] == "Yes":
                        page.get_by_role("row", name="Worker Self-Evaluation").locator("label").nth(3).check()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_RC_LRT_1"] == "No":
                        page.get_by_role("row", name="Worker Self-Evaluation").locator("label").nth(3).uncheck()
                        page.wait_for_timeout(3000)

        # Task 2
            if datadictvalue["C_P_PFM_TSK_2"] == "Manage Participant Feedback":
                # Standard Alert Days
                if datadictvalue["C_P_PFM_SLRT_2"] != '':
                    page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Standard Alert Days").clear()
                    page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Standard Alert Days").fill(str(datadictvalue["C_P_PFM_SLRT_2"]))
                    page.wait_for_timeout(3000)
                # Repeat Standard Alert Until Task Completes
                if datadictvalue["C_P_PFM_RP_LRT_2"] != '':
                    if datadictvalue["C_P_PFM_RP_LRT_2"] == "Yes":
                        page.get_by_role("row", name="Manage Participant Feedback").locator("label").nth(1).check()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_RP_LRT_2"] == "No":
                        page.get_by_role("row", name="Manage Participant Feedback").locator("label").nth(1).uncheck()
                        page.wait_for_timeout(3000)
                # Critical Alert Days
                if datadictvalue["C_P_PFM_CRT_LRT_2"] != '':
                    page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Critical Alert Days").click()
                    page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Critical Alert Days").fill(str(datadictvalue["C_P_PFM_CRT_LRT_2"]))
                    page.wait_for_timeout(3000)
                # Repeat Critical Alert Until Task Completes
                if datadictvalue["C_P_PFM_RC_LRT_2"] != '':
                    if datadictvalue["C_P_PFM_RC_LRT_2"] == "Yes":
                        page.get_by_role("row", name="Manage Participant Feedback").locator("label").nth(3).check()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_RC_LRT_2"] == "No":
                        page.get_by_role("row", name="Manage Participant Feedback").locator("label").nth(3).uncheck()
                        page.wait_for_timeout(3000)

        # Task 3
            if datadictvalue["C_P_PFM_TSK_3"] == "Manager Evaluation of Workers":
                # Standard Alert Days
                if datadictvalue["C_P_PFM_SLRT_3"] != '':
                    page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Standard Alert Days").clear()
                    page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Standard Alert Days").fill(str(datadictvalue["C_P_PFM_SLRT_3"]))
                    page.wait_for_timeout(3000)
                # Repeat Standard Alert Until Task Completes
                if datadictvalue["C_P_PFM_RP_LRT_3"] != '':
                    if datadictvalue["C_P_PFM_RP_LRT_3"] == "Yes":
                        page.get_by_role("row", name="Manager Evaluation of Workers").locator("label").nth(1).check()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_RP_LRT_3"] == "No":
                        page.get_by_role("row", name="Manager Evaluation of Workers").locator("label").nth(1).uncheck()
                        page.wait_for_timeout(3000)
                # Critical Alert Days
                if datadictvalue["C_P_PFM_CRT_LRT_3"] != '':
                    page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Critical Alert Days").click()
                    page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Critical Alert Days").fill(str(datadictvalue["C_P_PFM_CRT_LRT_3"]))
                    page.wait_for_timeout(3000)
                # Repeat Critical Alert Until Task Completes
                if datadictvalue["C_P_PFM_RC_LRT_3"] != '':
                    if datadictvalue["C_P_PFM_RC_LRT_3"] == "Yes":
                        page.get_by_role("row", name="Manager Evaluation of Workers").locator("label").nth(3).check()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_RC_LRT_3"] == "No":
                        page.get_by_role("row", name="Manager Evaluation of Workers").locator("label").nth(3).uncheck()
                        page.wait_for_timeout(3000)

        # Task 4
            if datadictvalue["C_P_PFM_TSK_4"] == "Manager Evaluation of Workers":
                # Standard Alert Days
                if datadictvalue["C_P_PFM_SLRT_4"] != '':
                    page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Standard Alert Days").clear()
                    page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Standard Alert Days").fill(str(datadictvalue["C_P_PFM_SLRT_4"]))
                    page.wait_for_timeout(3000)
                # Repeat Standard Alert Until Task Completes
                if datadictvalue["C_P_PFM_RP_LRT_4"] != '':
                    if datadictvalue["C_P_PFM_RP_LRT_4"] == "Yes":
                        page.get_by_role("row", name="Manager Evaluation of Workers").locator("label").nth(1).check()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_RP_LRT_4"] == "No":
                        page.get_by_role("row", name="Manager Evaluation of Workers").locator("label").nth(1).uncheck()
                        page.wait_for_timeout(3000)
                # Critical Alert Days
                if datadictvalue["C_P_PFM_CRT_LRT_4"] != '':
                    page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Critical Alert Days").click()
                    page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Critical Alert Days").fill(str(datadictvalue["C_P_PFM_CRT_LRT_4"]))
                    page.wait_for_timeout(3000)
                # Repeat Critical Alert Until Task Completes
                if datadictvalue["C_P_PFM_RC_LRT_4"] != '':
                    if datadictvalue["C_P_PFM_RC_LRT_4"] == "Yes":
                        page.get_by_role("row", name="Manager Evaluation of Workers").locator("label").nth(3).check()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_RC_LRT_4"] == "No":
                        page.get_by_role("row", name="Manager Evaluation of Workers").locator("label").nth(3).uncheck()
                        page.wait_for_timeout(3000)

        # Task 5
            if datadictvalue["C_P_PFM_TSK_5"] == "Manager Evaluation of Workers":
                # Standard Alert Days
                if datadictvalue["C_P_PFM_SLRT_5"] != '':
                    page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Standard Alert Days").clear()
                    page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Standard Alert Days").fill(str(datadictvalue["C_P_PFM_SLRT_5"]))
                    page.wait_for_timeout(3000)
                # Repeat Standard Alert Until Task Completes
                if datadictvalue["C_P_PFM_RP_LRT_5"] != '':
                    if datadictvalue["C_P_PFM_RP_LRT_5"] == "Yes":
                        page.get_by_role("row", name="Manager Evaluation of Workers").locator("label").nth(1).check()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_RP_LRT_5"] == "No":
                        page.get_by_role("row", name="Manager Evaluation of Workers").locator("label").nth(1).uncheck()
                        page.wait_for_timeout(3000)
                # Critical Alert Days
                if datadictvalue["C_P_PFM_CRT_LRT_5"] != '':
                    page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Critical Alert Days").click()
                    page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Critical Alert Days").fill(str(datadictvalue["C_P_PFM_CRT_LRT_5"]))
                    page.wait_for_timeout(3000)
                # Repeat Critical Alert Until Task Completes
                if datadictvalue["C_P_PFM_RC_LRT_5"] != '':
                    if datadictvalue["C_P_PFM_RC_LRT_5"] == "Yes":
                        page.get_by_role("row", name="Manager Evaluation of Workers").locator("label").nth(3).check()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_RC_LRT_5"] == "No":
                        page.get_by_role("row", name="Manager Evaluation of Workers").locator("label").nth(3).uncheck()
                        page.wait_for_timeout(3000)

        # Rating Calculations
        if datadictvalue["C_P_PFM_CLRT"] != '':
            if datadictvalue["C_P_PFM_CLRT"] == "No":
                page.get_by_text("Calculate ratings").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_P_PFM_CLRT"] == "Yes":
                page.get_by_text("Calculate ratings").check()
                page.wait_for_timeout(3000)
                # Display calculated ratings to worker
                if datadictvalue["C_P_PFM_CLRT_WRK"] != '':
                    if datadictvalue["C_P_PFM_CLRT_WRK"] == "No":
                        page.get_by_text("Display calculated ratings to worker").uncheck()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_CLRT_WRK"] == "Yes":
                        page.get_by_text("Display calculated ratings to worker").check()
                        page.wait_for_timeout(3000)
                # Display calculated ratings to manager
                if datadictvalue["C_P_PFM_CLRT_MGR"] != '':
                    if datadictvalue["C_P_PFM_CLRT_MGR"] == "No":
                        page.get_by_text("Display calculated ratings to manager").uncheck()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_CLRT_MGR"] == "Yes":
                        page.get_by_text("Display calculated ratings to manager").check()
                        page.wait_for_timeout(3000)
                # Display calculated ratings to participants
                if datadictvalue["C_P_PFM_RT_PRTC"] != '':
                    if datadictvalue["C_P_PFM_RT_PRTC"] == "No":
                        page.get_by_text("Display calculated ratings to participants").uncheck()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_RT_PRTC"] == "Yes":
                        page.get_by_text("Display calculated ratings to participants").check()
                        page.wait_for_timeout(3000)
                # Display calculated ratings to matrix managers
                if datadictvalue["C_P_PFM_RT_MM"] != '':
                    if datadictvalue["C_P_PFM_RT_MM"] == "No":
                        page.get_by_text("Display calculated ratings to matrix managers").uncheck()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_RT_MM"] == "Yes":
                        page.get_by_text("Display calculated ratings to matrix managers").check()
                        page.wait_for_timeout(3000)
                # Use calculated ratings only
                if datadictvalue["C_P_PFM_CL_RT"] != '':
                    if datadictvalue["C_P_PFM_CL_RT"] == "No":
                        page.get_by_text("Use calculated ratings only").uncheck()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_CL_RT"] == "Yes":
                        page.get_by_text("Use calculated ratings only").check()
                        page.wait_for_timeout(3000)

        # Processing Options
        # Display star ratings
        if datadictvalue["C_P_PFM_DSR"] != '':
            if datadictvalue["C_P_PFM_DSR"] == "No":
                page.get_by_text("Display star ratings").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_P_PFM_DSR"] == "Yes":
                page.get_by_text("Display star ratings").check()
                page.wait_for_timeout(3000)
        # Include digital signature
        if datadictvalue["C_P_PFM_IDS"] != '':
            if datadictvalue["C_P_PFM_IDS"] == "No":
                page.get_by_text("Include digital signatures").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_P_PFM_IDS"] == "Yes":
                page.get_by_text("Include digital signature").check()
                page.wait_for_timeout(3000)
        # Display Check-Ins
        if datadictvalue["C_P_PFM_CHK_IN"] != '':
            if datadictvalue["C_P_PFM_CHK_IN"] == "No":
                page.get_by_text("Display Check-Ins").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_P_PFM_CHK_IN"] == "Yes":
                page.get_by_text("Display Check-Ins").check()
                page.wait_for_timeout(3000)
        # Display Feedback Notes
        if datadictvalue["C_P_PFM_DFN"] != '':
            if datadictvalue["C_P_PFM_DFN"] == "No":
                page.get_by_text("Display Feedback Notes").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_P_PFM_DFN"] == "Yes":
                page.get_by_text("Display Feedback Notes").check()
                page.wait_for_timeout(3000)
        # Display Requested Feedback
        if datadictvalue["C_P_PFM_DRF"] != '':
            if datadictvalue["C_P_PFM_DRF"] == "No":
                page.get_by_text("Display Requested Feedback").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_P_PFM_DRF"] == "Yes":
                page.get_by_text("Display Requested Feedback").check()
                page.wait_for_timeout(3000)
        # Minimum Character Limit for Evaluation Comments
        if datadictvalue["C_P_PFM_MIN_CLEC"] != '':
            page.get_by_label("Minimum Character Limit for Evaluation Comments").click()
            page.get_by_label("Minimum Character Limit for Evaluation Comments").fill(str(datadictvalue["C_P_PFM_MIN_CLEC"]))
            page.wait_for_timeout(3000)
        # Maximum Character Limit for Evaluation Comments
        if datadictvalue["C_P_PFM_MAX_CLEC"] != '':
            page.get_by_label("Maximum Character Limit for Evaluation Comments").click()
            page.get_by_label("Maximum Character Limit for Evaluation Comments").fill(str(datadictvalue["C_P_PFM_MAX_CLEC"]))
            page.wait_for_timeout(3000)

        # Participant feedback is required - Not in UI / but in WB

        # Participant Options
        # Worker can view the participants added by manager or HR
        if datadictvalue["C_P_PFM_PRTC_HR"] != '':
            if datadictvalue["C_P_PFM_PRTC_HR"] == "No":
                page.get_by_text("Worker can view the participants added by manager or HR").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_P_PFM_PRTC_HR"] == "Yes":
                page.get_by_text("Worker can view the participants added by manager or HR").check()
                page.wait_for_timeout(3000)
        # Auto-populate matrix managers of the worker as participants
        if datadictvalue["C_P_PFM_MM_W_PRTC"] != '':
            if datadictvalue["C_P_PFM_MM_W_PRTC"] == "No":
                page.get_by_text("Auto-populate matrix managers of the worker as participants").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_P_PFM_MM_W_PRTC"] == "Yes":
                page.get_by_text("Auto-populate matrix managers of the worker as participants").check()
                page.wait_for_timeout(3000)
                # Allow matrix managers to access worker document automatically
                if datadictvalue["C_P_PFM_MM_WRK_DA"] != '':
                    if datadictvalue["C_P_PFM_MM_WRK_DA"] == "No":
                        page.get_by_text("Allow matrix managers to access worker document automatically").uncheck()
                        page.wait_for_timeout(3000)
                    if datadictvalue["C_P_PFM_MM_WRK_DA"] == "Yes":
                        page.get_by_text("Allow matrix managers to access worker document automatically").check()
                        page.wait_for_timeout(3000)
                # Default participant role
                if datadictvalue["C_P_PFM_DFT_PRTC"] != '':
                    page.get_by_role("combobox", name="Default participant role").click()
                    page.get_by_text(datadictvalue["C_P_PFM_DFT_PRTC"]).click()
                    page.wait_for_timeout(3000)
                # Manager Type
                if datadictvalue["C_P_PFM_MT"] != '':
                    page.get_by_role("combobox", name="Manager Type").click()
                    page.get_by_text(datadictvalue["C_P_PFM_MT"]).click()
                    page.wait_for_timeout(3000)
                    # page.locator("[id=\"_FOpt1\\:_FOr1\\:0\\:_FONSr2\\:0\\:MAnt2\\:2\\:AP1\\:smc2\\:\\:drop\"]").click()
                    # page.get_by_text("Line Manager").click()
        # Worker can assign participant roles that can view worker and manager evaluations
        if datadictvalue["C_P_PFM_WRK_MGR"] != '':
            if datadictvalue["C_P_PFM_WRK_MGR"] == "No":
                page.get_by_text("Worker can assign participant roles that can view worker and manager evaluations").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_P_PFM_WRK_MGR"] == "Yes":
                page.get_by_text("Worker can assign participant roles that can view worker and manager evaluations").check()
                page.wait_for_timeout(3000)
        # Manager can assign participant roles that can view worker and manager evaluations
        if datadictvalue["C_P_PFM_PRTC_MGR"] != '':
            if datadictvalue["C_P_PFM_PRTC_MGR"] == "No":
                page.get_by_text("Manager can assign participant roles that can view worker and manager evaluations").uncheck()
                page.wait_for_timeout(3000)
            if datadictvalue["C_P_PFM_PRTC_MGR"] == "Yes":
                page.get_by_text("Manager can assign participant roles that can view worker and manager evaluations").check()
                page.wait_for_timeout(3000)
        # Structure
        page.get_by_role("link", name="Structure").click()
        page.wait_for_timeout(3000)

        # Sections
        if datadictvalue["C_S_PT_SEC_NM_1"] != '':
            page.get_by_label("Section Name", exact=True).click()
            page.get_by_title("Search and Select: Section").click()
            page.get_by_text(datadictvalue["C_S_PT_SEC_NM_1"]).click()
            page.wait_for_timeout(3000)
            page.get_by_label("Sequence Number").click()
            page.get_by_label("Sequence Number").fill(datadictvalue["C_S_PT_SEQ_NUM_1"])

            # Processing by Role 1
            if datadictvalue["C_S_PR_SEC1_ROLE1"] != '':
                page.get_by_role("button", name="Add").nth(2)
                page.get_by_role("combobox", name="Role", exact=True).click()
                page.get_by_text(datadictvalue["C_S_PR_SEC1_ROLE1"]).click()
                # Item Ratings
                if datadictvalue["C_S_PR_SEC1_ITRAT_1"] != '':
                    page.get_by_role("combobox", name="Item Ratings").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_ITRAT_1"]).click()
                # Item Comments
                if datadictvalue["C_S_PR_SEC1_ITCMT_1"] != '':
                    page.get_by_role("combobox", name="Item Comments").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_ITCMT_1"]).click()
                # Choose to Evaluate Items
                if datadictvalue["C_S_PR_SEC1_CEI_1"] != '':
                    page.get_by_role("combobox", name="Choose to Evaluate Items").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_CEI_1"]).click()
                # Section Ratings
                if datadictvalue["C_S_PR_SEC1_SERT_1"] != '':
                    page.get_by_role("combobox", name="Section Ratings").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_SERT_1"]).click()
                # Section Comments
                if datadictvalue["C_S_PR_SEC1_SECMT_1"] != '':
                    page.get_by_role("combobox", name="Section Comments").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_SECMT_1"]).click()
                # Share Ratings
                if datadictvalue["C_S_PR_SEC1_SHRT_1"] != '':
                    page.get_by_role("combobox", name="Share Ratings").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_SHRT_1"]).click()
                # Share Comments
                if datadictvalue["C_S_PR_SEC1_SHCMT_1"] != '':
                    page.get_by_role("combobox", name="Share Comments").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_SHCMT_1"]).click()
                # Update Profile
                if datadictvalue["C_S_PR_SEC1_UP_1"] != '':
                    page.get_by_role("combobox", name="Update Profile").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_UP_1"]).click()

                # Instance Qualifier - C_S_PR_SEC1_IQ_1

                # View Participant Names
                if datadictvalue["C_S_PR_SEC1_VPN_1"] != '':
                    page.get_by_role("combobox", name="View Participant Names").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_VPN_1"]).click()

                # View Participant Roles
                if datadictvalue["C_S_PR_SEC1_VPR_1"] != '':
                    page.get_by_role("combobox", name="View Participant Roles").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_VPR_1"]).click()

                # View Manager Questionnaire - C_S_PR_SEC1_VMQ_1

                # View Manager Scores - C_S_PR_SEC1_VMS_1

                # View Worker Questionnaire - C_S_PR_SEC1_VWQ_1

                # View Worker Scores - C_S_PR_SEC1_VWS_1

                # View Participant Questionnaire - C_S_PR_SEC1_VPQ_1

                # View Participant Scores - C_S_PR_SEC1_VPS_1

                # View Own Scores - C_S_PR_SEC1_VOS_1

                # Participant Role Can enter Comments Visible To Worker - C_S_PR_SEC1_PRCVW_1

            # Processing by Role 2
            if datadictvalue["C_S_PR_SEC1_ROLE2"] != '':
                page.get_by_role("button", name="Add").nth(2)
                page.get_by_role("combobox", name="Role", exact=True).click()
                page.get_by_text(datadictvalue["C_S_PR_SEC1_ROLE2"]).click()
                # Item Ratings
                if datadictvalue["C_S_PR_SEC1_ITRAT_2"] != '':
                    page.get_by_role("combobox", name="Item Ratings").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_ITRAT_2"]).click()
                # Item Comments
                if datadictvalue["C_S_PR_SEC1_ITCMT_2"] != '':
                    page.get_by_role("combobox", name="Item Comments").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_ITCMT_2"]).click()
                # Choose to Evaluate Items - C_S_PR_SEC1_CEI_2

                # Section Ratings - C_S_PR_SEC1_SERT_2

                # Section Comments
                if datadictvalue["C_S_PR_SEC1_SECMT_2"] != '':
                    page.get_by_role("combobox", name="Section Comments").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_SECMT_2"]).click()
                # Share Ratings
                if datadictvalue["C_S_PR_SEC1_SHRT_2"] != '':
                    page.get_by_role("combobox", name="Share Ratings").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_SHRT_2"]).click()
                # Share Comments
                if datadictvalue["C_S_PR_SEC1_SHCMT_2"] != '':
                    page.get_by_role("combobox", name="Share Comments").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_SHCMT_2"]).click()
                # Update Profile - C_S_PR_SEC1_UP_2

                # Instance Qualifier - C_S_PR_SEC1_IQ_2

                # View Participant Names - C_S_PR_SEC1_VPN_2

                # View Participant Roles - C_S_PR_SEC1_VPR_2

                # View Manager Questionnaire - C_S_PR_SEC1_VMQ_2

                # View Manager Scores - C_S_PR_SEC1_VMS_2

                # View Worker Questionnaire - C_S_PR_SEC1_VWQ_2

                # View Worker Scores - C_S_PR_SEC1_VWS_2

                # View Participant Questionnaire - C_S_PR_SEC1_VPQ_2

                # View Participant Scores - C_S_PR_SEC1_VPS_2

                # View Own Scores - C_S_PR_SEC1_VOS_2

                # Participant Role Can enter Comments Visible To Worker - C_S_PR_SEC1_PRCVW_2

            # Processing by Role 3
            if datadictvalue["C_S_PR_SEC1_ROLE3"] != '':
                page.get_by_role("button", name="Add").nth(2)
                page.get_by_role("combobox", name="Role", exact=True).click()
                page.get_by_text(datadictvalue["C_S_PR_SEC1_ROLE3"]).click()
                # Item Ratings
                if datadictvalue["C_S_PR_SEC1_ITRAT_3"] != '':
                    page.get_by_role("combobox", name="Item Ratings").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_ITRAT_3"]).click()
                # Item Comments
                if datadictvalue["C_S_PR_SEC1_ITCMT_3"] != '':
                    page.get_by_role("combobox", name="Item Comments").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_ITCMT_3"]).click()

                # Choose to Evaluate Items - C_S_PR_SEC1_CEI_3

                # Section Ratings - C_S_PR_SEC1_SERT_3

                # Section Comments
                if datadictvalue["C_S_PR_SEC1_SECMT_3"] != '':
                    page.get_by_role("combobox", name="Section Comments").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_SECMT_3"]).click()
                # Share Ratings
                if datadictvalue["C_S_PR_SEC1_SHRT_3"] != '':
                    page.get_by_role("combobox", name="Share Ratings").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_SHRT_3"]).click()
                # Share Comments
                if datadictvalue["C_S_PR_SEC1_SHCMT_3"] != '':
                    page.get_by_role("combobox", name="Share Comments").click()
                    page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_S_PR_SEC1_SHCMT_3"]).click()
                # Update Profile - C_S_PR_SEC1_UP_3

                # Instance Qualifier - C_S_PR_SEC1_IQ_3

                # View Participant Names - C_S_PR_SEC1_VPN_3

                # View Participant Roles - C_S_PR_SEC1_VPR_3

                # View Manager Questionnaire - C_S_PR_SEC1_VMQ_3

                # View Manager Scores - C_S_PR_SEC1_VMS_3

                # View Worker Questionnaire - C_S_PR_SEC1_VWQ_3

                # View Worker Scores - C_S_PR_SEC1_VWS_3

                # View Participant Questionnaire - C_S_PR_SEC1_VPQ_3

                # View Participant Scores - C_S_PR_SEC1_VPS_3

                # View Own Scores - C_S_PR_SEC1_VOS_3

                # Participant Role Can enter Comments Visible To Worker - C_S_PR_SEC1_PRCVW_3
        page.pause()
        page.get_by_role("button", name="Cancel").click()
        page.wait_for_timeout(3000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Performance Templates")).to_be_visible()
            print("Performance Templates Saved Successfully")
            datadictvalue["RowStatus"] = "Performance Templates Submitted Successfully"
        except Exception as e:
            print("Performance Templates not saved")
            datadictvalue["RowStatus"] = "Performance Templates not submitted"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, PERFORMANCE_TEMPLATE):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, PERFORMANCE_TEMPLATE, PRCS_DIR_PATH + PERF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PERF_CONFIG_WRKBK, PERFORMANCE_TEMPLATE)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[
            0] + "_" + PERFORMANCE_TEMPLATE + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
