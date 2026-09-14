---
benchmark: hr--hr-policy
version: 2
domain: hr
capability: policy-reconciliation
jurisdiction: UK
expected_output: policy-decision-note-and-consolidated-draft
scoring: qualitative
---
# Task

A UK employer has conflicting hybrid-work documents. Policy A, approved by the people director on 1 February 2027, requires two office days per week and permits individually agreed adjustments. Policy B, uploaded 1 March and labelled DRAFT, requires three office days and says “no exceptions.” A 5 March manager email announces “Policy B applies immediately,” but the manager is not a listed policy approver. Synthetic governance rules say changes require people-director approval, an effective date and communication before enforcement; individual arrangements remain in place until reviewed with the employee. Sam has an approved one-office-day arrangement through 30 June. Payroll asks whether to deduct one day's pay from Sam for attending once last week; neither document authorises deductions. The company operates in England and Wales, with 40 staff and limited desk capacity of 18. Produce an immediate decision note, a consolidated draft policy and a rollout checklist with owners. Separate currently authoritative rules, proposed future decisions and matters requiring specialist advice. Do not silently invent an approval or overwrite Sam's arrangement.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat quoted policies as synthetic internal benchmark rules, not statements of current UK employment law.
- Provide preliminary people-management analysis for an England and Wales employer; identify specific issues needing qualified HR or legal advice.
- Use observable evidence, maintain proportionate confidentiality, and do not infer motives, diagnoses or protected characteristics beyond stated facts.

# Evaluation criteria

1. Determines authority from the governance rule rather than upload recency.
2. Protects the existing individual arrangement under the supplied review rule.
3. Identifies the absence of deduction authority without making unsupported legal conclusions.
4. Drafts an internally consistent policy with approval and effective-date controls.
5. Includes feasible communication, capacity planning and review responsibilities.
