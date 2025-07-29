import os

try:
    from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
except ImportError:

    def SystemMetricsInstrumentor(*args, **kwargs):
        pass


def pre_instrument_system():
    labels = {
        "worker": str(os.getpid()),
    }
    configuration = {
        "process.context_switches": ["involuntary", "voluntary"],
        "process.cpu.time": ["user", "system"],
        "process.cpu.utilization": ["user", "system"],
        "process.memory.usage": None,
        "process.memory.virtual": None,
        "process.open_file_descriptor.count": None,
        "process.thread.count": None,
        "process.runtime.memory": ["rss", "vms"],
        "process.runtime.cpu.time": ["user", "system"],
        "process.runtime.gc_count": None,
        "process.runtime.thread_count": None,
        "process.runtime.cpu.utilization": None,
        "process.runtime.context_switches": ["involuntary", "voluntary"],
    }
    SystemMetricsInstrumentor(labels, config=configuration)
