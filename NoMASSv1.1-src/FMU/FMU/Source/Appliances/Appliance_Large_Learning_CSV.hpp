// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef APPLIANCE_LARGE_LEARNING_CSV_HPP_
#define APPLIANCE_LARGE_LEARNING_CSV_HPP_

#include <string>
#include <vector>

#include <Appliances/Appliance_Large_Learning.hpp>

//**********************************************************************

/**
 * @brief Large appliances learning class with profile taken from CSV
 * @details This will handle the appliance learning model for profile shifting
 *          however the profile is now take from a csv file
 */
class Appliance_Large_Learning_CSV : public Appliance_Large_Learning
    {

    public:
        Appliance_Large_Learning_CSV();


    protected:
        void setupModel();
        void calculateProfile();
    private:
    };

//**********************************************************************

#endif  // APPLIANCE_LARGE_LEARNING_CSV_HPP_
