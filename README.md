# CommanDeft

CommanDeft is a simple Python CLI tool designed to generate useful shell commands based on user prompts. It utilizes OpenAI's chat models to provide intelligent suggestions and help users compose shell commands quickly and efficiently.

## Requirements

- In order to use CommanDeft you will need an OpenAI API Key which will be asked of you during the initial configuration.
  You can easily get one from [HERE](https://platform.openai.com/account/api-keys)

-If you are using Linux you might have to install `xclip` using your package manager.  
For example, in Debian:
`sudo apt-get install xclip`

## Installation

To install CommanDeft, you can use the following command:

```sh
pip install commandeft
```


### Example Usage

1.  Generate a shell command based on a prompt:

    ```sh
    commandeft --prompt "list all files in the current directory"
    OR
    commandeft -p "list all files in the current directory"
    ```
    

    This will provide a shell command suggestion based on the given prompt:

    ```sh
    > ls -a
    ```


2.  Run CommanDeft in interactive mode:

    `commandeft --interactive`

    This will start CommanDeft in interactive mode, allowing you to input prompts and receive command suggestions directly within the CLI.

3.  Re-configure:

    `commandeft --configure`

    This will run the configuration flow for CommanDeft, allowing you to set up your preferences and customize the behavior of the tool.

## Configuration

During the initial configuration or when running:

```sh
commandeft --configure (or -c)
```

- You can choose the generated answer's `temperature`. Because this tool is geared towards code generation, lower temperatures perform better.
  More information about temeratures [HERE](https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api-a-few-tips-and-tricks-on-controlling-the-creativity-deterministic-output-of-prompt-responses/172683)
- You can choose the `max_token` value.  
  ⚠️ Keep in Mind that the guided prompt(assistant role prompt + user role prompt without user's prompt) consumes ~70 tokens. The value you specify won't include these tokens.
- You will also be asked about the action that will be performed every time when you accept a generated command when running in interactive mode.  
  The available actions are:

1. Running the generated command
2. Copying it to the clipboard

Don't worry though, after this you will be asked to apply your selected action on every generation.

## Options

Once installed, you can run CommanDeft using the `commandeft` command. Here are the available options:

- `-h, --help`: Show the help message and exit.
- `-v, --version`: Show the version information and exit.
- `-c, --configure`: Configure CommanDeft (Like the one on the first run).
- `-i, --interactive`: Run CommanDeft in interactive mode.
- `-p, --prompt "TEXT"`: Specify your prompt inline.

## Contributing

Contributions to CommanDeft are welcome! If you encounter any issues, have suggestions for improvements, or would like to contribute code, please check out the project repository on GitHub: [Repo](https://https://github.com/Ferrum-Citadel/commandeft)

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Ferrum-Citadel/commandeft/blob/main/LICENSE) file for more details.

## Feedback

If you find CommanDeft useful or have any feedback, I would love to hear from you! Please feel free to reach out and let me know how I can make this tool even better.
