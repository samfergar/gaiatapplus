# Project Name
**Exomythology**

# High-Level Project Summary
🌌 Since ancient times, humans have looked at the sky to admire the beauty of the stars ✨ and find in them answers to some of the most deepest questions of life. From generation to generation, the stars remain in the firmament, sheltering our earth and shining for us, but most importantly, serving as an excuse to reunite and tell **stories** 📖

Stargazing 🌠 serves as a way to sit in the pitch black night with our kin, our friends and our loved ones to tell stories of great warriors, fierceful beasts, love rendezvous and passionate friendships. Stories that were told some day centuries ago remain relevant today, passing between eras ⌛ and all across the world 🌎, adding our own twists and beliefs, helping each and one of us buid our cosmovision 🌌

But... What would these stars look like from other worlds? 🪐 What kind of stories could we tell if we saw them from other perspectives? 🔭

We want to bring back the warmth and familiarity that can only be obtained by reading stories in the breathtaking sky that sits above us 🌠, but seen from another world: an **exoplanet**. Our deepest desire is to make a place for reunion by finding out what kind of epic stories can be told reading the celestial bodies from a whole new perspective. We yearn for these stories to pass down between the new generations; let them take shape within the river of time ⏳ and the vision of new stargazers 🔭 in order to expand their horizons, just like it happened with the stories of our elders

**Exomythology** is an interactive 3D web platform 🌐 that allows users to create, explore, share and comment stories gazing at the stars, creating and admiring constellations standing on different exoplanets 🪐. Users will be able to live the ancient tradition of storytelling under the shiny sky of a planet light-years away from our earth 🌌, and it will enable and encourage them to share these stories among their peers 👥. **Exomythology** comes to bring back the curiosity and passion of our species for the most arcane knowledge found within the stars 🌠

# Link to Project Demo

# Link to Final Project

# Detailed Project Description

## Mathematical Framework
Exomythology makes use of well established mathematical tools used in astronomical research, as well as some basic notions of algebra. In order to display a range of stars, we first do a selection based on perception of a distant body, being brightness the main contributor. After said selection, we project the stars on a cenital plane tangent to the celestial globe, taking the distance of the most distant star as the radius. This projection is then normalized in a given range to fit in the dome projection. 

Firstly, given a set of celestial coordinates (corresponding to target stars), we make a conversion into cartesian coordinates and recalculate the relative position of stars with a simple vector subtraction. Then we set that point as our new origin and recalculate all distances. Distance is calculated in parsecs from stellar parallax. 

$$
    x = r \cdot \cos(dec) \cos(Ra) \\
    y = r \cdot \cos(dec) \sin(Ra) \\
    z = r \cdot \sin(dec)
$$

Where $r$ is the distance (measured in *parsecs*) to the exoplanet or the sun, $Ra$ is the *right ascension* (i.e the "longitude" analogue, measured in *degrees*) and $dec$ is the *declination* (i.e the "latitude", measured in *degrees*).

We then use the following projection onto the cenital plane. We only select the stars with a positive z value to ensure we only display one hemisphere. To make all projected distances fit a convenient range, we then divide all distances by a normalization value. This is then served to the graphical interface to form the stellar dome.

$$
    \sigma : \mathbb{R}³ \rightarrow \{ z=R \} \\
    \sigma(x,y,z) = (\frac{R\cdot x}{z}, \frac{R\cdot y}{z})  
$$

Where $\sigma$ is the orthogonal projection over the $z=R$ plane and $R = \max\{d(\bar{x}_{exoplanet}, \bar{x}) | \bar{x} \in S\}$ and $S$ is the set of star positions in cartesian coordinates such that $\bar{x}_{exoplanet} = (0,0,0)$





# NASA & Space Agency Partner Data

-Gaia DR3 links
Python astroquery guide: https://astroquery.readthedocs.io/en/latest/gaia/gaia.html
Gaia Database: https://gea.esac.esa.int/archive/
Gaia DR3 documentation variable descriptions: https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html

This work has made use of data from the European Space Agency (ESA) mission Gaia (https://www.cosmos.esa.int/gaia), processed by the Gaia Data Processing and Analysis Consortium (DPAC, https://www.cosmos.esa.int/web/gaia/dpac/consortium). Funding 
for the DPAC has been provided by national institutions, in particular the institutions participating in the Gaia Multilateral Agreement.

-Exoplanet Archive
https://exoplanetarchive.ipac.caltech.edu/docs/data.html

This work has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, 
under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.

# References

* **<a href="https://ecma-international.org/publications-and-standards/standards/ecma-262/"> JavaScript </a>** (*ECMA International. (2024). Standard ECMA-262: ECMAScript® 2024 Language Specification*)

* **<a href="https://react.dev/"> React </a>** (*MIT License. Copyright (c) Meta Platforms, Inc. and affiliates*)

* **<a href="https://mui.com/material-ui/"> Material UI </a>** (*Open-core, MIT-licensed library*)

* **<a href="https://nodejs.org/en"> NodeJS </a>** (*MIT License. Copyright Node.js Website WG contributors. All rights reserved*)

* **<a href="https://godotengine.org/"> GODOT Engine </a>** (*Free and open source software released under the permissive MIT license*)

* **<a href="https://www.python.org/"> Python </a>** (*Open Source*)

* **<a href="https://www.astropy.org/index.html"> Astropy </a>** (*BSD 3-Clause "New" or "Revised" License. Copyright (c) 2011-2024, Astropy Developers. All rights reserved*)

* **<a href="https://astroquery.readthedocs.io/en/latest/"> Astroquery </a>** (*BSD 3-Clause "New" or "Revised" License. Copyright (c) 2011-2024, Astroquery Developers. All rights reserved*)

* **<a href="https://fastapi.tiangolo.com/"> FastAPI </a>** (*The MIT License (MIT). Copyright (c) 2018 Sebastián Ramírez*)

* **<a href="https://mariadb.org/"> MariaDB </a>** (*GNU General Public License, version 2*)

* **<a href="https://www.figma.com/es-la/"> Figma </a>** (*Collaborative web application for interface design*)

* **<a href="https://www.godaddy.com/es-es"> GoDaddy </a>** (*American publicly traded Internet domain registry, domain registrar and web hosting company*)

* **<a href="https://www.ovhcloud.com/en/vps/"> OVHCloud </a>** (*Virtual Private Server (VPS)*)

# Use of Artificial Intelligence