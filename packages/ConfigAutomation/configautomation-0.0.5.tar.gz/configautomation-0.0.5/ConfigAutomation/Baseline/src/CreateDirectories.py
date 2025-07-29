import os

os.chdir(os.environ['CFGAUTOROOT'])

#Base Directories
if not os.path.exists("workbooks"):
    os.mkdir("workbooks")
    print("Directory 'workbooks' created")
if not os.path.exists("results"):
    os.mkdir("results")
    print("Directory 'results' created")
if not os.path.exists("videos"):
    os.mkdir("videos")
    print("Directory 'videos' created")

#Source/Processing Directories
if not os.path.exists("workbooks/source"):
    os.mkdir("workbooks/source")
    print("Directory 'workbooks/source' created")
if not os.path.exists("workbooks/formatted"):
    os.mkdir("workbooks/formatted")
    print("Directory 'workbooks/formatted' created")
    
#Pillar Level Directories for ERP and HCM
if not os.path.exists("workbooks/source/ERP"):
    os.mkdir("workbooks/source/ERP")
    print("Directory 'workbooks/source/ERP' created")
if not os.path.exists("workbooks/formatted/ERP"):
    os.mkdir("workbooks/formatted/ERP")
    print("Directory 'workbooks/formatted/ERP' created")
if not os.path.exists("results/ERP"):
    os.mkdir("results/ERP")
    print("Directory 'results/ERP' created")
if not os.path.exists("videos/ERP"):
    os.mkdir("videos/ERP")
    print("Directory 'videos/ERP' created")

if not os.path.exists("workbooks/source/HCM"):
    os.mkdir("workbooks/source/HCM")
    print("Directory 'workbooks/source/HCM' created")
if not os.path.exists("workbooks/formatted/HCM"):
    os.mkdir("workbooks/formatted/HCM")
    print("Directory 'workbooks/formatted/HCM' created")
if not os.path.exists("results/HCM"):
    os.mkdir("results/HCM")
    print("Directory 'results/HCM' created")
if not os.path.exists("videos/HCM"):
    os.mkdir("videos/HCM")
    print("Directory 'videos/HCM' created")
    
#Module Level Directories
#General Ledger
if not os.path.exists("workbooks/source/ERP/GL"):
    os.mkdir("workbooks/source/ERP/GL")
    print("Directory 'workbooks/source/ERP/GL' created")
if not os.path.exists("workbooks/formatted/ERP/GL"):
    os.mkdir("workbooks/formatted/ERP/GL")
    print("Directory 'workbooks/formatted/ERP/GL' created")
if not os.path.exists("results/ERP/GL"):
    os.mkdir("results/ERP/GL")
    print("Directory 'results/ERP/GL' created")
if not os.path.exists("videos/ERP/GL"):
    os.mkdir("videos/ERP/GL")
    print("Directory 'videos/ERP/GL' created")

#Global HR
if not os.path.exists("workbooks/source/HCM/GHR"):
    os.mkdir("workbooks/source/HCM/GHR")
    print("Directory 'workbooks/source/HCM/GHR' created")
if not os.path.exists("workbooks/formatted/HCM/GHR"):
    os.mkdir("workbooks/formatted/HCM/GHR")
    print("Directory 'workbooks/formatted/HCM/GHR' created")
if not os.path.exists("results/HCM/GHR"):
    os.mkdir("results/HCM/GHR")
    print("Directory 'results/HCM/GHR' created")
if not os.path.exists("videos/HCM/GHR"):
    os.mkdir("videos/HCM/GHR")
    print("Directory 'videos/HCM/GHR' created")

#Payroll
if not os.path.exists("workbooks/source/HCM/Payroll"):
    os.mkdir("workbooks/source/HCM/Payroll")
    print("Directory 'workbooks/source/HCM/Payroll' created")
if not os.path.exists("workbooks/formatted/HCM/Payroll"):
    os.mkdir("workbooks/formatted/HCM/Payroll")
    print("Directory 'workbooks/formatted/HCM/Payroll' created")
