// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <algorithm>
#include <iostream>
#include <vector>

#include <DataStore/DataStore.hpp>
#include <Environment/Environment.hpp>
#include <Utility/Utility.hpp>

#include "Occupant_Zone.hpp"

//**********************************************************************

Occupant_Zone::Occupant_Zone() {}

/**
 * @brief is there currently a window action
 * @return true if there is a action taking place
 */
bool Occupant_Zone::isActionWindow() const
    {
    return ActionWindow;
    }

/**
 * @brief is there currently a Light action
 * @return true if there is a action taking place
 */
bool Occupant_Zone::isActionLights() const
    {
    return ActionLights;
    }

/**
 * @brief is there currently a shade action
 * @return true if there is a action taking place
 */
bool Occupant_Zone::isActionShades() const
    {
    return ActionShades;
    }

/**
 * @brief is there currently a heat gain action
 * @return true if there is a action taking place
 */
bool Occupant_Zone::isActionHeatGains() const
    {
    return ActionHeatGains;
    }

/**
 * @brief is there currently a learning action
 * @return true if there is a action taking place
 */
bool Occupant_Zone::isActionLearning() const
    {
    return ActionLearning;
    }


/**
 * @brief Initialises the occupants understanding of a zone
 * @details enables the different interactions that can take place in a zone
 * @param buildingID  The id of the building the zone is in
 * @param buldingZone The actual zone
 * @param agentid     The agents id
 * @param agent       The configuration struct for the agent
 */
void Occupant_Zone::setup(int buildingID, const Building_Zone & buldingZone,
                          int agentid, const ConfigStructAgent &agent)
    {
	//LOG << "          Occupant_Zone (...)" << "\n";
    id = buldingZone.getId();
    this->buildingID = buildingID;
    if (Configuration::info.agentHeatGains)
        {
        aahg.setup(buildingID, agentid);
        availableActions.push_back(0);
        }
    disableBDI();

    ActionHeatGains = false;
    ActionLearning = false;

	//LOG << "          setupWindows..." << "\n";
    setupWindows(agentid, agent, buldingZone);
	//LOG << "          setupLights..." << "\n";
	setupLights(agent, buldingZone);
	//LOG << "          setupShades..." << "\n";
	setupShades(agent, buldingZone);
	//LOG << "          info.learn..." << Configuration::info.learn << "\n";
    if (Configuration::info.learn > 0)
        {
        aalearn.setZoneId(id);
        aalearn.setup(agentid, Configuration::info.learn);
        }
	//LOG << "          agent.ApplianceDuringDay..." << agent.ApplianceDuringDay << "\n";
    if (agent.ApplianceDuringDay > 0)
        {
        aaa.setApplianceDuringDay(agent.ApplianceDuringDay);
        enableBDI();
        }
	//LOG << "          Occupant_Zone done!!!)" << "\n";
    }

void Occupant_Zone::setupLights(const ConfigStructAgent &agent,
                                const Building_Zone & buldingZone)
    {
    ActionLights = false;

    if ((agent.LightOffDuringAudioVisual > 0 ||
            agent.LightOffDuringSleep > 0) &&
            Configuration::info.lights
       )
        {
        availableActions.push_back(7);
        if (buldingZone.hasActivity(2))
            {
            aalBDI.setOffDuringAudioVisual(agent.LightOffDuringAudioVisual);
            }
        aalBDI.setOffDuringSleep(agent.LightOffDuringSleep);
        aalBDI.setAvailableActivities(buldingZone.getActivities());
        enableBDI();
        }
    else if (Configuration::info.lights)
        {
        availableActions.push_back(3);
        aal.setAvailableActivities(buldingZone.getActivities());
        }
    }

