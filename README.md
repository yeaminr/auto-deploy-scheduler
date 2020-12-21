# auto-deploy-scheduler
A Python Flask application that works as a central deployment scheduler server for on-prem clients

## Auto deployment solution

Given the increasing number of clients with on-prem environments, we have decided to start automating the deployment process to minimize the effort required to guarantee Anna is released continuously across our environments. 

Deployments are still triggered manually but can now be scheduled in advance, requiring the deployer only to observe as to guarantee a pain-free deployment.

Auto deployment runs a client script in all on-premise servers calling a lambda app in AWS to check for newly released versions and triggers deployments automatically when necessary.
<br/>
<br/>

## Auto Deployment Client.

The environments listed below run the auto deployment client script on a recurring schedule.
```shell
/opt/hyperanna/bin/run-deploy.sh
```
This script performs the following tasks:

* Obtains the deployed release on the current environment.
* Calls auto deploy server to check what should be the release for the current environment.
* Triggers a deployment with the new release when the expected version is newer.
* Notifies appropriate slack channels that a new release was triggered.

## Current schedule

All environments currently run the script once a day at `1800` hours on their local timezone.

The following environments have auto-deploy client script running with the respective timezone configurations:

| Environment | Timezone     | Australia/Sydney Timezone |
| :-----------| :----------: | --------------------:     |
| Açaí        | UTC          | No                        |
| Guava       | UTC+08:00    | No                        |
| Grapes      | UTC+11:00    | Yes                       |
| Bayberry    | UTC          | No                        |
| Prod SG     | UTC          | No                        |
 
<br/>
<br/>

## Deployment schedule file

On-Premise deployment is controlled by the deployment schedule file `deployment_schedule.json`. This file contains a list of multiple environments and their expected release.\
Currently, only the fields `environment` and `release` are being used. The field `deploy_time` it's ignored.

In the future, `deploy_time` will control when deployment gets triggered in the environment, meaning `not before` the listed time.

```json
[
    {
        "environment": "<env-name>",
        "release": "<RELEASE>",
        "deploy_time": "2020-01-01:00:00"
    } ...
]  
```

## Deployment oversight and debugging.

Even though deployment is becoming more automated, the expectation for the deployer is to ensure environments get the latest release on a regular schedule, and that potential deployment issues are addressed accordingly when needed. It's important to consider timezone differences and downtime when scheduling deployments for on-prem environments.

To help deployers work with auto deployment, notifications, health checks, and logging has been introduced. It's important to use them to guarantee a smooth deployment process.

## Auto deployment notifications
Check slack channel `#deployment` with the following messages to understand what is happening with auto deployment:

### Deployment started
```
Auto-deployer APP  18:13
Deploying RELEASE_2020.12.16.06.12.07.00 in ip-10-219-132-29 of analytics.nai.transport.nsw.gov.au ...
```

### Deployment finished successfully.
```
Deployer APP  18:19
####### Pacemaker reports All containers are Healthy after Deployment of RELEASE_2020.12.16.06.12.07.00 in ip-10-219-132-29 of analytics.nai.transport.nsw.gov.au :) #######
```

### Deployment finished with failure.
```
Deployer APP  18:25
!!!! @here These containers are Unhealthy after Deployment of RELEASE_2020.12.11.02.42.45.00 in anna02 of beta.hyperanna.com :
[{'subjectName':'dtect-content-api','checks':{'healthy':'false','status':'unreachable','msg':'Connection refused'}}]
```
<br/>

## Debugging auto deployment client.

In the event a deployment is not triggered on the expected schedule, please check the following log file in the on-prem environment for potential issues:
```shell
/var/log/run-deploy.log
```

#
## How To Deploy A New Release to Environments

### Cloning project locally 

1. Clone this repo into your local machine:
```shell
git clone git@github.com:hyperanna01/auto-deploy-scheduler.git
```

2. Modify the JSON file `deployment_schedule.json`, edit the `release` field value to the release you want to deploy. i.e. `RELEASE_2020.12.08.08.00.50.00`.

3. git push back to remote. 

<br/>
A circleci pipeline will deploy the changes into an AWS Lambda deployment that is running a Python Flask webserver. 

On the next scheduled calls comming from auto deployment client script the new release will be deployment for the updated environments. 

Deployers are not required to use pull request / pair review process to trigger deployments; however, pair review can be a helpful tool for critical deployments,  especially when issues arise. 
