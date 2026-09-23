# Don't evaluate type annotations at runtime
from __future__ import annotations

import importlib.abc
import importlib.machinery
import importlib.util
import io
import os
import sys
import threading
import time
import traceback
import site

import sublime
import sublime_api

from typing import TYPE_CHECKING
from collections.abc import Callable, Generator
from types import ModuleType

if TYPE_CHECKING:
    from sublime import AutoCompleteFlags
    from sublime_types import Value, Event, Point, CommandArgs, CompletionValue


api_ready = False

deferred_plugin_loadeds = []

application_command_classes = []
window_command_classes = []
text_command_classes = []

view_event_listener_classes = []
view_event_listeners = {}

all_command_classes = [
    application_command_classes,
    window_command_classes,
    text_command_classes]

all_callbacks = {
    'on_init': [],
    'on_new': [],
    'on_clone': [],
    'on_load': [],
    'on_revert': [],
    'on_reload': [],
    'on_pre_close': [],
    'on_close': [],
    'on_pre_save': [],
    'on_post_save': [],
    'on_pre_move': [],
    'on_post_move': [],
    'on_modified': [],
    'on_selection_modified': [],
    'on_activated': [],
    'on_deactivated': [],
    'on_query_context': [],
    'on_query_completions': [],
    'on_hover': [],
    'on_text_command': [],
    'on_window_command': [],
    'on_post_text_command': [],
    'on_post_window_command': [],
    'on_modified_async': [],
    'on_selection_modified_async': [],
    'on_pre_save_async': [],
    'on_post_save_async': [],
    'on_post_move_async': [],
    'on_activated_async': [],
    'on_deactivated_async': [],
    'on_new_async': [],
    'on_load_async': [],
    'on_revert_async': [],
    'on_reload_async': [],
    'on_clone_async': [],
    'on_new_buffer': [],
    'on_new_buffer_async': [],
    'on_associate_buffer': [],
    'on_associate_buffer_async': [],
    'on_close_buffer': [],
    'on_close_buffer_async': [],
    'on_new_project': [],
    'on_new_project_async': [],
    'on_load_project': [],
    'on_load_project_async': [],
    'on_pre_save_project': [],
    'on_post_save_project': [],
    'on_post_save_project_async': [],
    'on_pre_close_project': [],
    'on_new_window': [],
    'on_new_window_async': [],
    'on_pre_close_window': [],
    'on_exit': [],
}

pending_on_activated_async_lock = threading.Lock()

pending_on_activated_async_callbacks = {
    'EventListener': [],
    'ViewEventListener': [],
}

view_event_listener_excluded_callbacks = {
    'on_clone',
    'on_clone_async',
    'on_exit',
    'on_init',
    'on_load_project',
    'on_load_project_async',
    'on_new',
    'on_new_async',
    'on_new_buffer',
    'on_new_buffer_async',
    'on_associate_buffer',
    'on_associate_buffer_async',
    'on_close_buffer',
    'on_close_buffer_async',
    'on_new_project',
    'on_new_project_async',
    'on_new_window',
    'on_new_window_async',
    'on_post_save_project',
    'on_post_save_project_async',
    'on_post_window_command',
    'on_pre_close_project',
    'on_pre_close_window',
    'on_pre_save_project',
    'on_window_command',
}

text_change_listener_classes = []
text_change_listener_callbacks = {
    'on_text_changed',
    'on_text_changed_async',
    'on_revert',
    'on_revert_async',
    'on_reload',
    'on_reload_async',
}
text_change_listeners = {}

profile = {}


def add_profiling(event_handler: Callable[..., None]) -> Callable[..., None]:
    """
    Decorator to measure blocking event handler methods. Also prevents
    exceptions from interrupting other events handlers.

    :param event_handler:
        The event handler method - must be an unbound method

    :return:
        The decorated method

    :meta private:
    """

    def profiler(*args):
        t0 = time.time()
        try:
            return event_handler(*args)
        except (Exception) as e:
            # All this to include stack frames before the call to
            # event_handler() above
            tb = traceback.extract_stack()[:-1]
            tb += traceback.extract_tb(e.__traceback__)
            out = ["Traceback (most recent call last):\n"]
            out += traceback.format_list(tb)
            out += traceback.format_exception_only(type(e), e)
            print("".join(out), end="")
        finally:
            elapsed = time.time() - t0
            mod = event_handler.__module__
            p = profile.setdefault(event_handler.__name__, {})
            p.setdefault(mod, Summary()).record(elapsed)

    # Make the method look like the original for introspection
    profiler.__doc__ = event_handler.__doc__
    profiler.__name__ = event_handler.__name__
    profiler.__module__ = event_handler.__module__
    # Follow the pattern of decorators like @classmethod and @staticmethod
    profiler.__func__ = event_handler
    return profiler


def trap_exceptions(event_handler: Callable[..., None]) -> Callable[..., None]:
    """
    Decorator to prevent exceptions from interrupting other events handlers.

    :param event_handler:
        The event handler method - must be an unbound method

    :return:
        The decorated method

    :meta private:
    """

    def exception_handler(*args):
        try:
            return event_handler(*args)
        except (Exception) as e:
            # All this to include stack frames before the call to
            # event_handler() above
            tb = traceback.extract_stack()[:-1]
            tb += traceback.extract_tb(e.__traceback__)
            out = ["Traceback (most recent call last):\n"]
            out += traceback.format_list(tb)
            out += traceback.format_exception_only(type(e), e)
            print("".join(out), end="")

    # Make the method look like the original for introspection
    exception_handler.__doc__ = event_handler.__doc__
    exception_handler.__name__ = event_handler.__name__
    exception_handler.__module__ = event_handler.__module__
    event_handler.__name__ = '_wrapped_' + event_handler.__name__
    # Follow the pattern of decorators like @classmethod and @staticmethod
    exception_handler.__func__ = event_handler
    return exception_handler


def decorate_handler(cls: type, method_name: str):
    """
    Decorates an event handler method with exception trapping, and in the case
    of blocking calls, profiling.

    :param cls:
        The class object to decorate
    :param method_name:
        A unicode string of the name of the method to decorate

    :meta private:
    """

    # We have to use __dict__ rather than getattr(), otherwise the function
    # is passed through decorators, and we can't detect @classmethod and
    # @staticmethod
    method = cls.__dict__[method_name]
    if method_name.endswith('_async'):
        wrapper = trap_exceptions
    else:
        wrapper = add_profiling
    if isinstance(method, staticmethod):
        wrapped = staticmethod(wrapper(method.__func__))
    elif isinstance(method, classmethod):
        wrapped = classmethod(wrapper(method.__func__))
    else:
        wrapped = wrapper(method)
    setattr(cls, method_name, wrapped)


def unload_module(module: ModuleType):
    plugin_unloaded = getattr(module, 'plugin_unloaded', None)
    if plugin_unloaded is not None:
        try:
            plugin_unloaded()
        except:
            traceback.print_exc()

    # Unload the old plugins
    plugins = module.__dict__.pop('__plugins__', None)
    if plugins is not None:
        for listener_instances in view_event_listeners.values():
            for instance in listener_instances[:]:
                if type(instance) in plugins:
                    listener_instances.remove(instance)

        for listener_instances in text_change_listeners.values():
            for tcl in listener_instances[:]:
                if type(tcl) in plugins:
                    tcl.detach()
                    listener_instances.remove(tcl)

        for p in plugins:
            for cmd_cls_list in all_command_classes:
                try:
                    cmd_cls_list.remove(p)
                except ValueError:
                    pass

            for c in all_callbacks.values():
                try:
                    c.remove(p)
                except ValueError:
                    pass

            try:
                view_event_listener_classes.remove(p)
            except ValueError:
                pass

            try:
                text_change_listener_classes.remove(p)
            except ValueError:
                pass


