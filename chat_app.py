import streamlit as st
import chains  # The updated chains.py with summarization
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ChatGPT-Style Text-to-SQL", layout="centered")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("ChatGPT-Style Text-to-SQL")

# Display the conversation history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("df") is not None and msg.get("chart_type"):
            st.write("### Data Visualization")
            chains.generate_chart(msg["df"], msg["chart_type"])

# Input for new query
user_query = st.chat_input("Ask a database question or say hi...")

if user_query:
    st.session_state["messages"].append({
        "role": "user",
        "content": user_query
    })

    db_name, sql_query = chains.get_sql_query_and_db(user_query)

    if db_name is None or not sql_query.lower().startswith("select"):
        response_text = sql_query  # This is the AI's normal chat reply
        df = None
        chart_type = None
        summary = ""
    else:
        df = chains.get_response_from_db(sql_query, db_name)
        response_text = (
            f"**Database Selected:** `{db_name}`\n\n"
            f"**Generated SQL Query:** `{sql_query}`\n\n"
        )
        chart_type = None
        if df is not None and not df.empty:
            results_markdown = df.to_markdown(index=False)
            response_text += "### Query Results:\n" + results_markdown
            user_chart = chains.chart_type_from_question(user_query)
            auto_chart = chains.determine_chart_type(df)
            chart_type = user_chart if user_chart else auto_chart
            if chart_type:
                response_text += f"\n\n**Suggested Chart Type:** {chart_type}"
            else:
                response_text += "\n\nNo suitable chart type found."
            # Now, summarize the findings using the query results in markdown
            summary = chains.summarize_findings(results_markdown)
            response_text += f"\n\n**Summary of Findings:**\n{summary}"
        else:
            response_text += "No data returned from the query."
            summary = ""
    st.session_state["messages"].append({
        "role": "assistant",
        "content": response_text,
        "df": df,
        "chart_type": chart_type
    })
    # Optional: Force a re-run if desired (uncomment if supported)
    st.experimental_rerun()
