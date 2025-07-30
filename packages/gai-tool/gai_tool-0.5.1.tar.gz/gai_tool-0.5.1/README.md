![codecov](https://codecov.io/gh/Danielratmiroff/gai/branch/master/graph/badge.svg)
[![PyPI version](https://badge.fury.io/py/gai-tool.svg)](https://badge.fury.io/py/gai-tool)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Gai is a CLI Automation Tool for Git 🚀

command-line application that automates git commit messages and merge requests using AI.

![Demo](resources/video_demo.gif)

## ✨ Features

- Generate commit messages based on code diffs.
- Create merge requests with AI-generated titles and descriptions.
- Works with both GitHub and GitLab.

## 📦 Installation

Install gai-tool via pip:

```bash
pip install gai-tool
```

## 🚀 Getting Started

1. **Set API Tokens as Environment Variables**:

   ```bash
   # Ensure you have your AI interface and GitHub/GitLab API tokens set:
   export HUGGINGFACE_API_TOKEN='your_hf_api_token'    # If you want to use Hugging Face's API
   export GITHUB_TOKEN='your_github_token'             # If using GitHub
   export GITLAB_TOKEN='your_gitlab_token'             # If using GitLab
   ```

Supported interfaces:

- Groq (GROQ_API_KEY)
- Hugging Face (HUGGINGFACE_API_TOKEN)
- Gemini (GEMINI_API_KEY or GOOGLE_API_KEY) -- Gemini takes precedence when both are set.
- Ollama (OLLAMA_API_KEY)

2. **Navigate to your git repository**:

   ```bash
   cd /path/to/your/git/repo
   ```

3. **Start Using gai-tool**:

   ```bash
   # Generate an AI-powered commit message:
   gai commit -a
   ```

## ⚙️ Configuration

Configuration file is located at `~/.config/gai/config.yaml`. Customize settings like the AI interface, temperature, and target branch.

You can also initialize a local configuration file in your project directory:

```bash
gai init
```

This will create a `.gai.yaml` file in your current directory with your current settings. Local configuration takes precedence over global configuration.

Example configuration:

```yaml
interface: huggingface
temperature: 0.7
target_branch: master
```

### Customizing AI Behavior

You can customize the AI's behavior by editing the `gai-rules.md` file, which is created when you run `gai init`. These rules are injected into the AI's system prompt, allowing you to guide its output for commit messages and merge requests.

For a detailed guide, see [Customizing AI Behavior with Rules](./docs/customizing-ai-rules.md).

## 📖 Usage

gai-tool provides two main commands: `commit` and `merge`.

### 📝 Commit Messages

Generate an commit message:

```bash
gai commit
```

Options:

- `-a`, `--all`: Stage all changes before committing.
- `-t`, `--temperature`: Override the temperature specified in the config.
- `-i`, `--interface`: Specify and override the AI client API to use (`groq` or `huggingface`).

**Example**:

```bash
# Simply
gai commit -a
# Or
gai commit -a -i huggingface
```

### 🔀 Merge Requests

Create a merge request:

```bash
gai merge
```

Options:

- `[remote]`: Specify the remote git repository (default is `origin`).
- `--push`, `-p`: Push changes to remote before creating a merge request.
- `--target-branch`, `-tb`: Specify the target branch for the merge request (default is `master`).
- `-t`, `--temperature`: Override the temperature specified in the config.
- `-i`, `--interface`: Specify and override the AI client API to use (`groq` or `huggingface`).

**Example**:

```bash
# Simply
gai merge -p
# Or
gai merge origin --push --target-branch develop -interface groq
```

## 🛠 Build Instructions

Build gai-tool from source:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Danielratmiroff/gai.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd gai
   ```

3. **Create a Virtual Environment (Optional but Recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

4. **Install Build Tools and Dependencies**:

   ```bash
   pip install build
   pip install -r requirements.txt
   ```

5. **Build the Package**:

   ```bash
   python -m build
   ```

   This will generate distribution files in the `dist/` directory.

6. **Install the Built Package**:

   ```bash
   pip install dist/gai_tool-<VERSION>-py3-none-any.whl
   ```

## 🤝 Contributing

Contributions are welcome!

## 📄 License

MIT License - [LICENSE](LICENSE).
