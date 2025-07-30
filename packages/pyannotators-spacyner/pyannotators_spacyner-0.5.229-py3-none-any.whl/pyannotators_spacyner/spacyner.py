import os
import sys
from collections import defaultdict
from enum import Enum
from functools import lru_cache
from typing import Type, List, cast, Optional, Dict

import spacy
from pydantic import BaseModel, Field
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.annotator import AnnotatorParameters, AnnotatorBase
from pymultirole_plugins.v1.schema import Document, Span, Annotation, Term
from scispacy.linking_utils import Entity
from spacy.cli.download import download_model, get_compatibility, get_version
from spacy.language import Language
from spacy.util import run_command
from wasabi import msg

_home = os.path.expanduser('~')
xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or os.path.join(_home, '.cache')
cache_dir = os.path.join(xdg_cache_home, 'scispacy')
os.environ["SCISPACY_CACHE"] = cache_dir


class SpacyModelType(str, Enum):
    base = 'base'
    sci = 'sci'


class SpacyModelSize(str, Enum):
    sm = 'sm'
    md = 'md'
    lg = 'lg'


class SciSpacyLinker(str, Enum):
    umls = 'umls'
    mesh = 'mesh'


class SpacyLabel(str, Enum):
    # fr,de,pt,it
    PER = "PER"
    MISC = "MISC"
    # en,zh,nl
    LOC = "LOC"
    ORG = "ORG"
    PERSON = "PERSON"
    CARDINAL = "CARDINAL"
    DATE = "DATE"
    EVENT = "EVENT"
    FAC = "FAC"
    GPE = "GPE"
    LANGUAGE = "LANGUAGE"
    LAW = "LAW"
    MONEY = "MONEY"
    NORP = "NORP"
    ORDINAL = "ORDINAL"
    PERCENT = "PERCENT"
    PRODUCT = "PRODUCT"
    QUANTITY = "QUANTITY"
    TIME = "TIME"
    WORK_OF_ART = "WORK_OF_ART"
    # scispacy
    ENTITY = "ENTITY"


class SpacyNERParameters(AnnotatorParameters):
    model_type: SpacyModelType = Field(SpacyModelType.base,
                                       description="""Type of NER spacy model to use for NER extraction, can be:
                       <li>`base` for basic entities like location/person/organization provided by [spacy](https://spacy.io/models) or
                       <li>`sci` for biomedical entities provided by [scispacy](https://allenai.github.io/scispacy)""")
    mapping: Dict[str, List[SpacyLabel]] = Field(
        None,
        description="Map a label to a list of spacy NER labels",
        extra="key:label",
    )
    model_size: SpacyModelSize = Field(SpacyModelSize.sm,
                                       description="""Size of NER spacy model to use for NER extraction, can be:
                       <li>`sm` for small,
                       <li>`md` for medidum or
                       <li>`lg` for large""",
                                       extra="advanced,internal")
    scispacy_linker: Optional[SciSpacyLinker] = Field(None,
                                                      description="""Name of the [scispacy linker](https://github.com/allenai/scispacy) which performs linking to a knowledge base.<br/>
                                                      <b>Only valid with scispacy models</b>""",
                                                      extra="advanced")
    types_filter: Optional[str] = Field("", description="""Comma-separated list of UMLS [semantic types](https://lhncbc.nlm.nih.gov/ii/tools/MetaMap/documentation/SemanticTypesAndGroups.html) to keep.<br/>
                                                      For example `T028,T116,T123`<br/>
                                                      <b>Only valid with scispacy models</b>""",
                                        extra="advanced")
    mention_threshold: Optional[float] = Field(0.85,
                                               description="""The threshold that a entity candidate must reach to be added.<br/>
                                                      <b>Only valid with scispacy models</b>""",
                                               extra="advanced")
    mention_max: Optional[int] = Field(1,
                                       description="""The maximum number of entities which will be returned for a given mention.<br/>
                                                      <b>Only valid with scispacy models</b>""",
                                       extra="advanced")


SUPPORTED_LANGUAGES = "en,fr,de,nl,es,pt,it,zh,ru,ja"


