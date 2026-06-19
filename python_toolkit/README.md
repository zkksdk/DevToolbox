# Python Automation Toolkit
## 30+ Ready-to-Use Python Scripts to Save You Hours Every Week

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Scripts](https://img.shields.io/badge/Scripts-30+-orange.svg)](scripts/)

---

### What is this?

A comprehensive collection of **30+ production-ready Python scripts** that automate boring, repetitive tasks. Each script is standalone, well-documented, and tested. No dependencies beyond Python standard library for most scripts.

### Who is this for?

- **Developers** who want to automate their workflow
- **Data analysts** who need quick data processing tools
- **Sysadmins** managing files and servers
- **Freelancers** delivering work faster
- **Beginners** learning Python through real examples

---

## Quick Start

```bash
python toolkit.py              # Interactive menu
python toolkit.py --list       # List all scripts
python toolkit.py --help       # Help
```

Or run individual scripts:
```bash
python scripts/file_organizer.py /path/to/folder
python scripts/csv_to_json.py data.csv
python scripts/batch_rename.py /path "*_old" "_new"
```

---

## Scripts Included

### File Management (8 scripts)
| Script | Description |
|--------|-------------|
| `file_organizer.py` | Sort files by type/date/size |
| `batch_rename.py` | Bulk rename files with patterns |
| `duplicate_finder.py` | Find and remove duplicate files |
| `large_file_scanner.py` | Scan directories for large files |
| `backup_manager.py` | Create incremental backups |
| `clean_temp_files.py` | Remove temporary/junk files |
| `folder_sync.py` | Two-way folder synchronization |
| `disk_usage_reporter.py` | Disk usage analysis with charts |

### Data Processing (6 scripts)
| Script | Description |
|--------|-------------|
| `csv_to_json.py` | Convert CSV to JSON/YAML/XML |
| `excel_merger.py` | Merge multiple Excel files |
| `json_formatter.py` | Format, validate, query JSON |
| `text_cleaner.py` | Clean and normalize text data |
| `log_analyzer.py` | Parse and analyze log files |
| `data_sampler.py` | Random sampling from datasets |

### Web & API (5 scripts)
| Script | Description |
|--------|-------------|
| `bulk_url_checker.py` | Check status of multiple URLs |
| `sitemap_generator.py` | Generate XML sitemaps |
| `api_tester.py` | Test REST APIs with retry logic |
| `html_table_extractor.py` | Extract tables from HTML pages |
| `rss_reader.py` | RSS feed reader & aggregator |

### Image & Media (4 scripts)
| Script | Description |
|--------|-------------|
| `image_resizer.py` | Batch resize images |
| `image_converter.py` | Convert between image formats |
| `screenshot_taker.py` | Automated webpage screenshots |
| `video_thumbnailer.py` | Extract video thumbnails |

### Productivity (5 scripts)
| Script | Description |
|--------|-------------|
| `pomodoro_timer.py` | Command-line Pomodoro timer |
| `todo_manager.py` | CLI task manager with priorities |
| `meeting_notes.py` | Generate meeting note templates |
| `time_tracker.py` | Track time spent on projects |
| `clipboard_manager.py` | Multi-slot clipboard history |

### System & Network (4 scripts)
| Script | Description |
|--------|-------------|
| `network_scanner.py` | Scan local network for devices |
| `process_monitor.py` | Monitor CPU/Memory of processes |
| `service_watcher.py` | Watch and restart services |
| `bandwidth_monitor.py` | Monitor network bandwidth usage |

---

## Highlights

```python
# 1. Organize 1000 files in one command
$ python scripts/file_organizer.py ~/Downloads --by-type

# 2. Convert entire CSV folder to JSON
$ python scripts/csv_to_json.py data/ --batch --output json/

# 3. Find duplicates across drives
$ python scripts/duplicate_finder.py C:\ D:\ --min-size 1MB

# 4. Check 200 URLs in parallel
$ python scripts/bulk_url_checker.py urls.txt --concurrent 20

# 5. Merge 50 Excel files into one
$ python scripts/excel_merger.py reports/*.xlsx --output merged.xlsx
```

---

## Installation

```bash
# Clone the toolkit
git clone https://github.com/zkksdk/python-toolkit.git
cd python-toolkit

# Install optional dependencies
pip install -r requirements.txt

# Ready!
python toolkit.py
```

---

## Pricing & License

This toolkit is available under the MIT License. Use it freely in personal and commercial projects.

**If this saves you time, consider supporting development:**
- ⭐ Star the repo
- 💝 [GitHub Sponsors](https://github.com/sponsors/zkksdk)
- ☕ [Buy me a coffee](https://buymeacoffee.com/zkksdk)

---

## Why I Built This

Most "automation toolkits" are either too complex or too simple. This one is designed to be:
- **Immediately useful** - every script solves a real problem
- **Well documented** - clear docstrings and examples
- **Battle-tested** - production ready, not tutorial code
- **No bloat** - minimal dependencies, maximum utility

---

Built with ❤️ by zkksdk | [More tools](https://zkksdk.github.io/DevToolbox/)
