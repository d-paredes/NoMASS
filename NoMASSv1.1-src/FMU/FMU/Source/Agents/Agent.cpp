// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include "Agent.hpp"

//**********************************************************************

Agent::Agent() {}

void Agent::setup() {}

void Agent::preprocess() {}

void Agent::step() {}

void Agent::postprocess() {}

void Agent::postTimeStep() {}

void Agent::setBuildingID(const int id)
    {
    buildingID = id;
    }

void Agent::setID(const int id)
    {
    this->id = id;
    }

int Agent::getID() const
    {
    return id;
    }

int Agent::getBuildingID() const
    {
    return buildingID;
    }

void Agent::setIDString(const std::string & idString)
    {
    this->idString = idString;
    }

//**********************************************************************
