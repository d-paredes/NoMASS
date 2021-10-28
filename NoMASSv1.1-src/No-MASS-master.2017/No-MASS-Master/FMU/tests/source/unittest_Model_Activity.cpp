// Copyright 2015 Jacob Chapman

#include <limits.h>
#include <string>
#include <iostream>
#include <fstream>
#include "tests/Gen.hpp"
#include "Model_Activity.hpp"
#include "Configuration.hpp"
#include "Utility.hpp"

#include "gtest/gtest.h"

class Test_Model_Activity : public ::testing::Test {
 protected:
    Model_Activity ma;
    std::vector<double> activities;
    int buildingID = 0;
    virtual void SetUp();
    virtual void AfterConfiguration();
};

void Test_Model_Activity::SetUp() {
  Configuration::reset();
}

void Test_Model_Activity::AfterConfiguration() {
  Configuration::info.timeSteps = 105182;
  Configuration::info.timeStepsPerHour = 6;
  Configuration::info.startDayOfWeek = 2;
  Configuration::info.startMonth  = 1;
  Configuration::info.startDay  = 31;

  ConfigStructAgent agent = Configuration::buildings[0].agents[0];
  ma.setAge(agent.age);
  ma.setComputer(agent.computer);
  ma.setCivstat(agent.civstat);
  ma.setUnemp(agent.unemp);
  ma.setRetired(agent.retired);
  ma.setEdtry(agent.edtry);
  ma.setFamstat(agent.famstat);
  ma.setSex(agent.sex);
  ma.setProbMap(agent.profile);
  activities = ma.preProcessActivities();
}

TEST_F(Test_Model_Activity, Dissagregate) {
    Configuration::parseConfiguration
      (testFiles + "/SimulationConfig2.xml");
    AfterConfiguration();

    EXPECT_EQ(activities.at(0), 9);
    EXPECT_EQ(activities.at(1000), 2);
    EXPECT_EQ(activities.at(2000), 1);
    EXPECT_EQ(activities.at(3000), 9);
    EXPECT_EQ(activities.at(4000), 2);
    EXPECT_EQ(activities.at(5000), 8);
    EXPECT_EQ(activities.at(6000), 9);
    bool found = false;
    for (int i = 0; i < 10; i++) {
      for (double a : activities) {
        if (a == i) {
          found = true;
        }
      }
      EXPECT_TRUE(found);
      found = false;
    }
}

int getActivity(double *p, double drand) {
  int activity = -1;
  double sum = 0;
  for (int i =0; i < 10; i++) {
    sum += p[i];
    if (sum >= drand) {
        activity = i;
        break;
    }
  }
  return activity;
}

TEST_F(Test_Model_Activity, multinominalRandom) {
  double p[10] = {0.036078751, 0.12437013, 0.082256370, 0.003995250,
    0.027476964, 0.030800, 0.114028071, 0.0102342340, 0.043672692, 0.52712584};

  double drand = Utility::randomDouble(0.0, 1.0);
  drand = 0.001;
  int activity = getActivity(p, drand);
  EXPECT_EQ(activity, 0);
  drand = 0.11;
  activity = getActivity(p, drand);
  EXPECT_EQ(activity, 1);
  drand = 0.21;
  activity = getActivity(p, drand);
  EXPECT_EQ(activity, 2);
  drand = 0.243;
  activity = getActivity(p, drand);
  EXPECT_EQ(activity, 3);
  drand = 0.25;
  activity = getActivity(p, drand);
  EXPECT_EQ(activity, 4);
  drand = 0.29;
  activity = getActivity(p, drand);
  EXPECT_EQ(activity, 5);
  drand = 0.40;
  activity = getActivity(p, drand);
  EXPECT_EQ(activity, 6);
  drand = 0.4191;
  activity = getActivity(p, drand);
  EXPECT_EQ(activity, 7);
  drand = 0.43;
  activity = getActivity(p, drand);
  EXPECT_EQ(activity, 8);
  drand = 0.99999999;
  activity = getActivity(p, drand);
  EXPECT_EQ(activity, 9);
}

