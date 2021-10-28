// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

//#ifndef FMU_SOURCE_OCCUPANT_ACTION_LIGHTS_BDI_HPP_
//#define FMU_SOURCE_OCCUPANT_ACTION_LIGHTS_BDI_HPP_
#ifndef OCCUPANT_ACTION_LIGHTS_BDI_HPP_
#define OCCUPANT_ACTION_LIGHTS_BDI_HPP_

#include <vector>

#include <Occupants/Occupant_Action_Lights.hpp>

//**********************************************************************

/**
 * @brief Occupant action on lights using BDI
 * @details Occupant action on lights using BDI adapted from
 * \n Chapman, J., Siebers, P., & Robinson, D. (2017). Data Scarce Behavioural Modelling and the Representation of Social Interactions. Unpublished Manuscript, 1–48.
 */

//**********************************************************************

class Occupant_Action_Lights_BDI : public Occupant_Action_Lights
    {
    public:
        Occupant_Action_Lights_BDI();

        void setOffDuringSleep(double OffDuringSleep);
        void setOffDuringAudioVisual(double OffDuringAudioVisual);
        bool doRecipe(const std::vector<double> &activities);

    private:
        double OffDuringSleep;
        double OffDuringAudioVisual;
    };

//**********************************************************************

#endif  // FMU_SOURCE_OCCUPANT_ACTION_LIGHTS_BDI_HPP_
