import argparse
import logging
import sys

from exobrain.actions.client.accessor import ActionsAccessor
from exobrain.actions.client.http_client import ClientType, create_client

logger = logging.getLogger(__name__)

BASE_URL = "http://127.0.0.1:5001"


def run_demo(base_url: str = BASE_URL) -> None:
    # Create an HTTP client instance for the Exobrain Actions API
    client = create_client(ClientType.REQUESTS, base_url=base_url, timeout=10, verify=False)

    # Create an accessor instance to interact with the Exobrain Actions API
    accessor = ActionsAccessor(client)

    # Does the service respond to a ping?
    accessor.ping()
    logger.info("Ping successful: Exobrain Actions API is alive.")

    # Display the version status
    status = accessor.version_status()
    logger.info("Version Status: %s", status.status)
    logger.info("The service '%s' v%s is running on %s", status.service, status.version, base_url)
    logger.info("Git information: %s", status.git)

    # Display action data
    for service in (
        "alternate-supplier",
        "express-delivery",
        "full-container-deployment",
        "full-truck-load",
        "partial-delivery",
        "stock-rebalancing",
        "substitution",
        "agent-ai-procurement",
    ):
        data = accessor.get_action_data(service=service)
        logger.info("Action Data: %s", data.model_dump_json(indent=2, by_alias=True))

        # Example of calculating an action
        org_id = "5a8c76d9-eee0-4b74-9811-b427f272f8f9"
        action_id = "276728f4-3099-4ff5-b083-748478d15299"
        accessor.calculate(service=service, org_id=org_id, action_id=action_id)
        logger.info(
            "Calculation triggered for service '%s' with org_id '%s' and action_id '%s'.",
            service,
            org_id,
            action_id,
        )

        # Example of updating actuals
        kpis = {"RESPONSIVENESS": 0.85, "FLEXIBILITY": 0.72}
        accessor.update_actuals(service=service, org_id=org_id, action_id=action_id, kpis=kpis)
        logger.info(
            "Actuals updated for service '%s' with org_id '%s' and action_id '%s'.",
            service,
            org_id,
            action_id,
        )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    parser = argparse.ArgumentParser(description="Exobrain Actions API Demo Client")
    parser.add_argument(
        "--url",
        default=BASE_URL,
        help="Base URL for the Exobrain Actions API (default: %(default)s)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    if args.verbose:
        logger.info("Connecting to %s", args.url)

    run_demo(base_url=args.url)


if __name__ == "__main__":
    main()
