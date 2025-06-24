package(default_visibility = ["//visibility:public"])

licenses(["notice"])

load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "generate_go_protos",
    srcs = ["generate_go_protos.py"],
    main = "generate_go_protos.py",
    python_version = "PY3",
    visibility = ["//visibility:public"],
    deps = [
        "@abseil-py//absl:app",
        "@abseil-py//absl/flags",
    ],
) 