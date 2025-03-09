# Marketing Analyst Query Bot

## Overview

**Marketing Analyst Query Bot** is an innovative, ChatGPT-style application designed to empower marketing teams by transforming natural language queries into SQL commands. This tool makes data-driven decision-making accessible and instantaneous—no more waiting for specialized teams to generate reports!

## Key Features

- **Natural Language to SQL Conversion:**  
  Convert plain language questions into SQL queries using OpenAI’s API.
  
- **Real-Time Data Querying:**  
  Instantly execute generated SQL queries against your database and retrieve actionable insights.
  
- **Intuitive Visualizations:**  
  Automatically generate visualizations (bar charts, pie charts, histograms, etc.) based on the query results.
  
- **Summarization of Findings:**  
  Get a concise summary of your query results for quick insights.
  
- **Edge Case Handling:**  
  Includes logic for handling:
  - Mis-selected tables (e.g., ensuring "marks" queries target the student database)
  - Case-insensitive matching for columns (e.g., "laptop" vs. "Laptop")
  - Fallback for normal chat or greetings
  - Post-validation of generated SQL against your database schema

## Technology Stack

- **Frontend:**  
  - [Streamlit](https://streamlit.io/) for building an interactive, chat-like UI.
  
- **Backend & NLP:**  
  - [OpenAI API](https://openai.com/api/) (GPT-3.5 Turbo) for natural language processing and SQL generation.
  
- **Data Handling:**  
  - SQLite for a lightweight database solution.
  - [Pandas](https://pandas.pydata.org/) for data manipulation.
  
- **Visualization:**  
  - [Matplotlib](https://matplotlib.org/) for creating dynamic charts.
  
- **Environment & Configuration:**  
  - Python Dotenv for managing secret API keys securely.

## How It Works

1. **User Interaction:**  
   Users type queries in natural language (e.g., "Show me the laptop sales in North region") into the chat interface.

2. **SQL Generation:**  
   The application uses OpenAI's API to translate the query into a valid SQL command tailored to the underlying database schema.

3. **Query Execution:**  
   The generated SQL is executed against the appropriate database (e.g., student.db, employees.db, or sales.db), with built-in validation to ensure the correct data source is selected.

4. **Visualization & Summarization:**  
   Query results are displayed along with dynamic charts. A summary of the key findings is also generated to provide quick insights.

## Installation & Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Milkyy-way/AI_SQL_QUERY.git
   cd AI_SQL_QUERY
