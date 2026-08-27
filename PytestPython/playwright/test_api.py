from typing import Any
import uuid
from playwright.sync_api import Playwright
from playwright.sync_api import Page
import time
import pytest

def test_capture_auth_headers(page: Page):
    # Print headers the moment the browser calls /user/auth
    def on_request(request):
        if "user/auth" in request.url:
            print("\n" + "="*60)
            print("[FOUND REQUEST HEADERS SENT TO /user/auth]:")
            for header, val in request.headers.items():
                print(f"  {header}: {val}")
            print("="*60 + "\n")

    page.on("request", on_request)

    # Perform UI Login
    page.goto("https://dev.xaquaudp.io/login")
    page.get_by_label("USER ID").fill("Pranay")
    page.get_by_role("button", name="Continue").click()
    page.get_by_label("Password", exact=True).fill("Kolkata@#7531")
    page.locator("#v2-terms").check()
    page.get_by_role("button", name="Sign In").click()
    time.sleep(5)


def test_get_token(get_token):
    assert get_token is not None
    # print("\n[SUCCESS] Token received in test:", get_token)

@pytest.mark.skip
def test_rename_wf(playwright: Playwright, get_token):
    auth_header = get_token if get_token.startswith("Bearer ") else f"Bearer {get_token}"

    body_payload = {
        "dataAssetWorkflowDefinition": {
            "name": "Supply-wf",
            "links": [],
            "nodes": [
                {
                    "lastUpdatedTimeStamp": None,
                    "disabled": False,
                    "id": "99999",
                    "loc": "",
                    "name": "Initial Task"
                }
            ]
        },
        "taskContractValidationState": "Ok"
    }

    api_request_context = playwright.request.new_context(base_url="https://xaqua-udp-core-dmg-api-py-dev.xaquaudp.io")
    response = api_request_context.put(
        "/dataAssetWorkflow/updateWorkflowDefinition",
        params={"dataAssetWorkflowID": "6103295e021147b9af8e8ae1c4fc9241"},
        data=body_payload,
        headers={
            "Authorization": auth_header,
            "Content-Type": "application/json"
        }
    )

    print(f"\n[Status Code]: {response.status}")
    print("[Response JSON]:", response.json())

@pytest.fixture
def session_key(playwright:Playwright,get_token):
    auth_header=get_token if get_token.startswith('Bearer')else f"Bearer {get_token}"
    body_payload={
            
    "userID": "Pranay",
    "customerID": "TRUST",
    "actionType": "SES",
    "actionCode": "SES_INIT",
    "workflowDefination": None,
    "dataAssetID": None,
    "dataAssetType": None,
    "actionParameters": None,
    "sessionKey": None,
    "taskContentRequest": None,
    "queryScript": None,
    "dataBlendRule": None

     }
    api_request_context=playwright.request.new_context(base_url="https://xaqua-udp-core-dmg-api-py-dev.xaquaudp.io")
    response=api_request_context.post("/userDataSession",data=body_payload,
    headers={"Authorization":auth_header,
             "Content-Type":"application/json"
    })
    
    print(f"\n[Session Key Request Status]: {response.status}")
    try:
        res_json = response.json()
        print(f"[Session Key JSON Response]: {res_json}")
        if isinstance(res_json, dict) and "data" in res_json:
            clean_session_key = res_json.get("data")
        else:
            clean_session_key = response.text().strip().strip('"')
    except Exception:
        raw_text = response.text()
        print(f"[Session Key Raw Response]: {raw_text}")
        clean_session_key = raw_text.strip().strip('"')
        
    print(f"[Session Key Parsed]: {clean_session_key}")
    return clean_session_key



@pytest.fixture
def init_datasession(playwright:Playwright,get_token,session_key):
    auth_header=get_token if get_token.startswith('Bearer')else f"Bearer {get_token}"
    body_payload={
                    "userID": "Pranay",
                    "customerID": "TRUST",
                    "actionType": "DPT",
                    "actionCode": "DPT_INIT",
                    "workflowDefination": None,
                    "dataAssetID": "2938eddc-7e33-4891-b99d-b1879a6a5a7a",
                    "dataAssetType": "DF",
                    "sessionKey": session_key,
                    "taskContentRequest": None,
                    "taskName": None,
                    "taskParameters": None,
                    "taskTypeCode": None,
                    "previousTaskID": None,
                    "nextTaskID": None,
                    "taskID": None,
                    "isTaskContractValidationFailed": None,
                    "isActive": True,
                    "workflowDefinitionName": None,
                    "workflowDefinitionDescription": None
                }
                
    
     
    api_request_context=playwright.request.new_context(base_url="https://xaqua-udp-core-dmg-api-py-dev.xaquaudp.io")
    response=api_request_context.post("/userDataSession",data=body_payload,
    headers={"Authorization":auth_header,
             "Content-Type":"application/json"
    })
    print(f"\n[DPT_INIT Status Code]: {response.status}")
    assert response.status == 200, f"DPT_INIT failed: {response.text()}"
    return session_key
   
