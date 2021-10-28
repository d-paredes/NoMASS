// Copyright 2015 Jacob Chapman
#include <limits.h>
#include <vector>
#include "tests/Gen.hpp"

#include "Utility.hpp"
#include "Contract.hpp"
#include "Contract_Negotiation.hpp"

#include "gtest/gtest.h"

class Test_Contract_Negotiation  : public ::testing::Test {
 protected:
    Contract_Negotiation cn;

    virtual void SetUp();
    virtual void AfterConfiguration();
};

void Test_Contract_Negotiation::SetUp() {
}

void Test_Contract_Negotiation::AfterConfiguration() {
}

TEST_F(Test_Contract_Negotiation, contract1) {
  Contract c;
  c.id = 1;
  c.buildingID = 1;
  c.requested = 100.0;
  c.received = 0.0;
  c.receivedCost = 0.0;
  c.supplied = 0.0;
  c.suppliedCost = 0.0;
  c.suppliedLeft = 0.0;
  c.priority = 0.0;

  Contract d;
  d.id = 2;
  d.buildingID = 1;
  d.requested = 0.0;
  d.received = 0.0;
  d.receivedCost = 0.0;
  d.supplied = 100.0;
  d.suppliedCost = 0.0;
  d.suppliedLeft = d.supplied;
  d.priority = 0.0;
  cn.submit(c);
  cn.submit(d);
  cn.process();
  c = cn.getContract(1, 1);
  d = cn.getContract(1, 2);

  EXPECT_NEAR(c.received, 100.0, 0.1);
  cn.clear();
}


TEST_F(Test_Contract_Negotiation, power) {
  Contract c;
  c.id = 1;
  c.buildingID = 1;
  c.requested = 100.0;
  c.received = 0.0;
  c.receivedCost = 0.0;
  c.supplied = 0.0;
  c.suppliedCost = 0.0;
  c.suppliedLeft = 0.0;
  c.priority = 0.0;

  Contract d;
  d.id = 2;
  d.buildingID = 1;
  d.requested = 50.0;
  d.received = 0.0;
  d.receivedCost = 0.0;
  d.supplied = 0.0;
  d.suppliedCost = 0.0;
  d.suppliedLeft = 0.0;
  d.priority = 0.0;

  Contract e;
  e.id = 3;
  e.buildingID = 1;
  e.requested = 0.0;
  e.received = 0.0;
  e.receivedCost = 0.0;
  e.supplied = 200.0;
  e.suppliedCost = 0.0;
  e.suppliedLeft = e.supplied;
  e.priority = 0.0;
  cn.submit(c);
  cn.submit(d);
  cn.submit(e);
  cn.process();
  c = cn.getContract(1, 1);
  d = cn.getContract(1, 2);
  e = cn.getContract(1, 3);

  EXPECT_NEAR(c.received, 100.0, 0.1);
  EXPECT_NEAR(d.received, 50.0, 0.1);
  EXPECT_NEAR(e.suppliedLeft, 50.0, 0.1);
  cn.clear();
}

TEST_F(Test_Contract_Negotiation, Many) {
    Utility::setSeed(0);
    std::vector<ContractPtr> contractsSupplied;
    double requested = 1000;
    int max = 1000000;
    for(int i = 0; i < max; i++){
      Contract c;
      c.supplied = requested;
      c.suppliedLeft = requested;
      requested = Utility::randomDouble(0, 1000);
      c.id = i;
      c.buildingID = 0;
      c.requested = requested;
      c.received = 0;
      c.suppliedCost = Utility::randomDouble(0, 10000);
      c.priority = Utility::randomDouble(0, 100000);
      cn.submit(c);
    }
    cn.process();

    for(int i = 0; i < max; i++){
      Contract c;
      c = cn.getContract(0, i);
      EXPECT_NEAR(c.received, c.requested, 0.1);
    }
}
