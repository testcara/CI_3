#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

'''
__title__ = ''
__author__ = 'wlin'
__mtime__ = '10/9/18'
'''
from auto_testing_CI.CI3_module.report_parser import parser_build_testing_report
from auto_testing_CI.CI3_module.report_parser import performance_report_parser
import unittest
import logging
import os

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class TestBuildReportParser(unittest.TestCase):
  def test_build_report_parser(self):
    f = open('{}/fixtures/module_report_parser_test.txt'.format(os.getcwd()))
    content = f.read()
    f.close()
    parser = parser_build_testing_report.ParserBuildTestingReport(content)
    general_status_and_brief = parser.get_final_status_and_brief()
    self.assertEqual(general_status_and_brief,
                     "IN PROCESS-3 testings: 1 testing in process(Bug Regression Testing). 1 failed testing(TS2.0 UAT Testing). 1 passed testing(Performance Baseline Testing). ")


class TestSinglePerformanceParser(unittest.TestCase):
  def test_single_performace_parser(self):
    parser = performance_report_parser.SinglePerformanceReportParser(
      '{}/fixtures/single_performance_test.json'.format(os.getcwd()))
    output = parser.run_single_report_parser()
    self.assertEqual(output, {'Advisory_AddBugs_100': 7088, 'Advisory_AddBugs_Post_100': 9306, 'Advisory_New': 90,
                              'Advisory_New_FindNewBuild_5_nonrpm': 8040, 'Advisory_New_FindNewBuild_5_rpm': 7377,
                              'Advisory_New_SaveBuilds_5_nonrpm': 2638, 'Advisory_New_SaveBuilds_5_rpm': 17520,
                              'Advisory_New_SelectRelease': 7077, 'Advisory_New_Y-stream': 5752,
                              'Advisory_New_Y-stream_Go': 2375, 'Advisory_Post_Staging_CDN': 120,
                              'Advisory_Post_Staging_RHN': 123, 'Advisory_Push_Staging': 1550,
                              'Advisory_ReView_RpmdiffRuns': 1444, 'Advisory_RemoveBugs_100': 390,
                              'Advisory_RemoveBugs_Post_100': 6664, 'Advisory_Rhn_PushHistory': 133,
                              'Advisory_Rhn_PushResults_CDN': 117, 'Advisory_Rhn_PushResults_CDN_Stage': 151,
                              'Advisory_Rhn_PushResults_FTP': 144, 'Advisory_Rhn_PushResults_RHN': 176,
                              'Advisory_Rhn_PushResults_RHN_Stage': 105, 'Advisory_Summary_5_builds_norpm': 2250,
                              'Advisory_Summary_5_builds_rpm': 5873, 'Advisory_Summary_cgi_5_builds_norpm': 129,
                              'Advisory_Summary_cgi_5_builds_rpm': 138, 'Advisory_Update_Details': 592,
                              'Advisory_View_Builds_5_norpm': 1822, 'Advisory_View_Builds_5_rpm': 2732,
                              'Advisory_View_Builds_Json_5_norpm': 78, 'Advisory_View_Builds_Json_5_rpm': 772,
                              'Advisory_View_Builds_cgi_5_norpm': 1693, 'Advisory_View_Builds_cgi_5_rpm': 2500,
                              'Advisory_View_Builds_cgi_json_5_norpm': 91, 'Advisory_View_Builds_cgi_json_5_rpm': 712,
                              'Advisory_View_DEV': 2026, 'Advisory_View_Details_5_builds_ rpm': 3096,
                              'Advisory_View_Details_5_builds_nonrpm': 1461, 'Advisory_View_Details_DEV': 945,
                              'Advisory_View_Details_PM': 910, 'Advisory_View_Details_QE': 972,
                              'Advisory_View_DistQATps_DEV': 886, 'Advisory_View_DistQATps_PM': 946,
                              'Advisory_View_DistQATps_QE': 1037, 'Advisory_View_DocTextInfo_DEV': 678,
                              'Advisory_View_DocTextInfo_PM': 674, 'Advisory_View_DocTextInfo_QE': 649,
                              'Advisory_View_Docs_5_builds_norpm': 1061, 'Advisory_View_Docs_5_builds_rpm': 1750,
                              'Advisory_View_Docs_DEV': 1406, 'Advisory_View_Docs_PM': 1344,
                              'Advisory_View_Docs_QE': 1362, 'Advisory_View_PM': 2322, 'Advisory_View_QE': 2053,
                              'Advisory_View_RpmdiffRuns': 1455, 'Advisory_View_Rpmdiff_5_builds_norpm': 1535,
                              'Advisory_View_Rpmdiff_5_builds_rpm': 2131, 'Advisory_View_Text_DEV': 4811,
                              'Advisory_View_Text_PM': 285, 'Advisory_View_Text_QE': 254,
                              'Advisory_View_Tps_DEV': 1273, 'Advisory_View_Tps_PM': 1264, 'Advisory_View_Tps_QE': 945,
                              'Advisory_Waiting_Signature': 237, 'Get_Errata_ByFilter_DEV': 2794,
                              'Get_Errata_ByFilter_Json_DEV': 8722, 'Get_Errata_ByFilter_Json_PM': 8172,
                              'Get_Errata_ByFilter_PM': 2402, 'Get_Errata_Default_DEV': 2205,
                              'Get_Errata_Default_PM': 2696, 'Get_Releng_Default_Page': 243,
                              'SyncComponentListWithBugzilla_200': 9667, 'View_Advisory_Bugs_Json': 49,
                              'View_Advisory_Tps_Json': 168, 'View_Advisory_json': 135, 'View_Background_Job': 2602,
                              'View_DocsQueue_500': 12011, 'View_Docs_MyQueue_50': 7106, 'View_Errata_Json': 7562,
                              'View_Job_Tracker': 904, 'View_My_Request_Devel_20': 1841, 'View_My_Request_Qe_20': 197,
                              'View_One_Package': 2981, 'View_Package': 132, 'Xml-rpc:getErrataBrewBuilds_5_norpm': 68,
                              'Xml-rpc:getErrataBrewBuilds_5_rpm': 90, 'Xml-rpc:getErrataPackagesRHTS': 76,
                              'Xml-rpc:getRHNChannels': 343, 'Xml-rpc:get_advisory_cdn_file_list_100': 5926,
                              'Xml-rpc:get_advisory_cdn_file_list_20': 1486, 'Xml-rpc:get_advisory_list ': 2958,
                              'Xml-rpc:get_advisory_rhn_file_list_100': 5825,
                              'Xml-rpc:get_advisory_rhn_file_list_20': 1512,
                              'Xml-rpc:get_advisory_rhn_metadata_100': 5646,
                              'Xml-rpc:get_advisory_rhn_metadata_20': 1491, 'Xml-rpc:get_channel_packages_100': 3247,
                              'Xml-rpc:get_channel_packages_20': 884, 'Xml-rpc:get_pulp_packages_100': 3219,
                              'Xml-rpc:get_pulp_packages_20': 1033, 'Xml-rpc:get_released_channel_packages_100': 2376,
                              'Xml-rpc:get_released_channel_packages_20': 1430,
                              'Xml-rpc:get_released_pulp_packages_100': 1715,
                              'Xml-rpc:get_released_pulp_packages_20': 982, 'Xml-rpc:jobReport': 29}
                     )


