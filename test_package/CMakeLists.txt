cmake_minimum_required(VERSION 2.8.12)
project(PackageTest C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if (UNIX)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra")
    set(CMAKE_BUILD_WITH_INSTALL_RPATH ON)
    if (APPLE)
        set(CMAKE_INSTALL_RPATH "@executable_path/../lib")
    else ()
        set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")
    endif ()
endif ()

find_package(EXPAT REQUIRED)

add_executable(example example.c)
target_link_libraries(example PRIVATE ${EXPAT_LIBRARY})
target_include_directories(example PRIVATE ${EXPAT_INCLUDE_DIRS})
target_compile_definitions(example PRIVATE "-DXML_STATIC")
