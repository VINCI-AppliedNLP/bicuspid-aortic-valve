from medspacy.postprocess import Postprocessor, PostprocessingRule, PostprocessingPattern
from medspacy.postprocess import postprocessing_functions
from typing import Iterable, Union, Literal


# condition function 
def window_contains(ent, target):
    "Returns True if the window following an ent contains a target phrase (regex syntax)"
    wind = ent._.window(100, left=False, right=True)
    return postprocessing_functions.span_contains(wind, target, regex=True)


# action function
def set_bicuspid_struc(ent, i,    
                       input_type: Literal["ents", "group"] = "ents",
                       span_group_name: str = "medspacy_spans",
                       **kwargs
                       ): 
    ent._.structure_type = "BICUSPID_STRUCTURE"
    ent._.structure_text = "bicuspid"

def set_prosthetic(ent, i,
                       input_type: Literal["ents", "group"] = "ents",
                       span_group_name: str = "medspacy_spans",
                       **kwargs
                       ):
    ent._.is_prosthetic = True

def if_label(ent):
    return ent.label_ == "AORTIC_VALVE"

def if_type_none(ent):
    return ent._.structure_type == None

def if_type_bicusp(ent):
    return ent._.structure_type == "BICUSPID_STRUCTURE"


postprocess_rules = [
    PostprocessingRule(patterns=[
            # first select for aortic valve entities
            # then check if structure has already been set. If not, continue.
            PostprocessingPattern(if_label), # works
            PostprocessingPattern(if_type_none), # works

            # see if window following valve ent contains "bicuspid"
            PostprocessingPattern(window_contains, target="bicuspid"), # works

        ],
        action=set_bicuspid_struc,
        description="If an aortic valve does not have a structure within the same sentence, check the window for bicuspid terms."
    ),
    PostprocessingRule(patterns=[
        # first select for aortic valve entities
        # then check if structure has already been set. If not, continue.
        PostprocessingPattern(if_label),  # works
        PostprocessingPattern(if_type_bicusp),  # works

        # see if window following valve ent contains "aortic mechanical prosthesis"
        PostprocessingPattern(window_contains, target="aortic mechanical prosthesis"),
    ],
        action=set_prosthetic,
        description="pyrush sentencizer splits on period in St. Jude and prosthetic is missed. If a bicuspid aortic valve has 'aortic mechanical prosthesis' in the window following, set prosthetic flag to true."
    )
]