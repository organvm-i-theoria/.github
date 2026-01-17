#!/bin/bash
# Week 11 Phase 1 Deployment Script
# This script deploys labels and workflows to 3 pilot repositories
#
# Security: All scripts use 1Password CLI for secure token retrieval.
# Tokens are only in memory during execution, never written to disk.

set -e  # Exit on any error

echo "=================================================="
echo "Week 11 Phase 1 Deployment"
echo "=================================================="
echo ""
echo "🔐 Scripts will securely retrieve GitHub token from:"
echo "   1. 1Password CLI (item: batch-label-deployment-011726)"
echo "   2. Fallback to GITHUB_TOKEN environment variable"
echo ""

cd /workspace/automation/scripts

# Step 1: Deploy labels automatically
echo "📋 Step 1: Deploying labels to 3 repositories..."
echo ""
python3 validate_labels.py \
  --config ../config/batch-onboard-week11-phase1-pilot.yml \
  --fix

echo ""
echo "✅ Labels deployed!"
echo ""

# Step 2: Verify all prerequisites
echo "🔍 Step 2: Running pre-deployment checklist..."
echo ""
python3 pre_deployment_checklist.py --phase 1

echo ""
echo "=================================================="
echo "✅ Pre-deployment checks passed!"
echo "=================================================="
echo ""

# Step 3: Deploy workflows
echo "🚀 Step 3: Deploying workflows to repositories..."
echo ""
python3 batch_onboard_repositories.py \
  --config ../config/batch-onboard-week11-phase1-pilot.yml \
  --output week11-phase1-production.json

echo ""
echo "=================================================="
echo "🎉 Phase 1 Deployment Complete!"
echo "=================================================="
echo ""
echo "Results saved to: week11-phase1-production.json"
echo ""
echo "Next steps:"
echo "  1. Monitor repositories for 48 hours"
echo "  2. Verify workflow executions"
echo "  3. Proceed to Phase 2 after validation"
echo ""
