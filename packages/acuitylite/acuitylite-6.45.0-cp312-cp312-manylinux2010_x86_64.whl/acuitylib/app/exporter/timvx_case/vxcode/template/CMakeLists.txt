cmake_minimum_required (VERSION 3.14)

#TIM_VX_DIR= pwd/tim-vx/build/install
#VIVANTE_SDK_DIR= pwd/tim-vx/prebuilt-sdk/x86_64_linux/

set(TIM_VX_DIR "$ENV{TIM_VX_DIR}")
set(PKG_NAME "$ENV{VIVIANTE_SDK_DIR}")

message(STATUS "TIM_VX_DIR: ${TIM_VX_DIR}")
message(STATUS "VIVIANTE_SDK_DIR : ${PKG_NAME}")
if(NOT DEFINED APP_TARGET_NAME)
    set(APP_TARGET_NAME "#NETWORK_NAME_LOWER#")
endif()
message(STATUS "APP_TARGET_NAME : ${APP_TARGET_NAME}")

project(${APP_TARGET_NAME} LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")

include_directories(${TIM_VX_DIR}/include)
include_directories(${TIM_VX_DIR}/src/tim/vx/internal/include)

find_library(TIM_VX_LIB tim-vx PATHS ${TIM_VX_DIR}/lib)
message(STATUS "Found lib tim-vx at ${TIM_VX_LIB}")

set(${PKG_NAME}_LIBRARIES)
set(LIBS CLC GAL OpenVX OpenVXC OpenVXU VSC ArchModelSw NNArchPerf vdtproxy)
list(LENGTH LIBS count)
math(EXPR count "${count} - 1")
foreach(i RANGE ${count})
    list(GET LIBS ${i} lib)
    find_library(${PKG_NAME}_FOUND_LIB_${i}
        NAMES ${lib}
        PATHS ${PKG_NAME}/lib
    )
    message(STATUS "Found lib ${lib} at ${${PKG_NAME}_FOUND_LIB_${i}}")
    list(APPEND ${PKG_NAME}_LIBRARIES ${${PKG_NAME}_FOUND_LIB_${i}})
endforeach()
message(STATUS "${PKG_NAME}_LIBRARIES is: \n ${${PKG_NAME}_LIBRARIES}")

set(${APP_TARGET_NAME}_sources)
list(APPEND ${APP_TARGET_NAME}_sources
    main.cc
    vx_utils.cc
    vx_utils.h
    vx_model.cc
    vx_model.h
    )

add_executable(${APP_TARGET_NAME} ${${APP_TARGET_NAME}_sources})

target_link_libraries(${APP_TARGET_NAME} ${TIM_VX_LIB} ${${PKG_NAME}_LIBRARIES})
