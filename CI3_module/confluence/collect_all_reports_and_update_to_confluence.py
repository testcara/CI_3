from CI3_python_realization.CI3_module.confluence import confluence_api_client
import CI3_python_realization.ci3_error
import CI3_python_realization.CI3_module.confluence.generate_build_report_for_all_testings


class CollectAllReportsAndUpdateToConfluence():
  """
  Collect all testing reports and update them to the Confluence
  """
  def __init__(self, username, password, et_build_version, title, space, parent_page):
    """
    :param username: string  username to connect with Confulence then create/update testing reports
    :param password: string  password to the above username:
    :param et_build_version: string  the current Errata Tool version of the build, like 3354 and so on
    :param title: string  the title of the testing report generated/updated against Confluence
    :param space: string  the space of Confluence you would like to put your testing report
    :param parent_page: string  the parent page of Confluence you would like your testing report belongs to
    """
    self.username = username
    self.password = password
    self.et_build_version = et_build_version
    self.title = title
    self.space = space
    self.parent_page = parent_page

  def collect_reports_and_update_to_confluence(self):
    """
    :return: SUCCESS when it collects reports from Jenkins and update the general report to Confluence successfully
    """
    generator = auto_testing_CI.CI3_module.confluence.generate_build_report_for_all_testings.GenerateAllReports(self.username, self.password, self.et_build_version)
    report =generator.run_one_generator()
    confulence_api_client = confluence_api_client.ConfluenceClient(self.username, self.password, self.title, self.space,
                                                                   report, self.parent_page)
    return confulence_api_client.create_update_page()
