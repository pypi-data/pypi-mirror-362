# Claude Development Guidelines for SophiRead

## Overview

This document contains essential behavioral protocols for AI development work on the SophiRead project, extracted from extensive memory optimization and refactoring experience.

---

## Development Discipline Protocol

### STOP IMMEDIATELY IF:
- Creating test files without explicit approval
- Modifying code without showing exact before/after diffs
- Referencing functions without specific line numbers
- Making assumptions about APIs or function signatures
- Working on multiple files simultaneously
- Attempting to git commit anything
- Using ANY git commands whatsoever
- Using cd commands to change directories
- Suggesting code changes without reading source first

### REQUIRED WORKFLOW:
1. **READ**: Quote specific line numbers and actual code
2. **EXPLAIN**: What the code ACTUALLY does (not what it should do)
3. **VERIFY**: User confirms understanding before proceeding
4. **TODO**: Create one specific task at a time with code references
5. **IMPLEMENT**: Show exact diff before applying any changes

### RED FLAGS TO AVOID:
- "This probably..." / "This should..." / "I think this function..."
- "The API likely..." / Multiple file modifications
- No line number references / Creating functions without seeing them first

### VERIFICATION REQUIREMENTS:
- Every code reference must include file path and line numbers
- Every function mentioned must be shown with actual signature
- Every memory allocation must be traced to specific code
- No "imagined" or "assumed" behavior

---

## Test Failure Protocol

When unit tests fail after code changes, follow this MANDATORY process:

1. **DO NOT immediately assume the code is wrong**
2. **DO NOT offer to "fix" source code to match tests**
3. **STOP and analyze systematically:**

### Step 1: Understand the Test
- Read the test thoroughly
- Identify what behavior it's testing
- Understand the test's assumptions and design

### Step 2: Evaluate Test Relevance  
- Is this test still relevant after refactoring?
- Was the test written for an outdated API/design?
- Does the test test the right thing for the new architecture?

### Step 3: Analyze the Failure
- What specific assertion is failing?
- What was expected vs actual?
- Trace the failure back to source code changes

### Step 4: Root Cause Analysis
- Is the failure due to:
  - Bug in new code? 
  - Outdated test assumptions?
  - Changed API that test needs to adapt to?
  - Different but equivalent behavior?

### Step 5: Propose Solution WITH EXPLANATION
- If test needs updating: explain why and how
- If code needs fixing: explain the actual bug
- If test should be removed: explain why it's obsolete
- ALWAYS explain reasoning before making changes

### Example Decision Matrix:
```
Failure Type → Action
Wrong API usage in test → Update test to new API
Changed behavior (equivalent) → Update test expectations  
Test assumes old architecture → Rewrite or remove test
Actual bug found → Fix code (with explanation)
```

---

## Pixi Project Management

This project is managed by **pixi** - ALL commands must be run through pixi:

### Critical Rules:
1. **READ `pixi.toml` first** to understand available targets
2. **NEVER suggest arbitrary build commands** - use defined targets only
3. **Use single quotes** for Python commands: `pixi run python -c 'import sys; print(sys.version)'`
4. **NO `cd` commands allowed** - use full paths with pixi run
5. **Ask about tool availability** - don't assume tools exist

### Before Suggesting Tools:
- Check `pixi.toml` for available targets
- If tool not available, ASK USER to add it
- Don't cycle through different tools hoping one works
- Don't suggest installing tools directly

---

## TPX3 Data Structure Constraints

### Critical Understanding
The TPX3 raw data format imposes strict constraints on processing:

1. **Variable Section Sizes**: No padding or fixed boundaries
2. **Local Time Disorder**: Packets within sections NOT time-ordered
3. **Missing TDC Packets**: Hardware may drop TDC packets
4. **Sequential Dependencies**: TDC state must propagate in order

### DO NOT ATTEMPT
- ❌ Parallel section discovery (breaks variable section boundaries)
- ❌ Parallel TDC propagation (breaks sequential state dependencies)
- ❌ Any optimization that assumes time ordering within sections

