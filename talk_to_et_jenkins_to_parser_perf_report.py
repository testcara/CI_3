#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'talk_to_et_jenkins_to_parser_perf_report'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""
import os
import sys
import logging
from CI3_python_realization.CI3_module.jenkins.talk_to_et_jenkins import TalkToETCI
from CI3_python_realization.CI3_module import common_usage, basic_config
from CI3_python_realization.CI3_module.report_parser import performance_report_parser


class TalkToETJenkinsToParserPerfReport(TalkToETCI):
  """
  Talk to ET Performance Jenkins to get the direct result, then scp the original reports, finally parser them
  based on the exact tolernece and max_accepted_time to provide the final result.
  """
  def __init__(self, username, password, expected_build_version, tolerance, max_accepted_time,
               perf_jmeter_slave_server):
    """
    One parser instance to talk to Jenkins and Jmeter slave then provide the parser report
    :param username: string  username to connect to Jenkins
    :param password: string  password for the above username
    :param expected_build_version: string  the expected ET build version
    :param tolerance: string  the tolerance to check the regression is ok or not
    :param max_accepted_time: string  the max user accepted time
    :param perf_jmeter_slave_server: string   the Jmeter slave to run the performance testing
    """
    TalkToETCI.__init__(username, password, basic_config.ET_Jenkins, basic_config.perf_sub_ci_build_name, "")
    self.expected_build_version = expected_build_version
    self.tolerance = tolerance
    self.max_accepted_time = max_accepted_time
    self.perf_jmeter_slave_server = perf_jmeter_slave_server

  def scp_perf_builds_reports(self, testing_result_url):
    """
    :param testing_result_url: string  the original comparsion report url
    :return: list  the raw reports path we have got
    :rtype:
    """
    cu = common_usage.CommonUsage()
    cwd = os.getcwd()
    new_build, old_build = testing_result_url.split('/')[7], testing_result_url.split('/')[10]
    remote_perfomance_new_report_path = basic_config.perf_remote_base_path + str(
      new_build) + "/report/data/subreports/Performance.json"
    local_destination_new_report_path = cwd + "/new_performance.json"
    remote_perfomance_old_report_path = basic_config.perf_remote_base_path + str(
      old_build) + "/report/data/subreports/Performance.json"
    local_destination_old_report_path = cwd + "/old_performance.json"
    logging.info("Scp performance files:")
    logging.info("%s as %s", remote_perfomance_old_report_path, local_destination_old_report_path)
    logging.info("%s as %s", remote_perfomance_new_report_path, local_destination_new_report_path)
    cu.python_scp_get_files(self.perf_jmeter_slave_server, remote_perfomance_new_report_path,
                            local_destination_new_report_path)
    cu.python_scp_get_files(self.perf_jmeter_slave_server, remote_perfomance_old_report_path,
                            local_destination_old_report_path)
    return local_destination_new_report_path, local_destination_old_report_path

  def parser_and_comparsion_report(self, local_destination_new_report_path, local_destination_old_report_path):
    """
    Parser the local raw reports and do comparsion then output the detailed results
    :param local_destination_new_report_path: the path of the new report locally
    :param local_destination_old_report_path: the path of the old report locally
    :return: testing result will be returned
    """
    logging.info("Parsering the performance report")
    comparison_parser = performance_report_parser.PerformanceReportsComparison(local_destination_new_report_path,
                                                                               local_destination_old_report_path,
                                                                               self.tolerance,
                                                                               self.max_accepted_time)
    return comparison_parser.run_one_comparison()

  def summary_report(self, testing_result, testing_result_url):
    """
    Summary Report and Log them to Jenkins Console
    :param testing_result: the final performance testing result
    :param testing_result_url: the testing report url(console log or comparison report)
    :return: "SUCCESS" when the summary report is ready
    """
    logging.info("========== Testing Report: Begin ==========")
    logging.info(self.expected_build_version)
    logging.info("Testing Type: Performance Baseline Testing")
    logging.info("Testing Result: %s", testing_result)
    logging.info("Testing Result URL: %s", testing_result_url)
    logging.info("========== Testing Report: End ==========")
    return "SUCCESS"

  def parser_current_testing_result(self):
    """
    Collect the performance raw reports, parser them, get the real performance reports and output
    :return: 0 when the parser works well and the parser report is outputed
    """
    testing_report = self.get_test_report_from_console_log()
    testing_type, testing_result, testing_result_url = testing_report[0], testing_report[1], testing_report[2]
    current_build_version = self.get_current_version_from_console_log()
    if self.expected_build_version == current_build_version and testing_type == "Performance Baseline Testing":
      if testing_result == "FAILED":
        self.summary_report("FAILED (Unexpected Error)", testing_result_url)
      if testing_result == "FINISHED":
        local_destination_new_report_path, local_destination_old_report_path = self.scp_perf_builds_reports(
          testing_result_url)
        real_testing_result = self.parser_and_comparsion_report(local_destination_new_report_path,
                                                           local_destination_old_report_path)
        self.summary_report(real_testing_result, testing_result_url, )
    return "SUCCESS"


if __name__ == "__main__":
  username = sys.argv[1]
  password = sys.argv[2]
  expected_rc_version = sys.argv[3]
  tolerance = sys.argv[4]
  max_accepted_time = sys.argv[5]
  perf_jmeter_slave_server = sys.argv[6]
  perf = TalkToETJenkinsToParserPerfReport(username, password, expected_rc_version, tolerance, max_accepted_time,
                                           perf_jmeter_slave_server)
  perf.parser_current_testing_result()
