// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef CONTRACT_NEGOTIATION_HPP_
#define CONTRACT_NEGOTIATION_HPP_

#include <memory>
#include <unordered_map>
#include <vector>

#include <Contract/Contract.hpp>
#include <Contract/Contract_Node_Priority.hpp>
#include <Contract/Contract_Node_Supply.hpp>

//**********************************************************************

/**
 * @brief Manages the negotiation between the appliance contracts
 * @details Manages the negotiation between the appliance contracts
 */
class Contract_Negotiation
    {
    public:
        Contract_Negotiation();
        void submit(const Contract & c);
        void process();
        const Contract getContract(const int buildingID, const int id) const;
        double getReceivedPowerForContract(const int buildingID, const int id);
        double getCostOfPowerForContract(const int buildingID, const int id);
        void clear();
        double getDifference() const;

    private:
        void calcDifference(const Contract & c);
        void insertSupply(const ContractPtr &contract);
        void insertPriority(const ContractPtr &contract);
        void processContracts();
        bool sameContract(const ContractPtr &c1, const ContractPtr &c2) const;
        double difference;

        std::unordered_map<int, std::unordered_map<int, ContractPtr>> contracts;
        std::vector<ContractPtr> contractsSupplied;
        Contract_Node_Supply nodeSupply;
        Contract_Node_Priority nodePriority;
    };

//**********************************************************************

#endif  // CONTRACT_NEGOTIATION_HPP_
