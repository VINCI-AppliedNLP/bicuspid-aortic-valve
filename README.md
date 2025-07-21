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

### Pipeline Logic Diagram

<img width="1300" height="1881" alt="pipeline_diagram" src="https://github.com/user-attachments/assets/c8f56eab-ee2b-46ae-9e04-f57bd8455afb" />

## Running the System

Open the code in IDE of your preference. We recommend PyCharm Community version [ [https://www.jetbrains.com/pycharm/download] or VS Code [https://code.visualstudio.com/].

