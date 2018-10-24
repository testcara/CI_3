#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'talk_to_et_jenkins_to_send_report'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""
import time
import logging
from CI3_python_realization.CI3_module.jenkins.talk_to_et_jenkins import TalkToETCI
import CI3_python_realization.CI3_module.basic_config as basic_config


class TalkToETCIToSendReport(TalkToETCI):
  """
  Basic CI lib to send out report to mails
  """

  def __init__(self, username, password, build_name, et_build_version, status, brief_summary, space):
    """
    Launch one instance to connect ET Jenkins to send report
    :param username: string  username to connect to Jenkins
    :param password: string  password for the username
    :param build_name: string  connect to which jenkins build
    :param et_build_version: string  the ET build version like 3561
    :param status: string  one content of the mail,showing the general testing status of the current build testing
    :param brief_summary: string  one content of the mail, showing the brief summary of the current build testing
    :param space: string  one content of the report link as one content of the mail
    """
    TalkToETCI.__init__(username, password, basic_config.ET_Jenkins, build_name, "")
    self.space = space
    self.et_build_version = et_build_version
    self.status = status
    self.brief_summary = brief_summary

  def run_to_send_report(self):
    """
    Trigger the target Jenkins Job to send the report out
    :return: SUCCESS/exit code
    """
    logging.info("Start to send testing report")
    self.trigger_build(
      {'et_build_name_or_id': self.et_build_version, 'status': self.status, 'brief_summary': self.brief_summary,
       'space': self.space})
    time.sleep(30)
    if self.get_the_latest_testing_result() == "SUCCESS":
      logging.info("Completed to send testing report")
    return "SUCCESS"
