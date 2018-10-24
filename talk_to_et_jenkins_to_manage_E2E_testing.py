#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'talk_to_et_jenkins_to_manage_E2E_testing'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""
import re
import sys
import time
import logging
from CI3_python_realization.CI3_module.jenkins.talk_to_et_jenkins import TalkToETCI
from CI3_python_realization.CI3_module import basic_config


class TalkToETCIForE2E(TalkToETCI):
  """
  E2E Sub Testing Python Lib
  """

  def __init__(self, username, password, build_name, et_build_version, expected_run_time):
    """
    Launch one instance to connect ET E2E Basic Jenkins
    :param username: string  username to connect to Jenkins
    :param password: string  password for the username
    :param build_name: string  connect to which jenkins build
    :param expected_run_time: string  the time we expect one build will last
    """
    TalkToETCI.__init__(username, password, basic_config.ET_Jenkins, build_name, expected_run_time)
    self.et_build_version = et_build_version

  def check_console_log(self):
    """
    Based on the console log, get the final E2E testing report
    :return: list  [testing_result, testing_report_url]
    """
    console_log_url = self.get_the_latest_console_log_url()
    console_log_content = self.get_last_completed_build_console_log_content()
    testing_report_url = self.get_the_latest_cucumber_report_url()
    if console_log_content.find('Report:  /tmp/workspace/run-e2e/tests/Errata/results/report.html') < 0:
      logging.info("There is someting wrong. please check the log manually")
      logging.info("Console Log URL: %s", console_log_url)
      return "FAILED (unexpected error)", console_log_url
    else:
      logging.info("E2E has been finished")
      failed_cases_number = re.findall(r'[\d+]+ failed', console_log_content)[-1].split()[0]
      if int(failed_cases_number) != 0:
        logging.info("E2E testing has been FAILED")
        e2e_testing_result = "FAILED ({} cases failed)".format(failed_cases_number)
        return e2e_testing_result, testing_report_url
      else:
        logging.info("E2E testing has been PASSED")
        return "PASSED", testing_report_url

  def summary_report(self, e2e_testing_result, testing_report_url):
    """
    Summarize the final report for E2E testing
    :param e2e_testing_result: PASSED/FAILED
    :param testing_report_url: the exact testing report url(console log or cucumber report)
    :return: SUCCESS when the summary is ready
    """
    logging.info("========== Testing Report: Begin ==========")
    logging.info("Testing Type: E2E Testing")
    if self.et_build_version == "EMPTY":
      logging.info("RC Type: CD RC")
    else:
      logging.info("ET RC Version: %s", self.et_build_version)
      logging.info("RC Type: ET RC")
    logging.info("Testing Result: %s", e2e_testing_result)
    logging.info("Testing Report URL: %s", testing_report_url)
    logging.info("========== Testing Report: End ==========")
    return  "SUCCESS"

  def run_one_test(self):
    """
    Run E2E testing and summarize the final report
    :return: SUCCESS or other exit code during the whole process(run testing, monitor the testing,
    collect the testing result and show the result)
    """
    self.trigger_build({})
    time.sleep(30)
    self.check_the_lastest_running_job_finished_or_not()
    e2e_testing_result, testing_report_url = self.check_console_log()
    return self.summary_report(e2e_testing_result, testing_report_url)


if __name__ == "__main__":
  username = sys.argv[1]
  password = sys.argv[2]
  build_name = sys.argv[3]
  et_rc_version = ""
  expect_run_time = ""
  if len(sys.argv) == 5:
    et_rc_version = "EMPTY"
    expect_run_time = sys.argv[4]

  if len(sys.argv) == 6:
    et_rc_version = sys.argv[4]
    expect_run_time = sys.argv[5]

  e2e_rc_jenkins = TalkToETCIForE2E(username, password, build_name, et_rc_version, expect_run_time)
  e2e_rc_jenkins.run_one_test()
