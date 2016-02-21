# This file is part of clcc package and is licensed under the Simplified BSD license.
#    See LICENSE.rst for the full text of the license.


from __future__ import print_function, absolute_import
import os
import sys
import argparse
import re
import ctypes


from .opencl import OpenCL
from .opencl import PLATFORM_NAME as CL_PLATFORM_NAME, \
    PLATFORM_PROFILE as CL_PLATFORM_PROFILE, \
    PLATFORM_VERSION as CL_PLATFORM_VERSION, \
    DEVICE_NAME as CL_DEVICE_NAME, \
    DEVICE_EXTENSIONS as CL_DEVICE_EXTENSIONS, \
    DEVICE_TYPE as CL_DEVICE_TYPE, \
    DEVICE_TYPE_CPU as CL_DEVICE_TYPE_CPU, \
    DEVICE_TYPE_GPU as CL_DEVICE_TYPE_GPU, \
    DEVICE_TYPE_ACCELERATOR as CL_DEVICE_TYPE_ACCELERATOR, \
    DEVICE_TYPE_CUSTOM as CL_DEVICE_TYPE_CUSTOM, \
    DEVICE_GFXIP_MAJOR_AMD as CL_DEVICE_GFXIP_MAJOR_AMD, \
    DEVICE_GFXIP_MINOR_AMD as CL_DEVICE_GFXIP_MINOR_AMD, \
    DEVICE_COMPUTE_CAPABILITY_MAJOR_NV as CL_DEVICE_COMPUTE_CAPABILITY_MAJOR_NV, \
    DEVICE_COMPUTE_CAPABILITY_MINOR_NV as CL_DEVICE_COMPUTE_CAPABILITY_MINOR_NV, \
    CONTEXT_PLATFORM as CL_CONTEXT_PLATFORM
from . import report


parser = argparse.ArgumentParser(description="OpenCL compiler")
parser.add_argument("-std", dest="standard", choices=["1.0", "1.1", "1.2", "2.0", "2.1"],
                    help="Target OpenCL standard version")
command_options = parser.add_mutually_exclusive_group()
list_option = command_options.add_argument(
    "-l", dest="command", action="store_const", const="list",
    help="List OpenCL platforms and devices")
compile_option = command_options.add_argument(
    "-c", dest="command", action="store_const", const="compile",
    help="Compile source code to binary object (OpenCL 1.2+)")
check_option = command_options.add_argument(
    "-fsyntax-only", dest="command", action="store_const", const="check",
    help="Build program and discard produced object")
assembler_option = command_options.add_argument(
    "-S", dest="command", action="store_const", const="assemble",
    help="Build program and produce assembly listing (AMD platform only)")
debug_option = parser.add_argument(
    "-g", dest="debug", action="store_true",
    help="Generate debug info (where applicable)")
platform_option = parser.add_argument(
    "-p", "--platform", dest="platform",
    help="Target OpenCL platform")
device_option = parser.add_argument(
    "-d", "--device", dest="device", default=1, type=int,
    help="Target OpenCL device")
include_option = parser.add_argument(
    "-I", dest="include", action="append",
    help="Include directory paths")
parser.add_argument(
    "-o", dest="output",
    help="Output file name (object file)")
parser.add_argument(
    "input", nargs="?",
    help="Input file name (source file)")
parser.set_defaults(command="build")


