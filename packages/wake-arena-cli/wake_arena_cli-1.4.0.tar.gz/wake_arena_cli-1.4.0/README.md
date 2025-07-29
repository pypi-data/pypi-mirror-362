# Wake Arena CLI
Wake Arena command line interface to operate projects and vulnerability checks based on [Wake](https://github.com/Ackee-Blockchain/wake) testing tool.


## Quick start 🚀
1. Install wake are na cli
```shell
pip install wake-arena-cli
```
2. Initialize the CLI
```shell
wake-arena init
```
3. (optional) If you don't have any Wake version installed, use `wake install` and `wake use` command to activate specific version you want
```shell
wake-arena wake install
wake-arena wake use
```
4. Perform security audit using remote Wake execution
```shell
wake-arena check
```

## Env parameters 🚩
| Env                   | Description                                                        |
|-----------------------|--------------------------------------------------------------------|
| `WAKE_ARENA_API_KEY`  | Uses api key instead of configured authentication                  |
| `WAKE_ARENA_PROJECT`  | Project id. CLI will use this project instead of configured one    |