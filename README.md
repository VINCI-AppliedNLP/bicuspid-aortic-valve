# Heart Valve Leaflet Structure NLP System

If using the system, please cite:

Annie E. Bowles, Julie A. Lynch, Francisca Bermudez, Gabrielle E. Shakt, Tia DiNatale, Kathryn M. Pridgen, Renae L. Judy, Michael G. Levin, Katherine Hartmann, Scott M. Damrauer, Patrick R. Alba. Automated detection of bicuspid aortic valve from echocardiographic reports using natural language processing: a large-scale Veterans Affairs study. medRxiv. 2025.

```
@article{10.1101/2025.06.30.25330573,
    author = {Annie E. Bowles, Julie A. Lynch, Francisca Bermudez, Gabrielle E. Shakt, Tia DiNatale, Kathryn M. Pridgen, Renae L. Judy, Michael G. Levin, Katherine Hartmann, Scott M. Damrauer, Patrick R. Alba},
    title = "{Automated detection of bicuspid aortic valve from echocardiographic reports using natural language processing: a large-scale Veterans Affairs study}",
    journal = {medRxiv},
    year = {2025},
    month = {06},
    doi = {10.1101/2025.06.30.25330573},
    url = {https://www.medrxiv.org/content/10.1101/2025.06.30.25330573v1},
}
````
## Overview
This natural language processing (NLP) system identifies heart valves and their associated leaflet structures in echo reports. 
It is specifically designed to identify bicuspid aortic valves, an abnormality that affects approximately 1% of the population.  
It was developed using medspacy, a library for performing clinical NLP with the spaCy framework. For more info on medspacy, see [https://github.com/medspacy/medspacy] .
The system first identifies all heart valve terms in the document. This includes the four normal heart valves and prosthetic valves. 
Then the sentence is searched for structure terms – bicuspid, tricuspid, and normal – and the closest is attached to the valve term.  
Echo reports frequently include hedging statements (i.e., “Cannot rule out bicuspid aortic valve.”), so ConText is used to identify uncertainty and negation. 
Finally, for instances where an aortic valve is not attached to a structure in the same sentence, 
a window of text around the valve term that is larger than the sentence is created, and the system searches for bicuspid terms.

### System Performance

| **Heart Valve**       | **Precision** | **Recall** | **F1 Score** | **Support** |
|-----------------------|---------------|------------|--------------|-------------|
| Aortic                | 0.894         | 0.948      | 0.921        | 116         |
| Bicuspid aortic valve |         0.984 |      0.955 |        0.969 |          64 |
| Mitral                | 0.914         | 0.883      | 0.898        | 60          |
| Pulmonary             | 0.839         | 0.940      | 0.887        | 50          |
| Tricuspid             | 0.934         | 0.955      | 0.944        | 89          |
| **Overall**           | 0.899         | 0.937      | 0.918        | 315         |

System performance on the identification of each heart valve and corresponding leaflet structure. 
Support is the number of annotated heart valves where the leaflet structure is given. 

### Pipeline Logic Diagram

<img width="1300" height="1881" alt="pipeline_diagram" src="https://github.com/user-attachments/assets/c8f56eab-ee2b-46ae-9e04-f57bd8455afb" />

## Running the System

Open the code in IDE of your preference. We recommend PyCharm Community version [ [https://www.jetbrains.com/pycharm/download] or VS Code [https://code.visualstudio.com/].

`src\pipeline_creator.py` creates the NLP object for the project. Single documents can be tested with `src\testing_pipeline.py`. 

If processing mutiple documents, we recommend using the medSpaCy io functionality. [https://github.com/medspacy/medspacy/blob/34dbfc3c4a756a2fb96570806bb781e4dc0239ca/medspacy/io/config_example.py#L120]

Use these configurations in `config_example.py`:
    
    from src.pipeline_creator import nlp_factory
    
    #####################################################
    # DATA FORMAT CONFIG
    # Specify the columns names and types in the output
    # table. ID column should be at index 0.
    #
    # Note: This is not yet fully configurable. It is
    # dependent on the configuration of the DocConsumer
    # shown later.
    row_type = "ent"  # 'ent' or 'section'
    if row_type == "ent":
        # ENT OPTIONS:
        #   DEFAULT: text (str), start_char (str), end_char (str), label_ (str)
        #   CONTEXT: is_family (bool), is_negated (bool), is_uncertain (bool),
        #            is_hypothetical (bool), is_historical (bool)
        #   SECTION: section_title (str), section_parent (str)
        cols = [
            "id", #source document identifier
            "label", #valve_type
            "text", #valve_text
            "structure_type",
            "structure_text",
            "is_uncertain",
            "is_negated",
            "is_historical",
            "is_prosthetic",
            "is_functional",
            "snippet", #text surrounding the valve term that is larger than the sentence
            "start_char",
            "end_char",
            "label_"
        ]
        col_types = [
            "bigint",
            "varchar(50)",
            "varchar(100)",
            "varchar(50)",
            "varchar(100)",
            "bit",
            "bit",
            "bit",
            "bit",
            "bit",
            "varchar(max)", #can reduce if source documents are not above a certain length
            "int",
            "int"
        ]
    #####################################################
    # NLP FACTORY
    # initialize or call a method to produce your custom
    # NLP pipeline here.
    #
    # NOTE: DocConsumer MUST be present at the end.
    nlp = nlp_factory(consumer=True, cols=cols)
    #####################################################
