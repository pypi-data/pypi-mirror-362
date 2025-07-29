from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)

    page.get_by_placeholder("User ID").fill(IMPLUSRID)
    page.get_by_placeholder("Password").fill(IMPLUSRPWD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(4000)
    page.get_by_role("link", name="Home", exact=True).click()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Navigator").click()
    page.get_by_title("My Client Groups", exact=True).click()
    page.get_by_role("link", name="Performance").click()
    page.wait_for_timeout(2000)
    page.get_by_role("link", name="Performance Process Flows").click()
    page.wait_for_timeout(5000)
    i = 1
    while i < rowcount:
        datadictvalue = datadict[i]

        # Click on Add Button
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)

        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(datadictvalue["C_NAME"])
        page.wait_for_timeout(1000)
        #page.get_by_label("Description").fill(datadictvalue["C_PFM_PF_DSCPT"])
        #page.wait_for_timeout(1000)
        page.get_by_placeholder("m/d/yy").first.click()
        page.get_by_placeholder("m/d/yy").first.fill("")
        page.get_by_placeholder("m/d/yy").first.fill(datadictvalue["C_FROM_DATE"])
        page.wait_for_timeout(1000)
        page.get_by_placeholder("m/d/yy").nth(1).click()
        page.get_by_placeholder("m/d/yy").nth(1).fill("")
        page.get_by_placeholder("m/d/yy").nth(1).fill(datadictvalue["C_TO_DATE"])
        page.wait_for_timeout(1000)
        page.get_by_role("combobox", name="Status").click()
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()
        page.wait_for_timeout(1000)

        page.get_by_role("link", name="Tasks").click()
        page.wait_for_timeout(4000)

        #Worker Self-Evaluation and Manager Evaluation
        if datadictvalue["C_INCD_WRKR_SELF_EVLTN_OF_WRKR_TASK"] == "Yes":
            page.get_by_text("Include worker self-evaluation task").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_INCD_MNGR_EVLTN_OF_WRKR_TASK"] == "Yes":
            page.get_by_text("Include manager evaluation of worker task").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_DO_NOT_ALLOW_ADDTNL_EDIT_MNGR_TASK_WHEN_CMPLTD"] == "Yes":
            page.get_by_text("Don't allow additional edit of manager evaluation task when completed").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_EVLTN_TASKS_CAN_BE_PRFRMD_CNCRRNTLY"] == "Yes":
            page.get_by_text("Evaluation tasks can be performed concurrently").nth(1).check()
            page.wait_for_timeout(1000)

        #Participant Feedback
        if datadictvalue["C_INCLD_MNG_PRTCPNT_FDBCK_TASK"] == "Yes":
            page.get_by_text("Include manage participant feedback task").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_MNGR_CAN_SLCT_PRTCPNT"] == "Yes":
            page.get_by_text("Manager can select participant").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_MNGR_CAN_ADD_QSTNS"] == "Yes":
            page.get_by_text("Manager can add questions").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_MNGR_CAN_TRCK_PRTCPNTS"] == "Yes":
            page.get_by_text("Manager can track participants").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_MNGR_CAN_RPN_SBMTTD_FDBCK"] == "Yes":
            page.get_by_text("Manager can reopen submitted feedback").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_PRTCPNT_CAN_RPN_SBMTTD_FDBCK"] == "Yes":
            page.get_by_text("Participant can reopen submitted feedback").check()
            page.wait_for_timeout(1000)

        if datadictvalue["C_WRKR_CAN_SLCT_PRTCPNTS"] == "Yes":
            page.get_by_text("Worker can select participants").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_WRKR_CAN_ADD_QSTNS"] == "Yes":
            page.get_by_text("Worker can add questions").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_WRKR_CAN_RQST_FDBCK"] == "Yes":
            page.get_by_text("Worker can request feedback").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_WRKR_CAN_TRACK_PRTCPNT_FDBCK_STTS"] == "Yes":
            page.get_by_text("Worker can track participant feedback status").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_WRKR_CAN_VIEW_FDBCK_BFR_MNGR_EVLTN_IS_VSBL"] == "Yes":
            page.get_by_text("Worker can view feedback before evaluations are complete").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_WRKR_CAN_RPN_SBMTTD_FDBCK"] == "Yes":
            page.get_by_text("Worker can reopen submitted feedback").check()
            page.wait_for_timeout(1000)

        #Approval, Review and Meetings
        if datadictvalue["C_INCLD_APPRVL_PRCSSNG_TASK"] == "Yes":
            page.get_by_text("Include approval processing task").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_INCLD_SCND_APPRVL_PRCSSNG_TASK"] == "Yes":
            page.get_by_text("Include second approval processing task").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_ATMTCLLY_SBMT_APPRVLS_WHEN_PRCDNG_TASK_IS_CMPLTD"] == "Yes":
            page.get_by_text("Automatically submit approvals when preceding task is completed").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_INCLD_DCMNT_SHRNG_TASK"] == "Yes":
            page.get_by_text("Include document sharing task").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_ALLW_DCMNT_SHRNG_TASK_TO_BE_LCKD_FOR_CLBRTN"] == "Yes":
            page.get_by_text("Allow document sharing task to be locked for calibration").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_WRKR_MUST_ACKNWLDG_DCMNT"] == "Yes":
            page.get_by_text("Worker must acknowledge document").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_INCLD_RVW_MTNG_TASK"] == "Yes":
            page.get_by_text("Include review meeting task").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_WRKR_MUST_ACKNWLDG_RVW_MTNG"] == "Yes":
            page.get_by_text("Worker must acknowledge review meeting").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_INCLD_WRKR_PRVD_FINAL_FDBCK_TASK"] == "Yes":
            page.get_by_text("Include worker provide final feedback task").check()
            page.wait_for_timeout(1000)
        if datadictvalue["C_INCLD_MNGR_PRVD_FINAL_FDBCK_TASK"] == "Yes":
            page.get_by_text("Include manager provide final feedback task").check()
            page.wait_for_timeout(1000)

        #Task Sequence and Names
        page.get_by_role("link", name="Task Names").click()
        page.wait_for_timeout(4000)

        #Worker Self-Evaluation
        if datadictvalue["C_SQNC_NMBR_1"] != "No":
            page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Sequence Number").click()
            page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Sequence Number").fill("")
            page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Sequence Number").type(str(datadictvalue["C_SQNC_NMBR_1"]))
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_1"] != "No":
            page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Task Name for Manager Role").click()
            page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Task Name for Manager Role").fill("")
            page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Task Name for Manager Role").type(datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_1"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_1"] != "No":
            page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Task Name for Worker Role").click()
            page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Task Name for Worker Role").fill("")
            page.get_by_role("row", name="Worker Self-Evaluation").get_by_label("Task Name for Worker Role").type(datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_1"])
            page.wait_for_timeout(1000)

        #Manager Evaluation of Workers
        if datadictvalue["C_SQNC_NMBR_2"] != "No":
            page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Sequence Number").click()
            page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Sequence Number").fill("")
            page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Sequence Number").type(str(datadictvalue["C_SQNC_NMBR_2"]))
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_2"] != "No":
            page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Task Name for Manager Role").click()
            page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Task Name for Manager Role").fill("")
            page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Task Name for Manager Role").type(datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_2"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_2"] != "No":
            page.pause()
            page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Task Name for Worker Role").click()
            page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Task Name for Worker Role").fill("")
            page.get_by_role("row", name="Manager Evaluation of Workers").get_by_label("Task Name for Worker Role").type(datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_2"])
            page.wait_for_timeout(1000)

        #Manage Participant Feedback
        if datadictvalue["C_SQNC_NMBR_3"] != "No":
            page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Sequence Number").click()
            page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Sequence Number").fill("")
            page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Sequence Number").type(str(datadictvalue["C_SQNC_NMBR_3"]))
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_3"] != "No":
            page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Task Name for Manager Role").click()
            page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Task Name for Manager Role").fill("")
            page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Task Name for Manager Role").type(datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_3"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_3"] != "No":
            page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Task Name for Worker Role").click()
            page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Task Name for Worker Role").fill("")
            page.get_by_role("row", name="Manage Participant Feedback").get_by_label("Task Name for Worker Role").type(datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_3"])
            page.wait_for_timeout(1000)

        #First Approval
        if datadictvalue["C_SQNC_NMBR_4"] != "No":
            page.get_by_role("row", name="First Approval").get_by_label("Sequence Number").click()
            page.get_by_role("row", name="First Approval").get_by_label("Sequence Number").fill("")
            page.get_by_role("row", name="First Approval").get_by_label("Sequence Number").type(str(datadictvalue["C_SQNC_NMBR_4"]))
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_4"] != "No":
            page.get_by_role("row", name="First Approval").get_by_label("Task Name for Manager Role").click()
            page.get_by_role("row", name="First Approval").get_by_label("Task Name for Manager Role").fill("")
            page.get_by_role("row", name="First Approval").get_by_label("Task Name for Manager Role").type(datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_4"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_4"] != "No":
            page.get_by_role("row", name="First Approval").get_by_label("Task Name for Worker Role").click()
            page.get_by_role("row", name="First Approval").get_by_label("Task Name for Worker Role").fill("")
            page.get_by_role("row", name="First Approval").get_by_label("Task Name for Worker Role").type(datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_4"])
            page.wait_for_timeout(1000)

        # Second Approval
        if datadictvalue["C_SQNC_NMBR_8"] != "No":
            page.get_by_role("row", name="Second Approval").get_by_label("Sequence Number").click()
            page.get_by_role("row", name="Second Approval").get_by_label("Sequence Number").fill("")
            page.get_by_role("row", name="Second Approval").get_by_label("Sequence Number").type(str(datadictvalue["C_SQNC_NMBR_8"]))
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_8"] != "No":
            page.get_by_role("row", name="Second Approval").get_by_label("Task Name for Manager Role").click()
            page.get_by_role("row", name="Second Approval").get_by_label("Task Name for Manager Role").fill("")
            page.get_by_role("row", name="Second Approval").get_by_label("Task Name for Manager Role").type(datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_8"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_8"] != "No":
            page.get_by_role("row", name="Second Approval").get_by_label("Task Name for Worker Role").click()
            page.get_by_role("row", name="Second Approval").get_by_label("Task Name for Worker Role").fill("")
            page.get_by_role("row", name="Second Approval").get_by_label("Task Name for Worker Role").type(datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_8"])
            page.wait_for_timeout(1000)

        #Share Performance Document
        if datadictvalue["C_SQNC_NMBR_5"] != "No":
            page.get_by_role("row", name="Share Performance Document").get_by_label("Sequence Number").click()
            page.get_by_role("row", name="Share Performance Document").get_by_label("Sequence Number").fill("")
            page.get_by_role("row", name="Share Performance Document").get_by_label("Sequence Number").type(str(datadictvalue["C_SQNC_NMBR_5"]))
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_5"] != "No":
            page.get_by_role("row", name="Share Performance Document").get_by_label("Task Name for Manager Role").click()
            page.get_by_role("row", name="Share Performance Document").get_by_label("Task Name for Manager Role").fill("")
            page.get_by_role("row", name="Share Performance Document").get_by_label("Task Name for Manager Role").type(datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_5"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_5"] != "No":
            page.get_by_role("row", name="Share Performance Document").get_by_label("Task Name for Worker Role").click()
            page.get_by_role("row", name="Share Performance Document").get_by_label("Task Name for Worker Role").fill("")
            page.get_by_role("row", name="Share Performance Document").get_by_label("Task Name for Worker Role").type(datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_5"])
            page.wait_for_timeout(1000)

        #Confirm Review Meeting Held
        if datadictvalue["C_SQNC_NMBR_6"] != "No":
            page.get_by_role("row", name="Confirm Review Meeting Held").get_by_label("Sequence Number").click()
            page.get_by_role("row", name="Confirm Review Meeting Held").get_by_label("Sequence Number").fill("")
            page.get_by_role("row", name="Confirm Review Meeting Held").get_by_label("Sequence Number").type(str(datadictvalue["C_SQNC_NMBR_6"]))
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_6"] != "No":
            page.get_by_role("row", name="Confirm Review Meeting Held").get_by_label("Task Name for Manager Role").click()
            page.get_by_role("row", name="Confirm Review Meeting Held").get_by_label("Task Name for Manager Role").fill("")
            page.get_by_role("row", name="Confirm Review Meeting Held").get_by_label("Task Name for Manager Role").type(datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_6"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_6"] != "No":
            page.get_by_role("row", name="Confirm Review Meeting Held").get_by_label("Task Name for Worker Role").click()
            page.get_by_role("row", name="Confirm Review Meeting Held").get_by_label("Task Name for Worker Role").fill("")
            page.get_by_role("row", name="Confirm Review Meeting Held").get_by_label("Task Name for Worker Role").type(datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_6"])
            page.wait_for_timeout(1000)

        #Provide Final Feedback
        if datadictvalue["C_SQNC_NMBR_7"] != "No":
            page.get_by_role("row", name="Provide Final Feedback").get_by_label("Sequence Number").click()
            page.get_by_role("row", name="Provide Final Feedback").get_by_label("Sequence Number").fill("")
            page.get_by_role("row", name="Provide Final Feedback").get_by_label("Sequence Number").type(str(datadictvalue["C_SQNC_NMBR_7"]))
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_7"] != "No":
            page.get_by_role("row", name="Provide Final Feedback").get_by_label("Task Name for Manager Role").click()
            page.get_by_role("row", name="Provide Final Feedback").get_by_label("Task Name for Manager Role").fill("")
            page.get_by_role("row", name="Provide Final Feedback").get_by_label("Task Name for Manager Role").type(datadictvalue["C_TASK_NAME_FOR_MNGR_ROLE_7"])
            page.wait_for_timeout(1000)
        if datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_7"] != "No":
            page.get_by_role("row", name="Provide Final Feedback").get_by_label("Task Name for Worker Role").click()
            page.get_by_role("row", name="Provide Final Feedback").get_by_label("Task Name for Worker Role").fill("")
            page.get_by_role("row", name="Provide Final Feedback").get_by_label("Task Name for Worker Role").type(datadictvalue["C_TASK_NAME_FOR_WRKR_ROLE_7"])
            page.wait_for_timeout(1000)

        page.get_by_role("button", name="Save and Close").click()
        page.pause()
        page.wait_for_timeout(7000)

        i = i + 1

        try:
            expect(page.get_by_role("heading", name="Performance Process Flows")).to_be_visible()
            print("Performance Process Flows Saved Successfully")
            datadictvalue["RowStatus"] = "Performance Process Flows Submitted Successfully"
        except Exception as e:
            print("Review Periods not saved")
            datadictvalue["RowStatus"] = "Performance Process Flows not submitted"

    OraSignOut(page, context, browser, videodir)
    return datadict


# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, PERFORMANCE_PROCESS_FLOW):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK, PERFORMANCE_PROCESS_FLOW, PRCS_DIR_PATH + PERF_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + PERF_CONFIG_WRKBK, PERFORMANCE_PROCESS_FLOW)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0])
        write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", PERF_CONFIG_WRKBK)[0] + "_" + PERFORMANCE_PROCESS_FLOW + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