def list_devices(cl, min_standard):
    platform_name_map = {
        "AMD Accelerated Parallel Processing": "AMD",
        "NVIDIA CUDA": "nVidia",
        "Intel Gen OCL Driver": "Intel Beignet",
        "Intel(R) OpenCL": "Intel",
        "Apple": "Apple",
        "QUALCOMM Snapdragon(TM)": "Qualcomm",
        "ARM Platform": "ARM",
        "Portable Computing Language": "POCL"
    }
    platform_profile_map = {
        "FULL_PROFILE": "full profile",
        "EMBEDDED_PROFILE": "embedded profile"
    }
    device_type_map = {
        CL_DEVICE_TYPE_CPU: "CPU",
        CL_DEVICE_TYPE_GPU: "GPU",
        CL_DEVICE_TYPE_ACCELERATOR: "accelerator",
        CL_DEVICE_TYPE_CUSTOM: "custom"
    }
    gfxip_arch_map = {
        4: "VLIW5",
        5: "VLIW4",
        6: "GCN 1.0",
        7: "GCN 1.1",
        8: "GCN 1.2"
    }
    sm_arch_map = {
        1: "Tesla",
        2: "Fermi",
        3: "Kepler",
        5: "Maxwell",
        6: "Pascal",
        7: "Volta"
    }

    platforms = cl.get_platform_ids()
    if len(platforms) == 0:
        print("No OpenCL platforms found")
    else:
        for i, platform in enumerate(platforms):
            platform_name = cl.get_platform_info(platform, CL_PLATFORM_NAME)
            unified_platform_name = platform_name_map.get(platform_name, "Unknown (%s)" % platform_name)

            platform_profile = cl.get_platform_info(platform, CL_PLATFORM_PROFILE)
            unified_platform_profile = platform_profile_map.get(platform_profile, "unknown profile (%s)" % platform_profile)

            platform_version = cl.get_platform_info(platform, CL_PLATFORM_VERSION)
            platform_version_match = re.match(r"OpenCL (\d+\.\d+)", platform_version)
            if platform_version_match is not None:
                unified_platform_version = platform_version_match.group(0) + ", " + unified_platform_profile
                if min_standard is not None:
                    platform_standard = tuple(map(int, platform_version_match.group(1).split(".")))
                    if platform_standard < min_standard:
                        continue
            else:
                unified_platform_version = unified_platform_profile
                if min_standard is not None:
                    continue

            print("Platform #%d: %s [%s]" % (i + 1, unified_platform_name, unified_platform_version))

            devices = cl.get_platform_devices(platform)

            for j, device in enumerate(devices):
                device_type = cl.get_device_info(device, CL_DEVICE_TYPE, ctypes.c_uint64)
                unified_device_type = device_type_map.get(device_type, "unknown type (0x%X)" % device_type)

                device_name = cl.get_device_string_info(device, CL_DEVICE_NAME)
                unified_device_name = device_name

                device_extensions = cl.get_device_string_info(device, CL_DEVICE_EXTENSIONS).split(" ")
                if device_type == CL_DEVICE_TYPE_GPU:
                    if "cl_amd_device_attribute_query" in device_extensions:
                        device_gfxip_major = cl.get_device_info(device, CL_DEVICE_GFXIP_MAJOR_AMD, ctypes.c_uint32)
                        device_gfxip_minor = cl.get_device_info(device, CL_DEVICE_GFXIP_MINOR_AMD, ctypes.c_uint32)
                        if device_gfxip_major in gfxip_arch_map:
                            unified_device_name += " [GFXIP %d.%d; %s]" % (device_gfxip_major, device_gfxip_minor, gfxip_arch_map[device_gfxip_major])
                        else:
                            unified_device_name += " [GFXIP %d.%d]" % (device_gfxip_major, device_gfxip_minor)
                    elif "cl_nv_device_attribute_query" in device_extensions:
                        device_compute_capability_major = cl.get_device_info(device, CL_DEVICE_COMPUTE_CAPABILITY_MAJOR_NV, ctypes.c_uint32)
                        device_compute_capability_minor = cl.get_device_info(device, CL_DEVICE_COMPUTE_CAPABILITY_MINOR_NV, ctypes.c_uint32)
                        if device_compute_capability_major in sm_arch_map:
                            unified_device_name += " [SM %d.%d; %s]" % (device_compute_capability_major, device_compute_capability_minor, sm_arch_map[device_compute_capability_major])
                        else:
                            unified_device_name += " [SM %d.%d]" % (device_compute_capability_major, device_compute_capability_minor)

                print("\tDevice #%d [%s]: %s" % (j + 1, unified_device_type, unified_device_name))

                cl.release_device(device)