if not os.path.exists("results/HCM/Payroll"):
    os.mkdir("results/HCM/Payroll")
    print("Directory 'results/HCM/Payroll' created")
if not os.path.exists("videos/HCM/Payroll"):
    os.mkdir("videos/HCM/Payroll")
    print("Directory 'videos/HCM/Payroll' created")

#Benefits
if not os.path.exists("workbooks/source/HCM/Benefits"):
    os.mkdir("workbooks/source/HCM/Benefits")
    print("Directory 'workbooks/source/HCM/Benefits' created")
if not os.path.exists("workbooks/formatted/HCM/Benefits"):
    os.mkdir("workbooks/formatted/HCM/Benefits")
    print("Directory 'workbooks/formatted/HCM/Benefits' created")
if not os.path.exists("results/HCM/Benefits"):
    os.mkdir("results/HCM/Benefits")
    print("Directory 'results/HCM/Benefits' created")
if not os.path.exists("videos/HCM/Benefits"):
    os.mkdir("videos/HCM/Benefits")
    print("Directory 'videos/HCM/Benefits' created")


#Talent
if not os.path.exists("workbooks/source/HCM/Talent"):
    os.mkdir("workbooks/source/HCM/Talent")
    print("Directory 'workbooks/source/HCM/Talent' created")
if not os.path.exists("workbooks/formatted/HCM/Talent"):
    os.mkdir("workbooks/formatted/HCM/Talent")
    print("Directory 'workbooks/formatted/HCM/Talent' created")
if not os.path.exists("results/HCM/Talent"):
    os.mkdir("results/HCM/Talent")
    print("Directory 'results/HCM/Talent' created")
if not os.path.exists("videos/HCM/Talent"):
    os.mkdir("videos/HCM/Talent")
    print("Directory 'videos/HCM/Talent' created")
    
#Accounts Payable
if not os.path.exists("workbooks/source/ERP/AP"):
    os.mkdir("workbooks/source/ERP/AP")
    print("Directory 'workbooks/source/ERP/AP' created")
if not os.path.exists("workbooks/formatted/ERP/AP"):
    os.mkdir("workbooks/formatted/ERP/AP")
    print("Directory 'workbooks/formatted/ERP/AP' created")
if not os.path.exists("results/ERP/AP"):
    os.mkdir("results/ERP/AP")
    print("Directory 'results/ERP/AP' created")
if not os.path.exists("videos/ERP/AP"):
    os.mkdir("videos/ERP/AP")
    print("Directory 'videos/ERP/AP' created")
    
#Cash Management
if not os.path.exists("workbooks/source/ERP/CM"):
    os.mkdir("workbooks/source/ERP/CM")
    print("Directory 'workbooks/source/ERP/CM' created")
if not os.path.exists("workbooks/formatted/ERP/CM"):
    os.mkdir("workbooks/formatted/ERP/CM")
    print("Directory 'workbooks/formatted/ERP/CM' created")
if not os.path.exists("results/ERP/CM"):
    os.mkdir("results/ERP/CM")
    print("Directory 'results/ERP/CM' created")
if not os.path.exists("videos/ERP/CM"):
    os.mkdir("videos/ERP/CM")
    print("Directory 'videos/ERP/CM' created")

#Absence
if not os.path.exists("workbooks/source/HCM/Absence"):
    os.mkdir("workbooks/source/HCM/Absence")
    print("Directory 'workbooks/source/HCM/Absence' created")
if not os.path.exists("workbooks/formatted/HCM/Absence"):
    os.mkdir("workbooks/formatted/HCM/Absence")
    print("Directory 'workbooks/formatted/HCM/Absence' created")
if not os.path.exists("results/HCM/Absence"):
    os.mkdir("results/HCM/Absence")
    print("Directory 'results/HCM/Absence' created")
