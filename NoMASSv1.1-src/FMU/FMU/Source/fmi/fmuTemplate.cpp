// Copyright 2015
/* ---------------------------------------------------------------------------*
 * Implementation of the FMI interface based on functions and macros to
 * be defined by the includer of this file.
 * If FMI_COSIMULATION is defined, this implements "FMI for Co-Simulation 1.0",
 * otherwise "FMI for Model Exchange 1.0".
 * The "FMI for Co-Simulation 1.0", implementation assumes that exactly the
 * following capability flags are set to fmiTrue:
 *    canHandleVariableCommunicationStepSize, i.e. fmiDoStep step size can vary
 *    canHandleEvents, i.e. fmiDoStep step size can be zero
 * and all other capability flags are set to default, i.e. to fmiFalse or 0.
 *
 * Revision history
 *  07.02.2010 initial version for "Model Exchange 1.0" released in FMU SDK 1.0
 *  05.03.2010 bug fix: fmiSetString now copies the passed string argument
 *     and fmiFreeModelInstance frees all string copies
 *  11.12.2010 replaced calloc by functions.allocateMemory in fmiInstantiateModel
 *  04.08.2011 added support for "FMI for Co-Simulation 1.0"
 *
 * (c) 2011 QTronic GmbH
 * ---------------------------------------------------------------------------*/


#include <iterator>
#include <vector>
#include <string>
#include <cstring>
#include <cstddef>

#include <assert.h>

#include <memory>

#include <RapidXML/rapidxml_utils.hpp>
#include <RapidXML/rapidxml.hpp>
#include <Log/Log.hpp>
#include <DataStore/DataStore.hpp>
#include <Simulation/Simulation.hpp>
#include <Configuration/Configuration.hpp>

#include "fmuTemplate.hpp"
#include "fmiPlatformTypes.hpp"
//daps8.8.2018 --> unix #include <unistd.h>
//daps8.8.2018 --> windows #include <io.h>
//#ifdef __linux__
//	#include <unistd.h>
//#elif _WIN32
//	#include <io.h>
//#else
//#endif
#if defined(unix)        || defined(__unix)      || defined(__unix__) \
 || defined(linux)       || defined(__linux)     || defined(__linux__) \
 || defined(__CYGWIN__)
    #include <unistd.h>
#elif defined(_MSC_VER) || defined(WIN32)  || defined(_WIN32) || defined(__WIN32__) \
   || defined(WIN64)    || defined(_WIN64) || defined(__WIN64__)
    #include <io.h>
#else

#endif

// array of value references of states
#if NUMBER_OF_REALS > 0
// Linux: declare vrStates to be static so that we get the local definition.
static fmiValueReference vrStates[NUMBER_OF_STATES] = STATES;
#endif

#ifndef max
#define max(a, b) ((a) > (b) ? (a) : (b))
#endif

// ---------------------------------------------------------------------------
// Private helpers used below to implement functions
// ---------------------------------------------------------------------------

// fname is fmiInstantiateModel or fmiInstantiateSlave
static fmiComponent instantiateModel(const char* fname, fmiString instanceName,
                                     fmiString GUID, fmiCallbackFunctions functions, fmiBoolean loggingOn)
    {
    //LOG << "   ** No-MASS ** " << "instantiating Model " << Utility::getTime() << "\n";
    DataStore::clearValues();

    Configuration::setStepCount(-1);
    //ERROR("break after setStepCount(-1)");
    if (valToRefs.empty())
        {
        RESETLOG;
        //LOG << "Instance Name: " << instanceName << "\n";
        LOG << "GUID: " << GUID << "\n";
        //LOG << "Config.EnergyPlus version: " << Configuration::info.eplusVersion << "\n";
        //LOG << "FMU Location = " << fmuLocation << "\n";
        //LOG << "fmiInstantiateSlave.mimeType=[" << mimeType << "]\n";
        //LOG << "fmiInstantiateSlave.timeout=[" << timeout << "]\n";
        //LOG << "fmiInstantiateSlave.visible=[" << static_cast<int>(visible) << "]\n";
        //LOG << "fmiInstantiateSlave.interactive=[" << static_cast<int>(interactive) << "]\n";
        //LOG << "fmiInstantiateSlave.loggingOn=[" << static_cast<int>(loggingOn) << "]\n";
        //LOG << "fmiInstantiateSlave.Configuration::RunLocation=[" << fmuLocation << "]\n";


        LOG << "Instantiating Model: " << instanceName << " [" << Utility::getTime() << "]\n";
        loadVariables();
        modelInstance->sim.preprocess();
        }
    return modelInstance.get();
    }

