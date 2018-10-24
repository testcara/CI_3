#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'talk_to_et_jenkins_to_manage_TS2_testing'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""

import time
import re
import sys
import logging
from CI3_python_realization.CI3_module.jenkins.talk_to_et_jenkins import TalkToETCI
from CI3_python_realization.CI3_module import basic_config


class TalkToETCIForTS2(TalkToETCI):
  """
  TS2.0 Sub Testing Python Lib
  """
  def __init__(self, username, password, build_name, et_build_version, expected_run_time, coverage_testing=""):
    """
    Launch one instance to connect ET TS2.0 Basic Jenkins
    :param username: string  username to connect to Jenkins
    :param password: string  password for the username
    :param build_name: string  connect to which jenkins build
    :param expected_run_time: string  the time we expect one build will last
    :param coverage_testing: string  true/false to run the TS2.0 testing as coverage testing
    """
    TalkToETCI.__init__(username, password, basic_config.ET_Jenkins, build_name, expected_run_time)
    self.et_build_version = et_build_version
    self.coverage_testing = coverage_testing


  def check_console_log(self):
    """
    Based on the console log, get the final TS2.0 testing report
    :return: list  [testing_result, testing_report_url]
    """
    console_log_content = self.get_last_completed_build_console_log_content()
    console_log_url = self.get_the_latest_console_log_url()
    report_log_url = self.get_the_latest_cucumber_report_url()
    jobs_status_list = re.findall(r'status : [\w+]*', console_log_content)
    if len(jobs_status_list) < 5:
      logging.info("The Env Preparation meets some problem")
      return "FAILED", console_log_url
    elif jobs_status_list[4].find('FAILURE') > 0:
      logging.info("The Env Preparation has been finished")
      logging.info("The Cucumber TS2.0 UAT Testing is 'FAILED'")
      return "FAILED", report_log_url
    elif jobs_status_list[4].find('SUCCESS') > 0:
      logging.info("The Env Preparation has been finished")
      logging.info("The Cucumber TS2.0 UAT Testing PASSED")
      return "PASSED", report_log_url

  def summary_report(self, ts2_testing_result, testing_report_url):
    """
    Summarize the final report for TS2.0 testing
    :param ts2_testing_result: PASSED/FAILED
    :param testing_report_url: the exact testing report url(console log or cucumber report)
    :return: SUCCESS when the summary is ready
    """
    logging.info("========== Testing Report: Begin ==========")
    logging.info("ET RC Version: %s", str(self.et_build_version))
    logging.info("Testing Type: TS2.0 UAT Testing")
    logging.info("Testing Result: %s", ts2_testing_result)
    logging.info("Testing Report URL: %s", testing_report_url)
    logging.info("========== Testing Report: End ==========")
    return "SUCCESS"

  def run_one_test(self):
    """
    Run TS2.0 testing and summarize the final report
    :return: 0 or other exit code during the whole process(run testing, monitor the testing,
    collect the testing result and show the result)
    """
    self.trigger_build(
      {'RPM_BUILD_JOB_ID': self.et_build_version, 'IS_COVERAGE_NEEDED': self.coverage_testing})
    time.sleep(30)
    self.check_the_lastest_running_job_finished_or_not()

    ts2_testing_result, testing_report_url = self.check_console_log()
    return self.summary_report(ts2_testing_result, testing_report_url)


if __name__ == "__main__":
  username = sys.argv[1]
  password = sys.argv[2]
  build_name = sys.argv[3]
  et_rc_version = sys.argv[4]
  expect_run_time = sys.argv[5]
  talk_to_rc_jenkins = TalkToETCIForTS2(username, password, build_name, et_rc_version, expect_run_time)
  talk_to_rc_jenkins.run_one_test()
