from dtx.core import logging
from typing import Optional

from dtx_models.results import EvalReport
from dtx_models.repo.plugin2frameworks import Plugin2FrameworkMapper


from enum import Enum
from typing import Dict, List
from uuid import UUID
from collections import defaultdict

from pydantic import BaseModel, Field
from dtx_models.results import EvalResult


# Initialize module-level logger
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Enums
# ----------------------------------------------------------------------

class AIRiskSeverity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"

class AIEvalStatus(str, Enum):
    passed = "pass"
    failed = "fail"

# ----------------------------------------------------------------------
# Risk Check and Category Section
# ----------------------------------------------------------------------

class AIRiskCheck(BaseModel):
    id: str
    name: str
    status: AIEvalStatus
    severity: Optional[AIRiskSeverity] = None
    description: Optional[str] = None

class AIRiskCategorySection(BaseModel):
    id: str
    name: str
    title: str
    description: Optional[str] = None
    percent: int = Field(..., ge=0, le=100)
    passed: int
    failed: int
    total: int
    risks: List[AIRiskCheck]

# ----------------------------------------------------------------------
# Framework Breakdown
# ----------------------------------------------------------------------

class AIRiskFramework(BaseModel):
    id: str
    name: str
    title: str
    description: Optional[str] = None
    score: int = Field(..., ge=0, le=100)
    passed: int
    failed: int
    total: int
    controls: List[Dict] = []  # no detailed controls in EvalReport context

# ----------------------------------------------------------------------
# Summary / Stats Models
# ----------------------------------------------------------------------

class AIRiskOverallSeverityCounts(BaseModel):
    total: int
    passed: int
    failed: int
    critical: int
    high: int
    medium: int
    low: int
    jailbreaks: int

class AIRiskFrameworkOverview(BaseModel):
    id: str
    name: str
    title: str
    score: int = Field(..., ge=0, le=100)
    passed: int
    failed: int
    total: int

class AIRiskSectionStats(BaseModel):
    id: str
    name: str
    title: str
    description: Optional[str] = None
    score: int = Field(..., ge=0, le=100)
    passed: int
    failed: int
    total: int

class AIRiskOverallStats(BaseModel):
    overall: Dict[str, int]
    severity: AIRiskOverallSeverityCounts
    frameworks: List[AIRiskFrameworkOverview]
    sections: List[AIRiskSectionStats]

# ----------------------------------------------------------------------
# Per-Provider Risk Breakdown (stubbed)
# ----------------------------------------------------------------------

class AIRiskProviderReport(BaseModel):
    provider_id: Optional[UUID]
    provider_name: Optional[str]
    provider_type: Optional[str]
    risk_sections: List[AIRiskCategorySection] = []

class AIRiskAssessmentReport(BaseModel):
    overall_stats: AIRiskOverallStats
    frameworks: List[AIRiskFramework]
    risk_sections: List[AIRiskCategorySection]
    providers: List[AIRiskProviderReport]

# ----------------------------------------------------------------------
# Builder using EvalReport directly
# ----------------------------------------------------------------------

def _to_severity_enum(value: str) -> Optional[AIRiskSeverity]:
    val = value.lower()
    if 'critical' in val:
        return AIRiskSeverity.critical
    if 'high' in val:
        return AIRiskSeverity.high
    if 'medium' in val:
        return AIRiskSeverity.medium
    return AIRiskSeverity.low


def _humanize_slug(slug: str) -> str:
    if not slug:
        return ''
    return slug.replace('_', ' ').replace('-', ' ').title()