class TestingPerformanceReportsComparison(unittest.TestCase):

  def test_perf_general_comparison_parser_with_low_tolerance(self):
    parser = performance_report_parser.PerformanceReportsComparison(
      "{}/fixtures/comparison_perf_1.json".format(os.getcwd()),
      "{}/fixtures/comparison_perf_2.json".format(os.getcwd()), 0.25, 5000)
    output = parser.run_one_comparison()
    self.assertEquals(output,
                      "FAILED (Regression Transactions: {'Advisory_New_FindNewBuild_5_nonrpm': 0.30982587064676614, 'Advisory_New_SaveBuilds_5_rpm': 0.8398972602739726}).")

  def test_perf_general_comparison_parser_with_high_tolerance(self):
    parser = performance_report_parser.PerformanceReportsComparison(
      "{}/fixtures/comparison_perf_1.json".format(os.getcwd()),
      "{}/fixtures/comparison_perf_2.json".format(os.getcwd()), 0.5, 5000)
    output = parser.run_one_comparison()
    self.assertEqual(output, "FAILED (Regression Transactions: {'Advisory_New_SaveBuilds_5_rpm': 0.8398972602739726}).")

  def test_perf_general_comparison_parser_with_low_max_accpected_time(self):
    parser = performance_report_parser.PerformanceReportsComparison(
      "{}/fixtures/comparison_perf_1.json".format(os.getcwd()),
      "{}/fixtures/comparison_perf_2.json".format(os.getcwd()), 0.2, 2000)
    output = parser.run_one_comparison()
    self.assertEqual(output,"FAILED (Regression Transactions: {'Advisory_New_FindNewBuild_5_nonrpm': 0.30982587064676614, 'Advisory_New_SaveBuilds_5_nonrpm': 0.3309325246398787, 'Advisory_New_SaveBuilds_5_rpm': 0.8398972602739726}).")

if __name__ == '__main__':
  unittest.main()
