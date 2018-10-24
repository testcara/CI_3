#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

"""
__title__ = 'basic_config'
__author__ = 'wlin'
__mtime__ = '9/30/18'
"""
wiki_url = "https://docs.engineering.redhat.com"
testing_jenkins_result_builds_map = {'Performance Baseline Testing': 'Parser_Performance_Result',
                                     'TS2.0 UAT Testing': 'Trigger_TS2_UAT_Testing',
                                     'E2E Testing': 'Trigger_E2E_Testing',
                                     'Bug Regression Testing': 'Bug_Regression_Testing'}
e2e_env = '''
<p>ET Server: et-e2e.usersys.redhat.com</p>
<p>Pub Server: pub-e2e.usersys.redhat.com</p>
<p>pulp Rpm Server: pulp-e2e.usersys.redhat.com</p>
<p>pulp Docker Server: pulp-docker-e2e.usersys.redhat.com</p>
<p>Pub and Pulp Versions:</p>
'''

perf_env = '''
<p>ET Server: errata-stage-perf.host.stage.eng.bos.redhat.com</p>
<p>ET DB: errata-stage-perf-db.host.stage.eng.bos.redhat.com</p>
'''

bug_regression_env = 'ET Server: errata-web-03.host.qe.eng.pek2.redhat.com'

ts2_uat_env = 'ET server: et-system-test-qe-02.usersys.redhat.com'

env_map = {'Performance Baseline Testing': perf_env, 'TS2.0 UAT Testing': ts2_uat_env, 'E2E Testing': e2e_env,
           'Bug Regression Testing': bug_regression_env}
ET_Jenkins = "https://errata-jenkins.rhev-ci-vms.eng.rdu2.redhat.com"

ET_Perf_Server = "errata-stage-perf.host.stage.eng.bos.redhat.com"
ET_Stub_Server = "10.8.248.96/RPC2"
ET_DB_Server = "errata-stage-perf-db.host.stage.eng.bos.redhat.com"
Perf_Jenkins = "https://perfci.eng.pek2.redhat.com"

default_build_number_to_compare = 224
perf_sub_ci_build_name = 'Trigger_Perf_Testing_Remotely'
perf_remote_base_path = '/data/jenkins_workspace/workspace/ET_Baseline_PDI/perf-output/builds/'
dev_build_ci_name = "deployment-packages"
general_ci3_ci_name = "ET_Builds_Testing_Pipeline"
e2e_version_page_name = "Version of Applications in E2E"
e2e_version_page_space = "~lzhuang"
