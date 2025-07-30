# VerifyID Python SDK

[![PyPI - Version](https://img.shields.io/pypi/v/verifyid.svg)](https://pypi.org/project/verifyid/)

Official Python SDK for [VerifyID.io](https://api.verifyid.io) – seamless integration for KYC, AML, biometric, and document verification.

---

## Features

- **Multi-Platform Integration:** Works in any Python 3.7+ project.
- **All VerifyID Endpoints:** KYC, Face Match, Liveness, Deepfake, OCR, Credit Card/Barcode Reader, AML/PEP/Crime.
- **Modern & Simple:** Clean API with type hints and helpful error handling.

---

## Installation

**Via pip (recommended):**
```bash
pip install verifyid-sdk-python
```
## From Source
```bash
git clone https://github.com/OmniSolInfoTech/verifyid-sdk-python.git
cd verifyid-python-sdk
pip install .
```
## Usage
```bash
from verifyid import VerifyID

sdk = VerifyID("YOUR_API_KEY")

# Full KYC Verification
response = sdk.full_kyc_verification(front_image_b64, selfie_image_b64, back_image_b64)

# Face Match
response = sdk.face_match(front_image_b64, selfie_image_b64)

# Liveness Detection
response = sdk.liveness_detection(selfie_image_b64)

# Deepfake Detection
response = sdk.deepfake_detection(selfie_image_b64)

# Document OCR
response = sdk.document_reader(front_image_b64, back_image_b64)

# Credit Card Reader
response = sdk.credit_card_reader(credit_card_image_b64)

# Barcode Reader
response = sdk.barcode_reader(barcode_image_b64)

# AML/PEP/Crime Check
response = sdk.aml_pep_crime_checker(name="John Doe", entity=0, country="ZA", dataset="all")
```
### All images must be base64 encoded:
```bash
import base64
with open("selfie.jpg", "rb") as f:
    selfie_image_b64 = base64.b64encode(f.read()).decode()
```

## Endpoints Supported
* Full KYC Verification
* Face Match
* Liveness Detection
* Deepfake Detection
* Document Reader (OCR)
* Credit Card Reader
* Barcode Reader
* AML/PEP/Crime Checker

## Testing
```bash
pip install -e .[dev]
python -m unittest discover tests
```


