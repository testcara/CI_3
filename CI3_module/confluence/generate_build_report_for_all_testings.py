#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'generate_build_report_for_all_testings'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""
import logging
import CI3_python_realization.CI3_module.confluence.generate_build_report_for_one_testing
from CI3_python_realization.CI3_module import basic_config


class GenerateAllReports:
  logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

  def __init__(self, username, password, expected_build_version):
    self.username = username
    self.password = password
    self.expected_build_version = expected_build_version

  @staticmethod
  def generate_head_row_html():
    """
    :return: string head_row_html of the table of the report content
    """
    table_column = ['Test Type', 'Test Result', 'Test Result Url', 'Test Enviroment']
    head_row = ""
    for column_name in table_column:
      head_row += "<th colspan='1'>" + column_name + "</th>"
    head_row_html = "<tr>" + head_row + "</tr>"
    return head_row_html

  def generate_all_reports(self):
    general_report = ""
    for testing in basic_config.testing_jenkins_result_builds_map.keys():
      one_report_content_generator = auto_testing_CI.CI3_module.confluence.generate_build_report_for_one_testing.GenerateBuildReportContent(self.username,
                                                                                                                                            self.password,
                                                                                                                                            basic_config.testing_jenkins_result_builds_map[
                                                                                                        testing],
                                                                                                                                            self.expected_build_version)
      one_report = one_report_content_generator.generate_report_for_expected_build_version()
      general_report = general_report + one_report
    return general_report

  @staticmethod
  def format_all_content(head_row, general_report):
    general_report_content = "<table><tbody>" + head_row + general_report + "</tbody></table>"
    report_note_1 = "<p>The report is generated by CI_3(ET QE Build Testing CI[1]) automatically.</p>"
    report_note_2 = "<p>Note that 'PASSED' of 'Performance Baseline Testing' means the performance of current build is ok to release[2]. For others, 'PASSED' means all testing cases are passed.</p>"
    report_footer_1 = "<p>[1] ET QE Build Testing CI is one QE CI to track all processes of build testings, including enviroment preparation, testing, results collection and reports by on click.</p>"
    report_footer_2 = "<p>[2] 'ok to release' here means:</p>"
    report_footer_3 = "<p>     1. There is no obvious performance fallback of the current build.</p>"
    report_footer_4 = "<p>     2. There is few obvious (>20%) performance fallback. But QE has confirmed it will not block the release </p>"
    report_footer_5 = "<p>Anything about the reports or the testings, you can join #qe-bne or send mail to 'errata-qe-team' for help.</p>"
    report_beginning = report_note_1 + report_note_2
    report_ending = report_footer_1 + report_footer_2 + report_footer_3 + report_footer_4 + report_footer_5
    general_reports_content = report_beginning + "<p></p>" + general_report_content + "<p></p>" + report_ending
    return general_reports_content

  def run_one_generator(self):
    logging.info("Begin to generate report for all testing types!")
    head_row = self.generate_head_row_html()
    general_report = self.generate_all_reports()
    logging.info("Generated reports successfully, Cheers!")
    all_content = self.format_all_content(head_row, general_report)
    logging.info("The general report content is: \n%s", all_content)
    return all_content
