#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'generate_confluence_page_for_bugs'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""
import bugzilla
import re
import logging
import os


class GenerateConfluenceContentForBugs:
  """
  Generate the confluence content for bugs searched from bugzilla.
  """
  logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

  def __init__(self, username, password, bugs):
    self.username = username
    self.password = password
    self.bugs = bugs.split(' ')

  def _generate_bugzilla_conf_file(self):
    user_account = "[bugzilla.redhat.com]\nuser={}\npassword={}".format(self.username, self.password)
    f = open('{}/.bugzillarc'.format(os.environ['HOME']), 'w+')
    f.write(user_account)
    f.close()

  @staticmethod
  def _empty_bugzilla_conf_file():
    content = " "
    f = open('{}/.bugzillarc'.format(os.environ['HOME']), 'w')
    f.write(content)
    f.close()

  def _get_bug_and_format_bug(self, bug_id):
    bzapi = bugzilla.Bugzilla("bugzilla.redhat.com")
    bug = bzapi.getbug(int(bug_id))
    # for spike tasks, Let the script add 'qe_auto_coverage' flag automatically if needed
    if bug.summary.find('[Spike]') == 0 and isinstance(bug.get_flags('qe_auto_coverage'), string):
      # For spike bug, if the 'qe_auto_coverage' flag has not been set, set the flag automatically
      auto_flag = {}
      auto_flag['qe_auto_coverage'] = '-'
      bug.updateflags(auto_flag)
      # refetch the bug
      bug = bzapi.getbug(bug.id)

    # for otherQA bug, Let the script add 'qe_auto_coverage' flag as '-' automatically if needed
    if 'OtherQA' in bug.keywords and isinstance(bug.get_flags('qe_auto_coverage'), string):
      # For OtherQA bug, if the 'qe_auto_coverage' flag has not been set, set the flag automatically
      auto_flag = {}
      auto_flag['qe_auto_coverage'] = '-'
      bug.updateflags(auto_flag)
      # refetch the bug
      bug = bzapi.getbug(bug.id)

    qe_flag = False
    qe_bug_flag = ""
    for flag in bug.flags:
      if flag['name'] == "qe_auto_coverage":
        qe_flag = True
        qe_bug_flag = flag['status']
    bug_flag = qe_bug_flag if qe_flag else ""

    # deal with bug.summary: remove unchar letters to avoid the unexpected error when add confluence page
    regex = re.compile('[^a-zA-Z0-9 _?\[\]{}()]')
    summary = regex.sub('', bug.summary)

    bug_result = "PASSED" if bug.status in ['RELEASE_PENDING', 'VERIFIED', 'CLOSED'] and bug_flag in ['+', '-'] else ""

    return [bug.id, summary, bug.component, bug.status, bug.severity, bug.priority, bug_flag, bug.qa_contact,
            bug_result]

  def _get_bugs_and_format_bugs(self, bugs_list):
    formatted_bugs = []
    for bug in bugs_list:
      formatted_bugs.append(self._get_bug_and_format_bug(bug))
    return formatted_bugs

  def _get_formatted_automated_bugs_list(self, bugs_list):
    """
    get all passed bug for the second table
    :return: formatted bugs list for 'passed' bugs
    """
    formatted_automated_bugs = []
    for bug in bugs_list:
      if bug[8] == "PASSED":
        formatted_automated_bugs.append(bug)
    return formatted_automated_bugs

  def _get_formatted_manual_bugs_list(self, bugs_list):
    """
    get all manual testing bugs for the first table
    :return: formatted bugs list for 'manual' bugs
    """
    formatted_manual_bugs = []
    for bug in bugs_list:
      if bug[8] != "PASSED":
        formatted_manual_bugs.append(bug)
    return formatted_manual_bugs

  def _generate_page_content(self, formatted_bugs_list):
    head_row = ""
    for column_name in ['ID', 'Summary', 'Component', 'Status', 'Severity', 'Priority', 'qe_auto_coverage', 'QAOwner',
                        'Result']:
      head_row += "<th colspan='1'>{}</th>".format(column_name)

    headrow_html = "<tr>{}</tr>".format(head_row)
    bug_rows_html = ""
    for formatted_bug in formatted_bugs_list:
      bug_rows_html += self._generate_bug_content(formatted_bug)
    table_content = "<table><tbody>{}{}</tbody></table>".format(headrow_html, bug_rows_html)
    return table_content

  def _generate_bug_content(self, formatted_bug):
    bug_row = ""
    bug_id = str(formatted_bug[0])
    bug_details = formatted_bug[1:]
    bug_id_td_html = "<td><a href='https://bugzilla.redhat.com/show_bug.cgi?id ={}'>{}</a></td>".format(bug_id, bug_id)
    for bug_item in bug_details:
      if bug_item == "PASSED":
        bug_row += "<td><strong><span style='color: rgb(0,128,0);'>{}</span></strong></td>".format(bug_item)
      else:
        bug_row += "<td>{}</td>".format(bug_item)
    bug_row_html = "<tr>{}{}</tr>".format(bug_id_td_html, bug_row)
    return bug_row_html

  def run_generator(self):
    logging.info("Generating bug conf files")
    self._generate_bugzilla_conf_file()
    logging.info("Done for generating bug conf files")
    logging.info("Getting bugs from Bugzilla and formatting bugs")
    formatted_bugs_list = self._get_bugs_and_format_bugs(self.bugs)
    logging.info("Done for getting and formatting bugs")
    logging.info("Spliting bugs to automated and manual parts")
    formatted_automated_bugs = self._get_formatted_automated_bugs_list(formatted_bugs_list)
    formatted_manual_bugs = self._get_formatted_manual_bugs_list(formatted_bugs_list)
    logging.info("Done for spliting bugs to automated and manual parts")
    logging.info("Formatting content for automated bugs")
    logging.info(formatted_automated_bugs)
    formatted_automated_bugs_html = self._generate_page_content(formatted_automated_bugs)
    logging.info(formatted_automated_bugs_html)
    logging.info("Formatting content for manual bugs")
    formatted_manual_bugs_html = self._generate_page_content(formatted_manual_bugs)
    info_for_manual_testing_html = "<p>'' and '?' of 'qe_auto_coverage' of the following table means QE have not finished the automation tasks of the bugs.<strong> Manual testing is needed!</strong></p>"
    info_for_automated_testing_html = "<p> '-' of 'qe_auto_coverage' of the following table means QE have confirmed that <strong>no more manual testing is needed</strong>For dev's autoated testing has been covered or it is minor UI change or unimportant negative case can be ingored!<strong>Mark as 'PASSED' directly!</strong></p>"
    info_for_automated_testing_html += "<p>means QE have completed the automation tasks.<strong>TS2.0 has been covered it. Mark as PASSED directly!</strong></p>"
    page_notice_html = "<p>'qe_auto_coverage' on the page shows QE automation status for bugs.</p>"
    html = page_notice_html + info_for_manual_testing_html + formatted_manual_bugs_html + info_for_automated_testing_html + formatted_automated_bugs_html
    logging.info("Done for formatting content for bugs")
    self._empty_bugzilla_conf_file()
    logging.info("Done for cleaning the bug conf files")
    return html
