import abc
from typing import Optional, Sequence

from opentelemetry.context import Context
from opentelemetry.sdk.resources import Attributes
from opentelemetry.sdk.trace.sampling import Sampler, SamplingResult
from opentelemetry.trace import Link, SpanKind, TraceState


class CompositeSampler(Sampler, abc.ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sampler_by_name = {}

    def add_sampler_for_name(self, span_name: str, sampler: Sampler):
        """
        Return the names of the samplers that this sampler depends on
        :return: a set of sampler names
        """
        self._sampler_by_name[span_name] = sampler

    def should_sample(
        self,
        parent_context: Optional[Context],
        trace_id: int,
        name: str,
        kind: Optional[SpanKind] = None,
        attributes: Attributes = None,
        links: Optional[Sequence[Link]] = None,
        trace_state: Optional[TraceState] = None,
    ) -> SamplingResult:
        used_sampler = self._sampler_by_name.get(name) or super()
        return used_sampler.should_sample(parent_context, trace_id, name, kind, attributes, links, trace_state)
