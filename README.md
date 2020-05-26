[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/alanwill/aws-credy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/alanwill/aws-credy/context:python) [![CodeFactor](https://www.codefactor.io/repository/github/alanwill/aws-credy/badge)](https://www.codefactor.io/repository/github/alanwill/aws-credy) [![Maintainability](https://api.codeclimate.com/v1/badges/16a604124c7c9dc8a9f3/maintainability)](https://codeclimate.com/github/alanwill/aws-credy/maintainability) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/f178406375ff4d2abf7a616c6d020d7b)](https://www.codacy.com/manual/alanwill/aws-credy?utm_source=github.com&utm_medium=referral&utm_content=alanwill/aws-credy&utm_campaign=Badge_Grade)

# AWS Credy <!-- omit in toc -->

Credy is a simple utility for AWS SSO users using AWS CLI v2 with a need to keep their AWS credentials file updated with the latest profile STS credentials.

It's written in Python and all code is in this repo, however for ease of use you can download the latest binary directly from [here](https://github.com/alanwill/aws-credy/releases/latest).

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [macOS](#macos)
  - [Linux/Windows](#linuxwindows)
- [Sample Usage](#sample-usage)
- [Build](#build)

## Prerequisites

In order to use Credy you need to have the following steps completed:

1. Install the AWS CLI v2. Follow instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
2. Configure the AWS `config` file located in `~/.aws/config`. You can either update the file manually or run `aws sso login --profile my-dev-app` as explained [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html#sso-using-profile). A sample `config` file looks like:

   ```yaml
   [profile my-dev-app]
   sso_start_url = https://company.awsapps.com/start
   sso_region = us-east-1
   sso_account_id = 123456789012
   sso_role_name = AWSPowerUserAccess
   region = us-east-1
   [profile my-prod-app]
   sso_start_url = https://company.awsapps.com/start
   sso_region = us-east-1
   sso_account_id = 123456789013
   sso_role_name = AWSPowerUserAccess
   region = us-east-1
   ```

## Installation

Installation is pretty simple:

### macOS

1. Run the latest `aws-credy` binary [here](https://github.com/alanwill/aws-credy/releases/latest).
2. If you have Python 3.8 installed, you can clone this repo, run `aws-credy.py` and all required packages should automatically install.

### Linux/Windows

1. Clone this repo
2. Have Python 3.8 installed
3. Run `aws-credy.py` like `aws-credy.py --help`

## Sample Usage

```shell
❯ ./aws-credy --profile my-dev-app
Credentials for my-dev-app updated.
```

## Build

To create a binary build of Credy install the `PyInstaller` package and run `pyinstaller aws-credy.py --onefile --hidden-import="pkg_resources.py2_warn"`
