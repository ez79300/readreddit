# Reddit Web Z

This project is a simple web application that allows users to input a Reddit post URL, modifies the URL by adding a 'z' to the domain, and retrieves the post's title, self-text, and comments using the PRAW library.

## Project Structure

```
reddit-web-z
├── src
│   ├── app.py          # Main application file
│   ├── templates
│   │   └── index.html  # HTML template for the web page
│   └── static
│       └── style.css   # CSS styles for the web application
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Requirements

To run this project, you need to have Python installed along with the following packages:

- Flask
- PRAW

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Running the Application

1. Navigate to the project directory:

   ```
   cd reddit-web-z
   ```

2. Run the application:

   ```
   python src/app.py
   ```

3. Open your web browser and go to `http://127.0.0.1:5000` to access the application.

## Usage

- Enter a Reddit post URL in the input field.
- Click the submit button to fetch the post and comments.
- The modified URL will be used to retrieve the data, and the results will be displayed on the page.