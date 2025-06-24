#!/bin/bash
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# In order to run this script, you must have Go installed on your machine. This
# script will attempt to setup a GOPATH and GOBIN in your $HOME directory, if
# those environment variables are not already set. It will then attempt to
# install the dependencies needed to run (protoc-gen-go and protoc, needed to
# compile the protos).

# This should be run from the root FHIR repository, like so:
# ./go/generate_go_protos_default.sh

################################################################################
# <SUPERPOWER.COM ADDITION>
# A.S. 2025-06-24
#
# This script is a modified version of the original script from the FHIR repository.
# It adds a live timer to the script, fixes some Python dependencies, and a few other improvements :)
################################################################################

if [ "${GOPATH}" = "" ]; then
  echo "🔧 Setting temp GOPATH environment variable, creating GOPATH directory \$HOME/go"
  GOPATH="${HOME}/go"
  mkdir -p $GOPATH
fi

if [ "${GOBIN}" = "" ]; then
  echo "🔧 Setting temp GOBIN environment variable, creating GOBIN directory in \$GOPATH/bin"
  GOBIN="${GOPATH}/bin"
  mkdir -p $GOBIN
fi

if ! [ -x "$(command -v protoc)" ]; then
  echo '❌ protoc missing, please install the protobuf compiler. On linux: sudo apt install -y protobuf-compiler'
fi

go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.29.0
PATH=$PATH:$GOBIN

bazel run //go:generate_go_protos -- --repo-path="$(pwd)" &
bazel_pid=$!

echo "🚀 Generating Go protos. This step may take a while. Errors will appear below if any."
start_time=$(date +%s)

while kill -0 $bazel_pid 2>/dev/null; do
  current_time=$(date +%s)
  elapsed=$((current_time - start_time))
  printf "⏱️  Elapsed time: %ds...\r" "$elapsed"
  sleep 1
done
wait $bazel_pid

end_time=$(date +%s)
total_elapsed=$((end_time - start_time))
echo "\n🎉 All done in ${total_elapsed}s."
