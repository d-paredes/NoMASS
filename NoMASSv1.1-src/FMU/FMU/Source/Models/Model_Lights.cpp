// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <algorithm>

#include <Utility/Utility.hpp>

#include "Model_Lights.hpp"

//**********************************************************************

Model_Lights::Model_Lights() {}

// SIMULATION OF ACTIONS ON ELECTRICAL LIGHTING
// ACCORDING TO LIGHTSWITCH-2002 MODEL
// Christoph F. Reinhart, Lightswitch-2002:
// a model for manual and automated control of electric lighting and blinds,
// Solar Energy 77 (2004) 15-28

// Input parameters:
// Lumint: Indoor illuminance next to window (lux)

// computing the inside illuminance according
// as a sum of all walls' contributions //
// Dont have this figure
// float Lumint = pZone->getTotalInternalIlluminance0();

bool Model_Lights::arrival(bool state, double Lumint)
    {
    float a01arr = -0.0175;
    float b01arr = -4.0835;
    float c01arr = 1.0361;
    float m01arr = 1.8223;
    bool currentLightState = state;
    if (!state)
        {
        // Hunt D R G, 1980. Predicting artificial lighting use a method based upon observed patterns of behavior. Lighting Research & Technology 12[1], 7-14.
        // --- 2a. If the light is already off when occupant arrives ----------
        float probonarr;  //  hunt 1980 model
        float log10lumint = 0;
        if (Lumint > 0)
            {
            log10lumint = std::log10(Lumint);
            }

        if (log10lumint <= 0.843f)
            {
            probonarr = 1.f;
            }
        else if (log10lumint >= 2.818f)
            {
            probonarr = 0.f;
            }
        else
            {
            float log10lumintm01arr = 0;
            if (Lumint - m01arr > 0)
                {
                log10lumintm01arr = log10(Lumint - m01arr);
                }
            probonarr = a01arr + c01arr /
                        (1.f + exp(-b01arr * (log10lumintm01arr)));
            }
        // usage of the probability to define the lights state
        if (Utility::randomDouble(0.0, 1.0) < probonarr)
            {
            currentLightState = 1.f;
            }
        else
            {
            currentLightState = 0.f;
            }
        }
    return currentLightState;
    }

bool Model_Lights::intermediate(bool state, double Lumint)
    {
    float a01int = 0.0027;
    float b01int = 0.017;
    float c01int = -64.19;
    float d01int = 2.41;

    // === 3. Case during presence =============================================
    bool currentLightState = state;
    if (!state)
        {
        // --- 3a. If the light is already off at the previous time step -------
        float probonint = 0.f;
        if (Lumint == 0.f)
            {
            probonint = 1.f;
            }
        else
            {
            if (Lumint - d01int > 0)
                {
                probonint = a01int + b01int /
                            (c01int * (log10(Lumint - d01int)));
                }
            }
        // usage of the probability to define the lights state
        if (Utility::randomDouble(0.0, 1.0) < probonint)
            {
            currentLightState = 1.f;
            }
        else
            {
            currentLightState = 0.f;
            }
        }
    return currentLightState;
    }

bool Model_Lights::departure(bool state, double futureDuration)
    {
    bool currentLightState = state;
    if (state)
        {
        // --- 4b. If the light is already on when occupant leaves -------------
        float proboffdep;
        if (futureDuration < 30.f * 60.f)
            {
            proboffdep = 0.086f;
            }
        else if (futureDuration < 60.f * 60.f)
            {
            proboffdep = 0.314f;
            }
        else if (futureDuration < 2.f * 60.f * 60.f)
            {
            proboffdep = 0.380f;
            }
        else if (futureDuration < 4.f * 60.f * 60.f)
            {
            proboffdep = 0.600f;
            }
        else if (futureDuration < 12.f * 60.f * 60.f)
            {
            proboffdep = 0.960f;
            }
        else
            {
            proboffdep = 1.f;
            }
        // NOTE: These probabilities are based on Pigg, Eilers, Reed,
        // Behavioral Aspects of Lighting and Occupancy Sensors in
        // Private Offices: A Case Study of a University Office Building
        // usage of the probability to define the lights state
        if (Utility::randomDouble(0.0, 1.0) < proboffdep)
            {
            currentLightState = 0.f;
            }
        else
            {
            currentLightState = 1.f;
            }
        }
    return currentLightState;
    }

//**********************************************************************
