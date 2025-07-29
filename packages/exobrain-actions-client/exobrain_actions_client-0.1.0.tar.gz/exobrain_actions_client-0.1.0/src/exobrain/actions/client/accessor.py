from uuid import UUID

from exobrain.actions.client.http_client.interfaces import HTTPClientFacade
from exobrain.actions.schemas.action_data import ActionData
from exobrain.actions.schemas.version_info import VersionStatus


class ActionsAccessor:
    """
    Base class for accessing resources in the Exobrain Actions API.
    """

    def __init__(self, client: HTTPClientFacade) -> None:
        """
        Initialize the BaseAccessor with a client instance.

        :param client: An instance of the Client class.
        """
        self.client = client

    def version_status(self) -> VersionStatus:
        """
        Retrieve the version status of the Exobrain Actions API.

        :return: An instance of VersionStatus containing version details.
        """
        response = self.client.get("/")
        response.raise_for_status()
        json_data = response.json()
        return VersionStatus.model_validate(json_data)

    def ping(self) -> None:
        """
        Ping the Exobrain Actions API to check if it is alive.

        :raises HTTPStatusError: If the ping fails.
        """
        response = self.client.get("/health/ping")
        response.raise_for_status()

    def get_action_data(self, service: str = "") -> ActionData:
        """
        Retrieve action data for a specific service or the currently running service.

        Args:
            service: The service name (e.g., "alternate-supplier").
            If not provided, defaults to the currently running service.

        Returns:
            An instance of ActionData containing the action data.
        """
        params = {"service": service} if service else {}
        response = self.client.get("/actions/data", params=params)
        response.raise_for_status()
        return ActionData.model_validate(response.json())

    def calculate(self, service: str, org_id: str | UUID, action_id: str | UUID) -> None:
        """
        Trigger the calculation for a specific action.

        Args:
            service: The service name (e.g., "alternate-supplier").
            org_id: The organization ID.
            action_id: The action ID.
        """
        url = f"/{service}/organizations/{org_id}/actions/{action_id}"
        response = self.client.get(url)
        response.raise_for_status()

    def update_actuals(
        self,
        service: str,
        org_id: str | UUID,
        action_id: str | UUID,
        kpis: dict[str, float],
    ) -> None:
        """
        Update the KPIs for a specific action.

        Args:
            service: The service name (e.g., "alternate-supplier").
            org_id: The organization ID.
            action_id: The action ID.
            kpis: A dictionary containing the KPI data to update.
        """
        url = f"/{service}/organizations/{org_id}/actions/{action_id}/actuals"
        response = self.client.post(url, json=kpis)
        response.raise_for_status()
