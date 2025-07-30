"""portfolio_catalogue.py

Client wrapper for interacting with the Portfolio-Catalogue Service API.

This module exposes `PortfolioCatalogue`, a thin abstraction over the
shared :class:`bw_essentials.services.api_client.ApiClient` that collates
all URL templates and common logic required to communicate with the
Portfolio-Catalogue micro-service responsible for portfolio construction
and rebalancing operations.

Features
--------
- Centralised mapping of service endpoints.
- Uniform request/response logging using the shared API client helper.
- Simple, type-hinted public interface that hides low-level HTTP calls.

Example
-------
>>> from bw_essentials.services.portfolio_catalogue import PortfolioCatalogue
>>> client = PortfolioCatalogue(service_user="system")
>>> data = {
  "portfolioId": "BASKE_e3f7fc",
  "startDate": "2025-07-01",
  "endDate": "2025-07-10",
  "status": "active",
  "createdBy": "KP",
  "constituents": [
    {
      "symbol": "EROSMEDIA",
      "weight": 0.5,
      "isin": "INE416L01017",
      "status": "active",
      "rationale": "Hello"
    },
    {
      "symbol": "IDEA",
      "weight": 0.5,
      "isin": "INE669E01016",
      "status": "active",
      "rationale": "Hello"
    }
  ]
}
>>> response = client.create_rebalance(json=data)
>>> print(response)
"""

import logging
from typing import Optional, Dict, Any

from bw_essentials.constants.services import Services
from bw_essentials.services.api_client import ApiClient

logger = logging.getLogger(__name__)


class PortfolioCatalogue(ApiClient):
    """High-level client for the Portfolio-Catalogue Service.

    This class bundles together the logic for generating fully-qualified
    endpoint URLs and executing authenticated HTTP requests for
    portfolio rebalancing workflows.

    Attributes
    ----------
    base_url : str
        Resolved base URL for the Portfolio-Catalogue service obtained
        from configuration or environment variables.
    name : str
        Canonical service identifier used for logging and telemetry.
    urls : dict[str, str]
        Mapping of human-readable keys to relative endpoint paths.
    """

    def __init__(self, service_user: str):
        super().__init__(user=service_user)
        self.base_url = self.get_base_url(Services.PORTFOLIO_CATALOGUE.value)
        self.name = Services.PORTFOLIO_CATALOGUE.value
        self.urls = {
            "rebalance": "rebalance",
        }

    def create_rebalance(self, json: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Submit a rebalance request.

        Parameters
        ----------
        json : dict
            Request payload describing the rebalance parameters and
            portfolio metadata.

        Returns
        -------
        dict
            Parsed JSON response returned by the service.
        """
        logger.info("In - create_rebalance %s", json)
        data = self._post(
            url=self.base_url,
            endpoint=self.urls["rebalance"],
            json=json,
        )
        logger.info("%s", data)
        return data
