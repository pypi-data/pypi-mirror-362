from unittest.mock import Mock

from exobrain.actions.client.accessor import ActionsAccessor
from exobrain.actions.client.http_client.interfaces import HTTPClientFacade, HTTPResponse
from exobrain.actions.schemas.action_data import ActionData

ACTION_DATA = {
    "actionSettings": {
        "V_CO2": {
            "choice": True,
            "defaultValue": "M_SQUARE_PER_M_CUBE",
            "name": "VOLUME_CO2",
            "required": None,
            "type": None,
        }
    },
    "dataNeeded": {
        "CONTEXT": {
            "ITEM_CODE": {"TYPE": "STRING"},
            "LOCATION_CODE": {"TYPE": "STRING"},
            "QUANTITY_AT_RISK": {"TYPE": "STRING"},
        },
        "INPUTS": {
            "ITEM_MASTER": {
                "CATEGORY": "MASTER",
                "ITEM_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "ITEM_DESCRIPTION": {"IS_TAGGABLE": True, "REQUIRED": False, "TYPE": "STRING"},
                "ITEM_TYPE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "TYPE": "OBJECT",
                "UNIT_PER_PALLET": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER"},
                "WEIGHT_PER_UNIT_IN_KG": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER_W_KG"},
            },
            "LOCATION_ITEM_MASTER": {
                "CATEGORY": "MASTER",
                "DAYS_OF_SUPPLY_THRESHOLD": {"IS_TAGGABLE": True, "REQUIRED": False, "TYPE": "NUMBER_T_DAYS"},
                "ITEM_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "LOCATION_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "STANDARD_COST_PER_UNIT": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "AMOUNT"},
                "TYPE": "OBJECT",
            },
            "LOCATION_MASTERS": {
                "CATEGORY": "MASTER",
                "LOCATION_CITY": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "LOCATION_CONTACT_NAME": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "LOCATION_COUNTRY": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "LOCATION_DESCRIPTION": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "LOCATION_ID": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "LOCATION_PRIMARY_LANGUAGE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "LOCATION_TYPE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "LOCATION_ZIP_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "TYPE": "ARRAY",
            },
            "PROCUREMENT_INTERNAL_ROUTES": {
                "CATEGORY": "ACTION_CONTEXT_VIEW",
                "CO2_EMISSION_PER_KG_SHIPPED": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER_CO2_PER_KG"},
                "COST_PER_UNIT_CURRENCY": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "AMOUNT"},
                "DISTANCE_KM": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER_D_KM"},
                "LEAD_TIME_DAYS": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER_T_DAYS"},
                "MODE_OF_TRANSPORTATION": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "OTIF_PERCENT": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER"},
                "RECEIVING_LOCATION": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "ROUTE_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "ROUTE_DESCRIPTION": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "SHIPPING_LOCATION_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "TYPE": "OBJECT",
            },
            "PROCUREMENT_PO_CONDITION": {
                "CATEGORY": "ACTION_CONTEXT_VIEW",
                "CO2_EMISSION": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER_V_CO2"},
                "CONDITION_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "CONDITION_DESCRIPTION": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "COST_PER_UNIT_CURRENCY": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "AMOUNT"},
                "LEAD_TIME_DAYS": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER_T_DAYS"},
                "MODE_OF_TRANSPORTATION": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "RECEIVING_LOCATION_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "SUPPLIER_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "TYPE": "OBJECT",
            },
            "PROCUREMENT_PURCHASE_ORDER": {
                "CATEGORY": "ACTION_CONTEXT_VIEW",
                "CREATION_DATE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "DATE"},
                "DELIVERY_DATE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "DATE"},
                "ITEM_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "LINE_NUMBER": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "LINE_VALUE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "NUMBER": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "PURCHASE_COST_PER_UNIT": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "AMOUNT"},
                "QUANTITY": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER"},
                "RECEIVING_LOCATION_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "SHIPPING_DATE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "DATE"},
                "STANDARD_INBOUND_ROUTE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "STATUS": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "SUPPLIER_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "TYPE": "OBJECT",
                "UNIT_OF_MEASURE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
            },
            "PROCUREMENT_SHIPPING_CONDITIONS": {
                "CATEGORY": "ACTION_CONTEXT_VIEW",
                "CO2_EMISSION": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER_V_CO2"},
                "CONDITION_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "CONDITION_DESCRIPTION": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "COST_PER_UNIT_CURRENCY": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "AMOUNT"},
                "LEAD_TIME_DAYS": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER_T_DAYS"},
                "MODE_OF_TRANSPORTATION": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "OTIF_PERCENT": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER"},
                "RECEIVING_LOCATION_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "SUPPLIER_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "TYPE": "OBJECT",
            },
            "PROCUREMENT_SUBSTITUTION": {
                "ALTERNATE_COST_PER_UNIT": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "AMOUNT"},
                "ALTERNATE_SUPPLIER_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "ALTERNATE_SUPPLIER_COUNTRY_OF_ORIGIN": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "CATEGORY": "ACTION_CONTEXT_VIEW",
                "ITEM_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "LOCATION_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "SUBSTITUTE_ITEM_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "SUBSTITUTION_QUANTITY_RATIO": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER"},
                "SUPPLIER_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "TYPE": "ARRAY",
                "UNIT_OF_MEASURE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
            },
        },
        "OUTPUTS": {
            "AGENT_AI_ACTION_DETAILS": {
                "ACTION": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "CATEGORY": "ACTION_DETAILS",
                "EXPLANATION": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "SCORE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "TYPE": "OBJECT",
            },
            "AGENT_AI_IMPACT": {
                "CATEGORY": "RISK_IMPACTS",
                "DELIVERY_DATE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "DATE"},
                "LOCATION_CODE": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "STRING"},
                "QUANTITY_AT_RISK": {"IS_TAGGABLE": True, "REQUIRED": True, "TYPE": "NUMBER"},
                "TYPE": "OBJECT",
            },
        },
    },
    "kpis": ["FLEXIBILITY", "RELIABILITY", "RESPONSIVENESS"],
    "name": "AGENT_AI_PROCUREMENT",
    "reasons": [
        "f218957f-65a1-49c5-954a-4b1028c495ab",
        "83b0f297-2c44-4bd1-a2cf-2a051fe53fc7",
        "74972e98-f150-48a1-9f9a-030ca5d192d8",
    ],
}


