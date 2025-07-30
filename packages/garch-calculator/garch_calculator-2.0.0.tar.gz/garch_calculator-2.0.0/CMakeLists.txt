cmake_minimum_required(VERSION 3.12)
project(garch_calculator VERSION 1.0.0)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 编译选项
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG -march=native")
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -DDEBUG")

# 默认使用Release模式
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# 查找依赖包
find_package(Boost REQUIRED COMPONENTS system)

# 查找pybind11 - 使用多种方法
find_package(pybind11 QUIET)
if(NOT pybind11_FOUND)
    # 尝试通过pip安装的pybind11
    execute_process(
        COMMAND python3 -c "import pybind11; print(pybind11.get_cmake_dir())"
        OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ERROR_QUIET
    )
    if(PYBIND11_CMAKE_DIR)
        set(pybind11_DIR "${PYBIND11_CMAKE_DIR}")
        find_package(pybind11 REQUIRED)
    else()
        # 如果仍然找不到，提供友好的错误信息
        message(FATAL_ERROR "pybind11 not found. Please install it using: pip3 install pybind11")
    endif()
endif()

# 包含目录
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
include_directories(${Boost_INCLUDE_DIRS})

# 源文件
set(GARCH_SOURCES
    src/garch_calculator.cpp
)

# 头文件
set(GARCH_HEADERS
    include/garch_calculator.h
)

# 创建GARCH库 (静态库)
add_library(garch_static STATIC ${GARCH_SOURCES})
target_link_libraries(garch_static ${Boost_LIBRARIES})

# 创建GARCH库 (动态库)
add_library(garch_shared SHARED ${GARCH_SOURCES})
target_link_libraries(garch_shared ${Boost_LIBRARIES})

# 设置库的属性
set_target_properties(garch_static PROPERTIES OUTPUT_NAME garch)
set_target_properties(garch_shared PROPERTIES OUTPUT_NAME garch)

# Python绑定模块
pybind11_add_module(_garch_calculator 
    python/garch_bindings.cpp 
    ${GARCH_SOURCES}
)

# 设置Python模块属性
target_compile_definitions(_garch_calculator PRIVATE VERSION_INFO=${VERSION_INFO})
target_link_libraries(_garch_calculator PRIVATE ${Boost_LIBRARIES})

# 编译器特定选项
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(garch_static PRIVATE -Wall -Wextra -Wpedantic)
    target_compile_options(garch_shared PRIVATE -Wall -Wextra -Wpedantic)
    target_compile_options(_garch_calculator PRIVATE -Wall -Wextra -Wpedantic)
endif()

# 多线程支持
find_package(Threads REQUIRED)
target_link_libraries(garch_static Threads::Threads)
target_link_libraries(garch_shared Threads::Threads)
target_link_libraries(_garch_calculator PRIVATE Threads::Threads)

# 测试可执行文件
option(BUILD_TESTS "Build test programs" ON)
if(BUILD_TESTS)
    enable_testing()
    
    # 简单的C++测试
    add_executable(test_garch tests/test_garch.cpp)
    target_link_libraries(test_garch garch_static)
    add_test(NAME test_garch COMMAND test_garch)
endif()

# 安装目标
install(TARGETS garch_static garch_shared
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

install(FILES ${GARCH_HEADERS}
    DESTINATION include/garch
)

# 包配置已简化

# 显示配置信息
message(STATUS "GARCH Calculator Configuration:")
message(STATUS "  Version: ${PROJECT_VERSION}")
message(STATUS "  Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Boost Found: ${Boost_FOUND}")
message(STATUS "  Boost Version: ${Boost_VERSION}")
message(STATUS "  Build Tests: ${BUILD_TESTS}")