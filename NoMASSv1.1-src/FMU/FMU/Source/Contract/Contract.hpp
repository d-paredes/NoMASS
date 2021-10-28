// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef CONTRACT_HPP_
#define CONTRACT_HPP_

#include <memory>

//**********************************************************************

/**
 * @brief A contract submited from an appliance
 * @details A contract that the appliances submit to the @ref Contract_Negotiation class
 */
struct Contract
    {
    int id;
    int buildingID;
    double requested = 0.0;
    double received = 0.0;
    double receivedCost = 0.0;
    double supplied = 0.0;
    double suppliedCost = 0.0;
    double suppliedLeft = 0.0;
    double priority = 0.0;
    };

typedef std::shared_ptr<Contract> ContractPtr;

//**********************************************************************

#endif  // CONTRACT_HPP_