class TestActionsAccessor:
    def test_version_status(self) -> None:
        version_status = {
            "status": "ok",
            "service": "exobrain-actions",
            "version": "1.2.3",
            "git": {
                "commit": "abc123",
                "branch": "main",
                "date": "2023-10-01T12:27:00Z",
            },
        }
        mock_response = Mock(spec=HTTPResponse, json=Mock(return_value=version_status), raise_for_status=Mock())
        mock_client = Mock(spec=HTTPClientFacade, get=Mock(return_value=mock_response))
        accessor = ActionsAccessor(client=mock_client)
        actual = accessor.version_status()
        assert actual.status == "ok"
        assert actual.service == "exobrain-actions"
        assert actual.version == "1.2.3"
        assert actual.git.commit == "abc123"
        assert actual.git.branch == "main"
        assert actual.git.date == "2023-10-01T12:27:00Z"
        assert mock_client.get.call_count == 1
        assert mock_client.get.call_args[0][0] == "/"

    def test_ping(self) -> None:
        mock_response = Mock(spec=HTTPResponse, raise_for_status=Mock())
        mock_client = Mock(spec=HTTPClientFacade, get=Mock(return_value=mock_response))
        accessor = ActionsAccessor(client=mock_client)
        accessor.ping()
        assert mock_client.get.call_count == 1
        assert mock_client.get.call_args[0][0] == "/health/ping"

    def test_get_action_data(self) -> None:
        mock_response = Mock(spec=HTTPResponse, json=Mock(return_value=ACTION_DATA), raise_for_status=Mock())
        mock_client = Mock(spec=HTTPClientFacade, get=Mock(return_value=mock_response))
        accessor = ActionsAccessor(client=mock_client)
        actual = accessor.get_action_data(service="agent-ai-procurement")
        assert actual == ActionData.model_validate(ACTION_DATA)
        assert mock_client.get.call_count == 1
        assert mock_client.get.call_args[0][0] == "/actions/data"

    def test_calculate(self) -> None:
        mock_response = Mock(spec=HTTPResponse, raise_for_status=Mock())
        mock_client = Mock(spec=HTTPClientFacade, get=Mock(return_value=mock_response))
        accessor = ActionsAccessor(client=mock_client)
        accessor.calculate(service="alternate-supplier", org_id="1234567890", action_id="1234567890")
        assert mock_client.get.call_count == 1
        assert mock_client.get.call_args[0][0] == "/alternate-supplier/organizations/1234567890/actions/1234567890"

    def test_update_actuals(self) -> None:
        mock_response = Mock(spec=HTTPResponse, raise_for_status=Mock())
        mock_client = Mock(spec=HTTPClientFacade, post=Mock(return_value=mock_response))
        accessor = ActionsAccessor(client=mock_client)
        accessor.update_actuals(
            service="alternate-supplier",
            org_id="1234567890",
            action_id="1234567890",
            kpis={"RESPONSIVENESS": 0.85, "FLEXIBILITY": 0.72},
        )
        assert mock_client.post.call_count == 1
        assert (
            mock_client.post.call_args[0][0]
            == "/alternate-supplier/organizations/1234567890/actions/1234567890/actuals"
        )
        assert mock_client.post.call_args[1]["json"] == {"FLEXIBILITY": 0.72, "RESPONSIVENESS": 0.85}
