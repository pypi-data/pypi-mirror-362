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


# ────────────────────────────
# 🛠  Small generic helpers
# ────────────────────────────
def _remove_empty_str_values(d: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of *d* without keys whose value is an empty / blank string."""
    return {
        k: v
        for k, v in d.items()
        if not (isinstance(v, str) and v.strip() == "")
    }


def _build_common_params(
    search_params: BaseModel,
    max_entries: int,
    enrich_profiles: bool,
) -> Dict[str, Any]:
    """Convert a Pydantic model into Proxycurl query params, stripping empty strings."""
    params = search_params.model_dump(exclude_none=True)
    params = _remove_empty_str_values(params)

    params["page_size"] = max_entries if max_entries > 0 else 5
    params["enrich_profiles"] = "enrich" if enrich_profiles else "skip"
    params["use_cache"] = "if-present"
    return params


# ────────────────────────────
# 📄  Search parameter schemas
# ────────────────────────────
class PeopleSearchParams(BaseModel):
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
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    when: Optional[str] = None
    flexibility: Optional[str] = None
    geo_id: Optional[int] = None
    keyword: Optional[str] = None
    search_id: Optional[str] = None


# ────────────────────────────
# 👤  People search
# ────────────────────────────
@assistant_tool
async def proxycurl_people_search_leads(
    search_params: PeopleSearchParams,
    max_entries: int = 5,
    enrich_profiles: bool = False,
    tool_config: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """Search for leads on Proxycurl based on a plain‑English ICP description."""

    params = _build_common_params(search_params, max_entries, enrich_profiles)

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

    leads: List[Dict[str, Any]] = []
    for item in (data.get("results") or [])[:max_entries]:
        lead: Dict[str, Any] = {
            "user_linkedin_url": item.get("linkedin_profile_url"),
        }
        profile = item.get("profile") or {}
        if profile:
            first_exp = (profile.get("experiences") or [{}])[0]
            lead.update(
                {
                    "first_name": profile.get("first_name", ""),
                    "last_name": profile.get("last_name", ""),
                    "full_name": profile.get("full_name", ""),
                    "job_title": profile.get("occupation", ""),
                    "organization_name": first_exp.get("company", ""),
                    "organization_linkedin_url": first_exp.get(
                        "company_linkedin_profile_url", ""
                    ),
                }
            )
        if cleaned := cleanup_properties(lead):
            leads.append(cleaned)

    return leads


# ────────────────────────────
# 🏢  Company search
# ────────────────────────────
@assistant_tool
async def proxycurl_company_search_leads(
    search_params: CompanySearchParams,
    max_entries: int = 5,
    enrich_profiles: bool = False,
    tool_config: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """Search for companies on Proxycurl based on given parameters."""

    params = _build_common_params(search_params, max_entries, enrich_profiles)

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

    companies: List[Dict[str, Any]] = []
    for item in (data.get("results") or [])[:max_entries]:
        company: Dict[str, Any] = {
            "organization_linkedin_url": item.get("linkedin_profile_url"),
        }
        profile = item.get("profile") or {}
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
        if cleaned := cleanup_properties(company):
            companies.append(cleaned)

    return companies


# ────────────────────────────
# 💼  Job search
# ────────────────────────────
@assistant_tool
async def proxycurl_job_search(
    search_params: JobSearchParams,
    max_entries: int = 5,
    tool_config: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """List jobs posted by a company using Proxycurl's job search API."""

    # Job search endpoint does not support enrich_profiles
    params = _build_common_params(search_params, max_entries, enrich_profiles=False)

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

    job_entries: List[Dict[str, Any]] = []
    for item in (data.get("job") or data.get("jobs") or [])[:max_entries]:
        job: Dict[str, Any] = {
            "organization_name": item.get("company"),
            "organization_linkedin_url": item.get("company_url"),
            "job_title": item.get("job_title"),
            "job_posting_url": item.get("job_url"),
            "list_date": item.get("list_date"),
            "location": item.get("location"),
        }
        if cleaned := cleanup_properties(job):
            job_entries.append(cleaned)

    return job_entries