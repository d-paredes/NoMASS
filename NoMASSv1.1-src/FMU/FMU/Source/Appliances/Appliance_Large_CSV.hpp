// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef APPLIANCE_LARGE_CSV_HPP_
#define APPLIANCE_LARGE_CSV_HPP_

#include <vector>

#include <Appliances/Appliance_Large.hpp>
#include <Models/Model_Appliance_Large_Usage_Survival.hpp>

//**********************************************************************

/**
 * @brief Large appliances class which uses CSV profiles
 * @details The large appliance agent, handles the model survival/ markov hybrid model
 *          however the profile is now take from a csv file
 */
class Appliance_Large_CSV : public Appliance_Large
    {
    public:
        Appliance_Large_CSV();
        void step();

    protected:

        void setupModel();
        unsigned int count;
        bool running;

    private:
    };

//**********************************************************************

#endif  // APPLIANCE_LARGE_CSV_HPP_
