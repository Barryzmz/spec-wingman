from typing import Optional

from mcp.server.fastmcp import FastMCP

from tools.status import swm_status_tool
from tools.discover import swm_discover_context_tool, swm_write_discovery_tool
from tools.extract import swm_extract_context_tool, swm_write_extract_tool
from tools.clarify import swm_clarify_context_tool, swm_write_clarify_tool
from tools.analyze import swm_analyze_context_tool, swm_write_analyze_tool
from tools.spec import swm_spec_context_tool, swm_write_spec_tool
from tools.design import swm_design_context_tool, swm_write_design_tool
from tools.log import swm_log_context_tool, swm_write_log_tool
from tools.orchestrator import swm_next_tool

mcp = FastMCP("SpecWingman")


@mcp.tool()
def swm_next(project_path: str) -> str:
    """Orchestrator: inspect current workflow state and return the full context for the next pending step. The calling AI should process the returned context and call the corresponding swm_write_* tool, then call swm_next again to continue. Pauses at Step 3 when user answers are needed."""
    return swm_next_tool(project_path)


@mcp.tool()
def swm_status(project_path: str) -> str:
    """Scan specs/ directory and return SpecWingman workflow progress."""
    return swm_status_tool(project_path)


# ── Step 1: Discovery ──────────────────────────────────────────────────────────

@mcp.tool()
def swm_discover_context(project_path: str) -> str:
    """Step 1 (Discovery): Return the assembled prompt, CONSTITUTION, and all input files for the calling AI to process. After processing, call swm_write_discovery with the results."""
    return swm_discover_context_tool(project_path)


@mcp.tool()
def swm_write_discovery(
    project_path: str,
    source_summary: str,
    extracted_facts: str,
    open_questions: str,
    assumptions: str,
    glossary: str,
) -> str:
    """Step 1 (Discovery): Write the AI-generated discovery files to specs/01-discovery/."""
    return swm_write_discovery_tool(
        project_path, source_summary, extracted_facts, open_questions, assumptions, glossary
    )


# ── Step 2: Requirements ───────────────────────────────────────────────────────

@mcp.tool()
def swm_extract_context(project_path: str) -> str:
    """Step 2 (Requirements): Return the assembled prompt, CONSTITUTION, and discovery files for the calling AI to process. After processing, call swm_write_extract with the results."""
    return swm_extract_context_tool(project_path)


@mcp.tool()
def swm_write_extract(
    project_path: str,
    product_vision: str,
    functional_requirements: str,
    business_rules: str,
    data_requirements: str,
    workflow_requirements: str,
    permission_requirements: str,
    non_functional_requirements: str,
    user_roles: str,
) -> str:
    """Step 2 (Requirements): Write the AI-generated requirements files to specs/02-requirements/."""
    return swm_write_extract_tool(
        project_path,
        product_vision,
        functional_requirements,
        business_rules,
        data_requirements,
        workflow_requirements,
        permission_requirements,
        non_functional_requirements,
        user_roles,
    )


# ── Step 3: Clarify ────────────────────────────────────────────────────────────

@mcp.tool()
def swm_clarify_context(project_path: str) -> str:
    """Step 3 (Clarify): Return the assembled prompt, CONSTITUTION, discovery, requirements, and decision log for the calling AI to generate clarification questions. After the user answers, call swm_write_clarify with the full backfill."""
    return swm_clarify_context_tool(project_path)


@mcp.tool()
def swm_write_clarify(
    project_path: str,
    open_questions: str,
    answer_draft: Optional[str] = None,
    assumptions: Optional[str] = None,
    decision_log: Optional[str] = None,
) -> str:
    """Step 3 (Clarify): Write clarification outputs. Phase 1: pass only open_questions. Phase 2 (after user answers): pass all fields. answer_draft='' clears the file. None skips writing that file."""
    return swm_write_clarify_tool(
        project_path, open_questions, answer_draft, assumptions, decision_log
    )


# ── Step 4: Analyze ────────────────────────────────────────────────────────────

@mcp.tool()
def swm_analyze_context(project_path: str) -> str:
    """Step 4 (Analyze): Return the assembled prompt, CONSTITUTION, discovery, and requirements files for the calling AI to produce analysis documents. After processing, call swm_write_analyze with the results."""
    return swm_analyze_context_tool(project_path)


@mcp.tool()
def swm_write_analyze(
    project_path: str,
    use_cases: str,
    user_stories: str,
    acceptance_criteria: str,
    domain_model: str,
    state_transitions: str,
    edge_cases: str,
) -> str:
    """Step 4 (Analyze): Write the AI-generated analysis files to specs/03-analysis/."""
    return swm_write_analyze_tool(
        project_path,
        use_cases,
        user_stories,
        acceptance_criteria,
        domain_model,
        state_transitions,
        edge_cases,
    )


# ── Step 5: Spec ───────────────────────────────────────────────────────────────

@mcp.tool()
def swm_spec_context(project_path: str) -> str:
    """Step 5 (Spec): Return the assembled prompt, CONSTITUTION, all prior specs, and the requirement-spec template for the calling AI to generate the requirement spec. After processing, call swm_write_spec with the result."""
    return swm_spec_context_tool(project_path)


@mcp.tool()
def swm_write_spec(project_path: str, requirement_spec: str) -> str:
    """Step 5 (Spec): Write the AI-generated requirement spec to specs/04-design-ready/requirement-spec.md."""
    return swm_write_spec_tool(project_path, requirement_spec)


# ── Step 6: Design ─────────────────────────────────────────────────────────────

@mcp.tool()
def swm_design_context(project_path: str) -> str:
    """Step 6 (Design): Return the assembled prompt, CONSTITUTION, requirement-spec, and design templates for the calling AI to generate design-ready documents. After processing, call swm_write_design with the results."""
    return swm_design_context_tool(project_path)


@mcp.tool()
def swm_write_design(
    project_path: str,
    system_design_brief: str,
    api_draft: str,
    database_draft: str,
    frontend_pages: str,
    test_cases: str,
    development_tasks: str,
) -> str:
    """Step 6 (Design): Write the AI-generated design-ready files to specs/04-design-ready/."""
    return swm_write_design_tool(
        project_path,
        system_design_brief,
        api_draft,
        database_draft,
        frontend_pages,
        test_cases,
        development_tasks,
    )


# ── Step 7: Log ────────────────────────────────────────────────────────────────

@mcp.tool()
def swm_log_context(project_path: str) -> str:
    """Step 7 (Log): Return the assembled prompt, CONSTITUTION, all specs, and current version files for the calling AI to update the changelog and decision log. After processing, call swm_write_log with the results."""
    return swm_log_context_tool(project_path)


@mcp.tool()
def swm_write_log(project_path: str, changelog: str, decision_log: str) -> str:
    """Step 7 (Log): Write the updated changelog and decision log to specs/05-versions/."""
    return swm_write_log_tool(project_path, changelog, decision_log)


if __name__ == "__main__":
    mcp.run()
