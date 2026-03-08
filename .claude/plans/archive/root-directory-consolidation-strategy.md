# Root Directory Consolidation Strategy

**Goal**: Reduce root directory from 41 items to approximately 10 items by consolidating related files and dotfiles into existing subdirectories.

**Current State**: 41 items at root level
**Target State**: ~10 items at root level

## Current Root Directory Inventory (41 items)

### Dotfiles/Hidden Directories (14 items)
- `.claude/` - Claude Code local config
- `.commitlintrc.json` - Commit linting rules
- `.dockerignore` - Docker build ignore patterns
- `.env` - Environment variables (local)
- `.env.local` - Environment overrides (local)
- `.envrc` - direnv configuration
- `.git/` - Git repository metadata
- `.github/` - GitHub workflows and templates
- `.gitignore` - Git ignore rules
- `.husky/` - Git hooks
- `.lighthouserc.js` - Lighthouse CI configuration
- `.prettierrc` - Prettier formatting config
- `.release-please-manifest.json` - Release automation manifest
- `.serena/` - Serena project metadata

### Core Source Directories (4 items)
- `apps/` - Application layer (web, api, orchestrator)
- `packages/` - Shared packages (schema, core, content-model, design-system)
- `docs/` - Documentation (30+ files across 5 subdirectories)
- `infra/` - Infrastructure configs (20+ items across 7 subdirectories)

### Development & Build (2 items)
- `scripts/` - Dev utility scripts
- `node_modules/` - Dependencies (generated, can be gitignored)

### Configuration Files (7 items)
- `eslint.config.mjs` - ESLint flat config
- `turbo.json` - Turborepo configuration
- `vitest.config.ts` - Vitest test runner config
- `tsconfig.json` - TypeScript root configuration
- `seed.yaml` - Repository constraints/standards
- `.DS_Store` - macOS metadata (can be gitignored)
- `tsconfig.tsbuildinfo` - TypeScript build info (generated, can be gitignored)

### Root Documentation (7 items)
- `README.md` - Project overview
- `CHANGELOG.md` - Version history
- `CLAUDE.md` - Claude Code instructions
- `CONTRIBUTING.md` - Contribution guidelines
- `CODE_OF_CONDUCT.md` - Community guidelines
- `CODEOWNERS` - GitHub code ownership
- `LICENSE` - MIT license

### Package Management (3 items)
- `package.json` - Root workspace definition
- `pnpm-lock.yaml` - Dependency lock file
- `pnpm-workspace.yaml` - pnpm workspace config

### Automation & Secrets (2 items)
- `release-please-config.json` - Release automation config
- `secrets.env.op.sh` - 1Password secret integration script

---

## Consolidation Strategy

### Phase 1: Move Configuration Files to `config/` Subdirectory

**Create new directory structure**:
```
config/
├── .commitlintrc.json
├── .dockerignore
├── .env.example
├── .env.integration.example
├── .env.production.example
├── .lighthouserc.js
├── .prettierrc
├── .release-please-manifest.json
├── eslint.config.mjs
├── turbo.json
├── vitest.config.ts
├── tsconfig.json
├── tsconfig.base.json (if applicable)
├── seed.yaml
└── release-please-config.json
```

**Rationale**: Consolidates build/lint/test/release configurations into a dedicated `config/` directory. Update root-level imports in scripts and CI to reference `config/` paths.

**Impact**: Removes 13 items from root.

---

### Phase 2: Consolidate Dotfiles into `.config/` Hidden Directory

**Create new structure**:
```
.config/
├── husky/           → from .husky/
├── github/          → from .github/
├── claude.json      → from .claude/ (or keep .claude as-is for Claude Code integration)
├── env.local        → from .env.local
├── envrc            → from .envrc
└── gitignore        → optional, leave root .gitignore as standard
```

**Rationale**: 
- Keep `.github/` at root (GitHub convention for workflows/templates)
- Keep `.git/` at root (git standard)
- Keep `.husky/` at root (husky convention)
- Consider keeping `.claude/` at root (Claude Code integration needs it here)
- Consider keeping `.env` and `.env.local` at root (convention for many frameworks)
- `.gitignore` should remain at root (git standard)