def unload_plugin(modulename: str):
    print(f"unloading plugin {modulename}")

    if modulename in sys.modules:
        unload_module(sys.modules.pop(modulename))


def reload_plugin(modulename: str):
    print(f"reloading plugin {modulename}")

    if m := sys.modules.get(modulename, None):
        unload_module(m)
        m = importlib.reload(m)
    else:
        m = importlib.import_module(modulename)

    load_module(m)


def load_module(m: ModuleType):
    module_plugins = []
    on_activated_targets = []
    vel_on_activated_classes = []
    el_on_activated_async_targets = []
    vel_on_activated_async_targets = []
    module_view_event_listener_classes = []
    module_text_change_listener_classes = []

    module_exports = getattr(m, '__all__', None)
    # We build a set of allowed imports, but iterate over the module itself so
    # that the classes are added in order
    if module_exports is not None:
        module_exports = set(module_exports)
        objects = (o for name, o in m.__dict__.items() if name in module_exports)
    else:
        # When the plugin doesn't define __all__, we ignore "private" entries
        objects = (o for name, o in m.__dict__.items() if name[0] != '_')

    for t in objects:
        if not isinstance(t, type):
            continue

        if issubclass(t, ApplicationCommand) and t is not ApplicationCommand:
            application_command_classes.append(t)
            module_plugins.append(t)

        elif issubclass(t, WindowCommand) and t is not WindowCommand:
            window_command_classes.append(t)
            module_plugins.append(t)

        elif issubclass(t, TextCommand) and t is not TextCommand:
            text_command_classes.append(t)
            module_plugins.append(t)

        elif issubclass(t, EventListener) and t is not EventListener:
            for method_name in all_callbacks:
                if hasattr(t, method_name):
                    decorate_handler(t, method_name)

            obj = t()

            for method_name, listeners in all_callbacks.items():
                if hasattr(t, method_name):
                    listeners.append(obj)

            if hasattr(obj, 'on_activated'):
                on_activated_targets.append(obj)
            if hasattr(obj, 'on_activated_async'):
                el_on_activated_async_targets.append(obj)

            module_plugins.append(obj)

        elif issubclass(t, ViewEventListener) and t is not ViewEventListener:
            for method_name in all_callbacks:
                if hasattr(t, method_name) and method_name not in view_event_listener_excluded_callbacks:
                    decorate_handler(t, method_name)

            view_event_listener_classes.append(t)
            module_view_event_listener_classes.append(t)

            if hasattr(t, 'on_activated'):
                vel_on_activated_classes.append(t)
            if hasattr(t, 'on_activated_async'):
                vel_on_activated_async_targets.append(t)

            module_plugins.append(t)

        elif issubclass(t, TextChangeListener) and t is not TextChangeListener:
            for method_name in text_change_listener_callbacks:
                if hasattr(t, method_name):
                    decorate_handler(t, method_name)

            text_change_listener_classes.append(t)
            module_text_change_listener_classes.append(t)

            module_plugins.append(t)

    if el_on_activated_async_targets or vel_on_activated_async_targets:
        with pending_on_activated_async_lock:
            pending_on_activated_async_callbacks['EventListener'].extend(
                el_on_activated_async_targets
            )
            pending_on_activated_async_callbacks['ViewEventListener'].extend(
                vel_on_activated_async_targets
            )

    if module_plugins:
        m.__plugins__ = module_plugins

    plugin_loaded = getattr(m, 'plugin_loaded', None)

    if api_ready:
        if plugin_loaded is not None:
            try:
                plugin_loaded()
            except:
                traceback.print_exc()

        # Create any require ViewEventListener objects
        if module_view_event_listener_classes:
            for w in sublime.windows():
                for v in w.views(include_transient=True):
                    create_view_event_listeners(
                        module_view_event_listener_classes, v)

        # Create any required TextChangeListener objects
        if module_text_change_listener_classes:
            for b in sublime._buffers():
                attach_buffer(b)

        on_init(m.__name__)

        # Synthesize any required on_activated calls
        w = sublime.active_window()
        if w:
            v = w.active_view()
            if v:
                for el in on_activated_targets:
                    try:
                        el.on_activated(v)
                    except:
                        traceback.print_exc()

                for vel_cls in vel_on_activated_classes:
                    if vel := find_view_event_listener(v, vel_cls):
                        try:
                            vel.on_activated()
                        except:
                            traceback.print_exc()

    elif plugin_loaded is not None:
        deferred_plugin_loadeds.append(plugin_loaded)


def synthesize_on_activated_async():
    if not api_ready:
        return

    with pending_on_activated_async_lock:
        els = pending_on_activated_async_callbacks['EventListener']
        vels = pending_on_activated_async_callbacks['ViewEventListener']
        pending_on_activated_async_callbacks['EventListener'] = []
        pending_on_activated_async_callbacks['ViewEventListener'] = []

    window = sublime.active_window()
    if not window:
        return

    view = window.active_view()
    if not view:
        return

    for el in els:
        el.on_activated_async(view)

        if not view.is_valid():
            return

    for vel_cls in vels:
        vel = find_view_event_listener(view, vel_cls)
        if vel:
            vel.on_activated_async()

            if not view.is_valid():
                return


def _instantiation_error(cls: type, e: Exception):
    rex = RuntimeError(f"unable to instantiate '{cls.__module__}.{cls.__name__}'")
    rex.__cause__ = e
    traceback.print_exception(None, rex, None)


def notify_application_commands():
    sublime_api.notify_application_commands(create_application_commands())


def create_application_commands() -> list[tuple[ApplicationCommand, str]]:
    cmds = []
    for cls in application_command_classes:
        try:
            o = cls()
            cmds.append((o, o.name()))
        except Exception as e:
            _instantiation_error(cls, e)
    return cmds


def create_window_commands(window_id: int) -> list[tuple[WindowCommand, str]]:
    window = sublime.Window(window_id)
    cmds = []
    for cls in window_command_classes:
        try:
            o = cls(window)
            cmds.append((o, o.name()))
        except Exception as e:
            _instantiation_error(cls, e)
    return cmds


def create_text_commands(view_id: int) -> list[tuple[TextCommand, str]]:
    view = sublime.View(view_id)
    cmds = []
    for cls in text_command_classes:
        try:
            o = cls(view)
            cmds.append((o, o.name()))
        except Exception as e:
            _instantiation_error(cls, e)
    return cmds


def on_api_ready():
    global api_ready
    api_ready = True

    for plc in deferred_plugin_loadeds:
        try:
            plc()
        except:
            traceback.print_exc()
    deferred_plugin_loadeds.clear()

    # Create ViewEventListener instances
    if view_event_listener_classes:
        for w in sublime.windows():
            for v in w.views(include_transient=True):
                attach_view(v)

    # Create TextEventListener instances
    if text_change_listener_classes:
        for buf in sublime._buffers():
            attach_buffer(buf)

    def init():
        on_init(None)

        # Synthesize an on_activated call
        w = sublime.active_window()
        if w:
            view_id = sublime_api.window_active_view(w.window_id)
            if view_id != 0:
                on_activated(view_id)

    sublime.set_timeout(init)


def is_view_event_listener_applicable(cls: type[ViewEventListener], view: sublime.View) -> bool:
    if not cls.is_applicable(view.settings()):
        return False

    if cls.applies_to_primary_view_only() and not view.is_primary():
        return False

    return True


def create_view_event_listeners(classes: list[type[ViewEventListener]], view: sublime.View):
    if classes:
        if view.view_id not in view_event_listeners:
            view_event_listeners[view.view_id] = []

        for c in classes:
            if is_view_event_listener_applicable(c, view):
                view_event_listeners[view.view_id].append(c(view))


