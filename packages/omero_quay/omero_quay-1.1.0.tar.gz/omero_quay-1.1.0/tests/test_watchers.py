from __future__ import annotations

from omero_quay.watchers.omero import OmeroWatcher


def test_omero_watcher(conf):
    watcher = OmeroWatcher(conf, host="localhost")
    with watcher:
        events = watcher.find_events(since=10)
        if events:
            manifest = watcher.gen_manifest(*events)
            assert manifest
