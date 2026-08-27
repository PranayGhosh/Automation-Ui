

import time
from playwright.sync_api import Page,expect
import allure

# def test_playerightBasics(playwright):
#    browser= playwright.chromium.launch(headless=False)
#    context=browser.new_context()
#    page=context.new_page()
#    page.goto("https://dev.xaquaudp.io")

# def test_playerightShortcut(page:Page):
#     page.goto("https://dev.xaquaudp.io")

def test_xaquaDataStudio(xaquaLogin:Page, should_create_wf: bool):
    xaquaLogin.goto("https://dev.xaquaudp.io/home")

    xaquaLogin.get_by_role("button", name="Toggle home view").click()
    # time.sleep(5)
    xaquaLogin.locator("text=Create and Manage Data Products").click()
    # time.sleep(5)
    xaquaLogin.get_by_role("button", name="Expand Data Sources").click()
    # time.sleep(5)
    xaquaLogin.get_by_role("button", name="COllapse Data Sources").click()
    # time.sleep(5)
    xaquaLogin.get_by_role("button",name="Expand Uploaded Files",).click()
    # time.sleep(5)
    xaquaLogin.get_by_role("button",name="Expand FinalTesting",).click()
    # time.sleep(5)
    xaquaLogin.get_by_role("button",name="View National Intragency Fire Occurance-short").click()
    # time.sleep(5)
    # xaquaLogin.locator('app-button[aria-label="Open Data Studio"]').click()
    
    
    if should_create_wf:
        # 
        CancelcreateWorkflow(xaquaLogin)
        createWorkflow(xaquaLogin)

    else:
        selectExistingWorkflow(xaquaLogin)
        
#Command to run after crate wf freshlypytest test_playwrightBasics.py --create-wf --headed
#Command to run  only existing wf is pytest --headed
#Scenerio Cancel workflow creation  after  filling up of workflow name and description  

def CancelcreateWorkflow(xaquaLogin:Page):
    xaquaLogin.get_by_label("Open Data Studio").click()
   
 
    xaquaLogin.locator(".workflow-selector__dropdown").click()
   
    xaquaLogin.get_by_role("button",name="+ Add new workflow").click()
   
    xaquaLogin.get_by_role("textbox",name="Type a workflow name").fill("Pr_Test")
   
    xaquaLogin.get_by_role("textbox",name="Type a workflow description").fill("Pr_Desc")
    
    xaquaLogin.locator("#cancel-add-workflow").click()
   

#Scenerio  workflow creation  after  filling up of workflow name and description 
def createWorkflow(xaquaLogin:Page):
    
    # time.sleep(5)
    # xaquaLogin.get_by_role("button",name="Select workflow").click()
    xaquaLogin.locator(".workflow-selector__dropdown").click()
    # time.sleep(5)
    xaquaLogin.get_by_role("button",name="+ Add new workflow").click()
  
    xaquaLogin.get_by_role("textbox",name="Type a workflow name").fill("Md_Test_8_c")
   
    xaquaLogin.get_by_role("textbox",name="Type a workflow description").fill("Pr_Descrip")

    xaquaLogin.locator("#create-workflow").click()
    
    xaquaLogin.locator(".workflow-selector__dropdown").click()
    
    xaquaLogin.get_by_role("button",name="Confirm").click()
   
    # operationInf(xaquaLogin)
    # renameWf(xaquaLogin)
    wfOperations(xaquaLogin)
    chainSql_Mask(xaquaLogin)


    
#Selection and colfirm another workflow from the existing list
def selectExistingWorkflow(xaquaLogin:Page):
    xaquaLogin.get_by_label("Open Data Studio").click()
    xaquaLogin.locator(".workflow-selector__dropdown").click()

    xaquaLogin.get_by_text("Final-wf", exact=True).click()

    xaquaLogin.get_by_role("button",name="Confirm").click()
    time.sleep(5)
   
   #Workflow Operations
    # wfOperations(xaquaLogin)


    #Chain of  SQL-->Filter-->GroupBy-->Rename-->Sort-->MergeMultiple-->Mask
    chainSql_Mask(xaquaLogin)

    

    
def wfOperations(xaquaLogin:Page):
    Information(xaquaLogin)
    renameWf(xaquaLogin)

@allure.step("Information about workflow")
def Information(xaquaLogin:Page):
    xaquaLogin.locator(".fa-ellipsis-vertical").click()
    # time.sleep(5)
    xaquaLogin.get_by_role("menuitem", name="Information").click()
    # time.sleep(5)
    xaquaLogin.get_by_role("button",name="Close").click()
    # time.sleep(5)
