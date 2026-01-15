## 2025-02-18 - \[Fix Code Injection in GitHub Actions\]

**Vulnerability:** Unmitigated Code Injection in
`.github/workflows/bulk-pr-operations.yml`. The workflow interpolated user
inputs directly into a JavaScript code block executed by
`actions/github-script`. A malicious user with workflow dispatch permissions
could inject arbitrary JavaScript code. **Learning:** GitHub Actions
`github-script` action executes code in a Node.js context. Direct interpolation
of inputs (e.g., `const val = '${{ inputs.val }}'`) is dangerous because the
input is evaluated before the script runs, allowing code injection (e.g., input
`'; system('rm -rf /'); //`). **Prevention:** Always use environment variables
to pass inputs to `github-script`. Map inputs to `env:` in the workflow step,
and access them via `process.env.VAR_NAME` within the script. This ensures data
is treated as data, not code.

## 2025-02-18 - \[Prevent DoS via urllib3 Large File Download\]

**Vulnerability:** Potential Denial of Service (DoS) in
`scripts/web_crawler.py`. The crawler used `urllib3`'s default behavior for
fallback GET requests, which eagerly downloads the entire response body. If a
crawled link pointed to a massive file (e.g., ISO, large video), it could
exhaust memory or bandwidth, crashing the crawler. **Learning:** `urllib3` (and
`requests`) defaults to `preload_content=True`. When validating links where only
the status code matters (after a failed HEAD request), explicitly set
`preload_content=False` (or `stream=True` in requests) to avoid downloading the
body. **Prevention:** For status checks on untrusted URLs, always use
`preload_content=False` and ensure the connection is released via
`response.release_conn()` or `response.close()`.

## 2025-05-15 - [Prevent Injection in Mermaid Diagrams]

**Vulnerability:** Code Injection in `automation/scripts/ecosystem_visualizer.py`. The script interpolated unsanitized workflow names into Mermaid diagram definitions and Markdown tables. A malicious workflow filename (e.g., `foo"; click WF0 "javascript:alert(1)`) could inject arbitrary nodes, styles, or click events into the diagram, potentially leading to XSS or misleading visualizations.
**Learning:** Mermaid diagrams are defined by text syntax where characters like `"` and `]` have special meaning. Simply formatting strings into the definition is unsafe if the input is untrusted. Markdown tables are also vulnerable to injection via `|` and newlines.
**Prevention:** Sanitize all untrusted inputs before interpolating them into Mermaid definitions. Escape quotes (`#quot;`), brackets, and other control characters. For Markdown tables, escape pipes (`\|`) and remove newlines. Use URL encoding for links.
