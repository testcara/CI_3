#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'get_all_pub_pulp_product_version_content'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""

from CI3_python_realization.CI3_module.confluence import confluence_api_client
from CI3_python_realization.CI3_module import basic_config


class GetAllPubPulpVersionContent:
  """
  Get all pub and pulp product versions from E2E versions page like 'Version of Applications in E2E'
  """

  def __init__(self, username, password):
    """
    :param username: string  username to log in Confluence:
    :param password: string  password for the username
    """
    self.username = username
    self.password = password
    self._e2e_versions_content_list = []

  def _get_e2e_versions_content_list(self):
    """
    The function will get all e2e content from the target file 'Version of Applications in E2E'
    And split it to lists then initialize the Class variable 'e2e_versions_content_list'
    """
    e2e_confluence_client = confluence_api_client.ConfluenceClient(self.username, self.password,
                                                                   basic_config.e2e_version_page_name,
                                                                   basic_config.e2e_version_page_space)
    versions_content = e2e_confluence_client.get_page_content()
    self._e2e_versions_content_list = versions_content.split('</tr>')

  def _get_pub_content(self):
    """
    :return: string  pub versions content
    """
    return "<p>Pub:</p>{}".format(
      self._e2e_versions_content_list[3].split("</td>")[1].replace("td", 'p').replace("<tr>", "").replace("<p><p>",
                                                                                                          "<p>"))

  def _get_pulp_rpm_content(self):
    """
    :return: string  pulp rpm related versions content
    """
    return "<p>Pulp RPM:</p>{}".format(
      self._e2e_versions_content_list[4].split("</td>")[1].replace("td", 'p').replace("<tr>", "").replace("<p><p>",
                                                                                                          "<p>"))

  def _get_pulp_docker_content(self):
    '''
    :return: pulp docker related versions content
    :rtype: basestring
    '''
    return "<p>Pulp Docker:</p>{}".format(
      self._e2e_versions_content_list[5].split("</td>")[1].replace("td", 'p').replace("<tr>", "").replace("<p><p>",
                                                                                                          "<p>"))

  def get_all_pub_pulp_content(self):
    """
    :return: string  all e2e versions content including pub, pulp rpm and pulp docker
    """
    self._get_e2e_versions_content_list()
    pub_content = self._get_pub_content()
    pulp_rpm_content = self._get_pulp_rpm_content()
    pulp_docker_content = self._get_pulp_docker_content()
    return "{}{}{}".format(pub_content, pulp_rpm_content, pulp_docker_content)
