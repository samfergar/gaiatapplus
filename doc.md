# Exomythology

# High-Level Project Summary
🌌 Since ancient times, humans have looked at the sky to admire the beauty of the stars ✨ and find in them answers to some of the most deepest questions of life. From generation to generation, the stars remain in the firmament, sheltering our earth and shining for us, but most importantly, serving as an excuse to reunite and tell **stories** 📖

Stargazing 🌠 serves as a way to sit in the pitch black night with our kin, our friends and our loved ones to tell stories of great warriors, fierceful beasts, love rendezvous and passionate friendships. Stories that were told some day centuries ago remain relevant today, passing between eras ⌛ and all across the world 🌎, adding our own twists and beliefs, helping each and one of us buid our cosmovision 🌌

But... What would these stars look like from other worlds? 🪐 What kind of stories could we tell if we saw them from other perspectives? 🔭

We want to bring back the warmth and familiarity that can only be obtained by reading stories in the breathtaking sky that sits above us 🌠, but seen from another world: an **exoplanet**. Our deepest desire is to make a place for reunion by finding out what kind of epic stories can be told reading the celestial bodies from a whole new perspective. We yearn for these stories to pass down between the new generations; let them take shape within the river of time ⏳ and the vision of new stargazers 🔭 in order to expand their horizons, just like it happened with the stories of our elders

**Exomythology** is an interactive 3D web platform 🌐 that allows users to create, explore, share and comment stories gazing at the stars, creating and admiring constellations standing on different exoplanets 🪐. Users will be able to live the ancient tradition of storytelling under the shiny sky of a planet light-years away from our earth 🌌, and it will enable and encourage them to share these stories among their peers 👥. **Exomythology** comes to bring back the curiosity and passion of our species for the most arcane knowledge found within the stars 🌠

# Link to Project Demo

Figma slides: https://www.figma.com/design/TieiGjp3bZEGPYUniJ0TG5/NASA-Space-Apps?node-id=18-30&node-type=canvas&t=7CySUYSDM01vARwV-0
Github repository for the project: https://github.com/Guaaay/exosky-react
Github repository for processing the data from Gaia: https://github.com/samfergar/gaiatapplus

# Link to Final Project

https://exomythology.earth/

# Detailed Project Description

## Web Development 
Exomythology is an interactive 3D web platform. 

The whole project uses a database (MariaDB) of exoplanets sourced from NASA Exoplanet Archive, along with a table of constellations created from the users. We access to the database using an API from both the client and the game to get all the data to display it on the *Exoplanets* and *Constellations* subpages.

**How to use Exomythology Web:**
First you can navigate to *Exoplanets* subsection and select one of them. Once you choose an exoplanet,  you can begin exploring the sky from that perspective and view all the constellations created. You also can select some stars creating a new constellation and writing your own mythology!

Next, you can go to Constellations subsection and see all the constellations created by other users and rate them. For each constellation, you will see the name, the mythology behind it, and an audio narration telling the story.

## Godot Constellation Engine

Exomythology uses a Godot Web App compiled to HTML5 using WebGL in the back. The game app is hosted on itch.io and retrieved by our server. It is rendered on the exomythology web app when an exoplanet has been selected. Using the exoplanet id and positional parameters, the game first generates a procedural terrain unique to the exoplanet, using the exoplanet id as a seed. The exoplanet's terrain color is also proceduraly chosen. The game then requests the star data (position and apparent glow) from our backend, and receives it already translated according to the mathematical framework we describe. It then renders a series of glowing spheres projected onto a celestial dome. The game also retrieves the already created constellations along with the stars they involve. The game allows the player to draw constellations between stars. Once drawn, the game will send a message to the surrounding javascript environment. The message is intercepted by the react app and the form to submit a new constellation is shown with the just selected star data.

## Graphic Identity
The exploration of the logo started out with the creation of a moodboard based on the key words from our value proposal. The moodboard provided us with a color palette and then we started with the font trial.

For the design of this logo, we used At Haüss which is a contemporary neo-grotesque typeface. It is a pure and elegant typeface that stands on a solid and balanced structure. Born for maximum performance in communication, and great to be used on interfaces due to its high legibility.

ExoMythology is a product that brings both technology and stories to the user, so we wanted to create a logo that reflected both our storytelling and how we were going to use technology to bring them to life.

## Mathematical Framework
Exomythology makes use of well established mathematical tools used in astronomical research, as well as some basic notions of algebra. In order to display a range of stars, we first do a selection based on perception of a distant body, being brightness the main contributor. After said selection, we project the stars on a plane tangent to the celestial globe, taking the distance of the most distant star as the radius. This projection is then normalized in a given range to fit in the dome projection. 

Firstly, given a set of celestial coordinates (corresponding to target stars), we make a conversion into cartesian coordinates and recalculate the relative position of stars with a simple vector subtraction. Then we set that point as our new origin and recalculate all distances. Distance is calculated in *parsecs* from *stellar parallax*. 

