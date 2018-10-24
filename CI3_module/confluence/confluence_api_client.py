#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

'''
__title__ = 'confluence_rest_api_client'
__author__ = 'wlin'
__mtime__ = '9/30/18'
'''
import requests
from requests_kerberos import HTTPKerberosAuth
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class ConfluenceClientForUpdatePage:
  """
    A conflence component used to connect to confluence and perform
    confluence related tasks
    """

  def __init__(self, confluence_space, confluence_page_title,
               confluence_url, username=None, password=None,
               auth_type='basic'):
    '''
    Returns confluence client object
    :param string confluence_space : space to be used in confluence
    :param strinf confluence_page_title : Title of page to be created in confluence
    :param string confluence_url : url to connect confluence
    :param string username : optional username for basic auth
    :param string password : optional password for basic auth
    :param string auth_type : indicate auth scheme (basic/kerberos)
    '''
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    self.confluence_space = confluence_space
    self.confluence_page_title = confluence_page_title
    self.confluence_url = confluence_url
    self.username = username
    self.password = password
    self.authtype = auth_type
    self._req_kwargs = None

  @property
  def req_kwargs(self):
    """ Set the key-word arguments for python-requests depending on the
        auth type. This code should run on demand exactly once, which is
        why it is a property.
        :return dict _req_kwargs: dict with the right options to pass in
        """
    if self._req_kwargs is None:
      if self.authtype == 'kerberos':
        # First we get a cookie from the "step" site, which is just
        # an nginx proxy that is kerberos enabled.
        step_url = self.confluence_url + '/step-auth-gss'
        conf_resp = requests.get(step_url, auth=self.get_auth_object())
        conf_resp.raise_for_status()
        # Going forward, we just pass in "cookies", no need to provide
        # an auth object anymore. In fact if we do, it'll get
        # preferred and fail since the service itself is not kerberos
        # enabled.
        self._req_kwargs = {'cookies': conf_resp.cookies, 'verify': False}
      elif self.authtype == 'basic':
        self._req_kwargs = {'auth': self.get_auth_object(), 'verify': False}
    return self._req_kwargs

  def update_page(self, page_info, html):
    """
        Updates the page with html
        the function will get the info from page_info first, like page_id, page_version
        :param dict page_info: the info of the page
        :param string html : html content of the page
        :return json conf_resp: response from the confluence
        """

    page_id = page_info['id']
    version = page_info['version']
    title = page_info['title']

    confluence_rest_url = self.confluence_url + "/rest/api/content/" + \
                          page_id

    updated_page_version = int(version) + 1
    data = {
      'id': str(page_id),
      'type': 'page',
      'title': title,
      'version': {
        'number': updated_page_version},
      'body': {
        'storage': {
          'representation': 'storage',
          'value': html}}}
    resp = requests.put(confluence_rest_url, json=data, **self.req_kwargs)
    resp.raise_for_status()
    return resp.json()

  def get_auth_object(self):
    """Returns Auth object based on auth type
        :return : Auth Object
        """
    if self.authtype == 'kerberos':
      # I'm not sure disabling auth is a good idea, but most of the examples I've
      # seen internally do this. Probably makes me part of the problem.
      return HTTPKerberosAuth(mutual_authentication=False)
    elif self.authtype == "basic":
      return HTTPBasicAuth(self.username, self.password)


import sys
from confluence import Api
import logging
import auto_testing_CI.CI3_module.basic_config as basic_config


class ConfluenceClient:
  """
    A confluence client used to connect to confluence to get/create/update pages
  """

  def __init__(self, username, password, title, space, general_content="", parent_page=""):
    '''
		:param username: username to connect with Confluence
		:type string:
		:param password: password for the above username
		:type string:
		:param title: title for the testing report created against Confluence
		:type string:
		:param space: space for the testing report against Confluence
		:type string:
		:param general_content: contents for the testing report
		:type string:
		:param parent_page: the testing report parent page against Confluence
		:type string:
		'''
    self.username = username
    self.password = password
    self.title = title
    self.space = space
    self.general_content = general_content
    self.parent_page = parent_page
    self.api = Api(basic_config.wiki_url, self.username, self.password)

  def create_update_page(self):
    '''
    :return: string "SUCESS" when the the page is created/updated successfully
    '''
    content = self.get_page_content()
    if content.find("it does not exist.") > 0 or content.find("table") < 0:
      logging.info("CI will add page!")
      logging.info("The page title: %s!", self.title)
      self.api.addpage(self.title, self.space, self.general_content, parentpage=self.parent_page)
    else:
      page_info = self.get_page_all()
      logging.info("CI will update page!")
      logging.info("The page title: %s!", self.title)
      update_confluence_client = ConfluenceClientForUpdatePage(
        self.space, self.title,
        basic_config.wiki_url,
        self.username,
        self.password)
      update_confluence_client.update_page(dict(page_info), self.general_content)
      return "SUCCESS"

  def get_page_content(self):
    '''
    :return: content of the exact Confluence page
    :rtype: basestring
    '''
    try:
      content = self.api.getpagecontent(self.title, self.space)
    except Exception:
      ""
    return content

  def get_page_all(self):
    '''
    :return: all page info including the page id and so on
    :rtype: basestring
    '''
    page_all_info =""
    try:
      page_all_info = self.api.getpage(self.title, self.space)
    except Exception:
      ""
    return page_all_info


if __name__ == "__main__":
  get_page = "false"
  create_update_page = "false"
  if len(sys.argv) == 5:
    get_page = "true"
  elif len(sys.argv) == 7:
    create_update_page = "true"

  username = sys.argv[1]
  password = sys.argv[2]
  title = sys.argv[3]
  space = sys.argv[4]
  if get_page == "true":
    confulence_client = ConfluenceClient(username, password, title, space, "", "")
    confulence_client.get_page_content()
  if create_update_page == "true":
    content = sys.argv[5]
    parentpage = sys.argv[6]
    confulence_client = ConfluenceClient(username, password, title, space, content, parentpage)
    confulence_client.create_update_page()
