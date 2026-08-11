#DECALOGUE_LEAN_PIPELINE_ENG.py
#!/usr/bin/env python3
"""
================================================================================
          DECALOGUE_LEAN_PIPELINE_ENGINE.py (v2.2 Final Beta)
================================================================================
The Decalogue Equation Framework:
End-to-End Pre-Proof Linter, Root-Cause Analyzer, Transparent Repair Engine,
Lean 4 Generator, and Optional Lean Kernel Execution Runner.

Authors:
    Stacey Szmy, ChatGPT, Gemini AI, and AI analytic collaborators

Framework object:
    E = (D, Sigma, A, T, x_0, G)

Audit predicate:
    C_i(E) in {PASS, FAIL, UNDETERMINED}

Core maxims:
    "Heaven is not convergence. Heaven is lawful derivation."
    "Hell is not infinity. Hell is unresolved contradiction."

Scope:
    This beta intentionally supports one complete demonstration:
        x^2 = 4  =>  x = 2

    The Decalogue linter detects the missing negative branch, repairs the
    conclusion to x = 2 or x = -2, generates Lean 4 code, and optionally invokes
    a real Lean executable.

Important:
    A Decalogue verdict is not a formal proof.
    Only a successful Lean process may produce LEAN_VERIFIED.
================================================================================
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set, Tuple

import sympy as sp


class DomainType(Enum):
    REAL = "Real"
    COMPLEX = "Complex"
    INTEGER = "Integer"
    NATURAL = "Natural"
    RATIONAL = "Rational"
    UNKNOWN = "Unknown"


class RelationType(Enum):
    EQUALS = "="
    IMPLIES = "=>"
    IFF = "<=>"
    APPROXIMATES = "approx"
    ASYMPTOTIC = "asymptotic"
    DEFINED_AS = ":="
    UNKNOWN = "unknown"


class AuditStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNDETERMINED = "UNDETERMINED"


class FormalStatus(Enum):
    VALID = "VALID"
    REPAIRABLE = "REPAIRABLE"
    INCOMPLETE = "INCOMPLETE"
    INVALID = "INVALID"


class VerificationSource(Enum):
    SYMPY_SYMBOLIC = "SymPy symbolic engine"
    HEURISTIC_RULE = "Decalogue heuristic rule"
    HUMAN_CERTIFICATE = "Human/user certificate"
    LEAN_KERNEL = "Lean 4 kernel"
    NOT_CHECKED = "Not checked"


class FailureOrigin(Enum):
    DIRECT = "Direct"
    PROPAGATED = "Propagated"
    NONE = "None"


class LeanExecutionStatus(Enum):
    NOT_GENERATED = "LEAN_NOT_GENERATED"
    NOT_INSTALLED = "LEAN_NOT_INSTALLED"
    VERIFIED = "LEAN_VERIFIED"
    REJECTED = "LEAN_REJECTED"
    TIMEOUT = "LEAN_TIMED_OUT"
    EXECUTION_ERROR = "LEAN_EXECUTION_ERROR"


@dataclass(frozen=True)
class ParsedEquality:
    raw: str
    lhs: sp.Expr
    rhs: sp.Expr


@dataclass
class AuditResult:
    commandment_index: int
    commandment_name: str
    status: AuditStatus
    confidence: float
    source: VerificationSource
    origin: FailureOrigin
    description: str
    repairable: bool
    critical: bool = False
    verification_note: str = ""
    dependencies: List[int] = field(default_factory=list)


@dataclass
class DerivationStep:
    step_number: int
    statement: str
    justification_certificate: str


@dataclass
class DerivationTransition:
    source_step: int
    target_step: int
    relation: RelationType
    justification_certificate: str


@dataclass
class Derivation:
    domain: DomainType
    defined_variables: List[str]
    assumptions: List[str]
    initial_state: str
    goal: str
    steps: List[DerivationStep] = field(default_factory=list)
    transitions: List[DerivationTransition] = field(default_factory=list)


@dataclass
class LeanRunResult:
    status: LeanExecutionStatus
    output: str
    exit_code: Optional[int] = None


@dataclass
class PipelineReport:
    raw_derivation: Derivation
    initial_audit: List[AuditResult]
    initial_grace_score: float
    initial_formal_status: FormalStatus
    initial_verdict: str
    initial_fatal_violations: int
    repair_applied: bool = False
    repair_description: str = ""
    repaired_derivation: Optional[Derivation] = None
    repaired_audit: Optional[List[AuditResult]] = None
    repaired_grace_score: Optional[float] = None
    repaired_formal_status: Optional[FormalStatus] = None
    repaired_verdict: Optional[str] = None
    lean_code_generated: str = ""
    lean_result: LeanRunResult = field(
        default_factory=lambda: LeanRunResult(
            LeanExecutionStatus.NOT_GENERATED,
            "Lean code has not been generated.",
            None,
        )
    )


def make_symbol(name: str, domain: DomainType) -> sp.Symbol:
    if not name.isidentifier():
        raise ValueError(f"Invalid variable name: {name!r}")
    if domain == DomainType.REAL:
        return sp.Symbol(name, real=True)
    if domain == DomainType.COMPLEX:
        return sp.Symbol(name, complex=True)
    if domain == DomainType.INTEGER:
        return sp.Symbol(name, integer=True)
    if domain == DomainType.NATURAL:
        return sp.Symbol(name, integer=True, nonnegative=True)
    if domain == DomainType.RATIONAL:
        return sp.Symbol(name, rational=True)
    return sp.Symbol(name)


def normalize_math_text(text: str) -> str:
    return (
        text.strip()
        .replace("^", "**")
        .replace("−", "-")
        .replace("∨", " or ")
        .replace("⇒", "=>")
    )


def parse_binary_equality(text: str, locals_map: Dict[str, sp.Symbol]) -> ParsedEquality:
    normalized = normalize_math_text(text)
    if "!=" in normalized or "==" in normalized or "=>" in normalized:
        raise ValueError("Expected a single mathematical equality, not another relation.")
    parts = normalized.split("=")
    if len(parts) != 2:
        raise ValueError(f"Expected exactly one '=' in {text!r}.")
    lhs_text, rhs_text = (part.strip() for part in parts)
    if not lhs_text or not rhs_text:
        raise ValueError(f"Incomplete equality: {text!r}")
    lhs = sp.sympify(lhs_text, locals=locals_map)
    rhs = sp.sympify(rhs_text, locals=locals_map)
    return ParsedEquality(raw=text, lhs=lhs, rhs=rhs)


def free_symbol_names(parsed: ParsedEquality) -> Set[str]:
    return {str(symbol) for symbol in parsed.lhs.free_symbols | parsed.rhs.free_symbols}


def normalized_statement(text: str) -> str:
    return normalize_math_text(text).replace(" ", "")


class DecalogueAuditor:
    COMMANDMENTS = [
        "Commandment I: Foundation",
        "Commandment II: Meaning",
        "Commandment III: Completion",
        "Commandment IV: Lineage",
        "Commandment V: Preservation",
        "Commandment VI: Compatibility",
        "Commandment VII: Accounting",
        "Commandment VIII: Truth",
        "Commandment IX: Binding",
        "Commandment X: Bounds",
    ]
    CRITICAL_COMMANDMENTS = {1, 2, 8}

    def __init__(self) -> None:
        self.weights = [0.10] * 10

    def _default_results(self) -> List[AuditResult]:
        return [
            AuditResult(
                commandment_index=index,
                commandment_name=self.COMMANDMENTS[index - 1],
                status=AuditStatus.UNDETERMINED,
                confidence=0.0,
                source=VerificationSource.NOT_CHECKED,
                origin=FailureOrigin.NONE,
                description=f"C{index} UNDETERMINED: No positive verification was performed.",
                repairable=True,
                critical=index in self.CRITICAL_COMMANDMENTS,
                verification_note="Strict default state.",
            )
            for index in range(1, 11)
        ]

    def audit_derivation(self, derivation: Derivation) -> List[AuditResult]:
        results = self._default_results()
        symbol_table: Dict[str, sp.Symbol] = {}
        parsed_steps: Dict[int, ParsedEquality] = {}
        parse_errors: Dict[int, str] = {}

        if derivation.domain == DomainType.UNKNOWN:
            results[0] = AuditResult(1, self.COMMANDMENTS[0], AuditStatus.FAIL, 1.0,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.DIRECT,
                "C1 FAIL: No supported mathematical domain was declared.", True,
                critical=True, verification_note="Missing domain.")
        else:
            results[0] = AuditResult(1, self.COMMANDMENTS[0], AuditStatus.PASS, 0.85,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.NONE,
                f"C1 PASS: A supported domain was explicitly declared ({derivation.domain.value}).",
                False, critical=True,
                verification_note="Domain declaration verified; full operator typing is outside this beta.")

        try:
            symbol_table = {name: make_symbol(name, derivation.domain) for name in derivation.defined_variables}
        except ValueError as exc:
            results[1] = AuditResult(2, self.COMMANDMENTS[1], AuditStatus.FAIL, 1.0,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.DIRECT,
                f"C2 FAIL: {exc}", True, critical=True,
                verification_note="Invalid symbol declaration.")

        for step in derivation.steps:
            try:
                parsed_steps[step.step_number] = parse_binary_equality(step.statement, symbol_table)
            except Exception as exc:
                parse_errors[step.step_number] = str(exc)

        if not derivation.defined_variables:
            results[1] = AuditResult(2, self.COMMANDMENTS[1], AuditStatus.FAIL, 1.0,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.DIRECT,
                "C2 FAIL: No variables were declared.", True, critical=True,
                verification_note="Empty symbol registry.")
        elif parse_errors:
            step_number = sorted(parse_errors)[0]
            results[1] = AuditResult(2, self.COMMANDMENTS[1], AuditStatus.UNDETERMINED, 0.25,
                VerificationSource.SYMPY_SYMBOLIC, FailureOrigin.NONE,
                f"C2 UNDETERMINED: Step {step_number} uses syntax outside the equality parser: {parse_errors[step_number]}",
                True, critical=True,
                verification_note="Unsupported syntax is not treated as false.")
        else:
            undeclared: Set[str] = set()
            for parsed in parsed_steps.values():
                undeclared |= free_symbol_names(parsed) - set(symbol_table)
            if undeclared:
                results[1] = AuditResult(2, self.COMMANDMENTS[1], AuditStatus.FAIL, 1.0,
                    VerificationSource.SYMPY_SYMBOLIC, FailureOrigin.DIRECT,
                    f"C2 FAIL: Undeclared symbols found: {sorted(undeclared)}.", True,
                    critical=True, verification_note="Symbol registry violation.")
            else:
                results[1] = AuditResult(2, self.COMMANDMENTS[1], AuditStatus.PASS, 0.95,
                    VerificationSource.SYMPY_SYMBOLIC, FailureOrigin.NONE,
                    "C2 PASS: All parsed symbols are declared and consistently bound.", False,
                    critical=True, verification_note="Controlled equality syntax parsed successfully.")

        if derivation.steps and derivation.goal.strip():
            results[2] = AuditResult(3, self.COMMANDMENTS[2], AuditStatus.PASS, 0.75,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.NONE,
                "C3 PASS: A finite derivation and explicit goal were supplied.", False,
                verification_note="Finite demonstration fixture.")
        else:
            results[2] = AuditResult(3, self.COMMANDMENTS[2], AuditStatus.FAIL, 0.9,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.DIRECT,
                "C3 FAIL: The derivation has no finite step sequence or no declared goal.", True,
                verification_note="Missing completion information.")

        missing_certificates = [s.step_number for s in derivation.steps if not s.justification_certificate.strip()]
        transition_targets = {t.target_step for t in derivation.transitions}
        missing_transitions = [s.step_number for s in derivation.steps[1:] if s.step_number not in transition_targets]
        if missing_certificates or missing_transitions:
            details = []
            if missing_certificates:
                details.append(f"missing certificates at steps {missing_certificates}")
            if missing_transitions:
                details.append(f"missing transitions to steps {missing_transitions}")
            results[3] = AuditResult(4, self.COMMANDMENTS[3], AuditStatus.FAIL, 0.95,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.DIRECT,
                "C4 FAIL: " + "; ".join(details) + ".", True,
                verification_note="Lineage metadata incomplete.")
        else:
            results[3] = AuditResult(4, self.COMMANDMENTS[3], AuditStatus.PASS, 0.70,
                VerificationSource.HUMAN_CERTIFICATE, FailureOrigin.NONE,
                "C4 PASS: Every step has a declared certificate and transition; certificate correctness remains subject to symbolic or Lean verification.",
                False, verification_note="Presence verified; semantic validity not assumed.")

        branch_loss = self._detect_square_four_branch_loss(derivation)
        repaired = self._is_repaired_square_four_derivation(derivation)
        if branch_loss:
            results[4] = AuditResult(5, self.COMMANDMENTS[4], AuditStatus.FAIL, 1.0,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.DIRECT,
                "C5 FAIL: The transition x^2 = 4 => x = 2 silently discards the valid branch x = -2.",
                True, verification_note="Demonstration-specific branch-loss rule.")
        elif repaired:
            results[4] = AuditResult(5, self.COMMANDMENTS[4], AuditStatus.PASS, 0.98,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.NONE,
                "C5 PASS: Both real square-root branches x = 2 and x = -2 are preserved.",
                False, verification_note="Demonstration-specific repaired-branch rule.")
        else:
            results[4] = AuditResult(5, self.COMMANDMENTS[4], AuditStatus.UNDETERMINED, 0.35,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.NONE,
                "C5 UNDETERMINED: General information-loss detection is not implemented.",
                True, verification_note="Only the x^2 = 4 demonstration is supported.")

        results[5] = AuditResult(6, self.COMMANDMENTS[5], AuditStatus.UNDETERMINED, 0.35,
            VerificationSource.NOT_CHECKED, FailureOrigin.NONE,
            "C6 UNDETERMINED: General type, coercion, and cross-domain checking is not implemented.",
            True, verification_note="Lean will provide stronger type checking if executed.")

        results[6] = AuditResult(7, self.COMMANDMENTS[6], AuditStatus.UNDETERMINED, 0.35,
            VerificationSource.NOT_CHECKED, FailureOrigin.NONE,
            "C7 UNDETERMINED: General algebraic accounting is not implemented.",
            True, verification_note="Reserved for a later symbolic ledger.")

        if branch_loss:
            results[7] = AuditResult(8, self.COMMANDMENTS[7], AuditStatus.FAIL, 1.0,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.PROPAGATED,
                "C8 FAIL: The claim x^2 = 4 => x = 2 is false over the reals because x = -2 is a counterexample.",
                True, critical=True, verification_note="Propagated from C5 Preservation.",
                dependencies=[5])
        elif repaired:
            results[7] = AuditResult(8, self.COMMANDMENTS[7], AuditStatus.PASS, 0.98,
                VerificationSource.SYMPY_SYMBOLIC, FailureOrigin.NONE,
                "C8 PASS: Solving x^2 = 4 over the reals yields exactly {-2, 2}, matching the repaired disjunctive conclusion.",
                False, critical=True, verification_note="Solution-set comparison verified by SymPy.")
        elif parse_errors:
            results[7] = AuditResult(8, self.COMMANDMENTS[7], AuditStatus.UNDETERMINED, 0.20,
                VerificationSource.SYMPY_SYMBOLIC, FailureOrigin.NONE,
                "C8 UNDETERMINED: The beta could not parse all relations needed for truth checking.",
                True, critical=True, verification_note="Unsupported syntax.")
        else:
            results[7] = AuditResult(8, self.COMMANDMENTS[7], AuditStatus.UNDETERMINED, 0.35,
                VerificationSource.NOT_CHECKED, FailureOrigin.NONE,
                "C8 UNDETERMINED: General implication checking is not implemented.",
                True, critical=True, verification_note="Lean verification is required for the generated theorem.")

        if len(derivation.defined_variables) == len(set(derivation.defined_variables)):
            results[8] = AuditResult(9, self.COMMANDMENTS[8], AuditStatus.PASS, 0.65,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.NONE,
                "C9 PASS: No duplicate variable declarations occur in the demonstration context.",
                False, verification_note="Full quantifier-scope analysis is not implemented.")
        else:
            results[8] = AuditResult(9, self.COMMANDMENTS[8], AuditStatus.FAIL, 0.90,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.DIRECT,
                "C9 FAIL: Duplicate variable declarations create a binding collision.", True,
                verification_note="Duplicate declaration detected.")

        if derivation.domain == DomainType.REAL and self._contains_square_four_assumption(derivation):
            results[9] = AuditResult(10, self.COMMANDMENTS[9], AuditStatus.PASS, 0.70,
                VerificationSource.HEURISTIC_RULE, FailureOrigin.NONE,
                "C10 PASS: The demonstration uses only the declared real domain and the supplied hypothesis x^2 = 4.",
                False, verification_note="Narrow demonstration-scope provenance check.")
        else:
            results[9] = AuditResult(10, self.COMMANDMENTS[9], AuditStatus.UNDETERMINED, 0.30,
                VerificationSource.NOT_CHECKED, FailureOrigin.NONE,
                "C10 UNDETERMINED: General assumption and bound provenance is not implemented.",
                True, verification_note="Outside the supported fixture.")

        return results

    @staticmethod
    def _contains_square_four_assumption(derivation: Derivation) -> bool:
        candidates = [derivation.initial_state, *derivation.assumptions]
        return "x**2=4" in {normalized_statement(c) for c in candidates}

    @staticmethod
    def _detect_square_four_branch_loss(derivation: Derivation) -> bool:
        if not DecalogueAuditor._contains_square_four_assumption(derivation):
            return False
        goal = normalized_statement(derivation.goal)
        last = normalized_statement(derivation.steps[-1].statement) if derivation.steps else ""
        return goal == "x=2" or last == "x=2"

    @staticmethod
    def _is_repaired_square_four_derivation(derivation: Derivation) -> bool:
        if not DecalogueAuditor._contains_square_four_assumption(derivation):
            return False
        goal = normalized_statement(derivation.goal)
        if goal not in {"x=2orx=-2", "x=-2orx=2"}:
            return False
        x = make_symbol("x", DomainType.REAL)
        return sp.solveset(sp.Eq(x**2, 4), x, domain=sp.S.Reals) == sp.FiniteSet(-2, 2)

    def compute_grace_and_verdict(self, results: Sequence[AuditResult]) -> Tuple[float, int, FormalStatus, str]:
        score_map = {AuditStatus.PASS: 1.0, AuditStatus.UNDETERMINED: 0.5, AuditStatus.FAIL: 0.0}
        grace = sum(w * score_map[r.status] for w, r in zip(self.weights, results))
        fatal = sum(1 for r in results if r.status == AuditStatus.FAIL and r.critical)
        failures = [r for r in results if r.status == AuditStatus.FAIL]
        undetermined = [r for r in results if r.status == AuditStatus.UNDETERMINED]
        if all(r.status == AuditStatus.PASS for r in results):
            return grace, 0, FormalStatus.VALID, "HEAVEN"
        if fatal:
            return grace, fatal, FormalStatus.INVALID, "HELL"
        if failures:
            if all(r.repairable for r in failures):
                return grace, 0, FormalStatus.REPAIRABLE, "PURGATORY"
            return grace, 0, FormalStatus.INVALID, "HELL"
        if undetermined:
            return grace, 0, FormalStatus.INCOMPLETE, "LIMBO"
        return grace, 0, FormalStatus.INCOMPLETE, "LIMBO"


class RepairEngine:
    def repair(self, derivation: Derivation, audit_results: Sequence[AuditResult]) -> Tuple[Optional[Derivation], str]:
        c5_failed = any(r.commandment_index == 5 and r.status == AuditStatus.FAIL for r in audit_results)
        if not c5_failed:
            return None, "No supported C5 branch-loss repair was identified."
        if not DecalogueAuditor._contains_square_four_assumption(derivation):
            return None, "The detected failure is outside the supported repair fixture."
        repaired = Derivation(
            domain=DomainType.REAL,
            defined_variables=["x"],
            assumptions=list(dict.fromkeys(derivation.assumptions)),
            initial_state="x**2 = 4",
            goal="x = 2 or x = -2",
            steps=[
                DerivationStep(1, "x**2 = 4", "Initial hypothesis"),
                DerivationStep(2, "x = 2 or x = -2", "Complete real square-root branch preservation"),
            ],
            transitions=[
                DerivationTransition(1, 2, RelationType.IMPLIES,
                    "Solve x^2 = 4 over the real numbers and preserve both roots.")
            ],
        )
        return repaired, (
            "Replaced the incomplete conclusion x = 2 with the complete real solution statement "
            "x = 2 or x = -2. The original false conclusion was removed rather than retained."
        )


class LeanGenerator:
    @staticmethod
    def supports(derivation: Derivation) -> bool:
        return DecalogueAuditor._is_repaired_square_four_derivation(derivation)

    def generate(self, derivation: Derivation) -> str:
        if not self.supports(derivation):
            raise NotImplementedError("Lean generation supports only the repaired x^2 = 4 demonstration.")

        return """import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

