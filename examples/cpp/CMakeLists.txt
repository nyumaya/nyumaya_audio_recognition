cmake_minimum_required (VERSION 2.8.11)

project (nyumaya_example)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

LINK_DIRECTORIES(../../lib/linux_x86_64)
find_library(NYUMAYA_LIB NAMES libnyumaya_premium.so.3.0.0 PATHS ../../lib/linux_x86_64)


add_executable (arecord_sample arecord_sample.cpp)
add_executable (dummy_sample dummy_sample.cpp )


TARGET_LINK_LIBRARIES(dummy_sample  ${NYUMAYA_LIB} ${CMAKE_THREAD_LIBS_INIT} ${CMAKE_DL_LIBS})
TARGET_LINK_LIBRARIES(arecord_sample  ${NYUMAYA_LIB}  asound ${CMAKE_THREAD_LIBS_INIT} ${CMAKE_DL_LIBS})


target_include_directories(dummy_sample
	PUBLIC ../../include
)

target_include_directories(arecord_sample
	PUBLIC ../../include
)
