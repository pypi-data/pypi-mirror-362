DPPS v0.2.0 (2025-06-27)
------------------------



- New versions of DPPS subsystems [`!106 <https://gitlab.cta-observatory.org/cta-computing/dpps/dpps/-/merge_requests/106>`__]:

    - `Workload Management System v0.3.0 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/workload/wms/v0.3.0/>`_
    - `Bulk Data Management System v0.3.0 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/bdms/bdms/v0.3.0/>`_
    - `CalibPipe v0.2.0 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/calibrationpipeline/calibpipe/v0.2.0/>`_
    - `DataPipe v0.2.1 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/datapipe/datapipe/v0.2.1/>`_
    - `SimPipe v0.2.0 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/simpipe/simpipe/v0.2.0/>`_
    - `QualPipe v0.2.1 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/qualpipe/qualpipe/v0.2.1/>`_


- Add tests to verify collection of observability information. [`!97 <https://gitlab.cta-observatory.org/cta-computing/dpps/dpps/-/merge_requests/97>`__]

DPPS v0.1.1 (2025-06-11)
------------------------

This is a maintenance release updating the helm chart of DPPS and
BDMS

Maintenance
~~~~~~~~~~~

- Update dependencies of python package to pin CTADIRAC==2.2.74,
  WMS clients to 0.2.0 and BDMS clients to 0.2.1.
  [`!101 <https://gitlab.cta-observatory.org/cta-computing/dpps/dpps/-/merge_requests/101>`__]

- Update `BDMS to 0.2.1 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/bdms/bdms/latest/changelog.html#bdms-v0-2-1-2025-06-03>`_
  [`!98 <https://gitlab.cta-observatory.org/cta-computing/dpps/dpps/-/merge_requests/98>`__]

- Use dpps own chart templates, allows to skip WMS. [`!98 <https://gitlab.cta-observatory.org/cta-computing/dpps/dpps/-/merge_requests/98>`__]


DPPS v0.1.0 (2025-05-08)
------------------------

First DPPS release to integrate pipelines and add functionality to ingest ACADA DL0 data
into BDMS.

This release integrates:

- `Workload Management System v0.2.0 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/workload/wms/v0.2.0/>`_
- `Bulk Data Management System v0.2.0 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/bdms/bdms/v0.2.0/>`_
- `CalibPipe v0.1.0 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/calibrationpipeline/calibpipe/v0.1.0/>`_
- `DataPipe v0.1.0 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/datapipe/datapipe/v0.1.0/>`_
- `SimPipe v0.1.0 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/simpipe/simpipe/v0.1.0/>`_
- `QualPipe v0.1.0 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/qualpipe/qualpipe/v0.1.0/>`_


Deployment is facilitated by docker images and helm charts.


DPPS v0.0.0 (2025-02-26)
------------------------

Initial Release of the Data Processing and Preservation System.

This release integrates

- `Workload Management System v0.1.0 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/workload/wms/v0.1.0/>`_
- `Bulk Data Management System v0.1.0 <http://cta-computing.gitlab-pages.cta-observatory.org/dpps/bdms/bdms/v0.1.0/>`_

Deployment is facilitated by docker images and helm charts.
