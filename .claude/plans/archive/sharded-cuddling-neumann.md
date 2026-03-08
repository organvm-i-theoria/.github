# Organization Template Perfection Roadmap

## Objective
Transform this repository into a fully generic, reusable organization template applicable to any GitHub org.

---

## Current State

| Component | Count | Issues |
|-----------|-------|--------|
| Workflows | 129 | 17 PR workflows (consolidate), 40 missing concurrency |
| AI Agents | 32 | Triple-duplicate frontmatter |
| ChatModes | 90 | Broken YAML frontmatter |
| Python Scripts | 52 | 17 untested, uneven coverage |
| Documentation | 298 | Disorganized, branded |
| Branded References | 254 files | Org-specific names, URLs |

---

## Phase 0: Branding Removal & Template Variables (Week 1)

### 0.1 Create Template Variable System

**Create:** `.github/template-config.yml`
```yaml
# Template configuration - replace these values for your org
org:
  name: "{{ORG_NAME}}"
  display_name: "{{ORG_DISPLAY_NAME}}"
  github_url: "https://github.com/{{ORG_NAME}}"

product:
  name: "{{PRODUCT_NAME}}"
  api_endpoint: "{{API_ENDPOINT}}"

defaults:
  python_version: "3.12"
  node_version: "20"
```

### 0.2 Remove Organization Branding

**Files with `ivviiviivvi` references (254 files):**

**Root Documentation:**
- `README.md` → Generic "Organization Hub" title
- `GEMINI.md` → Generic title
- `CLAUDE.md` → Generic references

**Schema.org Metadata (4 files):**
- `.config/schema-org/organization.jsonld`
- `.config/schema-org/repository.jsonld`
- `.config/schema-org/ai-framework.jsonld`
- `.config/schema-org/documentation.jsonld`

**GitHub Configuration:**
- `.github/copilot-instructions.md`
- `.github/ISSUE_TEMPLATE/*.yml` (all templates)
- `.github/scheduled-walkthrough-config.yml`

**Data Files:**
- `docs/_data/links.yml`
- `docs/_data/app-deployments.yml`
- `docs/_data/walkthroughs.yml`
- `docs/registry/workflow-registry.json`
- `docs/site/_config.yml`

### 0.3 Remove Product Branding (AgentSphere)

**Delete or Genericize:**
| Current | Action | New Name |
|---------|--------|----------|
| `agentsphere-deployment.yml` | Rename | `demo-deployment.yml` |
| `agentsphere-config.yml` | Rename | `demo-config.yml` |
| `docs/guides/AGENTSPHERE_SETUP.md` | Delete | - |
| `docs/architecture/AGENTSPHERE_*.md` | Delete | - |
| `docs/guides/AUTONOMOUS_ECOSYSTEM_GUIDE.md` | Genericize | `AUTOMATION_GUIDE.md` |

### 0.4 Rename Branded Workflows

| Current | New Name |
|---------|----------|
| `safeguard-8-usage-monitoring.yml` | `usage-monitoring.yml` |
| `agentsphere-deployment.yml` | `demo-deployment.yml` |

---

## Phase 1: Critical Quality Fixes (Week 2)

### 1.1 Fix Agent Frontmatter (32 files)

**Directory:** `src/ai_framework/agents/`

**Files:**
```
amplitude-experiment-implementation.agent.md
CSharpExpert.agent.md
CSharpRefactoringSpecialist.agent.md
completionism-specialist.agent.md
data-forensics-specialist.agent.md
db-architect.agent.md
devops-infrastructure-specialist.agent.md
dotnet-expert.agent.md
dynatrace-expert.agent.md
github-org-manager.agent.md
greener-grass-workflow-benchmark.agent.md
House-Keeping--Pull-Request--Branch--Deep-Cleaner.agent.md
jfrog-sec.agent.md
launchdarkly-flag-cleanup.agent.md
ml-devops-engineer.agent.md
neon-optimization-analyzer.agent.md
nervous-archaeologist.agent.md
nextjs-specialist.agent.md
pagerduty-incident-responder.agent.md
pr-code-review-agent.agent.md
python-automation-specialist.agent.md
react-specialist.agent.md
security-analyst.agent.md
senior-software-engineer.agent.md
site-reliability-engineer.agent.md
team-github-admin.agent.md
technical-writer.agent.md
test-automation-engineer.agent.md
typescript-specialist.agent.md
vercel-deployment-specialist.agent.md
vue-specialist.agent.md
workflow-automation-agent.agent.md
```

**Fix:** Remove duplicate YAML frontmatter blocks from each file.

**Rename for ontological consistency:**
| Current | New Name |
|---------|----------|
| `CSharpExpert.agent.md` | `csharp-expert.agent.md` |
| `CSharpRefactoringSpecialist.agent.md` | `csharp-refactoring.agent.md` |
| `House-Keeping--Pull-Request--Branch--Deep-Cleaner.agent.md` | `pr-branch-cleanup.agent.md` |

