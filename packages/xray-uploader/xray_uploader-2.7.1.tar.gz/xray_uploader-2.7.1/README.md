# Xray Uploader

## usage

- import as a module:
```
from xray import Uploader

result_file = "res.xml"
summary = "automation test"
project_id = "12345"
result_format = "junit"

upl = Uploader({client_id}, {client_secret})
upl.import_execution(result_file, summary, project_id, result_format)
```

- execute as a command
```
usage: xray-uploader [-h] -r RESULT -f FORMAT -pi PROJECTID -s SUMMARY [-ci CLIENTID] [-cs CLIENTSECRET] [-tp TESTPLAN] [-se] [-cr]

Upload test results to Xray.

options:
  -h, --help            show this help message and exit
  -r RESULT, --result RESULT
                        A result file with absolute path.
  -f FORMAT, --format FORMAT
                        Format of the result file. Valid formats are testng, junit, json
  -pi PROJECTID, --projectId PROJECTID
                        ID of the project where the test execution is going to be created.
  -s SUMMARY, --summary SUMMARY
                        Summary of the test execution.
  -ci CLIENTID, --clientId CLIENTID
                        Client ID to authorize if it is specified, otherwise will read from env CLIENT_ID.
  -cs CLIENTSECRET, --clientSecret CLIENTSECRET
                        Client secret to authorize if it is specified, otherwise will read from env CLIENT_SECRET.
  -tp TESTPLAN, --testPlan TESTPLAN
                        The tests will be added automatically to the test plan if it is specified.
  -se, --setEnv         Set azure pipeline environment "XRAY_EXECUTION_ID" with xray key.
  -cr, --checkResult    Check xray format of the result file.

```