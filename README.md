# Architecture
## Public:
![image](https://raw.githubusercontent.com/airmonitor/cdk-serverless-web-form/main/architecture/public.png)

## Private:
(not included in this repository)
![image](https://raw.githubusercontent.com/airmonitor/cdk-serverless-web-form/main/architecture/private.png)


# Working example

https://cdk-serverless-web-form.airmonitor.pl/

![website](https://raw.githubusercontent.com/airmonitor/cdk-serverless-web-form/main/architecture/website.png)

# Pre-requisites
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
      - my.email@gmail.com
    slack_workspace_id: "" # CI/CD notifications through slack
    slack_channel_id: "" # CI/CD notifications through slack
    tags:
      Repo: "https://github.com/airmonitor/cdk-serverless-web-form"

```

# Deployment
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

```shell
    cd services/layers/frontend/python/lib/python3.9/site-packages
    pip install --upgrade -r requirements.txt -t .
    cdk synth
    cdk deploy cdk-serverless-web-form-pipeline/dev-cdk-serverless-web-form-services-stage/frontend-service-stack

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
