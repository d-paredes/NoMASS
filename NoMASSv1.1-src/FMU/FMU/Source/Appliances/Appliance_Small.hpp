// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef APPLIANCE_SMALL_HPP_
#define APPLIANCE_SMALL_HPP_

#include <string>
#include <vector>

#include <Appliances/Appliance.hpp>
#include <Models/Model_Appliance_Small_Usage.hpp>

//**********************************************************************

/**
 * @brief Small appliances class
 * @details The small appliance agent, handles the model
 */

class Appliance_Small : public Appliance
    {
    public:
        Appliance_Small();

        void setup(ConfigStructAppliance a);
        void step();

    private:
        Model_Appliance_Small_Usage model;
    };

//**********************************************************************

#endif  // APPLIANCE_SMALL_HPP_
