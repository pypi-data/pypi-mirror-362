"""
Main MCP server implementation for aibtcdev-backend API integration.

This module sets up the FastMCP server and registers tools.
"""

import logging
from typing import Annotated, Any, Dict, Optional

from fastmcp import Context, FastMCP
from pydantic import Field

from .tools import (
    approve_contract_for_agent_account,
    create_dao_action_proposal,
    fund_wallet_testnet_sbtc,
    fund_wallet_testnet_stx,
    generate_proposal_recommendation,
    run_comprehensive_evaluation,
    veto_dao_action_proposal,
)

logger = logging.getLogger(__name__)


class AibtcdevMCPServer(FastMCP):
    """
    A MCP server for aibtcdev-backend API integration.
    """

    def __init__(
        self,
        name: str = "mcp-server-aibtcdev",
        instructions: str | None = None,
        **settings: Any,
    ):
        super().__init__(name=name, instructions=instructions, **settings)
        self.setup_tools()

    def setup_tools(self):
        """
        Register the tools in the server.
        """

        async def fund_testnet_stx(ctx: Context) -> str:
            """
            Fund wallet with testnet STX tokens from faucet.
            :param ctx: The context for the request.
            :return: Result of the funding operation.
            """
            await ctx.debug("Funding wallet with testnet STX tokens")
            result = await fund_wallet_testnet_stx({})
            return result[0].text if result else "No response"

        async def fund_testnet_sbtc(ctx: Context) -> str:
            """
            Fund wallet with testnet sBTC tokens from Faktory faucet.
            :param ctx: The context for the request.
            :return: Result of the funding operation.
            """
            await ctx.debug("Funding wallet with testnet sBTC tokens")
            result = await fund_wallet_testnet_sbtc({})
            return result[0].text if result else "No response"

        async def create_dao_proposal(
            ctx: Context,
            agent_account_contract: Annotated[
                str, Field(description="Contract principal of the agent account")
            ],
            action_proposals_voting_extension: Annotated[
                str, Field(description="Contract principal for DAO action proposals")
            ],
            action_proposal_contract_to_execute: Annotated[
                str, Field(description="Contract principal of the action proposal")
            ],
            dao_token_contract_address: Annotated[
                str, Field(description="Contract principal of the DAO token")
            ],
            message: Annotated[
                str,
                Field(description="Message to be sent through the DAO proposal system"),
            ],
            memo: Annotated[
                Optional[str], Field(description="Optional memo for the proposal")
            ] = None,
        ) -> str:
            """
            Create a DAO action proposal for sending a message.
            :param ctx: The context for the request.
            :param agent_account_contract: Contract principal of the agent account.
            :param action_proposals_voting_extension: Contract principal for DAO action proposals.
            :param action_proposal_contract_to_execute: Contract principal of the action proposal.
            :param dao_token_contract_address: Contract principal of the DAO token.
            :param message: Message to be sent through the DAO proposal system.
            :param memo: Optional memo for the proposal.
            :return: Result of the proposal creation.
            """
            await ctx.debug(f"Creating DAO proposal with message: {message}")

            arguments = {
                "agent_account_contract": agent_account_contract,
                "action_proposals_voting_extension": action_proposals_voting_extension,
                "action_proposal_contract_to_execute": action_proposal_contract_to_execute,
                "dao_token_contract_address": dao_token_contract_address,
                "message": message,
            }
            if memo:
                arguments["memo"] = memo

            result = await create_dao_action_proposal(arguments)
            return result[0].text if result else "No response"

        async def veto_dao_proposal(
            ctx: Context,
            dao_action_proposal_voting_contract: Annotated[
                str, Field(description="Contract principal for DAO action proposals")
            ],
            proposal_id: Annotated[
                str, Field(description="ID of the proposal to veto")
            ],
        ) -> str:
            """
            Veto an existing DAO action proposal.
            :param ctx: The context for the request.
            :param dao_action_proposal_voting_contract: Contract principal for DAO action proposals.
            :param proposal_id: ID of the proposal to veto.
            :return: Result of the veto operation.
            """
            await ctx.debug(f"Vetoing DAO proposal: {proposal_id}")

            arguments = {
                "dao_action_proposal_voting_contract": dao_action_proposal_voting_contract,
                "proposal_id": proposal_id,
            }

            result = await veto_dao_action_proposal(arguments)
            return result[0].text if result else "No response"

        async def generate_dao_recommendation(
            ctx: Context,
            dao_id: Annotated[str, Field(description="The ID of the DAO")],
            focus_area: Annotated[
                Optional[str],
                Field(
                    description="Specific area of focus (default: general improvement)"
                ),
            ] = None,
            specific_needs: Annotated[
                Optional[str], Field(description="Specific needs or requirements")
            ] = None,
            model_name: Annotated[
                Optional[str], Field(description="LLM model to use (default: gpt-4.1)")
            ] = None,
            temperature: Annotated[
                Optional[float],
                Field(description="Temperature for LLM generation (default: 0.1)"),
            ] = None,
        ) -> str:
            """
            Generate AI-powered proposal recommendations for a DAO.
            :param ctx: The context for the request.
            :param dao_id: The ID of the DAO.
            :param focus_area: Specific area of focus.
            :param specific_needs: Specific needs or requirements.
            :param model_name: LLM model to use.
            :param temperature: Temperature for LLM generation.
            :return: Generated proposal recommendation.
            """
            await ctx.debug(f"Generating proposal recommendation for DAO: {dao_id}")

            arguments = {"dao_id": dao_id}
            if focus_area:
                arguments["focus_area"] = focus_area
            if specific_needs:
                arguments["specific_needs"] = specific_needs
            if model_name:
                arguments["model_name"] = model_name
            if temperature is not None:
                arguments["temperature"] = temperature

            result = await generate_proposal_recommendation(arguments)
            return result[0].text if result else "No response"

        async def approve_agent_contract(
            ctx: Context,
            agent_account_contract: Annotated[
                str, Field(description="Contract principal of the agent account")
            ],
            contract_to_approve: Annotated[
                str, Field(description="The contract principal to approve")
            ],
        ) -> str:
            """
            Approve a contract for use with an agent account.
            :param ctx: The context for the request.
            :param agent_account_contract: Contract principal of the agent account.
            :param contract_to_approve: The contract principal to approve.
            :return: Result of the approval operation.
            """
            await ctx.debug(
                f"Approving contract {contract_to_approve} for agent account {agent_account_contract}"
            )

            arguments = {
                "agent_account_contract": agent_account_contract,
                "contract_to_approve": contract_to_approve,
            }

            result = await approve_contract_for_agent_account(arguments)
            return result[0].text if result else "No response"

        async def run_evaluation(
            ctx: Context,
            proposal_id: Annotated[
                str, Field(description="Unique identifier for the proposal")
            ],
            proposal_content: Annotated[
                Optional[str], Field(description="Override proposal content")
            ] = None,
            dao_id: Annotated[
                Optional[str], Field(description="DAO ID for context")
            ] = None,
            custom_system_prompt: Annotated[
                Optional[str], Field(description="Custom system prompt")
            ] = None,
            custom_user_prompt: Annotated[
                Optional[str], Field(description="Custom user prompt")
            ] = None,
            config: Annotated[
                Optional[Dict[str, Any]],
                Field(description="Configuration for the evaluation agent"),
            ] = None,
        ) -> str:
            """
            Run comprehensive AI evaluation on a proposal.
            :param ctx: The context for the request.
            :param proposal_id: Unique identifier for the proposal.
            :param proposal_content: Override proposal content.
            :param dao_id: DAO ID for context.
            :param custom_system_prompt: Custom system prompt.
            :param custom_user_prompt: Custom user prompt.
            :param config: Configuration for the evaluation agent.
            :return: Result of the evaluation.
            """
            await ctx.debug(
                f"Running comprehensive evaluation for proposal: {proposal_id}"
            )

            arguments = {"proposal_id": proposal_id}
            if proposal_content:
                arguments["proposal_content"] = proposal_content
            if dao_id:
                arguments["dao_id"] = dao_id
            if custom_system_prompt:
                arguments["custom_system_prompt"] = custom_system_prompt
            if custom_user_prompt:
                arguments["custom_user_prompt"] = custom_user_prompt
            if config:
                arguments["config"] = config

            result = await run_comprehensive_evaluation(arguments)
            return result[0].text if result else "No response"

        # Register all tools
        self.tool(
            fund_testnet_stx,
            name="fund-wallet-testnet-stx",
            description="Fund wallet with testnet STX tokens from faucet",
        )

        self.tool(
            fund_testnet_sbtc,
            name="fund-wallet-testnet-sbtc",
            description="Fund wallet with testnet sBTC tokens from Faktory faucet",
        )

        self.tool(
            create_dao_proposal,
            name="create-dao-action-proposal",
            description="Create a DAO action proposal for sending a message",
        )

        self.tool(
            veto_dao_proposal,
            name="veto-dao-action-proposal",
            description="Veto an existing DAO action proposal",
        )

        self.tool(
            generate_dao_recommendation,
            name="generate-proposal-recommendation",
            description="Generate AI-powered proposal recommendations for a DAO",
        )

        self.tool(
            approve_agent_contract,
            name="approve-contract-for-agent-account",
            description="Approve a contract for use with an agent account",
        )

        self.tool(
            run_evaluation,
            name="run-comprehensive-evaluation",
            description="Run comprehensive AI evaluation on a proposal",
        )


# Create the MCP server instance
mcp = AibtcdevMCPServer()
