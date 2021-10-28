cmake_minimum_required (VERSION 2.6)


################################
# Options
################################

option(Tests "Tests" OFF)
option(CrossCompile32 "CrossCompile32" OFF)
option(CrossCompile64 "CrossCompile64" OFF)

################################
# Cross Compiling
################################

if(CrossCompile32 OR CrossCompile64)
  SET(CMAKE_SYSTEM_NAME Windows)
  set(COMPILER_PREFIX "i686-w64-mingw32")
  if(CrossCompile64)
    set(COMPILER_PREFIX "x86_64-w64-mingw32")
  endif()
  find_program(CMAKE_RC_COMPILER NAMES ${COMPILER_PREFIX}-windres)
  SET(CMAKE_RC_COMPILER ${COMPILER_PREFIX}-windres)
  find_program(CMAKE_C_COMPILER NAMES ${COMPILER_PREFIX}-gcc)
  SET(CMAKE_C_COMPILER ${COMPILER_PREFIX}-gcc)
  find_program(CMAKE_CXX_COMPILER NAMES ${COMPILER_PREFIX}-g++)
  SET(CMAKE_CXX_COMPILER ${COMPILER_PREFIX}-g++)

  set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
  set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
  set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

endif()

################################
# Project
################################

#project (FMI)
project (fmuNoMASS)

SET( SRC
Source/Agents/Agent.cpp
Source/Occupants/Occupant.cpp
Source/Occupants/Occupant_Action.cpp
Source/Occupants/Occupant_Action_Heat_Gains.cpp
Source/Occupants/Occupant_Action_Lights.cpp
Source/Occupants/Occupant_Action_Lights_BDI.cpp
Source/Occupants/Occupant_Action_Shades.cpp
Source/Occupants/Occupant_Action_Shades_BDI.cpp
Source/Occupants/Occupant_Action_Window.cpp
Source/Occupants/Occupant_Action_Window_Stochastic.cpp
Source/Occupants/Occupant_Action_Window_Stochastic_BDI.cpp
Source/Occupants/Occupant_Action_Window_Learning.cpp
Source/Occupants/Occupant_Action_Appliance.cpp
Source/Occupants/Occupant_Action_Appliance_BDI.cpp
Source/Occupants/Occupant_Action_HeatingSetPoints_Learning.cpp
Source/Occupants/Occupant_Zone.cpp
Source/DataStore/DataStore.cpp
Source/Log/Log.cpp
Source/Models/Model_Activity.cpp
Source/Models/Model_Activity_Survival.cpp
Source/Models/Model_ExternalShading.cpp
Source/Models/Model_HeatGains.cpp
Source/Models/Model_Lights.cpp
Source/Models/Model_Presence.cpp
Source/Models/Model_RandomWeibull.cpp
Source/Models/Model_Windows.cpp
Source/Models/Model_Appliance_Ownership.cpp
Source/Models/Model_Appliance_Large_Usage.cpp
Source/Models/Model_Appliance_Large_Usage_Survival.cpp
Source/Models/Model_Appliance_Small_Usage.cpp
Source/Models/Model_Appliance_Power_CSV.cpp
Source/Simulation/Simulation.cpp
Source/Configuration/Configuration.cpp
Source/Simulation/SimulationTime.cpp
Source/Simulation/State.cpp
Source/Simulation/StateMachine.cpp
Source/Utility/Utility.cpp
Source/Environment/Environment.cpp
Source/Building/Building.cpp
Source/Building/Building_Zone.cpp
Source/Building/Building_Appliances.cpp
Source/fmi/fmiFunctions.cpp
Source/QLearning/QLearning.cpp
Source/Appliances/Appliance.cpp
Source/Appliances/Appliance_Large.cpp
Source/Appliances/Appliance_Large_CSV.cpp
Source/Appliances/Appliance_Small.cpp
Source/Appliances/Appliance_Generic_CSV.cpp
Source/Appliances/Appliance_FMI.cpp
Source/Appliances/Appliance_Large_Learning.cpp
Source/Appliances/Appliance_Large_Learning_CSV.cpp
Source/Appliances/Appliance_Battery.cpp
Source/Appliances/Appliance_Battery_GridCost_Reward.cpp
Source/LVN/LVN.cpp
Source/LVN/LVN_Node.cpp
Source/Contract/Contract_Node_Priority.cpp
Source/Contract/Contract_Node_Supply.cpp
Source/Contract/Contract_Negotiation.cpp
Source/Version/Version.hpp
)

include_directories(${PROJECT_SOURCE_DIR}/Source)

ADD_LIBRARY(NoMASSstatic STATIC ${SRC})

ADD_LIBRARY(fmuNoMASS SHARED Source/fmi/fmuTemplate.cpp)
target_link_libraries(fmuNoMASS NoMASSstatic)

add_executable(NoMASS Source/main.cpp)
target_link_libraries(NoMASS NoMASSstatic)

if(UNIX OR APPLE)
  set_source_files_properties(${SRC} PROPERTIES COMPILE_FLAGS "-Werror -Wall -Wextra")
  SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -fPIC")
elseif(WIN32)
  SET( CMAKE_CXX_CREATE_SHARED_LIBRARY  "${CMAKE_CXX_CREATE_SHARED_LIBRARY} -static -fPIC" )
endif()

SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -std=c++11")



include_directories("${CMAKE_CURRENT_BINARY_DIR}")

################################
# Testing
################################
if (Tests)
 add_subdirectory(tests)
endif()
