import spacy
from spacy import Language
from spacy.language import Doc
from spacy.tokens import Token

# component name is set here. this will be used in spacy.add_pipe("my_component")
@Language.factory("my_component")
class MyComponent:
    """
    A basic component that shows custom spacy component functionality.
    """

    def __init__(self, nlp: Language, name = "my_component"):
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
        if not hasattr(Token._, "my_extension"):
            Token.set_extension("my_extension", default = None)

    def __call__(self, doc: Doc):
        """
        Makes the pipeline object callable, needed for custom component objects.

        Args:
            doc: The input spaCy doc

        Returns:
            The processed spaCy doc
        """
        # access the extension you just created. we access it through the _ object attached to each doc, token, and span
        doc[0]._.my_extension = "hello"

        return doc

