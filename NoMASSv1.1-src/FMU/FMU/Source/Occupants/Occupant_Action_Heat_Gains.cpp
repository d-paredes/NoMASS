// Undefined description of file -- Jacob Chapman -- 2015
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <iostream>
#include <string>
#include <vector>

#include <DataStore/DataStore.hpp>
#include <Models/Model_HeatGains.hpp>

#include "Occupant_Action_Heat_Gains.hpp"

//**********************************************************************

Occupant_Action_Heat_Gains::Occupant_Action_Heat_Gains() {}

void Occupant_Action_Heat_Gains::setup(int buildingID, int agentid)
    {
    this->buildingID = buildingID;
    this->id = agentid;
    std::string idAsString = "Building" + std::to_string(buildingID)
                             + "_Occupant"+ std::to_string(id);

    datastoreIdMetabolicRate =
        DataStore::addVariable(idAsString + "_Metabolic_Rate");
    datastoreIdClo = DataStore::addVariable(idAsString + "_CLO");
    datastoreIdPpd = DataStore::addVariable(idAsString + "_PPD");
    datastoreIdPmv = DataStore::addVariable(idAsString + "_PMV");
    datastoreIdPmvAirTemp = DataStore::addVariable(idAsString + "_PMV_airTemp");
    datastoreIdPmvAirHumid = DataStore::addVariable(idAsString + "_PMV_airHumid");
    datastoreIdPmvMeanRadient =
        DataStore::addVariable(idAsString + "_PMV_meanRadient");
    datastoreIdPmvSetpoint = DataStore::addVariable(idAsString + "_PMV_setpoint");
    }

void Occupant_Action_Heat_Gains::prestep(double clo, double metabolicRate)
    {
    this->clo = clo;
    this->metabolicRate = metabolicRate;
    }

void Occupant_Action_Heat_Gains::step(const Building_Zone& zone,
                                      const bool inZone)
    {
    ppd = 5;
    pmv = 0;
    result = 0;
    double airTemp = zone.getMeanAirTemperature();
    double airHumid = zone.getAirRelativeHumidity();
    double meanRadient = zone.getMeanRadiantTemperature();

    if (inZone)
        {
        Model_HeatGains h;
        /**
         * Calculates the Fanger pmv and sets the instance varibles related to results.
         * @param metabolicRate Metabolic Rate
         * @param partialWaterPressure partial water vapour kPa
         * @param meanRadiantTemperature mean radiant temperature C
         * @param externalWork external work
         * @param ta air temperature
         * @param clo Clothing value
         * @param airVelocity Air velocity
         */

        h.calculate(metabolicRate, airHumid, meanRadient, 0, airTemp, clo, 0.137);
        result = h.getAllHeatGains();
        ppd = h.getPpd();
        pmv = h.getPmv();
        }
    DataStore::addValue(datastoreIdMetabolicRate, metabolicRate);
    DataStore::addValue(datastoreIdClo, clo);
    DataStore::addValue(datastoreIdPpd, ppd);
    DataStore::addValue(datastoreIdPmv, pmv);
    DataStore::addValue(datastoreIdPmvAirTemp, airTemp);
    DataStore::addValue(datastoreIdPmvAirHumid, airHumid);
    DataStore::addValue(datastoreIdPmvMeanRadient, meanRadient);
    DataStore::addValue(datastoreIdPmvSetpoint, zone.getHeatingState());
    }

double Occupant_Action_Heat_Gains::getPMV() const
    {
    return pmv;
    }

double Occupant_Action_Heat_Gains::getPPD() const
    {
    return ppd;
    }

//**********************************************************************