if not os.path.exists("videos/HCM/Absence"):
    os.mkdir("videos/HCM/Absence")
    print("Directory 'videos/HCM/Absence' created")

#Expenses
if not os.path.exists("workbooks/source/ERP/Expenses"):
    os.mkdir("workbooks/source/ERP/Expenses")
    print("Directory 'workbooks/source/ERP/Expenses' created")
if not os.path.exists("workbooks/formatted/ERP/Expenses"):
    os.mkdir("workbooks/formatted/ERP/Expenses")
    print("Directory 'workbooks/formatted/ERP/Expenses' created")
if not os.path.exists("results/ERP/Expenses"):
    os.mkdir("results/ERP/Expenses")
    print("Directory 'results/ERP/Expenses' created")
if not os.path.exists("videos/ERP/Expenses"):
    os.mkdir("videos/ERP/Expenses")
    print("Directory 'videos/ERP/Expenses' created")

#Time&Labor
if not os.path.exists("workbooks/source/HCM/TimeandLabor"):
    os.mkdir("workbooks/source/HCM/TimeandLabor")
    print("Directory 'workbooks/source/HCM/TimeandLabor' created")
if not os.path.exists("workbooks/formatted/HCM/TimeandLabor"):
    os.mkdir("workbooks/formatted/HCM/TimeandLabor")
    print("Directory 'workbooks/formatted/HCM/TimeandLabor' created")
if not os.path.exists("results/HCM/TimeandLabor"):
    os.mkdir("results/HCM/TimeandLabor")
    print("Directory 'results/HCM/TimeandLabor' created")
if not os.path.exists("videos/HCM/TimeandLabor"):
    os.mkdir("videos/HCM/TimeandLabor")
    print("Directory 'videos/HCM/TimeandLabor' created")

#Fixed Assets
if not os.path.exists("workbooks/source/ERP/FA"):
    os.mkdir("workbooks/source/ERP/FA")
    print("Directory 'workbooks/source/ERP/FA' created")
if not os.path.exists("workbooks/formatted/ERP/FA"):
    os.mkdir("workbooks/formatted/ERP/FA")
    print("Directory 'workbooks/formatted/ERP/FA' created")
if not os.path.exists("results/ERP/FA"):
    os.mkdir("results/ERP/FA")
    print("Directory 'results/ERP/FA' created")
if not os.path.exists("videos/ERP/FA"):
    os.mkdir("videos/ERP/FA")
    print("Directory 'videos/ERP/FA' created")

#Accounts Receivables
if not os.path.exists("workbooks/source/ERP/AR"):
    os.mkdir("workbooks/source/ERP/AR")
    print("Directory 'workbooks/source/ERP/AR' created")
if not os.path.exists("workbooks/formatted/ERP/AR"):
    os.mkdir("workbooks/formatted/ERP/AR")
    print("Directory 'workbooks/formatted/ERP/AR' created")
if not os.path.exists("results/ERP/AR"):
    os.mkdir("results/ERP/AR")
    print("Directory 'results/ERP/AR' created")
if not os.path.exists("videos/ERP/AR"):
    os.mkdir("videos/ERP/AR")
    print("Directory 'videos/ERP/AR' created")


# Talent - Onboarding
if not os.path.exists("workbooks/source/HCM/Talent-Onboarding"):
    os.mkdir("workbooks/source/HCM/Talent-Onboarding")
    print("Directory 'workbooks/source/HCM/Talent-Onboarding' created")
if not os.path.exists("workbooks/formatted/HCM/Talent-Onboarding"):
    os.mkdir("workbooks/formatted/HCM/Talent-Onboarding")
    print("Directory 'workbooks/formatted/HCM/Talent-Onboarding' created")
if not os.path.exists("results/HCM/Talent-Onboarding"):
    os.mkdir("results/HCM/Talent-Onboarding")
    print("Directory 'results/HCM/Talent-Onboarding' created")
