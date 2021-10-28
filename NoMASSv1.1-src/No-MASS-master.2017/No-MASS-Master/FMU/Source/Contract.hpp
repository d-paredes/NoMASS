// Copyright 2016 Jacob Chapman

#ifndef CONTRACT_H_
#define CONTRACT_H_
#include <memory>

 /**
  * @brief A contract submited from an appliance
  * @details A contract that the appliances submit to the @ref Contract_Negotiation class
  */

struct Contract {
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

#endif  // CONTRACT_H_
