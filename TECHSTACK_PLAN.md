# Tech Stack Plan TUI

## Language
- **Golang**

## Core CLI Framework
- **`github.com/spf13/cobra`**
  - Command routing, argument parsing, and CLI scaffolding.

## Logging
- **`go.uber.org/zap`**
  - Structured, high-performance logging library from Uber.

## Storage
- **SQLite**
  - Database engine: `sqlite`
  - Go driver option: `github.com/mattn/go-sqlite3`

## Charm Ecosystem (preferred where possible)
- **`github.com/charmbracelet/bubbletea`**
  - TUI framework for interactive terminal applications.
- **`github.com/charmbracelet/lipgloss`**
  - Styling and layout for terminal UI components.
- **`github.com/charmbracelet/bubbles`**
  - Reusable Bubble Tea components.
- **`github.com/charmbracelet/log`** (optional)
  - Charm-native logger option if aligned with project conventions.

## Suggested Initial Dependency Set
```txt
github.com/spf13/cobra
go.uber.org/zap
github.com/mattn/go-sqlite3
github.com/charmbracelet/bubbletea
github.com/charmbracelet/lipgloss
github.com/charmbracelet/bubbles
```
