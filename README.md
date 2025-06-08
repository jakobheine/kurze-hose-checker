# Kurze Hose Checker - Alexa Skill 🩳

![Build Status](https://github.com/jakobheine/kurze-hose-checker/actions/workflows/cicd.yml/badge.svg)
![Coverage Status](https://codecov.io/gh/jakobheine/kurze-hose-checker/branch/main/graph/badge.svg?token=b481c683-4dd9-48c5-95c3-13289da7be67)
![LIVE](https://img.shields.io/badge/status-live-brightgreen)

This project implements an Alexa skill called **Kurze Hose Checker** ("Shorts Checker") that provides users with weather-based advice on whether they can wear shorts today at their postal code location in Germany. It integrates with Alexa device address APIs to get the user's postal code and uses the OpenRouter API for weather data, generating natural language responses.

---

## Features

- Automatically retrieves user’s postal code from Alexa device settings.
- Queries weather data for the specified postal code using OpenRouter.
- Returns a short, conversational answer on whether wearing shorts is appropriate today.
- Designed as an AWS Lambda function with Alexa SDK integration.

---

## Project Structure

- `src/khc/` - Application source code (handlers, services, clients).
- `test/` - Unit and integration tests.
- `requirements.txt` - Python runtime dependencies.
- `requirements-dev.txt` - Python development dependencies.
- `app.py` - Lambda entry point and skill setup.

---

## Prerequisites

- Python 3.13+
- AWS CLI and Lambda configured (optional for deployment)
- OpenRouter API key (sign up at https://openrouter.ai)
- Alexa Developer account (to enable device address permissions)

---

## Development Setup

Clone the repo and create a virtual environment:

```bash
git clone <repo_url>
cd kurze-hose-checker
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

## Running Tests and Coverage

Run tests with coverage reporting for source files in `src/`:

```bash
pytest --cov=src test/
```

This will output coverage info and show missing lines.
For line-by-line coverage details:

```zsh
pytest --cov=src --cov-report=term-missing test/
```

## Linting and Formatting

Use ruff to check and format code according to project style:
```zsh
ruff check src test
ruff format .
```

## Type Checking

Static type checks are done with Pyrefly:

```zsh
pyrefly check src test
```

## All in One
```zsh
ruff check src test --fix && pyrefly check src test && pytest --cov=src --cov-report=term-missing test/
```

## Deployment to AWS Lambda

Build and package the Lambda deployment ZIP from the project root:

```zsh
rm -rf package lambda_deployment_package.zip
mkdir package
pip install -r requirements.txt -t package/
cp -r src/khc package/
cp src/khc/app.py package/
cd package
zip -r ../lambda_deployment_package.zip .
cd ..
```

## Environment Variables

Set the OpenRouter API key for the skill:

- `OPENROUTER_API_KEY` - Your OpenRouter API key used in the weather service.

---

## Usage

After deploying and enabling the skill, users can ask Alexa whether they can wear shorts today by location. The skill will:

- Get the postal code from the Alexa device (requires permissions).
- Query weather via OpenRouter.
- Respond with a simple "Ja" or "Nein" answer tailored to the user's postal code.

---

## Troubleshooting

- Make sure the Alexa skill has permissions to read device address.
- Check API keys and environment variables are correctly set.
- Verify Lambda function logs in AWS CloudWatch for errors.
- Run tests locally to validate code changes.
