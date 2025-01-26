import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

st.logo("assets/analyzius_logo.png", size="large")

st.title("Gabriel's Dashboard")
st.write("This is my personal dashboard")

@st.cache_data
def load_data(data_path):
    df = pd.read_csv(data_path)
    
    return df


@st.cache_data
def extract_valua_metric(data_path):
    data = dict()

    years = data_path["Year"].unique().tolist()
    symbols = data_path["Symbol"].unique()

    for s in symbols:
        data[s] = dict()

        emiten = data_path[data_path["Symbol"] == s]

        revenue = pd.Series([int(_.replace(".", "")) for _ in emiten["Revenue"] if "." in _])
        np = pd.Series([int(_.replace(".", "")) for _ in emiten["Net Profit"] if "." in _])

        pb = []
        for _ in emiten["Price Book"]:
            if "." in _:
                pb.append(float(_.replace(".", "").replace(",", ".")))
            else:
                pb.append(float(_.replace(",", ".")))
        pb = pd.Series(pb)
        
        pr = []
        for _ in emiten["Price"]:
            if "." in _:
                pr.append(float(_.replace(".", "").replace(",", ".")))
            else:
                pr.append(float(_.replace(",", ".")))
        pr = pd.Series(pr)

        gpm = pd.Series([float(_.replace(",", ".")) for _ in emiten["GPM"] if "," in _])
        npm = pd.Series([float(_.replace(",", ".")) for _ in emiten["NPM"] if "," in _])
        roe = pd.Series([float(_.replace(",", ".")) for _ in emiten["ROE"] if "," in _])

        data[s]["Revenue"] = revenue
        data[s]["Net Profit"] = np
        data[s]["Price Book"] = pb
        data[s]["Price"] = pr
        data[s]["GPM"] = gpm
        data[s]["NPM"] = npm
        data[s]["ROE"] = roe

    return data


@st.cache_data
def get_statistic(val_met):
    symbols = [s for s in val_met]

    stats = dict()
    stats["Revenue"] = pd.DataFrame([val_met[s]["Revenue"].values for s in symbols], index=symbols, columns=years).T 
    stats["Net Profit"] = pd.DataFrame([val_met[s]["Net Profit"].values for s in symbols], index=symbols, columns=years).T
    stats["Price"] = pd.DataFrame([val_met[s]["Price"].values for s in symbols], index=symbols, columns=years).T
    stats["Price Book"] = pd.DataFrame([val_met[s]["Price Book"].values for s in symbols], index=symbols, columns=years).T
    stats["GPM"] = pd.DataFrame([val_met[s]["GPM"].values for s in symbols], index=symbols, columns=years).T
    stats["NPM"] = pd.DataFrame([val_met[s]["NPM"].values for s in symbols], index=symbols, columns=years).T
    stats["ROE"] = pd.DataFrame([val_met[s]["ROE"].values for s in symbols], index=symbols, columns=years).T
    
    return stats["Revenue"], stats["Net Profit"], stats["Price"], stats["Price Book"], stats["GPM"], stats["NPM"], stats["ROE"]


# Load Dataset
df = load_data("./data/properties_annualreport.csv")
years = df["Year"].unique().tolist()
symbols = df["Symbol"].unique().tolist()

# Extract Metrics
properties = extract_valua_metric(df)
rev_stats, np_stats, pr_stats, pb_stats, gpm_stats, npm_stats, roe_stats = get_statistic(properties)

st.bar_chart(rev_stats, x_label = "Years" , y_label = "Revenue", stack=False, height=600)
st.bar_chart(np_stats, x_label = "Years" , y_label = "RevNet Proft", stack=False, height=800)
st.line_chart(pr_stats, x_label = "Years" , y_label = "Price")
st.line_chart(pb_stats, x_label = "Years" , y_label = "Price Book")
st.line_chart(gpm_stats, x_label = "Years" , y_label = "GPM")
st.line_chart(npm_stats, x_label = "Years" , y_label = "NPM")
st.line_chart(roe_stats, x_label = "Years" , y_label = "ROE")

# Display Main Table and Graph
a, b = st.columns(2)

a.dataframe(df)
b.line_chart(pr_stats, x_label="Year", y_label="Price Book")

# # Display GPM Metrics
st.header("GPM Metrics")

cols = st.columns(4, border=True)
for i, col in enumerate(cols):
    col.metric(symbols[i], round(properties[symbols[i]]["GPM"].iloc[:-1].mean(), 2), delta = round(properties[symbols[i]]["GPM"].iloc[-1] - properties[symbols[i]]["GPM"].iloc[:-1].mean(), 2), help="GPM emiten" + symbols[i])

# Display NPM Metrics
st.header("NPM Metrics")

cols = st.columns(4, border=True)
for i, col in enumerate(cols):
    col.metric(symbols[i], round(properties[symbols[i]]["NPM"].iloc[:-1].mean(), 2), delta = round(properties[symbols[i]]["NPM"].iloc[-1] - properties[symbols[i]]["NPM"].iloc[:-1].mean(), 2), help="NPM emiten" + symbols[i])

# Display ROE Metrics
st.header("ROE Metrics")

cols = st.columns(4, border=True)
for i, col in enumerate(cols):
    col.metric(symbols[i], round(properties[symbols[i]]["ROE"].iloc[:-1].mean(), 2), delta = round(properties[symbols[i]]["ROE"].iloc[-1] - properties[symbols[i]]["ROE"].iloc[:-1].mean(), 2), help="ROE emiten" + symbols[i])