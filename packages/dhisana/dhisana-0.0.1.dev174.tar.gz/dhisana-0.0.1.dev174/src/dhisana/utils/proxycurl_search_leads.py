import logging
from typing import Any, Dict, List, Optional

import aiohttp
from pydantic import BaseModel

from dhisana.utils.generate_structured_output_internal import get_structured_output_internal
from dhisana.utils.proxy_curl_tools import get_proxycurl_access_token
from dhisana.utils.clean_properties import cleanup_properties
from dhisana.utils.assistant_tool_tag import assistant_tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PeopleSearchParams(BaseModel):
    """Subset of Proxycurl person search parameters used by this helper."""

    current_role_title: Optional[str] = None
    current_company_industry: Optional[str] = None
    current_company_employee_count_min: Optional[int] = None
    current_company_employee_count_max: Optional[int] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    summary: Optional[str] = None
    current_job_description: Optional[str] = None
    past_job_description: Optional[str] = None


class CompanySearchParams(BaseModel):
    """Subset of Proxycurl company search parameters used by this helper."""

    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    type: Optional[str] = None
    follower_count_min: Optional[int] = None
    follower_count_max: Optional[int] = None
    name: Optional[str] = None
    industry: Optional[str] = None
    employee_count_max: Optional[int] = None
    employee_count_min: Optional[int] = None
    description: Optional[str] = None
    founded_after_year: Optional[int] = None
    founded_before_year: Optional[int] = None
    funding_amount_max: Optional[int] = None
    funding_amount_min: Optional[int] = None
    funding_raised_after: Optional[str] = None
    funding_raised_before: Optional[str] = None
    public_identifier_in_list: Optional[str] = None
    public_identifier_not_in_list: Optional[str] = None


class JobSearchParams(BaseModel):
    """Parameters for Proxycurl's company job search API."""

    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    when: Optional[str] = None
    flexibility: Optional[str] = None
    geo_id: Optional[int] = None
    keyword: Optional[str] = None
    search_id: Optional[str] = None


@assistant_tool
async def proxycurl_people_search_leads(
    search_params: PeopleSearchParams,
    max_entries: int = 5,
    enrich_profiles: bool = False,
    tool_config: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """Search for leads on Proxycurl based on a plain-English ICP description."""


    if max_entries <= 0:
        max_entries = 5
    params = search_params.model_dump(exclude_none=True)
    params["page_size"] = max_entries
    if enrich_profiles:
        params["enrich_profiles"] = "enrich"
    else:
        params["enrich_profiles"] = "skip"
    params["use_cache"] = "if-present"

    api_key = get_proxycurl_access_token(tool_config)
    if not api_key:
        logger.error("PROXY_CURL_API_KEY not found")
        return []

    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://enrichlayer.com/api/v2/search/person"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    logger.error("Proxycurl search error %s", resp.status)
                    return []
                data = await resp.json()
    except Exception as exc:
        logger.exception("Exception during Proxycurl search: %s", exc)
        return []

    results = data.get("results") or []
    leads: List[Dict[str, Any]] = []

    for item in results[:max_entries]:
        lead = {}
        lead = {
            "user_linkedin_url": item.get("linkedin_profile_url"),
        }
        profile = item.get("profile", {}) if isinstance(item, dict) else {}
        if profile:
            experiences = profile.get("experiences") or []
            org_name = ""
            org_url = ""
            if experiences:
                first_exp = experiences[0]
                org_name = first_exp.get("company", "")
                org_url = first_exp.get("company_linkedin_profile_url", "")

            lead = {
                "first_name": profile.get("first_name", ""),
                "last_name": profile.get("last_name", ""),
                "full_name": profile.get("full_name", ""),
                "user_linkedin_url": item.get("linkedin_profile_url"),
                "job_title": profile.get("occupation", ""),
                "organization_name": org_name,
                "organization_linkedin_url": org_url,
            }
        cleaned = cleanup_properties(lead)
        if cleaned:
            leads.append(cleaned)

    return leads


@assistant_tool
async def proxycurl_company_search_leads(
    search_params: CompanySearchParams,
    max_entries: int = 5,
    enrich_profiles: bool = False,
    tool_config: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """Search for companies on Proxycurl based on given parameters."""

    if max_entries <= 0:
        max_entries = 5
    params = search_params.model_dump(exclude_none=True)
    params["page_size"] = max_entries
    params["enrich_profiles"] = "enrich" if enrich_profiles else "skip"
    params["use_cache"] = "if-present"

    api_key = get_proxycurl_access_token(tool_config)
    if not api_key:
        logger.error("PROXY_CURL_API_KEY not found")
        return []

    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://enrichlayer.com/api/v2/search/company"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    logger.error("Proxycurl company search error %s", resp.status)
                    return []
                data = await resp.json()
    except Exception as exc:
        logger.exception("Exception during Proxycurl company search: %s", exc)
        return []

    results = data.get("results") or []
    companies: List[Dict[str, Any]] = []

    for item in results[:max_entries]:
        company = {
            "organization_linkedin_url": item.get("linkedin_profile_url"),
        }
        profile = item.get("profile", {}) if isinstance(item, dict) else {}
        if profile:
            company.update(
                {
                    "organization_name": profile.get("name", ""),
                    "website": profile.get("website", ""),
                    "industry": profile.get("industry", ""),
                    "follower_count": profile.get("follower_count"),
                    "description": profile.get("description", ""),
                }
            )
        cleaned = cleanup_properties(company)
        if cleaned:
            companies.append(cleaned)

    return companies


@assistant_tool
async def proxycurl_job_search(
    search_params: JobSearchParams,
    max_entries: int = 5,
    tool_config: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """List jobs posted by a company using Proxycurl's job search API."""

    if max_entries <= 0:
        max_entries = 5
    params = search_params.model_dump(exclude_none=True)
    params["page_size"] = max_entries
    params["use_cache"] = "if-present"

    api_key = get_proxycurl_access_token(tool_config)
    if not api_key:
        logger.error("PROXY_CURL_API_KEY not found")
        return []

    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://enrichlayer.com/api/v2/company/job"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    logger.error("Proxycurl job search error %s", resp.status)
                    return []
                data = await resp.json()
    except Exception as exc:
        logger.exception("Exception during Proxycurl job search: %s", exc)
        return []

    jobs = data.get("job") or data.get("jobs") or []
    job_entries: List[Dict[str, Any]] = []

    for item in jobs[:max_entries]:
        job = {
            "organization_name": item.get("company"),
            "organization_linkedin_url": item.get("company_url"),
            "job_title": item.get("job_title"),
            "job_posting_url": item.get("job_url"),
            "list_date": item.get("list_date"),
            "location": item.get("location"),
        }
        cleaned = cleanup_properties(job)
        if cleaned:
            job_entries.append(cleaned)

    return job_entries