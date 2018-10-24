#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'get_pub_pulp_product_version'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""


class GetPubAndPulpVersion:
  """
  Get the pub or pulp product versions from E2E versions page like 'Version of Applications in E2E'
  """

  def __init__(self, e2e_page_content, build_name):
    """
    :param e2e_page_content: string  the content of E2E versions page
    :param build_name: string  which version you would like to know, like 'pub'/'pulp_for_rpm'
    """
    self.e2e_page_content = e2e_page_content
    self.build_name = build_name
    self._e2e_version_content_list = self.e2e_page_content.split('</tr>')
    self._pub_version = ""
    self._pub_build = ""
    self._pub_rcm_pa_tool_build = ""
    self._pulp_rpm_build = ""
    self._pulp_for_rpm = ""
    self._pulp_cdn_distributor_plugins_build = ""
    self._pulp_docker_build = ""
    self._pulp_for_docker = ""
    self._build_name_list = {}

  def _get_pub_build_name(self):
    """
    :return: string  return the pub build shown on the E2E versions page
    """
    self._pub_build = \
      self._e2e_version_content_list[3].split('</td>')[1].split("</p>")[0].split('>')[2].split('pub')[1].split("-1.el")[
        0]
    self._build_name_list['pub'] = 'pub-hub{}'.format(self._pub_build)

  def _get_pulp_build_name_for_pulprpm(self):
    """
    :return: string  return the 'pulp-server' build shown on the E2E versions page
    """
    self._pulp_build_for_rpm = \
      self._e2e_version_content_list[4].split("</td>")[1].split("</p>")[0].split(">")[2].split(':')[1]
    self._build_name_list['pulp_for_rpm'] = 'pulp-server-{}'.format(self._pulp_build_for_rpm.strip())

  def _get_pulp_rpm_build_name(self):
    """
    :return: string  return the 'pulp-rpm-plugins' build shown on the E2E versions page
    """
    self._pulp_rpm_build = \
      self._e2e_version_content_list[4].split("</td>")[1].split("</p>")[1].split('>')[1].split(':')[
        1]
    self._build_name_list['pulp-rpm-plugins'] = "pulp-rpm-plugins-".format(self._pulp_rpm_build.strip())

  def _get_pulp_cdn_distributor_plugins_build(self):
    """
    :return: string  return the 'pulp-cdn-distributor-plugins' build shown on the E2E versions page
    """
    self._pulp_cdn_distributor_plugins_build = \
      self._e2e_version_content_list[4].split("</td>")[1].split("</p>")[2].split('>')[1].split(":")[1]
    self._build_name_list[
      'pulp-cdn-distributor-plugins'] = "pulp-cdn-distributor-plugins-".format(
      self._pulp_cdn_distributor_plugins_build.strip())

  def _get_pulp_build_name_for_pulpdocker(self):
    """
    :return: string  return the 'pulp-server' build for pulp-docker shown on the E2E versions page
    """
    self._pulp_for_docker = \
      self._e2e_version_content_list[5].split('</td>')[1].split('</p>')[0].split('p>')[1].split(':')[1]
    self._build_name_list['pulp_for_docker'] = "pulp-server-".format(self._pulp_for_docker.strip())

  def _get_pulp_docker_build_name(self):
    """
    :return: string  return the 'pulp-docker-plugins' build for pulp-docker shown on the E2E versions page
    """
    self._pulp_docker_build = \
      self._e2e_version_content_list[5].split('</td>')[1].split('</p>')[1].split('<p>')[1].split(":")[1]
    self._build_name_list['pulp-docker-plugins'] = 'pulp-docker-plugins-'.format(self._pulp_docker_build.strip())

  def get_pub_or_pulp_versions(self):
    self._get_pub_build_name()
    self._get_pulp_build_name_for_pulprpm()
    self._get_pulp_rpm_build_name()
    self._get_pulp_cdn_distributor_plugins_build()
    self._get_pulp_build_name_for_pulpdocker()
    self._get_pulp_docker_build_name()
    return self._build_name_list[self.build_name]
