cmake_minimum_required(VERSION 3.18)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS  OFF)

file(STRINGS "${CMAKE_SOURCE_DIR}/project_name.txt" project_name)
file(STRINGS "${CMAKE_SOURCE_DIR}/version.txt" version)

project(${project_name}
        VERSION ${version}
        DESCRIPTION "Export of aidge"
        LANGUAGES CXX)

message(STATUS "Project name: ${CMAKE_PROJECT_NAME}")
message(STATUS "Project version: ${version}")

# Note : project name is ${CMAKE_PROJECT_NAME} and python module name is also ${CMAKE_PROJECT_NAME}
set(module_name _${CMAKE_PROJECT_NAME}) # target name

##############################################
# Define options
option(PYBIND "python binding" ON)
option(STANDALONE "Build standalone executable" ON)
option(WERROR "Warning as error" OFF)
option(TEST "Enable tests" OFF)
option(COVERAGE "Enable coverage" OFF)
option(ENABLE_ASAN "Enable ASan (AddressSanitizer) for runtime analysis of memory use (over/underflow, memory leak, ...)" OFF)

##############################################
# Import utils CMakeLists
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake")

if(CMAKE_COMPILER_IS_GNUCXX AND COVERAGE)
    Include(CodeCoverage)
endif()

##############################################
# FIND Dependencies
if(NOT $ENV{AIDGE_INSTALL} STREQUAL "")
    set(CMAKE_INSTALL_PREFIX $ENV{AIDGE_INSTALL})
    list(APPEND CMAKE_PREFIX_PATH $ENV{AIDGE_INSTALL})
    message(WARNING "Env var AIDGE_INSTALL detected : $ENV{AIDGE_INSTALL}. Set CMAKE_INSTALL_PREFIX to AIDGE_INSTALL & added to CMAKE_PREFIX_PATH"
                    "\n\tCMAKE_INSTALL_PREFIX = ${CMAKE_INSTALL_PREFIX}"
                    "\n\tCMAKE_PREFIX_PATH = ${CMAKE_PREFIX_PATH}")
endif()
find_package(aidge_core REQUIRED)
# find_package(aidge_backend_cpu REQUIRED) # example if you want to add aidge_backend_cpu as dependency to your export

##############################################
# Create target and set properties
file(GLOB_RECURSE src_files "src/*.cpp")
file(GLOB_RECURSE inc_files "include/*.hpp")

add_library(${module_name} ${src_files} ${inc_files})

target_link_libraries(${module_name}
    PUBLIC
        _aidge_core # _ is added because we link the exported target and not the project
        # _aidge_backend_cpu # example if you want to add aidge_backend_cpu as dependency to your export
)

#Set target properties
set_property(TARGET ${module_name} PROPERTY POSITION_INDEPENDENT_CODE ON)

# PYTHON BINDING
if (PYBIND)
    include(PybindModuleCreation)
    generate_python_binding(${CMAKE_PROJECT_NAME} ${module_name})
endif()

if( ${ENABLE_ASAN} )
    message("Building ${module_name} with ASAN.")
    set(SANITIZE_FLAGS -fsanitize=address -fno-omit-frame-pointer)
    target_link_libraries(${module_name}
        PUBLIC
            -fsanitize=address
    )
    target_compile_options(${module_name}
        PRIVATE
            ${SANITIZE_FLAGS}
    )
endif()

target_include_directories(${module_name}
    PUBLIC
        $<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

target_compile_features(${module_name} PRIVATE cxx_std_14)

target_compile_options(${module_name} PRIVATE
    $<$<OR:$<CXX_COMPILER_ID:Clang>,$<CXX_COMPILER_ID:AppleClang>,$<CXX_COMPILER_ID:GNU>>:
    -Wall -Wextra -Wold-style-cast -Winline -pedantic -Werror=narrowing -Wshadow $<$<BOOL:${WERROR}>:-Werror>>)
target_compile_options(${module_name} PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:
    /W4>)

if(CMAKE_COMPILER_IS_GNUCXX AND COVERAGE)
    append_coverage_compiler_flags()
endif()

##############################################
# Installation instructions
include(GNUInstallDirs)
set(INSTALL_CONFIGDIR ${CMAKE_INSTALL_LIBDIR}/cmake/${CMAKE_PROJECT_NAME})

install(TARGETS ${module_name} EXPORT ${CMAKE_PROJECT_NAME}-targets
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

#Export the targets to a script
install(EXPORT ${CMAKE_PROJECT_NAME}-targets
 FILE "${CMAKE_PROJECT_NAME}-targets.cmake"
 DESTINATION ${INSTALL_CONFIGDIR}
 COMPONENT ${module_name}
)

#Create a ConfigVersion.cmake file
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}-config-version.cmake"
    VERSION ${version}
    COMPATIBILITY AnyNewerVersion
)

configure_package_config_file("${CMAKE_PROJECT_NAME}-config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}-config.cmake"
    INSTALL_DESTINATION ${INSTALL_CONFIGDIR}
)

#Install the config, configversion and custom find modules
install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}-config.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}-config-version.cmake"
    DESTINATION ${INSTALL_CONFIGDIR}
)

##############################################
## Exporting from the build tree
message(STATUS "Exporting created targets to use them in another build")
export(EXPORT ${CMAKE_PROJECT_NAME}-targets
    FILE "${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}-targets.cmake")

if(STANDALONE)
    if(AIDGE_REQUIRES_PYTHON AND NOT AIDGE_PYTHON_HAS_EMBED)
        message(WARNING "Skipping compilation of standalone executable: missing Python embedded interpreter")
    else()
        add_executable(main main.cpp)
        target_link_libraries(main PRIVATE ${module_name})
    endif()
endif()
