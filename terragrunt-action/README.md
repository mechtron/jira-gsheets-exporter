# Hello world docker action

This action prints "Hello World" or "Hello" + the name of a person to greet to the log.

## Inputs

### `who-to-greet`

**Required** The name of the person to greet. Default `"World"`.

## Outputs

### `source_code_hash`

The Lambda-generated hash of the function's source code

## Example usage

uses: actions/hello-world-docker-action@0.1.0
with:
  who-to-greet: 'Mona the Octocat'
