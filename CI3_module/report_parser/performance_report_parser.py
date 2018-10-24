#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'performance_report_parser'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""

import json
from CI3_python_realization.CI3_module import common_usage
import logging

class SinglePerformanceReportParser:
  """
  Parser one raw performance report to get the regression transactions
  """

  def __init__(self, input_file):
    """
    :param input_file: file  the raw jmeter performance report file
    """
    one_common_usage = common_usage.CommonUsage()
    one_common_usage.check_file_exist(input_file)
    perf_file = open(input_file, 'r')
    perf_file_list = perf_file.readlines()
    perf_file.close()
    print(perf_file_list[0])
    perf_file_json = json.loads(perf_file_list[0])
    print(perf_file_json)
    self._perf_summary = perf_file_json['charts'][0]
    self._transactions = []
    self._transactions_time = []

  def _get_all_transactions(self):
    for items in self._perf_summary['rows']:
      transaction = items[0]['value']
      if transaction:
        self._transactions.append(transaction)

  def _get_all_transactions_average_time(self):
    for items_time in self._perf_summary['rows']:
      # get the 90% Line data to do the comparison, the comparison result
      # should be more correct than those shown in the perfci
      transaction_time = items_time[4]['value']
      if str(transaction_time):
        self._transactions_time.append(transaction_time)

  def run_single_report_parser(self):
    self._get_all_transactions()
    self._get_all_transactions_average_time()
    return dict(zip(self._transactions, self._transactions_time))


class PerformanceReportsComparison():
  def __init__(self, report_1, report_2, tolerance, max_accepted_time):
    self._parsered_report_1 = SinglePerformanceReportParser(report_1).run_single_report_parser()
    self._parsered_report_2 = SinglePerformanceReportParser(report_2).run_single_report_parser()
    self._worsen_transactions = {}
    self.tolerance = tolerance
    self.max_accepted_time = max_accepted_time

  def _compare_reports(self):
    if self._parsered_report_2.keys() == self._parsered_report_1.keys():
      logging.info("=== The Transactions are kept the same ===")
      logging.info("=== Comparing the reports ===")
      self._get_worsen_transactions()
    else:
      logging.info("=== The transactions are different this time ===")
      logging.info("=== Will not do the comparison ====")

  def _get_worsen_transactions(self):
    logging.info("== I am filtering out the block transactions if its time exceeds the max_accepted_time and its fallback overs the tolerance")
    for transaction in self._parsered_report_2.keys():
      new_time = self._parsered_report_1[transaction]
      old_time = self._parsered_report_2[transaction]

      if new_time > old_time and new_time > float(self.max_accepted_time):
        increment = float(new_time) - float(old_time)
        increment_percentage = increment / old_time
        if increment_percentage > float(self.tolerance):
          self._worsen_transactions[transaction] = increment_percentage

  def run_one_comparison(self):
    self._compare_reports()
    if len(self._worsen_transactions) == 0:
      return "PASSED"
    else:
      return "FAILED (Regression Transactions: {}).".format(self._worsen_transactions)


#if __name__ == "__main__":
#  perf = PerformanceReportsComparison("/tmp/rawdata_1/output/data/subreports/Performance.json",
#                                      "/tmp/rawdata_2/output/data/subreports/Performance.json", 0.25)
#  perf.compare_reports()
#  perf.comparsion_summary()
