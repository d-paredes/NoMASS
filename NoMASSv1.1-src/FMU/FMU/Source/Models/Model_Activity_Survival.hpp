// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef MODEL_ACTIVITY_SURVIVAL_HPP_
#define MODEL_ACTIVITY_SURVIVAL_HPP_

#include <vector>
#include <map>

#include <Configuration/Configuration.hpp>
#include <Models/Model_Activity.hpp>

//**********************************************************************

/**
 * @brief Models the survival fuction for the activity model
 * @details Models the survival fuction for the activity model adapted from
 * \n Jaboob, S. (2015). Stochastic Modelling of Occupants’ Activities and Related Behaviours. The University of Nottingham.
 */

//**********************************************************************

class Model_Activity_Survival : public Model_Activity
    {
    public:
        Model_Activity_Survival();
        int multinominalActivity(const double p[24][10], const int hourCount);

    private:
        void parseOther(rapidxml::xml_node<> *node);
        double randomWeibull(double scale, double shape) const;
        double duration;
        int state;
        std::map<int, std::vector<double>> shapes;
        std::map<int, std::vector<double>> scales;
    };

//**********************************************************************

#endif  //  MODEL_ACTIVITY_SURVIVAL_HPP_
