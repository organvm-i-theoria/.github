# Workflow Metrics Summary

**Last Updated**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

## Overview

This file is automatically updated every 6 hours with the latest workflow metrics.

$(python3 << 'PYTHON'
import json
with open('metrics/workflow-metrics.json', 'r') as f:
    data = json.load(f)

summary = data['summary']
print(f"- **Total Workflows**: {summary['total_workflows']}")
print(f"- **Active Workflows**: {summary['workflows_with_runs']}")
print(f"- **Runs Analyzed**: {summary['total_runs_analyzed']}")
print(f"- **Success Rate**: {summary['overall_success_rate']}%")
print(f"- **Avg Duration**: {summary['avg_workflow_duration_min']} minutes")
print()
print("## Top 10 Most Active Workflows")
print()
print("| Rank | Workflow | Runs | Success Rate | Avg Duration |")
print("|------|----------|------|--------------|--------------|")
for i, wf in enumerate(data['workflows'][:10], 1):
    print(f"| {i} | {wf['name']} | {wf['total_runs']} | {wf['success_rate']}% | {wf['avg_duration_min']} min |")
PYTHON
)

## Metrics Files

- `workflow-metrics.json` - Complete metrics data (updated automatically)
- `baseline-metrics.json` - Baseline for comparison

