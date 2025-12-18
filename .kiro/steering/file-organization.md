---
inclusion: always
---

# File Organization and Development Standards

## Core Principle

**Only production-ready, tested files should exist in main directories. All experimental, testing, and alternative versions MUST be in Debug folders.**

## Directory Structure Rules

### 1. Debug Folder Requirement

**MANDATORY:** Every directory containing scripts or tools MUST have a `Debug/` subdirectory with task-based organization.

```
Scripts/MapGenerators/
├── Debug/
│   ├── ddc-workaround/             # Task: Fix DDC issue
│   │   ├── generate_map_auto.bat
│   │   ├── auto_generate_and_quit.py
│   │   └── notes.txt
│   ├── remote-execution/           # Task: Remote execution attempt
│   │   ├── execute_in_running_editor.py
│   │   ├── generate_in_running_editor.bat
│   │   └── notes.txt
│   └── alternative-ui/             # Task: Alternative UI approaches
│       ├── show_instructions.bat
│       ├── generate_via_file.py
│       └── notes.txt
├── generate_map.bat                # ONLY production file
├── generate_cosmos_002_training_world.py
└── README.md
```

**Task Folder Naming:**
- Use lowercase with hyphens: `task-name/`
- Descriptive but concise: `ddc-workaround/`, `remote-execution/`
- Each task folder MUST have a `notes.txt` explaining what was attempted

### 2. Production Files (Main Directory)

**Rules:**
- Maximum 1-2 batch files per directory
- Only fully tested, working scripts
- Clear, simple naming
- Must be documented in README.md

**Allowed in main directory:**
- Primary execution script (1 file)
- Alternative method if necessary (1 file max)
- Core Python scripts (tested and working)
- Documentation files (README.md, etc.)

### 3. Debug Files (Debug/ Subdirectory)

**Must be in Debug/[task-name]/:**
- Test scripts for specific task
- Experimental implementations
- Alternative approaches being tested
- Failed attempts (for learning)
- Development notes (notes.txt in each task folder)
- Multiple versions of same functionality
- Scripts with known issues

**Task Folder Structure:**
```
Debug/
├── task-name-1/
│   ├── script1.py
│   ├── script2.bat
│   └── notes.txt          # Required: explains what was tried
├── task-name-2/
│   ├── alternative.py
│   └── notes.txt
└── README.txt             # Optional: overview of all tasks
```

### 4. File Naming Conventions

**Production files:**
```
generate_map.bat              ✅ Simple, clear
execute_script.py             ✅ Descriptive
README.md                     ✅ Standard
```

**Debug files:**
```
Debug/test_remote_execution.py        ✅ Prefixed with purpose
Debug/experimental_socket_comm.py     ✅ Clearly experimental
Debug/alternative_method_v2.bat       ✅ Version indicated
Debug/failed_ddc_workaround.py        ✅ Status clear
```

## Development Workflow

### Phase 1: Development (Debug/task-name/ folder)
1. Create task folder: `Debug/task-name/`
2. Create scripts in task folder
3. Test and iterate
4. Keep all versions for reference

### Phase 2: Testing (Debug/task-name/ folder)
1. Test thoroughly in task folder
2. Document in `notes.txt` what works and what doesn't
3. Identify the best solution

### Phase 3: Production (Main directory)
1. Move ONLY the working solution to main directory
2. Rename to simple, clear name
3. Keep failed attempts in `Debug/task-name/` with notes
4. Update README.md

### Phase 4: Cleanup (Debug folder)
1. Organize by task folders
2. Each task folder has `notes.txt`
3. Delete obvious duplicates
4. Keep one example of each approach with explanation

## Example: Map Generator Organization

**BEFORE (Messy):**
```
Scripts/MapGenerators/
├── generate_map_auto.bat
├── generate_map_editor.bat
├── generate_in_running_editor.bat
├── generate_instructions.bat
├── show_instructions.bat
├── 立即执行.bat
├── execute_in_running_editor.py
├── generate_via_file.py
├── auto_generate_and_quit.py
└── generate_cosmos_002_training_world.py
```

**AFTER (Clean with Task Folders):**
```
Scripts/MapGenerators/
├── Debug/
│   ├── ddc-workaround/
│   │   ├── generate_map_auto.bat
│   │   ├── auto_generate_and_quit.py
│   │   ├── DDC_FIX_GUIDE.md
│   │   └── notes.txt              # Explains DDC issue and attempts
│   ├── remote-execution/
│   │   ├── execute_in_running_editor.py
│   │   ├── generate_in_running_editor.bat
│   │   └── notes.txt              # Explains remote execution attempt
│   ├── ui-variations/
│   │   ├── show_instructions.bat
│   │   ├── generate_instructions.bat
│   │   ├── 立即执行.bat
│   │   ├── generate_via_file.py
│   │   └── notes.txt              # Explains different UI approaches
│   └── README.txt                 # Overview of all debug tasks
├── generate_map.bat               # ONLY production file
├── generate_cosmos_002_training_world.py
├── README.md
└── QUICK_START.md
```

## AI Agent Rules

### When Creating New Files

1. **First file:** Create in main directory
2. **Alternative approach:** Create `Debug/task-name/` folder first, then create files
3. **Testing variation:** Create in appropriate `Debug/task-name/` folder
4. **After testing:** Move working version to main, keep test in Debug with notes.txt

### When Multiple Solutions Exist

1. Create separate task folders in Debug: `Debug/approach-1/`, `Debug/approach-2/`
2. Test all approaches in their respective folders
3. Identify the best one
4. Move ONLY the best to main directory
5. Keep others in Debug with notes.txt in each folder

### When Cleaning Up

1. Ask user which solution worked
2. Move working solution to main directory
3. Organize Debug by task folders
4. Create `notes.txt` in each task folder explaining:
   - What was attempted
   - Why it failed or succeeded
   - What was learned
5. Create `Debug/README.txt` with overview

## User Benefits

✅ **Clear:** Only 1-2 files to choose from
✅ **Simple:** Obvious which file to run
✅ **Clean:** No clutter in main directory
✅ **Traceable:** Debug folder keeps history
✅ **Documented:** README explains the one production file

## Enforcement

**CRITICAL:** AI must follow these rules:
- ❌ Do NOT create multiple batch files in main directory
- ❌ Do NOT leave experimental files in main directory
- ❌ Do NOT dump all debug files in `Debug/` root
- ✅ DO create `Debug/task-name/` folders for each task/approach
- ✅ DO create `notes.txt` in each task folder
- ✅ DO move test files to appropriate task folders
- ✅ DO ask user which solution worked before finalizing
- ✅ DO keep main directory minimal (1-2 execution files max)
- ✅ DO organize Debug by task, not by file type

## Exception: Documentation

Documentation files can exist in main directory:
- README.md (required)
- QUICK_START.md (optional)
- One additional guide (optional)

All other documentation → Debug/docs/
