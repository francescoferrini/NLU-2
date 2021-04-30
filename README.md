# NLU-2

For this assignement there are:
- dada directory with the txt files
- utils.py and conll.py with some important functions used in the main files
- 3 main files, one for each point of the assignement

The requirements are spacy, pandas and sklearn. 


- **using pip:**
  ```
  pip install -U spacy
  python -m spacy download en_core_web_sm
  ```
  
- **using conda:**
  ```
  conda install -c conda-forge spacy
  python -m spacy download en_core_web_sm
  ```
  
- **from source:**
  ```
  pip install -U pip setuptools wheel
  git clone https://github.com/explosion/spaCy
  cd spaCy
  pip install -r requirements.txt
  python setup.py build_ext --inplace
  pip install .
  python -m spacy download en_core_web_sm
  ```
