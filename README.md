# superpowerdotcom/fhir

This is a fork of `google/fhir` with small additions to support custom Medplum sources. As of 06/23/2025, use this repo to work off of the protos for our Go implementations. We currently have custom proto definitions for:
- User

## Building the Go proto packages

Please ensure you have the following installed before proceeding:

### Prerequisites


1. **Go** (version 1.19 or later)
   ```bash
   brew install go
   go version  # Verify installation
   ```

2. **Protocol Buffer Compiler (protoc)**
   ```bash
   brew install protobuf
   protoc --version  # Verify installation
   ```

3. **Bazel** (for building the project)
   ```bash
   brew install bazel
   bazel version  # Verify installation
   ```

4. **Python 3** (usually pre-installed on macOS)
   ```bash
   brew install python3  # If not already installed
   python3 --version  # Verify installation
   ```

### Building Go Proto Packages

Once all prerequisites are installed, run the following command from the repository root:

```bash
./go/generate_go_protos_default.sh
```

This script will:
- Set up Go environment variables (GOPATH/GOBIN) if not already configured
- Install the required `protoc-gen-go` plugin automatically
- Generate Go protobuf files from the `.proto` definitions
- Place the generated files in the appropriate directories under `go/proto/`

**Note**: The first run may take longer as it downloads and sets up dependencies. Subsequent runs will be faster.

### Troubleshooting

- **"protoc not found"**: Ensure Protocol Buffer compiler is installed (see step 2 above)
- **"bazel not found"**: Ensure Bazel is installed (see step 3 above)  
- **Permission errors**: Make sure the script is executable: `chmod +x go/generate_go_protos_default.sh`

Below is the original README from the forked repo for more information.

---


# Introduction

FhirProto is Google’s implementation of the [FHIR Standard](http://hl7.org/fhir/) for Health Care data using [Protocol Buffers](https://developers.google.com/protocol-buffers).  By leveraging Google’s core data storage format, FhirProto provides a type-safe, strongly validated FHIR format with cross-language support at a fraction of the size on disk, making it a great data model to develop your Health Care application on.  Structured Codes and Extensions guarantee that your data will be in the correct format.  Support for generating and validating against custom Implementation Guides allow you to customize FhirProto to your dataset and requirements.  Parsing and Printing libraries make it easy to go back and forth between FhirProto format and JSON.

# Getting Started
We think the best way to get an idea of how FhirProto works is to get in and start playing with it.  To that end, we provide [https://github.com/google/fhir-examples](https://github.com/google/fhir-examples). This repo contains a script for using [Synthea](https://github.com/synthetichealth/synthea) to create a synthetic FHIR JSON dataset, and then shows some examples of parsing, printing, validating, profiling and querying.  The repo also contains a [walkthrough](https://github.com/google/fhir-examples/blob/master/EXAMPLES.md) of many of the examples.

A Reference User Guide with in-depth descriptions of different concepts can be found [here](https://github.com/google/fhir-examples/blob/master/USERGUIDE.md).

## Trademark
FHIR® is the registered trademark of HL7 and is used with the permission of HL7. Use of the FHIR trademark does not constitute endorsement of this product by HL7.

