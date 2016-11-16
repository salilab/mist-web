[![Build Status](https://travis-ci.org/salilab/mist-web.svg?branch=master)](https://travis-ci.org/salilab/mist-web)
[![codecov](https://codecov.io/gh/salilab/mist-web/branch/master/graph/badge.svg)](https://codecov.io/gh/salilab/mist-web)

This is the source code for [MiST](https://salilab.org/mist/), a web
service for scoring of affinity purification-mass spectrometry data.
It uses the [Sali lab web framework](https://github.com/salilab/saliweb/).

See [S. Jäger, P. Cimermancic et al., Nature, (2011) 481, 365-70](https://www.ncbi.nlm.nih.gov/pubmed/22190034) for details.

# Setup

First, install and set up the
[Sali lab web framework](https://github.com/salilab/saliweb/) and the
base [MiST algorithm](https://github.com/salilab/mist/).

The web service expects to find a `mist` [module](http://modules.sourceforge.net/),
i.e. it runs `module load mist`. This module should put the `MiST.py` script
in the system PATH. This location must be on a network filesystem that is
visible to all nodes in the compute cluster.

