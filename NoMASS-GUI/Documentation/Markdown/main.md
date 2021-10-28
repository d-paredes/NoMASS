# No-MASS-GUI                       {#mainpage}

[TOC]

<div id='Introduction'/>
## Introduction 					{#Introduction}
## Introduction

The No-MASS-GUI is a standalone tool that enable the No-MASS framework in building energy performance simulation tools such as EnergyPlus. 
For more details about the No-MASS framework (models of occupant interaction and appliance usage) refer to the No-MASS framework documentation.

The No-MASS framework relies on the fractional radiation transmitted through windows considering the proportion that shading devices are closed to enable interaction with shading devices.
EnergyPlus source code has been altered to allow the No-MASS access this estimate at each timestep during the co-simulation using the standard Functional Mock-Up Interface (FMI).

The modified source code has to be compiled to generate an executable version of EnergyPlus for the platform where building simulations are run. 
The process to build EnergyPlus on all platforms can be found at [https://github.com/NREL/EnergyPlus/wiki/BuildingEnergyPlus](https://github.com/NREL/EnergyPlus/wiki/BuildingEnergyPlus).
However, EnergyPlus does not support FMI on Mac OS.

<!-- 
The No-MASS framework is coupled to EnergyPlus simulations using an external interface. 
This allow the No-MASS framework to access variables such as mean air temperatura to estimate


The EnergyPlus source code was altered to provide a function
that reduces the radiation transmitted through the window in proportion to the fraction
that the shade was closed, this function can now be accessed from an external interface at
each timestep (see Appendix B for the source code changes).


EnergyPlus differences for allowing shading interactions.

To enable stochastic behaviours in the building performance, EnergyPlus source code has to be changed.
EnergyPlus differences for allowing shading interactions.

The process to generate a modified version of EnergyPlus is detailed in the following sections
-->

<div id='Pages'/>
## Pages 							{#Pages}
## Pages
* @subpage CompilingEnergyPlus
* @subpage Prerequisites
* @subpage Implementation
<!-- * @subpage ClassDiagram -->
<!-- * @subpage No-MASS-GUIClassDiagram -->
<!-- * @subpage EnergyPlusExamples -->