if not os.path.exists("videos/HCM/Talent-Onboarding"):
    os.mkdir("videos/HCM/Talent-Onboarding")
    print("Directory 'videos/HCM/Talent-Onboarding' created")

# Talent - Recruiting
if not os.path.exists("workbooks/source/HCM/Talent-Recruiting"):
    os.mkdir("workbooks/source/HCM/Talent-Recruiting")
    print("Directory 'workbooks/source/HCM/Talent-Recruiting' created")
if not os.path.exists("workbooks/formatted/HCM/Talent-Recruiting"):
    os.mkdir("workbooks/formatted/HCM/Talent-Recruiting")
    print("Directory 'workbooks/formatted/HCM/Talent-Recruiting' created")
if not os.path.exists("results/HCM/Talent-Recruiting"):
    os.mkdir("results/HCM/Talent-Recruiting")
    print("Directory 'results/HCM/Talent-Recruiting' created")
if not os.path.exists("videos/HCM/Talent-Recruiting"):
    os.mkdir("videos/HCM/Talent-Recruiting")
    print("Directory 'videos/HCM/Talent-Recruiting' created")

# Talent - Goals
if not os.path.exists("workbooks/source/HCM/Talent-Goals"):
    os.mkdir("workbooks/source/HCM/Talent-Goals")
    print("Directory 'workbooks/source/HCM/Talent-Onboarding' created")
if not os.path.exists("workbooks/formatted/HCM/Talent-Goals"):
    os.mkdir("workbooks/formatted/HCM/Talent-Goals")
    print("Directory 'workbooks/formatted/HCM/Talent-Goals' created")
if not os.path.exists("results/HCM/Talent-Goals"):
    os.mkdir("results/HCM/Talent-Goals")
    print("Directory 'results/HCM/Talent-Goals' created")
if not os.path.exists("videos/HCM/Talent-Goals"):
    os.mkdir("videos/HCM/Talent-Goals")
    print("Directory 'videos/HCM/Talent-Goals' created")


# Talent-Performance
if not os.path.exists("workbooks/source/HCM/Talent-Performance"):
    os.mkdir("workbooks/source/HCM/Talent-Performance")
    print("Directory 'workbooks/source/HCM/Talent-Performance' created")
if not os.path.exists("workbooks/formatted/HCM/Talent-Performance"):
    os.mkdir("workbooks/formatted/HCM/Talent-Performance")
    print("Directory 'workbooks/formatted/HCM/Talent-Performance' created")
if not os.path.exists("results/HCM/Talent-Performance"):
    os.mkdir("results/HCM/Talent-Performance")
    print("Directory 'results/HCM/Talent-Performance' created")
if not os.path.exists("videos/HCM/Talent-Performance"):
    os.mkdir("videos/HCM/Talent-Performance")
    print("Directory 'videos/HCM/Talent-Performance' created")


# Talent-Management
if not os.path.exists("workbooks/source/HCM/Talent-Management"):
    os.mkdir("workbooks/source/HCM/Talent-Management")
    print("Directory 'workbooks/source/HCM/Talent-Management' created")
if not os.path.exists("workbooks/formatted/HCM/Talent-Management"):
    os.mkdir("workbooks/formatted/HCM/Talent-Management")
    print("Directory 'workbooks/formatted/HCM/Talent-Management' created")
if not os.path.exists("results/HCM/Talent-Management"):
    os.mkdir("results/HCM/Talent-Management")
    print("Directory 'results/HCM/Talent-Management' created")
if not os.path.exists("videos/HCM/Talent-Management"):
    os.mkdir("videos/HCM/Talent-Management")
    print("Directory 'videos/HCM/Talent-Management' created")


# PPM(Project Foundation & Cost)
if not os.path.exists("workbooks/source/ERP/PPM"):
    os.mkdir("workbooks/source/ERP/PPM")
    print("Directory 'workbooks/source/ERP/PPM' created")
if not os.path.exists("workbooks/formatted/ERP/PPM"):
    os.mkdir("workbooks/formatted/ERP/PPM")
    print("Directory 'workbooks/formatted/ERP/PPM' created")
