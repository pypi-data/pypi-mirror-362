cmake_minimum_required(VERSION 3.15)
project(cbits LANGUAGES C)

include(CheckCCompilerFlag)

set(MODULE_NAME "_cbits")

if(DEFINED ENV{VIRTUAL_ENV})
	message(STATUS "Using Python from VIRTUAL_ENV=$ENV{VIRTUAL_ENV}")
	set(Python_ROOT_DIR "$ENV{VIRTUAL_ENV}")
	set(Python_FIND_STRATEGY LOCATION)
endif()

if(APPLE)
	set(Python_FIND_FRAMEWORK NEVER)
endif()

find_package(Python
	COMPONENTS Interpreter Development.Module
	REQUIRED
)

message(STATUS "Found Python ${Python_VERSION_STRING}")
message(STATUS "  Executable: ${Python_EXECUTABLE}")
message(STATUS "  Include dir: ${Python_INCLUDE_DIRS}")
message(STATUS "  Libraries: ${Python_LIBRARIES}")
message(STATUS "  Module ext: ${Python_MODULE_EXTENSION}")

add_library(${MODULE_NAME} MODULE
	src/bitvector.c
	src/compat_dispatch.c
	python/binding.c
)

set_target_properties(${MODULE_NAME} PROPERTIES
	PREFIX ""
)

target_include_directories(${MODULE_NAME}
	PRIVATE
		${Python_INCLUDE_DIRS}
		${CMAKE_SOURCE_DIR}/include
)

target_link_libraries(${MODULE_NAME}
	PRIVATE
		Python::Module
)

if (MSVC)
	if(CMAKE_SIZEOF_VOID_P EQUAL 8)
		target_compile_options(_cbits PRIVATE /O2 /arch:AVX2)
		target_compile_definitions(_cbits PRIVATE
			__AVX2__=1
		)
		check_c_compiler_flag("/arch:AVX512VPOPCNTDQ" HAS_AVX512VPOPCNTDQ)
		if(HAS_AVX512VPOPCNTDQ)
			target_compile_options(_cbits PRIVATE /arch:AVX512VPOPCNTDQ)
			target_compile_definitions(_cbits PRIVATE __AVX512VPOPCNTDQ__=1)
		endif()
	else()
		target_compile_options(_cbits PRIVATE /O2)
	endif()
	set_target_properties(${MODULE_NAME} PROPERTIES SUFFIX ".pyd")
else()
	if(CMAKE_OSX_ARCHITECTURES STREQUAL "x86_64" OR CMAKE_SYSTEM_PROCESSOR STREQUAL "x86_64")
		target_compile_definitions(${MODULE_NAME} PRIVATE USE_X86_INTRINSIC)
		target_compile_options(${MODULE_NAME} PRIVATE
			-O3 -funroll-loops -mavx2 -mavx512vpopcntdq
		)
	else()
		target_compile_options(${MODULE_NAME} PRIVATE -O3)
	endif()
	set_target_properties(${MODULE_NAME} PROPERTIES SUFFIX ".so")
endif()


install(TARGETS ${MODULE_NAME}
	LIBRARY DESTINATION cbits
	RUNTIME DESTINATION cbits
	ARCHIVE DESTINATION cbits
)

install(FILES ${CMAKE_SOURCE_DIR}/python/cbits/__init__.py
	DESTINATION cbits
)