def test_user_datasession_init(init_datasession: str):
    """Verifies that the session initialization fixture completed successfully."""
    assert init_datasession is not None
    print(f"\n[Test Verified]: Session active with key -> {init_datasession}")

@pytest.mark.skip
def test_user_datasession_create_wf(playwright:Playwright,get_token,init_datasession):
    auth_header=get_token if get_token.startswith('Bearer')else f"Bearer {get_token}"
    api_request_context=playwright.request.new_context(base_url="https://xaqua-udp-core-dmg-api-py-dev.xaquaudp.io")
    
   

    # 2. Save the workflow using DPT_SAVE_WORKFLOW
    save_payload = {
        "actionCode": "DPT_SAVE_WORKFLOW",
        "actionType": "DPT",
        "customerID": "TRUST",
        "dataAssetID": "2938eddc-7e33-4891-b99d-b1879a6a5a7a",
        "dataAssetType": "DF",
        "isActive": True,
        "isTaskContractValidationFailed": None,
        "nextTaskID": None,
        "previousTaskID": None,
        "sessionKey": init_datasession,
        "taskContentRequest": None,
        "taskID": None,
        "taskName": None,
        "taskParameters": None,
        "taskTypeCode": None, 
        "userID": "Pranay",
        "workflowDefination": {"name": "Final-wf20", "nodes": [], "links": []},
        "workflowDefinitionDescription": "This worklfow will by demoed to calsstrs",
        "workflowDefinitionName": "Final-wf20"
    }
    
    response=api_request_context.post("/userDataSession",data=save_payload,
    headers={"Authorization":auth_header,
             "Content-Type":"application/json"
    })
    print(f"[DPT_SAVE_WORKFLOW Status Code]: {response.status}")
    print("[Response JSON]: for creation workflow", response.json())
   
