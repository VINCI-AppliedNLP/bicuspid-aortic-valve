import spacy
from spacy import Language
from spacy.language import Doc
from spacy.tokens import Span


# component name is set here. this will be used in spacy.add_pipe("valve_struc_relationship")
@Language.factory("valve_struc_relationship")
class ValveStrucRel:
    """
    Create _.structure_type and _.structure_text extensions, then create a relationship between the valve and structure terms.
    """

    def __init__(self, nlp: Language, name = "valve_struc_relationship"):
        """
        Initialize my component

        Args:
            nlp: The spacy Language object for the nlp pipeline
            name: The name of the pipeline component
        """
        self.nlp = nlp
        self.my_configs = "set any initialization in __init__"

        # set a basic extension for the pipeline to use
        # note use of the _ in hasattr. We want to check extensions in spacy's custom attribute space
        # if not hasattr(Token._, "my_extension"):
        # Token.set_extension("my_extension", default = None)

        if not hasattr(Span._, "structure_type"):
            Span.set_extension("structure_type", default=None, force=True)
            Span.set_extension("structure_text", default=None, force=True)

            Span.set_extension("is_functional", default=False, force=True)
            Span.set_extension("is_prosthetic", default=False, force=True)
            Span.set_extension("snippet", default=False, force=True) # = 'window'# , where window = window(100, left=True, right=True)

    def set_all_attrs(self, doc):
        """
        First assigns bicuspid modifier if present, then tricuspid modifier, then normal modifier.
        When all 3 categories were in the same if statement, and 2 modifiers were in the same sentence, the second modifier would overwrite the first.
        For example, "The aortic valve is a tricuspid structure with normal leaflet thickness and mobility." normal overwrote tricuspid.

        In the future, figure out how to assign the modifier that is CLOSEST to the ent - use the span indexes
        """
        for ent in doc.ents:
            # set snippet for doc consumer
            ent._.snippet = ent._.window(100, left=True, right=True).text

            for mod in ent._.modifiers:
                if mod.category == 'FUNC_BICUSPID_STRUCTURE':
                    span = doc[mod.modifier_span[0]: mod.modifier_span[1]]
                    ent._.structure_text = span.text
                    ent._.structure_type = "BICUSPID_STRUCTURE"
                    ent._.is_functional = True
                elif mod.category == 'BICUSPID_STRUCTURE':  # or mod.category == 'TRICUSPID_STRUCTURE':# or mod.category == 'NORMAL_STRUCTURE':
                    span = doc[mod.modifier_span[0]: mod.modifier_span[1]]
                    ent._.structure_text = span.text
                    ent._.structure_type = mod.category
                elif mod.category == 'TRICUSPID_STRUCTURE' and ent._.structure_type is None:
                    span = doc[mod.modifier_span[0]: mod.modifier_span[1]]
                    ent._.structure_text = span.text
                    ent._.structure_type = mod.category
                elif mod.category == 'NORMAL_STRUCTURE' and ent._.structure_type is None:
                    span = doc[mod.modifier_span[0]: mod.modifier_span[1]]
                    ent._.structure_text = span.text
                    ent._.structure_type = mod.category
                elif mod.category == 'PROSTHETIC_FLAG':
                    ent._.is_prosthetic = True
        return doc

    def __call__(self, doc: Doc):
        """
        Makes the pipeline object callable, needed for custom component objects.

        Args:
            doc: The input spaCy doc

        Returns:
            The processed spaCy doc
        """
        # access the extension you just created. we access it through the _ object attached to each doc, token, and span
        # doc[0]._.structure_type = "hello"
        relationships = self.set_all_attrs(doc)

        #return doc
        return relationships

