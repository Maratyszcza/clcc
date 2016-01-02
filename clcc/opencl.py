# This file is part of clcc package and is licensed under the Simplified BSD license.
#    See LICENSE.rst for the full text of the license.


from __future__ import print_function, absolute_import
from ctypes import CDLL, POINTER, c_int32, c_uint32, c_uint64, c_void_p, c_char_p, c_size_t, byref, pointer, create_string_buffer, cast, sizeof
import sys

from . import report


PLATFORM_PROFILE    = 0x0900
PLATFORM_VERSION    = 0x0901
PLATFORM_NAME       = 0x0902
PLATFORM_EXTENSIONS = 0x0904

DEVICE_TYPE                        = 0x1000
DEVICE_NAME                        = 0x102B
DEVICE_EXTENSIONS                  = 0x1030
DEVICE_COMPILER_AVAILABLE          = 0x1028
DEVICE_LINKER_AVAILABLE            = 0x103E
DEVICE_BUILT_IN_KERNELS            = 0x103F
DEVICE_GFXIP_MAJOR_AMD             = 0x404A
DEVICE_GFXIP_MINOR_AMD             = 0x404B
DEVICE_COMPUTE_CAPABILITY_MAJOR_NV = 0x4000
DEVICE_COMPUTE_CAPABILITY_MINOR_NV = 0x4001

CONTEXT_DEVICES     = 0x1081
CONTEXT_NUM_DEVICES = 0x1083

PROGRAM_BINARY_SIZES = 0x1165
PROGRAM_BINARIES     = 0x1166
PROGRAM_NUM_KERNELS  = 0x1167
PROGRAM_KERNEL_NAMES = 0x1168
PROGRAM_IL           = 0x1169

PROGRAM_BUILD_LOG    = 0x1183

CONTEXT_PLATFORM            = 0x1084
CONTEXT_OFFLINE_DEVICES_AMD = 0x403F

DEVICE_TYPE_DEFAULT     = 0x00000001
DEVICE_TYPE_CPU         = 0x00000002
DEVICE_TYPE_GPU         = 0x00000004
DEVICE_TYPE_ACCELERATOR = 0x00000008
DEVICE_TYPE_CUSTOM      = 0x00000010
DEVICE_TYPE_ALL         = 0xFFFFFFFF


