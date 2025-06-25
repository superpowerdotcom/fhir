# Staging Releases Guide

NOTE: mr. robot generated this README, it's actually kind of a nice writeup on how pkg versioning should work for staging releases so i'm keeping it here ~ A.S
---

This guide explains how to create and use staging releases for the FHIR Go protobuf library.

## What are Staging Releases?

Staging releases are pre-release versions that allow you to test changes before they become part of a stable release. They use semantic versioning with pre-release identifiers like:

- `go/v1.2.3-beta.20250625151200`
- `go/v1.2.3-alpha.20250625151200`
- `go/v1.2.3-rc.20250625151200`

## Creating a Staging Release

### Prerequisites
- Push access to the repository
- Access to GitHub Actions

### Steps

1. **Navigate to GitHub Actions**
   - Go to the repository on GitHub
   - Click on "Actions" tab
   - Find "superpowerdotcom/fhir/go - Staging Release"

2. **Trigger the Workflow**
   - Click "Run workflow"
   - Select the branch you want to release from
   - Choose your options:
     - **Pre-release type**: `beta`, `alpha`, or `rc`
     - **Version increment**: `patch`, `minor`, or `major`
   - Click "Run workflow"

3. **Monitor the Release**
   - The workflow will run tests
   - Create a new tag with timestamp
   - Create a GitHub pre-release
   - Provide installation instructions

## Using Staging Releases

### Option 1: Direct Installation
```bash
go get github.com/superpowerdotcom/fhir/go@go/v1.2.3-beta.20250625151200
```

### Option 2: Update go.mod
```bash
go mod edit -require=github.com/superpowerdotcom/fhir/go@go/v1.2.3-beta.20250625151200
go mod download
```

### Option 3: Manual go.mod Edit
Edit your `go.mod` file:
```go
module your-project

go 1.22

require (
    github.com/superpowerdotcom/fhir/go go/v1.2.3-beta.20250625151200
)
```

## Version Strategy

### Pre-release Types
- **alpha**: Early development versions, may have breaking changes
- **beta**: Feature-complete versions for testing, fewer breaking changes expected
- **rc** (release candidate): Near-final versions, minimal changes expected

### Version Increments
- **patch**: Bug fixes and small improvements (`1.2.3` → `1.2.4`)
- **minor**: New features, backward compatible (`1.2.3` → `1.3.0`)
- **major**: Breaking changes (`1.2.3` → `2.0.0`)

## Examples

### Testing a Bug Fix
```bash
# Create a patch pre-release
# GitHub Actions: prerelease_type=beta, version_increment=patch
# Result: go/v1.2.4-beta.20250625151200

go get github.com/superpowerdotcom/fhir/go@go/v1.2.4-beta.20250625151200
```

### Testing a New Feature
```bash
# Create a minor pre-release
# GitHub Actions: prerelease_type=beta, version_increment=minor
# Result: go/v1.3.0-beta.20250625151200

go get github.com/superpowerdotcom/fhir/go@go/v1.3.0-beta.20250625151200
```

### Release Candidate Before Major Version
```bash
# Create a major pre-release
# GitHub Actions: prerelease_type=rc, version_increment=major
# Result: go/v2.0.0-rc.20250625151200

go get github.com/superpowerdotcom/fhir/go@go/v2.0.0-rc.20250625151200
```

## Reverting to Stable

When you're done testing, revert to the latest stable version:

```bash
go get github.com/superpowerdotcom/fhir/go@latest
```

Or specify a specific stable version:
```bash
go get github.com/superpowerdotcom/fhir/go@go/v1.2.3
```

## Best Practices

1. **Always test staging releases** in a development environment first
2. **Use descriptive commit messages** when creating the staging release
3. **Document what you're testing** in pull requests or issues
4. **Clean up** by reverting to stable versions after testing
5. **Use the appropriate pre-release type** for your testing phase

## Troubleshooting

### Module Cache Issues
If you have issues with Go module caching:
```bash
go clean -modcache
go mod download
```

### Version Not Found
Ensure the tag exists:
```bash
git fetch --tags
git tag -l "go/v*"
```

### Import Path Issues
Always use the full module path:
```go
import "github.com/superpowerdotcom/fhir/go/proto/google/fhir/proto/r4/core/profiles/datatypes_go_proto"
```

## Finding Staging Releases

- **GitHub Releases**: Look for releases marked as "Pre-release"
- **Tags**: All staging releases have timestamps in the format `YYYYMMDDHHMMSS`
- **Go Package Site**: Visit [pkg.go.dev/github.com/superpowerdotcom/fhir/go](https://pkg.go.dev/github.com/superpowerdotcom/fhir/go) and check the versions tab 