fmiComponent fmiInstantiateModel(fmiString instanceName, fmiString GUID,
                                 fmiCallbackFunctions functions, fmiBoolean loggingOn)
    {
    return instantiateModel("", instanceName, GUID, functions, loggingOn);
    }

// fname is fmiInitialize or fmiInitializeSlave

fmiStatus fmiInitialize(fmiComponent c, fmiBoolean toleranceControlled,
                        fmiReal relativeTolerance, fmiEventInfo* eventInfo)
    {
    if (LOG.getError())
        {
        return fmiError;
        }
    return fmiOK;
    }

// fname is fmiTerminate or fmiTerminateSlave
static fmiStatus terminate(const char* fname, fmiComponent c)
    {
    LOG << "Terminating... [" << Utility::getTime() << "]\n";
    LOG.printLog();
    return fmiOK;
    }

// fname is freeModelInstance of freeSlaveInstance
void freeInstance(char* fname, fmiComponent c)
    {
    }

// ---------------------------------------------------------------------------
// FMI functions: class methods not depending of a specific model instance
// ---------------------------------------------------------------------------

const char* fmiGetVersion()
    {
    return fmiVersion;
    }

// ---------------------------------------------------------------------------
// FMI functions: for FMI Model Exchange 1.0 and for FMI Co-Simulation 1.0
// logging control, setters and getters for Real, Integer, Boolean, String
// ---------------------------------------------------------------------------

fmiStatus fmiSetDebugLogging(fmiComponent c, fmiBoolean loggingOn)
    {
    return fmiOK;
    }

fmiStatus fmiSetReal(fmiComponent c, const fmiValueReference vr[],
                     size_t nvr, const fmiReal value[])
    {
    for (unsigned int i = 0; i < nvr; i++)
        {
        DataStore::addValueS(valToRefs.at(vr[i]), value[i]);
        }
    if (LOG.getError())
        {
        return fmiError;
        }
    return fmiOK;
    }

fmiStatus fmiSetInteger(fmiComponent c, const fmiValueReference vr[],
                        size_t nvr, const fmiInteger value[])
    {
    return fmiOK;
    }

fmiStatus fmiSetBoolean(fmiComponent c, const fmiValueReference vr[],
                        size_t nvr, const fmiBoolean value[])
    {
    return fmiOK;
    }

fmiStatus fmiSetString(fmiComponent c, const fmiValueReference vr[],
                       size_t nvr, const fmiString value[])
    {
    return fmiOK;
    }

fmiStatus fmiGetReal(fmiComponent c, const fmiValueReference vr[],
                     size_t nvr, fmiReal value[])
    {
    for (unsigned int i = 0; i < nvr; i++)
        {
        value[i] = DataStore::getValueS(valToRefs.at(vr[i]));
        }
    if (LOG.getError())
        {
        return fmiError;
        }
    return fmiOK;
    }

fmiStatus fmiGetInteger(fmiComponent c, const fmiValueReference vr[],
                        size_t nvr, fmiInteger value[])
    {
    return fmiOK;
    }

fmiStatus fmiGetBoolean(fmiComponent c, const fmiValueReference vr[],
                        size_t nvr, fmiBoolean value[])
    {
    return fmiOK;
    }

