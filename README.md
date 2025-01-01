# HarlanBOT

HarlanBOT is a Python module designed for creating AI-based chatbots. This module utilizes various natural language processing (NLP) and deep learning technologies to enable the bot to learn from registered conversation samples and provide relevant responses based on user input.

## Features

- **Easy Customization**: Easily add, modify, or remove intents and responses in the JSON file.
- **Train the ChatBot**: Train the chatbot using data from a JSON file containing intents and responses.
- **Real-time Interaction**: The chatbot can respond in real-time based on user input.

## Installation

Follow the steps below to install and set up HarlanBOT:

1. **Install the package**:

    ```bash
    pip install harlanbot
    ```

    This requires the modified `tflearn` package for compatibility with the AI:

    ```bash
    pip install git+https://github.com/harlansr/tflearn.git@master
    ```

2. **Create a Python script**:

    ```python
    from harlanbot import ChatBot
    bot = ChatBot()
    ```

    Run this code for the first time to create the `files/intents.json` file. You can also customize the file name as needed by passing a custom path.

    ```python
    from harlanbot import ChatBot
    bot = ChatBot(files="custom_file_name")
    ```

    This example will create a file named `custom_file_name/intents.json`.

3. **Edit the `intents.json` file**:

    `intents.json` is the file required to train the bot. To tailor the chatbot to your needs, edit the contents of the `intents.json` file.

## Usage

### Example `intents.json` File

```json
{
    "intents": {
        "main": [
            {
                "tag": "greeting",
                "patterns": [
                    "hello",
                    "who are you"
                ],
                "responses": [
                    "Hello, I'm your assistant",
                    "Hi, I'm your assistant"
                ]
            },
            {
                "tag": "goodbye",
                "patterns": [
                    "bye",
                    "I need to go"
                ],
                "responses": [
                    "Okay, have a nice day",
                    "See you again"
                ]
            }
        ]
    }
}
```

#### **Explanation:**

| Name      | Description                                                |
|-----------|------------------------------------------------------------|
| tag       | An identifier that should be unique across all intents.     |
| patterns  | Sample input texts; the more patterns, the better the model. |
| responses | Output responses when matching input patterns. Can be filled with multiple responses, which will be displayed randomly. |

### Training the ChatBot

After customizing the `intents.json` file, when you run:

```python
bot.train()
```

This will train the AI according to the data in `intents.json`. Alternatively, you can train the model everytime code running by modify the code like this:

```python
from harlanbot import ChatBot
bot = ChatBot(train=True)
```



## Documentation

### Functions

| Name         | Description                                                |
|--------------|------------------------------------------------------------|
| train()      | Manually train the chatbot with provided data             |
| load()       | Load the trained data model                               |
| ask()        | Ask a question to the AI and get an answer                  |
| run_loop()   | Run the chatbot in a loop to facilitate continuous Q&A    |

### Class **ChatBot( *train*, *accuracy*, *files*, *message_default* )**

| Name            | Type    | Default | Description                                |
|-----------------|---------|---------|--------------------------------------------|
| train           | boolean | False   | Run training when initiated                |
| accuracy        | float   | 0.8     | Accuracy of the response, recommended value is 0.9 |
| files           | string  | "files" | Directory name to store the data            |
| message_default | string  | "Sorry, I don't understand" | Message to display when the accuracy is below the defined threshold |


### Function **ask( *message*, *need_accuracy* )**

| Name         | Type    | Default | Description                                               |
|--------------|---------|---------|-----------------------------------------------------------|
| message      | string  |         | The message that you want to ask the bot                  |
| need_accuracy| boolean | False   | Whether to include the accuracy value with the response   |

### Function **run_loop( *need_accuracy* )**

| Name         | Type    | Default | Description                                               |
|--------------|---------|---------|-----------------------------------------------------------|
| need_accuracy| boolean | False   | Whether to include the accuracy value with the response   |

## Example Code

```python
from harlanbot import ChatBot

bot = ChatBot(True, 0.9)  # Set to False if you don't want the bot to train every time
answer = bot.ask("Hello, nice to meet you") 
print(answer)
```

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the GitHub [repository]('https://github.com/harlansr/harlanbot)
2. Create a new branch (`git checkout -b new-feature`)
3. Make the necessary changes
4. Commit the changes (`git commit -am 'Add new feature'`)
5. Push the branch (`git push origin new-feature`)
6. Create a Pull Request