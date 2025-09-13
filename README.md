# <img src="icon.png" width=50/> QgisSweptPath

[![Static Badge](https://img.shields.io/badge/LICENSE-GPLv3-ad0000?style=for-the-badge&logoColor=%23ffffff&color=ad0000)](LICENSE)

QgisSweptPath is a plug-in for the open source GIS software QGIS for simple sweep curve checks.
The plug-in is primarily suitable for rough feasibility studies and does not claim to achieve the accuracy and depth of analysis
of professional sweep curve simulation programmes for CAD systems.

During the development of the plug-in, care is taken to ensure that the sweep paths correspond as closely as possible to real vehicles
and the simulation results are checked to the best of our knowledge and belief. Nevertheless, it cannot be guaranteed that
the simulation correctly reflects reality in all cases. The developers accept no responsibility for the correctness and
accuracy of the sweep path checks performed with this plug-in. The user is responsible for checking and validating the simulation results.

For the developers of QgisSweptPath, Lukas Gafner

---

## Installation  
In the current version, the plug-in has not yet been published on the official QGIS plug-in website. However, the plug-in can be downloaded from the GitHub page and installed manually. To install it, follow these steps:

1. Download the zip file [QgisSweptPath_0.0.1](.)
2. Open the plug-in manager in QGIS
3. Select **Install from ZIP** and install the downloaded file

## Features already available
- Manual control of vehicles 
- Overdriven and swept over areas (as lines) as QGIS layers
- One standard bus and one articulated bus
- Various options and settings for vehicle control
- User manual in german

## Planned features still under development
- Automatic driving along previously drawn lines
- Additional standard vehicles (buses and lorries)
- Simulation of vehicles with rear-wheel steering
- Automatic dissolving the swept over lines to areas
- Developer manual (including instructions for adding your own vehicles) 

More information on the development progress and planned features can be found directly on [GitHub](https://github.com/users/lugafner/projects/3/views/1)

---

[![Static Badge](https://img.shields.io/badge/Benutzerhandbuch-DE-ad0000?style=for-the-badge&logoColor=%23ffffff&color=ad0000)](qgissweptpath_de.md)
![Static Badge](https://img.shields.io/badge/User%20manual-EN-ad0000?style=for-the-badge&logoColor=%23ffffff&color=ad0000)
![Static Badge](https://img.shields.io/badge/Developer%20guide-EN-ad0000?style=for-the-badge&logoColor=%23ffffff&color=ad0000)