def check_view_event_listeners(view: sublime.View):
    if view_event_listener_classes:
        if view.view_id not in view_event_listeners:
            view_event_listeners[view.view_id] = []

        listeners = view_event_listeners[view.view_id]

        for cls in view_event_listener_classes:
            instance = None
            for l in listeners:
                if l.__class__ is cls:
                    instance = l
                    break

            want = is_view_event_listener_applicable(cls, view)

            if want and instance is None:
                listeners.append(cls(view))
            elif instance is not None and not want:
                listeners.remove(instance)


def attach_view(view: sublime.View):
    if isinstance(view, int):
        view = sublime.View(view)

    check_view_event_listeners(view)

    view.settings().add_on_change(
        "check_view_event_listeners",
        lambda: check_view_event_listeners(view))


check_all_view_event_listeners_scheduled = False


def check_all_view_event_listeners():
    global check_all_view_event_listeners_scheduled
    check_all_view_event_listeners_scheduled = False

    for w in sublime.windows():
        for v in w.views(include_transient=True):
            check_view_event_listeners(v)


def detach_view(view_id: int):
    if view_id in view_event_listeners:
        del view_event_listeners[view_id]

    # A view has closed, which implies 'is_primary' may have changed, so see if
    # any of the ViewEventListener classes need to be created.
    # Call this in a timeout, as 'view' will still be reporting itself as a
    # primary at this stage
    global check_all_view_event_listeners_scheduled
    if not check_all_view_event_listeners_scheduled:
        check_all_view_event_listeners_scheduled = True
        sublime.set_timeout(check_all_view_event_listeners)


def find_view_event_listener(view: sublime.View, cls: type) -> ViewEventListener | None:
    if view.view_id in view_event_listeners:
        for vel in view_event_listeners[view.view_id]:
            if vel.__class__ is cls:
                return vel
    return None


def attach_buffer(buf: sublime.Buffer):
    for cls in text_change_listener_classes:
        if cls.is_applicable(buf):
            cls().attach(buf)


def check_text_change_listeners(buf: sublime.Buffer):
    if text_change_listener_classes:
        if buf.buffer_id not in text_change_listeners:
            text_change_listeners[buf.buffer_id] = []

        listeners = text_change_listeners[buf.buffer_id]

        for cls in text_change_listener_classes:
            instance = None
            for l in listeners:
                if l.__class__ is cls:
                    instance = l
                    break

            want = cls.is_applicable(buf)

            if want and instance is None:
                cls().attach(buf)
            elif instance is not None and not want:
                instance.detach()


def detach_buffer(buf: sublime.Buffer):
    if buf.buffer_id in text_change_listeners:
        listeners = text_change_listeners[buf.buffer_id]
        for tcl in listeners:
            tcl.detach()
        del text_change_listeners[buf.buffer_id]


def plugin_module_for_obj(obj: object) -> str:
    # Since objects in plugins may be defined deep in a sub-module, if we want
    # to filter by a module, we must make sure we are only looking at the
    # first two module labels
    cm = obj.__class__.__module__
    if cm.count('.') > 2:
        cm = '.'.join(cm.split('.', 2)[0:2])
    return cm


def el_callbacks(name: str) -> Generator[Callable[..., None]]:
    return (getattr(el, name) for el in all_callbacks[name])


def vel_callbacks(view: sublime.View, name: str) -> Generator[Callable[..., None]]:
    return (getattr(vel, name) for vel in view_event_listeners.get(view.view_id, [])
            if hasattr(vel, name))


def run_view_callbacks(name: str, view_id: int, *args: object, el_only: bool = False):
    v = sublime.View(view_id)

    for callback in el_callbacks(name):
        callback(v, *args)

    if el_only:
        return

    for callback in vel_callbacks(v, name):
        callback(*args)


def run_window_callbacks(name: str, window_id: int, *args: object):
    w = sublime.Window(window_id)

    for callback in el_callbacks(name):
        callback(w, *args)


def on_init(module: str | None):
    """
    Trigger the on_init() methods on EventListener and ViewEventListener
    objects. This is method that allows event listeners to run something
    once per view, even if the view is done loading before the listener
    starts listening.

    :param module:
        A unicode string of the name of a plugin module to filter listeners by

    :meta private:
    """

    buffers = sublime._buffers()

    for listener in all_callbacks['on_new_buffer']:
        if module is not None and plugin_module_for_obj(listener) != module:
            continue
        for b in buffers:
            listener.on_new_buffer(b)

    for listener in all_callbacks['on_new_buffer_async']:
        if module is not None and plugin_module_for_obj(listener) != module:
            continue

        def on_new_buffers_async(bufs=buffers, l=listener):
            for b in bufs:
                l.on_new_buffer_async(b)
        sublime.set_timeout_async(on_new_buffers_async, 0)

    views = [
        v
        for w in sublime.windows()
        for v in w.views(include_transient=True)
        if not v.is_loading()
    ]

    for listener in all_callbacks['on_init']:
        if module is not None and plugin_module_for_obj(listener) != module:
            continue
        listener.on_init(views)

    for v in views:
        for listener in view_event_listeners.get(v.view_id, []):
            if not hasattr(listener, 'on_init'):
                continue
            if module is not None and plugin_module_for_obj(listener) != module:
                continue
            listener.on_init()


def on_new(view_id: int):
    run_view_callbacks('on_new', view_id, el_only=True)


def on_new_async(view_id: int):
    run_view_callbacks('on_new_async', view_id, el_only=True)


def on_new_buffer(buffer_id: int):
    buf = sublime.Buffer(buffer_id)

    attach_buffer(buf)

    for callback in el_callbacks('on_new_buffer'):
        callback(buf)


def on_new_buffer_async(buffer_id: int):
    buf = sublime.Buffer(buffer_id)

    for callback in el_callbacks('on_new_buffer_async'):
        callback(buf)


def on_associate_buffer(buffer_id: int):
    buf = sublime.Buffer(buffer_id)

    check_text_change_listeners(buf)

    for callback in el_callbacks('on_associate_buffer'):
        callback(buf)


def on_associate_buffer_async(buffer_id: int):
    buf = sublime.Buffer(buffer_id)

    for callback in el_callbacks('on_associate_buffer_async'):
        callback(buf)


def on_close_buffer(buffer_id: int):
    buf = sublime.Buffer(buffer_id)

    detach_buffer(buf)

    for callback in el_callbacks('on_close_buffer'):
        callback(buf)


def on_close_buffer_async(buffer_id: int):
    buf = sublime.Buffer(buffer_id)

    for callback in el_callbacks('on_close_buffer_async'):
        callback(buf)


def on_clone(view_id: int):
    run_view_callbacks('on_clone', view_id, el_only=True)


def on_clone_async(view_id: int):
    run_view_callbacks('on_clone_async', view_id, el_only=True)


class Summary:
    def __init__(self):
        self.max: float = 0.0
        self.sum: float = 0.0
        self.count: int = 0

    def record(self, x: float):
        self.count += 1
        self.sum += x
        self.max = max(self.max, x)


def get_profiling_data() -> list[tuple[str, str, int, float, float]]:
    return [
        (event, plugin, s.count, s.max, s.sum)
        for event, data in profile.items()
        for plugin, s in data.items()
    ]


def on_load(view_id: int):
    run_view_callbacks('on_load', view_id)


def on_load_async(view_id: int):
    run_view_callbacks('on_load_async', view_id)


def on_revert(view_id: int):
    run_view_callbacks('on_revert', view_id)


def on_revert_async(view_id: int):
    run_view_callbacks('on_revert_async', view_id)


def on_reload(view_id: int):
    run_view_callbacks('on_reload', view_id)


def on_reload_async(view_id: int):
    run_view_callbacks('on_reload_async', view_id)


def on_pre_close(view_id: int):
    run_view_callbacks('on_pre_close', view_id)