@allure.step("Rename workflow")
def renameWf(xaquaLogin:Page):
    xaquaLogin.locator(".fa-ellipsis-vertical").click()
    # time.sleep(5)
    xaquaLogin.get_by_role("menuitem",name="Rename").click()

    xaquaLogin.locator("mat-dialog-container").get_by_role("textbox").fill("Rem26")
    # time.sleep(5)

    xaquaLogin.get_by_role("button",name="Cancel").click()
    xaquaLogin.locator(".fa-ellipsis-vertical").click()

    xaquaLogin.get_by_role("menuitem",name="Rename").click()

    xaquaLogin.locator("mat-dialog-container").get_by_role("textbox").fill("Rem26")
    xaquaLogin.get_by_role("button",name="Rename").click()



#Chain of  SQL-->Filter-->GroupBy-->Rename-->Sort-->MergeMultiple-->Mask
def chainSql_Mask(xaquaLogin:Page):
    addSQlTask(xaquaLogin)
    addFilterTask(xaquaLogin)
    addGroupByTask(xaquaLogin)
    renameColumns(xaquaLogin)
    sortColumns(xaquaLogin)
    mergeMultipleColumn(xaquaLogin)
    maskColumn(xaquaLogin)
    # rearrange_canvas_tasks_grid(xaquaLogin)
    # xaquaLogin.wait_for_timeout(1000)
    

    # with allure.step("Rearrange Canvas into 2-Row Grid"):
    #     rearrange_canvas_tasks_grid(xaquaLogin)
    #     xaquaLogin.wait_for_timeout(1000) # Pause briefy for visual layout rendering
    

@allure.step("SQL Task Execution")
def addSQlTask(xaquaLogin:Page):
    xaquaLogin.get_by_role("button",name="Add Task").click()
    xaquaLogin.locator("udp-form-field[label='Task Name'] input").fill("SQL Task")
    xaquaLogin.locator("udp-icon-button[mattooltip='Change task type']").click()
    xaquaLogin.get_by_role("button",name="SQL Query").click()
    xaquaLogin.locator("ngx-monaco-editor").click()
    xaquaLogin.keyboard.type('''SELECT 
    "STATE",
    "FIRE_SIZE_CLASS",
    COUNT("OBJECTID") AS "TOTAL_INCIDENTS",
    ROUND(SUM("FIRE_SIZE"), 2) AS "TOTAL_ACRES_BURNED",
    ROUND(AVG("FIRE_SIZE"), 2) AS "AVG_ACRES_PER_FIRE",
    SUM(COALESCE("DISCOVERY_TIME", 0)) AS "TOTAL_DISCOVERY_TIME",
    ROUND(MIN("FIRE_SIZE"), 2) AS "MIN_FIRE_SIZE",
    ROUND(MAX("FIRE_SIZE"), 2) AS "MAX_FIRE_SIZE",
    MIN("FIRE_YEAR") AS "EARLIEST_FIRE_YEAR",
    MAX("FIRE_YEAR") AS "LATEST_FIRE_YEAR",
    ROUND(AVG("DISCOVERY_DOY"), 2) AS "AVG_DISCOVERY_DOY",
    ROUND(AVG("CONTAINMENT_DAY_OF_YEAR"), 2) AS "AVG_CONTAINMENT_DOY",
    ROUND(AVG("CONTAINMENT_TIME"), 2) AS "AVG_CONTAINMENT_TIME",
    ROUND(AVG("LATITUDE"), 4) AS "AVG_LATITUDE",
    ROUND(AVG("LONGITUDE"), 4) AS "AVG_LONGITUDE",
    COUNT(DISTINCT "NWCG_REPORTING_AGENCY") AS "DISTINCT_REPORTING_AGENCIES",
    COUNT(DISTINCT "NWCG_GENERAL_CAUSE") AS "DISTINCT_GENERAL_CAUSES",
    COUNT(DISTINCT "OWNER_DESCR") AS "DISTINCT_OWNER_DESCR"
    FROM "National Intragency Fire Occurance-short"
    GROUP BY "STATE", "FIRE_SIZE_CLASS"
    ORDER BY "STATE" ASC, "FIRE_SIZE_CLASS" ASC;''')



    xaquaLogin.get_by_role("button",name="Save & Run").click()
    xaquaLogin.locator("button[id$='-save-workflow']").click()
    xaquaLogin.get_by_role("button", name="Yes, save").click()
    xaquaLogin.locator("#tour-dl-data").wait_for(state="visible")
    xaquaLogin.locator("#tour-dl-data").scroll_into_view_if_needed()

