import sys
import argparse
import time
import tempfile
import requests
import json
import os
import glob

try:
    from .junit_xml import JunitXml
except ImportError:
    from junit_xml import JunitXml

try:
    from .logger import logger
except ImportError:
    from logger import logger


class Uploader:
    TESTNG = 'testng'
    JUNIT = 'junit'
    JSON = 'json'
    VALID_FORMATS = (TESTNG, JUNIT, JSON)

    def __init__(self, client_id, client_secret):
        self._id = client_id
        self._secret = client_secret
        self._token = None

    def fetch_token(self):
        """
        Fetch the token from xray cloud server with client id and secret.
        :return:
        """
        auth_url = 'https://xray.cloud.getxray.app/api/v1/authenticate'
        cloud_auth = {
            'client_id': self._id,
            'client_secret': self._secret
        }
        logger.info('Try to get the token from server.')
        res = requests.post(url=auth_url, data=cloud_auth)
        assert res.status_code == 200, f"Expected status code 200, but got {res.status_code} with message:\n{res.text}"
        self._token = res.text.strip('"')
        logger.info('Get the token successfully.')

    @staticmethod
    def dump_info(info_json, execution_summary, project_id, testplan_id):
        """
        Compose the post info for the xray server, and write it to a json file.
        testplan_id is optional, if specified, the test execution will be added automatically to the test plan.
        """
        info = {
            'fields': {
                'project': {
                    'id': project_id
                },
                'summary': execution_summary,
                'issuetype': {
                    'id': '10221'
                }
            }
        }
        if testplan_id:
            info['xrayFields'] = {'testPlanKey': testplan_id}
        logger.info(f'Posted info:\n{info}')
        json.dump(info, open(info_json, 'w'), indent=4)

    def import_execution(self, res_file, execution_summary, project_id, res_format, testplan_id=''):
        """
        :param res_file: result file path
        :param execution_summary: test execution summary
        :param project_id: jira project id, string type.
        Can get it with the API: https://hexagon.atlassian.net/rest/api/latest/project/XX (XX is the alias of the project)
        :param testplan_id: test plan id, string type. This is optional, if specified, the test execution will be added automatically to the test plan.
        :param res_format: result format, string type
        """
        retry_times = 5
        retry_interval = 30
        try_index = 1
        while try_index <= retry_times:
            try:
                self.fetch_token()
                if res_format != self.JSON:
                    url = f'https://xray.cloud.getxray.app/api/v1/import/execution/{res_format}/multipart'
                else:
                    url = f'https://xray.cloud.getxray.app/api/v1/import/execution/multipart'
                headers = {
                    'Authorization': f'Bearer {self._token}'
                }
                info_json = os.path.join(os.path.dirname(__file__), 'info_temp.json')
                self.dump_info(info_json, execution_summary, project_id, testplan_id)
                files = {
                    'info': open(info_json, 'rb'),
                    'results': open(res_file, 'rb')
                }
                logger.info('Try to import test results into xray by creating a test execution')
                res = requests.post(url, headers=headers, files=files)
                assert res.status_code == 200, f"Expected status code 200, but got {res.status_code} with message:\n{res.text}"
                logger.info(f'Import the results into xray successfully. Response:\n{res.json()}')
                return res.json()
            except Exception as e:
                try_index += 1
                if try_index != retry_times:
                    logger.error(f'Failed to import the results into xray with error:\n{e}, \nwill retry in {retry_interval} seconds...')
                    time.sleep(retry_interval)
        else:
            logger.error(f'Failed to import the results into xray after {retry_times} times retry.')
            exit(1)


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, prog='xray-uploader',
                                     description='Upload test results to Xray.')

    parser.add_argument('-ci', '--clientId',
                        help='Client ID to authorize if it is specified, otherwise will read from env CLIENT_ID.')
    parser.add_argument('-cs', '--clientSecret',
                        help='Client secret to authorize if it is specified, otherwise will read from env CLIENT_SECRET.')

    parser.add_argument('-r', '--result', help='A result file with absolute path, if not specified, will try to query the unique one from the current working directory.')
    parser.add_argument('-f', '--format', required=True,
                        help=f'Format of the result file. Valid formats are {", ".join(Uploader.VALID_FORMATS)}')
    parser.add_argument('-tp', '--testPlan', default='',
                        help='The tests will be added automatically to the test plan if it is specified.')
    parser.add_argument('-pi', '--projectId', required=True,
                        help='ID of the project where the test execution is going to be created.')
    parser.add_argument('-s', '--summary', help='Summary of the test execution, if not specify, will use {PIPELINE_NAME}_{BUILD_VERSION}_{DATE_TIME} as default.')

    parser.add_argument('-se', '--setEnv', action='store_true', help='Set azure pipeline environment "XRAY_EXECUTION_ID" with xray key.')
    parser.add_argument('-cr', '--checkResult', action='store_true', help='Check xray format of the result file.')
    args, _ = parser.parse_known_args()

    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
        parser.print_help()
        sys.exit(0)
    else:
        args, _ = parser.parse_known_args()
        return vars(args)


