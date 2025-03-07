# import spacy
from spacy import Language
import os
import medspacy
# from spacy.tokens import Span
from medspacy.target_matcher import TargetRule
# from medspacy.context import ConTextRule, ConText
# from medspacy.postprocess import Postprocessor, PostprocessingRule, PostprocessingPattern
# from medspacy.postprocess import postprocessing_functions
# from typing import Iterable, Union, Literal
# import os

# pycharm will say this is unused, but it's needed to register the component factory
# from src.pipeline_components import ValveStrucRel
from .pipeline_components import ValveStrucRel

# from resources import postprocess_rules
from .pipeline_components import postprocess_rules
from medspacy.preprocess import Preprocessor, PreprocessingRule
from spacy.util import compile_infix_regex, compile_prefix_regex,compile_suffix_regex


def nlp_factory(**kwargs) -> Language:
    '''
    Creates a spacy model for the project.

    Args:
        **kwargs: all keyword arguemnts needed to initialize the spacy model. In the deployment pipeline, this sends in
            configs for including a doc consumer.

    Returns:
        The NLP object for the project.
    '''

    nlp = medspacy.load(medspacy_enable=["medspacy_pyrush"])

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))
    valve_rules_path = os.path.join(base_path, 'valve_ent_rules.json')
    context_rules_path = os.path.join(base_path, 'context_rules.json')
    structure_rules_path = os.path.join(base_path, 'structure_rules.json')
    # load target_matcher - valve ents
    valve_rules = TargetRule.from_json(valve_rules_path)
    target_matcher = nlp.add_pipe("medspacy_target_matcher")
    target_matcher.add(valve_rules)

    # context
    nlp.add_pipe("medspacy_context"
                 , config={
            "rules": context_rules_path})

    # structures
    nlp.add_pipe("medspacy_context",
                 name='structures',
                 after='medspacy_context',
                 config={
                     "rules": structure_rules_path,
                     "span_attrs": None})

    # connect valves and structures - custom component in the pipeline components folder
    nlp.add_pipe("valve_struc_relationship",
                 after='structures')

    # postprocessor
    postprocessor = nlp.add_pipe("medspacy_postprocessor", after='valve_struc_relationship')
    postprocessor.add(postprocess_rules.postprocess_rules)

    # DocConsumer - needed to run the deployment_pipeline.py
    if "cols" in kwargs.keys():
        nlp.add_pipe("medspacy_doc_consumer", config={"dtype_attrs": {"ents": kwargs["cols"][1:]}})

    return nlp

