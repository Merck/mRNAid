# mRNAid: mRNA optimization tool

![PyPI - Version](https://img.shields.io/pypi/v/mRNAid)

mRNAid is an experimentally validated open-source tool for optimization and visualisation of mRNA molecules. It features
 different optimization strategies based on user preferences.

mRNAid is available at: [https://mrnaid.dichlab.org](https://mrnaid.dichlab.org)

More information about the tool and experiments performed for its evaluation is available in the following publication:

> Nikita Vostrosablin, Shuhui Lim, Pooja Gopal, Kveta Brazdilova, Sushmita Parajuli, Xiaona Wei, Anna Gromek, 
>Martin Spale, Anja Muzdalo, Constance Yeo, Joanna Wardyn, Petr Mejzlik, Brian Henry, Anthony W Partridge and 
>Danny A. Bitton: **mRNAid, an Open-Source Platform for Therapeutic mRNA Design and Optimization Strategies**, 2022
> 
>[bioRxiv link](https://www.biorxiv.org/content/10.1101/2022.04.04.486952v1)

You can find brief manual on how to use the tool [here](./usage_manual/Manual.md).

## Command-line interface setup

Install mRNAid with pip:
```bash
pip install mRNAid
```

See help using:
```bash
mrnaid optimize --help
```

Example:
```bash
mrnaid optimize \
  --output example.json \
  --five-end ATG \
  --three-end CGG \
  --input-mRNA AGCAGAGAAGGCGGAAGCAGTGGCGTCCGCAGCTGGGGCTTGGCCTGCGGGCGGCCAGCGAAGGTGGCGAAGGCTCCCACTGGATCCAGAGTTTGCCGTCCAAGCAGCCTCGTCTCGGCGCGCAGTGTCTGTGTCCGTCCTCTACCAGCGCCTTGGCTGAGCGGAGTCGTGCGGTTGGTGGGGGAGCCCTGCCCTCCTGGTTCGGCCTCCCCGCGCACTAGAACGATCATGAACTTCTGAAGGGACCCAGCTTTCTTTGTGTGCTCCAAGTGATTTGCACAAATAATAATATATATATTTATTGAAGGAGAGAATCAGAGCAAGTGATAATCAAGTTACTATGAGTCTGCTAAACTGTGAAAACAGCTGTGGATCCAGCCAGTCTGAAAGTGACTGCTGTGTGGCCATGGCCAGCTCCTGTAGCGCTGTAACAAAAGATGATAGTGTGGGTGGAACTGCCAGCACGGGGAACCTCTCCAGCTCATTTATGGAGGAGATCCAGGGATATGATGTAGAGTTTGACCCACCCCTGGAAAGCAAGTATGAATGCCCCATCTGCTTGATGGCATTACGAGAAGCAGTGCAAACGCCATGCGGCCATAGGTTCTGCAAAGCCTGCATCATAAAATCAATAAGGGATGCAGGTCACAAATGTCCAGTTGACAATGAAATACTGCTGGAAAATCAACTATTTCCAGACAATTTTGCAAAACGTGAGATTCTTTCTCTGATGGTGAAATGTCCAAATGAAGGTTGTTTGCACAAGATGGAACTGAGACATCTTGAGGATCATCAAGCACATTGTGAGTTTGCTCTTATGGATTGTCCCCAATGCCAGCGTCCCTTCCAAAAATTCCATATTAATATTCACATTCTGAAGGATTGTCCAAGGAGACAGGTTTCTTGTGACAACTGTGCTGCATCAATGGCATTTGAAGATAAAGAGATCCATGACCAGAACTGTCCTTTGGCAAATGTCATCTGTGAATACTGCAATACTATACTCATCAGAGAACAGATGCCTAATCATTATGATCTAGACTGCCCTACAGCCCCAATTCCATGCACATTCAGTACTTTTGGTTGCCATGAAAAGATGCAGAGGAATCACTTGGCACGCCACCTACAAGAGAACACCCAGTCACACATGAGAATGTTGGCCCAGGCTGTTCATAGTTTGAGCGTTATACCCGACTCTGGGTATATCTCAGAGGTCCGGAATTTCCAGGAAACTATTCACCAGTTAGAGGGTCGCCTTGTAAGACAAGACCATCAAATCCGGGAGCTGACTGCTAAAATGGAAACTCAGAGTATGTATGTAAGTGAGCT 
```

You can also invoke mRNAid directly from Python:
```python
from mrnaid import optimize

optimize(
    input_mrna='AGCAGAGAAGGCGGAAGCAGTGGCGTCCGCAGCTGGGGCTTGGCCTGCGGGCGGCCAGCGAAGGTGGCGAAGGCTCCCACTGGATCCAGAGTTTGCCGTCCAAGCAGCCTCGTCTCGGCGCGCAGTGTCTGTGTCCGTCCTCTACCAGCGCCTTGGCTGAGCGGAGTCGTGCGGTTGGTGGGGGAGCCCTGCCCTCCTGGTTCGGCCTCCCCGCGCACTAGAACGATCATGAACTTCTGAAGGGACCCAGCTTTCTTTGTGTGCTCCAAGTGATTTGCACAAATAATAATATATATATTTATTGAAGGAGAGAATCAGAGCAAGTGATAATCAAGTTACTATGAGTCTGCTAAACTGTGAAAACAGCTGTGGATCCAGCCAGTCTGAAAGTGACTGCTGTGTGGCCATGGCCAGCTCCTGTAGCGCTGTAACAAAAGATGATAGTGTGGGTGGAACTGCCAGCACGGGGAACCTCTCCAGCTCATTTATGGAGGAGATCCAGGGATATGATGTAGAGTTTGACCCACCCCTGGAAAGCAAGTATGAATGCCCCATCTGCTTGATGGCATTACGAGAAGCAGTGCAAACGCCATGCGGCCATAGGTTCTGCAAAGCCTGCATCATAAAATCAATAAGGGATGCAGGTCACAAATGTCCAGTTGACAATGAAATACTGCTGGAAAATCAACTATTTCCAGACAATTTTGCAAAACGTGAGATTCTTTCTCTGATGGTGAAATGTCCAAATGAAGGTTGTTTGCACAAGATGGAACTGAGACATCTTGAGGATCATCAAGCACATTGTGAGTTTGCTCTTATGGATTGTCCCCAATGCCAGCGTCCCTTCCAAAAATTCCATATTAATATTCACATTCTGAAGGATTGTCCAAGGAGACAGGTTTCTTGTGACAACTGTGCTGCATCAATGGCATTTGAAGATAAAGAGATCCATGACCAGAACTGTCCTTTGGCAAATGTCATCTGTGAATACTGCAATACTATACTCATCAGAGAACAGATGCCTAATCATTATGATCTAGACTGCCCTACAGCCCCAATTCCATGCACATTCAGTACTTTTGGTTGCCATGAAAAGATGCAGAGGAATCACTTGGCACGCCACCTACAAGAGAACACCCAGTCACACATGAGAATGTTGGCCCAGGCTGTTCATAGTTTGAGCGTTATACCCGACTCTGGGTATATCTCAGAGGTCCGGAATTTCCAGGAAACTATTCACCAGTTAGAGGGTCGCCTTGTAAGACAAGACCATCAAATCCGGGAGCTGACTGCTAAAATGGAAACTCAGAGTATGTATGTAAGTGAGCT',
    five_end='ATG',
    three_end='CGG'
)
```

## Local web server setup

If you don't want to use public server you can install this tool locally on your machine.

### 1. Using docker-compose

The easiest way to run the tool locally is to use `docker`. You will have to install docker first and it should either
contain `docker-compose` utility as a part of the distribution or you will need to 
[install it](https://docs.docker.com/compose/install/) separately.

Navigate to the project folder and execute:


```bash
docker-compose up --build
```

The tool will be available at [http://localhost/](http://localhost/)

### 2. Without docker

To be able to run the tool without `docker` you will need to run frontend and backend separately.

#### Backend

You need [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html) or one of 
the alternatives ([Miniconda](https://docs.conda.io/en/latest/miniconda.html), [Miniforge](https://github.com/conda-forge/miniforge)) 
being installed.
Navigate to the `backend/flask_app/` directory and execute following commands:

* Create a new virtual environment:

```bash
make env-create
```

* Install redis database

```bash
make redis-install
```

- In separate terminals execute following commands:
    1. Start redis server: `make redis-run`
    2. Start uwsgi server: `make uwsgi-run`
    3. Start celery: `make celery-run`

- After these steps are executed, the job submission is available at the "optimize" API url: http://localhost/api/v1/optimize.
Example of the json submitted to the "optimize" end point:

```json
{
  "config": {
    "avoided_motifs": ["EcoRI", "UUU"],
    "codon_usage_frequency_threshold": 0.1,
	"max_GC_content": 0.9,
	"min_GC_content": 0.5,
	"GC_window_size": 100,
	"organism": "m_musculus",
	"entropy_window": 30,
  "number_of_sequences": 2
  },
  "dinucleotides": false, 
  "match_codon_pair": false,
  "uridine_depletion": true,
  "CAI": false,
  "precise_MFE_algorithm": true,
  "file_name": "test",
  "sequences": {
    "five_end_flanking_sequence": "UGAAUUCAGCAAUCU",
    "gene_of_interest": "AAUCAAAUAGGGUUAAGUCUAGGAUUGUUAGUCUGCUAAGGUCUGCAGUUACUGUGUCUACUGAUGAUAGUUCGCAUUGACAAU",
    "three_end_flanking_sequence": "GC"
  }
}
```

- The job execution results are available at: http://localhost/api/v1/status/task-id, where `task-id` should be 
replaced with actual task id received after the request is submitted to the "optimize" API




   
##### Running the tests

To be able to execute tests for backend with pytest, you need to set up following environmental variables in the corresponding
environment:

- PYTHONPATH=..:../common:../flask_app
- LOG_FILE=../flask_app/logs/logs.log
- BACKEND_OBJECTIVES_DATA=../common/objectives/data

Tests can be found in `backend/tests/` directory

#### Frontend

Install [Node.js](https://nodejs.org/en/download/) and [Nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/) 
web server.

* Navigate to `frontend` directory
* Build a package:

```bash
npm ci && npm run build
```

* Remove default nginx configurations from nginx system directory

```bash
# location may vary based on your system and installation
rm /etc/nginx/conf.d/default.conf
```

* Replace deleted configs with custom ones
```bash
# target location may vary based on your system and installation
cp ./config/nginx.conf /etc/nginx/conf.d/
```

* Move build files to the corresponding nginx directory
```bash
cp -R ./build/* /usr/share/nginx/html
```

* Restart nginx web server



## Contributing

mRNAid is an open platform, please propose your changes and improvements. This can be done through the [Issues](link)
tab.
## License

Released under MIT License

