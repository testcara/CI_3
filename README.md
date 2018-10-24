
Introduction
===
[CI_3](https://errata-jenkins.rhev-ci-vms.eng.rdu2.redhat.com/view/wip/job/ET_Builds_Testing_Pipeline/) is the one-click CI test suite of the Errata Tool automating everything from deployment and configuration, to triggering test suites, up through reporting for Errata Tool build testing.
And it covers all automated testing type, like the E2E testing, performance baseline testing, TS2.O UAT testing and bug regression testing.

Why We Have CI_3
===
With it, we would like to
- improve the efficiency and reduce the time on repeated tasks
- improve the test stability and frequency
- make sure every one can go all testings and get the final results, even he has no idea about performance testing, E2E or TS2.0

The Design
===
Generally, 4 sub pipeline testings compose the top CI_3 pipeline.

![CI_3_design](https://gitlab.cee.redhat.com/wlin/CI_3/raw/master/README_resource/CI_3_design.jpg)

In fact, besides the CI shown above, 3 CIs works with CI_3 together. They are:
- 'nightly CI' is one CI to trigger CI_3 for the latest dev build every night
- 'monitor slaves CI' is one CI to monitor some key slaves used by CI_3 to avoid the Openstack instability
- 'hunter' CI is one CI to analyze the failure, collect questionable scenarios and show coverage of TS2.0 testing

More, currently most Jenkins slaves are running in Openstack. Usually, the slave just provides docker function. Jenkins jobs connects to the slave, pull the docker images then do the testings.  

The Benefits We Have Achieved
===
- It saves more than 6 hours (300+30+25+15=370) for each build testing
- It standardizes all testing process
- It is shared cross different teams
- It enables QE can finish one build testing in one day

The Problems CI_3 have
===
- The Openstack is not very stable. Sometimes the slaves of our Jenkins does not work well.
- The CI_3 is just used for Errata Tool QE.

The Later Plan of CI_3
===
- Migrate CI_3 to Upshift to resolve the stability problem of Jenkins slaves
- TBD

Other References of CI_3
===
- [Hunter CI introduction of CI_3](https://docs.google.com/document/d/1Ve_3FgiQ78cDyM1uWOV257AdzfYzHEN1WvrvEv71nDk/edit) 
- [E2E CI introduction of CI_3](https://docs.google.com/document/d/1yl8GoOHrmtoqa5daeLmajkQagJUB5dQZPauyYgcCHbc/edit)
- [CI_3 demo](https://docs.google.com/document/d/1Pe9HnsrAfqhojeXPBFzAWWPrMY0cii3BphAiSO_K4CE/edit)