class AssessmentReportBuilder:
    def __init__(self, eval_report: EvalReport, plugin2framework_mapper: Plugin2FrameworkMapper):
        self.report = eval_report
        self.results: List[EvalResult] = eval_report.eval_results
        self.plugin2framework_mapper = plugin2framework_mapper


    def build(self) -> AIRiskAssessmentReport:
        overall = self._compute_overall_stats()
        frameworks = self._build_frameworks()
        sections = self._build_sections()
        providers = []  

        # populate overview lists
        overall.frameworks = [self._to_framework_overview(fw) for fw in frameworks]
        overall.sections = [self._to_section_stats(sec) for sec in sections]

        return AIRiskAssessmentReport(
            overall_stats=overall,
            frameworks=frameworks,
            risk_sections=sections,
            providers=providers,
        )

    def _compute_overall_stats(self) -> AIRiskOverallStats:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.responses and r.responses[0].success)
        failed = total - passed
        jailbreaks = sum(1 for r in self.results if r.responses and r.responses[0].jailbreak_achieved)

        buckets = dict(critical=0, high=0, medium=0, low=0)
        for r in self.results:
            sev = r.risk_score.overall.overall_score.severity.value.lower()
            if 'critical' in sev:
                buckets['critical'] += 1
            elif 'high' in sev:
                buckets['high'] += 1
            elif 'medium' in sev:
                buckets['medium'] += 1
            else:
                buckets['low'] += 1

        return AIRiskOverallStats(
            overall=dict(total=total, passed=passed, failed=failed),
            severity=AIRiskOverallSeverityCounts(
                total=total,
                passed=passed,
                failed=failed,
                critical=buckets['critical'],
                high=buckets['high'],
                medium=buckets['medium'],
                low=buckets['low'],
                jailbreaks=jailbreaks,
            ),
            frameworks=[],
            sections=[],
        )

    def _build_frameworks(self) -> List[AIRiskFramework]:
        framework_data = defaultdict(lambda: {
            "passed": 0,
            "failed": 0,
            "total": 0,
            "framework_title": None,
            "framework_description": None,
        })

        for r in self.results:
            plugin_id = r.plugin_id
            if not plugin_id:
                continue

            plugin_dto = self.plugin2framework_mapper.get_plugin_with_frameworks(plugin_id)
            if not plugin_dto:
                continue

            is_pass = r.responses and r.responses[0].success

            for ctrl in plugin_dto.compliance_controls:
                f_id = ctrl.framework_id
                framework_data[f_id]["total"] += 1
                if is_pass:
                    framework_data[f_id]["passed"] += 1
                else:
                    framework_data[f_id]["failed"] += 1

                # Save title/description if not already
                if not framework_data[f_id]["framework_title"]:
                    framework_data[f_id]["framework_title"] = ctrl.framework_title
                if not framework_data[f_id]["framework_description"]:
                    framework_data[f_id]["framework_description"] = ctrl.framework_description

        frameworks = []
        for fid, data in framework_data.items():
            total = data["total"]
            passed = data["passed"]
            failed = data["failed"]
            score = int((passed / total) * 100) if total else 0
            frameworks.append(
                AIRiskFramework(
                    id=fid,
                    name=_humanize_slug(fid),
                    title=data["framework_title"] or fid,
                    description=data["framework_description"],
                    score=score,
                    passed=passed,
                    failed=failed,
                    total=total,
                    controls=[],  # Optionally include control list
                )
            )

        return frameworks

    def _build_sections(self) -> List[AIRiskCategorySection]:
        # Group by plugin_id category
        tree: Dict[str, List[EvalResult]] = defaultdict(list)
        for r in self.results:
            cat = r.plugin_id.split(':')[0] if r.plugin_id else 'Unknown'
            tree[cat].append(r)

        sections: List[AIRiskCategorySection] = []
        for cat, items in tree.items():
            passed = sum(1 for r in items if r.responses and r.responses[0].success)
            failed = len(items) - passed
            total = len(items)
            percent = int((passed / total) * 100) if total else 0

            checks: List[AIRiskCheck] = []
            for r in items:
                sev_value = r.risk_score.overall.overall_score.severity.value
                checks.append(
                    AIRiskCheck(
                        id=r.run_id,
                        name=_humanize_slug(r.plugin_id),
                        status=AIEvalStatus.passed if r.responses[0].success else AIEvalStatus.failed,
                        severity=_to_severity_enum(sev_value),
                    )
                )

            sections.append(
                AIRiskCategorySection(
                    id=cat,
                    name=_humanize_slug(cat),
                    title=_humanize_slug(cat),
                    percent=percent,
                    passed=passed,
                    failed=failed,
                    total=total,
                    risks=checks,
                )
            )
        return sections

    def _to_framework_overview(self, fw: AIRiskFramework) -> AIRiskFrameworkOverview:
        return AIRiskFrameworkOverview(
            id=fw.id,
            name=fw.name,
            title=fw.title,
            score=fw.score,
            passed=fw.passed,
            failed=fw.failed,
            total=fw.total,
        )

    def _to_section_stats(self, sec: AIRiskCategorySection) -> AIRiskSectionStats:
        return AIRiskSectionStats(
            id=sec.id,
            name=sec.name,
            title=sec.title,
            description=sec.description,
            score=sec.percent,
            passed=sec.passed,
            failed=sec.failed,
            total=sec.total,
        )


