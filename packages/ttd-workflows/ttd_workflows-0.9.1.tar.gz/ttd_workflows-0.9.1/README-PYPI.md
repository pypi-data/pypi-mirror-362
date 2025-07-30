# ttd-workflows-python

<!-- Start Summary [summary] -->
## Summary

Workflows Service: 
This service provides operations for commonly used workflows on The Trade Desk's platform.
In addition, this service provides generic operations for submitting:

- GraphQL API requests
- REST API requests

For further explanation on the entities encountered in this documentation (e.g.,
[campaigns](https://partner.thetradedesk.com/v3/portal/api/doc/Campaigns) and
[ad groups](https://partner.thetradedesk.com/v3/portal/api/doc/AdGroup)), visit the
[Partner Portal](https://partner.thetradedesk.com/v3/portal/api/doc/ApiUseCases).
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [ttd-workflows-python](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#ttd-workflows-python)
  * [SDK Installation](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#sdk-installation)
  * [IDE Support](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#ide-support)
  * [SDK Example Usage](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#sdk-example-usage)
  * [Authentication](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#authentication)
  * [Available Resources and Operations](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#available-resources-and-operations)
  * [Retries](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#retries)
  * [Error Handling](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#error-handling)
  * [Server Selection](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#server-selection)
  * [Custom HTTP Client](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#custom-http-client)
  * [Resource Management](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#resource-management)
  * [Debugging](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#debugging)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install ttd-workflows
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add ttd-workflows
```

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from ttd-workflows python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "ttd-workflows",
# ]
# ///

from ttd_workflows import Workflows

sdk = Workflows(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
import os
import ttd_workflows
from ttd_workflows import Workflows


with Workflows(
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:

    res = workflows.ad_groups.create(request={
        "primary_input": {
            "is_enabled": False,
            "description": "twine from gosh poor safely editor astride vice lost and",
            "budget": {
                "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                "budget_in_advertiser_currency": 3786.02,
                "budget_in_impressions": 783190,
                "daily_target_in_advertiser_currency": 9747.02,
                "daily_target_in_impressions": 985999,
            },
            "base_bid_cpm_in_advertiser_currency": 3785.04,
            "max_bid_cpm_in_advertiser_currency": 7447.3,
            "audience_targeting": {
                "audience_id": "<id>",
                "audience_accelerator_exclusions_enabled": True,
                "audience_booster_enabled": True,
                "audience_excluder_enabled": True,
                "audience_predictor_enabled": False,
                "cross_device_vendor_list_for_audience": [
                    107263,
                ],
                "recency_exclusion_window_in_minutes": 90062,
                "target_trackable_users_enabled": True,
                "use_mc_id_as_primary": True,
            },
            "roi_goal": {
                "maximize_reach": True,
                "maximize_ltv_incremental_reach": False,
                "cpc_in_advertiser_currency": 2280.31,
                "ctr_in_percent": None,
                "nielsen_otp_in_percent": 5175.21,
                "cpa_in_advertiser_currency": 2544.37,
                "return_on_ad_spend_percent": 8201.47,
                "vcr_in_percent": 4846.08,
                "viewability_in_percent": None,
                "vcpm_in_advertiser_currency": 4649.53,
                "cpcv_in_advertiser_currency": 313.95,
                "miaozhen_otp_in_percent": 4704.1,
            },
            "creative_ids": None,
            "associated_bid_lists": [
                {
                    "bid_list_id": "<id>",
                    "is_enabled": False,
                    "is_default_for_dimension": True,
                },
            ],
            "name": "<value>",
            "channel": ttd_workflows.AdGroupChannel.DISPLAY,
            "funnel_location": ttd_workflows.AdGroupFunnelLocation.CONSIDERATION,
            "programmatic_guaranteed_private_contract_id": "<id>",
        },
        "campaign_id": "<id>",
        "advanced_input": {
            "koa_optimization_settings": {
                "are_future_koa_features_enabled": False,
                "predictive_clearing_enabled": False,
            },
            "comscore_settings": {
                "is_enabled": False,
                "population_id": None,
                "demographic_member_ids": [
                    959580,
                    236376,
                ],
                "mobile_demographic_member_ids": [
                    664689,
                    827980,
                    21321,
                ],
            },
            "contract_targeting": {
                "allow_open_market_bidding_when_targeting_contracts": True,
            },
            "dimensional_bidding_auto_optimization_settings": [
                [],
                [],
            ],
            "is_use_clicks_as_conversions_enabled": False,
            "is_use_secondary_conversions_enabled": False,
            "nielsen_tracking_attributes": {
                "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                "gender": ttd_workflows.TargetingGender.MALE,
                "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                "end_age": ttd_workflows.TargetingEndAge.SEVENTEEN,
                "countries": [
                    "<value 1>",
                    "<value 2>",
                    "<value 3>",
                ],
            },
            "new_frequency_configs": [
                {
                    "counter_name": None,
                    "frequency_cap": 375286,
                    "frequency_goal": 534735,
                    "reset_interval_in_minutes": 788122,
                },
            ],
            "flights": [
                {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 4070.96,
                    "budget_in_impressions": 901477,
                    "daily_target_in_advertiser_currency": 5847.35,
                    "daily_target_in_impressions": 257517,
                    "campaign_flight_id": 874887,
                },
            ],
        },
        "validate_input_only": True,
    })

    assert res.ad_group_payload is not None

    # Handle response
    print(res.ad_group_payload)
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
import os
import ttd_workflows
from ttd_workflows import Workflows

async def main():

    async with Workflows(
        ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
    ) as workflows:

        res = await workflows.ad_groups.create_async(request={
            "primary_input": {
                "is_enabled": False,
                "description": "twine from gosh poor safely editor astride vice lost and",
                "budget": {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 3786.02,
                    "budget_in_impressions": 783190,
                    "daily_target_in_advertiser_currency": 9747.02,
                    "daily_target_in_impressions": 985999,
                },
                "base_bid_cpm_in_advertiser_currency": 3785.04,
                "max_bid_cpm_in_advertiser_currency": 7447.3,
                "audience_targeting": {
                    "audience_id": "<id>",
                    "audience_accelerator_exclusions_enabled": True,
                    "audience_booster_enabled": True,
                    "audience_excluder_enabled": True,
                    "audience_predictor_enabled": False,
                    "cross_device_vendor_list_for_audience": [
                        107263,
                    ],
                    "recency_exclusion_window_in_minutes": 90062,
                    "target_trackable_users_enabled": True,
                    "use_mc_id_as_primary": True,
                },
                "roi_goal": {
                    "maximize_reach": True,
                    "maximize_ltv_incremental_reach": False,
                    "cpc_in_advertiser_currency": 2280.31,
                    "ctr_in_percent": None,
                    "nielsen_otp_in_percent": 5175.21,
                    "cpa_in_advertiser_currency": 2544.37,
                    "return_on_ad_spend_percent": 8201.47,
                    "vcr_in_percent": 4846.08,
                    "viewability_in_percent": None,
                    "vcpm_in_advertiser_currency": 4649.53,
                    "cpcv_in_advertiser_currency": 313.95,
                    "miaozhen_otp_in_percent": 4704.1,
                },
                "creative_ids": None,
                "associated_bid_lists": [
                    {
                        "bid_list_id": "<id>",
                        "is_enabled": False,
                        "is_default_for_dimension": True,
                    },
                ],
                "name": "<value>",
                "channel": ttd_workflows.AdGroupChannel.DISPLAY,
                "funnel_location": ttd_workflows.AdGroupFunnelLocation.CONSIDERATION,
                "programmatic_guaranteed_private_contract_id": "<id>",
            },
            "campaign_id": "<id>",
            "advanced_input": {
                "koa_optimization_settings": {
                    "are_future_koa_features_enabled": False,
                    "predictive_clearing_enabled": False,
                },
                "comscore_settings": {
                    "is_enabled": False,
                    "population_id": None,
                    "demographic_member_ids": [
                        959580,
                        236376,
                    ],
                    "mobile_demographic_member_ids": [
                        664689,
                        827980,
                        21321,
                    ],
                },
                "contract_targeting": {
                    "allow_open_market_bidding_when_targeting_contracts": True,
                },
                "dimensional_bidding_auto_optimization_settings": [
                    [],
                    [],
                ],
                "is_use_clicks_as_conversions_enabled": False,
                "is_use_secondary_conversions_enabled": False,
                "nielsen_tracking_attributes": {
                    "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                    "gender": ttd_workflows.TargetingGender.MALE,
                    "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                    "end_age": ttd_workflows.TargetingEndAge.SEVENTEEN,
                    "countries": [
                        "<value 1>",
                        "<value 2>",
                        "<value 3>",
                    ],
                },
                "new_frequency_configs": [
                    {
                        "counter_name": None,
                        "frequency_cap": 375286,
                        "frequency_goal": 534735,
                        "reset_interval_in_minutes": 788122,
                    },
                ],
                "flights": [
                    {
                        "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                        "budget_in_advertiser_currency": 4070.96,
                        "budget_in_impressions": 901477,
                        "daily_target_in_advertiser_currency": 5847.35,
                        "daily_target_in_impressions": 257517,
                        "campaign_flight_id": 874887,
                    },
                ],
            },
            "validate_input_only": True,
        })

        assert res.ad_group_payload is not None

        # Handle response
        print(res.ad_group_payload)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name       | Type   | Scheme  | Environment Variable |
| ---------- | ------ | ------- | -------------------- |
| `ttd_auth` | apiKey | API key | `WORKFLOWS_TTD_AUTH` |

To authenticate with the API the `ttd_auth` parameter must be set when initializing the SDK client instance. For example:
```python
import os
import ttd_workflows
from ttd_workflows import Workflows


with Workflows(
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:

    res = workflows.ad_groups.create(request={
        "primary_input": {
            "is_enabled": False,
            "description": "twine from gosh poor safely editor astride vice lost and",
            "budget": {
                "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                "budget_in_advertiser_currency": 3786.02,
                "budget_in_impressions": 783190,
                "daily_target_in_advertiser_currency": 9747.02,
                "daily_target_in_impressions": 985999,
            },
            "base_bid_cpm_in_advertiser_currency": 3785.04,
            "max_bid_cpm_in_advertiser_currency": 7447.3,
            "audience_targeting": {
                "audience_id": "<id>",
                "audience_accelerator_exclusions_enabled": True,
                "audience_booster_enabled": True,
                "audience_excluder_enabled": True,
                "audience_predictor_enabled": False,
                "cross_device_vendor_list_for_audience": [
                    107263,
                ],
                "recency_exclusion_window_in_minutes": 90062,
                "target_trackable_users_enabled": True,
                "use_mc_id_as_primary": True,
            },
            "roi_goal": {
                "maximize_reach": True,
                "maximize_ltv_incremental_reach": False,
                "cpc_in_advertiser_currency": 2280.31,
                "ctr_in_percent": None,
                "nielsen_otp_in_percent": 5175.21,
                "cpa_in_advertiser_currency": 2544.37,
                "return_on_ad_spend_percent": 8201.47,
                "vcr_in_percent": 4846.08,
                "viewability_in_percent": None,
                "vcpm_in_advertiser_currency": 4649.53,
                "cpcv_in_advertiser_currency": 313.95,
                "miaozhen_otp_in_percent": 4704.1,
            },
            "creative_ids": None,
            "associated_bid_lists": [
                {
                    "bid_list_id": "<id>",
                    "is_enabled": False,
                    "is_default_for_dimension": True,
                },
            ],
            "name": "<value>",
            "channel": ttd_workflows.AdGroupChannel.DISPLAY,
            "funnel_location": ttd_workflows.AdGroupFunnelLocation.CONSIDERATION,
            "programmatic_guaranteed_private_contract_id": "<id>",
        },
        "campaign_id": "<id>",
        "advanced_input": {
            "koa_optimization_settings": {
                "are_future_koa_features_enabled": False,
                "predictive_clearing_enabled": False,
            },
            "comscore_settings": {
                "is_enabled": False,
                "population_id": None,
                "demographic_member_ids": [
                    959580,
                    236376,
                ],
                "mobile_demographic_member_ids": [
                    664689,
                    827980,
                    21321,
                ],
            },
            "contract_targeting": {
                "allow_open_market_bidding_when_targeting_contracts": True,
            },
            "dimensional_bidding_auto_optimization_settings": [
                [],
                [],
            ],
            "is_use_clicks_as_conversions_enabled": False,
            "is_use_secondary_conversions_enabled": False,
            "nielsen_tracking_attributes": {
                "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                "gender": ttd_workflows.TargetingGender.MALE,
                "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                "end_age": ttd_workflows.TargetingEndAge.SEVENTEEN,
                "countries": [
                    "<value 1>",
                    "<value 2>",
                    "<value 3>",
                ],
            },
            "new_frequency_configs": [
                {
                    "counter_name": None,
                    "frequency_cap": 375286,
                    "frequency_goal": 534735,
                    "reset_interval_in_minutes": 788122,
                },
            ],
            "flights": [
                {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 4070.96,
                    "budget_in_impressions": 901477,
                    "daily_target_in_advertiser_currency": 5847.35,
                    "daily_target_in_impressions": 257517,
                    "campaign_flight_id": 874887,
                },
            ],
        },
        "validate_input_only": True,
    })

    assert res.ad_group_payload is not None

    # Handle response
    print(res.ad_group_payload)

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [ad_group](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/adgroup/README.md)

* [create_ad_groups_job](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/adgroup/README.md#create_ad_groups_job) - Create multiple new ad groups with required fields
* [update_ad_groups_job](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/adgroup/README.md#update_ad_groups_job) - Update multiple ad groups with specified fields

### [ad_groups](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/adgroups/README.md)

* [create](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/adgroups/README.md#create) - Create a new ad group with required fields
* [update](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/adgroups/README.md#update) - Update an ad group with specified fields
* [archive](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/adgroups/README.md#archive) - Archive multiple ad groups

### [campaign](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/campaign/README.md)

* [create](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/campaign/README.md#create) - Create a new campaign with required fields
* [create_campaigns_job](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/campaign/README.md#create_campaigns_job) - Create multiple new campaigns with required fields
* [update_campaigns_job](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/campaign/README.md#update_campaigns_job) - Update multiple campaigns with specified fields
* [get_version](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/campaign/README.md#get_version) - Get a campaign's version

### [campaigns](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/campaigns/README.md)

* [update](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/campaigns/README.md#update) - Update a campaign with specified fields
* [archive](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/campaigns/README.md#archive) - Archive multiple campaigns

### [dmp](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/dmp/README.md)

* [get_first_party_data_job](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/dmp/README.md#get_first_party_data_job) - Submit a job for first-party data retrieval for an advertiser
* [get_third_party_data_job](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/dmp/README.md#get_third_party_data_job) - Submit a job for third-party data retrieval for a partner

### [graph_ql_request](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/graphqlrequest/README.md)

* [submit_graph_ql_request](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/graphqlrequest/README.md#submit_graph_ql_request) - Submit a valid GraphQL query or mutation
* [submit_graph_ql_query_job](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/graphqlrequest/README.md#submit_graph_ql_query_job) - Submit a valid bulk GraphQL query

### [job_status](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/jobstatus/README.md)

* [get_graph_ql_query_job_status](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/jobstatus/README.md#get_graph_ql_query_job_status) - Get the status of a previously submitted GraphQL query job.
* [get_job_status](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/jobstatus/README.md#get_job_status) - Get the status of a previously submitted job

### [rest_request](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/restrequest/README.md)

* [submit_rest_request](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/restrequest/README.md#submit_rest_request) - Submit a valid REST request


</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
import os
import ttd_workflows
from ttd_workflows import Workflows
from ttd_workflows.utils import BackoffStrategy, RetryConfig


with Workflows(
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:

    res = workflows.ad_groups.create(request={
        "primary_input": {
            "is_enabled": False,
            "description": "twine from gosh poor safely editor astride vice lost and",
            "budget": {
                "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                "budget_in_advertiser_currency": 3786.02,
                "budget_in_impressions": 783190,
                "daily_target_in_advertiser_currency": 9747.02,
                "daily_target_in_impressions": 985999,
            },
            "base_bid_cpm_in_advertiser_currency": 3785.04,
            "max_bid_cpm_in_advertiser_currency": 7447.3,
            "audience_targeting": {
                "audience_id": "<id>",
                "audience_accelerator_exclusions_enabled": True,
                "audience_booster_enabled": True,
                "audience_excluder_enabled": True,
                "audience_predictor_enabled": False,
                "cross_device_vendor_list_for_audience": [
                    107263,
                ],
                "recency_exclusion_window_in_minutes": 90062,
                "target_trackable_users_enabled": True,
                "use_mc_id_as_primary": True,
            },
            "roi_goal": {
                "maximize_reach": True,
                "maximize_ltv_incremental_reach": False,
                "cpc_in_advertiser_currency": 2280.31,
                "ctr_in_percent": None,
                "nielsen_otp_in_percent": 5175.21,
                "cpa_in_advertiser_currency": 2544.37,
                "return_on_ad_spend_percent": 8201.47,
                "vcr_in_percent": 4846.08,
                "viewability_in_percent": None,
                "vcpm_in_advertiser_currency": 4649.53,
                "cpcv_in_advertiser_currency": 313.95,
                "miaozhen_otp_in_percent": 4704.1,
            },
            "creative_ids": None,
            "associated_bid_lists": [
                {
                    "bid_list_id": "<id>",
                    "is_enabled": False,
                    "is_default_for_dimension": True,
                },
            ],
            "name": "<value>",
            "channel": ttd_workflows.AdGroupChannel.DISPLAY,
            "funnel_location": ttd_workflows.AdGroupFunnelLocation.CONSIDERATION,
            "programmatic_guaranteed_private_contract_id": "<id>",
        },
        "campaign_id": "<id>",
        "advanced_input": {
            "koa_optimization_settings": {
                "are_future_koa_features_enabled": False,
                "predictive_clearing_enabled": False,
            },
            "comscore_settings": {
                "is_enabled": False,
                "population_id": None,
                "demographic_member_ids": [
                    959580,
                    236376,
                ],
                "mobile_demographic_member_ids": [
                    664689,
                    827980,
                    21321,
                ],
            },
            "contract_targeting": {
                "allow_open_market_bidding_when_targeting_contracts": True,
            },
            "dimensional_bidding_auto_optimization_settings": [
                [],
                [],
            ],
            "is_use_clicks_as_conversions_enabled": False,
            "is_use_secondary_conversions_enabled": False,
            "nielsen_tracking_attributes": {
                "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                "gender": ttd_workflows.TargetingGender.MALE,
                "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                "end_age": ttd_workflows.TargetingEndAge.SEVENTEEN,
                "countries": [
                    "<value 1>",
                    "<value 2>",
                    "<value 3>",
                ],
            },
            "new_frequency_configs": [
                {
                    "counter_name": None,
                    "frequency_cap": 375286,
                    "frequency_goal": 534735,
                    "reset_interval_in_minutes": 788122,
                },
            ],
            "flights": [
                {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 4070.96,
                    "budget_in_impressions": 901477,
                    "daily_target_in_advertiser_currency": 5847.35,
                    "daily_target_in_impressions": 257517,
                    "campaign_flight_id": 874887,
                },
            ],
        },
        "validate_input_only": True,
    },
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    assert res.ad_group_payload is not None

    # Handle response
    print(res.ad_group_payload)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
import os
import ttd_workflows
from ttd_workflows import Workflows
from ttd_workflows.utils import BackoffStrategy, RetryConfig


with Workflows(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:

    res = workflows.ad_groups.create(request={
        "primary_input": {
            "is_enabled": False,
            "description": "twine from gosh poor safely editor astride vice lost and",
            "budget": {
                "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                "budget_in_advertiser_currency": 3786.02,
                "budget_in_impressions": 783190,
                "daily_target_in_advertiser_currency": 9747.02,
                "daily_target_in_impressions": 985999,
            },
            "base_bid_cpm_in_advertiser_currency": 3785.04,
            "max_bid_cpm_in_advertiser_currency": 7447.3,
            "audience_targeting": {
                "audience_id": "<id>",
                "audience_accelerator_exclusions_enabled": True,
                "audience_booster_enabled": True,
                "audience_excluder_enabled": True,
                "audience_predictor_enabled": False,
                "cross_device_vendor_list_for_audience": [
                    107263,
                ],
                "recency_exclusion_window_in_minutes": 90062,
                "target_trackable_users_enabled": True,
                "use_mc_id_as_primary": True,
            },
            "roi_goal": {
                "maximize_reach": True,
                "maximize_ltv_incremental_reach": False,
                "cpc_in_advertiser_currency": 2280.31,
                "ctr_in_percent": None,
                "nielsen_otp_in_percent": 5175.21,
                "cpa_in_advertiser_currency": 2544.37,
                "return_on_ad_spend_percent": 8201.47,
                "vcr_in_percent": 4846.08,
                "viewability_in_percent": None,
                "vcpm_in_advertiser_currency": 4649.53,
                "cpcv_in_advertiser_currency": 313.95,
                "miaozhen_otp_in_percent": 4704.1,
            },
            "creative_ids": None,
            "associated_bid_lists": [
                {
                    "bid_list_id": "<id>",
                    "is_enabled": False,
                    "is_default_for_dimension": True,
                },
            ],
            "name": "<value>",
            "channel": ttd_workflows.AdGroupChannel.DISPLAY,
            "funnel_location": ttd_workflows.AdGroupFunnelLocation.CONSIDERATION,
            "programmatic_guaranteed_private_contract_id": "<id>",
        },
        "campaign_id": "<id>",
        "advanced_input": {
            "koa_optimization_settings": {
                "are_future_koa_features_enabled": False,
                "predictive_clearing_enabled": False,
            },
            "comscore_settings": {
                "is_enabled": False,
                "population_id": None,
                "demographic_member_ids": [
                    959580,
                    236376,
                ],
                "mobile_demographic_member_ids": [
                    664689,
                    827980,
                    21321,
                ],
            },
            "contract_targeting": {
                "allow_open_market_bidding_when_targeting_contracts": True,
            },
            "dimensional_bidding_auto_optimization_settings": [
                [],
                [],
            ],
            "is_use_clicks_as_conversions_enabled": False,
            "is_use_secondary_conversions_enabled": False,
            "nielsen_tracking_attributes": {
                "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                "gender": ttd_workflows.TargetingGender.MALE,
                "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                "end_age": ttd_workflows.TargetingEndAge.SEVENTEEN,
                "countries": [
                    "<value 1>",
                    "<value 2>",
                    "<value 3>",
                ],
            },
            "new_frequency_configs": [
                {
                    "counter_name": None,
                    "frequency_cap": 375286,
                    "frequency_goal": 534735,
                    "reset_interval_in_minutes": 788122,
                },
            ],
            "flights": [
                {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 4070.96,
                    "budget_in_impressions": 901477,
                    "daily_target_in_advertiser_currency": 5847.35,
                    "daily_target_in_impressions": 257517,
                    "campaign_flight_id": 874887,
                },
            ],
        },
        "validate_input_only": True,
    })

    assert res.ad_group_payload is not None

    # Handle response
    print(res.ad_group_payload)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

[`WorkflowsError`](https://github.com/thetradedesk/ttd-workflows-python/blob/master/./src/ttd_workflows/models/workflowserror.py) is the base class for all HTTP error responses. It has the following properties:

| Property           | Type             | Description                                                                             |
| ------------------ | ---------------- | --------------------------------------------------------------------------------------- |
| `err.message`      | `str`            | Error message                                                                           |
| `err.status_code`  | `int`            | HTTP response status code eg `404`                                                      |
| `err.headers`      | `httpx.Headers`  | HTTP response headers                                                                   |
| `err.body`         | `str`            | HTTP body. Can be empty string if no body is returned.                                  |
| `err.raw_response` | `httpx.Response` | Raw HTTP response                                                                       |
| `err.data`         |                  | Optional. Some errors may contain structured data. [See Error Classes](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#error-classes). |

### Example
```python
import os
import ttd_workflows
from ttd_workflows import Workflows, models


with Workflows(
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:
    res = None
    try:

        res = workflows.ad_groups.create(request={
            "primary_input": {
                "is_enabled": False,
                "description": "twine from gosh poor safely editor astride vice lost and",
                "budget": {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 3786.02,
                    "budget_in_impressions": 783190,
                    "daily_target_in_advertiser_currency": 9747.02,
                    "daily_target_in_impressions": 985999,
                },
                "base_bid_cpm_in_advertiser_currency": 3785.04,
                "max_bid_cpm_in_advertiser_currency": 7447.3,
                "audience_targeting": {
                    "audience_id": "<id>",
                    "audience_accelerator_exclusions_enabled": True,
                    "audience_booster_enabled": True,
                    "audience_excluder_enabled": True,
                    "audience_predictor_enabled": False,
                    "cross_device_vendor_list_for_audience": [
                        107263,
                    ],
                    "recency_exclusion_window_in_minutes": 90062,
                    "target_trackable_users_enabled": True,
                    "use_mc_id_as_primary": True,
                },
                "roi_goal": {
                    "maximize_reach": True,
                    "maximize_ltv_incremental_reach": False,
                    "cpc_in_advertiser_currency": 2280.31,
                    "ctr_in_percent": None,
                    "nielsen_otp_in_percent": 5175.21,
                    "cpa_in_advertiser_currency": 2544.37,
                    "return_on_ad_spend_percent": 8201.47,
                    "vcr_in_percent": 4846.08,
                    "viewability_in_percent": None,
                    "vcpm_in_advertiser_currency": 4649.53,
                    "cpcv_in_advertiser_currency": 313.95,
                    "miaozhen_otp_in_percent": 4704.1,
                },
                "creative_ids": None,
                "associated_bid_lists": [
                    {
                        "bid_list_id": "<id>",
                        "is_enabled": False,
                        "is_default_for_dimension": True,
                    },
                ],
                "name": "<value>",
                "channel": ttd_workflows.AdGroupChannel.DISPLAY,
                "funnel_location": ttd_workflows.AdGroupFunnelLocation.CONSIDERATION,
                "programmatic_guaranteed_private_contract_id": "<id>",
            },
            "campaign_id": "<id>",
            "advanced_input": {
                "koa_optimization_settings": {
                    "are_future_koa_features_enabled": False,
                    "predictive_clearing_enabled": False,
                },
                "comscore_settings": {
                    "is_enabled": False,
                    "population_id": None,
                    "demographic_member_ids": [
                        959580,
                        236376,
                    ],
                    "mobile_demographic_member_ids": [
                        664689,
                        827980,
                        21321,
                    ],
                },
                "contract_targeting": {
                    "allow_open_market_bidding_when_targeting_contracts": True,
                },
                "dimensional_bidding_auto_optimization_settings": [
                    [],
                    [],
                ],
                "is_use_clicks_as_conversions_enabled": False,
                "is_use_secondary_conversions_enabled": False,
                "nielsen_tracking_attributes": {
                    "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                    "gender": ttd_workflows.TargetingGender.MALE,
                    "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                    "end_age": ttd_workflows.TargetingEndAge.SEVENTEEN,
                    "countries": [
                        "<value 1>",
                        "<value 2>",
                        "<value 3>",
                    ],
                },
                "new_frequency_configs": [
                    {
                        "counter_name": None,
                        "frequency_cap": 375286,
                        "frequency_goal": 534735,
                        "reset_interval_in_minutes": 788122,
                    },
                ],
                "flights": [
                    {
                        "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                        "budget_in_advertiser_currency": 4070.96,
                        "budget_in_impressions": 901477,
                        "daily_target_in_advertiser_currency": 5847.35,
                        "daily_target_in_impressions": 257517,
                        "campaign_flight_id": 874887,
                    },
                ],
            },
            "validate_input_only": True,
        })

        assert res.ad_group_payload is not None

        # Handle response
        print(res.ad_group_payload)


    except models.WorkflowsError as e:
        # The base class for HTTP error responses
        print(e.message)
        print(e.status_code)
        print(e.body)
        print(e.headers)
        print(e.raw_response)

        # Depending on the method different errors may be thrown
        if isinstance(e, models.ProblemDetailsError):
            print(e.data.type)  # OptionalNullable[str]
            print(e.data.title)  # OptionalNullable[str]
            print(e.data.status)  # OptionalNullable[int]
            print(e.data.detail)  # OptionalNullable[str]
            print(e.data.instance)  # OptionalNullable[str]
```

### Error Classes
**Primary errors:**
* [`WorkflowsError`](https://github.com/thetradedesk/ttd-workflows-python/blob/master/./src/ttd_workflows/models/workflowserror.py): The base class for HTTP error responses.
  * [`ProblemDetailsError`](https://github.com/thetradedesk/ttd-workflows-python/blob/master/./src/ttd_workflows/models/problemdetailserror.py): Bad Request.

<details><summary>Less common errors (5)</summary>

<br />

**Network errors:**
* [`httpx.RequestError`](https://www.python-httpx.org/exceptions/#httpx.RequestError): Base class for request errors.
    * [`httpx.ConnectError`](https://www.python-httpx.org/exceptions/#httpx.ConnectError): HTTP client was unable to make a request to a server.
    * [`httpx.TimeoutException`](https://www.python-httpx.org/exceptions/#httpx.TimeoutException): HTTP request timed out.


**Inherit from [`WorkflowsError`](https://github.com/thetradedesk/ttd-workflows-python/blob/master/./src/ttd_workflows/models/workflowserror.py)**:
* [`ResponseValidationError`](https://github.com/thetradedesk/ttd-workflows-python/blob/master/./src/ttd_workflows/models/responsevalidationerror.py): Type mismatch between the response data and the expected Pydantic model. Provides access to the Pydantic validation error via the `cause` attribute.

</details>
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Select Server by Name

You can override the default server globally by passing a server name to the `server: str` optional parameter when initializing the SDK client instance. The selected server will then be used as the default on the operations that use it. This table lists the names associated with the available servers:

| Name      | Server                                          | Description                          |
| --------- | ----------------------------------------------- | ------------------------------------ |
| `prod`    | `https://api.thetradedesk.com/workflows`        | The production environment.          |
| `sandbox` | `https://ext-api.sb.thetradedesk.com/workflows` | The sandbox environment for testing. |

#### Example

```python
import os
import ttd_workflows
from ttd_workflows import Workflows


with Workflows(
    server="sandbox",
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:

    res = workflows.ad_groups.create(request={
        "primary_input": {
            "is_enabled": False,
            "description": "twine from gosh poor safely editor astride vice lost and",
            "budget": {
                "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                "budget_in_advertiser_currency": 3786.02,
                "budget_in_impressions": 783190,
                "daily_target_in_advertiser_currency": 9747.02,
                "daily_target_in_impressions": 985999,
            },
            "base_bid_cpm_in_advertiser_currency": 3785.04,
            "max_bid_cpm_in_advertiser_currency": 7447.3,
            "audience_targeting": {
                "audience_id": "<id>",
                "audience_accelerator_exclusions_enabled": True,
                "audience_booster_enabled": True,
                "audience_excluder_enabled": True,
                "audience_predictor_enabled": False,
                "cross_device_vendor_list_for_audience": [
                    107263,
                ],
                "recency_exclusion_window_in_minutes": 90062,
                "target_trackable_users_enabled": True,
                "use_mc_id_as_primary": True,
            },
            "roi_goal": {
                "maximize_reach": True,
                "maximize_ltv_incremental_reach": False,
                "cpc_in_advertiser_currency": 2280.31,
                "ctr_in_percent": None,
                "nielsen_otp_in_percent": 5175.21,
                "cpa_in_advertiser_currency": 2544.37,
                "return_on_ad_spend_percent": 8201.47,
                "vcr_in_percent": 4846.08,
                "viewability_in_percent": None,
                "vcpm_in_advertiser_currency": 4649.53,
                "cpcv_in_advertiser_currency": 313.95,
                "miaozhen_otp_in_percent": 4704.1,
            },
            "creative_ids": None,
            "associated_bid_lists": [
                {
                    "bid_list_id": "<id>",
                    "is_enabled": False,
                    "is_default_for_dimension": True,
                },
            ],
            "name": "<value>",
            "channel": ttd_workflows.AdGroupChannel.DISPLAY,
            "funnel_location": ttd_workflows.AdGroupFunnelLocation.CONSIDERATION,
            "programmatic_guaranteed_private_contract_id": "<id>",
        },
        "campaign_id": "<id>",
        "advanced_input": {
            "koa_optimization_settings": {
                "are_future_koa_features_enabled": False,
                "predictive_clearing_enabled": False,
            },
            "comscore_settings": {
                "is_enabled": False,
                "population_id": None,
                "demographic_member_ids": [
                    959580,
                    236376,
                ],
                "mobile_demographic_member_ids": [
                    664689,
                    827980,
                    21321,
                ],
            },
            "contract_targeting": {
                "allow_open_market_bidding_when_targeting_contracts": True,
            },
            "dimensional_bidding_auto_optimization_settings": [
                [],
                [],
            ],
            "is_use_clicks_as_conversions_enabled": False,
            "is_use_secondary_conversions_enabled": False,
            "nielsen_tracking_attributes": {
                "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                "gender": ttd_workflows.TargetingGender.MALE,
                "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                "end_age": ttd_workflows.TargetingEndAge.SEVENTEEN,
                "countries": [
                    "<value 1>",
                    "<value 2>",
                    "<value 3>",
                ],
            },
            "new_frequency_configs": [
                {
                    "counter_name": None,
                    "frequency_cap": 375286,
                    "frequency_goal": 534735,
                    "reset_interval_in_minutes": 788122,
                },
            ],
            "flights": [
                {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 4070.96,
                    "budget_in_impressions": 901477,
                    "daily_target_in_advertiser_currency": 5847.35,
                    "daily_target_in_impressions": 257517,
                    "campaign_flight_id": 874887,
                },
            ],
        },
        "validate_input_only": True,
    })

    assert res.ad_group_payload is not None

    # Handle response
    print(res.ad_group_payload)

```

### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
import os
import ttd_workflows
from ttd_workflows import Workflows


with Workflows(
    server_url="https://api.thetradedesk.com/workflows",
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:

    res = workflows.ad_groups.create(request={
        "primary_input": {
            "is_enabled": False,
            "description": "twine from gosh poor safely editor astride vice lost and",
            "budget": {
                "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                "budget_in_advertiser_currency": 3786.02,
                "budget_in_impressions": 783190,
                "daily_target_in_advertiser_currency": 9747.02,
                "daily_target_in_impressions": 985999,
            },
            "base_bid_cpm_in_advertiser_currency": 3785.04,
            "max_bid_cpm_in_advertiser_currency": 7447.3,
            "audience_targeting": {
                "audience_id": "<id>",
                "audience_accelerator_exclusions_enabled": True,
                "audience_booster_enabled": True,
                "audience_excluder_enabled": True,
                "audience_predictor_enabled": False,
                "cross_device_vendor_list_for_audience": [
                    107263,
                ],
                "recency_exclusion_window_in_minutes": 90062,
                "target_trackable_users_enabled": True,
                "use_mc_id_as_primary": True,
            },
            "roi_goal": {
                "maximize_reach": True,
                "maximize_ltv_incremental_reach": False,
                "cpc_in_advertiser_currency": 2280.31,
                "ctr_in_percent": None,
                "nielsen_otp_in_percent": 5175.21,
                "cpa_in_advertiser_currency": 2544.37,
                "return_on_ad_spend_percent": 8201.47,
                "vcr_in_percent": 4846.08,
                "viewability_in_percent": None,
                "vcpm_in_advertiser_currency": 4649.53,
                "cpcv_in_advertiser_currency": 313.95,
                "miaozhen_otp_in_percent": 4704.1,
            },
            "creative_ids": None,
            "associated_bid_lists": [
                {
                    "bid_list_id": "<id>",
                    "is_enabled": False,
                    "is_default_for_dimension": True,
                },
            ],
            "name": "<value>",
            "channel": ttd_workflows.AdGroupChannel.DISPLAY,
            "funnel_location": ttd_workflows.AdGroupFunnelLocation.CONSIDERATION,
            "programmatic_guaranteed_private_contract_id": "<id>",
        },
        "campaign_id": "<id>",
        "advanced_input": {
            "koa_optimization_settings": {
                "are_future_koa_features_enabled": False,
                "predictive_clearing_enabled": False,
            },
            "comscore_settings": {
                "is_enabled": False,
                "population_id": None,
                "demographic_member_ids": [
                    959580,
                    236376,
                ],
                "mobile_demographic_member_ids": [
                    664689,
                    827980,
                    21321,
                ],
            },
            "contract_targeting": {
                "allow_open_market_bidding_when_targeting_contracts": True,
            },
            "dimensional_bidding_auto_optimization_settings": [
                [],
                [],
            ],
            "is_use_clicks_as_conversions_enabled": False,
            "is_use_secondary_conversions_enabled": False,
            "nielsen_tracking_attributes": {
                "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                "gender": ttd_workflows.TargetingGender.MALE,
                "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                "end_age": ttd_workflows.TargetingEndAge.SEVENTEEN,
                "countries": [
                    "<value 1>",
                    "<value 2>",
                    "<value 3>",
                ],
            },
            "new_frequency_configs": [
                {
                    "counter_name": None,
                    "frequency_cap": 375286,
                    "frequency_goal": 534735,
                    "reset_interval_in_minutes": 788122,
                },
            ],
            "flights": [
                {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 4070.96,
                    "budget_in_impressions": 901477,
                    "daily_target_in_advertiser_currency": 5847.35,
                    "daily_target_in_impressions": 257517,
                    "campaign_flight_id": 874887,
                },
            ],
        },
        "validate_input_only": True,
    })

    assert res.ad_group_payload is not None

    # Handle response
    print(res.ad_group_payload)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from ttd_workflows import Workflows
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Workflows(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from ttd_workflows import Workflows
from ttd_workflows.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Workflows(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `Workflows` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
import os
from ttd_workflows import Workflows
def main():

    with Workflows(
        ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
    ) as workflows:
        # Rest of application here...


# Or when using async:
async def amain():

    async with Workflows(
        ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
    ) as workflows:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from ttd_workflows import Workflows
import logging

logging.basicConfig(level=logging.DEBUG)
s = Workflows(debug_logger=logging.getLogger("ttd_workflows"))
```

You can also enable a default debug logger by setting an environment variable `WORKFLOWS_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->
