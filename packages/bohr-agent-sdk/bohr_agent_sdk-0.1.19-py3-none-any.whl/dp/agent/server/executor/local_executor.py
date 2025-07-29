import asyncio
import importlib
import inspect
import jsonpickle
import os
import psutil
import sys
import uuid
from multiprocessing import Process
from typing import Dict, Optional

from .base_executor import BaseExecutor


def wrapped_fn(fn, kwargs):
    pid = os.getpid()
    try:
        if inspect.iscoroutinefunction(fn):
            result = asyncio.run(fn(**kwargs))
        else:
            result = fn(**kwargs)
    except Exception as e:
        with open("err", "w") as f:
            f.write(str(e))
        raise e
    with open("%s.txt" % pid, "w") as f:
        f.write(jsonpickle.dumps(result))


def reload_dflow_config():
    if "dflow.config" in sys.modules:
        config = sys.modules["dflow"].config
        s3_config = sys.modules["dflow"].s3_config
        s3_config["storage_client"] = None
        importlib.reload(sys.modules["dflow.config"])
        if "dflow.plugins.bohrium" in sys.modules:
            bohrium_config = sys.modules["dflow.plugins.bohrium"].config
            importlib.reload(sys.modules["dflow.plugins.bohrium"])
        importlib.reload(sys.modules["dflow"])
        config.update(sys.modules["dflow"].config)
        sys.modules["dflow"].config = config
        s3_config.update(sys.modules["dflow"].s3_config)
        sys.modules["dflow"].s3_config = s3_config
        if "dflow.plugins.bohrium" in sys.modules:
            bohrium_config.update(sys.modules["dflow.plugins.bohrium"].config)
            sys.modules["dflow.plugins.bohrium"].config = bohrium_config


class LocalExecutor(BaseExecutor):
    def __init__(self, env: Optional[Dict[str, str]] = None):
        """
        Execute the tool locally
        Args:
            env: The environmental variables at run time
        """
        self.env = env or {}

    def set_env(self):
        old_env = {}
        for k, v in self.env.items():
            if k in os.environ:
                old_env[k] = os.environ[k]
            os.environ[k] = v
        return old_env

    def recover_env(self, old_env):
        for k, v in self.env.items():
            if k in old_env:
                os.environ[k] = old_env[k]
            else:
                del os.environ[k]

    def submit(self, fn, kwargs):
        os.environ["DP_AGENT_RUNNING_MODE"] = "1"
        old_env = self.set_env()
        p = Process(target=wrapped_fn, kwargs={"fn": fn, "kwargs": kwargs})
        p.start()
        self.recover_env(old_env)
        return {"job_id": str(p.pid)}

    def query_status(self, job_id):
        try:
            p = psutil.Process(int(job_id))
            if p.status() not in ["zombie", "dead"]:
                return "Running"
        except psutil.NoSuchProcess:
            pass

        if os.path.isfile("%s.txt" % job_id):
            return "Succeeded"
        else:
            return "Failed"

    def terminate(self, job_id):
        try:
            p = psutil.Process(int(job_id))
            p.terminate()
        except Exception:
            pass

    def get_results(self, job_id):
        if os.path.isfile("%s.txt" % job_id):
            with open("%s.txt" % job_id, "r") as f:
                return jsonpickle.loads(f.read())
        elif os.path.isfile("err"):
            with open("err", "r") as f:
                err_msg = f.read()
            raise RuntimeError(err_msg)
        return {}

    async def async_run(self, fn, kwargs, context, trace_id):
        os.environ["DP_AGENT_RUNNING_MODE"] = "1"
        old_env = self.set_env()
        try:
            # explicitly reload dflow config in sync mode
            reload_dflow_config()
            if inspect.iscoroutinefunction(fn):
                result = await fn(**kwargs)
            else:
                result = fn(**kwargs)
        finally:
            self.recover_env(old_env)
        return {
            "job_id": str(uuid.uuid4()),
            "result": result,
        }
