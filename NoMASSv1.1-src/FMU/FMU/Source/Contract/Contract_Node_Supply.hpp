// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef CONTRACT_NODE_SUPPLY_HPP_
#define CONTRACT_NODE_SUPPLY_HPP_

#include <Contract/Contract.hpp>
#include <Contract/Contract_Node_Tree.hpp>

//**********************************************************************

/**
 * @brief Tree of contracts sorted by the supplied energy left
 * @details Tree of contracts sorted by the supplied energy left in the contracts
 */
class Contract_Node_Supply : public Contract_Node_Tree<ContractPtr>
    {
    public:
        Contract_Node_Supply();
        bool compare(const ContractPtr &insert) const;
        bool isNodeRemoveable(
            const std::shared_ptr<Contract_Node_Tree<ContractPtr>> & ptr) const;
        void makeLeft();
        void makeRight();
        bool isRemoveable() const;
    };

//**********************************************************************

#endif  // CONTRACT_NODE_SUPPLY_HPP_
