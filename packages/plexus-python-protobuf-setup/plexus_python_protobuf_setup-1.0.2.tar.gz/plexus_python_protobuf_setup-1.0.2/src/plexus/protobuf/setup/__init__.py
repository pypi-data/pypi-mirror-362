import importlib.metadata
from os import PathLike
from typing import Iterable

try:
    __version__ = importlib.metadata.version("plexus-python-protobuf-setup")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


def compile_protos(
    out_dir: str | PathLike[str],
    proto_dirs: Iterable[str | PathLike[str]],
    include_dirs: Iterable[str | PathLike[str]],
    *,
    descriptor_path: str | PathLike[str] | None = None,
    with_grpc: bool = False,
) -> None:
    """
    Compiles .proto files in the specified directory

    :param out_dir: Directory where the compiled files will be placed.
    :param proto_dirs: Directories containing .proto files which are used for generating target source codes
    :param include_dirs: Directories containing .proto files which are used only in compiling
    :param descriptor_path: Optional path to output the descriptor set file.
    :param with_grpc: If True, also generates gRPC Python code.
    :raises FileNotFoundError: If the proto directory does not exist.
    """
    import glob
    import os
    import subprocess
    import sys

    proto_files = []
    for proto_dir in proto_dirs:
        if not os.path.exists(proto_dir):
            raise FileNotFoundError(f"proto directory '{proto_dir}' does not exist")
        proto_files.extend(glob.glob(os.path.join(proto_dir, "**", "*.proto"), recursive=True))

    if not proto_files:
        print("No .proto files found")
        return

    cmd = [sys.executable, "-m", "grpc_tools.protoc"]

    for include_dir in include_dirs:
        if not os.path.exists(include_dir):
            raise FileNotFoundError(f"include directory '{include_dir}' does not exist")
        cmd.extend(("--proto_path", include_dir))

    cmd.extend(("--python_out", out_dir))
    cmd.extend(("--pyi_out", out_dir))
    if with_grpc:
        cmd.extend(("--grpc_python_out", out_dir))

    if descriptor_path:
        cmd.extend(("--descriptor_set_out",
                    descriptor_path,
                    "--include_imports",
                    "--include_source_info",
                    "--retain_options",
                    ))
    cmd.extend(proto_files)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    subprocess.check_call(cmd)
