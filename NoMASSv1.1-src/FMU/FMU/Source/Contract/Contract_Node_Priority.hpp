// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef CONTRACT_NODE_PRIORITY_HPP_
#define CONTRACT_NODE_PRIORITY_HPP_

#include <Contract/Contract.hpp>
#include <Contract/Contract_Node_Tree.hpp>

//**********************************************************************

/**
 * @brief Tree of contracts sorted by the priority
 * @details Tree of contracts sorted by the priority of the contracts
 */
class Contract_Node_Priority : public Contract_Node_Tree<ContractPtr>
    {
    public:
        Contract_Node_Priority();
        bool compare(const ContractPtr &insert) const;
        bool isNodeRemoveable(
            const std::shared_ptr<Contract_Node_Tree<ContractPtr>> & ptr) const;
        void makeLeft();
        void makeRight();
        bool isRemoveable() const;
    };

//**********************************************************************

#endif  // CONTRACT_NODE_PRIORITY_HPP_