def on_close(view_id: int):
    run_view_callbacks('on_close', view_id)


def on_pre_save(view_id: int):
    run_view_callbacks('on_pre_save', view_id)


def on_pre_save_async(view_id: int):
    run_view_callbacks('on_pre_save_async', view_id)


def on_post_save(view_id: int):
    run_view_callbacks('on_post_save', view_id)


def on_post_save_async(view_id: int):
    run_view_callbacks('on_post_save_async', view_id)


def on_pre_move(view_id: int):
    run_view_callbacks('on_pre_move', view_id)


def on_post_move(view_id: int):
    run_view_callbacks('on_post_move', view_id)


def on_post_move_async(view_id: int):
    run_view_callbacks('on_post_move_async', view_id)


def on_modified(view_id: int):
    run_view_callbacks('on_modified', view_id)


def on_modified_async(view_id: int):
    run_view_callbacks('on_modified_async', view_id)


def on_selection_modified(view_id: int):
    run_view_callbacks('on_selection_modified', view_id)


def on_selection_modified_async(view_id: int):
    run_view_callbacks('on_selection_modified_async', view_id)


def on_activated(view_id: int):
    run_view_callbacks('on_activated', view_id)


def on_activated_async(view_id: int):
    run_view_callbacks('on_activated_async', view_id)


def on_deactivated(view_id: int):
    run_view_callbacks('on_deactivated', view_id)


def on_deactivated_async(view_id: int):
    run_view_callbacks('on_deactivated_async', view_id)


def on_query_context(view_id: int, key: str, operator: str, operand: str, match_all: bool) -> bool:
    v = sublime.View(view_id)
    for callback in el_callbacks('on_query_context'):
        val = callback(v, key, operator, operand, match_all)
        if val:
            return True
    for callback in vel_callbacks(v, 'on_query_context'):
        val = callback(key, operator, operand, match_all)
        if val:
            return True
    return False


def split_trigger(trigger: str) -> tuple[str, str]:
    idx = trigger.find("\t")
    if idx < 0:
        return (trigger, "")
    else:
        return (trigger[0:idx], trigger[idx + 1:])


def on_query_completions(view_id: int, req_id: int, prefix: str, locations: Point):
    v = sublime.View(view_id)

    mlist = sublime_api.MultiCompletionList(view_id, req_id)

    def norm_res(
        res: list[CompletionValue] | tuple[list[CompletionValue], AutoCompleteFlags] | sublime.CompletionList | None
    ) -> sublime.CompletionList:
        if isinstance(res, sublime.CompletionList):
            return res
        elif isinstance(res, tuple):
            return sublime.CompletionList(res[0], flags=res[1])
        elif isinstance(res, list):
            return sublime.CompletionList(res)
        else:
            return sublime.CompletionList([])

    for callback in el_callbacks('on_query_completions'):
        mlist.append(norm_res(callback(v, prefix, locations)))

    for callback in vel_callbacks(v, 'on_query_completions'):
        mlist.append(norm_res(callback(prefix, locations)))

    mlist.ready()


def on_hover(view_id: int, point: Point, hover_zone: sublime.HoverZone):
    run_view_callbacks('on_hover', view_id, point, hover_zone)


def on_text_command(view_id: int, name: str, args: CommandArgs) -> tuple[str, Value]:
    v = sublime.View(view_id)

    for callback in vel_callbacks(v, 'on_text_command'):
        res = callback(name, args)
        if isinstance(res, tuple):
            return res
        if res:
            return (res, None)

    for callback in el_callbacks('on_text_command'):
        res = callback(v, name, args)
        if isinstance(res, tuple):
            return res
        if res:
            return (res, None)

    return ("", None)


def on_window_command(window_id: int, name: str, args: CommandArgs) -> tuple[str, Value]:
    w = sublime.Window(window_id)
    for callback in el_callbacks('on_window_command'):
        res = callback(w, name, args)
        if isinstance(res, tuple):
            return res
        if res:
            return (res, None)

    return ("", None)


def on_post_text_command(view_id: int, name: str, args: CommandArgs):
    run_view_callbacks('on_post_text_command', view_id, name, args)


def on_post_window_command(window_id: int, name: str, args: CommandArgs):
    run_window_callbacks('on_post_window_command', window_id, name, args)


def on_new_project(window_id: int):
    run_window_callbacks('on_new_project', window_id)


def on_new_project_async(window_id: int):
    run_window_callbacks('on_new_project_async', window_id)


def on_load_project(window_id: int):
    run_window_callbacks('on_load_project', window_id)


def on_load_project_async(window_id: int):
    run_window_callbacks('on_load_project_async', window_id)


def on_pre_save_project(window_id: int):
    run_window_callbacks('on_pre_save_project', window_id)


def on_post_save_project(window_id: int):
    run_window_callbacks('on_post_save_project', window_id)


def on_post_save_project_async(window_id: int):
    run_window_callbacks('on_post_save_project_async', window_id)


def on_pre_close_project(window_id: int):
    run_window_callbacks('on_pre_close_project', window_id)


def on_new_window(window_id: int):
    run_window_callbacks('on_new_window', window_id)


def on_new_window_async(window_id: int):
    run_window_callbacks('on_new_window_async', window_id)


def on_pre_close_window(window_id: int):
    run_window_callbacks('on_pre_close_window', window_id)


def on_exit(log_path: str):
    # on_exit() is called once the API it shutdown, which means that stdout
    # will not be visible for debugging. Thus we write to a log file.
    stdout = io.StringIO()
    sys.stdout = stdout
    sys.stderr = stdout

    for callback in el_callbacks('on_exit'):
        callback()

    if len(stdout.getvalue()):
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(stdout.getvalue())
    else:
        os.unlink(log_path)


def split_identifier(s):
    part_start = 0

    for i, c in enumerate(s):
        if i == part_start:
            is_upper = c.isupper()

        if c.isupper():
            # If an upper-case follows a lower-case then that's a split
            if not is_upper:
                yield s[part_start:i]
                part_start = i
                is_upper = True

        elif c.islower():
            # If a lower-case follows a series of upper-case that's a split
            if is_upper and i - part_start > 1:
                yield s[part_start:i - 1]
                part_start = i - 1

            is_upper = False

        elif c in (' ', '\t', '_', '-'):
            yield s[part_start:i]
            part_start = i + 1

        else:
            # Numbers/symbols are treated as a lower-case sequence, so
            # that "A1B" gets split as "A1","B". But they do not cause a split,
            # so that "HTTP1" and "A11y" are not split.
            is_upper = False

    if part_start < len(s):
        yield s[part_start:]