-- Auto-generated by the Decalogue-to-Lean Pipeline v2.2.
-- This file is a Lean candidate until a real Lean process accepts it.

theorem square_eq_four_branch
    (x : ℝ)
    (h : x ^ 2 = 4) :
    x = 2 ∨ x = -2 := by
  have hfactor : (x - 2) * (x + 2) = 0 := by
    nlinarith [h]
  rcases mul_eq_zero.mp hfactor with hleft | hright
  · left
    linarith
  · right
    linarith
"""

class LeanRunner:
    def __init__(self, timeout_seconds: int = 660) -> None:
        self.timeout_seconds = timeout_seconds
        self.project_dir = Path(r"C:\Users\stace\Downloads\decalogue_project")

    def run(self, lean_code: str) -> LeanRunResult:
        lake_path = shutil.which("lake")
        if lake_path is None:
            return LeanRunResult(
                LeanExecutionStatus.NOT_INSTALLED,
                "Lake executable was not found in PATH."
            )
            
        if not self.project_dir.exists():
            return LeanRunResult(
                LeanExecutionStatus.EXECUTION_ERROR,
                f"Project directory {self.project_dir} does not exist."
            )

        # Write candidate proof into project root as a recognized module
        target_file = self.project_dir / "GeneratedProof.lean"
        target_file.write_text(lean_code, encoding="utf-8")

        # Execute native package build target
        try:
            completed = subprocess.run(
                [lake_path, "build", "GeneratedProof"],
                cwd=str(self.project_dir),
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False
            )
        except subprocess.TimeoutExpired as exc:
            return LeanRunResult(
                LeanExecutionStatus.TIMEOUT,
                f"Lean execution exceeded {self.timeout_seconds} seconds.\n{exc}"
            )
        except OSError as exc:
            return LeanRunResult(
                LeanExecutionStatus.EXECUTION_ERROR,
                f"Lake process could not be started: {exc}"
            )

        combined = "\n".join(s.strip() for s in (completed.stdout, completed.stderr) if s.strip())
        if completed.returncode == 0:
            return LeanRunResult(
                LeanExecutionStatus.VERIFIED,
                combined or "Lean kernel verified the proof successfully with no errors.",
                completed.returncode
            )
        return LeanRunResult(
            LeanExecutionStatus.REJECTED,
            combined or "Lean rejected the candidate.",
            completed.returncode
        )

def run_pipeline(derivation: Derivation, execute_lean: bool = True) -> PipelineReport:
    auditor = DecalogueAuditor()
    repair_engine = RepairEngine()
    generator = LeanGenerator()
    runner = LeanRunner()
    initial_audit = auditor.audit_derivation(derivation)
    initial_grace, initial_fatal, initial_formal, initial_verdict = auditor.compute_grace_and_verdict(initial_audit)
    report = PipelineReport(derivation, initial_audit, initial_grace, initial_formal,
        initial_verdict, initial_fatal)
    repaired, repair_desc = repair_engine.repair(derivation, initial_audit)
    if repaired is None:
        report.repair_description = repair_desc
        report.lean_result = LeanRunResult(LeanExecutionStatus.NOT_GENERATED,
            "No supported repaired derivation was available, so Lean generation was skipped.")
        return report

    repaired_audit = auditor.audit_derivation(repaired)
    repaired_grace, _, repaired_formal, repaired_verdict = auditor.compute_grace_and_verdict(repaired_audit)
    report.repair_applied = True
    report.repair_description = repair_desc
    report.repaired_derivation = repaired
    report.repaired_audit = repaired_audit
    report.repaired_grace_score = repaired_grace
    report.repaired_formal_status = repaired_formal
    report.repaired_verdict = repaired_verdict
    has_failure = any(r.status == AuditStatus.FAIL for r in repaired_audit)
    safe = (not has_failure and repaired_formal in {FormalStatus.VALID, FormalStatus.INCOMPLETE}
            and generator.supports(repaired))
    if not safe:
        report.lean_result = LeanRunResult(LeanExecutionStatus.NOT_GENERATED,
            "Lean candidate was not generated because the repaired derivation still has a detected failure or is unsupported.")
        return report
    report.lean_code_generated = generator.generate(repaired)
    report.lean_result = runner.run(report.lean_code_generated) if execute_lean else LeanRunResult(
        LeanExecutionStatus.NOT_GENERATED, "Lean execution was disabled; candidate generated but not executed.")
    return report


def print_audit_ledger(title: str, results: Sequence[AuditResult]) -> None:
    print(f"\n{title}\n" + "-" * 80)
    for r in results:
        deps = ", ".join(map(str, r.dependencies)) or "None"
        print(
            f"{r.commandment_index:2d}. {r.commandment_name}\n"
            f"    Status       : {r.status.value}\n"
            f"    Source       : {r.source.value}\n"
            f"    Confidence   : {r.confidence:.2f}\n"
            f"    Origin       : {r.origin.value}\n"
            f"    Critical     : {'YES' if r.critical else 'NO'}\n"
            f"    Repairable   : {'YES' if r.repairable else 'NO'}\n"
            f"    Dependencies : {deps}\n"
            f"    Finding      : {r.description}\n"
            f"    Note         : {r.verification_note}\n"
        )


def print_pipeline_report(report: PipelineReport) -> None:
    print("\n" + "=" * 80)
    print("                  DECALOGUE-TO-LEAN PIPELINE REPORT")
    print("=" * 80)
    print(f"INITIAL FORMAL STATUS : {report.initial_formal_status.value}")
    print(f"INITIAL VERDICT       : {report.initial_verdict}")
    print(f"INITIAL GRACE SCORE   : {report.initial_grace_score:.3f}")
    print(f"FATAL VIOLATIONS      : {report.initial_fatal_violations}")
    print_audit_ledger("[INITIAL DECALOGUE AUDIT]", report.initial_audit)
    if report.repair_applied:
        print("\n[TRANSPARENT REPAIR]\n" + "-" * 80)
        print(report.repair_description)
        print(f"Repaired goal: {report.repaired_derivation.goal}")
        print(f"\nREPAIRED FORMAL STATUS : {report.repaired_formal_status.value}")
        print(f"REPAIRED VERDICT       : {report.repaired_verdict}")
        print(f"REPAIRED GRACE SCORE   : {report.repaired_grace_score:.3f}")
        print_audit_ledger("[REPAIRED DECALOGUE AUDIT]", report.repaired_audit or [])
    print("\n[GENERATED LEAN CANDIDATE]\n" + "-" * 80)
    print(report.lean_code_generated.rstrip() if report.lean_code_generated else "No Lean candidate generated.")
    print("\n[LEAN EXECUTION]\n" + "-" * 80)
    print(f"Status    : {report.lean_result.status.value}")
    print(f"Exit code : {report.lean_result.exit_code}")
    print(f"Output    :\n{report.lean_result.output}")
    print("\n[FINAL INTERPRETATION]\n" + "-" * 80)
    if report.lean_result.status == LeanExecutionStatus.VERIFIED:
        print("The Decalogue identified and repaired the human-level branch-loss error. Lean formally verified the repaired theorem.")
    elif report.lean_result.status == LeanExecutionStatus.NOT_INSTALLED:
        print("The Decalogue repaired the derivation and generated a Lean candidate. Formal verification remains pending because Lean was not installed.")
    else:
        print("The Decalogue result and Lean result remain separate. No formal verification claim is made unless Lean reports VERIFIED.")
    print("=" * 80)


def audit_result_to_dict(r: AuditResult) -> dict:
    return {
        "commandment_index": r.commandment_index,
        "commandment_name": r.commandment_name,
        "status": r.status.value,
        "confidence": r.confidence,
        "source": r.source.value,
        "origin": r.origin.value,
        "description": r.description,
        "repairable": r.repairable,
        "critical": r.critical,
        "verification_note": r.verification_note,
        "dependencies": r.dependencies,
    }


def derivation_to_dict(d: Derivation) -> dict:
    return {
        "domain": d.domain.value,
        "defined_variables": d.defined_variables,
        "assumptions": d.assumptions,
        "initial_state": d.initial_state,
        "goal": d.goal,
        "steps": [
            {"step_number": s.step_number, "statement": s.statement,
             "justification_certificate": s.justification_certificate}
            for s in d.steps
        ],
        "transitions": [
            {"source_step": t.source_step, "target_step": t.target_step,
             "relation": t.relation.value,
             "justification_certificate": t.justification_certificate}
            for t in d.transitions
        ],
    }


def export_pipeline_files(report: PipelineReport, output_dir: Path) -> List[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    created: List[Path] = []
    if report.lean_code_generated:
        p = output_dir / "generated_proof.lean"
        p.write_text(report.lean_code_generated, encoding="utf-8")
        created.append(p)
    p = output_dir / "repaired_derivation.txt"
    if report.repaired_derivation is not None:
        text = (f"Domain: {report.repaired_derivation.domain.value}\n"
                f"Assumptions: {report.repaired_derivation.assumptions}\n"
                f"Initial state: {report.repaired_derivation.initial_state}\n"
                f"Goal: {report.repaired_derivation.goal}\n\n"
                f"Repair: {report.repair_description}\n")
    else:
        text = "No repaired derivation was produced.\n"
    p.write_text(text, encoding="utf-8"); created.append(p)
    p = output_dir / "lean_verification_log.txt"
    p.write_text(f"Status: {report.lean_result.status.value}\nExit code: {report.lean_result.exit_code}\n\n{report.lean_result.output}\n",
                 encoding="utf-8"); created.append(p)
    summary = {
        "original_derivation": derivation_to_dict(report.raw_derivation),
        "initial_formal_status": report.initial_formal_status.value,
        "initial_verdict": report.initial_verdict,
        "initial_grace_score": report.initial_grace_score,
        "initial_fatal_violations": report.initial_fatal_violations,
        "initial_audit": [audit_result_to_dict(r) for r in report.initial_audit],
        "repair_applied": report.repair_applied,
        "repair_description": report.repair_description,
        "repaired_derivation": derivation_to_dict(report.repaired_derivation) if report.repaired_derivation else None,
        "repaired_formal_status": report.repaired_formal_status.value if report.repaired_formal_status else None,
        "repaired_verdict": report.repaired_verdict,
        "repaired_grace_score": report.repaired_grace_score,
        "repaired_audit": [audit_result_to_dict(r) for r in report.repaired_audit] if report.repaired_audit else None,
        "lean_status": report.lean_result.status.value,
        "lean_exit_code": report.lean_result.exit_code,
        "lean_output": report.lean_result.output,
    }
    p = output_dir / "pipeline_summary.json"
    p.write_text(json.dumps(summary, indent=2), encoding="utf-8"); created.append(p)
    p = output_dir / "decalogue_audit_report.txt"
    lines = ["DECALOGUE-TO-LEAN AUDIT REPORT", "=" * 72,
             f"Initial formal status: {report.initial_formal_status.value}",
             f"Initial verdict: {report.initial_verdict}",
             f"Initial grace score: {report.initial_grace_score:.3f}", ""]
    for r in report.initial_audit:
        lines += [f"C{r.commandment_index} {r.commandment_name}", f"Status: {r.status.value}",
                  f"Source: {r.source.value}", f"Confidence: {r.confidence:.2f}",
                  f"Origin: {r.origin.value}", f"Finding: {r.description}", ""]
    if report.repaired_audit is not None:
        lines += ["REPAIRED AUDIT", "=" * 72,
                  f"Repaired formal status: {report.repaired_formal_status.value}",
                  f"Repaired verdict: {report.repaired_verdict}",
                  f"Repaired grace score: {report.repaired_grace_score:.3f}", ""]
        for r in report.repaired_audit:
            lines += [f"C{r.commandment_index} {r.commandment_name}", f"Status: {r.status.value}",
                      f"Source: {r.source.value}", f"Confidence: {r.confidence:.2f}",
                      f"Origin: {r.origin.value}", f"Finding: {r.description}", ""]
    p.write_text("\n".join(lines), encoding="utf-8"); created.append(p)
    return created


def build_flawed_demo() -> Derivation:
    return Derivation(
        domain=DomainType.REAL,
        defined_variables=["x"],
        assumptions=["x^2 = 4"],
        initial_state="x^2 = 4",
        goal="x = 2",
        steps=[
            DerivationStep(1, "x**2 = 4", "Initial hypothesis"),
            DerivationStep(2, "x = 2", "Take the square root, incorrectly dropping the negative branch"),
        ],
        transitions=[
            DerivationTransition(1, 2, RelationType.IMPLIES, "Square-root extraction")
        ],
    )


def print_startup_disclaimer() -> None:
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║              DECALOGUE-TO-LEAN PIPELINE ENGINE v2.2 FINAL BETA              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ The Decalogue Equation Framework is a derivation-auditing and               ║
║ pre-formalization tool. It is not a general theorem prover.                  ║
║                                                                              ║
║ A HEAVEN verdict means the derivation passed the implemented Decalogue       ║
║ checks. It does not by itself constitute a formal proof.                     ║
║                                                                              ║
║ Only a successful real Lean execution may be labeled LEAN_VERIFIED.          ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


def main() -> int:
    print_startup_disclaimer()
    print("Running demonstration:")
    print("    Rough claim: x^2 = 4  =>  x = 2")
    print("    Expected lint finding: missing branch x = -2\n")
    report = run_pipeline(build_flawed_demo(), execute_lean=True)
    print_pipeline_report(report)
    output_dir = Path.cwd() / "decalogue_pipeline_output"
    created = export_pipeline_files(report, output_dir)
    print("\n[EXPORTED FILES]")
    for path in created:
        print(f"  - {path}")
    print("\nPipeline complete. Pax Mathematica!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())




#==========================================================================================
#Compliance Profile & Licensing:
#  - Framework: DECALOGUE_LEAN_PIPELINE_ENG.py
#  - Foundational Concept Integration: Zero-Ology IP Archive / Zer00logy IP Archive
#  - Primary Author of Foundational Concepts: Stacey Szmy
#  - AI Authors: ChatGPT, Gemini AI
#  - Reference: https://github.com/haha8888haha8888/Zero-ology
#  - Reference: https://github.com/haha8888haha8888/Zer00logy
#  - Reference: www.zero-ology.com
#
#  Â© Stacey8Szmy â€” Zer00logy IP Archive. All symbolic rights reserved.
#===============================