if not os.path.exists("results/ERP/PPM"):
    os.mkdir("results/ERP/PPM")
    print("Directory 'results/ERP/PPM' created")
if not os.path.exists("videos/ERP/PPM"):
    os.mkdir("videos/ERP/PPM")
    print("Directory 'videos/ERP/PPM' created")

# Talent-Learnings
if not os.path.exists("workbooks/source/HCM/Talent-Learnings"):
    os.mkdir("workbooks/source/HCM/Talent-Learnings")
    print("Directory 'workbooks/source/HCM/Talent-Learnings' created")
if not os.path.exists("workbooks/formatted/HCM/Talent-Learnings"):
    os.mkdir("workbooks/formatted/HCM/Talent-Learnings")
    print("Directory 'workbooks/formatted/HCM/Talent-Learnings' created")
if not os.path.exists("results/HCM/Talent-Learnings"):
    os.mkdir("results/HCM/Talent-Learnings")
    print("Directory 'results/HCM/Talent-Learnings' created")
if not os.path.exists("videos/HCM/Talent-Learnings"):
    os.mkdir("videos/HCM/Talent-Learnings")
    print("Directory 'videos/HCM/Talent-Learnings' created")

# HCM-Health Safety
if not os.path.exists("workbooks/source/HCM/Health and Safety"):
    os.mkdir("workbooks/source/HCM/Health and Safety")
    print("Directory 'workbooks/source/HCM/Health and Safety' created")
if not os.path.exists("workbooks/formatted/HCM/Health and Safety"):
    os.mkdir("workbooks/formatted/HCM/Health and Safety")
    print("Directory 'workbooks/formatted/HCM/Health and Safety' created")
if not os.path.exists("results/HCM/Health and Safety"):
    os.mkdir("results/HCM/Health and Safety")
    print("Directory 'results/HCM/Health and Safety' created")
if not os.path.exists("videos/HCM/Health and Safety"):
    os.mkdir("videos/HCM/Health and Safety")
    print("Directory 'videos/HCM/Health and Safety' created")

# HCM Payroll Object Group
if not os.path.exists("workbooks/source/HCM/Payroll Object Group"):
    os.mkdir("workbooks/source/HCM/Payroll Object Group")
    print("Directory 'workbooks/source/HCM/Payroll Object Group' created")
if not os.path.exists("workbooks/formatted/HCM/Payroll Object Group"):
    os.mkdir("workbooks/formatted/HCM/Payroll Object Group")
    print("Directory 'workbooks/formatted/HCM/Payroll Object Group' created")
if not os.path.exists("results/HCM/Payroll Object Group"):
    os.mkdir("results/HCM/Payroll Object Group")
    print("Directory 'results/HCM/Payroll Object Group' created")
if not os.path.exists("videos/HCM/Payroll Object Group"):
    os.mkdir("videos/HCM/Payroll Object Group")
    print("Directory 'videos/HCM/Payroll Object Group' created")

# Security Segment Roles Object Group
if not os.path.exists("workbooks/source/SECURITY/Segment Object Group"):
    os.mkdir("workbooks/source/SECURITY/Segment Object Group")
    print("Directory 'workbooks/source/SECURITY/Segment Object Group' created")
if not os.path.exists("workbooks/formatted/SECURITY/Segment Object Group"):
    os.mkdir("workbooks/formatted/SECURITY/Segment Object Group")
    print("Directory 'workbooks/formatted/SECURITY/Segment Object Group' created")
if not os.path.exists("results/SECURITY/Segment Object Group"):
    os.mkdir("results/SECURITY/Segment Object Group")
    print("Directory 'results/SECURITY/Segment Object Group' created")
if not os.path.exists("videos/SECURITY/Segment Object Group"):
    os.mkdir("videos/SECURITY/Segment Object Group")
    print("Directory 'videos/SECURITY/Segment Object Group' created")






