"""
Health checker for ACOLYTE services
"""

import time
import requests
from typing import Dict, Any
from acolyte.core.logging import logger


class ServiceHealthChecker:
    """Health checker for ACOLYTE services"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.timeout = 120  # 2 minutos máximo

    def _check_service_once(self, service_name: str, port: int, endpoint: str) -> bool:
        """Check if a service is ready (single attempt)"""
        url = f"http://localhost:{port}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                # For health endpoint, also check the JSON status
                if endpoint == "/api/health":
                    try:
                        data = response.json()
                        status = data.get("status", "unknown")
                        # Accept both healthy and degraded as "ready"
                        is_ready = status in ["healthy", "degraded"]
                        if is_ready:
                            logger.info("Service ready", service=service_name, status=status)
                        return is_ready
                    except (ValueError, KeyError, requests.exceptions.JSONDecodeError):
                        # If can't parse JSON, assume it's not ready
                        return False
                return True
            return False
        except requests.RequestException:
            return False

    def _wait_for_service(self, service_name: str, port: int, endpoint: str) -> bool:
        """Generic method to wait for a service to be ready"""
        url = f"http://localhost:{port}{endpoint}"

        logger.info("Waiting for service", service=service_name)
        for attempt in range(self.timeout):
            try:
                # AUMENTAR TIMEOUT para health checks complejos
                # El endpoint /api/health puede tardar hasta 15s en checkear la DB
                timeout = 20 if endpoint == "/api/health" else 5
                response = requests.get(url, timeout=timeout)
                if response.status_code == 200:
                    # For health endpoint, check the actual status
                    if endpoint == "/api/health":
                        try:
                            data = response.json()
                            status = data.get("status", "unknown")
                            if status in ["healthy", "degraded"]:
                                if status == "degraded":
                                    logger.warning(
                                        "Service ready but degraded", service=service_name
                                    )
                                    # Get details about what's degraded
                                    services = data.get("services", {})
                                    for svc_name, svc_data in services.items():
                                        if svc_data.get("status") == "unhealthy":
                                            logger.warning(
                                                "Degraded service detail",
                                                service=svc_name,
                                                error=svc_data.get('error', 'unhealthy'),
                                            )
                                else:
                                    logger.info("Service ready and healthy", service=service_name)
                                return True
                            else:
                                # Status is not healthy or degraded, keep trying
                                logger.debug(
                                    "Service returned non-ready status",
                                    service=service_name,
                                    status=status,
                                )
                                # Continue to next iteration
                        except (ValueError, KeyError, requests.exceptions.JSONDecodeError) as e:
                            # If can't parse JSON, log and continue trying
                            logger.debug(
                                "Service JSON parse error", service=service_name, error=str(e)
                            )
                            # Continue to next iteration
                    else:
                        # For non-health endpoints, 200 means success
                        logger.info("Service ready", service=service_name)
                        return True
            except requests.RequestException:
                pass

            if attempt % 10 == 0:  # Show progress every 10 seconds
                logger.info(
                    "Health check attempt",
                    service=service_name,
                    attempt=attempt + 1,
                    timeout=self.timeout,
                )
            time.sleep(1)

        logger.error("Service failed to start", service=service_name, timeout=self.timeout)
        return False

    def wait_for_backend(self) -> bool:
        """Wait until backend is ready"""
        backend_port = self.config['ports']['backend']
        return self._wait_for_service("Backend", backend_port, "/api/health")

    def wait_for_weaviate(self) -> bool:
        """Wait until Weaviate is ready"""
        weaviate_port = self.config['ports']['weaviate']
        return self._wait_for_service("Weaviate", weaviate_port, "/v1/.well-known/ready")

    def wait_for_ollama(self) -> bool:
        """Wait until Ollama is ready"""
        ollama_port = self.config['ports']['ollama']
        url = f"http://localhost:{ollama_port}/api/tags"

        logger.info("Waiting for service", service="Ollama")
        for attempt in range(self.timeout):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    logger.info("Service ready", service="Ollama")
                    return True
            except requests.RequestException:
                pass

            if attempt % 10 == 0:  # Mostrar progreso cada 10 segundos
                logger.info(
                    "Health check attempt",
                    service="Ollama",
                    attempt=attempt + 1,
                    timeout=self.timeout,
                )
            time.sleep(1)

        logger.error("Service failed to start", service="Ollama", timeout=self.timeout)
        return False

    def check_all_services(self) -> Dict[str, bool]:
        """Verifica el estado de todos los servicios"""
        results = {}

        results['weaviate'] = self.wait_for_weaviate()
        results['ollama'] = self.wait_for_ollama()
        results['backend'] = self.wait_for_backend()

        return results
