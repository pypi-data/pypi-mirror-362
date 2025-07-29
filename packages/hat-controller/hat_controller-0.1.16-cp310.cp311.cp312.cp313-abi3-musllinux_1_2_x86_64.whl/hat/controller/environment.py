from collections.abc import Collection
import asyncio
import logging
import typing

from hat import aio
from hat import json

from hat.controller import common
import hat.controller.evaluators
import hat.controller.interpreters


mlog = logging.getLogger(__name__)


class UnitProxy(typing.NamedTuple):
    unit: common.Unit
    info: common.UnitInfo


class Environment(aio.Resource):

    def __init__(self,
                 environment_conf: json.Data,
                 proxies: Collection[UnitProxy],
                 trigger_queue_size: int = 4096):
        self._name = environment_conf['name']
        self._loop = asyncio.get_running_loop()
        self._executor = aio.Executor(1, log_exceptions=False)
        self._trigger_queue = aio.Queue(trigger_queue_size)
        self._proxies = {proxy.info.name: proxy for proxy in proxies}
        self._last_trigger = None
        self._action_triggers = {
            action_conf['name']: [(tuple(trigger_conf['type'].split('/')),
                                   tuple(trigger_conf['name'].split('/')))
                                  for trigger_conf in action_conf['triggers']]
            for action_conf in environment_conf['actions']}

        interpreter_type = hat.controller.interpreters.InterpreterType(
            environment_conf['interpreter'])
        init_code = environment_conf['init_code']
        action_codes = {action_conf['name']: action_conf['code']
                        for action_conf in environment_conf['actions']}

        self.async_group.spawn(self._run_loop, interpreter_type, init_code,
                               action_codes)

    @property
    def async_group(self) -> aio.Group:
        return self._executor.async_group

    async def enqueue_trigger(self, trigger: common.Trigger):
        await self._trigger_queue.put(trigger)

    async def _run_loop(self, interpreter_type, init_code, action_codes):
        try:
            infos = (proxy.info for proxy in self._proxies.values())

            evaluator = await self._executor.spawn(
                hat.controller.evaluators.create_evaluator,
                interpreter_type, action_codes, infos, self._ext_call)

            await self._executor.spawn(self._ext_eval_init, evaluator,
                                       init_code)

            while True:
                self._last_trigger = await self._trigger_queue.get()

                action_names = self._get_matching_action_names(
                    self._last_trigger)
                for action_name in action_names:
                    await self._executor.spawn(self._ext_eval_action,
                                               evaluator, action_name)

        except Exception as e:
            mlog.error('environment %s run loop error: %s',
                       self._name, e, exc_info=e)

        finally:
            self.close()
            self._trigger_queue.close()

    async def _call(self, unit_name, function, args):
        proxy = self._proxies[unit_name]
        return await aio.call(proxy.unit.call, function, args,
                              self._last_trigger)

    def _ext_call(self, unit_name, function, args):
        coro = self._call(unit_name, function, args)
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()

    def _ext_eval_init(self, evaluator, code):
        try:
            evaluator.eval_code(code)

        except Exception as e:
            mlog.error("environment %s init error: %s",
                       self._name, e, exc_info=e)

    def _ext_eval_action(self, evaluator, action_name):
        try:
            evaluator.eval_action(action_name)

        except Exception as e:
            mlog.error("environment %s action %s error: %s",
                       self._name, action_name, e, exc_info=e)

    def _get_matching_action_names(self, trigger):
        for action_name, action_triggers in self._action_triggers.items():
            for type_query, name_query in action_triggers:
                if not _match_query(trigger.type, type_query):
                    continue

                if not _match_query(trigger.name, name_query):
                    continue

                yield action_name
                break


def _match_query(value, query):
    if query and query[-1] == '*':
        query = query[:-1]
        value = value[:len(query)]

    if len(value) != len(query):
        return False

    for v, q in zip(value, query):
        if q != '?' and v != q:
            return False

    return True
