cmake_minimum_required(VERSION 3.0.0)
project(curium VERSION 0.1.0)

include(CTest)
enable_testing()

add_executable(curium main.cpp curium/opcodes.cpp curium/assemble.cpp)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)


add_compile_definitions(VERSION_MAJOR=0 VERSION_MINOR=0 VERSION_PATCH=0)