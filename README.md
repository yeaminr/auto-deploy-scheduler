# auto-deploy-scheduler
A Python Flask application that works as a central deployment scheduler server for onprem clients

### How To Deploy A New Release to Environments

1. Clone this repo into your local machine:
git clone git@github.com:hyperanna01/auto-deploy-scheduler.git

2. Modify the JSON file `deployment_schedule.json`, edit the `release` field value to the release you want to deploy. i.e. `RELEASE_2020.12.08.08.00.50.00`.

3. git push back to remote. 

A circleci pipeline will deploy the changes into an AWS Lambda deployment that is running a Python Flask webserver. A bash script running in crontab of the onprem environments query this webserver and if the Release suggested back in response to the query is later than the current Release they have, deployment happens.

 