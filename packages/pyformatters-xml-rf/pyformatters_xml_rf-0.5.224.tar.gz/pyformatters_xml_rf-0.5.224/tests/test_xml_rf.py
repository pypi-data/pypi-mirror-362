import json
from pathlib import Path

import pytest
from fastapi import HTTPException
from multipart.multipart import parse_options_header
from starlette.responses import Response

from pyformatters_xml_rf.xml_rf import RFXmlFormatter, RFXmlParameters
from pymultirole_plugins.v1.schema import Document
import lxml.etree as ET


def test_files():
    testdir = Path(__file__).parent / 'data'
    return testdir.glob('*.json')


def descriptors_mix_test_files():
    testdir = Path(__file__).parent / 'data'
    return testdir.glob('descriptors_mix*.json')


def test_no_sourceText():
    with pytest.raises(HTTPException) as err:
        formatter = RFXmlFormatter()
        resp: Response = formatter.format(Document(text="text"), RFXmlFormatter())
        assert resp.status_code == 400
    assert err.value.status_code == 400


@pytest.mark.parametrize('test_file', test_files())
def test_xml_rf(test_file):
    with test_file.open("r") as fin:
        docs = json.load(fin)
        doc = Document(**docs[0])
        formatter = RFXmlFormatter()
        options = RFXmlParameters()
        resp: Response = formatter.format(doc, options)
        assert resp.status_code == 200
        assert resp.media_type.startswith("application/xml")
        result = test_file.with_suffix(".xml")
        with result.open("wb") as fout:
            fout.write(resp.body)
        root = ET.fromstring(resp.body)
        baseNs = root.nsmap.get(None, None)
        all_descs = list(root.iterdescendants(f"{{{baseNs}}}DESCRIPTEUR"))
        all_forms = list(root.iterdescendants(f"{{{baseNs}}}FORME"))
        assert len(all_descs) > 0
        assert len(all_forms) > 0


@pytest.mark.parametrize('test_file', test_files())
def test_xml_rf_without_forms(test_file):
    with test_file.open("r") as fin:
        docs = json.load(fin)
        doc = Document(**docs[0])
        formatter = RFXmlFormatter()
        options = RFXmlParameters(with_forms=False, absolute_uri=False)
        resp: Response = formatter.format(doc, options)
        assert resp.status_code == 200
        assert resp.media_type.startswith("application/xml")
        content_type, content_parameters = parse_options_header(resp.headers['Content-Disposition'])
        if doc.properties and 'fileName' in doc.properties:
            if b'filename' in content_parameters:
                filename = content_parameters[b'filename'].decode("utf-8")
            assert Path(doc.properties['fileName']).stem == Path(filename).stem
        root = ET.fromstring(resp.body)
        baseNs = root.nsmap.get(None, None)
        all_descs = list(root.iterdescendants(f"{{{baseNs}}}DESCRIPTEUR"))
        all_forms = list(root.iterdescendants(f"{{{baseNs}}}FORME"))
        for desc in all_descs:
            assert "#" not in desc.attrib['Id']
        assert len(all_descs) > 0
        assert len(all_forms) == 0


@pytest.mark.parametrize('test_file', descriptors_mix_test_files())
def test_xml_rf_descriptors_mix(test_file):
    with test_file.open("r") as fin:
        docs = json.load(fin)
        doc = Document(**docs[0])
        formatter = RFXmlFormatter()
        options = RFXmlParameters(with_forms=True, absolute_uri=False)
        resp: Response = formatter.format(doc, options)
        assert resp.status_code == 200
        assert resp.media_type.startswith("application/xml")
        content_type, content_parameters = parse_options_header(resp.headers['Content-Disposition'])
        if b'filename' in content_parameters:
            filename = content_parameters[b'filename'].decode("utf-8")
        assert Path(doc.properties['fileName']).stem == Path(filename).stem
        root = ET.fromstring(resp.body)
        ns = {'rf': 'http://www.grouperf.com'}
        subs = root.findall("./rf:DOC_ANNEXES/rf:ANNOTATIONS_THESAURUS/*", ns)
        unique_subs = []
        for sub in subs:
            tag = sub.tag[len('{http://www.grouperf.com}DESCRIPTEURS_'):]
            if len(unique_subs) == 0 or unique_subs[-1] != tag:
                unique_subs.append(tag)

        assert unique_subs == ['DOC_INTRO', 'DOC_DEV', 'SECTION'] or unique_subs == ['DOC_DEV', 'SECTION']
