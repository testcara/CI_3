import logging
from CI3_python_realization.CI3_module.jenkins.talk_to_et_jenkins import TalkToETCI
from CI3_python_realization.CI3_module import basic_config
from CI3_python_realization.CI3_module.pub_pulp_collections import get_all_pub_pulp_product_version_content


class GenerateBuildReportContent:
  """
  Generte the exact build report for the specific build
  """
  logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

  def __init__(self, username, password, build_name, et_build_version):
    """
    :param username: username to connect with Jenkins then to get the report from the Jenkins console log
    :param password: password of the above username
    :param build_name: the Jenkins build name
    :param et_build_version: the Errata Tool build version like 3354, CI will check whether the Jenkins run is for the build.
    """
    self.username = username
    self.password = password
    self.build_name = build_name
    self.et_build_version = et_build_version
    self._et_ci_jenkins = TalkToETCI(self.username, self.password, basic_config.ET_Jenkins, self.build_name)
    self._test_report = self._et_ci_jenkins.get_test_report_from_console_log()
    self._current_build_version = self._et_ci_jenkins.get_current_version_from_console_log()

  def _update_e2e_env_with_pub_pulp(self):
    '''
		:return: e2e enviroment content
		:rtype: basestring
		'''
    get_pub_pulp_content = get_all_pub_pulp_product_version_content.GetAllPubPulpVersionContent(self.username,
                                                                                                self.password)
    pub_pulp_versions = get_pub_pulp_content.get_all_pub_pulp_content()
    e2e_env = basic_config.e2e_env + pub_pulp_versions
    return e2e_env

  def _generate_test_report_row_html(self):
    """
    :return: the test report html
    """
    if self.build_name.find("E2E") >= 0:
      basic_config.e2e_env = self._update_e2e_env_with_pub_pulp()
      basic_config.env_map['E2E Testing'] = basic_config.e2e_env
    test_type = self._test_report[0]
    test_table_row_content_body = ""
    for item in self._test_report:
      if item == "PASSED":
        test_table_row_content_body += "<td>" + "<strong><span style='color: rgb(0,128,0);'>" + item + "</span></strong>" + "</td>"
      if item.find("FAILED") > -1:
        test_table_row_content_body += "<td>" + "<strong><span style='color: rgb(255,0,0);'>" + item + "</span></strong>" + "</td>"
      if item == "IN PROGRESS":
        test_table_row_content_body += "<td>" + "<strong><span style='color: rgb(255,204,0);'>" + item + "</span></strong>" + "</td>"
      if item.find("http") > -1:
        test_table_row_content_body += "<td>" + "<a href='" + item + "'>" + item + "</a>" + "</td>"
      if item.find("Testing") > -1 and item.find("http") < 0:
        test_table_row_content_body += "<td>" + item + "</td>"
    test_table_row_content_body += "<td>" + basic_config.env_map[test_type] + "</td>"
    test_report_row_html = "<tr>" + test_table_row_content_body + "</tr>"
    return test_report_row_html

  def generate_report_for_expected_build_version(self):
    '''
    :return: the test report for the expected build version of the specific testing type
    :rtype: basestring
    '''
    test_report_html = ""
    if self.et_build_version == self._current_build_version:
      logging.info("The latest build version is the expected build version! Generating report for the build: %s",
                   self.build_name)
      test_report_html = self._generate_test_report_row_html()
      logging.info("The report is:\n%s", test_report_html)
      logging.info("Generated successfully, Cheers!")
    else:
      logging.info("Expected Build Version: %s", self.et_build_version)
      logging.info("The Lastest Build Version: %s", self._current_build_version)
      logging.warning("The latest job is not for the expected build, will not generate report for the build: %s",
                      self.build_name)
    return test_report_html
