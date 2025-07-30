# coding: utf-8
from __future__ import absolute_import

from spyne.model.complex import ComplexModelBase
from spyne.model.complex import ComplexModelMeta


def namespace(ns):

    ComplexModel = ComplexModelMeta(
        "ComplexModel", (ComplexModelBase,), {"__namespace__": ns})

    return ComplexModel
