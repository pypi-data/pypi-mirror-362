function(generate_python_binding name target_to_bind)

    find_package(Python COMPONENTS Interpreter Development.Module)

    Include(FetchContent)
    FetchContent_Declare(
    PyBind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.13.6 # or a later release
    )
    FetchContent_MakeAvailable(PyBind11)

    message(STATUS "Creating binding for module ${name}")
    file(GLOB_RECURSE pybind_src_files "python_binding/*.cpp")

    pybind11_add_module(${name} MODULE ${pybind_src_files} "NO_EXTRAS") # NO EXTRA recquired for pip install
    target_include_directories(${name} PRIVATE "python_binding")

    # Link target library to bind
    target_link_libraries(${name} PRIVATE ${target_to_bind})

endfunction()
