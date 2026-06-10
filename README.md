# AccessiScan_AI_Platform

## Overview

AccessiScan AI is an accessibility auditing platform developed to support infrastructure inspectors, compliance officers, and researchers in assessing accessibility compliance against the Disability Standards for Accessible Public Transport (DSAPT).

The platform combines a FastAPI backend, SQLite database, and a custom-trained YOLOv8-Pose computer vision model to automate the detection and evaluation of accessibility infrastructure components such as ramps, stairs, tactile indicators, handrails, platform gaps, and accessibility signage.

The system processes uploaded inspection images, performs AI-powered accessibility analysis, generates compliance findings, and stores inspection records for future review and auditing.

---

# Repository Structure

```text
AccessiScan_AI_Platform/
│
├── main.py
├── LICENSE
├── .gitignore
├── requirements.txt
├── README.md
├── pytest.ini
│
├── accessiscan_backend/
│   ├── app/
│   └── tests/
│
└── accessiscan_engine/
    ├── accessiscan_dataset/
    ├── ai_engine.py
    ├── train_engine.py
    ├── models/
    └── scripts/
```

---

# Project Components

## main.py

The primary application entry point.

Responsibilities:

* Initializes the FastAPI application.
* Registers API routes.
* Configures startup events.
* Connects the backend and AI inference engine.
* Launches the AccessiScan platform.

---

## accessiscan_backend

The backend service responsible for API management, database operations, inspection workflows, and audit persistence.

### app/api/v1/

Contains versioned API endpoints.

#### inspections.py

Responsible for:

* Inspection image uploads
* File validation
* Inspection registration
* Background inference execution
* Retrieval of inspection and detection results

Primary endpoint:

```text
POST /api/v1/inspections/process-asset
```

---

### app/db/

#### session.py

Database session and engine management using SQLModel.

Responsibilities:

* Creates SQLite connections.
* Generates database tables during startup.
* Provides database session dependencies.

---
### app/models/

Contains the SQLModel entity definitions used by the AccessiScan persistence layer.

#### user.py

Defines user account records and administrative metadata used for user management and future access-control functionality.

#### inspection.py

Stores inspection metadata, including submitted accessibility audits, inspection status, timestamps, and associated records.

#### detection.py

Stores AI-generated accessibility detections, confidence scores, compliance findings, and relationships to inspections and images.

#### report.py

Stores audit report metadata and compliance assessment results generated during inspection processing.

#### image.py

Stores image metadata and maintains relationships between uploaded inspection assets and generated audit records.

Together, these entities form the relational persistence layer of the AccessiScan platform and enable inspection traceability, audit storage, and compliance reporting.

---

### app/core/

#### config.py

Centralized application configuration.

Responsibilities:

* Database configuration
* Model path configuration
* Environment settings
* Global application parameters

---

### app/utils/

Contains supporting services and utility components including:

* Inference integration services
* Report generation utilities
* Supporting business logic

---

### tests/

Automated testing suite.

Includes:

* API endpoint tests
* Database tests
* Inspection workflow tests
* Integration tests

---

## accessiscan_engine

Computer vision and accessibility auditing engine.

### train.py

Model training and retraining module.

Responsibilities:

- Loads the annotated YOLO dataset.
- Trains the YOLOv8-Pose model.
- Evaluates model performance.
- Generates updated model weights.
- Supports future model refinement and dataset expansion.

### ai_engine.py

Primary AI controller.

Responsibilities:

* Loads the trained YOLOv8-Pose model.
* Validates image inputs.
* Executes accessibility audits.
* Generates accessibility findings.
* Produces compliance outputs.

---

### scripts/detect.py

Core object detection and image annotation module.

Responsibilities:

* Object detection
* Landmark extraction
* Accessibility feature identification
* Image annotation

---

### scripts/storage_manager.py

Responsible for:

* Audit artifact generation
* JSON ledger creation
* Evidence image persistence

---

### scripts/system_utils.py

Provides runtime compatibility and environment configuration utilities.

---

# Models

Located within:

```text
accessiscan_engine/models/train/weights/
```

### best.pt

Primary YOLOv8-Pose model used for accessibility auditing.

### best.onnx

Optional ONNX model export used for deployment optimization and accelerated inference.

---

# Dataset

Located within:

```text
accessiscan_engine/accessiscan_dataset/
```

Contains the annotated training, validation, and testing datasets used during model development and evaluation.

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd AccessiScan_AI_Platform
```

---

## 2. Create a Virtual Environment

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

Install all required packages from the project root:

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

# Running the Platform

From the project root directory:

```bash
uvicorn main:app --reload
```

Alternatively:

```bash
python main.py
```

A successful startup should display messages similar to:

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete
```

---

# Swagger API Interface

Open a web browser and navigate to:

```text
http://127.0.0.1:8000/docs
```

The Swagger interface provides:

* Endpoint testing
* Request validation
* Response inspection
* API documentation

---

# Running an Accessibility Audit

1. Open the Swagger interface.
2. Expand:

```text
POST /api/v1/inspections/process-asset
```

3. Select **Try it out**.
4. Upload an inspection image.
5. Execute the request.

The platform will:

* Validate the uploaded image.
* Execute YOLOv8-Pose inference.
* Detect accessibility features.
* Evaluate compliance criteria.
* Store inspection data in SQLite.
* Generate audit findings and evidence imagery.

---

# Database

AccessiScan utilizes:

```text
SQLite + SQLModel
```

Database tables are automatically generated during application startup.

Core entities include:

* User
* Inspection
* Detection
* Report
* Image

The database file is stored locally as:

```text
accessiscan_backend/app.db
```

---

# Testing

Execute the automated test suite:

```bash
pytest
```

The testing framework validates:

* API endpoints
* Database functionality
* Inspection workflows
* Persistence operations
* Integration behaviour

---

# Technologies Used

* Python
* FastAPI
* SQLModel
* SQLite
* Uvicorn
* Ultralytics YOLOv8-Pose
* OpenCV
* NumPy
* Pydantic
* Pytest

---

# Current Project Status

AccessiScan AI is currently implemented as a Technology Readiness Level 3 (TRL 3) Proof of Concept.

Current capabilities include:

* Accessibility image auditing
* AI-powered feature detection
* Compliance assessment
* Audit evidence generation
* JSON audit ledger generation
* SQLite-based persistence

Future development will focus on:

* Dashboard-based user interfaces
* Mobile field-auditing support
* Automated PDF report generation
* Enhanced model accuracy through dataset expansion
* Real-time video auditing capabilities
* Expanded accessibility feature coverage
* Advanced compliance analytics and reporting
* Cloud deployment and scalability enhancements
