// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef APPLIANCE_FMI_HPP_
#define APPLIANCE_FMI_HPP_

#include <string>

#include <Appliances/Appliance.hpp>

//**********************************************************************

/**
 * @brief FMI appliances class
 * @details This will handles the power coming from the FMI interface
 * for example electric heaters
 */
class Appliance_FMI : public Appliance
    {
    public:
        Appliance_FMI();
        void setup(ConfigStructAppliance a);
        void step();
        void setFMIVariableName(const std::string & FMIVariableName);
    private:
        int FMIVariableName;
    };

//**********************************************************************

#endif  // APPLIANCE_FMI_HPP_
