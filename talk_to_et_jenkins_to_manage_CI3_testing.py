import sys
import time
from CI3_python_realization.CI3_module.jenkins.talk_to_et_jenkins import TalkToETCI
from CI3_python_realization.CI3_module import basic_config
import logging


class TalkToETCIForCI3:
  """
  Trigger CI_3 with specific parameters. Now it is used by nightly CI

  """
  def __init__(self, username, password, parent_page, IS_COVERAGE_NEEDED):
    self.username = username
    self.password = password
    self.parent_page = parent_page
    self.IS_COVERAGE_NEEDED = IS_COVERAGE_NEEDED

  def get_the_latest_dev_build_id(self):
    """
    :return: the latest id of the build package jenkins job
    """
    et_ci = TalkToETCI(self.username, self.password, basic_config.ET_Jenkins, basic_config.dev_build_ci_name,"")
    return et_ci.get_last_completed_build_number()

  def run_ci3_build_testing(self):
    """
    :return: "SUCCESS" when the CI_3 job is triggered successfully
    """
    et_ci = TalkToETCI(self.username, self.password, basic_config.ET_Jenkins, basic_config.general_ci3_ci_name, "")
    build_testing_parameter = {}
    build_testing_parameter['username'] = self.username
    build_testing_parameter['password'] = self.password
    build_testing_parameter['et_build_name_or_id'] = self.get_the_latest_dev_build_id()
    build_testing_parameter['parent_page'] = self.parent_page
    build_testing_parameter['IS_COVERAGE_NEEDED'] = self.IS_COVERAGE_NEEDED
    et_ci.trigger_build(build_testing_parameter)
    time.sleep(30)
    logging.info("The nightly build testing has been triggered. Cheers!")
    logging.info("You can check the exact console log to get more details: {}".format(et_ci.get_the_latest_console_log_url()))
    return "SUCCESS"

if __name__ == "__main__":
  username = sys.argv[1]
  password = sys.argv[2]
  parent_page = sys.argv[3]
  IS_COVERAGE_NEEDED = sys.argv[4]
  monitor = TalkToETCIForCI3(username, password, parent_page, IS_COVERAGE_NEEDED)
  monitor.run_ci3_build_testing()
