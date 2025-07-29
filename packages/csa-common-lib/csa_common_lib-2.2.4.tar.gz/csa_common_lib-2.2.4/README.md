# PSR_LIBRARY

The PSR Library is the core framework for calculating relevance-based prediction models and managing interactions with AWS Lambda functions. It includes several modules ranging from core math functions to end-user APIs and internal tools to support the operation of Cambridge Sports Analytics' prediction models.

## Repository Structure

The repository is structured into several key components:

### Key Directories

- **`_aws_layers/`**: Contains the AWS Lambda layers needed for dependencies such as Python packages to be used in Lambda functions.
  
- **`csa_common_lib/`**: A collection of common utilities and helper functions that can be reused across different modules in the repository, including shared classes, validation utilities, and enumerations.

- **`csanalytics/`**: The package intended for the end-user interaction, primarily to interface with Cambridge Sports Analytics' prediction engine API. It provides functions to call predictive models, fetch results, and handle user data.

- **`csanalytics_local/`**: Internal tools used for development and infrastructure management, meant for use by CSA engineers.

- **`lambda_functions/`**: Contains various AWS Lambda functions that handle job processing, submission, and results retrieval. These functions facilitate interaction with the PSR models through serverless operations.
  
  - **`accessid_usage_handler/`**: Lambda function for handling access ID usage.
  - **`filter_response/`**: Lambda function for filtering responses from job results.
  - **`get_accessid_usage/`**: Retrieves access ID usage statistics.
  - **`get_apikey_usage/`**: Retrieves API key usage statistics.
  - **`get_job_results/`**: Fetches results of a job from the server.
  - **`post_job/`**: Submits a job to the PSR prediction engine.
  - **`process_job/`**: Processes a job and manages its state.
  - **`start_state_machine_psr/`**: Starts an AWS Step Functions state machine to manage long-running jobs.

- **`psr/`**: The main library where core mathematical modules are implemented. This is the heart of the PSR system, containing the math and algorithms for relevance-based predictions.

- **`psr_lambda/`**: Helper functions and utilities for managing AWS Lambda functions specifically for PSR-related tasks. This package helps with the deployment and orchestration of Lambda functions for running predictions.

## Getting Started

### Cloning the Repository
To get started, clone this repository using:

```bash
git clone https://github.com/CambridgeSportsAnalytics/PSR_LIBRARY.git
```

### Setting Up Your Environment

The repository includes various packages and functions that require dependencies for AWS Lambda and Python packages. Make sure you have the necessary Python environment set up, and install required dependencies using:

```bash
pip install -r requirements.txt
```

### Running Lambda Functions

To interact with AWS Lambda functions, you can navigate to the lambda_functions/ directory and deploy the functions using the AWS CLI or your preferred deployment method (e.g., AWS SAM or Serverless Framework).

## Documentation

For full documentation on each module and function, refer to the inline docstrings and module-specific README files located within each subdirectory. You can contact Cel Kulasekaran or Logan Waien for technical inquiries.

## License

(c) 2023 - 2024 Cambridge Sports Analytics, LLC. All rights reserved.
