from flask import jsonify, request, send_file
from models.dashboard import Dashboard
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend, required for Flask
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from calendar import month_abbr
import io
from sklearn.linear_model import LinearRegression
import numpy as np

# ── helpers ────────────────────────────────────────────────────────────────

def _fig_to_response(fig):
    """Serialize a matplotlib figure to a PNG and return it as a Flask response."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=130)
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype="image/png")

def _get(key):
    """Pull a field from form data or JSON, whichever was sent."""
    if request.content_type and 'application/json' in request.content_type:
        return request.get_json(silent=True, force=True).get(key) if request.get_json(silent=True) else None
    return request.form.get(key)
# ── JSON endpoints ──────────────────────────────────────────────────────────

def get_department_workload():
    try:
        rows = Dashboard.get_department_workload()
        data = [
            {
                "dept_name":          r[0],
                "total_encounters":   r[1],
                "active_encounters":  r[2],
                "avg_length_of_stay": float(r[3]) if r[3] else 0.0
            }
            for r in rows
        ]
        return jsonify({ "data": data, "error": None }), 200
    except Exception as e:
        return jsonify({ "data": None, "error": { "message": str(e) } }), 500


def get_top_diagnoses():
    try:
        rows = Dashboard.get_top_diagnoses()
        data = [
            {
                "icd10_code":             r[0],
                "diagnosis_description":  r[1],
                "frequency":              r[2]
            }
            for r in rows
        ]
        return jsonify({ "data": data, "error": None }), 200
    except Exception as e:
        return jsonify({ "data": None, "error": { "message": str(e) } }), 500


def get_seasonal_patterns():
    try:
        rows = Dashboard.get_seasonal_patterns()
        # Group by month so frontend can chart easily
        from collections import defaultdict
        grouped = defaultdict(list)
        for yr, mo, wk, icd, desc, count in rows:
            grouped[f"{yr}-{str(mo).zfill(2)}"].append({
                "icd10_code":   icd,
                "description":  desc,
                "case_count":   count
            })
        data = [{ "period": k, "diagnoses": v } for k, v in sorted(grouped.items())]
        return jsonify({ "data": data, "error": None }), 200
    except Exception as e:
        return jsonify({ "data": None, "error": { "message": str(e) } }), 500

# ── chart endpoints (return PNG) ────────────────────────────────────────────

def chart_department_workload():
    try:
        rows = Dashboard.get_department_workload()
        df = pd.DataFrame(rows, columns=["dept_name", "total_encounters", "active_encounters", "avg_los"])

        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.barh(df["dept_name"], df["total_encounters"], color="#3a7ebf", label="Total")
        ax.barh(df["dept_name"], df["active_encounters"],  color="#e07b3a", label="Active")
        ax.set_xlabel("Encounters")
        ax.set_title("Department Workload")
        ax.legend()
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        fig.tight_layout()
        return _fig_to_response(fig)
    except Exception as e:
        return jsonify({ "data": None, "error": { "message": str(e) } }), 500


def chart_top_diagnoses():
    try:
        rows = Dashboard.get_top_diagnoses()
        if not rows:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.text(0.5, 0.5, "No diagnosis data available", ha="center", va="center", fontsize=14, color="gray")
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            fig.tight_layout()
            return _fig_to_response(fig)
        
        df = pd.DataFrame(rows, columns=["icd10_code", "description", "frequency"])

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(df["icd10_code"], df["frequency"], color="#5ba85a")
        ax.set_xlabel("Cases")
        ax.set_title("Top 10 Diagnoses")
        # annotate each bar with the description
        for i, (_, row) in enumerate(df.iterrows()):
            desc = row["description"] if row["description"] else row["icd10_code"]
            desc_text = str(desc)[:35]
            ax.text(0.5, i, desc_text, va="center", fontsize=7, color="white")
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        fig.tight_layout()
        return _fig_to_response(fig)
    except Exception as e:
        return jsonify({ "data": None, "error": { "message": str(e) } }), 500


def chart_monthly_volume():
    try:
        rows = Dashboard.get_monthly_encounter_volume()
        df = pd.DataFrame(rows, columns=["yr", "mo", "wk", "total"])
        df["label"] = df.apply(lambda r: f"{month_abbr[int(r.mo)]} {int(r.yr)}", axis=1)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df["label"], df["total"], marker="o", linewidth=2, color="#3a7ebf")
        ax.fill_between(range(len(df)), df["total"], alpha=0.15, color="#3a7ebf")
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels(df["label"], rotation=45, ha="right", fontsize=8)
        ax.set_ylabel("Encounters")
        ax.set_title("Monthly Encounter Volume")
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        fig.tight_layout()
        return _fig_to_response(fig)
    except Exception as e:
        return jsonify({ "data": None, "error": { "message": str(e) } }), 500
    

def forecast_department_demand():
    """
    JSON endpoint — returns historical counts + 3-month forecast per department.
    """
    try:
        rows = Dashboard.get_encounter_history_by_dept()
        if not rows:
            return jsonify({ "data": None, "error": { "message": "No encounter history found" } }), 404

        df = pd.DataFrame(rows, columns=["dept_name", "yr", "mo", "wk", "total"])

        # Convert yr+mo into a single integer time index per department
        df["time_index"] = (df["yr"] - df["yr"].min()) * 12 + df["mo"]

        MONTHS_AHEAD = 3
        result = {}

        for dept, group in df.groupby("dept_name"):
            group = group.sort_values("time_index").reset_index(drop=True)
            X = group["time_index"].values.reshape(-1, 1)
            y = group["total"].values

            model = LinearRegression()
            model.fit(X, y)

            # Build historical series
            history = [
                {
                    "period": f"{int(r.yr)}-{str(int(r.mo)).zfill(2)}",
                    "actual": int(r.total)
                }
                for _, r in group.iterrows()
            ]

            # Project forward
            last_index = int(group["time_index"].max())
            last_yr    = int(group["yr"].max())
            last_mo    = int(group["mo"].max())
            forecast   = []

            for i in range(1, MONTHS_AHEAD + 1):
                future_index = last_index + i
                predicted    = max(0, round(float(model.predict([[future_index]])[0])))
                mo = (last_mo - 1 + i) % 12 + 1
                yr = last_yr + ((last_mo - 1 + i) // 12)
                forecast.append({
                    "period":    f"{yr}-{str(mo).zfill(2)}",
                    "predicted": predicted
                })

            result[dept] = {
                "history":  history,
                "forecast": forecast,
                "trend":    "increasing" if model.coef_[0] > 0.5
                            else "decreasing" if model.coef_[0] < -0.5
                            else "stable"
            }

        return jsonify({ "data": result, "error": None }), 200

    except Exception as e:
        return jsonify({ "data": None, "error": { "message": str(e) } }), 500


def chart_forecast_demand():
    """
    PNG chart — one subplot per department showing history + forecast.
    """
    try:
        rows = Dashboard.get_encounter_history_by_dept()
        if not rows or len(rows) == 0:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.text(0.5, 0.5, "No encounter data available", ha="center", va="center", fontsize=14, color="gray")
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            fig.tight_layout()
            return _fig_to_response(fig)

        df = pd.DataFrame(rows, columns=["dept_name", "yr", "mo", "wk", "total"])
        df["time_index"] = (df["yr"] - df["yr"].min()) * 12 + df["mo"]

        MONTHS_AHEAD = 3
        depts = sorted(df["dept_name"].unique())

        # Dynamic grid — 2 columns, enough rows to fit all departments
        n_cols = 2
        n_rows = (len(depts) + 1) // n_cols
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(13, 4 * n_rows))
        axes = axes.flatten()

        for i, dept in enumerate(depts):
            ax    = axes[i]
            group = df[df["dept_name"] == dept].sort_values("time_index").reset_index(drop=True)
            X     = group["time_index"].values.reshape(-1, 1)
            y     = group["total"].values

            model = LinearRegression()
            model.fit(X, y)

            # Labels for historical x-axis
            hist_labels = [
                f"{month_abbr[int(r.mo)]} {str(int(r.yr))[2:]}"
                for _, r in group.iterrows()
            ]

            # Build forecast points
            last_index = int(group["time_index"].max())
            last_yr    = int(group["yr"].max())
            last_mo    = int(group["mo"].max())
            f_vals, f_labels = [], []

            for j in range(1, MONTHS_AHEAD + 1):
                fi  = last_index + j
                mo  = (last_mo - 1 + j) % 12 + 1
                yr  = last_yr + ((last_mo - 1 + j) // 12)
                f_vals.append(max(0, round(float(model.predict([[fi]])[0]))))
                f_labels.append(f"{month_abbr[mo]} {str(yr)[2:]}")

            # Trend line across full range (history + forecast)
            all_x      = np.array(list(X.flatten()) + [last_index + j for j in range(1, MONTHS_AHEAD + 1)])
            trend_y    = model.predict(all_x.reshape(-1, 1))
            all_labels = hist_labels + f_labels
            n_hist     = len(hist_labels)

            # Plot
            ax.plot(range(n_hist), y,       marker="o", color="#3a7ebf",
                    linewidth=2, label="Actual")
            ax.plot(range(n_hist, n_hist + MONTHS_AHEAD), f_vals,
                    marker="s", color="#e07b3a", linewidth=2,
                    linestyle="--", label="Forecast")
            ax.plot(range(len(all_labels)), trend_y,
                    color="gray", linewidth=1, linestyle=":", label="Trend")

            # Shaded forecast region
            ax.axvspan(n_hist - 0.5, n_hist + MONTHS_AHEAD - 0.5,
                       alpha=0.08, color="#e07b3a")

            # Annotate forecast values
            for j, val in enumerate(f_vals):
                ax.annotate(str(val),
                            xy=(n_hist + j, val),
                            xytext=(0, 6), textcoords="offset points",
                            ha="center", fontsize=8, color="#e07b3a")

            ax.set_title(dept, fontsize=10, fontweight="bold")
            ax.set_ylabel("Encounters", fontsize=8)
            ax.set_xticks(range(len(all_labels)))
            ax.set_xticklabels(all_labels, rotation=45, ha="right", fontsize=7)
            ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            ax.legend(fontsize=7)

        # Hide any unused subplots
        for j in range(len(depts), len(axes)):
            axes[j].set_visible(False)

        fig.suptitle("Department Demand Forecast", fontsize=13, fontweight="bold", y=1.01)
        fig.tight_layout()
        return _fig_to_response(fig)

    except Exception as e:
        return jsonify({ "data": None, "error": { "message": str(e) } }), 500