class CommandInputHandler:
    """
    """

    def name(self) -> str:
        """
        The command argument name this input handler is editing. Defaults to
        ``foo_bar`` for an input handler named ``FooBarInputHandler``.
        """
        clsname = self.__class__.__name__
        name = '_'.join(n.lower() for n in split_identifier(clsname))
        if name.endswith("_input_handler"):
            name = name[0:-14]
        return name

    def placeholder(self) -> str:
        """
        Placeholder text is shown in the text entry box before the user has
        entered anything. Empty by default.
        """
        return ""

    def initial_text(self) -> str:
        """
        Initial text shown in the text entry box. Empty by default.
        """
        return ""

    def initial_selection(self) -> list[tuple[int, int]]:
        """
        A list of 2-element tuples, defining the initially selected parts of the
        initial text.

        .. since:: 4081
        """
        return []

    def preview(self, text: str) -> str | sublime.Html:
        """
        Called whenever the user changes the text in the entry box. The returned
        value (either plain text or HTML) will be shown in the preview area of
        the *Command Palette*.
        """
        return ""

    def validate(self, text: str, event: Event | None = None) -> bool:
        """
        Called whenever the user presses enter in the text entry box.
        Return :py:`False` to disallow the current value.

        :param event: Only passed when `want_event` returns ``True``.
        """
        return True

    def cancel(self):
        """
        Called when the input handler is canceled, either by the user pressing
        backspace or escape.
        """

    def confirm(self, text: str, event: Event | None = None):
        """
        Called when the input is accepted, after the user has pressed enter and
        the text has been validated.

        :param event: Only passed when `want_event` returns ``True``.
        """

    def next_input(self, args) -> CommandInputHandler | None:
        """
        Return the next input after the user has completed this one. May return
        :py:`None` to indicate no more input is required, or
        `sublime_plugin.BackInputHandler()` to indicate that the input handler
        should be popped off the stack instead.
        """
        return None

    def create_input_handler_(self, args: CommandArgs) -> CommandInputHandler | None:
        return self.next_input(args)

    def preview_(self, v: str) -> tuple[str | sublime.Html, int]:
        ret = self.preview(v)

        if ret is None:
            return ("", 0)
        elif isinstance(ret, sublime.Html):
            return (ret.data, 1)
        else:
            return (ret, 0)

    def validate_(self, v: str, event: Event | None) -> bool:
        if self.want_event():
            return self.validate(v, event)
        return self.validate(v)

    def cancel_(self):
        self.cancel()

    def confirm_(self, v: str, event: Event | None):
        if self.want_event():
            self.confirm(v, event)
        else:
            self.confirm(v)

    def want_event(self) -> bool:
        """
        Whether the `validate()` and `confirm()` methods should received a
        second `Event` parameter. Returns :py:`False` by default.

        .. since:: 4096
        """
        return False


class BackInputHandler(CommandInputHandler):
    """
    """

    def name(self) -> str:
        return "_Back"


class TextInputHandler(CommandInputHandler):
    """
    TextInputHandlers can be used to accept textual input in the *Command
    Palette*. Return a subclass of this from `Command.input()`.

    *For an input handler to be shown to the user, the command returning the
    input handler MUST be made available in the Command Palette by adding the
    command to a :path:`Default.sublime-commands` file.*
    """
    def description(self, text: str) -> str:
        """
        The text to show in the *Command Palette* when this input handler is not
        at the top of the input handler stack. Defaults to the text the user
        entered.
        """
        return text

    def setup_(self, args: CommandArgs) -> tuple[list[object], dict[str, Value]]:
        props = {
            "initial_text": self.initial_text(),
            "initial_selection": self.initial_selection(),
            "placeholder_text": self.placeholder(),
            "type": "text",
        }

        return ([], props)

    def description_(self, value: Value, text: str) -> str:
        res = self.description(text)
        if res is None:
            return ""
        return res


class ListInputHandler(CommandInputHandler):
    """
    ListInputHandlers can be used to accept a choice input from a list items in
    the *Command Palette*. Return a subclass of this from `Command.input()`.

    *For an input handler to be shown to the user, the command returning the
    input handler MUST be made available in the Command Palette by adding the
    command to a :path:`Default.sublime-commands` file.*
    """

    def list_items(self) -> list[str] | \
            tuple[list[str], int] | \
            list[tuple[str, Value]] | \
            tuple[list[tuple[str, Value]], int] | \
            list[sublime.ListInputItem] | \
            tuple[list[sublime.ListInputItem], int]:
        """
        This method should return the items to show in the list.

        The returned value may be a ``list`` of item, or a 2-element ``tuple``
        containing a list of items, and an ``int`` index of the item to
        pre-select.

        The each item in the list may be one of:

        * A string used for both the row text and the value passed to the
          command
        * A 2-element tuple containing a string for the row text, and a `Value`
          to pass to the command
        * .. since:: 4095
            A `sublime.ListInputItem` object
        """
        return []

    def description(self, value: Value, text: str) -> str:
        """
        The text to show in the *Command Palette* when this input handler is not
        at the top of the input handler stack. Defaults to the text of the list
        item the user selected.
        """
        return text

    def setup_(self, args: CommandArgs) -> tuple[list[object], dict[str, Value]]:
        items = self.list_items()

        selected_item_index = -1

        if isinstance(items, tuple):
            items, selected_item_index = items

        item_tuples = []
        for item in items:
            if isinstance(item, str):
                item_tuples.append((item, item))
            elif isinstance(item, (list, tuple)):
                item_tuples.append(item)
            elif isinstance(item, sublime.ListInputItem):
                details = "\x1f".join(item.details) if isinstance(item.details, (list, tuple)) else item.details
                if item.annotation != "" or item.kind != (sublime.KIND_ID_AMBIGUOUS, "", ""):
                    kind_letter = 0
                    if isinstance(item.kind[1], str) and len(item.kind[1]) == 1:
                        kind_letter = ord(item.kind[1])
                    item_tuples.append((
                        (
                            item.text,
                            details,
                            item.annotation,
                            (item.kind[0], kind_letter, item.kind[2])
                        ),
                        item.value
                    ))
                elif details is not None and details != "":
                    item_tuples.append(((item.text, details, True), item.value))
                else:
                    item_tuples.append((item.text, item.value))
            else:
                raise TypeError("items must contain only str, list, tuple or sublime.ListInputItem objects")

        props = {
            "initial_text": self.initial_text(),
            "initial_selection": self.initial_selection(),
            "placeholder_text": self.placeholder(),
            "selected": selected_item_index,
            "type": "list",
        }

        return (item_tuples, props)

    def description_(self, value: Value, text: str) -> str:
        res = self.description(value, text)
        if res is None:
            return ""
        return res


class Command:
    """
    """

    def name(self) -> str:
        """
        Return the name of the command. By default this is derived from the name
        of the class.
        """
        clsname = self.__class__.__name__
        name = '_'.join(n.lower() for n in split_identifier(clsname))
        if name.endswith("_command"):
            name = name[0:-8]
        return name

    def is_enabled_(self, args: CommandArgs) -> bool:
        ret = None
        try:
            args = self.filter_args(args)
            if args:
                ret = self.is_enabled(**args)
            else:
                ret = self.is_enabled()
        except TypeError:
            ret = self.is_enabled()

        if not isinstance(ret, bool):
            raise ValueError("is_enabled must return a bool", self)

        return ret

    def is_enabled(self) -> bool:
        """
        Return whether the command is able to be run at this time. Command
        arguments are passed as keyword arguments. The default implementation
        simply always returns :py:`True`.
        """
        return True

    def is_visible_(self, args: CommandArgs) -> bool:
        ret = None
        try:
            args = self.filter_args(args)
            if args:
                ret = self.is_visible(**args)
            else:
                ret = self.is_visible()
        except TypeError:
            ret = self.is_visible()

        if not isinstance(ret, bool):
            raise ValueError("is_visible must return a bool", self)

        return ret

    def is_visible(self) -> bool:
        """
        Return whether the command should be shown in the menu at this time.
        Command arguments are passed as keyword arguments. The default
        implementation always returns :py:`True`.
        """
        return True

    def is_checked_(self, args: CommandArgs) -> bool:
        ret = None
        try:
            args = self.filter_args(args)
            if args:
                ret = self.is_checked(**args)
            else:
                ret = self.is_checked()
        except TypeError:
            ret = self.is_checked()

        if not isinstance(ret, bool):
            raise ValueError("is_checked must return a bool", self)

        return ret

    def is_checked(self) -> bool:
        """
        Return whether a checkbox should be shown next to the menu item. Command
        arguments are passed as keyword arguments. The :path:`.sublime-menu`
        file must have the ``"checkbox"`` key set to :json:`true` for this to
        be used.
        """
        return False

    def description_(self, args: CommandArgs) -> str:
        try:
            args = self.filter_args(args)
            if args is not None:
                res = self.description(**args)
            else:
                res = self.description()
            if res is None:
                return ""
            return res
        except TypeError:
            return ""

    def description(self) -> str | None:
        """
        Return a description of the command with the given arguments. Command
        arguments are passed as keyword arguments. Used in the menu, if no
        caption is provided. Return :py:`None` to get the default description.
        """
        return ""

    def filter_args(self, args: CommandArgs) -> CommandArgs:
        if args:
            if 'event' in args and not self.want_event():
                args = args.copy()
                del args['event']

        return args

    def want_event(self) -> bool:
        """
        Return whether to receive an `Event` argument when the command is
        triggered by a mouse action. The event information allows commands to
        determine which portion of the view was clicked on. The default
        implementation returns :py:`False`.
        """
        return False

    def input(self, args: dict) -> CommandInputHandler | None:
        """
        If this returns something other than :py:`None`, the user will be
        prompted for an input before the command is run in the *Command
        Palette*.

        .. since:: 3154
        """
        return None

    def input_description(self) -> str:
        """
        Allows a custom name to be show to the left of the cursor in the input
        box, instead of the default one generated from the command name.

        .. since:: 3154
        """
        return ""

    def create_input_handler_(self, args: CommandArgs) -> CommandInputHandler | None:
        return self.input(args)

    def run(self, **kwargs: Value):
        """
        Called when the command is run. Command arguments are passed as keyword
        arguments.
        """


