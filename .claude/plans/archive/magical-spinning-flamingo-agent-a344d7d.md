# Template Placeholder System Audit

## Mapping Table: Template Variables → Config YAML Fields

| Template Variable | Files Using | Config Field | Resolution | Status |
|---|---|---|---|---|
| `{{CONDUCT_EMAIL}}` | CODE_OF_CONDUCT.md:39, CONTRIBUTING.md:42 | `emails.conduct` | organvum-i-theoria: `conduct@organvum.org` | ✓ RESOLVED |
| `{{ORG_DISPLAY_NAME}}` | CONTRIBUTING.md:1, FUNDING.yml:1, SECURITY.md:12, profile/README.md:3 | `org.display_name` | organvum-i-theoria: `ORGAN I: Theoria` | ✓ RESOLVED |
| `{{ORG_NAME}}` | CONTRIBUTING.md:7, SECURITY.md:36, ISSUE_TEMPLATE/config.yml:4, profile/README.md:24 | `org.name` | organvum-i-theoria: `organvum-i-theoria` | ✓ RESOLVED |
| `{{SUPPORT_EMAIL}}` | CONTRIBUTING.md:46 | `emails.support` | organvum-i-theoria: `support@organvum.org` | ✓ RESOLVED |
| `{{SECURITY_EMAIL}}` | SECURITY.md:19 | `emails.security` | organvum-i-theoria: `security@organvum.org` | ✓ RESOLVED |
| `{{ORGAN_ETYMOLOGY}}` | profile/README.md:5 | `organ.etymology` | organvum-i-theoria: `θεωρία — contemplation, theory` | ✓ RESOLVED |
| `{{ORGAN_TAGLINE}}` | profile/README.md:7 | `organ.tagline` | organvum-i-theoria: `Epistemological frameworks and recursive systems` | ✓ RESOLVED |
| `{{ORGAN_DESCRIPTION}}` | profile/README.md:13 | `organ.*` (no direct match) | ✗ UNDEFINED | ⚠ UNDEFINED |
| `{{TAXIS_ORG}}` | CONTRIBUTING.md:3,7 | N/A in config | ✗ NOT IN CONFIG | ⚠ UNDEFINED |

## Gap Analysis

### A. Undefined Placeholders (Used in Templates, Missing from Config)

1. **`{{ORGAN_DESCRIPTION}}`** (profile/README.md:13)
   - Used in: Organization profile README
   - Expected config field: `organ.description` or similar
   - Current behavior: Would appear as literal `{{ORGAN_DESCRIPTION}}` in rendered README
   - **Status**: CRITICAL GAP — No config field provides this value

2. **`{{TAXIS_ORG}}`** (CONTRIBUTING.md:3, 7)
   - Used in: CONTRIBUTING.md lines 3 and 7
   - Line 3: "This organization is part of the [organvm](https://github.com/{{TAXIS_ORG}}) seven-organ creative-institutional system."
   - Line 7: "See the [main organvm repo](https://github.com/{{TAXIS_ORG}}/blob/main/.github/CONTRIBUTING.md)"
   - Expected config field: Should reference the orchestration organ (ORGAN IV: Taxis)
   - Current behavior: Would appear as literal `{{TAXIS_ORG}}` in rendered CONTRIBUTING.md
   - **Status**: CRITICAL GAP — This placeholder expects `organvum-iv-taxis` but is NOT provided by any config field
   - **Resolution source**: Should likely be a cross-organ reference or global system config value

### B. Unused Config Fields (Present in YAML, Never Referenced in Templates)

The following config fields have no corresponding template variables:

1. **Organization-level fields**:
   - `org.website` — Not used in any template
   - `org.email_domain` — Not used (individual emails used instead)

2. **Repository-level fields**:
   - `repo.name` — Not used in any template (currently `.github`)
   - `repo.npm_scope` — Not used in any template

3. **Social fields**:
   - `social.discord_invite` — Not used in any template

4. **Team fields** (all unused):
   - `teams.leadership`
   - `teams.engineering`
   - `teams.devops`
   - `teams.security`

5. **Product fields** (all unused):
   - `product.name`
   - `product.api_endpoint`

6. **Defaults fields** (all unused):
   - `defaults.python_version`
   - `defaults.node_version`
   - `defaults.go_version`
   - `defaults.rust_version`

7. **Template fields** (all unused):
   - `template.version`
   - `template.source`
   - `template.description`

8. **Features fields** (all unused):
   - `features.ai_agents`
   - `features.advanced_ci`
   - `features.security_scanning`
   - `features.automated_releases`
   - `features.demo_sandbox`
   - `features.documentation_site`
   - `features.slack_notifications`
   - `features.ml_workflows`

9. **Organ fields** (partially used):
   - `organ.key` — Not used in any template
   - `organ.domain` — Not used in any template
   - `organ.license` — Not used in any template

### C. Hardcoded Values That Should Be Placeholders

**File: profile/README.md, line 24**
```markdown
This organization is one of 7 in the [organvm](https://github.com/organvum-iv-taxis) creative-institutional system:
```

**Issue**: Hardcoded `organvum-iv-taxis` should be `{{TAXIS_ORG}}`

**Reason**: This hardcodes a cross-organ dependency that breaks if the template is used for non-ORGAN-IV organizations. The same profile README template is used for all 7 organs, but it currently hardcodes a link to ORGAN IV.

### D. Profile README Placeholder Verification

Testing all 5 profile/README.md placeholders against organvum-i-theoria.template-config.yml:

| Placeholder | Config Path | Value | Resolvable? |
|---|---|---|---|
| `{{ORG_DISPLAY_NAME}}` | `org.display_name` | `ORGAN I: Theoria` | ✓ YES |
| `{{ORGAN_ETYMOLOGY}}` | `organ.etymology` | `θεωρία — contemplation, theory` | ✓ YES |
| `{{ORGAN_TAGLINE}}` | `organ.tagline` | `Epistemological frameworks and recursive systems` | ✓ YES |
| `{{ORGAN_DESCRIPTION}}` | (missing) | N/A | ✗ NO |
| `{{ORG_NAME}}` | `org.name` | `organvum-i-theoria` | ✓ YES |

**Result**: 4 of 5 placeholders are resolvable. `{{ORGAN_DESCRIPTION}}` is NOT resolvable.

## Summary of Issues

| Category | Count | Severity |
|---|---|---|
| Undefined placeholders | 2 | CRITICAL |
| Unused config fields | 21 | LOW (config is over-provisioned) |
| Hardcoded org names | 1 | HIGH |
| Profile README unresolvable placeholders | 1 | CRITICAL |

## Recommendations

1. **Add `organ.description` to config schema** — All config files should include `organ.description` field to resolve `{{ORGAN_DESCRIPTION}}` placeholder.

2. **Add `taxis_org` to config schema** — All config files should include a `cross_organ_refs.taxis_org` or similar field with value `organvum-iv-taxis` to resolve `{{TAXIS_ORG}}` placeholder.

3. **Fix hardcoded org name in profile/README.md:24** — Replace `organvum-iv-taxis` with `{{TAXIS_ORG}}` placeholder.

4. **Consider template variable coverage** — The 21 unused config fields suggest the config schema is over-specified for the current template requirements. Either:
   - Extend templates to use these fields, OR
   - Trim config schema to essential fields only

