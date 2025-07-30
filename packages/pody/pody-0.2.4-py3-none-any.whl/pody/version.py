
VERSION_HISTORY = {
    "0.1.9": [
        "Improve help route, format help output as table", 
    ], 
    "0.1.10": [
        "Remove /status route, add /host/spec and /version routes", 
    ], 
    "0.1.11": [
        "Use sqlite for logging", 
        "Add version client command",
        "Improve response for duplicate pod creation",
    ],
    "0.1.12": [
        "Allow image config without tag", 
        "Refactor docker controller using oop", 
        "Fix log keyerror for admin status change", 
        "Fix log level query for below py311", 
    ], 
    "0.1.13": [
        "Add optional instance name prefix", 
        "Improve pod name validation", 
    ], 
    "0.1.14": [
        "Fix for empty name prefix",
    ], 
    "0.1.15": [
        "Add shm_size quota", 
    ], 
    "0.2.0": [
        "Split user and quota database",
        "Add default fallback quota to config",
        "Remove previous database auto upgrade script",
        "Quota name change: storage limit -> storage size",
    ], 
    "0.2.1": [
        "Add `podx` command line tool",
        "Improve error handling for client",
        "Show help when fetching for path ending with /",
    ], 
    "0.2.2": [
        "Add gpu visibility to quota",
        "Use bind mount for volumes",
        "Fix log home directory initialization",
    ], 
    "0.2.3": [
        "Add `copy-id` command to copy public key to server", 
        "Add `pody-util` command and to generate systemd service file",
        "Change default service port to 8799"
    ],
    "0.2.4": [
        "Add `config` subcommand to `util` to edit configuration file",
        "Add `reset-quota` subcommand to `user` to reset user quota",
        "Add `--changelog` option to `pody version`", 
        "Reverse log show order",
        "Fix documentation",
    ],
}

VERSION = tuple([int(x) for x in list(VERSION_HISTORY.keys())[-1].split('.')])