---

## API Verification Requirements

### Before Writing ANY Code That Calls a Function:
- **ALWAYS read the actual function signature** from the source file if available
- **NEVER assume parameter names or return values**
- **If you cannot find the API, STOP and tell the user explicitly**

### Show Your Work:
When solving problems:
1. State what you're looking for and why
2. Show which files you're checking
3. Quote the exact lines you're basing decisions on
4. Explain your reasoning before implementing

### Honesty About Uncertainty:
When you're not sure:
- Say "I need to check the actual implementation"
- Say "I'm assuming X, let me verify"
- Say "I cannot find the reference for Y"
- **NEVER fill in gaps with plausible-sounding code**

---

## Environment-Specific Behavior

### For Pixi Projects (pyproject.toml + pixi.toml):
**MUST**:
- Check `[tool.pixi.dependencies]` for available packages
- Check `[tool.pixi.pypi-dependencies]` for pip packages
- Use `pixi run <command>` for ALL Python execution
- Check if package is installed as editable before adding path hacks
- Look for `[tool.pixi.tasks]` for predefined commands

**NEVER**:
- Use pip install directly
- Assume global packages are available
- Add sys.path manipulations for editable packages

---

## Error Handling Protocol

### Command Execution Failures:
When ANY command fails or produces an error:
1. **IMMEDIATELY read this CLAUDE.md file**
2. **Check which protocol rule was forgotten**
3. **Identify the specific violation (git, cd, missing pixi run, etc.)**
4. **Acknowledge the mistake and correct approach**
5. **Then proceed with proper protocol**

### Common Error Sources:
- Forgetting `pixi run` prefix
- Attempting git operations  
- Using cd commands
- Suggesting code without reading source
- Assuming APIs without verification

---

## User Control Commands

- **STOP**: Halt immediately, no questions asked
- **SHOW ME**: Provide exact code with line numbers
- **READ AGAIN**: Re-read file without assumptions
- **ONE THING ONLY**: Focus on single task
- **VERIFY**: Confirm understanding before proceeding

---

## Memory and Performance Context

### Key Completed Optimizations (Reference for Future Work):
- ✅ Zero-copy Python bindings (50% memory reduction)
- ✅ Function bloat elimination (58% total memory reduction: 48GB → 20GB)
- ✅ Pre-calculated TDC values (billions of FLOPs saved)
- ✅ Debug-only coordinate validation (2 billion operations eliminated)
- ✅ Pre-allocated vectors (eliminated reallocation overhead)
- ✅ Chunk-based memory mapping (5.6GB → 512MB, 91% reduction)

### Always Consider:
- Memory impact of any new data structures
- Cache locality for hot paths
- Zero-copy patterns where possible
- Pixi environment constraints

---

---

## Critical Lessons Learned (2025-01-14)

### Stateless is NOT Optional - It's the ONLY Path
**Context**: During Week 3 memory optimization, attempted to maintain both stateful and stateless clustering algorithms

**Mistake Made**: 
- Tried to keep SimpleABSClustering (stateful) alive alongside StatelessABSClustering
- Treated stateless as an "incremental improvement" rather than a fundamental requirement
- Lost sight of the >120M hits/sec performance target

**Why This Failed**:
- Stateful algorithms CANNOT safely run in parallel with TBB
- The race conditions are fundamental, not fixable with mutexes or workarounds
- Trying to support both creates impossible architectural conflicts

**Correct Approach**:
1. **Stateless is MANDATORY** for the speed requirements
2. **Delete/deprecate all stateful implementations** - they're dead ends
3. **Commit fully to the stateless architecture** - no compromises
4. **Focus on the project goal** (>120M hits/sec), not code safety

**Remember**: "You can't boil water and add ice in the same pot" - stateful and stateless are fundamentally incompatible approaches. Choose one (stateless) and commit.

---

*Document Purpose: Maintain development discipline and prevent regression of hard-won optimizations*