@allure.step("Group By Task Execution")
def addGroupByTask(xaquaLogin:Page):
    xaquaLogin.get_by_role("button",name="Add Task").click()
    xaquaLogin.locator("udp-form-field[label='Task Name'] input").fill("Group_By_Summary")
    xaquaLogin.locator("udp-icon-button[mattooltip='Change task type']").click()
    xaquaLogin.locator(".task-type-option").filter(has_text="Group By Summary").click()
    source = xaquaLogin.locator("mat-list-item").filter(has_text="FIRE_SIZE_CLASS")
    target = xaquaLogin.locator(".cdk-drop-list").filter(has=xaquaLogin.locator(".config-section__header", has_text="Columns"))
    angular_cdk_drag(xaquaLogin, source, target)
    source = xaquaLogin.locator("mat-list-item").filter(has_text="TOTAL_ACRES_BURNED")
    target = xaquaLogin.locator(".cdk-drop-list").filter(has=xaquaLogin.locator(".config-section__header", has_text="Values"))
    angular_cdk_drag(xaquaLogin, source, target)
    
    xaquaLogin.locator("mat-select").last.click()

    xaquaLogin.get_by_role("option", name="SUM").click()

    source=xaquaLogin.locator("mat-list-item").filter(has_text="STATE")
    target = xaquaLogin.locator(".cdk-drop-list").filter(has=xaquaLogin.locator(".config-section__header", has_text="Columns"))
    angular_cdk_drag(xaquaLogin, source, target)

    source=xaquaLogin.locator("mat-list-item").filter(has_text="TOTAL_INCIDENTS")
    target = xaquaLogin.locator(".cdk-drop-list").filter(has=xaquaLogin.locator(".config-section__header", has_text="Values"))
    angular_cdk_drag(xaquaLogin, source, target)
    xaquaLogin.locator("mat-select").last.click()
    xaquaLogin.get_by_role("option", name="Mean (Average)").click()
    xaquaLogin.get_by_role("button",name="Save & Run").click()
    xaquaLogin.locator("button[id$='-save-workflow']").click()
    xaquaLogin.get_by_role("button", name="Yes, save").click()
    xaquaLogin.locator("#tour-dl-data").wait_for(state="visible")
    xaquaLogin.locator("#tour-dl-data").scroll_into_view_if_needed()
  
    
@allure.step("Rename Columns Execution")
def renameColumns(xaquaLogin:Page):
    xaquaLogin.get_by_role("button",name="Add Task").click()
    xaquaLogin.locator("udp-form-field[label='Task Name'] input").fill("Rename-Columns")
    xaquaLogin.locator("udp-icon-button[mattooltip='Change task type']").click()
    xaquaLogin.locator(".task-type-option").filter(has_text="Rename Columns").click()
    xaquaLogin.locator("tr").filter(has_text="FIRE_SIZE_CLASS").get_by_role("textbox").fill("FireSizeClass")
    xaquaLogin.locator("tr").filter(has_text="TOTAL_INCIDENTS").get_by_role("textbox").fill("TotalIncidents")

    xaquaLogin.get_by_role("button",name="Save & Run").click()
    xaquaLogin.locator("button[id$='-save-workflow']").click()
    xaquaLogin.get_by_role("button", name="Yes, save").click()
    xaquaLogin.locator("#tour-dl-data").wait_for(state="visible")
    xaquaLogin.locator("#tour-dl-data").scroll_into_view_if_needed()

# def renameColumns_int(xaquaLogin:Page):
#     xaquaLogin.get_by_role("button",name="Add Task").click()
#     xaquaLogin.locator("udp-form-field[label='Task Name'] input").fill("Rename Columns")
#     xaquaLogin.locator("udp-icon-button[mattooltip='Change task type']").click()
#     xaquaLogin.locator(".task-type-option").filter(has_text="Rename Columns").click()
#     xaquaLogin.locator("tr").filter(has_text="STATE").get_by_role("textbox").fill("State")
    

#     xaquaLogin.get_by_role("button",name="Save & Run").click()
#     xaquaLogin.locator("button[id$='-save-workflow']").click()
#     xaquaLogin.get_by_role("button", name="Yes, save").click()
#     xaquaLogin.locator("#tour-dl-data").wait_for(state="visible")
#     xaquaLogin.locator("#tour-dl-data").scroll_into_view_if_needed()
    