def select_platform(cl, target_platform):
    platforms = cl.get_platform_ids()
    if len(platforms) == 0:
        report.error("no OpenCL platforms found")
    elif target_platform is None:
        if len(platforms) == 1:
            return platforms[0]
        else:
            report.error("no target OpenCL platform specified")
    else:
        try:
            target_platform_id = int(target_platform)
            if target_platform_id <= 0:
                report.error("invalid platform value %s: positive number required (clcc -l to list platforms)" % target_platform)
            elif target_platform_id > len(platforms):
                report.error("invalid platform value %s: only %d OpenCL platforms are available (clcc -l to list platforms)" % (target_platform, len(platforms)))
            else:
                return platforms[target_platform_id - 1]
        except ValueError:
            platform_name_map = {
                "amd": "AMD Accelerated Parallel Processing",
                "AMD": "AMD Accelerated Parallel Processing",
                "intel": "Intel(R) OpenCL",
                "Intel": "Intel(R) OpenCL",
                "beignet": "Intel Gen OCL Driver",
                "Beignet": "Intel Gen OCL Driver",
                "nv": "NVIDIA CUDA",
                "nvidia": "NVIDIA CUDA",
                "nVidia": "NVIDIA CUDA",
                "apple": "Apple",
                "Apple": "Apple",
                "pocl": "Portable Computing Language",
                "POCL": "Portable Computing Language",
                "qcom": "QUALCOMM Snapdragon(TM)",
                "qualcomm": "QUALCOMM Snapdragon(TM)",
                "Qualcomm": "QUALCOMM Snapdragon(TM)",
                "arm": "ARM Platform",
                "ARM": "ARM Platform"
            }
            if target_platform in platform_name_map:
                target_platform_name = platform_name_map[target_platform]
                for platform in platforms:
                    platform_name = cl.get_platform_info(platform, CL_PLATFORM_NAME)
                    if platform_name == target_platform_name:
                        return platform
                else:
                    report.error("platform \"%s\" (%s) is not available" % (target_platform, target_platform_name))
            else:
                report.error("invalid platform name %s: use one of (amd, intel, beignet, nvidia, apple, pocl, qualcom, arm)" % target_platform)


def compile_code(cl, command, input_filename, output_filename, include_paths, debug_build, target_platform, device_id, standard):
    open_kwargs = {}
    if sys.version_info >= (3,):
        open_kwargs["encoding"] = "utf8"
    with open(input_filename, "r", **open_kwargs) as input_file:
        source_code = input_file.read()

    platform = select_platform(cl, target_platform)
    devices = cl.get_platform_devices(platform)
    device = devices[device_id - 1]
    for d in devices:
        if d is not device:
            cl.release_device(d)

    clflags = []
    if cl.get_platform_info(platform, CL_PLATFORM_NAME) == "AMD Accelerated Parallel Processing":
        if not debug_build:
            clflags += ["-fno-bin-source", "-fno-bin-llvmir", "-fno-bin-amdil"]

    if standard is not None:
        clflags += ["-cl-std=CL" + standard]
    for include_path in include_paths:
        clflags += ["-I" + include_path]

    context_properties = (ctypes.c_void_p * 4)()
    context_properties[0] = ctypes.cast(CL_CONTEXT_PLATFORM, ctypes.c_void_p)
    context_properties[1] = platform
    context = cl.create_context(context_properties, device)
    program = cl.create_program_with_source(context, source_code)
    if command == "build":
        status = cl.build_program(program, device, " ".join(clflags))
    else:
        status = cl.compile_program(program, device, " ".join(clflags))
    build_log = cl.get_program_build_log(program, device)
    if build_log:
        print(build_log)
    elif status != 0:
        print("Program build failed")

    if command == "check":
        if output_filename is not None:
            report.warning("option -o is ignored due to -fsyntax-only")
    else:
        binary = cl.get_program_binary(program)
        with open(output_filename, "wb") as output_file:
            output_file.write(binary)

    cl.release_context(context)
    cl.release_device(device)


def main(args=sys.argv[1:]):
    options = parser.parse_args(args)
    opencl_path = "OpenCL"
    if sys.platform == "darwin":
        opencl_path = "/Library/Frameworks/OpenCL.framework/OpenCL"
    elif sys.platform.startswith("linux"):
        opencl_path = "libOpenCL.so"
    elif sys.platform == "win32":
        opencl_path = "OpenCL.dll"

    cl = OpenCL(opencl_path)
    if options.command is "build" or options.command == "compile" or options.command == "check":
        compile_code(cl, options.command or "build", options.input, options.output, options.include, options.debug, options.platform, options.device,
            standard=options.standard)
    elif options.command == "list":
        min_standard = None if options.standard is None else tuple(map(int, options.standard.split(".")))
        list_devices(cl, min_standard)


if __name__ == "__main__":
    main()
