# Backend structure

Backend is based on several components:

- Flask application for API
- UWSGI web server to serve the Flask application
- Redis in-memory database as a message broker between flask application and celery worker
- Celery task queue



## backend/flask_app

This folder contains two main files:
- `routes.py`. This file defines the routes used by the Flask app
- `tasks.py`. This file defines Celery tasks which should be executed in `routes.py`

## backend/common/utils

This folder contains different useful classes:

- `Exceptions.py`. This file contains, as the name suggests, custom exceptions used across the backend logic
- `Logger.py`. This file contains `myLogger` class which can be imported to other modules for logging.
- `RequestParser.py`. This file contains definition of RequestParser class which is used to parse the request coming to `/api/v1/optimize` endpoint
- `Datatypes.py`. This file contains definitions of main data structures.


## backend/common/constraints

This folder contains files related with everything needed to set up hard constraints for the optimization

- `UridineDepletion`. This file contains the custom specification to deplete the uridine on the third position of every codon
- `Constraints.py`. This file contains a `Constraints` class which is used in `Optimization.py` to collect and prepare all the required constraints for optimization: AvoidPattern, EnforceGCContent, AvoidCodon, UridineDepletion, EnforceTranslation, AvoidRareCodons

## backend/common/objectives

This folder contains everything related to creation of objectives (soft constraints for the optimization).

- `Dinucleotide_usage.py`. This file contains a logic to optimize for nucleotide pairs in sequence based on the usage frequency table exported from CoCoPUTs database.

- `Codon_pair_usage.py`. This file contains a logic to optimize for codon pairs usage statistics. It is based on the usage frequency table exported from CoCoPUTs database.

- `MFE_optimization.py`. This file contains custom specification for a new optimization objective - MFE optimization. It uses two possible algorithms - one from RNAfold (ViennaRNA) package, another one is a custom algorithm defined in `MFE.py`

- `MFE.py`. This file contains a custom MFE estimation algorithm which is base on publication: *Nucleic Acids Research, 2013, Vol. 41, No. 6 e73: ['mRNA secondary structure optimization using a correlated stem–loop prediction'](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4914086/)*

- `Objectives.py`. This file contains the logic to set up and prepare all the objectives for further optimization: MatchTargetCodonUsage, EnforceGCContent, MinimizeMFE, MatchTargetPairUsage.

## backend/tests

As the name implies, this folder contains unit tests for the main functionality of the application.