class ApplicationCommand(Command):
    """
    A `Command` instantiated just once.
    """
    def run_(self, edit_token: int, args: CommandArgs):
        args = self.filter_args(args)
        try:
            if args:
                return self.run(**args)
            else:
                return self.run()
        except TypeError as e:
            if 'required positional argument' in str(e):
                if sublime_api.can_accept_input(self.name(), args):
                    sublime.active_window().run_command(
                        'show_overlay',
                        {
                            'overlay': 'command_palette',
                            'command': self.name(),
                            'args': args
                        }
                    )
                    return
            raise

    def run(self, **kwargs: Value):
        """
        Called when the command is run. Command arguments are passed as keyword
        arguments.
        """


class WindowCommand(Command):
    """
    A `Command` instantiated once per window. The `Window` object may be
    retrieved via `self.window <window>`.
    """

    def __init__(self, window: sublime.Window):
        """ :meta private: """
        super().__init__()

        self.window: sublime.Window = window
        """ The `Window` this command is attached to. """

    def run_(self, edit_token: int, args: CommandArgs):
        args = self.filter_args(args)
        try:
            if args:
                return self.run(**args)
            else:
                return self.run()
        except TypeError as e:
            if 'required positional argument' in str(e):
                if sublime_api.window_can_accept_input(self.window.id(), self.name(), args):
                    sublime_api.window_run_command(
                        self.window.id(),
                        'show_overlay',
                        {
                            'overlay': 'command_palette',
                            'command': self.name(),
                            'args': args
                        }
                    )
                    return
            raise

    def run(self, **kwargs: Value):
        """
        Called when the command is run. Command arguments are passed as keyword
        arguments.
        """


class TextCommand(Command):
    """
    A `Command` instantiated once per `View`. The `View` object may be retrieved
    via `self.view <view>`.
    """

    def __init__(self, view: sublime.View):
        """ :meta private: """
        super().__init__()

        self.view: sublime.View = view
        """ The `View` this command is attached to. """

    def run_(self, edit_token: int, args: CommandArgs):
        args = self.filter_args(args)
        try:
            if args:
                edit = self.view.begin_edit(edit_token, self.name(), args)
                try:
                    return self.run(edit, **args)
                finally:
                    self.view.end_edit(edit)
            else:
                edit = self.view.begin_edit(edit_token, self.name())
                try:
                    return self.run(edit)
                finally:
                    self.view.end_edit(edit)
        except TypeError as e:
            if 'required positional argument' in str(e):
                if sublime_api.view_can_accept_input(self.view.id(), self.name(), args):
                    sublime_api.window_run_command(
                        sublime_api.view_window(self.view.id()),
                        'show_overlay',
                        {
                            'overlay': 'command_palette',
                            'command': self.name(),
                            'args': args
                        }
                    )
                    return
            raise

    def run(self, edit: sublime.Edit, **kwargs: Value):
        """
        Called when the command is run. Command arguments are passed as keyword
        arguments.
        """


