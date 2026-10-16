---
name: token-saver
description: Best practices and guidelines for AI agents to minimize token consumption while maintaining high quality and accuracy.
---

# Token Saver Skill Plugin

This skill provides actionable strategies and operational constraints for AI agents to drastically minimize input and output token consumption without sacrificing response accuracy or solution quality.

---

## 1. Core Principles of Token Efficiency

1. **Be Direct & Concise**: Omit conversational filler, politeness boilerplate (e.g., "Sure, I can help with that!"), and redundant restatements of user requests.
2. **Minimize Context Overhead**: Read only the necessary sections of files, avoid printing massive files or logs into context when summary or targeted grepping suffices.
3. **Batch Operations**: Execute multiple tool calls in parallel when independent, reducing intermediate multi-turn conversation rounds.
4. **Structured & Compact Outputs**: Prefer concise markdown, bullet points, or structured formats over long prose paragraphs.

---

## 2. Practical Strategies for AI Agents

### A. Output Optimization (Saving Generation Tokens)
- **No Pleasantries**: Skip introductory and concluding conversational fluff.
- **Direct Code Diffs / Snip-Editing**: Output only modified code blocks or diffs rather than re-printing entire unmodified multi-hundred-line files.
- **Brevity in Explanation**: Provide brief context for code changes rather than exhaustive line-by-line narrations.
- **Use Abbreviations / Compact Formats**: Use concise lists, tables, or key-value pairs where appropriate.

### B. Input Context Optimization (Saving Context Tokens)
- **Targeted File Reading**: Avoid reading full large files if `grep`, `head`, `tail`, or AST tools can isolate the needed code segment.
- **Trimmed Command Outputs**: Limit bash output verbosity (e.g., using `head -n 20`, `--quiet`, redirecting noise to `/dev/null`, or filtering log outputs).
- **Clean Workspace Environment**: Avoid leaving massive output files in working directories that might be scanned repeatedly.

### C. Tool Call Efficiency
- **Multi-Tool Invocation**: Call tools together in a single response cycle when operations are independent.
- **Fail Fast & Query Precisely**: Formulate precise search regexes or queries to find exact symbols instead of broad file listings.

---

## 3. Quick Reference Checklist for AI Agents

- [ ] Am I avoiding fluff like "Hello! I would be happy to assist..."?
- [ ] Am I reading only relevant lines or files instead of dumping whole directories?
- [ ] Am I sending unified tool calls where possible?
- [ ] Is my code explanation clear yet minimal?
- [ ] Have I summarized large command outputs before injecting them into memory?
