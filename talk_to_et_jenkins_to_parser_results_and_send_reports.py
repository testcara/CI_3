#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'parser_confulence_report_and_send_mail_report'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""
import sys
from CI3_python_realization.CI3_module.report_parser import parser_build_testing_report
from CI3_python_realization.CI3_module.jenkins import talk_to_et_jenkins_to_send_report
from CI3_python_realization.CI3_module.confluence import confluence_api_client


class ParserConfulenceReportAndSendMailReport:
  """
  Parser the general testing report and send the mail report out
  """
  def __init__(self, username, password, et_build_version, title, space, send_report_jenkins_name):
    """
    Launch one instance to paser the report and send mail
    :param username:
    :param password:
    :param et_build_version:
    :param title:
    :param space:
    :param send_report_jenkins_name:
    """
    self.username = username
    self.password = password
    self.et_build_version = et_build_version
    self.title = title
    self.space = space
    self.send_report_jenkins_name = send_report_jenkins_name

  def get_testing_report_content(self):
    """
    :return: string  the content of the testing report
    """
    connector = confluence_api_client.ConfluenceClient(self.username, self.password, self.title, self.space,
                                                   "", "")
    return connector.get_page_content()

  def get_result_and_summary_from_one_report_parser(self):
    """"""
    parser = parser_build_testing_report.ParserBuildTestingReport(self.get_testing_report_content())
    result,summary = parser.get_final_status_and_brief().split('-')
    return result, summary

  def send_report_out_with_result_and_summary(self):
    result, summary = self.get_result_and_summary_from_one_report_parser()
    send_reporter = talk_to_et_jenkins_to_send_report.TalkToETCIToSendReport(self.username, self.password,
                                                                          self.send_report_jenkins_name,
                                                                          self.et_build_version,
                                                                          result,
                                                                          summary,
                                                                          self.space)
    return send_reporter.run_to_send_report()


if __name__ == "__main__":
  username = sys.argv[1]
  password = sys.argv[2]
  et_build_version = sys.argv[3]
  title = sys.argv[4]
  space = sys.argv[5]
  send_report_jenkins_name = sys.argv[6]
  parser_and_sender = ParserConfulenceReportAndSendMailReport(username, password, et_build_version, title, space,
                                                              send_report_jenkins_name)
  parser_and_sender.send_report_out_with_result_and_summary()