class SpacyNERAnnotator(AnnotatorBase):
    __doc__ = """[Spacy](https://spacy.io/api/entityrecognizer) annotator.
    #need-segments
    #languages:""" + SUPPORTED_LANGUAGES

    def annotate(self, documents: List[Document], parameters: AnnotatorParameters) \
            -> List[Document]:
        params: SpacyNERParameters = \
            cast(SpacyNERParameters, parameters)
        supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)
        if params.mapping is not None:
            spacy2labels = defaultdict(list)
            for k, label_lst in params.mapping.items():
                for label in label_lst:
                    spacy2labels[label].append(k)
        else:
            spacy2labels = None
        for document in documents:
            lang = document_language(document, None)
            if lang is None or lang not in supported_languages:
                raise AttributeError(f"Metadata language {lang} is required and must be in {SUPPORTED_LANGUAGES}")
            # Create parsing context with time and language information
            nlp, linker = get_nlp(lang, params.model_type, params.model_size, params.scispacy_linker)
            types_filter = comma_separated_to_list(params.types_filter.strip())
            types_as_set = set(types_filter or [])
            document.annotations = []
            if not document.sentences:
                document.sentences = [Span(start=0, end=len(document.text))]
            sents = [document.text[s.start:s.end] for s in document.sentences]
            asents = nlp.pipe(sents)
            for sent, asent in zip(document.sentences, asents):
                for ent in asent.ents:
                    if spacy2labels is None or ent.label_ in spacy2labels:
                        start = sent.start + ent.start_char
                        end = sent.start + ent.end_char
                        terms = []
                        if linker is not None:
                            for umls_ent in ent._.kb_ents:
                                score = umls_ent[1]
                                if score >= params.mention_threshold:
                                    kbent: Entity = linker.kb.cui_to_entity[umls_ent[0]]
                                    types = types_as_set.intersection(kbent.types)
                                    if types or len(types_as_set) == 0:
                                        props = {'types': kbent.types if len(types_as_set) == 0 else list(types),
                                                 'aliases': kbent.aliases}
                                        term = Term(identifier=umls_ent[0], lexicon=params.scispacy_linker.value,
                                                    preferredForm=kbent.canonical_name, score=score, properties=props)
                                        if len(terms) < params.mention_max:
                                            terms.append(term)
                                        else:
                                            break
                        if spacy2labels is None:  # same as before
                            document.annotations.append(Annotation(start=start, end=end,
                                                                   labelName=ent.label_.lower(),
                                                                   label=ent.label_,
                                                                   text=document.text[start:end],
                                                                   terms=terms if linker is not None else None))
                        else:
                            for lname in spacy2labels[ent.label_]:
                                document.annotations.append(Annotation(start=start, end=end,
                                                                       labelName=lname,
                                                                       text=document.text[start:end],
                                                                       terms=terms if linker is not None else None))
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SpacyNERParameters


def document_language(doc: Document, default: str = None):
    if doc.metadata is not None and 'language' in doc.metadata:
        return doc.metadata['language']
    return default


@lru_cache(maxsize=None)
def get_nlp(lang, model_type, model_size, linker=None):
    model = lang
    if model_type == SpacyModelType.sci:
        if lang != 'en':
            raise AttributeError("scispacy model is only available in english")
        else:
            model += f"_core_{model_type.value}"
    else:
        model += "_core"
        if lang in ['en', 'zh']:
            model += "_web"
        else:
            model += "_news"
    model += f"_{model_size.value}"
    try:
        nlp: Language = spacy.load(model)
    except BaseException:
        nlp: Language = load_spacy_model(model)
    if model_type == SpacyModelType.sci and linker is not None:
        from scispacy.linking import EntityLinker
        linker: EntityLinker = nlp.add_pipe("scispacy_linker", config={"linker_name": linker.value})
    return nlp, linker


def load_spacy_model(model, *pip_args):
    if '_sci_' in model:
        model_name = model
        download_sci_model(model)
    else:
        suffix = "-py3-none-any.whl"
        dl_tpl = "{m}-{v}/{m}-{v}{s}#egg={m}=={v}"
        model_name = model
        compatibility = get_compatibility()
        version = get_version(model_name, compatibility)
        download_model(dl_tpl.format(m=model_name, v=version, s=suffix), pip_args)
    msg.good(
        "Download and installation successful",
        f"You can now load the package via spacy.load('{model_name}')",
    )
    # If a model is downloaded and then loaded within the same process, our
    # is_package check currently fails, because pkg_resources.working_set
    # is not refreshed automatically (see #3923). We're trying to work
    # around this here be requiring the package explicitly.
    require_package(model_name)
    return spacy.load(model_name)


def require_package(name):
    try:
        import pkg_resources

        pkg_resources.working_set.require(name)
        return True
    except:  # noqa: E722
        return False


def download_sci_model(
        filename: str, user_pip_args=None) -> None:
    download_url = f"https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/{filename}-0.4.0.tar.gz"
    pip_args = list(user_pip_args) if user_pip_args is not None else []
    cmd = [sys.executable, "-m", "pip", "install"] + pip_args + [download_url]
    run_command(cmd)