void Occupant_Zone::setupShades(const ConfigStructAgent &agent,
                                const Building_Zone & buldingZone)
    {
    ActionShades = false;
    if ((agent.ShadeClosedDuringSleep > 0 ||
            agent.ShadeDuringNight > 0 ||
            agent.ShadeDuringAudioVisual > 0 ||
            agent.ShadeClosedDuringWashing > 0)
            && Configuration::info.shading)
        {
        aasBDI.setup(agent.shadeId);
        if (buldingZone.hasActivity(0))
            {
            aasBDI.setClosedDuringSleep(agent.ShadeClosedDuringSleep);
            }
        if (buldingZone.hasActivity(6))
            {
            aasBDI.setClosedDuringWashing(agent.ShadeClosedDuringWashing);
            }
        aasBDI.setClosedDuringNight(agent.ShadeDuringNight);
        if (buldingZone.hasActivity(2))
            {
            aasBDI.setClosedDuringAudioVisual(agent.ShadeDuringAudioVisual);
            }
        availableActions.push_back(8);
        enableBDI();
        }
    else if (Configuration::info.shading)
        {
        aas.setup(agent.shadeId);
        availableActions.push_back(2);
        }
    }

void Occupant_Zone::setupWindows(int agentid, const ConfigStructAgent &agent,
                                 const Building_Zone & buldingZone)
    {
    ActionWindow = false;

	//LOG << "               agent.WindowOpenDuringCooking: [" << agent.WindowOpenDuringCooking << "]" << "\n";
	//LOG << "               agent.WindowOpenDuringWashing: [" << agent.WindowOpenDuringWashing << "]" << "\n";
	//LOG << "               agent.WindowOpenDuringSleeping: [" << agent.WindowOpenDuringSleeping << "]" << "\n";
	//LOG << "               info.windows: [" << Configuration::info.windows << "]" << "\n";
    if ((agent.WindowOpenDuringCooking > 0 ||
            agent.WindowOpenDuringWashing > 0 ||
            agent.WindowOpenDuringSleeping > 0) &&
            Configuration::info.windows)
        {
		//LOG << "                    FIRST OPTION" << "\n";
		//LOG << "                    enableBDI()" << "\n";
        enableBDI();
		//LOG << "                    aawBDI.setup(agent.windowId:[" << agent.windowId << "], agentid:[" << agentid << "])..." << "\n";
        aawBDI.setup(agent.windowId, agentid);
        if (buldingZone.hasActivity(4))
            {
			//LOG << "                    setOpenDuringCooking" << "\n";
            aawBDI.setOpenDuringCooking(agent.WindowOpenDuringCooking);
            }
        if (buldingZone.hasActivity(6))
            {
			//LOG << "                    setOpenDuringWashing" << "\n";
			aawBDI.setOpenDuringWashing(agent.WindowOpenDuringWashing);
            }
        if (buldingZone.hasActivity(0))
            {
			//LOG << "                    setOpenDuringSleeping" << "\n";
            aawBDI.setOpenDuringSleeping(agent.WindowOpenDuringSleeping);
            }
		//LOG << "                    aawBDI.setAvailableActivities(buldingZone.getActivities(" << "buldingZone.getActivities()" << "))..." << "\n";
        aawBDI.setAvailableActivities(buldingZone.getActivities());
        availableActions.push_back(6);
		//LOG << "                    done!" << "\n";
        }
    else if (Configuration::info.windows)
        {
		//LOG << "                    SECOND OPTION else if (Configuration::info.windows)..." << "\n";
		//LOG << "                      aaw.setup -> agent.windowId [" << agent.windowId << "], agentid [" << agentid << "]" << "\n";
        aaw.setup(agent.windowId, agentid);
		//LOG << "                      setAvailableActivities -> [" << "buldingZone.getActivities()" << "]" << "\n";
        aaw.setAvailableActivities(buldingZone.getActivities());
        availableActions.push_back(1);
		//LOG << "                    SECOND OPTION DONE!!!" << "\n";
        }
    else if (Configuration::info.windowsLearn)
        {
		//LOG << "                    THIRD OPTION Configuration::info.windowsLearn..." << "\n";
        aawLearn.setZoneId(id);
        aawLearn.setup(agentid);
        availableActions.push_back(4);
		//LOG << "                    THIRD OPTION DONE!!!" << "\n";
        }
    }

void Occupant_Zone::shuffleActions()
    {
    std::shuffle(availableActions.begin(), availableActions.end(), Utility::engine);
    }

