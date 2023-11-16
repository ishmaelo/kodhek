import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "apps": [
            "https://roadmap.streamlit.app",
            "https://extras.streamlit.app",
            "https://issues.streamlit.app",
            "https://30days.streamlit.app",
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "apps": st.column_config.LinkColumn(
            "Trending apps",
            help="The top trending Streamlit apps",
            validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
        )
    },
    hide_index=False,
)


import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('db/patient.db')

# Execute a SQL query
cursor = conn.cursor()
cursor.execute('SELECT patient_name,sex FROM biodata')

# Get the results of the query
#users = cursor.fetchall()

# Display the results in Streamlit
#st.dataframe(users)

df = pd.DataFrame(cursor.fetchall(),columns=['patient_name','sex'])

#You first sort df by Name
df = df.sort_values(by='patient_name')
df['patient_name'] = df.apply(
    lambda row: '<a href="{}">{}</a>'.format(row['patient_name'], row['sex']),
    axis=1)

# You can choose to drop the Website column
#df = df.drop('Website', axis=1)

st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

####################################################
st.data_editor(
    data_df,
    column_config={
        "apps": st.column_config.LinkColumn(
            "Trending apps",
            help="The top trending Streamlit apps",
            validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
        )
    },
    hide_index=True,
)

st.link_button("Go to gallery", "https://streamlit.io/gallery")


import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

data_df = pd.DataFrame(
    {
        "apps": [
            "roadmap",
            "extras",
            "issues",
            "30days",
        ],
        "urls": [
            "https://roadmap.streamlit.app",
            "https://extras.streamlit.app",
            "https://issues.streamlit.app",
            "https://30days.streamlit.app",
        ],
    }
)

data = {
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [25, 30, 35],
    'Website': ['https://www.example.com',
                'https://www.google.com',
                'https://www.openai.com']
}
df = pd.DataFrame(data)

#You first sort df by Name
df = df.sort_values(by='Name')
df['Name'] = df.apply(
    lambda row: '<a href="{}">{}</a>'.format(row['Website'], row['Name']),
    axis=1)

# You can choose to drop the Website column
#df = df.drop('Website', axis=1)

st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)


import streamlit as st
import numpy as np
import pandas as pd

df = pd.DataFrame(
    {
        "Animal": ["Lion", "Elephant", "Giraffe", "Monkey", "Zebra"],
        "Habitat": ["Savanna", "Forest", "Savanna", "Forest", "Savanna"],
        "Lifespan (years)": [15, 60, 25, 20, 25],
        "Average weight (kg)": [190, 5000, 800, 10, 350],
    }
)

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)


selection = dataframe_with_selections(df)
st.write("Your selection:")
st.write(selection)


import pandas as pd

df = pd.DataFrame({
    'name': ['stackoverflow', 'gis stackexchange', 'meta stackexchange'],
    'url': ['https://stackoverflow.com', 'https://gis.stackexchange.com/', 'https://meta.stackexchange.com']
})

def make_clickable(url, name):
    return  st.markdown('<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url, name),unsafe_allow_html=True)


df

def line_graph_options():
    import altair as alt
    from vega_datasets import data


    source = data.stocks()

    base = alt.Chart(source).encode(
        alt.Color("symbol").legend(None)
    ).transform_filter(
        "datum.symbol !== 'IBM'"
    ).properties(
        width=500
    )

    line = base.mark_line().encode(x="date", y="price")


    last_price = base.mark_circle().encode(
        alt.X("last_date['date']:T"),
        alt.Y("last_date['price']:Q")
    ).transform_aggregate(
        last_date="argmax(date)",
        groupby=["symbol"]
    )

    company_name = last_price.mark_text(align="left", dx=4).encode(text="symbol")

    chart = (line + last_price + company_name).encode(
        x=alt.X().title("date"),
        y=alt.Y().title("price")
    )

    chart
    
    
    import altair as alt
    chart = (
        alt.Chart(
            data=df,
            title="Your title",
        )
        .mark_line()
        .encode(
            x=alt.X("Reading date", axis=alt.Axis(title="BGM Reading date")),
            y=alt.Y("Score", axis=alt.Axis(title="MPC Score")),
        )
    )

    st.altair_chart(chart,use_container_width=True)

