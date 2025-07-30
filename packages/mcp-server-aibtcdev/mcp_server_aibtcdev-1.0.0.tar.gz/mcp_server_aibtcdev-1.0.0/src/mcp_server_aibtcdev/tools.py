"""
Tool implementations for the aibtcdev MCP server.

This module contains all the MCP tool implementations for interacting
with the aibtcdev-backend API.
"""

import json
from typing import Any, Dict, List, Optional

import httpx
from mcp.types import TextContent

from .settings import config


async def make_api_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    auth_type: str = "auto",
) -> Dict[str, Any]:
    """Make an authenticated API request"""
    if not config.has_auth():
        raise Exception(
            "No authentication credentials available. Set AIBTC_BEARER_TOKEN or AIBTC_API_KEY environment variables."
        )

    url = f"{config.base_url}{endpoint}"
    headers = config.get_auth_headers(auth_type)

    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = await client.post(
                    url, headers=headers, json=data, params=params
                )
            elif method.upper() == "PUT":
                response = await client.put(
                    url, headers=headers, json=data, params=params
                )
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
            try:
                error_data = e.response.json()
                if "message" in error_data:
                    error_msg = error_data["message"]
            except ValueError:
                pass
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"API request failed: {str(e)}")


# =============================================================================
# TRADING & FINANCE TOOLS
# =============================================================================


async def fund_wallet_testnet_stx(arguments: dict) -> List[TextContent]:
    """Fund wallet with testnet STX tokens from faucet"""
    try:
        result = await make_api_request("POST", "/tools/wallet/fund_testnet_faucet")
        return [
            TextContent(
                type="text",
                text=f"Testnet STX funding successful: {json.dumps(result, indent=2)}",
            )
        ]

    except Exception as e:
        return [
            TextContent(
                type="text", text=f"Error funding wallet with testnet STX: {str(e)}"
            )
        ]


async def fund_wallet_testnet_sbtc(arguments: dict) -> List[TextContent]:
    """Fund wallet with testnet sBTC tokens from Faktory faucet"""
    try:
        result = await make_api_request("POST", "/tools/faktory/fund_testnet_sbtc")
        return [
            TextContent(
                type="text",
                text=f"Testnet sBTC funding successful: {json.dumps(result, indent=2)}",
            )
        ]

    except Exception as e:
        return [
            TextContent(
                type="text", text=f"Error funding wallet with testnet sBTC: {str(e)}"
            )
        ]


# =============================================================================
# DAO MANAGEMENT TOOLS
# =============================================================================


async def create_dao_action_proposal(arguments: dict) -> List[TextContent]:
    """Create a DAO action proposal for sending a message"""
    required_fields = [
        "agent_account_contract",
        "action_proposals_voting_extension",
        "action_proposal_contract_to_execute",
        "dao_token_contract_address",
        "message",
    ]

    for field in required_fields:
        if not arguments.get(field):
            return [TextContent(type="text", text=f"Error: {field} is required")]

    try:
        data = {
            "agent_account_contract": arguments["agent_account_contract"],
            "action_proposals_voting_extension": arguments[
                "action_proposals_voting_extension"
            ],
            "action_proposal_contract_to_execute": arguments[
                "action_proposal_contract_to_execute"
            ],
            "dao_token_contract_address": arguments["dao_token_contract_address"],
            "message": arguments["message"],
        }

        if arguments.get("memo"):
            data["memo"] = arguments["memo"]

        result = await make_api_request(
            "POST", "/tools/dao/action_proposals/propose_send_message", data=data
        )
        return [
            TextContent(
                type="text",
                text=f"DAO action proposal created: {json.dumps(result, indent=2)}",
            )
        ]

    except Exception as e:
        return [TextContent(type="text", text=f"Error creating DAO proposal: {str(e)}")]


async def veto_dao_action_proposal(arguments: dict) -> List[TextContent]:
    """Veto an existing DAO action proposal"""
    dao_contract = arguments.get("dao_action_proposal_voting_contract")
    proposal_id = arguments.get("proposal_id")

    if not dao_contract or not proposal_id:
        return [
            TextContent(
                type="text",
                text="Error: dao_action_proposal_voting_contract and proposal_id are required",
            )
        ]

    try:
        data = {
            "dao_action_proposal_voting_contract": dao_contract,
            "proposal_id": proposal_id,
        }

        result = await make_api_request(
            "POST", "/tools/dao/action_proposals/veto_proposal", data=data
        )
        return [
            TextContent(
                type="text", text=f"DAO proposal vetoed: {json.dumps(result, indent=2)}"
            )
        ]

    except Exception as e:
        return [TextContent(type="text", text=f"Error vetoing DAO proposal: {str(e)}")]


async def generate_proposal_recommendation(arguments: dict) -> List[TextContent]:
    """Generate AI-powered proposal recommendations for a DAO"""
    dao_id = arguments.get("dao_id")
    if not dao_id:
        return [TextContent(type="text", text="Error: dao_id is required")]

    try:
        data = {"dao_id": dao_id}

        # Optional parameters
        optional_fields = ["focus_area", "specific_needs", "model_name", "temperature"]
        for field in optional_fields:
            if arguments.get(field):
                data[field] = arguments[field]

        result = await make_api_request(
            "POST", "/tools/dao/proposal_recommendations/generate", data=data
        )
        return [
            TextContent(
                type="text",
                text=f"Proposal recommendation generated: {json.dumps(result, indent=2)}",
            )
        ]

    except Exception as e:
        return [
            TextContent(
                type="text", text=f"Error generating proposal recommendation: {str(e)}"
            )
        ]


# =============================================================================
# AGENT ACCOUNT MANAGEMENT TOOLS
# =============================================================================


async def approve_contract_for_agent_account(arguments: dict) -> List[TextContent]:
    """Approve a contract for use with an agent account"""
    agent_account_contract = arguments.get("agent_account_contract")
    contract_to_approve = arguments.get("contract_to_approve")

    if not agent_account_contract or not contract_to_approve:
        return [
            TextContent(
                type="text",
                text="Error: agent_account_contract and contract_to_approve are required",
            )
        ]

    try:
        data = {
            "agent_account_contract": agent_account_contract,
            "contract_to_approve": contract_to_approve,
        }

        result = await make_api_request(
            "POST", "/tools/agent_account/approve_contract", data=data
        )
        return [
            TextContent(
                type="text",
                text=f"Contract approved for agent account: {json.dumps(result, indent=2)}",
            )
        ]

    except Exception as e:
        return [TextContent(type="text", text=f"Error approving contract: {str(e)}")]


# =============================================================================
# AI EVALUATION TOOLS
# =============================================================================


async def run_comprehensive_evaluation(arguments: dict) -> List[TextContent]:
    """Run comprehensive AI evaluation on a proposal"""
    proposal_id = arguments.get("proposal_id")
    if not proposal_id:
        return [TextContent(type="text", text="Error: proposal_id is required")]

    try:
        data = {"proposal_id": proposal_id}

        # Optional parameters
        optional_fields = [
            "proposal_content",
            "dao_id",
            "custom_system_prompt",
            "custom_user_prompt",
            "config",
        ]
        for field in optional_fields:
            if arguments.get(field):
                data[field] = arguments[field]

        result = await make_api_request(
            "POST", "/tools/evaluation/comprehensive", data=data
        )
        return [
            TextContent(
                type="text",
                text=f"Comprehensive evaluation completed: {json.dumps(result, indent=2)}",
            )
        ]

    except Exception as e:
        return [TextContent(type="text", text=f"Error running evaluation: {str(e)}")]