@allure.step("Sort Columns Execution")
def sortColumns(xaquaLogin:Page):
    xaquaLogin.get_by_role("button",name="Add Task").click()
    xaquaLogin.locator("udp-form-field[label='Task Name'] input").fill("Sort")
    xaquaLogin.locator("udp-icon-button[mattooltip='Change task type']").click()
    xaquaLogin.locator(".task-type-option").filter(has_text="Sort Columns").click()

    xaquaLogin.locator("udp-form-field[label='Column']").get_by_role("combobox").click()
    xaquaLogin.get_by_role("option",name='TOTAL_ACRES_BURNED').click()
    xaquaLogin.locator("udp-form-field[label='Sort Order']").get_by_role("combobox").click()
    xaquaLogin.get_by_role("option",name="Ascending").click()
    xaquaLogin.get_by_role("button",name="Save & Run").click()
    xaquaLogin.locator("button[id$='-save-workflow']").click()
    xaquaLogin.get_by_role("button", name="Yes, save").click()
    xaquaLogin.locator("#tour-dl-data").wait_for(state="visible")
    xaquaLogin.locator("#tour-dl-data").scroll_into_view_if_needed()


@allure.step("Mask Columns Execution")

def maskColumn(xaquaLogin:Page):
   xaquaLogin.get_by_role("button",name="Add Task").click()
   xaquaLogin.locator("udp-form-field[label='Task Name'] input").fill("Mask")
   xaquaLogin.locator("udp-icon-button[mattooltip='Change task type']").click()
   xaquaLogin.locator(".task-type-option").filter(has_text="Mask Columns").click()
   xaquaLogin.get_by_role("button",name="+ Column To Mask").click()
   xaquaLogin.locator("udp-form-field").filter(has_text="Column Name").get_by_role("combobox").click()
   xaquaLogin.get_by_role("option", name="StateFireSizeClass", exact=False).click()
   xaquaLogin.locator("udp-form-field").filter(has_text="Mask Type").get_by_role("combobox").click()
   xaquaLogin.get_by_role("option", name="SCRAMBLE", exact=False).click()
   xaquaLogin.locator("udp-form-field").filter(has_text="Mask Subtype").get_by_role("combobox").click()
   xaquaLogin.get_by_role("option", name="Scramble Characters", exact=False).click()
   xaquaLogin.get_by_role("button",name="Save & Run").click()
   xaquaLogin.locator("button[id$='-save-workflow']").click()
   xaquaLogin.get_by_role("button", name="Yes, save").click()
   xaquaLogin.locator("#tour-dl-data").wait_for(state="visible")
   xaquaLogin.locator("#tour-dl-data").scroll_into_view_if_needed()




@allure.step("Merge Multiple Columns Execution")
def mergeMultipleColumn(xaquaLogin:Page):
    xaquaLogin.get_by_role("button",name="Add Task").click()
    xaquaLogin.locator("udp-form-field[label='Task Name'] input").fill("Merge-Multiple-Columns")
    xaquaLogin.locator("udp-icon-button[mattooltip='Change task type']").click()
    xaquaLogin.locator(".task-type-option").filter(has_text="Merge Multiple Columns").click()
    xaquaLogin.locator("udp-form-field[label='New Column Name'] input").fill("StateFireSizeClass")
    xaquaLogin.locator("udp-form-field").filter(has_text="Column 1").get_by_role("combobox").click()
    xaquaLogin.get_by_role("option", name="STATE").click()
    xaquaLogin.locator("udp-form-field").filter(has_text="Column 2").get_by_role("combobox").click()
    xaquaLogin.get_by_role("option", name="FireSizeClass").click()
    xaquaLogin.locator("udp-form-field").filter(has_text="Separator").get_by_role("combobox").click()
    xaquaLogin.get_by_role("option", name="Comma (,)").click()
    xaquaLogin.locator("udp-form-field").filter(has_text="Ignore NA Values").get_by_role("combobox").click()
    xaquaLogin.get_by_role("option", name="true").click()
    xaquaLogin.locator("udp-form-field").filter(has_text="Drop Source Columns After Merge").get_by_role("combobox").click()
    xaquaLogin.get_by_role("option", name="false").click()

    xaquaLogin.get_by_role("button",name="Save & Run").click()
    xaquaLogin.locator("button[id$='-save-workflow']").click()
    xaquaLogin.get_by_role("button", name="Yes, save").click()
    xaquaLogin.locator("#tour-dl-data").wait_for(state="visible")
    xaquaLogin.locator("#tour-dl-data").scroll_into_view_if_needed()