Transformation from stellar coordinates to cartesian coordinates is performed as follows:

$$
    x = r \cdot \cos(dec) \cos(Ra) \\
    y = r \cdot \cos(dec) \sin(Ra) \\
    z = r \cdot \sin(dec)
$$

Where $r$ is the distance (measured in *parsecs*) to the exoplanet or the sun, $Ra$ is the *right ascension* (i.e the "longitude" analogue, measured in *degrees*) and $dec$ is the *declination* (i.e the "latitude", measured in *degrees*).

We then use the following projection onto the plane. We only select the stars with a positive $z$ value to ensure we only display one hemisphere. To make all projected distances fit a convenient range, we then divide all distances by a normalization value. This is then served to the graphical interface to form the ***stellar dome***.

Lastly, projection onto the plane is performed as follows:

$$
    \sigma : \mathbb{R}³ \rightarrow \{ z=R \} \\
    \sigma(x,y,z) = (\frac{R\cdot x}{z}, \frac{R\cdot y}{z})  
$$

Where $\sigma$ is the orthogonal projection over the $z=R$ plane and $R = \max\{d(\bar{x}_{exoplanet}, \bar{x}) | \bar{x} \in S\}$ and $S$ is the set of star positions in cartesian coordinates such that $\bar{x}_{exoplanet} = (0,0,0)$

# NASA & Space Agency Partner Data

## Gaia DR3 Resources

* **<a href="https://astroquery.readthedocs.io/en/latest/gaia/gaia.html"> Python astroquery guide </a>**

* **<a href="https://gea.esac.esa.int/archive/"> Gaia Database </a>**

* **<a href="https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html"> Gaia DR3 documentation variable descriptions </a>**

## European Space Agency (ESA) Resources

This work has made use of data from the **<a href="https://www.cosmos.esa.int/gaia"> European Space Agency (ESA) mission Gaia </a>**, processed by the **<a href="https://www.cosmos.esa.int/web/gaia/dpac/consortium"> Gaia Data Processing and Analysis Consortium (DPAC) </a>**. Funding 
for the DPAC has been provided by national institutions, in particular the institutions participating in the **Gaia Multilateral Agreement**.

## National Aeronautics and Space Administration (NASA) Resources

This work has made use of the **<a href="https://exoplanetarchive.ipac.caltech.edu/docs/data.html"> NASA Exoplanet Archive </a>**, which is operated by the **California Institute of Technology**, 
under contract with the **National Aeronautics and Space Administration** under the **Exoplanet Exploration Program**.

# References

## Frontend Resources

* **<a href="https://ecma-international.org/publications-and-standards/standards/ecma-262/"> JavaScript </a>** (*ECMA International. (2024). Standard ECMA-262: ECMAScript® 2024 Language Specification*)

* **<a href="https://react.dev/"> React </a>** (*MIT License. Copyright (c) Meta Platforms, Inc. and affiliates*)

* **<a href="https://mui.com/material-ui/"> Material UI </a>** (*Open-core, MIT-licensed library*)

* **<a href="https://nodejs.org/en"> NodeJS </a>** (*MIT License. Copyright Node.js Website WG contributors. All rights reserved*)

## Backend Resources

* **<a href="https://godotengine.org/"> GODOT Engine </a>** (*Free and open source software released under the permissive MIT license*)

* **<a href="https://fastapi.tiangolo.com/"> FastAPI </a>** (*The MIT License (MIT). Copyright (c) 2018 Sebastián Ramírez*)

## Data Resources

* **<a href="https://www.python.org/"> Python </a>** (*Open Source*)

* **<a href="https://www.astropy.org/index.html"> Astropy </a>** (*BSD 3-Clause "New" or "Revised" License. Copyright (c) 2011-2024, Astropy Developers. All rights reserved*)

* **<a href="https://astroquery.readthedocs.io/en/latest/"> Astroquery </a>** (*BSD 3-Clause "New" or "Revised" License. Copyright (c) 2011-2024, Astroquery Developers. All rights reserved*)

* **<a href="https://mariadb.org/"> MariaDB </a>** (*GNU General Public License, version 2*)

## Design Resources

* **<a href="https://www.figma.com/es-la/"> Figma </a>** (*Collaborative web application for interface design*)

## Web & Hosting Resources

* **<a href="https://www.godaddy.com/es-es"> GoDaddy </a>** (*American publicly traded Internet domain registry, domain registrar and web hosting company*)

* **<a href="https://www.ovhcloud.com/en/vps/"> OVHCloud </a>** (*Virtual Private Server (VPS)*)

# Use of Artificial Intelligence

**Exomythology** is ✨*AI-Free*✨ and relies only on mathematical algorithms, a videogame engine and exquisite design in order to bring a cosmic experience.

Nevertheless, AI models such as *Chat-GPT* and *GitHub Copilot* were used to assist in the creation of the project. That way our team of mathematicians, developers and designers could focus on the most creative and critical tasks, optimizing the time spent in less-critical more mechanic tasks. 