def main_cli():
    args = parse_arguments()
    try:
        client_id = args.get('clientId') if args.get('clientId') is not None else os.environ['CLIENT_ID']
    except KeyError:
        logger.error('Either specifying "clientId" in the arguments or predefining the env var CLIENT_ID.')
        exit(1)
    try:
        client_secret = args.get('clientSecret') if args.get('clientSecret') is not None else os.environ['CLIENT_SECRET']
    except KeyError:
        logger.error('Either specifying "clientSecret" in the arguments or predefining the env var CLIENT_SECRET.')
        exit(1)

    assert args['format'] in Uploader.VALID_FORMATS, f'{args["format"]} is not supported now, valid formats are {", ".join(Uploader.VALID_FORMATS)}.'
    if args['summary'] is None:
        pipeline = os.environ["BUILD_DEFINITIONNAME"].split('_')[0] if os.getenv('BUILD_DEFINITIONNAME') else 'Unknown_Product'
        version = os.getenv('LATEST_VERSION', 'Unknown_Version')
        passed_summary = f'{pipeline}_{version}_{time.strftime("%Y-%m-%d_%H-%M-%S")}'
    else:
        passed_summary = args['summary']
    if args['result'] is None:
        results = glob.glob(os.path.join(os.getcwd(), 'output', 'results', 'py_result*.xml'))
        assert len(results) == 1, f'{results} length is not 1.'
        passed_result = results[0]
    else:
        assert os.path.isfile(args['result']), f'{args["result"]} is not a valid file path.'
        passed_result = args['result']

    uploader = Uploader(client_id, client_secret)
    if args.get('checkResult'):
        updated_result = passed_result.replace('py_result', 'xray_result')
        JunitXml(passed_result).dump_xray_format_xml(updated_result)
        passed_result = updated_result
    res_dict = uploader.import_execution(passed_result, passed_summary, args['projectId'], args['format'], args['testPlan'])

    if args.get('setEnv'):
        # Set the xray key to azure pipeline environment variable XRAY_EXECUTION_ID
        logger.info(f'The returned result from server is:\n{res_dict}')
        xray_key = res_dict.get('key', None)
        if xray_key is None:
            logger.warning('No xray key is returned from the server.')
            return
        logger.info(f'Set the xray key {xray_key} to azure pipeline environment "XRAY_EXECUTION_ID".')
        print(f'##vso[task.setvariable variable=XRAY_EXECUTION_ID]{xray_key}')
        # Also record the xray key into a temp file for later use.
        temp_info = os.path.join(tempfile.gettempdir(), 'XRAY_EXECUTION_ID')
        logger.info(f'Record the xray key {xray_key} into {temp_info}.')
        with open(temp_info, 'w') as f:
            f.write(xray_key)


if __name__ == '__main__':
    main_cli()
