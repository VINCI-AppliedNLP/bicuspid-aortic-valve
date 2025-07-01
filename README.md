This natural language processing (NLP) system identifies heart valves and their associated leaflet structures in echo reports. 
It is specifically designed to identify bicuspid aortic valves, an abnormality that affects approximately 1% of the population.  
It was developed using medspacy, a library for performing clinical NLP with the spaCy framework.
The system first identifies all heart valve terms in the document. This includes the four normal heart valves and prosthetic valves. 
Then the sentence is searched for structure terms – bicuspid, tricuspid, and normal – and the closest is attached to the valve term.  
Echo reports frequently include hedging statements (i.e., “Cannot rule out bicuspid aortic valve.”), so ConText is used to identify uncertainty and negation. 
Finally, for instances where an aortic valve is not attached to a structure in the same sentence, 
a window of text around the valve term that is larger than the sentence is created, and the system searches for bicuspid terms.
