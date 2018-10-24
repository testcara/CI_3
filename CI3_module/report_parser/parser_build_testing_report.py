#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'parser_build_testing_report'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""

class ParserBuildTestingReport:
  """
  One parser to analyze the testing report, output the general result and brief summary
  """

  def __init__(self, content):
    self.content = content
    self._content_list = self.content.split("</tr>")
    self._testing_type_numbers = len(self._content_list) - 2
    self._failed_testing = []
    self._passed_testing = []
    self._inprocess_testing = []

  def _get_testing_type_and_result(self):
    # failed_testing = passed_testing = inprocess_testing = [] will raise unexpected problem.
    for index in range(1, len(self._content_list) - 1):
      testing_type = self._content_list[index].split("</td>")[0].split("<td>")[1]
      testing_result = self._content_list[index].split("</td>")[1].split("<td>")[1]
      if testing_result.find("FAILED") > -1:
        self._failed_testing.append(testing_type)
      elif testing_result.find("PASSED") > -1:
        self._passed_testing.append(testing_type)
      else:
        self._inprocess_testing.append(testing_type)

  def _summerize_general_testing_status(self):
    if len(self._passed_testing) == self._testing_type_numbers:
      return "PASSED"
    elif len(self._inprocess_testing) > 0:
      return "IN PROCESS"
    else:
      return "FAILED"

  def _get_testing_brief_and_summary(self):
    brief_summary = str(self._testing_type_numbers) + " testings: "

    if len(self._inprocess_testing) == 1:
      brief_summary += "1 testing in process({}). ".format(self._inprocess_testing[0])
    elif len(self._inprocess_testing) >= 2:
      brief_summary += " {} in process testings({}). ".format(
        str(len(self._inprocess_testing)), ', '.join(self._inprocess_testing))

    if len(self._failed_testing) == 1:
      brief_summary += "1 failed testing({}). ".format(self._failed_testing[0])
    elif len(self._failed_testing) >= 2:
      brief_summary += "{} failed testings({}). ".format(str(len(self._failed_testing))
                                                              , ", ".join(self._failed_testing))
    if len(self._passed_testing) == 1:
      brief_summary += "1 passed testing({}). ".format(self._passed_testing[0])
    elif len(self._passed_testing) >= 2:
      brief_summary += "{} passed testings({}). ".format(str(len(self._passed_testing))
                                                              , ", ".join(self._passed_testing))
    return brief_summary

  def get_final_status_and_brief(self):
    self._get_testing_type_and_result()
    return "{}-{}".format(self._summerize_general_testing_status(), self._get_testing_brief_and_summary())
