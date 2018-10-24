#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'talk_to_et_jenkins'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""
import jenkins
import re
import time
import logging


class TalkToETCI:
  """
  Connect to ET Jenkins and do some basic actions
  """

  def __init__(self, username, password, jenkins_name, build_name, expected_run_time=""):
    """
    Launch one instance to connect ET Jenkins
    :param username: username to connect to Jenkins
    :param password: password for the username
    :param jenkins_name: Jenkins URL to be connected to
    :param build_name: connect to which jenkins build
    :param expected_run_time: the time we expect one build will last
    """
    self.username = username
    self.password = password
    self.build_name = build_name
    self.expected_run_time = expected_run_time
    self.jenkins_name = jenkins_name
    self._server = jenkins.Jenkins(self.jenkins_name, username=username, password=password)

  def get_last_completed_build_number(self):
    """
    Get the latest completed build number of the exact Jenkins build
    :return: int  the number of the Jenkins lastComplatedBuild
    """
    return self._server.get_job_info(self.build_name)['lastCompletedBuild']['number']

  def get_last_completed_build_console_log_content(self):
    """
    Get the console log of the latest Jenkins build job
    :return: string  the console log of the Jenkins build
    """
    last_completed_build_number = self.get_last_completed_build_number()
    return self._server.get_build_console_output(self.build_name, last_completed_build_number)

  def get_current_version_from_console_log(self):
    """
    Get the current version from the console log. In fact, we output some reports in the console logs
    :return: string  ET version like 3354
    """
    console_log_content = self.get_last_completed_build_console_log_content()
    current_build_version_list = re.findall(r'ET RC Version: [\w+ \\.]+', console_log_content)
    if len(current_build_version_list) > 0:
      current_build_version = current_build_version_list[0].split(':')[-1].strip()
    else:
      current_build_version = "NULL"
    return current_build_version

  def get_the_lastest_running_build_number(self):
    """
    Get the latest running build number
    :return: int  build number
    """
    return self._server.get_job_info(self.build_name)['lastBuild']['number']

  def get_test_report_from_console_log(self):
    """
    Collect the testing type, testing result and testing result urls as the testing report
    :return: list  [testing_type testing_result, testing_result_url]
    """
    console_log_content = self.get_last_completed_build_console_log_content() or ""
    testing_type = re.findall(r'Testing Type: [\w+ \\.]+', console_log_content)[0].replace("Testing Type: ", "") or ""
    testing_result = "" or re.findall(r'Testing Result: [\w+ \\.]+', console_log_content)[0].replace("Testing Result: ",
                                                                                                    "") or ""
    testing_result_url = "" or re.findall(r'Testing Report URL: [^\n]+', console_log_content)[0].replace(
      "Testing Report URL: ", "").replace("'", "") or ""
    testing_report = [testing_type, testing_result, testing_result_url]
    return testing_report

  def get_the_latest_testing_result(self):
    """
    Get the result of latest Jenkins build
    :return: string  "SUCCESS/FAILED/ABORTED"
    """
    latest_build_number = self.get_the_lastest_running_build_number()
    return self._server.get_build_info(self.build_name, latest_build_number)['result']

  def get_the_latest_console_log_url(self):
    """
    Get the console log URL of latest Jenkins build
    :return: string  the console log URL like ET_Jenkins/job/ET_Builds_Testing_Pipeline/48/console
    """
    latest_build_number = self.get_the_lastest_running_build_number()
    return "{}/job/{}/{}/console".format(self.jenkins_name, self.build_name, str(latest_build_number))

  def stop_the_latest_running_build(self):
    """
    Stop the latest Jenkins build
    :return: int the stop_build function return code
    """
    latest_build_number = self.get_the_lastest_running_build_number()
    return self._server.stop_build(self.build_name, latest_build_number)

  def check_the_lastest_running_job_finished_or_not(self):
    """
    Monitor the running Jenkins job. If it is kept too long, we abort it automatically.
    :return: string  the job result
    """
    for i in range(2):
      time.sleep(int(self.expected_run_time) * 60)
      if not self.get_the_latest_testing_result():
        logging.info("The job is still running")
        continue
      else:
        logging.info("The job has been finished")
        break
    if not self.get_the_latest_testing_result():
      logging.info("The testing is running too long, we would stop the job manually")
      self.stop_the_latest_running_build()
      testing_result = "FAILED"
    else:
      testing_result = self.get_the_latest_testing_result()
    return testing_result

  def trigger_build(self, *args):
    """
    Trigger Jenkins job with the specific parameters
    :param args: *args  parameters for Jenkins build job
    :return: int  exit code of build_job function
    """
    return self._server.build_job(self.build_name, args)

  def get_the_latest_cucumber_report_url(self):
    """
    Get the cucumber report URL of the latest Jenkins build
    :return: string  cucumber report
    """
    latest_build_number = self.get_the_lastest_running_build_number()
    return "{}/job/{}/{}/cucumber-html-reports/overview-features.html".format(self.jenkins_name, self.build_name,
                                                                              str(latest_build_number))