fmiStatus fmiGetString(fmiComponent c, const fmiValueReference vr[],
                       size_t nvr, fmiString  value[])
    {
    return fmiOK;
    }

// ---------------------------------------------------------------------------
// FMI functions: only for FMI Co-Simulation 1.0
// ---------------------------------------------------------------------------

const char* fmiGetTypesPlatform()
    {
    return fmiPlatform;
    }

fmiComponent fmiInstantiateSlave(fmiString  instanceName, fmiString  GUID,
                                 fmiString  fmuLocation, fmiString  mimeType, fmiReal timeout,
                                 fmiBoolean visible, fmiBoolean interactive, fmiCallbackFunctions functions,
                                 fmiBoolean loggingOn)
    {
    // ignoring arguments: fmuLocation, mimeType, timeout, visible, interactive
    //RESETLOG;
    LOG << "Instantiating Slave [" << Utility::getTime() << "]\n";
    //LOG << "fmiInstantiateSlave.instanceName=[" << instanceName << "]\n";
    //LOG << "fmiInstantiateSlave.GUID=[" << GUID << "]\n";
    //LOG << "fmiInstantiateSlave.fmuLocation=[" << fmuLocation << "]\n";
    //LOG << "fmiInstantiateSlave.mimeType=[" << mimeType << "]\n";
    //LOG << "fmiInstantiateSlave.timeout=[" << timeout << "]\n";
    //LOG << "fmiInstantiateSlave.visible=[" << static_cast<int>(visible) << "]\n";
    //LOG << "fmiInstantiateSlave.interactive=[" << static_cast<int>(interactive) << "]\n";
    //LOG << "fmiInstantiateSlave.loggingOn=[" << static_cast<int>(loggingOn) << "]\n";
    //LOG << "fmiInstantiateSlave.Configuration::RunLocation=[" << fmuLocation << "]\n";
    LOG.printLog();

    Configuration::RunLocation = fmuLocation;
    Configuration::RunLocation = Configuration::RunLocation + "/";
    return instantiateModel("fmiInstantiateSlave", instanceName,
                            GUID, functions, loggingOn);
    }

fmiStatus fmiInitializeSlave(fmiComponent c, fmiReal tStart,
                             fmiBoolean StopTimeDefined, fmiReal tStop)
    {
    return fmiOK;
    }

fmiStatus fmiTerminateSlave(fmiComponent c)
    {
    return terminate("fmiTerminateSlave", c);
    }

fmiStatus fmiResetSlave(fmiComponent c)
    {
    return fmiOK;
    }

void fmiFreeSlaveInstance(fmiComponent c)
    {
    modelInstance->sim.postprocess();
    }

fmiStatus fmiSetRealInputDerivatives(fmiComponent c,
                                     const fmiValueReference vr[], size_t nvr, const fmiInteger order[],
                                     const fmiReal value[])
    {
    return fmiWarning;
    }

fmiStatus fmiGetRealOutputDerivatives(fmiComponent c,
                                      const fmiValueReference vr[], size_t  nvr,
                                      const fmiInteger order[], fmiReal value[])
    {
    return fmiWarning;
    }

fmiStatus fmiCancelStep(fmiComponent c)
    {
    return fmiError;
    }

/**
 * @brief [brief description]
 * @details [long description]
 *
 * @param c simulation pointer
 * @param currentCommunicationPoint
 * @param communicationStepSize
 * @param newStep
 * @return
 */
fmiStatus fmiDoStep(fmiComponent c, fmiReal currentCommunicationPoint,
                    fmiReal communicationStepSize, fmiBoolean newStep)
    {
    modelInstance->sim.preTimeStep();
    modelInstance->sim.timeStep();
    modelInstance->sim.postTimeStep();
    if (LOG.getError())
        {
        return fmiError;
        }
    return fmiOK;
    }

