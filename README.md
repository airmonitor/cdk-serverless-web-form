To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install --upgrade -r requirements.txt
$ pip install --upgrade -r requirements-dev.txt
$ pre-commit install
$ cd services/layers/frontend/python/lib/python3.9/site-packages
$ pip install -r requirements.txt -t .
$ cd services/layers/create_jira_task/python/lib/python3.9/site-packages
$ pip install -r requirements.txt -t .
$ cd services/layers/send_email_notification/python/lib/python3.9/site-packages
$ pip install -r requirements.txt -t .

```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

And deploy

```
$ cdk deploy
```


To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

# Documentation

Solution has been deployed to Shared & Management account (174334470447)
## Pre-requisites
* Create file ***cdk/config/dev/config.yaml*** with below content, replace account and region

```shell
  dev_aws_account: "11223344"
  dev_aws_region: "eu-central-1"
```


* Create file ***cdk/config/config-ci-cd.yaml*** with below content, replace necessary sections
```shell
    project: "cdk-serverless-web-form"
    aws_account: "11223344"
    aws_region: "eu-central-1"
    dev_aws_account: "11223344"
    dev_aws_region: "eu-central-1"
    repository: "cdk-serverless-web-form"
    ci_cd_notification_email: my.email@gmail.com
    alarm_emails:
      - my.emai@gmail.com
    slack_workspace_id: "" # CI/CD notifications through slack
    slack_channel_id: "" # CI/CD notifications through slack
    tags:
      Repo: "https://github.com/airmonitor/cdk-serverless-web-form"

```

## Deployment procedure
```shell
    cdk synth
    cdk deploy cdk-serverless-web-form-pipeline/dev-cdk-serverless-web-form-services-stage/frontend-service-stack
```
