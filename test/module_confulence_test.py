#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = ''
__author__ = 'wlin'
__mtime__ = '10/8/18'
"""
import unittest
import os
import sys

sys.path.insert(0, '/mnt/wlin_laptop/PycharmProjects/RC_CI')
from auto_testing_CI.CI3_module.confluence import generate_confluence_page_for_bugs

class TestGeneratePageForBugs(unittest.TestCase):

  def test_content_can_be_generated(self):
    username = os.getenv("TestUsername")
    password = os.getenv("TestPassword")
    testing_bugs = '1138548 1573770'
    generator = generate_confluence_page_for_bugs.GenerateConfluenceContentForBugs(username, password, testing_bugs)
    generated_content = generator.run_generator()
    expected_content = "<p>'qe_auto_coverage' on the page shows QE automation status for bugs.</p><p>'' and '?' of 'qe_auto_coverage' of the following table means QE have not finished the automation tasks of the bugs.<strong> Manual testing is needed!</strong></p><table><tbody><tr><th colspan='1'>ID</th><th colspan='1'>Summary</th><th colspan='1'>Component</th><th colspan='1'>Status</th><th colspan='1'>Severity</th><th colspan='1'>Priority</th><th colspan='1'>qe_auto_coverage</th><th colspan='1'>QAOwner</th><th colspan='1'>Result</th></tr></tbody></table><p> '-' of 'qe_auto_coverage' of the following table means QE have confirmed that <strong>no more manual testing is needed</strong>For dev's autoated testing has been covered or it is minor UI change or unimportant negative case can be ingored!<strong>Mark as 'PASSED' directly!</strong></p><p>means QE have completed the automation tasks.<strong>TS2.0 has been covered it. Mark as PASSED directly!</strong></p><table><tbody><tr><th colspan='1'>ID</th><th colspan='1'>Summary</th><th colspan='1'>Component</th><th colspan='1'>Status</th><th colspan='1'>Severity</th><th colspan='1'>Priority</th><th colspan='1'>qe_auto_coverage</th><th colspan='1'>QAOwner</th><th colspan='1'>Result</th></tr><tr><td><a href='https://bugzilla.redhat.com/show_bug.cgi?id =1138548'>1138548</a></td><td>wrong warning appears with the errata has embargo bugs when pushing</td><td>webui</td><td>CLOSED</td><td>medium</td><td>medium</td><td>-</td><td>jingwang@redhat.com</td><td><strong><span style='color: rgb(0,128,0);'>PASSED</span></strong></td></tr><tr><td><a href='https://bugzilla.redhat.com/show_bug.cgi?id =1573770'>1573770</a></td><td>[Regression] Allow nonuseradmins to view readonly version of httpserrataengineeringredhatcomuser</td><td>Administration</td><td>CLOSED</td><td>high</td><td>high</td><td>+</td><td>hongliu@redhat.com</td><td><strong><span style='color: rgb(0,128,0);'>PASSED</span></strong></td></tr></tbody></table>"

    print(expected_content)
    self.assertEquals(generated_content, expected_content)





if __name__ == '__main__':
  unittest.main()
