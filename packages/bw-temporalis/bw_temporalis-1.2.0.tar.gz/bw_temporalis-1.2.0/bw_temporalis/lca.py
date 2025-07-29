import json
import warnings
from collections import defaultdict
from collections.abc import Iterable
from datetime import datetime
from heapq import heappop, heappush
from typing import Union

import bw2data as bd
import numpy as np
from bw2calc import LCA
from bw2data.backends import ActivityDataset as AD
from bw2data.backends import Exchange
from bw2data.backends import ExchangeDataset as ED
from bw_graph_tools import NewNodeEachVisitGraphTraversal

from .temporal_distribution import TDAware, TemporalDistribution
from .timeline import Timeline


class MultipleTechnosphereExchanges(Exception):
    pass


class NoExchange:
    """The edge was created dynamically via a datapackage. There is no edge in the database."""

    pass


class TemporalisLCA:
    """
    Calculate an LCA using graph traversal, with edges using temporal distributions.

    Edges with temporal distributions should store this information using `"temporal_distributions"`:

    ```python
        exchange["temporal_distribution"] = bw_temporalis.TemporalDistribution(
            times=numpy.array([-2, -1, 0, 1, 2], dtype="timedelta64[s]"),
            values=numpy.ones(5)
        )
    ```

    Temporal distribution times must always have the data type `timedelta64[s]`. Not all edges need to have temporal distributions.

    Temporal distributions are **not density functions** - their values should sum to the exchange amount.

    As graph traversal is much slower than matrix calculations, we can limit which nodes get traversed in several ways:

    * All activities in a database marked as `static`
    * Any activity ids passed in `static_activity_indices`
    * Any activities whose cumulative impact is below the cutoff score

    The output of a Temporalis LCA calculation is a `bw_temporalis.Timeline`, which can be characterized.

    Parameters
    ----------
    lca_object : bw2calc.LCA
        The already instantiated and calculated LCA class (i.e. `.lci()` and `.lcia()` have already been done)
    starting_datetime : datetime.datetime | str
        When the functional unit happens. Must be a point in time. Normally something like `"now"` or `"2023-01-01"`.
    cutoff : float
        The fraction of the total score below which graph traversal should stop. In range `(0, 1)`.
    biosphere_cutoff : float
        The fraction of the total score below which we don't include separate biosphere nodes to be characterized in the `Timeline`. In range `(0, 1)`.
    max_calc : int
        Total number of LCA inventory calculations to perform during graph traversal
    static_activity_indices : set[int]
        Activity database node `id` values where graph traversal will stop
    skip_coproducts : bool
        Should we also traverse edges for the other products in multioutput activities?
    functional_unit_unique_id : int
        The unique id of the functional unit. Strongly recommended to leave as default.
    graph_traversal : bw_graph_tools.NewNodeEachVisitGraphTraversal
        Optional subclass of `NewNodeEachVisitGraphTraversal` for advanced usage

    """

    def __init__(
        self,
        lca_object: LCA,
        starting_datetime: datetime | str = "now",
        cutoff: float | None = 5e-4,
        biosphere_cutoff: float | None = 1e-6,
        max_calc: int | None = 2000,
        static_activity_indices: set[int] | None = None,
        skip_coproducts: bool | None = False,
        functional_unit_unique_id: int | None = -1,
        graph_traversal: (
            NewNodeEachVisitGraphTraversal | None
        ) = NewNodeEachVisitGraphTraversal,
    ):
        self.lca_object = lca_object
        self.unique_id = functional_unit_unique_id
        self.t0 = TemporalDistribution(
            np.array([np.datetime64(starting_datetime)]),
            np.array([1]),
        )

        if static_activity_indices is None:
            static_activity_indices = set()

        for db in bd.databases:
            if bd.databases[db].get("static"):
                static_activity_indices.update(
                    obj[0] for obj in AD.select(AD.id).where(AD.database == db).tuples()
                )

        # Translate database indices to matrix indices which `graph_traversal` expects
        static_activity_indices = {
            self.lca_object.dicts.activity[x] for x in static_activity_indices
        }

        print("Starting graph traversal")
        gt = graph_traversal.calculate(
            lca_object=lca_object,
            static_activity_indices=static_activity_indices,
            max_calc=max_calc,
            cutoff=cutoff,
            biosphere_cutoff=biosphere_cutoff,
            separate_biosphere_flows=True,
            skip_coproducts=skip_coproducts,
            functional_unit_unique_id=functional_unit_unique_id,
        )
        print("Calculation count:", gt["calculation_count"])
        self.nodes = gt["nodes"]
        self.edges = gt["edges"]
        self.edge_mapping = defaultdict(list)
        for edge in self.edges:
            self.edge_mapping[edge.consumer_unique_id].append(edge)

        self.flows = gt["flows"]
        self.flow_mapping = defaultdict(list)
        for flow in self.flows:
            self.flow_mapping[flow.activity_unique_id].append(flow)

    def build_timeline(self, node_timeline: bool | None = False) -> Timeline:
        heap = []
        timeline = Timeline()

        if node_timeline:
            warnings.warn(
                """This functionality is experimental, and will change.
You have been warned."""
            )

        for edge in self.edge_mapping[self.unique_id]:
            node = self.nodes[edge.producer_unique_id]
            heappush(
                heap,
                (
                    1 / node.cumulative_score,
                    self.t0 * edge.amount,
                    node,
                ),
            )

        while heap:
            _, td, node = heappop(heap)
            if node_timeline:
                num_flows, num_flows_td = 0, 0
                for flow in self.flow_mapping.get(node.unique_id, []):
                    for exchange in self.get_biosphere_exchanges(
                        flow.flow_datapackage_id, node.activity_datapackage_id
                    ):
                        if exchange.data.get("temporal_distribution"):
                            num_flows_td += 1
                        num_flows += 1
                timeline.add_node_temporal_distribution(
                    td=td,
                    activity=node.activity_datapackage_id,
                    num_flows=num_flows,
                    num_flows_td=num_flows_td,
                )
            else:
                for flow in self.flow_mapping.get(node.unique_id, []):
                    for exchange in self.get_biosphere_exchanges(
                        flow.flow_datapackage_id, node.activity_datapackage_id
                    ):
                        value = self._exchange_value(
                            exchange=exchange,
                            row_id=flow.flow_datapackage_id,
                            col_id=node.activity_datapackage_id,
                            matrix_label="biosphere_matrix",
                        )
                        timeline.add_flow_temporal_distribution(
                            td=(td * value).simplify(),
                            flow=flow.flow_datapackage_id,
                            activity=node.activity_datapackage_id,
                        )

            for edge in self.edge_mapping[node.unique_id]:
                row_id = self.nodes[edge.producer_unique_id].activity_datapackage_id
                col_id = node.activity_datapackage_id
                exchange = self.get_technosphere_exchange(
                    input_id=row_id,
                    output_id=col_id,
                )
                value = (
                    self._exchange_value(
                        exchange=exchange,
                        row_id=row_id,
                        col_id=col_id,
                        matrix_label="technosphere_matrix",
                    )
                    / node.reference_product_production_amount
                )
                producer = self.nodes[edge.producer_unique_id]
                heappush(
                    heap,
                    (
                        1 / node.cumulative_score,
                        (td * value).simplify(),
                        producer,
                    ),
                )
        return timeline

    def _exchange_value(
        self,
        exchange: Union[bd.backends.ExchangeDataset, NoExchange],
        row_id: int,
        col_id: int,
        matrix_label: str,
    ) -> Union[float, TemporalDistribution]:
        from . import loader_registry

        if exchange is NoExchange:
            td = None
        else:
            td = exchange.data.get("temporal_distribution")
            if isinstance(td, str) and "__loader__" in td:
                data = json.loads(td)
                try:
                    td = loader_registry[td["__loader__"]](data)
                except KeyError:
                    raise KeyError(
                        "Can't find correct loader {} in `loader_registry`".format(
                            td["__loader__"]
                        )
                    )
            elif not (isinstance(td, (TemporalDistribution, TDAware)) or td is None):
                raise ValueError(
                    f"Can't understand value for `temporal_distribution` in exchange {exchange}"
                )

            sign = (
                1
                if exchange.data["type"] not in ("generic consumption", "technosphere")
                else -1
            )

        if matrix_label == "technosphere_matrix":
            value = self.lca_object.technosphere_matrix[
                self.lca_object.dicts.product[row_id],
                self.lca_object.dicts.activity[col_id],
            ]
            if exchange is NoExchange:
                # Assume technosphere input so negative sign, unless we have a
                # positive value and the number is on the diagonal, or the
                # IDs are the same (shared product/process, not on the diagonal
                # for whatever reason).
                if row_id == col_id:
                    sign = 1
                elif (
                    value > 0
                    and self.lca_object.dicts.biosphere[row_id]
                    == self.lca_object.dicts.activity[col_id]
                ):
                    sign = 1
                else:
                    sign = -1

            amount = sign * value
        elif matrix_label == "biosphere_matrix":
            amount = (
                exchange.data.get("fraction", 1) if exchange is not NoExchange else 1
            ) * self.lca_object.biosphere_matrix[
                self.lca_object.dicts.biosphere[row_id],
                self.lca_object.dicts.activity[col_id],
            ]
        else:
            raise ValueError(f"Unknown matrix type {matrix_label}")

        if td is None:
            return amount
        else:
            return td * amount

    def _exchange_iterator(self, input_id: int, output_id: int) -> list[ED]:
        inp = AD.get(AD.id == input_id)
        outp = AD.get(AD.id == output_id)
        return list(
            ED.select().where(
                ED.input_code == inp.code,
                ED.input_database == inp.database,
                ED.output_code == outp.code,
                ED.output_database == outp.database,
            )
        )

    def get_biosphere_exchanges(self, flow_id: int, activity_id: int) -> Iterable[ED]:
        exchanges = self._exchange_iterator(flow_id, activity_id)
        if len(exchanges) > 1:
            total = sum(exc.data["amount"] for exc in exchanges)
            for exc in exchanges:
                exc.data["fraction"] = exc.data["amount"] / total
                yield exc
        elif len(exchanges) == 1:
            yield from exchanges
        else:
            yield NoExchange

    def get_technosphere_exchange(self, input_id: int, output_id: int) -> ED:
        def printer(x):
            return "({}|{}|{})".format(x["database"], x["code"], x["name"])

        exchanges = self._exchange_iterator(input_id, output_id)
        if len(exchanges) > 1:
            _exchange = Exchange(exchanges[0])
            raise MultipleTechnosphereExchanges(
                "Found {} exchanges for link between {} and {}".format(
                    len(exchanges), printer(_exchange.input), printer(_exchange.output)
                )
            )
        elif not exchanges:
            # Edge injected via datapackage, no exchange in dataset
            return NoExchange
        else:
            return exchanges[0]
