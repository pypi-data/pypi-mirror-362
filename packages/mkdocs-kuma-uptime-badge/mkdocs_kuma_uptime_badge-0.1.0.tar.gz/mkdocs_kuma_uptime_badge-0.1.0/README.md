# MkDocs Kuma Uptime Badge Plugin

A tiny MkDocs plugin that converts shorthand placeholders to full Uptime Kuma badge links during the build.

## Installation

Using pip:

```bash
pip install mkdocs-kuma-uptime-badge
```

Using Poetry:

```bash
poetry add mkdocs-kuma-uptime-badge
```

For development:

```bash
# Clone the repository
git clone https://github.com/culturepulse/mkdocs-kuma-uptime-badge.git
cd mkdocs-kuma-uptime-badge

# Install with Poetry (recommended)
poetry install

# Or with pip
pip install -e .
```

## Usage

1. Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - kuma-uptime-badge:
      base_url: https://your-kuma-instance.example.com
```

2. In your Markdown files, use the shorthand syntax:

```markdown
{{uptime id=1}}  # Basic status badge

{{uptime id=2 type=uptime hours=24}}  # Uptime badge for the last 24 hours

{{uptime id=3 type=ping hours=720 label="30" labelSuffix="d"}}  # Ping badge with custom label
```

These will be converted to full Markdown image links during the build:

```markdown
![status](https://your-kuma-instance.example.com/api/badge/1/status)

![uptime](https://your-kuma-instance.example.com/api/badge/2/uptime/24)

![ping](https://your-kuma-instance.example.com/api/badge/3/ping/720?label=30&labelSuffix=d)
```

## Syntax

The general syntax for the shorthand is:

```
{{uptime id=<monitorID> [type=<badgeType>] [hours=<int>] [key=value ...]}}
```

Where:

- `id` (required): The monitor ID from Uptime Kuma
- `type` (optional): The badge type, one of:
  - `status` (default)
  - `uptime`
  - `ping`
  - `avg-response`
  - `cert-exp`
  - `response`
- `hours` (optional): Duration in hours, only used for `uptime`, `ping`, `avg-response`, and `response` badge types
- Additional key-value pairs: Any other parameters will be added as query string parameters to the badge URL

### Examples

#### Status Badge

```markdown
{{uptime id=1}}
{{uptime id=1 type=status}}
{{uptime id=1 upLabel="Online" downLabel="Offline"}}
{{uptime id=1 upColor="green" downColor="red"}}
```

#### Uptime Badge

```markdown
{{uptime id=1 type=uptime hours=24}}
{{uptime id=1 type=uptime hours=720 label="30" labelSuffix="d"}}
{{uptime id=1 type=uptime hours=24 color="blue"}}
```

#### Ping Badge

```markdown
{{uptime id=1 type=ping hours=24}}
{{uptime id=1 type=ping hours=24 labelPrefix="Average" label="Ping" labelSuffix=""}}
```

#### Certificate Expiry Badge

```markdown
{{uptime id=1 type=cert-exp}}
{{uptime id=1 type=cert-exp warnDays=14 downDays=7}}
```

#### Badge Styles

```markdown
{{uptime id=1 style=flat}}  # Default
{{uptime id=1 style=flat-square}}
{{uptime id=1 style=plastic}}
{{uptime id=1 style=for-the-badge}}
{{uptime id=1 style=social}}
```

## Configuration

The plugin supports the following configuration options:

- `base_url`: The base URL of your Uptime Kuma instance (default: `https://kuma.intra`)

---
Made with ❤️ and ☕️ by [CulturePulse](https://www.culturepulse.ai/) development team
