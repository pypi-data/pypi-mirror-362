import xml.etree.ElementTree as ET

try:
    from .logger import logger
except ImportError:
    from logger import logger


class JunitXml:
    def __init__(self, file_path: str):
        self._root = ET.parse(file_path).getroot()

    def dump_xray_format_xml(self, out_path):
        """
        Remove tests that do not contain the required 'test_key' property, or value of 'test_key' is empty.
        :param out_path:
        :return:
        """
        for test_suite in self._root.findall('testsuite'):
            for test_case in test_suite.findall('testcase'):
                properties_ele = test_case.find('properties')
                # If there is no properties element, remove the test case because it does not contain the required 'test_key' property.
                # missing "test_key" results in a new xray test case being created, which is not desired.
                if properties_ele is None:
                    logger.warning(f'{test_case.attrib} is going to be removed.')
                    test_suite.remove(test_case)
                else:
                    property_ele = properties_ele.find('property')
                    attrs = property_ele.attrib
                    try:
                        assert attrs['name'] == 'test_key'
                        assert attrs['value']
                    except AssertionError:
                        logger.warning(f'{test_case.attrib} is going to be removed.')
                        test_suite.remove(test_case)
        tree = ET.ElementTree(self._root)
        tree.write(out_path)
