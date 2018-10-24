#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'talk_to_et_jenkins_to_parser_perf_report'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""
import time
import re
import os
import sys
import logging
from CI3_python_realization.CI3_module.jenkins.talk_to_et_jenkins import TalkToETCI
from CI3_python_realization.CI3_module import basic_config


class TalktoPerfCI(TalkToETCI):
  """
  Connect to Perf Jenkins and do some basic actions
  """
  default_build_number_to_compare = basic_config.default_build_number_to_compare

  def __init__(self, username, password, build_name, et_build_version, expected_run_time=""):
    """
     Launch one instance to connect Perf Jenkins
     :param username: string  username to connect to Jenkins
     :param password: string  password for the username
     :param build_name: connect to which jenkins build
     :param expected_run_time: the time we expect one build will last
     """
    TalkToETCI.__init__(username, password, basic_config.Perf_Jenkins, build_name, expected_run_time)
    self.et_build_version = et_build_version


  def get_the_latest_console_log_url(self):
    """
    Get the console log URL of latest Jenkins build
    :return: string  the perf console log URL
    """
    return "{}/view/ET/job/{}/{}/console".format(basic_config.Perf_Jenkins, self.build_name, str(
      self.get_the_lastest_running_build_number()))


  def get_comparison_report_url(self):
    """
    Get the performance comparison report URL
    :return:
    :rtype:
    """
    return "{}/view/ET/job/{}/performance-report/comparisonReport/{}/monoReport#!/report/_/Perf-build_{}_vs_{}/perfcharts-simple-perfcmp".format(
      basic_config.Perf_Jenkins, self.build_name, self.get_last_completed_build_number(),
      basic_config.default_build_number_to_compare, self.get_last_completed_build_number(), str(
        self.default_build_number_to_compare))

  def check_console_log(self):
    """
     Based on the console log, get the final performance testing report
     :return: list  [testing_result, testing_report_url]
     """
    console_log_content = self.get_the_lastest_running_build_number()
    logging.info("Checking the console log to make sure the testing is running well")
    error_item = re.findall(r'Err: [\d+\\.]+', console_log_content)
    comparison_report_url = self.get_comparison_report_url()
    console_report_url = self.get_the_latest_console_log_url()
    for error in error_item:
      if error.split()[1] > 20:
        logging.info("There is something wrong shown in the console log, please check manually")
        return "FAILED", console_report_url
      else:
        continue
    logging.info("The perf testing has been done")
    return "FINISHED", comparison_report_url

  def summary_report(self, perf_testing_result, testing_report_url):
    """
    Summarize the final report for performance testing
    :param perf_testing_result: PASSED/FAILED
    :param testing_report_url: the exact testing report url(console log or performance comparison report)
    :return: "SUCCESS" when the summary is ready
    """
    logging.info("========== Testing Report: Begin ==========")
    logging.info("ET RC Version: %s", self.et_build_version)
    logging.info("Testing Type: Performance Baseline Testing")
    logging.info("Testing Result: %s", perf_testing_result)
    logging.info("Testing Report URL: %s ", testing_report_url)
    logging.info("========== Testing Report: End ==========")

  def run_one_test(self):
    """
    Run performance testing and summarize the final report
    :return: 0 or other exit code during the whole process(run testing, monitor the testing,
    collect the testing result and show the result)
    """
    self.trigger_build({'ET_SERVER': basic_config.ET_Perf_Server, 'Stub_Server': basic_config.ET_Stub_Server,
                        'ET_DB': basic_config.ET_DB_Server})
    time.sleep(30)
    self.check_the_lastest_running_job_finished_or_not()
    perf_testing_result, testing_report_url = self.check_console_log()
    self.summary_report(perf_testing_result, testing_report_url)


if __name__ == "__main__":
  testing_type = sys.argv[1]
  perf_expect_run_time = sys.argv[2]
  username = os.environ.get('ET_Perf_User') or sys.argv[3]
  password = os.environ.get('ET_Perf_User_Password') or sys.argv[4]
  et_rc_version = sys.argv[-1]
  if testing_type == "smoke":
    talk_to_jenkinks_smoke = TalktoPerfCI(username, password, "ET_Baseline_PDI_MIN", 5, et_rc_version)
    talk_to_jenkinks_smoke.run_one_test()
  if testing_type == "full_perf":
    talk_to_jenkinks_smoke = TalktoPerfCI(username, password, "ET_Baseline_PDI", perf_expect_run_time,
                                          et_rc_version)
    talk_to_jenkinks_smoke.run_one_test()
  if testing_type == "all":
    talk_to_jenkinks_smoke = TalktoPerfCI(username, password, "ET_Baseline_PDI_MIN", 5, et_rc_version)
    talk_to_jenkinks_smoke.run_one_test()
    talk_to_jenkinks_smoke = TalktoPerfCI(username, password, "ET_Baseline_PDI", 80, et_rc_version)
    talk_to_jenkinks_smoke.run_one_test()