TEST_F(Test_Model_Activity, multinominalActivity) {
  double p0[1][10] = {{1, 0, 0, 0, 0, 0, 0, 0, 0, 0}};
  EXPECT_EQ(ma.multinominalActivity(p0, 0), 0);
  double p1[1][10] = {{0, 1, 0, 0, 0, 0, 0, 0, 0, 0}};
  EXPECT_EQ(ma.multinominalActivity(p1, 0), 1);
  double p2[1][10] = {{0, 0, 1, 0, 0, 0, 0, 0, 0, 0}};
  EXPECT_EQ(ma.multinominalActivity(p2, 0), 2);
  double p3[1][10] = {{0, 0, 0, 1, 0, 0, 0, 0, 0, 0}};
  EXPECT_EQ(ma.multinominalActivity(p3, 0), 3);
  double p4[1][10] = {{0, 0, 0, 0, 1, 0, 0, 0, 0, 0}};
  EXPECT_EQ(ma.multinominalActivity(p4, 0), 4);
  double p5[1][10] = {{0, 0, 0, 0, 0, 1, 0, 0, 0, 0}};
  EXPECT_EQ(ma.multinominalActivity(p5, 0), 5);
  double p6[1][10] = {{0, 0, 0, 0, 0, 0, 1, 0, 0, 0}};
  EXPECT_EQ(ma.multinominalActivity(p6, 0), 6);
  double p7[1][10] = {{0, 0, 0, 0, 0, 0, 0, 1, 0, 0}};
  EXPECT_EQ(ma.multinominalActivity(p7, 0), 7);
  double p8[1][10] = {{0, 0, 0, 0, 0, 0, 0, 0, 1, 0}};
  EXPECT_EQ(ma.multinominalActivity(p8, 0), 8);
  double p9[1][10] = {{0, 0, 0, 0, 0, 0, 0, 0, 0, 1}};
  EXPECT_EQ(ma.multinominalActivity(p9, 0), 9);

  double p[1][10] = {{0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1}};

  double top = 10000;

  double px[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  for (int i = 0; i < top; i++) {
      int activity = ma.multinominalActivity(p, 0);
      px[activity] = px[activity] + 1;
  }

  for (int i = 0; i < 10; i++) {
    EXPECT_NEAR(px[i] / top, 0.1, 0.007);
    px[i] = 0;
  }

    double pp[1][10] = {{0.036078751, 0.12437013, 0.082256370, 0.003995250,
        0.027476964, 0.030800, 0.114028071, 0.0102342340, 0.043672692, 0.52712584}};

  double sum = 0;
  for (int i = 0; i < 10; i++) {
    sum += pp[0][i];
  }
  EXPECT_NEAR(sum, 1, 0.001);

  for (int i = 0; i < top; i++) {
      int activity = ma.multinominalActivity(pp, 0);
      px[activity] = px[activity] + 1;
  }

  EXPECT_NEAR(px[0] / top, 0.036, 0.005);
  EXPECT_NEAR(px[1] / top, 0.124, 0.005);
  EXPECT_NEAR(px[2] / top, 0.087, 0.005);
  EXPECT_NEAR(px[3] / top, 0.003, 0.005);
  EXPECT_NEAR(px[4] / top, 0.027, 0.005);
  EXPECT_NEAR(px[5] / top, 0.030, 0.005);
  EXPECT_NEAR(px[6] / top, 0.112, 0.005);
  EXPECT_NEAR(px[7] / top, 0.010, 0.005);
  EXPECT_NEAR(px[8] / top, 0.043, 0.005);
  EXPECT_NEAR(px[9] / top, 0.527, 0.05);
}

TEST_F(Test_Model_Activity, multinominalP) {
    Configuration::parseConfiguration(testFiles + "SimulationConfig1.xml");
    Configuration::FileActivity = testFiles + "Activity.xml";
    AfterConfiguration();

    std::vector<double> activities = ma.preProcessActivities();
    double p[4][7][24][10];
    ma.multinominalP(p);
    double sum = 0;
    for (int s = 0; s < 4; s++) {
      for (int d = 0; d < 7; d++) {
        std::string file2 = "season" + std::to_string(s) +
          "day" + std::to_string(d) +
          "sex2famstat3edtry1age2computer0civstat1unemp0retired1.csv";
        std::ofstream myfile2;
        myfile2.open(file2.c_str());

        for (int h = 0; h < 24; h++) {
          sum = 0;
          for (int i = 0; i < 10; i++) {
            sum += p[s][d][h][i];
            myfile2 << p[s][d][h][i];
            if (i < 9) {
              myfile2 << ",";
            }
          }
          myfile2 << std::endl;
          EXPECT_NEAR(sum, 1, 0.000000001);
        }

        myfile2.close();
      }
    }
}



TEST_F(Test_Model_Activity, multinominalP2) {
    Configuration::parseConfiguration(testFiles + "SimulationConfig1a.xml");
    Configuration::FileActivity = testFiles + "Activity.xml";
    AfterConfiguration();

    std::vector<double> activities = ma.preProcessActivities();
    double p[4][7][24][10];
    ma.multinominalP(p);
    double sum = 0;
    for (int s = 0; s < 4; s++) {
      for (int d = 0; d < 7; d++) {
        std::string file2 = "season" + std::to_string(s) +
          "day" + std::to_string(d) +
          "sex2famstat3edtry1age2computer0civstat1unemp0retired0.csv";
        std::ofstream myfile2;
        myfile2.open(file2.c_str());

        for (int h = 0; h < 24; h++) {
          sum = 0;
          for (int i = 0; i < 10; i++) {
            sum += p[s][d][h][i];
            myfile2 << p[s][d][h][i];
            if (i < 9) {
              myfile2 << ",";
            }
          }
          myfile2 << std::endl;
          EXPECT_NEAR(sum, 1, 0.000000001);
        }

        myfile2.close();
      }
    }
}

TEST_F(Test_Model_Activity, multinominal) {
    Utility::setSeed(1);
    Configuration::parseConfiguration(testFiles + "/SimulationConfig1.xml");
    Configuration::FileActivity = testFiles + "Activity.xml";
    AfterConfiguration();

    EXPECT_EQ(activities.at(0), 7);
    EXPECT_EQ(activities.at(1000), 1);
    EXPECT_EQ(activities.at(2000), 1);
    EXPECT_EQ(activities.at(3000), 9);
    EXPECT_EQ(activities.at(4000), 2);
    EXPECT_EQ(activities.at(5000), 2);
    EXPECT_EQ(activities.at(6000), 9);
    bool found = false;
    for (int i = 0; i < 3; i++) {
      for (double a : activities) {
        if (a == i) {
          found = true;
        }
      }

      EXPECT_TRUE(found);
      found = false;
    }
    for (int i = 4; i < 10; i++) {
      for (double a : activities) {
        if (a == i) {
          found = true;
        }
      }

      EXPECT_TRUE(found);
      found = false;
    }
}
/*
TEST(Appliance, Ownership) {

  Appliance a;
  EXPECT_NEAR(0.932138, a.ownership(), 0.001);
  EXPECT_GT(a.ownership(), 0);
  EXPECT_GT(1, a.ownership());

}



TEST(Appliance, switchon) {

  Appliance a;
  a.setAppliance(2);
  //EXPECT_FALSE(a.onAt(1));
  EXPECT_NEAR(0.0308,a.getMeanFraction(), 0.001);


}
*/
