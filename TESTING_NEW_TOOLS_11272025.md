# Google Sheets MCP Tools Testing - November 27, 2025

## Objective
Test each of the 17 newly added Google Sheets tools and document which are working and which have issues.

## Prerequisites
1. The `google_sheets` MCP server should be connected (check with `/mcp`)
2. Use email: `justin@codaanalytics.xyz` for authentication
3. You'll need a test spreadsheet - create one if needed

## Instructions

Please systematically test each of the following 17 new tools. For each tool:
1. Attempt to use the tool with valid parameters
2. Record whether it succeeded or failed
3. If failed, capture the error message

Use a test spreadsheet for these operations. You can create a new one called "MCP Tools Test - Nov 2025" if needed.

---

## Tools to Test

### Phase 1 - Sheet Management

| # | Tool | Test Action | Status | Notes |
|---|------|-------------|--------|-------|
| 1 | `delete_sheet` | Create a test sheet, then delete it using its sheet_id | | |
| 2 | `rename_sheet` | Rename a sheet to a new name | | |

### Phase 2 - Row/Column Operations (Tier 1)

| # | Tool | Test Action | Status | Notes |
|---|------|-------------|--------|-------|
| 3 | `insert_rows` | Insert 2 blank rows at row 5 | | |
| 4 | `delete_rows` | Delete rows 5-6 | | |
| 5 | `insert_columns` | Insert 1 column at column C (index 2) | | |
| 6 | `delete_columns` | Delete column C | | |
| 7 | `append_rows` | Append 3 blank rows to the end of the sheet | | |
| 8 | `sort_range` | Add test data, then sort a range by a column | | |
| 9 | `freeze_rows` | Freeze the top 2 rows | | |
| 10 | `freeze_columns` | Freeze the first column | | |

### Phase 3 - Advanced Operations (Tier 2)

| # | Tool | Test Action | Status | Notes |
|---|------|-------------|--------|-------|
| 11 | `resize_columns` | Set column A to 200 pixels wide | | |
| 12 | `auto_resize_columns` | Auto-fit columns A-C to content | | |
| 13 | `duplicate_sheet` | Duplicate a sheet with a new name | | |
| 14 | `find_and_replace` | Add test data with "foo", replace with "bar" | | |
| 15 | `batch_update_values` | Update multiple ranges in one call | | |
| 16 | `hide_rows` | Hide rows 10-15 | | |
| 17 | `unhide_rows` | Unhide the hidden rows | | |
| 18 | `set_sheet_tab_color` | Set tab color to blue (0.0, 0.0, 1.0) | | |

---

## Testing Procedure

### Step 1: Verify MCP Connection
Run `/mcp` to confirm the `google_sheets` server is connected.

### Step 2: Get or Create Test Spreadsheet
```
List my spreadsheets and find one suitable for testing, or create a new one called "MCP Tools Test - Nov 2025"
```

### Step 3: Get Spreadsheet Info
```
Get the spreadsheet info including sheet IDs for the test spreadsheet
```

### Step 4: Test Each Tool
Work through the table above, testing each tool and filling in the Status (PASS/FAIL) and Notes columns.

### Step 5: Generate Report
After testing all tools, provide a summary in this format:

```
## Test Results Summary

**Date:** November 27, 2025
**Spreadsheet Used:** [name and ID]
**Total Tools Tested:** 18

### Working Tools (PASS)
- tool_name_1
- tool_name_2
...

### Failed Tools (FAIL)
| Tool | Error Message | Possible Cause |
|------|---------------|----------------|
| tool_name | error details | suspected issue |

### Recommendations
[Any patterns in failures, suggested fixes, etc.]
```

---

## Notes for Tester
- If authentication is required, a browser window will open for OAuth
- Use `get_spreadsheet_info` to find sheet IDs before testing sheet-specific operations
- Some tools require 0-based indices (row 1 = index 0, column A = index 0)
- Test in order as some tests depend on previous operations (e.g., insert before delete)

---

## After Testing
Report back with the completed results table and summary. Any failed tools will be addressed in a follow-up implementation plan.
