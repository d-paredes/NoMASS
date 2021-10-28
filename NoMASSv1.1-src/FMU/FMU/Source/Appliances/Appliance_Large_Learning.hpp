// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef APPLIANCE_LARGE_LEARNING_HPP_
#define APPLIANCE_LARGE_LEARNING_HPP_

#include <queue>
#include <string>
#include <vector>

#include <QLearning/QLearning.hpp>
#include <Appliances/Appliance_Large.hpp>

//**********************************************************************

struct profileStruct
    {
    std::vector<double> power;
    int startTime = -1;
    double maxTimeRequired = 0;
    double cost = 0;
    bool isLearningPeriod = false;
    int nonLearningStep = 0;
    unsigned int learningStep = 0;
    int requestedTime;
    };

/**
 * @brief Large appliances learning class
 * @details This will handle the appliance learning model for profile shifting
 */
class Appliance_Large_Learning : public Appliance_Large
    {
    public:
        Appliance_Large_Learning();
        void setup(ConfigStructAppliance a);
        void step();
        void postprocess();
        double getRequiredTime(int hourOfDay) const;
        void addToCost(const double cost);
        void setHoulyTimeRequired(const std::vector<double> & houlyTimeRequired);

        bool isModelOn();

    protected:
        virtual double getPowerAt(const int timestep);
        virtual void calculateProfile();

        std::queue<profileStruct> powerProfile;

    private:

        void beforeClear();
        int databaseIDactual;
        std::vector<double> houlyTimeRequired;
        QLearning qLearning;

        void stepApplianceOffAndNotLearning(const int hourOfTheDay);

        void calculateLearntStartTime();
        void startLearningPeriod(const int hourOfTheDay);
        void stopLearningPeriod(const int hourOfTheDay);
        void saveActualProfile();
        double calculateReward();
        bool learnStepLessThanProfile() const;
        void eraseFirstPowerProfile();
    };

//**********************************************************************

#endif  // APPLIANCE_LARGE_LEARNING_HPP_