### 1.2 Fix ChatMode Frontmatter (90 files)

**Directory:** `src/ai_framework/chatmodes/`

**Sample files needing fixes:**
```
api-architect.chatmode.md
api-design-patterns.chatmode.md
azure-architect.chatmode.md
azure-devops-pipeline.chatmode.md
[...86 more files]
```

**Rename for consistency:**
| Current | New Name |
|---------|----------|
| `4.1-Beast.chatmode.md` | `enhanced-reasoning.chatmode.md` |
| `gpt-5-beast-mode.chatmode.md` | `advanced-reasoning.chatmode.md` |
| `Ultimate-Transparent-Thinking-Beast-Mode.chatmode.md` | `transparent-thinking.chatmode.md` |
| `voidbeast-gpt41enhanced.chatmode.md` | `deep-analysis.chatmode.md` |
| `Thinking-Beast-Mode.chatmode.md` | `chain-of-thought.chatmode.md` |

### 1.3 Add Workflow Permissions (6 files)

**Workflows missing `permissions:` block:**
```bash
grep -L "permissions:" .github/workflows/*.yml
```

Add minimal permissions to each:
```yaml
permissions:
  contents: read
```

---

## Phase 2: Workflow Consolidation (Week 3-4)

### 2.1 PR Automation Consolidation (17 → 4)

**Current workflows to consolidate:**
```
.github/workflows/auto-merge.yml
.github/workflows/auto-assign.yml
.github/workflows/auto-assign-reviewers.yml
.github/workflows/auto-batch-prs.yml
.github/workflows/auto-enable-merge.yml
.github/workflows/auto-labeler.yml
.github/workflows/auto-pr-create.yml
.github/workflows/batch-pr-lifecycle.yml
.github/workflows/draft-to-ready-automation.yml
.github/workflows/bulk-pr-operations.yml
.github/workflows/pr-task-catcher.yml
.github/workflows/pr-title-lint.yml
.github/workflows/pr-quality-checks.yml
.github/workflows/claude-code-review.yml
.github/workflows/combine-prs.yml
.github/workflows/pr-batch-merge.yml
.github/workflows/pr-suggestion-implementation.yml
```

**New reusable workflows:**
```
.github/workflows/reusable/pr-validation.yml      # lint, quality, tasks
.github/workflows/reusable/pr-automation.yml      # assign, label, merge
.github/workflows/reusable/pr-review.yml          # code review, suggestions
.github/workflows/reusable/pr-batching.yml        # combine, batch ops
```

### 2.2 CI/Testing Consolidation (8 → 2)

**Current:**
```
.github/workflows/ci.yml
.github/workflows/ci-advanced.yml
.github/workflows/test-coverage.yml
.github/workflows/code-coverage.yml
.github/workflows/run-integration-tests.yml
.github/workflows/test-batch-onboarding-validation.yml
.github/workflows/accessibility-testing.yml
.github/workflows/mutation-testing.yml
```

**New:**
```
.github/workflows/reusable/ci-pipeline.yml           # unified CI
.github/workflows/reusable/specialized-testing.yml   # a11y, mutation, integration
```

### 2.3 Add Concurrency Controls (40 workflows)

**Workflows needing concurrency:**
```bash
grep -L "concurrency:" .github/workflows/*.yml | head -40
```

**Template to add:**
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

---

## Phase 3: Metadata & Documentation (Week 5-6)

### 3.1 Create .meta.json Files (124 workflows)

**Current coverage:** 5/129 (3.9%)

**Schema:**
```json
{
  "layer": "core|interface|logic|application",
  "category": "ci|security|deployment|automation|pr|release",
  "description": "Brief purpose",
  "dependencies": [],
  "triggers": ["push", "pull_request", "schedule", "workflow_dispatch"]
}
```

**Priority workflows for metadata:**
```
.github/workflows/ci.yml                    → core.ci
.github/workflows/security-scan.yml         → core.security
.github/workflows/release.yml               → application.release
.github/workflows/deployment.yml            → application.deployment
.github/workflows/pr-title-lint.yml         → interface.validation
```

### 3.2 Implement Version Variables

**Create repository variables:**
- `PYTHON_VERSION_DEFAULT` = `3.12`
- `NODE_VERSION_DEFAULT` = `20`
- `GO_VERSION_DEFAULT` = `1.22`

**Update 40+ workflow references:**
```yaml
# Before
python-version: '3.12'

# After
python-version: ${{ vars.PYTHON_VERSION_DEFAULT || '3.12' }}
```

### 3.3 Create Documentation Portal

**Create:** `docs/INDEX.md`