static fmiStatus getStatus(const char* fname, fmiComponent c,
                           const fmiStatusKind s)
    {
    return fmiError;
    }

fmiStatus fmiGetStatus(fmiComponent c, const fmiStatusKind s,
                       fmiStatus* value)
    {
    return getStatus("fmiGetStatus", c, s);
    }

fmiStatus fmiGetRealStatus(fmiComponent c, const fmiStatusKind s,
                           fmiReal* value)
    {
    return getStatus("fmiGetRealStatus", c, s);
    }

fmiStatus fmiGetIntegerStatus(fmiComponent c, const fmiStatusKind s,
                              fmiInteger* value)
    {
    return getStatus("fmiGetIntegerStatus", c, s);
    }

fmiStatus fmiGetBooleanStatus(fmiComponent c, const fmiStatusKind s,
                              fmiBoolean* value)
    {
    return getStatus("fmiGetBooleanStatus", c, s);
    }

fmiStatus fmiGetStringStatus(fmiComponent c, const fmiStatusKind s,
                             fmiString*  value)
    {
    return getStatus("fmiGetStringStatus", c, s);
    }

/**
 * @brief Checks the modelDescription file for parameter names
 * @details Checks the modelDescription file so the agent model know which variables in the array are which
 */
void loadVariables()
    {
    std::string filename =
        Configuration::RunLocation + "modelDescription.xml";

    LOG << " Loading XML file: -" << filename << "-\n";

    namespace rx = rapidxml;
    rx::file<> xmlFile(filename.c_str());  // Default template is char
    rx::xml_document<> doc;
    doc.parse<0>(xmlFile.data());    // 0 means default parse flags
    rx::xml_node<> *root_node = doc.first_node("fmiModelDescription");
    rx::xml_node<> *mv_node = root_node->first_node("ModelVariables");
    rx::xml_node<> *node = mv_node->first_node("ScalarVariable");
    while (node)
        {
        rx::xml_attribute<> *pAttr;
        pAttr = node->first_attribute("name");
        std::string name = pAttr->value();
        pAttr = node->first_attribute("causality");
        std::string causality = pAttr->value();
        pAttr = node->first_attribute("valueReference");
        int valueReference = std::stoi(pAttr->value());
        Configuration::outputRegexs.push_back(name);
        DataStore::addVariable(name);
        if (causality.compare("input") == 0)
            {
            //std::cout << "added: " << name << std::endl;
            }
        else
            {
            rx::xml_node<> *cnode = node->first_node();
            double starValue = 0;
            if (std::strcmp(cnode->name(), "Real") == 0)
                {
                pAttr = cnode->first_attribute("start");
                starValue = std::stod(pAttr->value());
                }
            DataStore::addValueS(name, starValue);
            }
        valToRefs[valueReference] = name;
        node = node->next_sibling();
        }
    LOG << " Loaded XML file: -" << filename << "-\n";
    }

fmiStatus fmiGetModelTypesPlatform()
    {
    return fmiOK;
    }
fmiStatus fmiFreeModelInstance()
    {
    return fmiOK;
    }
fmiStatus fmiSetTime()
    {
    return fmiOK;
    }
fmiStatus fmiSetContinuousStates()
    {
    return fmiOK;
    }
fmiStatus fmiCompletedIntegratorStep()
    {
    return fmiOK;
    }

fmiStatus fmiGetDerivatives()
    {
    return fmiOK;
    }
fmiStatus fmiGetEventIndicators()
    {
    return fmiOK;
    }
fmiStatus fmiEventUpdate()
    {
    return fmiOK;
    }
fmiStatus fmiGetContinuousStates()
    {
    return fmiOK;
    }
fmiStatus fmiGetNominalContinuousStates()
    {
    return fmiOK;
    }
fmiStatus fmiGetStateValueReferences()
    {
    return fmiOK;
    }
fmiStatus fmiTerminate()
    {
    return fmiOK;
    }
