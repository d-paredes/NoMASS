// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <memory>

#include "Contract_Node_Supply.hpp"

//**********************************************************************

Contract_Node_Supply::Contract_Node_Supply() {}

bool Contract_Node_Supply::compare(const ContractPtr &insert) const
    {
    return insert->suppliedCost < nodeObject->suppliedCost;
    }

bool Contract_Node_Supply::isNodeRemoveable(
    const std::shared_ptr<Contract_Node_Tree<ContractPtr>> & ptr) const
    {
    return ptr->isRemoveable();
    }

void Contract_Node_Supply::makeLeft()
    {
    pLeft = std::make_shared<Contract_Node_Supply>();
    }

void Contract_Node_Supply::makeRight()
    {
    pRight = std::make_shared<Contract_Node_Supply>();
    }

bool Contract_Node_Supply::isRemoveable() const
    {
    return getNodeObject()->suppliedLeft <= 0;
    }

//**********************************************************************
