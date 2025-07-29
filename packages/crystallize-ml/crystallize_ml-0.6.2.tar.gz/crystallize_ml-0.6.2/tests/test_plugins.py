import logging

from crystallize.core.datasource import DataSource
from crystallize.core.experiment import Experiment
from crystallize.core.pipeline import Pipeline
from crystallize.core.pipeline_step import PipelineStep
from crystallize.core.plugins import LoggingPlugin
from crystallize.core.result import Result
from crystallize.core.result_structs import ExperimentMetrics, TreatmentMetrics, HypothesisResult


class DummySource(DataSource):
    def fetch(self, ctx):
        return 0


class DummyStep(PipelineStep):
    def __call__(self, data, ctx):  # pragma: no cover - simple pass-through
        return {"metric": data}

    @property
    def params(self):
        return {}


def _make_experiment(plugin: LoggingPlugin) -> Experiment:
    pipeline = Pipeline([DummyStep()])
    ds = DummySource()
    exp = Experiment(datasource=ds, pipeline=pipeline, plugins=[plugin])
    exp.replicates = 2
    exp.treatments = []
    exp.hypotheses = []
    return exp


def _make_result() -> Result:
    metrics = ExperimentMetrics(
        baseline=TreatmentMetrics({"metric": [0]}),
        treatments={},
        hypotheses=[
            HypothesisResult(
                name="h",
                results={"baseline": {"value": 1}},
                ranking={"best": None},
            )
        ],
    )
    return Result(metrics=metrics, errors={})


def test_logging_plugin_emits_messages(caplog):
    plugin = LoggingPlugin(verbose=True, log_level="INFO")
    exp = _make_experiment(plugin)
    result = _make_result()
    with caplog.at_level(logging.INFO, logger="crystallize"):
        plugin.before_run(exp)
        plugin.after_step(exp, DummyStep(), None, exp._setup_ctx)
        plugin.after_run(exp, result)
    messages = [r.getMessage() for r in caplog.records]
    assert any("Experiment:" in m for m in messages)
    assert any("finished step DummyStep" in m for m in messages)
    assert any(m.startswith("Completed in") for m in messages)


def test_logging_plugin_invalid_level(monkeypatch):
    captured = {}

    def fake_basic(**kwargs):
        captured["level"] = kwargs.get("level")

    monkeypatch.setattr(logging, "basicConfig", fake_basic)
    plugin = LoggingPlugin(log_level="WRONG")
    exp = _make_experiment(plugin)
    plugin.before_run(exp)
    assert captured["level"] == logging.INFO
