![](https://www.banana.dev/lib_zOkYpJoyYVcAamDf/x2p804nk9qvjb1vg.svg?w=340 "Banana.dev")

# Banana.dev bark starter template

This is a bark starter template from [Banana.dev](https://www.banana.dev) that allows on-demand serverless GPU inference.

You can fork this repository and deploy it on Banana as is, or customize it based on your own needs.


# Running this app

## Deploying on Banana.dev

1. [Fork this](https://github.com/bananaml/demo-bark/fork) repository to your own GitHub account.
2. Connect your GitHub account on Banana.
3. [Create a new model](https://app.banana.dev/deploy) on Banana from the forked GitHub repository.

## Running after deploying

1. Wait for the model to build after creating it.
2. Add your S3 bucket credentials in `app.py`.
3. Make an API request using one of the provided snippets in your Banana dashboard. However, instead of sending a prompt as provided in the snippet, fit the prompt to the needs of the bark model:

```python
inputs = {
    "prompt": "Let's try generating speech, with Bark, a text-to-speech model"
}
```

For more info, check out the [Banana.dev docs](https://docs.banana.dev/banana-docs/).