class EventListener:
    """
    .. method:: on_init(views: List[View])

        Called once with a list of views that were loaded before the
        EventListener was instantiated

        .. since:: 4050

    .. method:: on_exit()

        Called once after the API has shut down, immediately before the
        plugin_host process exits

        .. since:: 4050

    .. method:: on_new(view: View)

        Called when a new file is created.

    .. method:: on_new_async(view: View)

        Called when a new buffer is created. Runs in a separate thread, and does
        not block the application.

    .. method:: on_associate_buffer(buffer: View)

        Called when a buffer is associated with a file. buffer will be a Buffer
        object.

        .. since:: 4084

    .. method:: on_associate_buffer_async(buffer: View)

        Called when a buffer is associated with file. Runs in a separate thread,
        and does not block the application. buffer will be a Buffer object.

        .. since:: 4084

    .. method:: on_clone(view: View)

        Called when a view is cloned from an existing one.

    .. method:: on_clone_async(view: View)

        Called when a view is cloned from an existing one. Runs in a separate
        thread, and does not block the application.

    .. method:: on_load(view: View)

        Called when the file is finished loading.

    .. method:: on_load_async(view: View)

        Called when the file is finished loading. Runs in a separate thread, and
        does not block the application.

    .. method:: on_reload(view: View)

        Called when the View is reloaded.

        .. since:: 4050

    .. method:: on_reload_async(view: View)

        Called when the View is reloaded. Runs in a separate thread, and does
        not block the application.

        .. since:: 4050

    .. method:: on_revert(view: View)

        Called when the View is reverted.

        .. since:: 4050

    .. method:: on_revert_async(view: View)

        Called when the View is reverted. Runs in a separate thread, and does
        not block the application.

        .. since:: 4050

    .. method:: on_pre_move(view: View)

        Called right before a view is moved between two windows or within a
        window. Passed the View object.

        .. since:: 4050

    .. method:: on_post_move(view: View)

        Called right after a view is moved between two windows or within a
        window. Passed the View object.

        .. since:: 4050

    .. method:: on_post_move_async(view: View)

        Called right after a view is moved between two windows or within a
        window. Passed the View object. Runs in a separate thread, and does not
        block the application.

        .. since:: 4050

    .. method:: on_pre_close(view: View)

        Called when a view is about to be closed. The view will still be in the
        window at this point.

    .. method:: on_close(view: View)

        Called when a view is closed (note, there may still be other views into
        the same buffer).

    .. method:: on_pre_save(view: View)

        Called just before a view is saved.

    .. method:: on_pre_save_async(view: View)

        Called just before a view is saved. Runs in a separate thread, and does
        not block the application.

    .. method:: on_post_save(view: View)

        Called after a view has been saved.

    .. method:: on_post_save_async(view: View)

        Called after a view has been saved. Runs in a separate thread, and does
        not block the application.

    .. method:: on_modified(view: View)

        Called after changes have been made to a view.

    .. method:: on_modified_async(view: View)

        Called after changes have been made to a view. Runs in a separate
        thread, and does not block the application.

    .. method:: on_selection_modified(view: View)

        Called after the selection has been modified in a view.

    .. method:: on_selection_modified_async(view: View)

        Called after the selection has been modified in a view. Runs in a
        separate thread, and does not block the application.

    .. method:: on_activated(view: View)

        Called when a view gains input focus.

    .. method:: on_activated_async(view: View)

        Called when a view gains input focus. Runs in a separate thread, and
        does not block the application.

    .. method:: on_deactivated(view: View)

        Called when a view loses input focus.

    .. method:: on_deactivated_async(view: View)

        Called when a view loses input focus. Runs in a separate thread, and
        does not block the application.

    .. method:: on_hover(view: View, point: Point, hover_zone: HoverZone)

        Called when the user's mouse hovers over the view for a short period.

        :param view: The view
        :param point:
            The closest point in the view to the mouse location. The mouse may
            not actually be located adjacent based on the value of
            ``hover_zone``.
        :param hover_zone:
            Which element in Sublime Text the mouse has hovered over.

    .. method:: on_query_context(\
            view: View, key: str, operator: QueryOperator, operand: Value, match_all: bool) -> bool | None

        Called when determining to trigger a key binding with the given context
        key. If the plugin knows how to respond to the context, it should
        return either True of False. If the context is unknown, it should
        return None.

        :param key:
            The context key to query. This generally refers to specific state
            held by a plugin.
        :param operator:
            The operator to check against the operand; whether to check
            equality, inequality, etc.
        :param operand: The value against which to check using the ``operator``.
        :param match_all:
            This should be used if the context relates to the selections: does
            every selection have to match(``match_all == True``), or is at
            least one matching enough (``match_all == False``)?
        :returns:
            ``True`` or ``False`` if the plugin handles this context key and it
            either does or doesn't match. If the context is unknown return
            ``None``.

    .. method:: on_query_completions(view: View, prefix: str, locations: List[Point]) -> Union[\
            None, List[CompletionValue], tuple[List[CompletionValue], AutoCompleteFlags], CompletionList]

        Called whenever completions are to be presented to the user.

        :param prefix: The text already typed by the user.
        :param locations: The list of points being completed. Since this method
                          is called for all completions no matter the syntax,
                          ``self.view.match_selector(point, relevant_scope)``
                          should be called to determine if the point is
                          relevant.
        :returns: A list of completions in one of the valid formats or ``None`` if no completions are provided.

    .. method:: on_text_command(view: View, command_name: str, args: CommandArgs) -> (str, CommandArgs)

        Called when a text command is issued. The listener may return a
        (command, arguments) tuple to rewrite the command, or ``None`` to run
        the command unmodified.

    .. method:: on_window_command(window: Window, command_name: str, args: CommandArgs) -> (str, CommandArgs)

        Called when a window command is issued. The listener may return a
        (command, arguments) tuple to rewrite the command, or ``None`` to run
        the command unmodified.

    .. method:: on_post_text_command(view: View, command_name: str, args: CommandArgs)

        Called after a text command has been executed.

    .. method:: on_post_window_command(window: Window, command_name: str, args: CommandArgs)

        Called after a window command has been executed.

    .. method:: on_new_window(window: Window)

        Called when a window is created, passed the Window object.

        .. since:: 4050

    .. method:: on_new_window_async(window: Window)

        Called when a window is created, passed the Window object. Runs in a
        separate thread, and does not block the application.

        .. since:: 4050

    .. method:: on_pre_close_window(window: Window)

        Called right before a window is closed, passed the Window object.

        .. since:: 4050

    .. method:: on_new_project(window: Window)

        Called right after a new project is created, passed the Window object.

        .. since:: 4050

    .. method:: on_new_project_async(window: Window)

        Called right after a new project is created, passed the Window object.
        Runs in a separate thread, and does not block the application.

        .. since:: 4050

    .. method:: on_load_project(window: Window)

        Called right after a project is loaded, passed the Window object.

        .. since:: 4050

    .. method:: on_load_project_async(window: Window)

        Called right after a project is loaded, passed the Window object. Runs
        in a separate thread, and does not block the application.

        .. since:: 4050

    .. method:: on_pre_save_project(window: Window)

        Called right before a project is saved, passed the Window object.

        .. since:: 4050

    .. method:: on_post_save_project(window: Window)

        Called right after a project is saved, passed the Window object.

        .. since:: 4050

    .. method:: on_post_save_project_async(window: Window)

        Called right after a project is saved, passed the Window object. Runs in
        a separate thread, and does not block the application.

        .. since:: 4050

    .. method:: on_pre_close_project(window: Window)

        Called right before a project is closed, passed the Window object.
    """


class ViewEventListener:
    """
     A class that provides similar event handling to `EventListener`, but bound
     to a specific view. Provides class method-based filtering to control what
     views objects are created for.

    .. method:: on_load()

        Called when the file is finished loading.

        .. since:: 3155

    .. method:: on_load_async()

        Same as `on_load` but runs in a separate thread, not blocking the
        application.

        .. since:: 3155

    .. method:: on_reload()

        Called when the file is reloaded.

        .. since:: 4050

    .. method:: on_reload_async()

        Same as `on_reload` but runs in a separate thread, not blocking the
        application.

        .. since:: 4050

    .. method:: on_revert()

        Called when the file is reverted.

        .. since:: 4050

    .. method:: on_revert_async()

        Same as `on_revert` but runs in a separate thread, not blocking the
        application.

        .. since:: 4050

    .. method:: on_pre_move()

        Called right before a view is moved between two windows or within a
        window.

        .. since:: 4050

    .. method:: on_post_move()

        Called right after a view is moved between two windows or within a
        window.

        .. since:: 4050

    .. method:: on_post_move_async()

        Same as `on_post_move` but runs in a separate thread, not blocking the
        application.

        .. since:: 4050

    .. method:: on_pre_close()

        Called when a view is about to be closed. The view will still be in the
        window at this point.

        .. since:: 3155

    .. method:: on_close()

        Called when a view is closed (note, there may still be other views into
        the same buffer).

        .. since:: 3155

    .. method:: on_pre_save()

        Called just before a view is saved.

        .. since:: 3155

    .. method:: on_pre_save_async()

        Same as `on_pre_save` but runs in a separate thread, not blocking the
        application.

        .. since:: 3155

    .. method:: on_post_save()

        Called after a view has been saved.

        .. since:: 3155

    .. method:: on_post_save_async()

        Same as `on_post_save` but runs in a separate thread, not blocking the
        application.

        .. since:: 3155

    .. method:: on_modified()

        Called after changes have been made to the view.

    .. method:: on_modified_async()

        Same as `on_modified` but runs in a separate thread, not blocking the
        application.

    .. method:: on_selection_modified()

        Called after the selection has been modified in the view.

    .. method:: on_selection_modified_async()

        Called after the selection has been modified in the view. Runs in a
        separate thread, and does not block the application.

    .. method:: on_activated()

        Called when a view gains input focus.

    .. method:: on_activated_async()

        Called when the view gains input focus. Runs in a separate thread, and
        does not block the application.

    .. method:: on_deactivated()

        Called when the view loses input focus.

    .. method:: on_deactivated_async()

        Called when the view loses input focus. Runs in a separate thread, and
        does not block the application.

    .. method:: on_hover(point: Point, hover_zone: HoverZone)

        Called when the user's mouse hovers over the view for a short period.

        :param point:
            The closest point in the view to the mouse location. The mouse may
            not actually be located adjacent based on the value of
            ``hover_zone``.
        :param hover_zone:
            Which element in Sublime Text the mouse has hovered over.

    .. method:: on_query_context(key: str, operator: QueryOperator, operand: Value, match_all: bool) -> bool | None

        Called when determining to trigger a key binding with the given context
        key. If the plugin knows how to respond to the context, it should
        return either True of False. If the context is unknown, it should
        return None.

        :param key: The context key to query. This generally refers to specific
                    state held by a plugin.
        :param operator: The operator to check against the operand; whether to
                         check equality, inequality, etc.
        :param operand: The value against which to check using the ``operator``.
        :param match_all: This should be used if the context relates to the
                          selections: does every selection have to match
                          (``match_all == True``), or is at least one matching
                          enough (``match_all == False``)?
        :returns: ``True`` or ``False`` if the plugin handles this context key
                  and it either does or doesn't match. If the context is unknown
                  return ``None``.

    .. method:: on_query_completions(prefix: str, locations: List[Point]) -> Union[\
            None, List[CompletionValue], tuple[List[CompletionValue], AutoCompleteFlags], CompletionList]

        Called whenever completions are to be presented to the user.

        :param prefix: The text already typed by the user.
        :param locations: The list of points being completed. Since this method
                          is called for all completions no matter the syntax,
                          ``self.view.match_selector(point, relevant_scope)``
                          should be called to determine if the point is
                          relevant.
        :returns: A list of completions in one of the valid formats or ``None`` if no completions are provided.

    .. method:: on_text_command(command_name: str, args: CommandArgs) -> tuple[str, CommandArgs]

        Called when a text command is issued. The listener may return a
        `` (command, arguments)`` tuple to rewrite the command, or ``None`` to
        run the command unmodified.

        .. since:: 3155

    .. method:: on_post_text_command(command_name: str, args: CommandArgs)

        Called after a text command has been executed.
    """

    @classmethod
    def is_applicable(cls, settings: sublime.Settings) -> bool:
        """
        :returns: Whether this listener should apply to a view with the given `Settings`.
        """
        return True

    @classmethod
    def applies_to_primary_view_only(cls) -> bool:
        """
        :returns: Whether this listener should apply only to the primary view
                  for a file or all of its clones as well.
        """
        return True

    def __init__(self, view: sublime.View):
        super().__init__()

        self.view: sublime.View = view