**Structure:**
```
docs/
├── INDEX.md                    # Entry point
├── getting-started/
│   ├── QUICKSTART.md
│   ├── CONFIGURATION.md
│   └── CUSTOMIZATION.md
├── guides/
│   ├── WORKFLOWS.md
│   ├── AGENTS.md
│   ├── CHATMODES.md
│   └── AUTOMATION.md
├── reference/
│   ├── WORKFLOW_CATALOG.md
│   ├── AGENT_CATALOG.md
│   └── SCRIPT_REFERENCE.md
└── architecture/
    ├── OVERVIEW.md
    └── DECISIONS.md
```

### 3.4 Populate Prompts Directory

**Directory:** `src/ai_framework/prompts/`

**Create:**
```
code-review.prompt.md
refactor-for-performance.prompt.md
security-audit.prompt.md
documentation-generation.prompt.md
test-generation.prompt.md
bug-fix-analysis.prompt.md
```

---

## Phase 4: Test Coverage & Security (Week 7-8)

### 4.1 High-Risk Scripts (3 files)

| Script | Current | Target |
|--------|---------|--------|
| `src/automation/scripts/intelligent_routing.py` | 38% | 80% |
| `src/automation/scripts/ab_test_assignment.py` | 45% | 80% |
| `src/automation/scripts/ecosystem_visualizer.py` | 49% | 80% |

### 4.2 Untested Scripts (17 files)

**Create test files for:**
```
tests/unit/test_validate_agent_frontmatter.py
tests/unit/test_validate_labels.py
tests/unit/test_validate_tokens.py
tests/unit/test_validate_workflow_syntax.py
tests/unit/test_generate_agent_inventory.py
tests/unit/test_generate_chatmode_inventory.py
tests/unit/test_generate_collection_inventory.py
tests/unit/test_analyze_workflows.py
tests/unit/test_auto_docs.py
tests/unit/test_check_workflow_health.py
tests/unit/test_dependency_graph.py
tests/unit/test_workflow_linter.py
tests/unit/test_workflow_metrics.py
tests/unit/test_workflow_optimizer.py
tests/unit/test_workflow_validator.py
tests/unit/test_github_api_wrapper.py
tests/unit/test_notification_manager.py
```

### 4.3 Security Hardening

**Pin tool versions in workflows:**
```yaml
# Before
pip install truffleHog detect-secrets

# After
pip install truffleHog==5.0.0 detect-secrets==1.5.0
```

**Add container image scanning:**
```yaml
- name: Scan container image
  run: trivy image --format sarif --output trivy-image.sarif $IMAGE
```

**Audit `contents: write` (58 workflows)** - tighten to minimal permissions.

---

## File Inventory Summary

### Phase 0: Branding (254+ files)
- Root docs: 3 files
- Schema.org: 4 files
- Issue templates: 6 files
- Data files: 4 files
- Workflows: 3 files (rename)
- Docs: 100+ files (search/replace)

### Phase 1: Quality (128 files)
- Agents: 32 files (fix frontmatter, rename 3)
- ChatModes: 90 files (fix frontmatter, rename 5)
- Workflows: 6 files (add permissions)

### Phase 2: Consolidation (65 files)
- PR workflows: 17 → 4 (delete 13, create 4)
- CI workflows: 8 → 2 (delete 6, create 2)
- Concurrency: 40 files (add block)

### Phase 3: Metadata (170+ files)
- Meta files: 124 new files
- Version refs: 40 files
- Docs portal: 10+ new files
- Prompts: 6 new files

### Phase 4: Testing (20+ files)
- Test files: 17 new files
- Script coverage: 3 files enhanced
- Security: 10+ workflow updates

---

## Verification Commands

```bash
# 1. Check branding removal
grep -r "ivviiviivvi" --include="*.yml" --include="*.md" --include="*.json"

# 2. Validate frontmatter
python -c "
import yaml, glob
for f in glob.glob('src/ai_framework/**/*.md', recursive=True):
    content = open(f).read()
    if content.startswith('---'):
        yaml.safe_load(content.split('---')[1])
        print(f'✅ {f}')
"

# 3. Check permissions coverage
grep -L "permissions:" .github/workflows/*.yml | wc -l  # Should be 0

# 4. Run full test suite
pytest --cov=src/automation --cov-fail-under=58

# 5. Validate YAML
for f in .github/workflows/*.yml; do
  python -c "import yaml; yaml.safe_load(open('$f'))" && echo "✅ $f"
done
```

---

## Timeline

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1 | Branding | Template variables, org name removal |
| 2 | Quality | Fixed frontmatter (122 files), permissions |
| 3-4 | Consolidation | 6 reusable workflows, deprecate 19 |
| 5-6 | Metadata | 124 meta files, docs portal, prompts |
| 7-8 | Testing | 17 test files, security hardening |

**Total: 8 weeks, ~450 file modifications**