void Occupant_Zone::step(const Building_Zone& zone,
                         const Building_Zone& zonePrevious,
                         const std::vector<double> &activities)
    {
	//LOG << "    step \n " <<
		//"getAirRelativeHumidity[" << zone.getAirRelativeHumidity() << "]\n";// <<
		//"getAirSystemSensibleHeatingRate[" << zone.getAirSystemSensibleHeatingRate() << "]\n" <<
		//"getBlindState[" << zone.getBlindState() << "]\n" <<
		//"getCurrentOccupantCount[" << zone.getCurrentOccupantCount() << "]\n" <<
		//"getCurrentOccupantGains[" << zone.getCurrentOccupantGains() << "]\n" <<
		//"getDaylightingReferencePoint1Illuminance[" << zone.getDaylightingReferencePoint1Illuminance() << "]\n" <<
		//"getGroundFloor[" << zone.getGroundFloor() << "]\n" <<
		//"getHeatingState[" << zone.getHeatingState() << "]\n" <<
		//"getId[" << zone.getId() << "]\n" <<
		//"getLightState[" << zone.getLightState() << "]\n" <<
		//"getMeanAirTemperature[" << zone.getMeanAirTemperature() << "]\n" <<
		//"getMeanRadiantTemperature[" << zone.getMeanRadiantTemperature() << "]\n";
		//"getNumberOfActivities[" << zone.getNumberOfActivities() << "]\n" <<
		//"getOccupantFraction[" << zone.getOccupantFraction() << "]\n" <<
		//"getWindowDurationOpen[" << zone.getWindowDurationOpen() << "]\n" <<
		//"getWindowState[" << zone.getWindowState() << "]\n";
		//"hasActivity[" << zone.hasActivity() << "]\n" <<
		//"isActive[" << zone.isActive() << "]\n";
		//"isNamed[" << zone.isNamed() << "]\n"
		//;
    bool inZone = zone.getId() == id;
    bool previouslyInZone = zonePrevious.getId() == id;
    if (isInBuilding())
        {
        if (inZone)
            {
            shuffleActions();
            for (int a : availableActions)
                {
                actionStep(a, zone, inZone, previouslyInZone, activities);
                }
            }
        if (Configuration::info.heating && Configuration::info.learn > 0)
            {
            actionStep(5, zone, inZone, previouslyInZone, activities);
            }
        }
    BDI(activities);
    }

void Occupant_Zone::stepPre(const Building_Zone& zone,
                            const Building_Zone& zonePrevious,
                            const std::vector<double> &activities)
    {
    bool inZone = zone.getId() == id;
    bool previouslyInZone = zonePrevious.getId() == id;
    if ( !inZone && previouslyInZone && isInBuilding())
        {
        shuffleActions();
        for (int a : availableActions)
            {
            actionStep(a, zonePrevious, inZone, previouslyInZone, activities);
            }
        }
    if (inZone || previouslyInZone)
        {
        if (Configuration::info.windows)
            {
            aaw.saveResult();
            }
        }
    }

void Occupant_Zone::BDI(const std::vector<double> &activities)
    {
    if (hasBDI)
        {
        if (aawBDI.doRecipe(activities))
            {
            desiredWindowState = aawBDI.getResult();
            ActionWindow = true;
            }

        if (aasBDI.doRecipe(activities))
            {
            desiredShadeState = aasBDI.getResult();
            ActionShades = true;
            }

        if (aalBDI.doRecipe(activities))
            {
            desiredLightState = aalBDI.getResult();
            ActionLights = true;
            }

        if (aaa.doRecipe(activities))
            {
            desiredApplianceState = aaa.getResult();
            ActionAppliance = true;
            }
        }
    }

