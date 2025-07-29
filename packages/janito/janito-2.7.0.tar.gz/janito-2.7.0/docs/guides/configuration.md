# Configuration Guide

Janito can be configured using command-line options, environment variables, or configuration files. This guide shows you how to set up API keys, select providers and models, and adjust other settings.

## 1. Command-Line Options (Recommended for Most Users)

Set API keys, providers, and models directly when running Janito:

```bash
janito --set-api-key YOUR_API_KEY -p PROVIDER_NAME
janito --set provider=openai
janito -p openai -m gpt-3.5-turbo "Your prompt here"
```

- Use `-p PROVIDER_NAME` to select a provider.
- Use `-m MODEL_NAME` to select a model for the provider.
- See [CLI Options](../reference/cli-options.md) for the full list of flags.

## 3. Configuration File

Janito uses a `config.json` file located in the `.janito` directory under your home folder for persistent settings.

**Path:**

- Windows: `C:\Users\<YourUser>\.janito\config.json`
- Linux/macOS: `/home/<youruser>/.janito/config.json`

You can edit this file directly or use Janito CLI commands to update your configuration.

## Viewing Effective Configuration

Show the current configuration with:
```bash
janito --show-config
```

## More Information

- See [CLI Options Reference](../reference/cli-options.md) for all configuration flags.
- For provider-specific settings, see the [Supported Providers & Models](../supported-providers-models.md) page.
- For troubleshooting, use `janito --help` or consult the [Usage Guide](using.md).
