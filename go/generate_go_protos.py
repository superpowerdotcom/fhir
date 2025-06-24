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
"""generate_go_protos is responsible for regenerating the go FHIR proto code.

This script regenerates the go FHIR proto code. This should be run whenever the
protos themselves are updated to ensure the generated go code is in sync.
Committing the generated go source code into the repository is necessary to
support go modules.
"""

import os
import shutil
import tempfile
import uuid
import sys
import time

from absl import app
from absl import flags

FLAGS = flags.FLAGS

_REPO_PATH = flags.DEFINE_string(
    "repo-path", None,
    "The path to the root of the FHIR repository."
)

def log(msg):
    print(msg)
    sys.stdout.flush()

def move_generated_go_protos(tmp_dir: str):
  """Responsible for moving the generated go protos to their final destination.

  Args:
    tmp_dir: the temporary directory where the proto building and
      transformations occur.
  """
  dest_root = _REPO_PATH.value
  proto_dest_dir = os.path.join(dest_root, "go/proto/google")
  shutil.rmtree(proto_dest_dir, ignore_errors=True)
  
  src_proto_dir = os.path.join(tmp_dir, "proto-out/github.com/superpowerdotcom/fhir/go/proto/google")
  if os.path.exists(src_proto_dir):
    shutil.move(src_proto_dir, proto_dest_dir)

  accessor_out = os.path.join(
      dest_root, "go/jsonformat/internal/accessor/accessor_test_go_proto")
  shutil.rmtree(accessor_out, ignore_errors=True)
  
  src_accessor_dir = os.path.join(
      tmp_dir,
      "proto-out/github.com/superpowerdotcom/fhir/go/jsonformat/internal/accessor/accessor_test_go_proto"
  )
  if os.path.exists(src_accessor_dir):
    shutil.copytree(src_accessor_dir, accessor_out)

  protopath_dest_dir = os.path.join(
      dest_root, "go/protopath/protopathtest_go_proto")
  shutil.rmtree(protopath_dest_dir, ignore_errors=True)
  
  src_protopath_dir = os.path.join(
      tmp_dir,
      "proto-out/github.com/superpowerdotcom/fhir/go/protopath/protopathtest_go_proto"
  )
  if os.path.exists(src_protopath_dir):
    shutil.copytree(src_protopath_dir, protopath_dest_dir)


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")

  log("🚀 [generate_go_protos.py] Starting Go proto generation. This step may take a while. Errors will appear below if any.")

  start_time = time.time()
  tmp_dir = tempfile.mkdtemp(prefix="fhir-")
  repo_tmp_dir = os.path.join(tmp_dir, "repo")
  proto_out_dir = os.path.join(tmp_dir, "proto-out")

  # Copy repository to the tmp_dir for proto generation.
  log("🔧 [generate_go_protos.py] Copying repository to temp directory...")
  shutil.copytree(_REPO_PATH.value, repo_tmp_dir)

  # Add the correct go_package option to all the protos in the tmp_dir.
  log("🔧 [generate_go_protos.py] Adding go_package options to protos...")
  for dirpath, _, file_names in os.walk(repo_tmp_dir):
    for fn in file_names:
      if fn.endswith(".proto"):
        prefix = fn.split(".proto")[0]

        old_file_path = os.path.join(dirpath, fn)
        new_file_path = os.path.join(dirpath, fn + "_with_go_package")

        repo_relative_path = dirpath.split(repo_tmp_dir)[1]
        assert repo_relative_path[0] == "/"
        repo_relative_path = repo_relative_path[1:]

        has_go_package = False
        with open(old_file_path, "rt") as fin:
          with open(new_file_path, "wt") as fout:
            for line in fin:
              if line.startswith("option go_package = \""):
                has_go_package = True
              fout.write(line)
            if not has_go_package:
              fout.write(
                  "option go_package = \"github.com/superpowerdotcom/fhir/go/{}/{}_go_proto\";"
                  .format(repo_relative_path, prefix))

        # Remove the old file, and replace with the go_package modified file.
        os.remove(old_file_path)
        os.rename(new_file_path, old_file_path)

  # Run the protoc go generation commands
  log("🔧 [generate_go_protos.py] Running protoc to generate Go code...")
  if not os.path.exists(proto_out_dir):
    os.makedirs(proto_out_dir)
    
  proto_dir = os.path.join(repo_tmp_dir, "proto")
  if os.path.exists(proto_dir):
    os.system(
        r"find {0} -type f -name '*.proto' -exec protoc --proto_path={1} --go_out={2} {{}} \; "
        .format(proto_dir, repo_tmp_dir, proto_out_dir))
  
  go_proto_dir = os.path.join(repo_tmp_dir, "go")
  if os.path.exists(go_proto_dir):
    os.system(
        r"find {0} -type f -name '*.proto' -exec protoc --proto_path={1} --go_out={2} {{}} \; "
        .format(go_proto_dir, repo_tmp_dir, proto_out_dir))

  move_generated_go_protos(tmp_dir)
  
  # Clean up temp directory (ignore permission errors)
  log("🔧 [generate_go_protos.py] Moving generated files to final destination...")
  shutil.rmtree(tmp_dir, ignore_errors=True)

  end_time = time.time()
  elapsed = int(end_time - start_time)
  log(f"\n✅ [generate_go_protos.py] Go proto generation completed in {elapsed}s.")

if __name__ == "__main__":
  flags.mark_flag_as_required("repo-path")
  app.run(main)
