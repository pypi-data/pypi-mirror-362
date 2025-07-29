LaunchDarkly Server-side OTEL library for Python
==============================================

[![PyPI](https://img.shields.io/pypi/v/launchdarkly-server-sdk-otel.svg?maxAge=2592000)](https://pypi.python.org/pypi/launchdarkly-server-sdk-otel)
[![Quality Control](https://github.com/launchdarkly/python-server-sdk-otel/actions/workflows/ci.yml/badge.svg)](https://github.com/launchdarkly/python-server-sdk-otel/actions/workflows/ci.yml)
[![readthedocs](https://readthedocs.org/projects/launchdarkly-python-sdk-otel-integration/badge/)](https://launchdarkly-python-sdk-otel-integration.readthedocs.io/en/latest/)

LaunchDarkly overview
-------------------------
[LaunchDarkly](https://www.launchdarkly.com) is a feature management platform that serves trillions of feature flags daily to help teams build better software, faster. [Get started](https://docs.launchdarkly.com/home/getting-started) using LaunchDarkly today!

[![Twitter Follow](https://img.shields.io/twitter/follow/launchdarkly.svg?style=social&label=Follow&maxAge=2592000)](https://twitter.com/intent/follow?screen_name=launchdarkly)

Supported Python versions
-----------------------

This version of the library has a minimum Python version of 3.9.

Getting started
-----------

Install the package

    $ pip install launchdarkly-server-sdk-otel

The provided `TracingHook` can be setup as shown below:

```python
from ldotel.tracing import Hook
import ldclient

ldclient.set_config(Config('sdk-key', hooks=[Hook()]))
client = ldclient.get()

set_tracer_provider(TracerProvider())
tracer = get_tracer_provider().get_tracer('pytest')

with tracer.start_as_curent_span('top-level span'):
    client.variation('boolean', Context.create('org-key', 'org'), False)
```

Learn more
-----------

Read our [documentation](http://docs.launchdarkly.com) for in-depth instructions on configuring and using LaunchDarkly. You can also head straight to the [reference guide for the python SDK](http://docs.launchdarkly.com/docs/python-sdk-reference).

Generated API documentation for all versions of the library is on [readthedocs](https://launchdarkly-python-sdk-otel-integration.readthedocs.io/en/latest/).

Contributing
------------

We encourage pull requests and other contributions from the community. Check out our [contributing guidelines](CONTRIBUTING.md) for instructions on how to contribute to this library.

Verifying library build provenance with the SLSA framework
------------

LaunchDarkly uses the [SLSA framework](https://slsa.dev/spec/v1.0/about) (Supply-chain Levels for Software Artifacts) to help developers make their supply chain more secure by ensuring the authenticity and build integrity of our published library packages. To learn more, see the [provenance guide](PROVENANCE.md).

About LaunchDarkly
-----------

* LaunchDarkly is a continuous delivery platform that provides feature flags as a service and allows developers to iterate quickly and safely. We allow you to easily flag your features and manage them from the LaunchDarkly dashboard.  With LaunchDarkly, you can:
    * Roll out a new feature to a subset of your users (like a group of users who opt-in to a beta tester group), gathering feedback and bug reports from real-world use cases.
    * Gradually roll out a feature to an increasing percentage of users, and track the effect that the feature has on key metrics (for instance, how likely is a user to complete a purchase if they have feature A versus feature B?).
    * Turn off a feature that you realize is causing performance problems in production, without needing to re-deploy, or even restart the application with a changed configuration file.
    * Grant access to certain features based on user attributes, like payment plan (eg: users on the ‘gold’ plan get access to more features than users in the ‘silver’ plan). Disable parts of your application to facilitate maintenance, without taking everything offline.
* LaunchDarkly provides feature flag SDKs for a wide variety of languages and technologies. Read [our documentation](https://docs.launchdarkly.com/sdk) for a complete list.
* Explore LaunchDarkly
    * [launchdarkly.com](https://www.launchdarkly.com/ "LaunchDarkly Main Website") for more information
    * [docs.launchdarkly.com](https://docs.launchdarkly.com/  "LaunchDarkly Documentation") for our documentation and SDK reference guides
    * [apidocs.launchdarkly.com](https://apidocs.launchdarkly.com/  "LaunchDarkly API Documentation") for our API documentation
    * [blog.launchdarkly.com](https://blog.launchdarkly.com/  "LaunchDarkly Blog Documentation") for the latest product updates
