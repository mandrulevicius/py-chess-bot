# Instructions for AI Agents: Creating Documentation for Other AI Agents

## 🎯 **Core Principle**
AI agents need **structured, contextual information** that enables rapid understanding without cognitive overload. Think "executive briefing" rather than "comprehensive manual."

## ⚠️ **CRITICAL: Documentation Maintenance**
**Documentation decays rapidly during active development.** These instructions emphasize **mandatory pre-commit updates** throughout. Documentation that doesn't reflect current reality is worse than no documentation at all.

**Key maintenance principles repeated throughout this guide:**
- 📝 **Break work into todo list items** - makes documentation updates manageable
- 🔄 **Update docs before EVERY commit**
- 📝 **One commit per logical task** (easier to document)
- ⚠️ **Stale docs are toxic** - they mislead rather than help

## 📋 **Essential Documentation Components**

### 1. **Architecture Overview** (Most Critical)
```
WHAT TO INCLUDE:
✅ System structure (components, dependencies, data flow)  
✅ Critical files and their roles (start here, core utilities, high-impact)
✅ Key patterns and design decisions (layered architecture, no circular deps)
✅ Current development hotspots vs stable components

WHAT TO AVOID:
❌ Implementation details of individual functions
❌ Historical design alternatives that weren't chosen
❌ Detailed API specifications (unless critical to understanding)
```

### 2. **Development Context** (Workflow & Methodology)
```
WHAT TO INCLUDE:
✅ Development methodology (TDD, specific workflow patterns)
✅ Essential commands for testing/running/debugging
✅ Code style patterns and conventions to follow
✅ High-impact files that require extra care when changing

WHAT TO AVOID:
❌ Exhaustive command line options
❌ Environment setup instructions (assume working environment)
❌ IDE-specific configurations
```

### 3. **Project Context** (Goals & Current State)
```
WHAT TO INCLUDE:  
✅ Project purpose and target audience
✅ Current capabilities vs original goals
✅ Technology choices and their rationale
✅ Current development focus areas

WHAT TO AVOID:
❌ Complete feature wishlists
❌ Detailed user stories or requirements specs  
❌ Marketing-style feature descriptions
```

## 🏗️ **Information Architecture Principles**

### **Layered Information Design**
1. **Essential Layer** - What every AI agent must know (4-5 key files max)
2. **Detailed Layer** - Comprehensive analysis for deep dives (when needed)
3. **Historical Layer** - Legacy docs and decision history (rarely needed)

### **Optimize for AI Consumption**
- **Structured data** over prose when possible
- **Clear hierarchies** with consistent formatting
- **Scannable sections** with descriptive headers  
- **Actionable insights** rather than just descriptions

## 📝 **Writing Guidelines**

### **Structure Each Document**
```markdown
# Title - Purpose Statement

> One-sentence description of what this doc provides

## 🎯 **Quick Start** (Always include)
- Most important 3-5 points for immediate understanding
- Links to key files or concepts

## 📊 **Main Content**
- Use consistent emoji/formatting for visual scanning
- Group related information clearly
- Include practical examples

## ⚠️ **Critical Considerations**  
- High-impact areas requiring extra care
- Common gotchas or important patterns

## 🛠️ **Practical Actions**
- Commands to run, files to check, patterns to follow
```

### **Language Patterns**
- **Lead with the conclusion** - most important info first
- **Use active voice** - "The system does X" not "X is done by the system"
- **Include context** - not just what, but why and when
- **Be specific** - "5 dependents" not "many dependents"

## 🔍 **Content Curation Strategy**

### **Information Hierarchy**
1. **Architecture understanding** (essential for any changes)
2. **Current state context** (active areas, stable areas) 
3. **Development workflow** (how to make changes safely)
4. **Implementation details** (only when architecturally relevant)

### **Redundancy Management**
- **Consolidate overlapping content** rather than linking
- **Single source of truth** for each type of information
- **Cross-reference sparingly** - prefer self-contained sections

### **Freshness Indicators**
- **Date documentation** so AI agents know recency
- **Mark development hotspots** vs stable components
- **Include activity indicators** (commit counts, recent changes)

## 🎯 **Quality Checklist**

