import requests
from typing import Optional, Dict, Any

class VerifyID:
    """
    Python SDK for interacting with the VerifyID.io API endpoints.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.verifyid.io"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Any:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def full_kyc_verification(
        self,
        front_image: str,
        selfie_image: str,
        back_image: Optional[str] = None,
        threshold: float = 0.6
    ) -> Any:
        payload = {
            "front_image": front_image,
            "selfie_image": selfie_image,
            "threshold": threshold
        }
        if back_image:
            payload["back_image"] = back_image
        return self._post("/kyc/full_verification", payload)

    def face_match(
        self,
        front_image: str,
        selfie_image: str,
        threshold: float = 0.6
    ) -> Any:
        payload = {
            "front_image": front_image,
            "selfie_image": selfie_image,
            "threshold": threshold
        }
        return self._post("/face-match", payload)

    def liveness_detection(self, image_base64: str) -> Any:
        payload = {"image_base64": image_base64}
        return self._post("/liveness-detection", payload)

    def deepfake_detection(self, image_base64: str) -> Any:
        payload = {"image_base64": image_base64}
        return self._post("/deepfake-detection", payload)

    def document_reader(
        self, image_front: str, image_back: Optional[str] = None
    ) -> Any:
        payload = {"image_front": image_front}
        if image_back:
            payload["image_back"] = image_back
        return self._post("/document-reader", payload)

    def credit_card_reader(self, image_base64: str) -> Any:
        payload = {"image_base64": image_base64}
        return self._post("/credit-card-reader", payload)

    def barcode_reader(self, image_base64: str) -> Any:
        payload = {"image_base64": image_base64}
        return self._post("/barcode-reader", payload)

    def aml_pep_crime_checker(
        self,
        name: Optional[str] = None,
        entity: Optional[int] = None,
        country: Optional[str] = None,
        dataset: Optional[str] = None
    ) -> Any:
        payload = {}
        if name is not None:
            payload["name"] = name
        if entity is not None:
            payload["entity"] = entity
        if country is not None:
            payload["country"] = country
        if dataset is not None:
            payload["dataset"] = dataset
        return self._post("/aml-pep-crime-checker", payload)
