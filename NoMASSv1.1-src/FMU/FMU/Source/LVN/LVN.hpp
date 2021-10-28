// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef LVN_HPP_
#define LVN_HPP_

#include <vector>

#include <LVN/LVN_Node.hpp>

//**********************************************************************

/**
 * @brief Models the survival fuction for the activity model
 * @details The low voltage network used to calculate cable losses
 * \n Sancho-Tomás, A., Chapman, J., & Robinson, D. (2017). Extending No-MASS: Multi-Agent Stochastic Simulation for Demand Response of residential appliances. In Building Simulation 2017.
 */

//**********************************************************************

class LVN
    {
    public:
        LVN();
        void setup();
        void postTimeStep();
        void setPowerForID(const double power, const int id);

    private:
        LVN_Node rootNode;
        bool enabled;
    };

//**********************************************************************

#endif  // LVN_HPP_