@allure.step("Filter Task Execution")
def addFilterTask(xaquaLogin:Page):
    xaquaLogin.get_by_role("button",name="Add Task").click()
    xaquaLogin.locator("udp-form-field[label='Task Name'] input").fill("Filter")
    xaquaLogin.locator("udp-icon-button[mattooltip='Change task type']").click()
    xaquaLogin.locator(".task-type-option").filter(has_text="Filter").click()
    # xaquaLogin.get_by_role("button",name="+ Ruleset").click()
    xaquaLogin.get_by_role("button", name="+ Rule", exact=True).click()
    xaquaLogin.locator("udp-form-field[label='Column Name']").get_by_role("combobox").click()
    xaquaLogin.get_by_role("option", name="STATE").click()
    xaquaLogin.locator("udp-form-field[label='Operator']").get_by_role("combobox").click()
    xaquaLogin.get_by_role("option", name="is equal to").click()
    xaquaLogin.locator("udp-form-field[label='Value'] input").fill("CA")
    xaquaLogin.locator("udp-form-field[label='Select Column to Include']").get_by_role("combobox").click()
    xaquaLogin.get_by_role("option",name="All Column").click()
    xaquaLogin.locator("udp-form-field[label='Keep or remove duplicate rows']").get_by_role("combobox").click()
    xaquaLogin.get_by_role("option",name="NONE").click()
    xaquaLogin.locator("udp-form-field[label='Keep or remove rows with missing value']").get_by_role("combobox").click()
    xaquaLogin.get_by_role("option",name="NONE").click()
    xaquaLogin.get_by_role("button",name="Save & Run").click()
    xaquaLogin.locator("button[id$='-save-workflow']").click()
    xaquaLogin.get_by_role("button", name="Yes, save").click()
    xaquaLogin.locator("#tour-dl-data").wait_for(state="visible")
    xaquaLogin.locator("#tour-dl-data").scroll_into_view_if_needed()
    

   




def addPivotTaskOperation(xaquaLogin:Page):
    xaquaLogin.get_by_role("button",name="Add Task").click()
    # time.sleep(5)
    
    xaquaLogin.locator("udp-form-field[label='Task Name'] input").fill("Pivot Task")
    # time.sleep(5)
    
    # Drag to Columns
    source = xaquaLogin.locator("mat-list-item").filter(has_text="CONTAINMENT_DAY_OF_YEAR")
    target = xaquaLogin.locator(".cdk-drop-list").filter(has=xaquaLogin.locator(".config-section__header", has_text="Columns"))
    # source.drag_to(target)
    angular_cdk_drag(xaquaLogin, source, target)
    # time.sleep(5)

    # Drag to Rows
    source = xaquaLogin.locator("mat-list-item").filter(has_text="DISCOVERY_DOY")
    target = xaquaLogin.locator(".cdk-drop-list").filter(has=xaquaLogin.locator(".config-section__header", has_text="Rows"))
    # source.drag_to(target)
    angular_cdk_drag(xaquaLogin, source, target)
    # time.sleep(5)
    
    # Drag to Values
    source = xaquaLogin.locator("mat-list-item").filter(has_text="DISCOVERY_TIME")
    source.scroll_into_view_if_needed()
    # time.sleep(1)
    target = xaquaLogin.locator(".cdk-drop-list").filter(has=xaquaLogin.locator(".config-section__header", has_text="Values"))
    target.scroll_into_view_if_needed()
    # time.sleep(1)
    angular_cdk_drag(xaquaLogin, source, target)
    # source.drag_to(target)
    # time.sleep(5)   
    # Select dropdown in Values section
    xaquaLogin.locator("mat-select").last.click()
    # time.sleep(2)
    xaquaLogin.get_by_role("option", name="SUM").click()
    # time.sleep(2)
    
    xaquaLogin.get_by_role("button",name="Save & Run").click()







def angular_cdk_drag(page: Page, source_locator, target_locator):
    source_locator.scroll_into_view_if_needed()
    target_locator.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    # Calculate center points
    s_box = source_locator.bounding_box()
    t_box = target_locator.bounding_box()
    
    src_x = s_box["x"] + s_box["width"] / 2
    src_y = s_box["y"] + s_box["height"] / 2
    tgt_x = t_box["x"] + t_box["width"] / 2
    tgt_y = t_box["y"] + t_box["height"] / 2

    # Execute human-like mouse movement
    page.mouse.move(src_x, src_y)
    page.mouse.down()
    page.mouse.move(tgt_x, tgt_y, steps=30)
    page.mouse.up()

#