def add_sql_task(playwright:Playwright,get_token,init_datasession):
    auth_header=get_token if get_token.startswith('Bearer')else f"Bearer {get_token}"
    api_request_context=playwright.request.new_context(base_url="https://xaqua-udp-core-dmg-api-py-dev.xaquaudp.io")
    sql_id = str(uuid.uuid4())
   

    # 2. Save the workflow using DPT_SAVE_WORKFLOW
    task_payload = {
            
    "userID": "Pranay",
    "customerID": "TRUST",
    "actionType": "DPT",
    "actionCode": "DPT_ADD_TASK",
    "workflowDefination": None,
    "dataAssetID": "2938eddc-7e33-4891-b99d-b1879a6a5a7a",
    "dataAssetType": "DF",
    "sessionKey":init_datasession,
    "taskContentRequest":None,
    "taskName": "New task",
    "taskParameters": {
        "sql": '''SELECT "STATE", "FIRE_SIZE_CLASS", COUNT("OBJECTID") AS "TOTAL_INCIDENTS", ROUND(SUM("FIRE_SIZE"), 2) AS "TOTAL_ACRES_BURNED", ROUND(AVG("FIRE_SIZE"), 2) AS "AVG_ACRES_PER_FIRE", SUM(COALESCE("DISCOVERY_TIME", 0)) AS "TOTAL_DISCOVERY_TIME", ROUND(MIN("FIRE_SIZE"), 2) AS "MIN_FIRE_SIZE", ROUND(MAX("FIRE_SIZE"), 2) AS "MAX_FIRE_SIZE", MIN("FIRE_YEAR") AS "EARLIEST_FIRE_YEAR", MAX("FIRE_YEAR") AS "LATEST_FIRE_YEAR", ROUND(AVG("DISCOVERY_DOY"), 2) AS "AVG_DISCOVERY_DOY", ROUND(AVG("CONTAINMENT_DAY_OF_YEAR"), 2) AS "AVG_CONTAINMENT_DOY", ROUND(AVG("CONTAINMENT_TIME"), 2) AS "AVG_CONTAINMENT_TIME", ROUND(AVG("LATITUDE"), 4) AS "AVG_LATITUDE", ROUND(AVG("LONGITUDE"), 4) AS "AVG_LONGITUDE", COUNT(DISTINCT "NWCG_REPORTING_AGENCY") AS "DISTINCT_REPORTING_AGENCIES", COUNT(DISTINCT "NWCG_GENERAL_CAUSE") AS "DISTINCT_GENERAL_CAUSES", COUNT(DISTINCT "OWNER_DESCR") AS "DISTINCT_OWNER_DESCR" FROM "National Intragency Fire Occurance-short" GROUP BY "STATE", "FIRE_SIZE_CLASS" ORDER BY "STATE" ASC, "FIRE_SIZE_CLASS" ASC;''',
        "sql-prompt": "",
        "requestText": ""
    },
    "taskTypeCode": "SQL",
    "previousTaskID": None,
    "nextTaskID": None,
    "taskID":sql_id ,
    "isTaskContractValidationFailed":None,
    "isActive": True,
    "workflowDefinitionName": "ts-version-1",
    "workflowDefinitionDescription": "se"
    }
    
    response=api_request_context.post("/userDataSession",data=task_payload,
    headers={"Authorization":auth_header,
             "Content-Type":"application/json"
    })
    print(f"[DPT_SAVE_WORKFLOW Status Code]: {response.status}")

    save_payload = {
                    
            "userID": "Pranay",
            "customerID": "TRUST",
            "actionType": "DPT",
            "actionCode": "DPT_SAVE_WF_TASK_SCHEMA",
            "workflowDefination":None,
            "dataAssetID": "2938eddc-7e33-4891-b99d-b1879a6a5a7a",
            "dataAssetWorkflowId": "2bf3f9b57e864433a24877b726f9b883",
            "dataAssetType": "DF",
            "sessionKey":init_datasession,
            "taskContentRequest": None,
            "taskName": None,
            "taskParameters": None,
            "taskTypeCode": None,
            "previousTaskID": None,
            "nextTaskID": None,
            "taskID": None,
            "isTaskContractValidationFailed": None,
            "isActive": True,
            "workflowDefinitionName": "ts-version-1",
            "workflowDefinitionDescription": None
   
        }
    
    response=api_request_context.post("/userDataSession",data=save_payload,
    headers={"Authorization":auth_header,
             "Content-Type":"application/json"
    })
    print(f"[DPT_SAVE_WORKFLOW Status Code]: {response.status}")
    print("[Response JSON]: for Save  workflow", response.json())

    query_params:dict[str, Any] = {
					"dataAssetWorkflowID": "2bf3f9b57e864433a24877b726f9b883",
					"userID": "Pranay",
					"customerID": "TRUST",
					"workflowDefinitionName": "ts-version-1",
					"workflowDefinitionDescription": "se"
			   }

    update_payload = {
            "dataAssetWorkflowDefinition": {
                "name": "ts-version-1",
                "nodes": [
                    {
                        "lastUpdatedTimeStamp": 1787651872,
                        "id": "99999",  # Root dataset ID
                        "profileSummary": [],
                        "taskName": "Initial Task",
                        "type": "InitDF",
                        "taskParameters": "",
                        "loc": "",
                        "taskDashboardConfig": []
                    },
                    {
                        "lastUpdatedTimeStamp": int(time.time()),
                        "name": "Sql-Task",
                        "type": "SQL",
                        "loc": "-120 -47.5",
                        "properties": {
                            "sql": "SELECT \"STATE\", \"FIRE_SIZE_CLASS\", COUNT(\"OBJECTID\") AS \"TOTAL_INCIDENTS\" FROM \"National Intragency Fire Occurance-short\" GROUP BY \"STATE\", \"FIRE_SIZE_CLASS\" ORDER BY \"STATE\" ASC, \"FIRE_SIZE_CLASS\" ASC;",
                            "sql-prompt": "",
                            "requestText": ""
                        },
                        "id": sql_id  # <--- MUST MATCH taskID from DPT_ADD_TASK
                    }
                ],
                "links": []
            },
            "taskContractValidationState": "Ok"
            }
    res_update=api_request_context.put("/dataAssetWorkflow/updateWorkflowDefinition",params=query_params,data=update_payload,
    headers={"Authorization":auth_header,
             "Content-Type":"application/json"
    })
    assert res_update.status == 200
    print(f"\n[Helper]: Created SQL Task Node ({sql_id})")

    return sql_id


    # print("[Response JSON]: for Save Add task ", response.json())


