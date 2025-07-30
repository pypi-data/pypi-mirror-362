from pymultirole_plugins.v1.schema import Document, Annotation

from pyprocessors_nameparser.name_parser import (
    NameParserProcessor,
    NameParserParameters
)


def test_model():
    model = NameParserProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == NameParserParameters


def test_nameparser():
    processor = NameParserProcessor()
    parameters = NameParserParameters(name_labels=['auteur'])
    doc = Document(text="Olivier Terrier",
                   annotations=[Annotation(label='Auteur', labelName='auteur', start=0, end=15)])
    docs = processor.process([doc], parameters)
    doc0 = docs[0]
    ot = doc0.annotations[0]
    assert len(ot.properties) > 0
