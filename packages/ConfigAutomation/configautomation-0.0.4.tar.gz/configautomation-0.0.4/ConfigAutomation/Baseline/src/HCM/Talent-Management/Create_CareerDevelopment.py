from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    # Login to application
    page.get_by_placeholder("User ID").click()
    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(3000)

    # Navigate to Setup and Maintenance
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Settings and Actions").click()
    page.get_by_role("link", name="Setup and Maintenance").click()
    page.get_by_role("link", name="Tasks").click()
    page.wait_for_timeout(3000)
    page.get_by_title("Actions", exact=True).click()
    page.get_by_text("Go to Offerings").click()
    page.wait_for_timeout(6000)
    page.get_by_role("link", name="Workforce Development").click()
    page.get_by_role("button", name="Opt In Features").click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(3000)

        # Career Development
        page.wait_for_timeout(3000)
        page.locator("//span[text()='Career Development']//following::a[@title='Features']").first.click()
        page.wait_for_timeout(3000)
        if datadictvalue["C_CRR_DVLPMNT_APPRVLS"] == "Yes":
            print(datadictvalue["C_CRR_DVLPMNT_APPRVLS"])
            if not page.get_by_role("cell", name="Career Development Approvals").locator("label").is_checked():
                page.get_by_role("cell", name="Career Development Approvals").locator("label").first.click()
                page.wait_for_timeout(5000)
        # Edit
            page.get_by_role("cell", name="Career Development Approval Options").get_by_role("link", name="Features").first.click()
        # Approval required for adding goals
            if datadictvalue["C_APPRVL_RQRD_FOR_ADDNG_GOALS"] == "Yes":
                print(datadictvalue["C_APPRVL_RQRD_FOR_ADDNG_GOALS"])
                if not page.get_by_text("[id=\"__af_Z_window\"]").get_by_text("Approval required for adding goals").is_checked():
                    page.get_by_text("[id=\"__af_Z_window\"]").get_by_text("Approval required for adding goals").click()
                    page.wait_for_timeout(5000)
        # Approval required for changes to key goal fields
            if datadictvalue["C_APPRVL_RQRD_FOR_CHNGS_TO_KEY_GOAL_FLDS"] == "Yes":
                print(datadictvalue["C_APPRVL_RQRD_FOR_CHNGS_TO_KEY_GOAL_FLDS"])
                if not page.get_by_text("[id=\"__af_Z_window\"]").get_by_text("Approval required for changes to key goal fields").is_checked():
                    page.get_by_text("[id=\"__af_Z_window\"]").get_by_text("Approval required for changes to key goal fields").click()
                    page.wait_for_timeout(5000)
        # Approval required for goal completion
            if datadictvalue["C_APPRVL_RQRD_FOR_GOAL_CMPLTN"] == "Yes":
                print(datadictvalue["C_APPRVL_RQRD_FOR_GOAL_CMPLTN"])
                if not page.get_by_text("[id=\"__af_Z_window\"]").get_by_text("Approval required for goal completion").is_checked():
                    page.get_by_text("[id=\"__af_Z_window\"]").get_by_text("Approval required for goal completion").click()
                    page.wait_for_timeout(5000)
            page.get_by_role("button", name="Save and Close").click()

        # Career Development Notifications
        page.wait_for_timeout(3000)
        if datadictvalue["C_CRR_DVLPMNT_NTFCTNS"] == "Yes":
            print(datadictvalue["C_CRR_DVLPMNT_NTFCTNS"])
            if not page.get_by_role("cell", name="Career Development Notifications").locator("label").is_checked():
                page.get_by_role("cell", name="Career Development Notifications").locator("label").first.click()
                page.wait_for_timeout(3000)
            # Edit
            page.get_by_role("cell", name="Career Development Notification Options").get_by_role("link", name="Features").first.click()
            # ALL
            if datadictvalue["C_ALL"] == "Yes":
                print(datadictvalue["C_ALL"])
                if not page.get_by_role("option", name="All", exact=True).is_checked():
                    page.get_by_role("option", name="All", exact=True).click()
                    page.wait_for_timeout(3000)
            # Goals assigned by HR Specialist notification
            if datadictvalue["C_GOAL_ASSGND_BY_HR_SPCLST_NTFCTN"] == "Yes":
                print(datadictvalue["C_GOAL_ASSGND_BY_HR_SPCLST_NTFCTN"])
                if not page.get_by_role("option", name="Goals assigned by HR Specialist notification", exact=True).is_checked():
                    page.get_by_role("option", name="Goals assigned by HR Specialist notification", exact=True).click()
                    page.wait_for_timeout(3000)
            # Goals updated by HR Specialist notification
            if datadictvalue["C_GOAL_UPDTD_BY_HR_SPCLST_NTFCTN"] == "Yes":
                print(datadictvalue["C_GOAL_UPDTD_BY_HR_SPCLST_NTFCTN"])
                if not page.get_by_role("option", name="Goals updated by HR Specialist notification", exact=True).is_checked():
                    page.get_by_role("option", name="Goals updated by HR Specialist notification", exact=True).click()
                    page.wait_for_timeout(3000)
            # Goals deleted by HR Specialist notification
            if datadictvalue["C_GOAL_DLTD_BY_HR_SPCLST_NTFCTN"] == "Yes":
                print(datadictvalue["C_GOAL_DLTD_BY_HR_SPCLST_NTFCTN"])
                if not page.get_by_role("option", name="Goals deleted by HR Specialist notification", exact=True).is_checked():
                    page.get_by_role("option", name="Goals deleted by HR Specialist notification", exact=True).click()
                    page.wait_for_timeout(3000)
            # Goals assigned by managers notification
            if datadictvalue["C_GOAL_ASSGND_BY_MNGRS_NTFCTN"] == "Yes":
                print(datadictvalue["C_GOAL_ASSGND_BY_MNGRS_NTFCTN"])
                if not page.get_by_role("option", name="Goals assigned by managers notification", exact=True).is_checked():
                    page.get_by_role("option", name="Goals assigned by managers notification", exact=True).click()
                    page.wait_for_timeout(3000)
            # Goals created by managers notification
            if datadictvalue["C_GOAL_CRTD_BY_MNGRS_NTFCTN"] == "Yes":
                print(datadictvalue["C_GOAL_CRTD_BY_MNGRS_NTFCTN"])
                if not page.get_by_role("option", name="Goals created by managers notification", exact=True).is_checked():
                    page.get_by_role("option", name="Goals created by managers notification", exact=True).click()
                    page.wait_for_timeout(3000)
            # Completed goals updated by manager notification
            if datadictvalue["C_CMPLTD_GOALS_UPDTD_BY_MNGRS_NTFCTN"] == "Yes":
                print(datadictvalue["C_CMPLTD_GOALS_UPDTD_BY_MNGRS_NTFCTN"])
                if not page.get_by_role("option", name="Completed goals updated by managers notification", exact=True).is_checked():
                    page.get_by_role("option", name="Completed goals updated by managers notification", exact=True).click()
                    page.wait_for_timeout(3000)
            # Goals updated by managers notification
            if datadictvalue["C_GOALS_UPDTD_BY_MNGRS_NTFCTN"] == "Yes":
                print(datadictvalue["C_GOALS_UPDTD_BY_MNGRS_NTFCTN"])
                if not page.get_by_role("option", name="Goals updated by managers notification", exact=True).is_checked():
                    page.get_by_role("option", name="Goals updated by managers notification", exact=True).click()
                    page.wait_for_timeout(3000)
            # Goals shared by managers or colleagues notification
            if datadictvalue["C_GOALS_SHRD_BY_MNGRS_OR_CLLGS_NTFCTN"] == "Yes":
                print(datadictvalue["C_GOALS_SHRD_BY_MNGRS_OR_CLLGS_NTFCTN"])
                if not page.get_by_role("option", name="Goals shared by managers or colleagues notification", exact=True).is_checked():
                    page.get_by_role("option", name="Goals shared by managers or colleagues notification", exact=True).click()
                    page.wait_for_timeout(3000)
            # Goals completed by workers notification
            if datadictvalue["C_GOALS_CMPLTD_BY_WRKRS_NTFCTN"] == "Yes":
                print(datadictvalue["C_GOALS_CMPLTD_BY_WRKRS_NTFCTN"])
                if not page.get_by_role("option", name="Goals completed by workers notification", exact=True).is_checked():
                    page.get_by_role("option", name="Goals completed by workers notification", exact=True).click()
                    page.wait_for_timeout(3000)
            # Assigned goals inactivated by worker notification
            if datadictvalue["C_ASSGND_GOALS_INCTVTD_BY_WRKR_NTFCTN"] == "Yes":
                print(datadictvalue["C_ASSGND_GOALS_INCTVTD_BY_WRKR_NTFCTN"])
                if not page.get_by_role("option", name="Assigned goals inactivated by worker notification", exact=True).is_checked():
                    page.get_by_role("option", name="Assigned goals inactivated by worker notification", exact=True).click()
                    page.wait_for_timeout(3000)
            # Goals deleted by managers notification
            if datadictvalue["C_GOALS_DLTD_BY_MNGRS_NTFCTN"] == "Yes":
                print(datadictvalue["C_GOALS_DLTD_BY_MNGRS_NTFCTN"])
                if not page.get_by_role("option", name="Goals deleted by managers notification", exact=True).is_checked():
                    page.get_by_role("option", name="Goals deleted by managers notification", exact=True).click()
                    page.wait_for_timeout(3000)
            # Assigned goals inactivated by manager notification
            if datadictvalue["C_ASSGND_GOALS_INCTVTD_BY_MNGR_NTFCTN"] == "Yes":
                print(datadictvalue["C_ASSGND_GOALS_INCTVTD_BY_MNGR_NTFCTN"])
                if not page.get_by_role("option", name="Assigned goals inactivated by manager notification", exact=True).is_checked():
                    page.get_by_role("option", name="Assigned goals inactivated by manager notification", exact=True).click()
                    page.wait_for_timeout(3000)
            # Assigned goal deleted by manager notification
            if datadictvalue["C_ASSGND_GOAL_DLTD_BY_MNGR_NTFCTN"] == "Yes":
                print(datadictvalue["C_ASSGND_GOAL_DLTD_BY_MNGR_NTFCTN"])
                if not page.get_by_label("Assigned goals deleted by manager notification").is_checked():
                    page.get_by_label("Assigned goals deleted by manager notification").click()
                    page.wait_for_timeout(3000)
            # Assigned goals deleted by worker notification
            if datadictvalue["C_ASSGND_GOAL_DLTD_BY_WRKR_NTFCTN"] == "Yes":
                print(datadictvalue["C_ASSGND_GOAL_DLTD_BY_WRKR_NTFCTN"])
                if not page.get_by_label("Assigned goals deleted by worker notification").is_checked():
                    page.get_by_label("Assigned goals deleted by worker notification").click()
                    page.wait_for_timeout(3000)
            # Manager creates a note for a worker goals
            if datadictvalue["C_MNGR_CRTS_A_NOTE_FOR_A_WRKR_GOALS"] == "Yes":
                print(datadictvalue["C_MNGR_CRTS_A_NOTE_FOR_A_WRKR_GOALS"])
                if not page.get_by_role("option", name="Completed goals updated by managers notification").is_checked():
                    page.get_by_role("option", name="Completed goals updated by managers notification").click()
                    page.wait_for_timeout(3000)
            # Manager deletes a note for a worker goals
            if datadictvalue["C_MNGR_DLTS_A_NOTE_FOR_A_WRKR_GOALS"] == "Yes":
                print(datadictvalue["C_MNGR_DLTS_A_NOTE_FOR_A_WRKR_GOALS"])
                if not page.get_by_label("Manager creates a note for a worker goals").is_checked():
                    page.get_by_label("Manager deletes a note for a worker goals").click()
                    page.wait_for_timeout(3000)
            # Worker creates a note for a goal
            if datadictvalue["C_WRKR_CRTS_A_NOTE_FOR_A_GOAL"] == "Yes":
                print(datadictvalue["C_WRKR_CRTS_A_NOTE_FOR_A_GOAL"])
                if not page.get_by_label("Worker creates a note for a goal").is_checked():
                    page.get_by_label("Worker creates a note for a goal").click()
                    page.wait_for_timeout(3000)
            # Worker deletes a note for a goal
            if datadictvalue["C_WRKR_DLTS_A_NOTE_FOR_A_GOAL"] == "Yes":
                print(datadictvalue["C_WRKR_DLTS_A_NOTE_FOR_A_GOAL"])
                if not page.get_by_label("Worker deletes a note for a goal").is_checked():
                    page.get_by_label("Worker deletes a note for a goal").click()
                    page.wait_for_timeout(3000)
            # Completed goals updated by worker
            if datadictvalue["C_CMPLTD_GOALS_UPDTD_BY_WRKR"] == "Yes":
                print(datadictvalue["C_CMPLTD_GOALS_UPDTD_BY_WRKR"])
                if not page.get_by_label("Completed goals updated by worker").is_checked():
                    page.get_by_label("Completed goals updated by worker").click()
                    page.wait_for_timeout(3000)
            page.get_by_role("button", name="Save and Close").click()
            page.wait_for_timeout(3000)

        # Completed Goal Edit Option
        page.get_by_role("cell", name="Completed Goal Edit Option").get_by_role("link",name="Features").first.click()
        page.wait_for_timeout(3000)
        if datadictvalue["C_RPN"] == "Yes":
            print(datadictvalue["C_RPN"])
            if not page.locator("[id=\"__af_Z_window\"]").get_by_text("Reopen").is_checked():
                page.locator("[id=\"__af_Z_window\"]").get_by_text("Reopen").click()
                page.wait_for_timeout(3000)
        if datadictvalue["C_ALWYS_OPEN"] == "Yes":
            print(datadictvalue["C_ALWYS_OPEN"])
            if not page.locator("[id=\"__af_Z_window\"]").get_by_text("Always Open").is_checked():
                page.locator("[id=\"__af_Z_window\"]").get_by_text("Always Open").click()
                page.wait_for_timeout(3000)
        if datadictvalue["C_NEVER"] == "Yes":
            print(datadictvalue["C_NEVER"])
            if not page.locator("[id=\"__af_Z_window\"]").get_by_text("Never").is_checked():
                page.locator("[id=\"__af_Z_window\"]").get_by_text("Never").click()
                page.wait_for_timeout(3000)
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        # Development Goal Tasks
        if datadictvalue["C_DVLPMNT_GOAL_TASKS"] == "Yes":
            print(datadictvalue["C_DVLPMNT_GOAL_TASKS"])
            if not page.get_by_role("cell", name="Development Goal Tasks").locator("label").is_checked():
                page.get_by_role("cell", name="Development Goal Tasks").locator("label").first.click()
                page.wait_for_timeout(2000)

        # Development Goals Sharing
        if datadictvalue["C_DVLPMNT_GOALS_SHRNG"] == "Yes":
            print(datadictvalue["C_DVLPMNT_GOALS_SHRNG"])
            if not page.get_by_role("cell", name="Development Goals Sharing").locator("label").is_checked():
                page.get_by_role("cell", name="Development Goals Sharing").locator("label").first.click()
                page.wait_for_timeout(2000)

        # Development Intents
        if datadictvalue["C_DVLPMNT_INTNTS"] == "Yes":
            print(datadictvalue["C_DVLPMNT_INTNTS"])
            if not page.get_by_role("cell", name="Development Intents").locator("label").is_checked():
                page.get_by_role("cell", name="Development Intents").locator("label").first.click()
                page.wait_for_timeout(2000)

        # Favorites
        if datadictvalue["C_FVRTS"] == "Yes":
            print(datadictvalue["C_FVRTS"])
            if not page.get_by_role("cell", name="Favorites").locator("label").is_checked():
                page.get_by_role("cell", name="Favorites").locator("label").first.click()
                page.wait_for_timeout(2000)

        # Goal Library
        page.wait_for_timeout(3000)
        if datadictvalue["C_GOAL_LBRY"] == "Yes":
            print(datadictvalue["C_GOAL_LBRY"])
            if not page.get_by_role("cell", name="Goal Library").locator("label").is_checked():
                page.get_by_role("cell", name="Goal Library").locator("label").first.click()

        # Restrict Library Goal
            if datadictvalue["C_RSTRCT_LBRRY_GOAL"] == "Yes":
                print(datadictvalue["C_RSTRCT_LBRRY_GOAL"])
                if not page.get_by_role("cell", name="Restrict Library Goal").locator("label").is_checked():
                    page.get_by_role("cell", name="Restrict Library Goal").locator("label").first.click()
                    page.wait_for_timeout(2000)

        # Matrix Management
        if datadictvalue["C_MTRX_MNGMNT"] == "Yes":
            print(datadictvalue["C_MTRX_MNGMNT"])
            if not page.get_by_role("cell", name="Matrix Management").locator("label").is_checked():
                page.get_by_role("cell", name="Matrix Management").locator("label").first.click()
                page.wait_for_timeout(2000)

        # Target Outcomes
        if datadictvalue["C_TRGT_OTCMS"] == "Yes":
            print(datadictvalue["C_TRGT_OTCMS"])
            if not page.get_by_role("cell", name="Target Outcomes").locator("label").is_checked():
                page.get_by_role("cell", name="Target Outcomes").locator("label").first.click()
                page.wait_for_timeout(2000)

        # Development Goal Details Drill Down Page
        if datadictvalue["C_DVLPMNT_GOAL_DTLS_DRILL_DOWN_PAGE"] == "Yes":
            print(datadictvalue["C_DVLPMNT_GOAL_DTLS_DRILL_DOWN_PAGE"])
            if not page.get_by_role("cell", name="Development Goal Details Drill Down Page").locator("label").is_checked():
                page.get_by_role("cell", name="Development Goal Details Drill Down Page").locator("label").first.click()
                page.wait_for_timeout(2000)

        # Development Goal Measurement
        if datadictvalue["C_DVLPMNT_GOAL_MSRMNT"] == "Yes":
            print(datadictvalue["C_DVLPMNT_GOAL_MSRMNT"])
            if not page.get_by_role("cell", name="Development Goal Measurement").locator("label").is_checked():
                page.get_by_role("cell", name="Development Goal Measurement").locator("label").first.click()
                page.wait_for_timeout(2000)

        # Delete Development Goals Assigned by HR
        if datadictvalue["C_DLT_DVLPMNT_GOALS_ASSGND_BY_HR"] == "Yes":
            print(datadictvalue["C_DLT_DVLPMNT_GOALS_ASSGND_BY_HR"])
            if not page.get_by_role("cell", name="Delete Development Goals Assigned by HR").locator("label").is_checked():
                page.get_by_role("cell", name="Delete Development Goals Assigned by HR").locator("label").first.click()
                page.wait_for_timeout(2000)

        # Inactivate Development Goals Assigned by HR
        if datadictvalue["C_INCTVT_DVLPMNT_GOALS_ASSGND_BY_HR"] == "Yes":
            print(datadictvalue["C_INCTVT_DVLPMNT_GOALS_ASSGND_BY_HR"])
            if not page.get_by_role("cell", name="Inactivate Development Goals Assigned by HR").locator("label").is_checked():
                page.get_by_role("cell", name="Inactivate Development Goals Assigned by HR").locator("label").first.click()
                page.wait_for_timeout(2000)

        # Development Goal Learning
        if datadictvalue["C_DVLPMNT_GOAL_LRNNG"] == "Yes":
            print(datadictvalue["C_DVLPMNT_GOAL_LRNNG"])
            if not page.get_by_role("cell", name="Development Goal Learning").locator("label").is_checked():
                page.get_by_role("cell", name="Development Goal Learning").locator("label").first.click()
                page.wait_for_timeout(2000)

        # Career Ambassadors
        if datadictvalue["C_CRR_AMBSSDRS"] == "Yes":
            print(datadictvalue["C_CRR_AMBSSDRS"])
            if not page.get_by_role("cell", name="Career Ambassadors").locator("label").is_checked():
                page.get_by_role("cell", name="Career Ambassadors").locator("label").first.click()
                page.wait_for_timeout(2000)

        # Development Goal Notes
        if datadictvalue["C_DVLPMNT_GOAL_NOTES"] == "Yes":
            print(datadictvalue["C_DVLPMNT_GOAL_NOTES"])
            if not page.get_by_role("cell", name="Development Goal Notes").locator("label").is_checked():
                page.get_by_role("cell", name="Development Goal Notes").locator("label").first.click()
                page.wait_for_timeout(2000)

        page.get_by_role("button", name="Done").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Done").click()

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Career Development")).to_be_visible()
            print("Career Development Saved Successfully")
            datadictvalue["RowStatus"] = "Career Development Submitted Successfully"
        except Exception as e:
            print("Career Development not saved")
            datadictvalue["RowStatus"] = "Career Development not submitted"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + MGMT_CONFIG_WRKBK, CAREER_DEV):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + MGMT_CONFIG_WRKBK, CAREER_DEV, PRCS_DIR_PATH + MGMT_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + MGMT_CONFIG_WRKBK, CAREER_DEV)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk,VIDEO_DIR_PATH + re.split(".xlsx", MGMT_CONFIG_WRKBK)[0] + "_" + CAREER_DEV)
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", MGMT_CONFIG_WRKBK)[0] + "_" + CAREER_DEV + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