# def test_save_task_to_wf(get_token,init_datasession,playwright:Playwright):
#     auth_header=get_token if get_token.(startswith('Bearer')else f"Bearer {get_token}"
#     api_request_context=playwright.request.new_context(base_url="https://xaqua-udp-core-dmg-api-py-dev.xaquaudp.io")
def filter_task(playwright:Playwright,init_datasession,get_token,previous_task_id):
    auth_header=get_token if get_token.startswith('Bearer')else f"Bearer {get_token}"
    api_request_context=playwright.request.new_context(base_url="https://xaqua-udp-core-dmg-api-py-dev.xaquaudp.io")

    filter_task_id=str(uuid.uuid4())

    task_payload = {
                
        "userID": "Pranay",
        "customerID": "TRUST",
        "actionType": "DPT",
        "actionCode": "DPT_ADD_TASK",
        "workflowDefination": None,
        "dataAssetID": "2938eddc-7e33-4891-b99d-b1879a6a5a7a",
        "dataAssetType": "DF",
        "sessionKey": init_datasession,
        "taskContentRequest": None,
        "taskName": "New task",
        "taskParameters": {
            "filterExpressionType": "CONFIG",
            "filterSQLStatement": "",
            "includeAllColumns": True,
            "filterConfig": [
            {
                "columnName": "STATE",
                "operator": "=",
                "valueType": "value",
                "ignoreCase": None,
                "comparisonValue": {
                "singleValue": "AZ",
                "valueRangeFrom": None,
                "valueRangeTo": None,
                "valueList": None
                }
            }
            ],
            "returnRowRange": "",
            "includedColumnList": "",
            "filterColumn": {
            "includeAllColumns": True,
            "includedColumnList": [],
            "excludedColumnList": []
            },
            "krRowsByRowNumber": {
            "keep": None,
            "rowFilterByRowNumberType": None,
            "firstNRows": None,
            "lastNRows": None,
            "startRowNumber": None,
            "endRowNumber": None
            },
            "krByDuplicateRows": {
            "keep": None,
            "basedOnAllColumn": False,
            "basedOnColumns": []
            },
            "krRowsWithMissingValues": {
            "keep": None,
            "missingValueCols": []
            }
        },
        "taskTypeCode": "Filter",
        "previousTaskID":previous_task_id,
        "nextTaskID": None,
        "taskID": filter_task_id,
        "isTaskContractValidationFailed": None,
        "isActive": True,
        "workflowDefinitionName": "ts-version-1",
        "workflowDefinitionDescription": "se"
    }

    res_filter=api_request_context.post("/userDataSession",data=task_payload,
    headers={"Authorization":auth_header,
             "Content-Type":"application/json"
    })
    print(f"[DPT_SAVE_WORKFLOW Status Code]: {res_filter.status}")
    print("[Response JSON]: for Save Filter  task ", res_filter.json())

    save_payload = {
                    
            "userID": "Pranay",
            "customerID": "TRUST",
            "actionType": "DPT",
            "actionCode": "DPT_SAVE_WF_TASK_SCHEMA",
            "workflowDefination":None,
            "dataAssetID": "2938eddc-7e33-4891-b99d-b1879a6a5a7a",
            "dataAssetWorkflowId": "2bf3f9b57e864433a24877b726f9b883",
            "dataAssetType": "DF",
            "sessionKey":init_datasession,
            "taskContentRequest": None,
            "taskName": None,
            "taskParameters": None,
            "taskTypeCode": None,
            "previousTaskID":None,
            "nextTaskID": None,
            "taskID": None,
            "isTaskContractValidationFailed": None,
            "isActive": True,
            "workflowDefinitionName": "ts-version-1",
            "workflowDefinitionDescription": None
   
        }
    
    response=api_request_context.post("/userDataSession",data=save_payload,
    headers={"Authorization":auth_header,
             "Content-Type":"application/json"
    })
    print(f"[DPT_SAVE_WORKFLOW Status Code]: {response.status}")
    print("[Response JSON]: for Save  workflow", response.json())
    update_payload = {
                        "dataAssetWorkflowDefinition": {
                            "name": "ts-version-1",
                            "nodes": [
                                {
                                    "lastUpdatedTimeStamp": 1787656319,
                                    "id": "99999",
                                    "profileSummary": [],
                                    "taskName": "Initial Task",
                                    "type": "InitDF",
                                    "taskParameters": "",
                                    "loc": "",
                                    "taskDashboardConfig": []
                                },
                                {
                                    "lastUpdatedTimeStamp": int(time.time()),
                                    "disabled": False,
                                    "id": previous_task_id,  # Dynamic SQL Parent Task ID
                                    "loc": "-120 -47.5",
                                    "name": "Sql-Task",
                                    "properties": {
                                    "requestText": "",
                                     "sql": '''SELECT 
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
                                                    ORDER BY "STATE" ASC, "FIRE_SIZE_CLASS" ASC;''',
                                        "sql-prompt": ""
                                    },
                                    "type": "SQL"
                                },
                                {
                                    "lastUpdatedTimeStamp": int(time.time()),
                                    "name": "New task",
                                    "type": "Filter",
                                    "loc": "240 -47.5",
                                    "properties": {
                                        "filterExpressionType": "CONFIG",
                                        "filterSQLStatement": "",
                                        "includeAllColumns": True,
                                        "filterConfig": [
                                            {
                                                "columnName": "STATE",
                                                "operator": "=",
                                                "valueType": "value",
                                                "ignoreCase": None,
                                                "comparisonValue": {
                                                    "singleValue": "AZ",
                                                    "valueRangeFrom": None,
                                                    "valueRangeTo": None,
                                                    "valueList": None
                                                }
                                            }
                                        ],
                                        "returnRowRange": "",
                                        "includedColumnList": "",
                                        "filterColumn": {
                                            "includeAllColumns": True,
                                            "includedColumnList": [],
                                            "excludedColumnList": []
                                        },
                                        "krRowsByRowNumber": {
                                            "keep": None,
                                            "rowFilterByRowNumberType": None,
                                            "firstNRows": None,
                                            "lastNRows": None,
                                            "startRowNumber": None,
                                            "endRowNumber": None
                                        },
                                        "krByDuplicateRows": {
                                            "keep": None,
                                            "basedOnAllColumn": False,
                                            "basedOnColumns": []
                                        },
                                        "krRowsWithMissingValues": {
                                            "keep": None,
                                            "missingValueCols": []
                                        }
                                    },
                                    "id": filter_task_id  # Dynamic Filter Task ID
                                }
                            ],
                            "links": [
                                {
                                    "from": previous_task_id,       # Chained from SQL Task
                                    "to": filter_task_id,      # Connected to Filter Task
                                    "fromPort": "Right",
                                    "toPort": "Left",
                                    "id": str(uuid.uuid4())    # Dynamic link ID
                                }
                            ]
                        },
                        "taskContractValidationState": "Ok"
    }
    query_params:dict[str, Any] = {
                                    "dataAssetWorkflowID": "2bf3f9b57e864433a24877b726f9b883",
                                    "userID": "Pranay",
                                    "customerID": "TRUST",
                                    "workflowDefinitionName": "ts-version-1",
                                    "workflowDefinitionDescription": "se"
			                    }

    res_filter=api_request_context.put("/dataAssetWorkflow/updateWorkflowDefinition",params=query_params,data=update_payload,
    headers={"Authorization":auth_header,
             "Content-Type":"application/json"
    })
    print(f"[DPT_SAVE_WORKFLOW Status Code]: {res_filter.status}")
    print("[Response JSON]: for Save Filter  task ", res_filter.json())

    print(f"[PUT updateWorkflowDefinition Status Code]: {res_filter.status}")
    print(f"\n[Helper]: Created SQL Task Node ({filter_task_id})")
    # print("[Response JSON]: for Save Filter task ", res_filter.json())
    assert res_filter.status == 200
    return filter_task_id


def test_create_chained_sql_and_filter_workflow(
    playwright: Playwright, 
    get_token: str, 
    init_datasession: str):
    sql_task_id = add_sql_task(
        playwright=playwright,
        get_token=get_token,
        init_datasession=init_datasession
    )
    assert sql_task_id is not None

    # 2. Execute Filter Task creation helper using sql_task_id as previousTaskID
    filter_task_id = filter_task(
        playwright=playwright,
        get_token=get_token,
        init_datasession=init_datasession,
        previous_task_id=sql_task_id
    )
    assert filter_task_id is not None

    print(f"\n[Test Verified]: Successfully chained SQL ({sql_task_id}) -> Filter ({filter_task_id})")

    
    