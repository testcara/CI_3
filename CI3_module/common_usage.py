#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'common usage'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""
import os
import os.path
import logging
from paramiko import SSHClient
from scp import SCPClient


class CommonUsage():
  """
  Common Functions like check the files existed or scp files and so on
  """
  def check_file_exist(self, file):
    """
    Checking files existed or not
    :param file: string  the file path you would like to check
    :return: int 0/1 when the file exists, return 0
    """
    if os.path.isfile(file) and os.access(file, os.R_OK):
      logging.info("File exists and is readable")
      return 0
    else:
      logging.info("Either file is missing or not readable")
      return 1

  def python_scp_get_files(self, remote_host, src, destination):
    """
    Scp files from remote to destination
    :param remote_host: string  remote host
    :param src: string  target files
    :param destination: string remote destination
    :return: 0 when it scps files successfully
    """
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(remote_host)
    # SCPCLient takes a paramiko transport as an argument
    scp = SCPClient(ssh.get_transport())
    scp.get(src, destination)
    scp.close()
    return 0