class TextChangeListener:
    """
    A class that provides event handling about text changes made to a specific
    Buffer. Is separate from `ViewEventListener` since multiple views can
    share a single buffer.

    .. since:: 4081

    .. method:: on_text_changed(changes: List[TextChange])

        Called once after changes has been made to a buffer, with detailed
        information about what has changed.

    .. method:: on_text_changed_async(changes: List[TextChange]):

        Same as `on_text_changed` but runs in a separate thread, not blocking
        the application.

    .. method:: on_revert()

        Called when the buffer is reverted.

        A revert does not trigger text changes. If the contents of the buffer
        are required here use `View.substr`.

    .. method:: on_revert_async()

        Same as `on_revert` but runs in a separate thread, not blocking the
        application.

    .. method:: on_reload()

        Called when the buffer is reloaded.

        A reload does not trigger text changes. If the contents of the buffer
        are required here use `View.substr`.

    .. method:: on_reload_async()

        Same as `on_reload` but runs in a separate thread, not blocking the
        application.
    """

    @classmethod
    def is_applicable(cls, buffer: sublime.Buffer) -> bool:
        """
        :returns: Whether this listener should apply to the provided buffer.
        """
        return True

    def __init__(self):
        """ """
        super().__init__()

        self.__key: str | None = None
        self.buffer: sublime.Buffer | None = None

    def detach(self):
        """
        Remove this listener from the buffer.

        Async callbacks may still be called after this, as they are queued
        separately.

        :raises ValueError: if the listener is not attached.
        """
        if self.__key is None:
            raise ValueError('TextChangeListener is not attached')

        sublime_api.buffer_clear_text_listener(self.buffer.buffer_id, self.__key)
        if self.buffer.buffer_id in text_change_listeners:
            new_listeners = [
                listener
                for listener in text_change_listeners[self.buffer.buffer_id]
                if listener is not self
            ]
            text_change_listeners[self.buffer.buffer_id] = new_listeners
        self.__key = None

    def attach(self, buffer: sublime.Buffer):
        """
        Attach this listener to a buffer.

        :raises ValueError: if the listener is already attached.
        """
        if not isinstance(buffer, sublime.Buffer):
            raise TypeError('Must be a buffer')

        if self.__key is not None:
            raise ValueError('TextChangeListener is already attached')

        self.buffer = buffer
        if buffer.buffer_id not in text_change_listeners:
            text_change_listeners[buffer.buffer_id] = []
        text_change_listeners[buffer.buffer_id].append(self)
        self.__key = sublime_api.buffer_add_text_listener(buffer.buffer_id, self)

    def is_attached(self) -> bool:
        """
        :returns:
            whether the listener is receiving events from a buffer. May not be
            called from ``__init__``.
        """
        return self.__key is not None


class PackagePathFinder(importlib.abc.MetaPathFinder):
    """ :meta private: """

    def __init__(self):
        self.packages = {}

    def add_package(self, package):
        name = os.path.splitext(os.path.basename(package))[0]
        self.packages[name] = package

    def update_packages(self, pkgs):
        self.packages = {}

        for p in pkgs:
            self.add_package(p)

    def find_spec(self, fullname, path, target=None):
        parts = fullname.partition('.')
        archive = parts[0]

        package = self.packages.get(archive)
        if not package:
            return None

        res_path = f'Packages/{fullname.replace('.', '/')}'

        paths = [
            (f'{res_path}/__init__.pyc', True, True),
            (f'{res_path}/__init__.py', False, True),
            (f'{res_path}.pyc', True, False),
            (f'{res_path}.py', False, False),
        ]

        make_loader = True

        for (path, is_bytecode, is_package) in paths:
            if file_stats := sublime_api.stat_resource_file(path):
                break
        else:
            if file_stats := sublime_api.stat_resource_dir(res_path):
                path = res_path
                is_bytecode = False
                is_package = True
                make_loader = False
            else:
                return None

        fullpath, size, write_time = file_stats

        if make_loader:
            path_stats = {'size': size, 'mtime': write_time}

            loader_t = (PackageSourcelessFileLoader if is_bytecode else PackageSourceFileLoader)
            loader = loader_t(fullname, fullpath, path, path_stats)
        else:
            loader = None

        spec = importlib.util.spec_from_loader(
            fullname,
            loader,
            origin=fullpath,
            is_package=is_package
        )
        spec.has_location = True
        if is_package:
            spec.submodule_search_locations = [package]
        return spec


class PackageSourceFileLoader(importlib.machinery.SourceFileLoader):
    """ :meta private: """

    def __init__(self, fullname, path, resource_path, path_stats):
        super().__init__(fullname, path)

        self.resource_path = resource_path
        self._path_stats = path_stats

    def path_stats(self, path):
        return self._path_stats

    def get_data(self, path):
        ext = os.path.splitext(path)[1]
        if ext not in ('.pyc', '.py'):
            return b''

        # .pyc files can end up outside our packages path if they're contained
        # in __pycache__, so first try to load them from the filesystem.
        if ext == '.pyc':
            try:
                with io.open_code(path) as f:
                    return f.read()
            except:
                pass

        res = sublime_api.load_binary_resource(self.resource_path, -1)
        if isinstance(res, type):
            # Ignore errors, just return empty.
            return b''
        return res


class PackageSourcelessFileLoader(importlib.machinery.SourcelessFileLoader):
    """ :meta private: """

    def __init__(self, fullname, path, resource_path, path_stats):
        super().__init__(fullname, path)

        self.resource_path = resource_path
        self._path_stats = path_stats

    def path_stats(self, path):
        return self._path_stats

    # This has all the same logic as PackageSourceFileLoader, but with a
    # different parent
    get_data = PackageSourceFileLoader.get_data


multi_importer = PackagePathFinder()
sys.meta_path.insert(0, multi_importer)


def update_compressed_packages(pkgs):
    multi_importer.update_packages(pkgs)


# Setup site packages to process pth files. We check for existence of the API
# function to catch import mocks, such as when generating docs.
if sublime_api.lib_path:
    # setup site and handle .pth files.
    site.addsitedir(os.path.join(sublime.lib_path(), "python314"))

    if not os.environ.get('SSL_CERT_FILE'):
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
