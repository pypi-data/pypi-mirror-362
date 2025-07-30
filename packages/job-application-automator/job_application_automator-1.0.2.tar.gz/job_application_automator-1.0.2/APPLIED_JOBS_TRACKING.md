# Applied Jobs Tracking - MCP Tool Documentation

## Overview

A new MCP tool `get_app### 📈 Recent Applications List
- Numbered list (most recent first)
- Auto-detected company names with building emoji
- Application date and time
- Direct application URL links

### 📊 Smart Company Detection
- Automatically detects company names from common job board URLs
- Supports major platforms: Google, Microsoft, Apple, Meta, Amazon, Cisco, etc.
- Greenhouse, Workday, and Lever job boards with company extraction
- Fallback to domain-based company name detectionjobs` has been added to the Form Automation Server that automatically tracks all job applications and displays them in a beautiful markdown dashboard.

## Features

### ✅ Automatic Logging
- **When**: Every time `simple_form_filling` tool is called
- **What**: Logs timestamp and application URL only
- **Where**: Stored in `applied_jobs.txt` in the project root directory
- **Company Detection**: Company names are automatically detected from URLs when displaying the dashboard

### ✅ Beautiful Dashboard
- **Tool Name**: `get_applied_jobs`
- **Display**: Most recent applications at the top
- **Format**: Markdown artifact (automatically rendered)
- **Statistics**: Total applications, unique companies, monthly/weekly counts

## How It Works

### 1. Automatic Logging Process
```
User calls simple_form_filling tool
    ↓
Extracts: URL from form_data
    ↓
Logs to applied_jobs.txt: "timestamp | url"
    ↓
Form filling proceeds normally (browser opens, etc.)
```

### 2. Viewing Applied Jobs
```
User calls get_applied_jobs tool
    ↓
Reads applied_jobs.txt file
    ↓
Parses entries and sorts by most recent first
    ↓
Auto-detects company names from URLs
    ↓
Generates beautiful markdown dashboard
    ↓
Returns as markdown artifact (auto-rendered)
```

## Log File Format

The `applied_jobs.txt` file uses this simplified format:
```
YYYY-MM-DD HH:MM:SS | Application URL
```

**Example entries:**
```
2025-07-17 14:30:22 | https://careers.google.com/jobs/results/123456789/
2025-07-16 09:15:45 | https://careers.microsoft.com/us/en/job/1234567/
2025-07-17 00:21:10 | https://jobs.netflix.com/jobs/123456789
```

**Backward Compatibility**: The tool also supports the old 4-field format for existing log entries:
```
YYYY-MM-DD HH:MM:SS | Company Name | Job Title | Application URL
```

## Tool Details

### `get_applied_jobs` Tool

**Type**: ARTIFACT-ONLY TOOL  
**Input**: None required  
**Output**: Pre-formatted markdown content

**Special Behavior**:
- Tool description forces Claude to ALWAYS generate an artifact
- No additional commentary or explanations allowed
- Direct markdown rendering only

**Tool Description Quote**:
> "CRITICAL: This tool ALWAYS returns the complete content as Markdown text that MUST be rendered as an artifact immediately without any additional commentary or explanation."

## Dashboard Features

### 📊 Application Summary
- Total number of applications
- Last updated timestamp
- Quick overview stats

### � Smart Company Detection
- Automatically detects company names from common job board URLs
- Supports major platforms: Google, Microsoft, Apple, Meta, Amazon, Cisco, etc.
- Greenhouse, Workday, and Lever job boards with company extraction
- Fallback to domain-based company name detection

### 📊 Statistics Table
- Total Applications
- Unique Companies
- This Month count
- This Week count

### 🎨 Visual Elements
- Emoji icons for visual appeal
- Professional markdown formatting
- Clean table layouts
- Proper section headers

## Example Dashboard Output

