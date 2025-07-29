
from playwright.sync_api import Playwright, sync_playwright, expect
from ConfigAutomation.Baseline.src.utils import *


def configure(playwright: Playwright, rowcount, datadict, videodir) -> dict:
    browser, context, page = OpenBrowser(playwright, False, videodir)
    page.goto(BASEURL)
    page.get_by_placeholder("User ID").click()
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
    page.get_by_role("textbox").type("Checklist Templates")
    page.get_by_role("textbox").press("Enter")
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Checklist Templates", exact=True).click()

    i = 0
    while i < rowcount:
        datadictvalue = datadict[i]
        page.wait_for_timeout(5000)

        # Clicking on Create Button
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(5000)

        # Adding Name
        page.get_by_label("Name", exact=True).clear()
        page.get_by_label("Name", exact=True).type(datadictvalue["C_NAME"])

        # Adding Checklist
        page.get_by_label("Checklist Code").click()
        page.wait_for_timeout(3000)
        page.get_by_label("Checklist Code").clear()
        page.get_by_label("Checklist Code").type(datadictvalue["C_CHCKLST_CODE"])

        # Adding Country
        page.get_by_title("Search: Country").click()
        page.wait_for_timeout(2000)
        page.get_by_text(datadictvalue["C_CNTRS"],exact=True).click()

        # Adding Category
        page.get_by_role("combobox", name="Category").click()
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_CTGRY"]).click()

        # Archive After Months
        page.get_by_label("Archive After Months").clear()
        page.get_by_label("Archive After Months").type(str(datadictvalue["C_ARCHV_AFTER_MNTHS"]))

        # Purge After Months
        page.get_by_label("Purge After Months").clear()
        page.get_by_label("Purge After Months").type(str(datadictvalue["C_PURGE_AFTER_MNTHS"]))

        # Clicking on OK button
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(3000)

        # Status
        page.get_by_role("combobox", name="Status").click()
        page.wait_for_timeout(2000)
        page.get_by_text(datadictvalue["C_STTS"], exact=True).click()

        # Description
        if datadictvalue["C_DSCRPTN"]!='':
            page.get_by_label("Description").clear()
            page.get_by_label("Description").type(datadictvalue["C_DSCRPTN"])

        # Date From
        page.locator("(//label[text()='Date From']//following::input[1])[1]").clear()
        page.locator("(//label[text()='Date From']//following::input[1])[1]").type(datadictvalue["C_DATE_FROM"].strftime("%m/%d/%Y"))

        # Date To
        if datadictvalue["C_DATE_TO"]!='':
            page.locator("(//label[text()='Date To']//following::input[1])[1]").clear()
            page.locator("(//label[text()='Date To']//following::input[1])[1]").type(datadictvalue["C_DATE_TO"].strftime("%m/%d/%Y"))

        # Eligibility Profile
        page.get_by_title("Search: Eligibility Profile").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(2000)
        page.locator("//div[text()='Search and Select: Eligibility Profile']//following::label[text()='Name']//following::input[1]").clear()
        page.locator("//div[text()='Search and Select: Eligibility Profile']//following::label[text()='Name']//following::input[1]").type(datadictvalue["C_ELGBLTY_PRFL"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_ELGBLTY_PRFL"], exact=True).click()
        page.get_by_role("button", name="OK").click()

        # Allocation Criteria
        page.get_by_role("combobox", name="Allocation Criteria").click()
        page.wait_for_timeout(2000)
        page.get_by_text(datadictvalue["C_ALLCTN_CRTR"],exact=True).click()

        # Completion Criteria
        page.get_by_role("combobox", name="Completion Criteria").click()
        page.wait_for_timeout(2000)
        page.get_by_text(datadictvalue["C_CMPLTN_CRTR"],exact=True).click()

        # Click on Save button
        page.get_by_role("button", name="Save", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="OK").click()

        # Clicking on Task Tab
        page.get_by_role("link", name="Tasks").click()
        page.wait_for_timeout(2000)

        # Adding Task Details
        page.get_by_role("button", name="Create").click()
        page.get_by_text("Create Task", exact=True).click()
        page.wait_for_timeout(2000)

        ## Task Name
        page.get_by_label("Name", exact=True).type(datadictvalue["C_TASK_NAME"])

        ## Sequence
        page.get_by_label("Sequence").clear()
        page.get_by_label("Sequence").type(str(datadictvalue["C_TASK_SQNC"]))

        ## Required
        if datadictvalue["C_TASK_RQRD"]=='Yes':
            page.locator("//label[text()='Required']//following::label[1]").check()
        if datadictvalue["C_TASK_RQRD"]=='No':
            page.locator("//label[text()='Required']//following::label[1]").uncheck()

        ## Code
        page.get_by_label("Code", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_label("Code", exact=True).clear()
        page.get_by_label("Code", exact=True).type(datadictvalue["C_TASK_CODE"])

        ## Status
        page.get_by_role("combobox", name="Status").click()
        page.wait_for_timeout(2000)
        page.get_by_text(datadictvalue["C_TASK_STTS"], exact=True).click()

        ## Task Description
        page.get_by_label("Description").clear()
        page.get_by_label("Description").fill(datadictvalue["C_TASK_DSCRPTN"])

        ## Expire
        page.get_by_label("Expire").click()
        page.get_by_label("Expire").type(str(datadictvalue["C_EXPRD"]))

        ## Days
        page.get_by_role("combobox", name="Days").click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_DAYS"], exact=True).click()

        ## Performer
        page.get_by_role("combobox", name="Performer", exact=True).click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_PRFRMR"], exact=True).click()

        ## Owner
        page.get_by_role("combobox", name="Owner", exact=True).click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_OWNER"], exact=True).click()

        ## Task Type
        page.get_by_role("combobox", name="Task Type").click()
        page.wait_for_timeout(2000)
        page.locator("[id=\"__af_Z_window\"]").get_by_text(datadictvalue["C_TASK_TYPE"], exact=True).click()
        page.wait_for_timeout(2000)

        ## Saving Task Details
        page.get_by_title("Save and Close").click()
        page.get_by_text("Save", exact=True).click()
        page.wait_for_timeout(4000)
        page.get_by_role("button", name="OK").click()
        page.wait_for_timeout(2000)

        # Notification and Reminders
        page.get_by_role("link", name="Notification and Reminders").click()
        page.wait_for_timeout(2000)

        ## When task is assigned or reassigned
        if datadictvalue["C_WHEN_TASK_IS_ASSGND_OR_RSSGND"]!='NA':
            if datadictvalue["C_WHEN_TASK_IS_ASSGND_OR_RSSGND"]=='Performer':
                page.get_by_role("row", name="When task is assigned or").locator("label").nth(1).check()
            if datadictvalue["C_WHEN_TASK_IS_ASSGND_OR_RSSGND"]=='Owner':
                page.get_by_role("row", name="When task is assigned or").locator("label").first.check()
            if datadictvalue["C_WHEN_TASK_IS_ASSGND_OR_RSSGND"] == 'Owner-Performer':
                page.get_by_role("row", name="When task is assigned or").locator("label").first.check()
                page.get_by_role("row", name="When task is assigned or").locator("label").nth(1).check()

        ## When task is completed
        if datadictvalue["C_WHEN_TASK_IS_CMPLTD"]!='NA':
            if datadictvalue["C_WHEN_TASK_IS_CMPLTD"] == 'Owner-Performer':
                page.get_by_role("row", name="When task is completed").locator("label").first.check()
                page.get_by_role("row", name="When task is completed").locator("label").nth(1).check()
            if datadictvalue["C_WHEN_TASK_IS_CMPLTD"] == 'Owner':
                page.get_by_role("row", name="When task is completed").locator("label").first.check()
            if datadictvalue["C_WHEN_TASK_IS_CMPLTD"] == 'Performer':
                page.get_by_role("row", name="When task is completed").locator("label").nth(1).check()

        ## When task is unassigned
        if datadictvalue["C_WHEN_TASK_IS_UNSSGND"]!='NA':
            if datadictvalue["C_WHEN_TASK_IS_UNSSGND"] == 'Performer':
                page.get_by_role("row", name="When task is unassigned").locator("label").nth(1).check()
            if datadictvalue["C_WHEN_TASK_IS_UNSSGND"] == 'Owner':
                page.get_by_role("row", name="When task is unassigned").locator("label").first.check()
            if datadictvalue["C_WHEN_TASK_IS_UNSSGND"] == 'Owner-Performer':
                page.get_by_role("row", name="When task is unassigned").locator("label").first.check()
                page.get_by_role("row", name="When task is unassigned").locator("label").nth(1).check()


        ## When task is updated
        if datadictvalue["C_WHEN_TASK_IS_UPDTD"]!='N/A':
            if datadictvalue["C_WHEN_TASK_IS_UPDTD"] == 'Performer':
                page.get_by_role("row", name="When task is updated").locator("label").nth(1).check()
            if datadictvalue["C_WHEN_TASK_IS_UPDTD"] == 'Owner':
                page.get_by_role("row", name="When task is updated").locator("label").first.check()
            if datadictvalue["C_WHEN_TASK_IS_UPDTD"] == 'Owner-Performer':
                page.get_by_role("row", name="When task is updated").locator("label").first.check()
                page.get_by_role("row", name="When task is updated").locator("label").nth(1).check()

        page.wait_for_timeout(10000)

        ## Save and Close Details
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        # Click on Actions and Events tab
        page.get_by_role("link", name="Actions and Events").click()

        ## Click on Add button
        page.get_by_role("button", name="Add").first.click()
        page.wait_for_timeout(3000)

        ## Active
        if datadictvalue["C_ACTV"]!='NA':
            if datadictvalue["C_ACTV"]=='Yes':
                page.get_by_role("row", name="Name Search: Name").locator("label").first.check()
            if datadictvalue["C_ACTV"]=='No':
                page.get_by_role("row", name="Name Search: Name").locator("label").first.uncheck()


        ## Action Name
        page.get_by_title("Search: Name").click()
        page.get_by_role("link", name="Search...").click()
        page.wait_for_timeout(2000)
        page.get_by_label("Action Name").clear()
        page.get_by_label("Action Name").type(datadictvalue["C_ACTN_NAME"])
        page.get_by_role("button", name="Search", exact=True).click()
        page.wait_for_timeout(3000)
        page.get_by_text(datadictvalue["C_ACTN_NAME"], exact=True).click()
        page.get_by_role("button", name="OK").click()

        ## Action Reason
        if datadictvalue["C_ACTN_RSN"]!='NA':
            page.get_by_title("Search: Reason").click()
            page.get_by_role("link", name="Search...").click()
            page.wait_for_timeout(2000)
            page.get_by_label("Action Reason").clear()
            page.get_by_label("Action Reason").type(datadictvalue["C_ACTN_RSN"])
            page.get_by_role("button", name="Search", exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_text(datadictvalue["C_ACTN_RSN"], exact=True).click()
            page.get_by_role("button", name="OK").click()

        # Save and Close
        page.get_by_role("button", name="Save and Close").click()
        page.wait_for_timeout(3000)

        try:
            expect(page.get_by_role("heading", name="Checklist Templates")).to_be_visible()
            print("Manage Journey Configurations Saved Successfully")
            datadictvalue["RowStatus"] = "Manage Journey Configurations Saved"
        except Exception as e:
            print("Unable to save Manage Journey Configurations")
            datadictvalue["RowStatus"] = "Unable to save Manage Journey Configurations"

        print("Row Added - ", str(i))
        datadictvalue["RowStatus"] = "Manage Journey Configurations Added Successfully"
        i = i + 1

    OraSignOut(page, context, browser, videodir)
    return datadict

# ****** Execution Starts Here ******
print("Process Started At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
if CheckWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_JOURNY_CONFIG):
    CreateWrkbkForProcessing(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_JOURNY_CONFIG, PRCS_DIR_PATH + GHR_CONFIG_WRKBK)
    rows, cols, datadictwrkbk = ImportWrkbk(PRCS_DIR_PATH + GHR_CONFIG_WRKBK, MANAGE_JOURNY_CONFIG)
    if rows > 0:
        with sync_playwright() as pw:
            output = configure(pw, rows, datadictwrkbk, VIDEO_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0]+ "_" + MANAGE_JOURNY_CONFIG)
            write_status(output, RESULTS_DIR_PATH + re.split(".xlsx", GHR_CONFIG_WRKBK)[0] + "_" + MANAGE_JOURNY_CONFIG + "_Results_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    else:
        print("No data rows to process. Check the source workbook to ensure it is valid!")
print("Process Ended At - ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))