void Occupant_Zone::actionStep(int action,
                               const Building_Zone &zone, bool inZone, bool preZone,
                               const std::vector<double> &activities)
    {
    switch (action)
        {
        case 0:
            if (inZone)
                {
                ActionHeatGains = true;
                aahg.prestep(clo, metabolicRate);
                aahg.step(zone, inZone);
                heatgains = aahg.getResult();
                previous_pmv = pmv;
                pmv = aahg.getPMV();
                ppd = aahg.getPPD();
                }

            break;
        case 1:
            {
            ActionWindow = true;
            double dailyMeanTe = Environment::getDailyMeanTemperature();
            aaw.setDailyMeanTemperature(dailyMeanTe);
            aaw.step(zone, inZone, preZone, activities);
            desiredWindowState = aaw.getResult();
            }
        break;
        case 2:
            {
            ActionShades = true;
            double ill = zone.getDaylightingReferencePoint1Illuminance();
            aas.setIndoorIlluminance(ill);
            aas.step(zone, inZone, preZone);
            desiredShadeState = aas.getResult();
            }
        break;
        case 3:
            ActionLights = true;
            aal.step(zone, inZone, preZone, activities);
            desiredLightState = aal.getResult();
            break;
        case 4:
            ActionWindow = true;
            aawLearn.setReward(pmv);
            aawLearn.step(zone, inZone, preZone);
            desiredWindowState = aawLearn.getResult();
            break;
        case 5:
            ActionLearning = true;
            aalearn.setReward(pmv);
            aalearn.step(zone, inZone);
            desiredHeatingSetPoint = aalearn.getResult();
            break;
        case 6:
            {
            ActionWindow = true;
            double dailyMeanTe = Environment::getDailyMeanTemperature();
            aawBDI.setDailyMeanTemperature(dailyMeanTe);
            aawBDI.step(zone, inZone, preZone, activities);
            desiredWindowState = aawBDI.getResult();
            }
        break;
        case 7:
            ActionLights = true;
            aalBDI.step(zone, inZone, preZone, activities);
            desiredLightState = aalBDI.getResult();
            break;
        case 8:
            {
            ActionShades = true;
            double ill = zone.getDaylightingReferencePoint1Illuminance();
            aasBDI.setIndoorIlluminance(ill);
            aasBDI.step(zone, inZone, preZone);
            desiredShadeState = aasBDI.getResult();
            }
        break;
        }
    }

int Occupant_Zone::getId() const
    {
    return id;
    }

bool Occupant_Zone::getDesiredWindowState() const
    {
    return desiredWindowState;
    }

bool Occupant_Zone::getDesiredLightState() const
    {
    return desiredLightState;
    }

double Occupant_Zone::getPMV() const
    {
    return pmv;
    }

double Occupant_Zone::getHeatgains() const
    {
    return heatgains;
    }

double Occupant_Zone::getDesiredHeatingSetPoint() const
    {
    return desiredHeatingSetPoint;
    }

double Occupant_Zone::getDesiredShadeState() const
    {
    return desiredShadeState;
    }

void Occupant_Zone::setClo(double clo)
    {
    this->clo = clo;
    }

void Occupant_Zone::setMetabolicRate(double metabolicRate)
    {
    this->metabolicRate = metabolicRate;
    }

void Occupant_Zone::postprocess()
    {
    if (isInBuilding() && Configuration::info.learn > 0)
        {
        aalearn.print();
        aalearn.reset();
        }
    if (isInBuilding() && Configuration::info.windowsLearn > 0)
        {
        aawLearn.print();
        aawLearn.reset();
        }
    }

void Occupant_Zone::postTimeStep()
    {
    ActionWindow = false;
    ActionLights = false;
    ActionShades = false;
    ActionHeatGains = false;
    ActionLearning = false;
    }

bool Occupant_Zone::isInBuilding() const
    {
    return id > 0;  // 0 is the ID for the outside zone
    }

int Occupant_Zone::getDesiredWindowDuration() const
    {
    return aaw.durationOpen();
    }

double Occupant_Zone::getDesiredAppliance() const
    {
    return desiredApplianceState;
    }

bool Occupant_Zone::isActionAppliance() const
    {
    return ActionAppliance;
    }

void Occupant_Zone::disableBDI()
    {
    hasBDI = false;
    }

void Occupant_Zone::enableBDI()
    {
    hasBDI = true;
    }

//**********************************************************************
