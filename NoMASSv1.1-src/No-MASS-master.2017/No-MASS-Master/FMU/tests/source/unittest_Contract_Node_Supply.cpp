// Copyright 2015 Jacob Chapman
#include <limits.h>
#include <vector>
#include <memory>
#include "tests/Gen.hpp"

#include "Configuration.hpp"
#include "Utility.hpp"
#include "Contract.hpp"
#include "Contract_Node_Supply.hpp"

#include "gtest/gtest.h"

class Test_Contract_Node_Supply : public ::testing::Test {
 protected:
    Contract_Node_Supply nodeSupply;

    virtual void SetUp();
    virtual void AfterConfiguration();
};

void Test_Contract_Node_Supply::SetUp() {
  nodeSupply.clear();
}

void Test_Contract_Node_Supply::AfterConfiguration() {
}

TEST_F(Test_Contract_Node_Supply, one) {
    Contract c;
    ContractPtr cp = std::make_shared<Contract>(c);
    cp->id = 0;
    cp->buildingID = 0;
    cp->requested = 0.0;
    cp->received = 0.0;
    cp->receivedCost = 0.0;
    cp->supplied = 0.0;
    cp->suppliedCost = 0.0;
    cp->suppliedLeft = 0.0;
    cp->priority = 0.0;
    nodeSupply.insert(cp, cp->suppliedCost);
    ContractPtr op1;
    op1 = nodeSupply.popLeftEdge();
    EXPECT_NEAR(op1->suppliedCost, 0.0, 0.1);
    EXPECT_NEAR(cp->suppliedCost, 0.0, 0.1);
    op1->suppliedCost = 10.0;
    EXPECT_NEAR(op1->suppliedCost, 10.0, 0.1);
    EXPECT_NEAR(cp->suppliedCost, 10.0, 0.1);
}

TEST_F(Test_Contract_Node_Supply, twoDifferent) {
    Contract c;
    ContractPtr cp = std::make_shared<Contract>(c);
    cp->id = 0;
    cp->buildingID = 0;
    cp->supplied = 100.0;
    cp->suppliedCost = 0.0;

    Contract c2;
    ContractPtr cp2 = std::make_shared<Contract>(c2);
    cp2->id = 1;
    cp2->buildingID = 0;
    cp2->supplied = 100.0;
    cp2->suppliedCost = 1.0;

    nodeSupply.insert(cp, cp->suppliedCost);
    nodeSupply.insert(cp2, cp2->suppliedCost);

    ContractPtr op1;
    op1 = nodeSupply.popLeftEdge();
    EXPECT_NEAR(op1->suppliedCost, 0.0, 0.1);
    EXPECT_NEAR(cp->suppliedCost, 0.0, 0.1);
    EXPECT_EQ(op1->id, 0);
    EXPECT_EQ(cp->id, 0);

    cp->supplied = 0.0;

    ContractPtr op2;
    op2 = nodeSupply.popLeftEdge();
    EXPECT_NEAR(op2->suppliedCost, 1.0, 0.1);
    EXPECT_NEAR(cp2->suppliedCost, 1.0, 0.1);
    EXPECT_EQ(op2->id, 1);
    EXPECT_EQ(cp2->id, 1);
}


TEST_F(Test_Contract_Node_Supply, twoEqual) {
    Contract c;
    ContractPtr cp = std::make_shared<Contract>(c);
    cp->id = 0;
    cp->buildingID = 0;
    cp->supplied = 100.0;
    cp->suppliedCost = 0.0;

    Contract c2;
    ContractPtr cp2 = std::make_shared<Contract>(c2);
    cp2->id = 1;
    cp2->buildingID = 0;
    cp2->supplied = 100.0;
    cp2->suppliedCost = 0.0;
    cp2->suppliedLeft = 100.0;

    nodeSupply.insert(cp, cp->suppliedCost);
    nodeSupply.insert(cp2, cp2->suppliedCost);

    ContractPtr op1;
    op1 = nodeSupply.popLeftEdge();
    EXPECT_NEAR(op1->suppliedCost, 0.0, 0.1);
    EXPECT_NEAR(cp->suppliedCost, 0.0, 0.1);
    EXPECT_EQ(op1->id, 0);
    EXPECT_EQ(cp->id, 0);

    cp->supplied = 0.0;

    ContractPtr op2;
    op2 = nodeSupply.popLeftEdge();
    EXPECT_NEAR(op2->suppliedCost, 0.0, 0.1);
    EXPECT_NEAR(cp2->suppliedCost, 0.0, 0.1);
    EXPECT_EQ(op2->id, 1);
    EXPECT_EQ(cp2->id, 1);
}


TEST_F(Test_Contract_Node_Supply, Many) {
    Utility::setSeed(0);
    std::vector<ContractPtr> contractsSupplied;
    for(int i = 0; i < 100000; i++){
      Contract c;
      contractsSupplied.push_back(std::make_shared<Contract>(c));
      contractsSupplied.back()->id = i;
      contractsSupplied.back()->buildingID = 0;
      contractsSupplied.back()->supplied = 100.0;
      contractsSupplied.back()->suppliedCost = Utility::randomDouble(0, 10000000);
      contractsSupplied.back()->suppliedLeft = 100.0;
      nodeSupply.insert(contractsSupplied.back(), contractsSupplied.back()->suppliedCost);
    }

    std::vector<ContractPtr> contractsSuppliedEmp;
    ContractPtr op2 = nodeSupply.popLeftEdge();
    while(op2){
      contractsSuppliedEmp.push_back(op2);
      op2 = nodeSupply.popLeftEdge();
    }

    std::vector<ContractPtr>::iterator cs = contractsSuppliedEmp.begin();
    while (cs != contractsSuppliedEmp.end()) {
        (*cs)->suppliedLeft = 0;
        cs++;
    }

    for(const ContractPtr opx2 : contractsSupplied){
      EXPECT_NEAR(opx2->suppliedLeft, 0.0, 0.1);
    }
}
