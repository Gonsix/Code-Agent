# Code-Agent 🚀
## Use `codex` command to automate software development workflows. ✨

Hi👋  I'm Shingo Morimoto, an University student in Japan. I'm so interested in creating LLM application using LangChain. 

The `codex` command,including subcommands: gen-commit, gen-readme, describe, suggest-comment, suggest-code, is a powerful tool to integrate your code with LLM power.✨
Currently, you can execute `codex gen-commit` to automate the creation of Git commit message from diff between HEAD commit and index.

## 🌟 Getting Started



### Install code-agent with pip 📁: 

To use the codex command anywhere install it with pip:

`pip install code-agent` or `pip install --break-system-packages code-agent ` if you are using newer pip. 

### Export OPENAI_API_KEY ⚙️:

You must exoport an `OPENAI_API_KEY` in your environment.
Also, you must have an access to the GPT-4 model to call OpenAI API.

###  **Usage** 🚀:

Amazing! Now you can use `codex` command anywhere!
```
$ codex --help

 Usage: codex [OPTIONS] COMMAND [ARGS]...

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                    │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                             │
│ --help                        Show this message and exit.                                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ describe            [Unimplemented feature]: Describe the source code in files -> codex describe --help                                                    │
│ gen-commit          Generate a commit message from Git diff between HEAD and index.                                                                        │
│ gen-readme          [Unimplemented feature]: Generate Awesome README for your project in interactive way -> codex gen_readme --help                        │
│ say-goodbye                                                                                                                                                │
│ say-hello                                                                                                                                                  │
│ suggest-code        [Unimplemented feature]: Refactor and Suggest code for source code in specified files -> codex suggest_code --help                     │
│ suggest-comment     [Unimplemented feature]: Suggest comment for source code in specified files -> codex suggest_comment --help                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Generation Result Example🤩:　
`codex gen-commit`
```
    🌟 Implement Rust cat command with line numbering features

    Changes(4):
     🚩 Added command-line parsing   @ src/lib.rs
         Integrated clap library for command-line argument parsing with custom Args struct, supporting file inputs and line numbering options.
     🚩 Implemented file reading functionality   @ src/lib.rs
         Developed file opening and reading capabilities, handling both standard input and file input streams.
     🚩 Implemented line numbering features   @ src/lib.rs
         Added functionality to number lines and number nonblank lines as per command-line arguments.
     🚩 Added main application logic   @ src/main.rs
         Created the main function to parse arguments and execute the application logic, with error handling and process exit on failure.
```
## Dive in! 🌊

With these steps, you're all set to revolutionize your Git commits. May your coding be effortless and your repositories vibrant! 💫
