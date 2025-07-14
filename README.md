# 🚦 NYC Collision Dashboard

An interactive web dashboard for visualizing traffic collisions in New York City using Streamlit.

## 🔍 Project Overview

This app provides:
- 📊 Real-time KPIs for injuries and fatalities
- 🕒 Collision distribution by hour
- 🚸 Breakdown by affected group (pedestrians, cyclists, motorists)
- 🗺️ Borough-based filtering
- 🚗 Vehicle-type and contributing factor analysis (Pro version)

Built with `Streamlit`, `Pandas`, `Seaborn`, and `Matplotlib`.

---

## 📁 Project Structure

```
nyc-collision-dashboard/
│
├── data/
│   └── collisions.csv
├── notebooks/
│   └── 01_EDA.ipynb
├── app.py               <- Base app with basic UI
├── app_ui_pro.py        <- Advanced UI version
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/kooroosh1363/nyc-collision-dashboard.git
   cd nyc-collision-dashboard
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

Or for the advanced UI:
```bash
streamlit run app_ui_pro.py
```

---

## ☁️ Deploy to Streamlit Cloud

1. Push this project to a **public GitHub repo**
2. Visit: [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click `Create App` and select your repo
4. Set `app.py` or `app_ui_pro.py` as the main file
5. Done! 🚀

---

## 🛠 Built With

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)

---

## 📬 Contact

Made with ❤️ by [@kooroosh1363](https://github.com/kooroosh1363)  
Feel free to contribute or raise issues!
