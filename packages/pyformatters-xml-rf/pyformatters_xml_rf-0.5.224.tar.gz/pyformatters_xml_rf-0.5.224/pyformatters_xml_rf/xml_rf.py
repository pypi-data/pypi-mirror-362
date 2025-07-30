from collections import defaultdict, Counter, deque
from pathlib import Path
from typing import Type

import lxml.etree as ET
from Ranger import RangeBucketMap, Range
from fastapi import HTTPException
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.formatter import FormatterBase, FormatterParameters
from pymultirole_plugins.v1.schema import Document, Boundary, Annotation
from starlette.responses import Response


class RFXmlParameters(FormatterParameters):
    boundaries: str = Field("SECTIONS", description="Name of boundaries to consider")
    with_forms: bool = Field(True, description="Add list of all matching forms")
    absolute_uri: bool = Field(True, description="Use absolute or relative URI as identifier")


class RFXmlFormatter(FormatterBase):
    """Groupe RF XML formatter.
    """

    def format(self, document: Document, parameters: FormatterParameters) \
            -> Response:
        """Parse the input document and return a formatted response.

        :param document: An annotated document.
        :param parameters: options of the parser.
        :returns: Response.
        """
        parameters: RFXmlParameters = parameters
        if not document.sourceText:
            raise HTTPException(status_code=400, detail="No source xml text")
        try:
            data = document.sourceText
            encoding = document.properties.get('encoding', "UTF-8") if document.properties else "UTF-8"
            # parser = ET.XMLParser(encoding="utf-8")
            if document.sourceText and document.boundaries:
                if data.lower().startswith("<?xml"):
                    decl, data = data.split("?>", maxsplit=1)
                    decl += "?>"
                # root: ET.Element = ET.fromstring(data, parser=parser)
                root: ET.Element = ET.fromstring(data)
                baseNs = root.nsmap.get(None, None)
                # Ignore all namespaces
                for el in root.iter():
                    if baseNs and el.tag not in [ET.Comment, ET.PI, ET.Entity] and el.tag.startswith(f"{{{baseNs}}}"):
                        _, _, el.tag = el.tag.rpartition('}')
                doc_annexes = root.find("DOC_ANNEXES")
                if not doc_annexes:
                    doc_annexes = ET.Element("DOC_ANNEXES")
                    root.append(doc_annexes)
                thesaurus: ET.Element = doc_annexes.find("ANNOTATIONS_THESAURUS")
                if not thesaurus:
                    thesaurus = ET.Element("ANNOTATIONS_THESAURUS")
                    doc_annexes.insert(0, thesaurus)
                thesaurus.clear()
                boundaries = {}
                buckets = RangeBucketMap()
                terms = defaultdict(lambda: defaultdict(list))
                for b in document.boundaries.get(parameters.boundaries, []):
                    boundary = Boundary(**b) if isinstance(b, dict) else b
                    r = root.xpath(boundary.name)
                    if len(r) == 1:
                        node = r[0]
                        boundaries[node] = 0
                        buckets[Range.closedOpen(boundary.start, boundary.end)] = node

                # compute depth first order of boundaries
                queue = deque([root])
                index = 0
                while queue:
                    el = queue.popleft()
                    if el in boundaries:
                        boundaries[el] = index
                    queue.extend(el)
                    index = index + 1

                if document.annotations:
                    for a in document.annotations:
                        annotation = Annotation(**a) if isinstance(a, dict) else a
                        form = document.text[annotation.start:annotation.end]
                        if buckets.contains(annotation.start) and buckets.contains(annotation.end):
                            zones = buckets[Range.closedOpen(annotation.start, annotation.end)]
                            for zone in zones:
                                for term in annotation.terms:
                                    if parameters.absolute_uri or '#' not in term.identifier:
                                        ident = term.identifier
                                    else:
                                        ident = term.identifier[term.identifier.index("#") + 1:]
                                    terms[zone][ident].append(form)

                def depth_first_order(item):
                    node_index = item[1]
                    return node_index

                sorted_boundaries = sorted(boundaries.items(), key=depth_first_order, reverse=False)

                for node, ignored in sorted_boundaries:
                    if node in terms and terms[node]:
                        descripteurs = ET.Element("DESCRIPTEURS_" + node.tag, node.attrib)
                        for ident, forms in terms[node].items():
                            c = Counter(forms)
                            freq = sum(c.values())
                            descripteur = ET.Element("DESCRIPTEUR", Id=ident, Freq=str(freq))
                            if parameters.with_forms:
                                desc_forms = ET.Element("FORMES")
                                for form, ffreq in c.items():
                                    desc_form = ET.Element("FORME", Freq=str(ffreq))
                                    desc_form.text = form
                                    desc_forms.append(desc_form)
                                descripteur.insert(0, desc_forms)
                            descripteurs.append(descripteur)
                        thesaurus.append(descripteurs)

                data = ET.tostring(root, pretty_print=True, encoding=encoding, xml_declaration=True)
                # data = ET.tostring(root, encoding=encoding, xml_declaration=True)
            filename = "file.xml"
            if document.properties and "fileName" in document.properties:
                filepath = Path(document.properties['fileName'])
                filename = f"{filepath.stem}.xml"
            media_type = "application/xml" if encoding.lower() == "utf-8" \
                else f"application/xml; charset={encoding.lower()}"
            resp = Response(content=data, media_type=media_type)
            resp.headers["Content-Disposition"] = f"attachment; filename={filename}"
            resp.charset = encoding
            return resp
        except BaseException as err:
            raise err

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return RFXmlParameters