class OpenCL:
    def __init__(self, library_path):
        try:
            self.library = CDLL(library_path)
        except:
            report.error("failed to load OpenCL library (%s)" % library_path)

        # cl_int clGetPlatformIDs(cl_uint, cl_platform_id*, cl_uint*)
        self._get_platform_ids = self.library.clGetPlatformIDs
        self._get_platform_ids.restype = c_int32
        self._get_platform_ids.argtype = [c_uint32, POINTER(c_void_p), POINTER(c_uint32)]

        # cl_int clGetPlatformInfo(cl_platform_id, cl_platform_info, size_t, void*, size_t*)
        self._get_platform_info = self.library.clGetPlatformInfo
        self._get_platform_info.restype = c_int32
        self._get_platform_info.argtype = [c_void_p, c_uint32, c_size_t, c_void_p, POINTER(c_size_t)]

        # cl_int clGetDeviceIDs(cl_platform_id, cl_device_type, cl_uint, cl_device_id*, cl_uint*)
        self._get_device_ids = self.library.clGetDeviceIDs
        self._get_device_ids.restype = c_int32
        self._get_device_ids.argtype = [c_void_p, c_uint64, c_uint32, POINTER(c_void_p), POINTER(c_uint32)]

        # cl_int clGetDeviceInfo(cl_device_id, cl_device_info, size_t, void*, size_t*)
        self._get_device_info = self.library.clGetDeviceInfo
        self._get_device_info.restype = c_int32
        self._get_device_info.argtype = [c_void_p, c_uint32, c_size_t, c_void_p, POINTER(c_size_t)]

        try:
            # cl_int clReleaseDevice(cl_device_id)
            self._release_device = self.library.clReleaseDevice
            self._release_device.restype = c_int32
            self._release_device.argtype = [c_void_p]
        except:
            self._release_device = None

        # cl_context clCreateContext(cl_context_properties*, cl_uint num_devices, const cl_device_id*, void (*)(const char*, const void*, size_t, void*), void*, cl_int*)
        self._create_context = self.library.clCreateContext
        self._create_context.restype = c_void_p
        self._create_context.argtype = [POINTER(c_void_p), c_uint32, POINTER(c_void_p), c_void_p, c_void_p, POINTER(c_int32)]

        # cl_context clCreateContextFromType(cl_context_properties*, cl_device_type, void (*)(const char*, const void*, size_t, void*), void*, cl_int*)
        self._create_context_from_type = self.library.clCreateContextFromType
        self._create_context_from_type.restype = c_void_p
        self._create_context_from_type.argtype = [POINTER(c_void_p), c_uint64, c_void_p, c_void_p, POINTER(c_int32)]

        # cl_int clGetContextInfo(cl_context, cl_context_info, size_t, void*, size_t)
        self._get_context_info = self.library.clGetContextInfo
        self._get_context_info.restype = c_int32
        self._get_context_info.argtype = [c_void_p, c_uint32, c_size_t, c_void_p, POINTER(c_size_t)]

        # cl_int clReleaseContext(cl_context)
        self.release_context = self.library.clReleaseContext
        self.release_context.restype = c_int32
        self.release_context.argtype = [c_void_p]

        # cl_program clCreateProgramWithSource(cl_context, cl_uint, const char**, const size_t*, cl_int*)
        self._create_program_with_source = self.library.clCreateProgramWithSource
        self._create_program_with_source.restype = c_void_p
        self._create_program_with_source.argtype = [c_void_p, c_uint32, POINTER(c_char_p), POINTER(c_size_t), POINTER(c_int32)]

        # cl_int clBuildProgram(cl_program, cl_uint, const cl_device_id*, const char*, void (*)(cl_program, void*), void*)
        self._build_program = self.library.clBuildProgram
        self._build_program.restype = c_int32
        self._build_program.argtype = [c_uint32, POINTER(c_void_p), c_char_p, c_void_p, c_void_p]

        try:
            # cl_int clCompileProgram(cl_program, cl_uint, const cl_device_id*, const char*, cl_uint, const cl_program*, const char**, void (*)(cl_program, void*), void*)
            self._compile_program = self.library.clCompileProgram
            self._compile_program.restype = c_int32
            self._compile_program.argtype = [c_void_p, c_uint32, POINTER(c_void_p), c_char_p, c_uint32, POINTER(c_void_p), POINTER(c_char_p), c_void_p, c_void_p]
        except:
            self._compile_program = None

        # cl_int clGetProgramBuildInfo(cl_program, cl_device_id, cl_program_build_info, size_t, void*, size_t*)
        self._get_program_build_info = self.library.clGetProgramBuildInfo
        self._get_program_build_info.restype = c_int32
        self._get_program_build_info.argtype = [c_void_p, c_void_p, c_uint32, c_size_t, c_void_p, POINTER(c_size_t)]

        # cl_int clGetProgramInfo(cl_program, cl_program_info, size_t, void*, size_t*)
        self._get_program_info = self.library.clGetProgramInfo
        self._get_program_info.restype = c_int32
        self._get_program_info.argtype = [c_void_p, c_uint32, c_size_t, c_void_p, POINTER(c_size_t)]

        # cl_int clReleaseProgram(cl_program)
        self.release_program = self.library.clReleaseProgram
        self.release_program.restype = c_int32
        self.release_program.argtype = [c_void_p]

    def get_platform_ids(self):
        platforms_count = c_uint32()
        status = self._get_platform_ids(0, None, byref(platforms_count))
        if status != 0:
            report.error("could not get the number of platforms", function="clGetPlatformIDs", cl_status=status)

        if platforms_count.value == 0:
            return tuple()
        else:
            platforms = (c_void_p * platforms_count.value)()
            status = self._get_platform_ids(platforms_count.value, platforms, None)
            if status != 0:
                report.error("could not get platform IDs", function="clGetPlatformIDs", cl_status=status)
            return tuple(c_void_p(platform) for platform in platforms)

    def get_platform_info(self, platform, info_type):
        info_size = c_size_t()
        status = self._get_platform_info(platform, info_type, 0, None, byref(info_size))
        if status == 0:
            info = create_string_buffer(info_size.value + 1)
            status = self._get_platform_info(platform, info_type, info_size.value, info, None)

        if status != 0:
            report.error("could not get platform info", function="clGetPlatformInfo", cl_status=status)

        if sys.version_info >= (3,):
            # Python 3: str and bytes are different types
            return str(info.value, "ascii")
        else:
            return info.value

    def get_device_ids(self, platform, device_type=DEVICE_TYPE_ALL):
        devices_count = c_uint32()
        status = self._get_device_ids(platform, device_type, 0, None, byref(devices_count))
        if status != 0:
            report.error("could not get the number of devices", function="clGetDeviceIDs", cl_status=status)

        if devices_count.value == 0:
            return tuple()
        else:
            devices = (c_void_p * devices_count.value)()
            status = self._get_device_ids(platform, device_type, devices_count.value, devices, None)
            if status != 0:
                report.error("could not get device IDs", function="clGetDeviceIDs", cl_status=status)
            return tuple(c_void_p(device) for device in devices)

    def get_device_string_info(self, device, info_id):
        info_size = c_size_t()
        status = self._get_device_info(device, info_id, 0, None, byref(info_size))
        if status == 0:
            info = create_string_buffer(info_size.value + 1)
            status = self._get_device_info(device, info_id, info_size.value, info, None)

        if status != 0:
            report.error("could not get device info", function="clGetDeviceInfo", cl_status=status)

        if sys.version_info >= (3,):
            # Python 3: str and bytes are different types
            return str(info.value, "ascii")
        else:
            return info.value

    def get_device_info(self, device, info_id, info_type):
        info = info_type()
        status = self._get_device_info(device, info_id, sizeof(info_type), byref(info), None)
        if status != 0:
            report.error("could not get device info", function="clGetDeviceInfo", cl_status=status)
        return info.value

    def release_device(self, device):
        if self._release_device:
            status = self._release_device(device)
            if status != 0:
                report.Warning("could not release device object", function="clReleaseDevice", cl_status=status)

    def create_context(self, context_properties, device):
        status = c_int32()
        context = self._create_context(context_properties, 1, byref(device), None, None, byref(status))
        if status.value != 0:
            report.error("could not create context", function="clCreateContext", cl_status=status.value)
        return context

    def create_context_from_type(self, context_properties, device_type=DEVICE_TYPE_ALL):
        status = c_int32()
        context = self._create_context_from_type(context_properties, device_type, None, None, byref(status))
        if status.value != 0:
            report.error("could not create context", function="clCreateContextFromType", cl_status=status.value)
        return context

    def get_context_devices(self, context):
        devices_count = c_uint32()
        status = self._get_context_info(context, CONTEXT_NUM_DEVICES, sizeof(devices_count), byref(devices_count), None)
        if status != 0:
            report.error("could not get the number of devices in a context", function="clGetContextInfo", cl_status=status)

        if devices_count.value == 0:
            return tuple()

        devices = (c_void_p * devices_count.value)()
        status = self._get_context_info(context, CONTEXT_DEVICES, sizeof(devices), devices, None)
        if status != 0:
            report.error("could not get the list of devices in a context", function="clGetContextInfo", cl_status=status)

        return tuple(c_void_p(device) for device in devices)

    def get_platform_devices(self, platform, device_type=DEVICE_TYPE_ALL, online_only=False):
        platform_extensions = self.get_platform_info(platform, PLATFORM_EXTENSIONS).split(" ")
        if not online_only and "cl_amd_offline_devices" in platform_extensions:
            context_properties = (c_void_p * 6)()
            context_properties[0] = cast(CONTEXT_PLATFORM, c_void_p)
            context_properties[1] = platform
            context_properties[2] = cast(CONTEXT_OFFLINE_DEVICES_AMD, c_void_p)
            context_properties[3] = cast(1, c_void_p)
            context = self.create_context_from_type(context_properties)
            devices = self.get_context_devices(context)
            self.release_context(context)
            return devices
        else:
            return self.get_device_ids(platform)

    def create_program_with_source(self, context, code):
        code_pointer = c_char_p(code)
        status = c_int32()
        program = self._create_program_with_source(context, 1, pointer(code_pointer), None, byref(status))
        if status.value != 0:
            report.error("could not create program", function="clCreateProgramWithSource", cl_status=status.value)
        return program

    def build_program(self, program, device, options):
        return self._build_program(program, 1, byref(device), c_char_p(options), None, None)

    def compile_program(self, program, device, options):
        return self._compile_program(program, 1, byref(device), c_char_p(options), 0, None, None, None, None)

    def get_program_binary(self, program):
        binary_size = c_size_t()
        status = self._get_program_info(program, PROGRAM_BINARY_SIZES, sizeof(binary_size), byref(binary_size), None)
        if status != 0:
            report.error("could not get program binary size", function="clGetProgramInfo", cl_status=status)

        binary = create_string_buffer(binary_size.value)
        binary_pointer = cast(binary, c_void_p)
        status = self._get_program_info(program, PROGRAM_BINARIES, sizeof(binary_pointer), byref(binary_pointer), None)
        if status != 0:
            report.error("could not get program binary", function="clGetProgramInfo", cl_status=status)

        return bytearray(binary.raw)

    def get_program_build_log(self, program, device):
        log_size = c_size_t()
        status = self._get_program_build_info(program, device, PROGRAM_BUILD_LOG, 0, None, byref(log_size))
        if status == 0:
            log_data = create_string_buffer(log_size.value + 1)
            status = self._get_program_build_info(program, device, PROGRAM_BUILD_LOG, log_size.value, log_data, None)

        if status != 0:
            report.error("could not get program build log", function="clGetProgramBuildInfo", cl_status=status)

        if sys.version_info >= (3,):
            # Python 3: str and bytes are different types
            return str(log_data.value, "utf8")
        else:
            return log_data.value