```markdown
# 📋 Applied Jobs Dashboard

## 🎯 Application Summary
- **Total Applications:** 5
- **Last Updated:** July 17, 2025 at 12:04 AM

---

## 📈 Recent Applications

### 1. Senior Software Engineer
**🏢 Company:** Google  
**📅 Applied:** July 17, 2025 at 02:30 PM  
**🔗 Application URL:** [Google - Senior Software Engineer](https://careers.google.com/jobs/results/123456789/)

---

### 2. Principal Software Engineer
**🏢 Company:** Microsoft  
**📅 Applied:** July 16, 2025 at 09:15 AM  
**🔗 Application URL:** [Microsoft - Principal Software Engineer](https://careers.microsoft.com/us/en/job/1234567/)

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total Applications | 5 |
| Unique Companies | 5 |
| This Month | 5 |
| This Week | 5 |
```

## Error Handling

### No Applications Yet
Shows a friendly message encouraging users to start applying.

### File Doesn't Exist
Creates appropriate "no applications yet" message.

### Parsing Errors
Gracefully handles malformed log entries and continues processing valid ones.

### System Errors
Shows error message with details for troubleshooting.

## Integration with Existing Tools

### No Changes Required
- `simple_form_filler.py` script remains **UNCHANGED**
- Logging happens at the MCP tool level only
- No impact on existing form filling functionality

### Updated Tool List
The Form Automation MCP Server now includes:
1. `simple_form_extraction` - Extract form data from URLs
2. `simple_form_filling` - Fill forms (now with auto-logging)
3. `create_cover_letter` - Generate cover letter files
4. `get_applied_jobs` - **NEW** - View applied jobs dashboard
5. `health_check` - Server health status

## Usage Instructions

### For Users
1. Use form filling tools normally - logging happens automatically
2. Call `get_applied_jobs` anytime to see your application history
3. Dashboard updates in real-time with each new application

### For Claude
- When `get_applied_jobs` is called, MUST create markdown artifact
- No text responses or explanations allowed
- Direct artifact rendering only

## File Locations

```
project_root/
├── applied_jobs.txt                 # Auto-generated log file
├── mcp/
│   └── form_automation_server.py    # Updated with new tool
└── simple_form_filler.py           # Unchanged
```

## Technical Implementation

### Logging Function
```python
def _log_job_application(url: str, job_title: str, company: str) -> None:
    # Simplified: Timestamp + URL only
    # Format: "YYYY-MM-DD HH:MM:SS | URL"
    # Appends to applied_jobs.txt
```

### Company Detection
```python
# Smart URL-based company detection
if 'careers.google.com' in url:
    company = "Google"
elif 'greenhouse.io' in url:
    # Extract company from greenhouse URLs
    company_part = url.split('greenhouse.io/')[1].split('/')[0]
    company = company_part.title()
# ... more detection patterns
```

### Tool Implementation
```python
@mcp.tool()
async def get_applied_jobs() -> str:
    # Reads applied_jobs.txt
    # Parses entries
    # Sorts by timestamp (newest first) 
    # Generates markdown
    # Returns artifact-ready content
```

## Benefits

1. **Simplified Logging**: Minimal data storage (timestamp + URL only)
2. **Smart Company Detection**: Intelligent URL-based company identification
3. **Beautiful Visualization**: Professional markdown dashboard
4. **Chronological Order**: Most recent applications first
5. **Rich Statistics**: Application counts and trends
6. **Backward Compatibility**: Supports both old and new log formats
7. **No Disruption**: Existing tools work unchanged
8. **Real-time Updates**: Dashboard reflects latest applications immediately

## Future Enhancements

Potential future additions:
- Application status tracking (applied/interview/rejected/offer)
- Company statistics and insights
- Export functionality (PDF, CSV)
- Application reminder system
- Integration with job boards
- Application success rate analytics

---

**Created**: July 17, 2025  
**Version**: 1.0.0  
**Status**: Production Ready ✅