**Revised approach**: Keep most dotfiles in place (they're framework/tool conventions). Move only:
- `commitlintrc.json` → `config/.commitlintrc.json`
- `lightouserc.js` → `config/.lighthouserc.js`
- `prettierrc` → `config/.prettierrc`

**Impact**: Minimal—removes ~3 items, keeps standard dotfiles in place.

---

### Phase 3: Consolidate Build/Release Configuration

Move to `infra/config/` (instead of new root-level `config/`):
```
infra/config/
├── build/
│   ├── eslint.config.mjs
│   ├── vitest.config.ts
│   ├── tsconfig.json
│   └── turbo.json
├── release/
│   ├── release-please-config.json
│   └── .release-please-manifest.json
└── test/
    └── seed.yaml
```

**Rationale**: Groups infrastructure-related configs alongside deployment configs in the existing `infra/` directory, maintaining logical separation.

**Impact**: Removes 7 items from root (eslint, turbo, vitest, tsconfig, release-please-config, seed.yaml, plus commit/prettier/lighthouse).

---

### Phase 4: Generated Files to .gitignore

Ensure the following are in `.gitignore` (should already be present):
- `node_modules/`
- `tsconfig.tsbuildinfo`
- `.DS_Store`
- `dist/`, `build/`, `.turbo/`

**Rationale**: These are generated artifacts and shouldn't clutter the root directory in the first place.

**Impact**: Visually removes 3 items (though they're in git, they won't appear in working tree).

---

## Proposed Target Root Directory (10 items)

```
life-my--midst--in/
├── apps/                           # Source code (web, api, orchestrator)
├── packages/                        # Shared packages (schema, core, content-model, design-system)
├── docs/                           # Documentation and decision records
├── infra/                          # Infrastructure, deployment, k8s configs (now includes config/build|release)
├── scripts/                        # Development utility scripts
├── .github/                        # GitHub workflows and templates (keep at root)
├── .husky/                         # Git hooks (keep at root)
├── package.json                    # Root workspace definition
├── pnpm-workspace.yaml             # pnpm workspace config
└── README.md                       # Main project overview
```

**Optional near-root files** (can go to ~10 or slightly above):
- `CLAUDE.md` - Claude Code instructions
- `CONTRIBUTING.md` - Contribution guidelines
- `LICENSE` - MIT license
- `.env.local` - Local environment overrides

---

## Migration Steps

### Step 1: Create `infra/config/` subdirectories
```bash
mkdir -p infra/config/{build,release,test}
```

### Step 2: Move build configuration
```bash
mv eslint.config.mjs infra/config/build/
mv turbo.json infra/config/build/
mv vitest.config.ts infra/config/build/
mv tsconfig.json infra/config/build/
mv seed.yaml infra/config/test/
```

### Step 3: Move release configuration
```bash
mv release-please-config.json infra/config/release/
mv .release-please-manifest.json infra/config/release/
```

### Step 4: Move lint configuration
```bash
mv .commitlintrc.json infra/config/
mv .prettierrc infra/config/
mv .lighthouserc.js infra/config/
```

### Step 5: Update references in scripts and workflows
- Update `package.json` scripts that reference config file paths
- Update GitHub Actions workflows in `.github/workflows/` to reference new paths
- Update root TypeScript imports if they reference `tsconfig.json`
- Update ESLint to reference `infra/config/build/eslint.config.mjs`
- Update Prettier to reference `infra/config/.prettierrc`
- Update turbo CLI references to `infra/config/build/turbo.json`

### Step 6: Verify and test
```bash
pnpm install
pnpm lint
pnpm test
pnpm build
```

---

## Files to Keep at Root (Non-Negotiable)

| File | Reason |
|------|--------|
| `.git/` | Git standard location |
| `.github/` | GitHub Actions convention |
| `.gitignore` | Git standard location |
| `.husky/` | Husky hook convention |
| `.env` | Framework environment convention |
| `.env.local` | Local overrides convention |
| `.envrc` | direnv convention |
| `package.json` | pnpm workspace root definition |
| `pnpm-workspace.yaml` | Workspace definition |
| `README.md` | Project overview at root |
| `LICENSE` | Open-source convention |

---

## Files to Consider at Root (Project-Specific)

| File | Keep? | Reason |
|------|-------|--------|
| `.claude/` | **Yes** | Claude Code integration requires this location |
| `.serena/` | **Yes** | Serena project metadata (if needed) |
| `CLAUDE.md` | **Yes** | Developer instructions for Claude Code |
| `CONTRIBUTING.md` | **Yes** | Contribution guidelines (GitHub convention) |
| `CHANGELOG.md` | **Optional** | Can move to `docs/CHANGELOG.md` |
| `CODE_OF_CONDUCT.md` | **Optional** | Can move to `docs/CODE_OF_CONDUCT.md` |
| `CODEOWNERS` | **Yes** | GitHub convention at root |

---

## Estimated Impact

| Phase | Items Removed | New Root Count |
|-------|--------------|-----------------|
| Current state | — | 41 |
| Phase 1-3 (consolidate configs) | ~15 | 26 |
| Phase 4 (ignore generated) | ~3 | 23 (visually ~10-12 in `ls`) |
| Keep standards + project docs | — | ~12 final |

**Final root (with docs kept separate)**: ~10 functional items + 2-3 documentation files = 12-13 items

---

## Alternative: More Aggressive Consolidation

If targeting exactly 10 items, move documentation to `docs/`:
- Move `CONTRIBUTING.md` → `docs/CONTRIBUTING.md`
- Move `CHANGELOG.md` → `docs/CHANGELOG.md`
- Move `CODE_OF_CONDUCT.md` → `docs/CODE_OF_CONDUCT.md`
- Keep only `README.md` at root

**Final state (most aggressive)**:
```
life-my--midst--in/
├── apps/                    # Applications
├── packages/                # Shared packages
├── docs/                    # All documentation (including CHANGELOG, CONTRIBUTING, etc.)
├── infra/                   # Infrastructure (including configs)
├── scripts/                 # Development utilities
├── .github/                 # GitHub workflows
├── .husky/                  # Git hooks
├── package.json
├── pnpm-workspace.yaml
└── README.md
```

**Result**: 10 items exactly at root.

---

## Recommendation

**Adopt Phase 1-3 strategy** (move configs to `infra/config/`) while keeping these at root:
- Standard dotfiles (`.github/`, `.git/`, `.husky/`, `.gitignore`, `.env`, `.env.local`, `.envrc`)
- Project integration files (`.claude/`, `.serena/`)
- Package management (`package.json`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`)
- Primary documentation (`README.md`)
- Project governance (`LICENSE`, `CODEOWNERS`, `CONTRIBUTING.md`)

This reduces root clutter from 41 to ~12-13 items while respecting framework/tool conventions and maintaining developer ergonomics.

---

## Implementation Priority

1. **High Priority**: Move build/test configs to `infra/config/build/` (high impact, low risk)
2. **High Priority**: Move release configs to `infra/config/release/` (consolidates automation)
3. **Medium Priority**: Update all references in scripts/workflows (ensures functionality)
4. **Low Priority**: Move additional lint/doc configs (minimal impact)
5. **Optional**: Move documentation to `docs/` if targeting exactly 10 items

