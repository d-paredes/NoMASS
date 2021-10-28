// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

//#ifndef FMU_SOURCE_OCCUPANT_ACTION_SHADES_BDI_HPP_
//#define FMU_SOURCE_OCCUPANT_ACTION_SHADES_BDI_HPP_
#ifndef OCCUPANT_ACTION_SHADES_BDI_HPP_
#define OCCUPANT_ACTION_SHADES_BDI_HPP_

#include <vector>

#include <Occupants/Occupant_Action_Shades.hpp>

//**********************************************************************

/**
 * @brief Occupant action on shades using BDI
 * @details Occupant action on shades using BDI adapted from
 * \n Chapman, J., Siebers, P., & Robinson, D. (2017). Data Scarce Behavioural Modelling and the Representation of Social Interactions. Unpublished Manuscript, 1–48.
 */

//**********************************************************************

class Occupant_Action_Shades_BDI : public Occupant_Action_Shades
    {
    public:
        Occupant_Action_Shades_BDI();
        void setClosedDuringSleep(double ShadeClosedDuringSleep);
        void setClosedDuringWashing(double ShadeClosedDuringWashing);
        void setClosedDuringNight(double ShadeClosedDuringNight);
        void setClosedDuringAudioVisual(double ShadeClosedDuringAudioVisual);

        bool doRecipe(const std::vector<double> &activities);
    private:

        double ShadeClosedDuringSleep;
        double ShadeClosedDuringWashing;
        double ShadeClosedDuringNight;
        double ShadeClosedDuringAudioVisual;
    };

//**********************************************************************

//#endif  // FMU_SOURCE_OCCUPANT_ACTION_SHADES_BDI_HPP_
#endif  // OCCUPANT_ACTION_SHADES_BDI_HPP_
