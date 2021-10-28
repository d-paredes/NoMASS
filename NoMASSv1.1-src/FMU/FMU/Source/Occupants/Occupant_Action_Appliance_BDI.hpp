// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef FMU_SOURCE_OCCUPANT_ACTION_APPLIANCE_BDI_HPP_
#define FMU_SOURCE_OCCUPANT_ACTION_APPLIANCE_BDI_HPP_

#include <vector>

#include <Occupants/Occupant_Action_Appliance.hpp>

//**********************************************************************

/**
 * @brief Occupant action on appliances using BDI
 * @details Occupant action on appliances using BDI adapted from
 * \n Chapman, J., Siebers, P., & Robinson, D. (2017). Data Scarce Behavioural Modelling and the Representation of Social Interactions. Unpublished Manuscript, 1–48.
 */

//**********************************************************************

class Occupant_Action_Appliance_BDI : public Occupant_Action_Appliance
    {
    public:
        Occupant_Action_Appliance_BDI();
        void setApplianceDuringDay(double ApplianceDuringDay);
        bool doRecipe(const std::vector<double> &activities);

    private:
        double ApplianceDuringDay;
        int first;
        int last;
        void calculateFirstLastCouts(const std::vector<double> &activities);
    };

//**********************************************************************

#endif  // FMU_SOURCE_OCCUPANT_ACTION_APPLIANCE_BDI_HPP_
