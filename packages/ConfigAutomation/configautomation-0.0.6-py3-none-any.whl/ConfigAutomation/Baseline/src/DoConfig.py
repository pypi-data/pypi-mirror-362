import os

from ConfigAutomation.Baseline.src.utils import *
from ConfigAutomation.Baseline.src.Sheet2ScriptMapping import *

#os.chdir(os.environ['CFGAUTOROOT'])

print('''
    =============================================================================================
    ************************Welcome to Automated Configuration Execution*************************
    Few Points to Note:
    
    1. Configuration Workbook Name should match based on agreed pre-defined names
    2. Configuration Sheet Names should match based on agreed pre-defined names
    3. To know the workbook/sheet names, refer to the file 'ConfigFileNames.py' in src directory
    4. Ensure 'A_TemplateDetails' Tab in the config workbook is updated to have only those 
       sheet names for which configuration has to be performed
    5. The config workbook with the correct name should be placed in the 'src/workbooks/source'
       folder where config automation is installed
    6. When prompted enter the module code for which the configuration has to be performed. The
       module codes are provided for your reference below
    7. For any questions, reach out to the QA team    
    =============================================================================================
    
    Module Codes for Configuration:
    -------------------------------
    ENT - Enterprise Structures
    GL - General Ledger                                  GHR - Global HR
    AP - Accounts Payables                               BEN - Benefits
    AR - Accounts Receivables                            ABS - Absence
    EXP - Expenses                                       PAY - Payroll
    CM - Cash Management                                 RCM - Recruitment
    FA - Fixed Assets                                    OTL - Time and Labor
    PPMF - Projects Foundation                           GLM - Goals Management
    PPMB - Projects Billing                              PRF - Performance Management
    PPMG - Projects & Grants                             LRN - Learn
    PPMO - Projects Organization                         HSF - Health & Safety
                                                         TLCD - Talent Career Development
                                                         ORC - Talent Recruiting
                                                         TLONB - Talent Onboarding
                                                         SEC - Security
                                                         
    ''')
SheetNames = ""
ModOption = input("Enter the module code for which the configuration has to be performed: ")

# Every workbook should correspond to a single option above. The below logic supplies
# the correct workbook name based on the option chosen. Once the workbook is supplied
# the code gets all the sheet names defined in the worbook template details tab.
# For every sheet identified, the code executes the corresponding script that has been
# created.
# Note1: All workbook and sheet names are defined in ConfigFileNames.py script.
# Note2: All sheet to script mapping is defined in Sheet2ScriptMapping.py
# Review the above scripts for accuracy for the logic to work as intended

if ModOption == "GL":
    print("Performing configuration for GL")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + GL_WORKBOOK)
elif ModOption == "ENT":
    print("Performing configuration for Enterprise Structures")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + GHR_ENTSTRUCT_CONFIG_WRKBK)
elif ModOption == "GHR":
    print("Performing configuration for GHR")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + GHR_CONFIG_WRKBK)
elif ModOption == "BEN":
    print("Performing configuration for BEN")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + BENEFITS_CONFIG_WRKBK)
elif ModOption == "AP":
    print("Performing configuration for AP")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + AP_WORKBOOK)
elif ModOption == "AR":
    print("Performing configuration for AR")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + AR_WORKBOOK)
elif ModOption == "CM":
    print("Performing configuration for CM")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + CM_WORKBOOK)
elif ModOption == "EXP":
    print("Performing configuration for EXP")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + EXP_WORKBOOK)
elif ModOption == "OTL":
    print("Performing configuration for OTL")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + HCM_TIME_AND_LABOR_WRKBK)
elif ModOption == "FA":
    print("Performing configuration for FA")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + FA_WORKBOOK)
elif ModOption == "ABS":
    print("Performing configuration for ABS")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + ABSENCE_CONFIG_WRKBK)
elif ModOption == "PAY":
    print("Performing configuration for PAY")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + PAYROLL_SLA_CONFIG_WB)
elif ModOption == "PPMO":
    print("Performing configuration for PPM-Project Organization")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + PPM_ORG_CONFIG_WRKBK)
elif ModOption == "PPMF":
    print("Performing configuration for PPM-Project Organization")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + PPM_PFC_CONFIG_WRKBK)
elif ModOption == "PPMG":
    print("Performing configuration for PPM-Grants")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + PPM_GRNTS_CONFIG_WRKBK)
elif ModOption == "PPMB":
    print("Performing configuration for PPM-Billing")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + PPM_BILLING_CONFIG_WRKBK)
elif ModOption == "TLCD":
    print("Performing configuration for Talent-Career Deveploment")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + MGMT_CONFIG_WRKBK)
elif ModOption == "LRN":
    print("Performing configuration for Talent-Learnings")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + LEARNINGS_CONFIG_WRKBK)
elif ModOption == "GLM":
    print("Performing configuration for Talent-Goals")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + GOAL_CONFIG_WRKBK)
elif ModOption == "PRF":
    print("Performing configuration for Talent-Performance")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + PERF_CONFIG_WRKBK)
elif ModOption == "ORC":
    print("Performing configuration for Talent - ORC")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + Recruiting_CONFIG_WRKBK)
elif ModOption == "TLONB":
    print("Performing configuration for Talent - OnBoarding")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + ONBOARDING_CONFIG_WRKBK)
elif ModOption == "HSF":
    print("Performing configuration for Health & Safety")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + HEAL_SAF_CONFIG_WRKBK)
elif ModOption == "SEC":
    print("Performing configuration Segment Roles")
    SheetNames = GetSheetNames(SOURCE_DIR_PATH + SECURITY_OBJ_GRP_CONFIG_WRKBK)


# Execute the corresponding python script for the sheet name.
if SheetNames != "":
    i = 0
    while i < len(SheetNames):
        print("Executing for Sheet Name - ", SheetNames[i])
        Script = Script2Run[SheetNames[i].strip()].split(";")
        j = 0
        while j < len(Script):
            print("Executing script - ", Script[j].strip())
            exec(open(os.getcwd() + Script[j]).read())
            j = j + 1
        i = i + 1