### **For Each Document, Ask:**
- [ ] Can an AI agent understand the system architecture in 5 minutes?
- [ ] Are the most critical files and their relationships clear?  
- [ ] Is current development context (what's changing vs stable) obvious?
- [ ] Are there clear next steps for common development tasks?
- [ ] Is information organized for scanning rather than sequential reading?

### **For the Documentation Set, Ask:**
- [ ] Is there a clear entry point and reading order?
- [ ] Are there different detail levels without redundancy?
- [ ] Can an AI agent find what they need without reading everything?
- [ ] Is the cognitive load appropriate (4-6 essential files max)?

## 🔄 **Documentation Maintenance Discipline** (CRITICAL)

### **⚠️ UPDATE DOCS BEFORE EVERY COMMIT**
Documentation is **only valuable if current**. Stale docs are worse than no docs.

**MANDATORY PRE-COMMIT CHECKLIST:**
- [ ] Do architectural changes affect the Architecture Overview?
- [ ] Do new high-impact files need to be documented?
- [ ] Has the development focus shifted to new areas?
- [ ] Are the "current hotspots" still accurate?
- [ ] Do new patterns or conventions need documentation?

### **Commit Frequency Strategy**
- **One commit per logical task/todo item** - makes documentation updates manageable
- **Small, frequent commits** are easier to document than large changes
- **Document during development**, not as an afterthought

### **Signs Documentation Needs Updates**
- **New critical files** with multiple dependents
- **Architecture changes** (new layers, different patterns)
- **Development focus shifts** (new active areas)
- **Technology decisions** (new dependencies, frameworks)
- **Workflow changes** (new testing approaches, tools)

## 💡 **Meta-Principles**

### **Design for Scanning**
AI agents process information differently than humans. Optimize for:
- **Pattern recognition** - consistent structure across docs
- **Rapid context switching** - clear section boundaries  
- **Information density** - more insight per paragraph
- **Actionable content** - what to do, not just what exists

### **Assume Working Environment**  
Don't waste cognitive bandwidth on:
- Basic tool installation or environment setup
- Generic programming concepts or patterns
- Detailed troubleshooting for common issues

### **Focus on Decision Support**
The goal is enabling good decisions about:
- **What files to examine** for understanding the system
- **Where to make changes** safely and effectively  
- **What patterns to follow** when extending the system
- **What areas require extra care** due to high impact

---

## 🚀 **Recommended Development Workflow**

### **Task-Based Development with Documentation**
1. **Create todo list items** - break complex work into specific, manageable tasks
2. **Work on one todo item at a time** - complete fully before moving to next
3. **Update documentation** if the task changed architecture/patterns
4. **Mark todo complete and commit** - one commit per completed todo item
5. **Repeat** - small, documented, frequent commits

### **Why Todo Lists Are Essential**
- **Manageable scope** - easier to document small, specific changes
- **Progress tracking** - clear completion criteria for each task
- **Commit boundaries** - natural points for documentation updates
- **Context preservation** - future AI agents can understand work breakdown

### **Documentation Maintenance Triggers**
**ALWAYS UPDATE DOCS WHEN:**
- ⚠️ **Adding new critical files** (high dependency count)
- ⚠️ **Changing architecture patterns** (layering, data flow)
- ⚠️ **Shifting development focus** (new active areas)
- ⚠️ **Adding new technologies** or changing tooling
- ⚠️ **Before any major commit** - check if docs are still accurate

### **Pre-Commit Documentation Checklist** 
```bash
# Before every git commit, ask:
- Did I complete this todo item fully?
- Do my changes affect the architectural overview?
- Are the "current hotspots" still accurate?  
- Did I add files that other developers need to know about?
- Are my workflow/methodology changes documented?
- Is the development context still current?
- Should I mark this todo as completed in the commit?
```

### **Todo List Best Practices**
- **Use the TodoWrite tool** to track progress throughout development
- **Be specific** - "Add user authentication" vs "Implement login system with session management"
- **One logical change per todo** - enables clean commits and documentation
- **Mark completed immediately** - maintains accurate progress tracking
- **Clean up stale todos** - remove or update items that are no longer relevant

## 🎯 **Bottom Line**

Good AI-to-AI documentation is like a **well-designed API** - it provides the right abstractions at the right level of detail, with clear contracts and minimal cognitive overhead. 

Focus on **architectural understanding, current context, and practical guidance** rather than comprehensive coverage. The goal is **effective collaboration**, not complete documentation.

**⚠️ CRITICAL REMINDER: Documentation is only valuable when current. Update before every commit, or it becomes a liability rather than an asset.**

## 📚 **Template Structure Example**

For any new project, create this essential documentation structure:

```
docs/relevant_docs/
├── ARCHITECTURE_OVERVIEW.md    # System structure, dependencies, key files
├── DEVELOPMENT_GUIDE.md        # TDD workflow, commands, patterns  
├── PROJECT_CONTEXT.md          # Goals, decisions, current state
└── README.md                   # Navigation and quick start
```

Each document should be **self-contained**, **scannable**, and **actionable** for maximum AI agent effectiveness.