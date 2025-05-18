import streamlit as st
import pandas as pd
from distributed_shift_simulation import run_distributed_simulation

st.set_page_config(page_title="統合ポーカー統計UI", layout="wide")
st.title("ポーカー統計ツール - 分担＆結果確認 一体型UI")

# --- 入力エリア ---
st.header("① 分担計算設定")

st.markdown("#### ハンドグループを選択")
groups = [
    "High Pair", "Mid Pair", "Low Pair",
    "Broadway", "Suited Connectors", "Offsuit Connectors",
    "Suited Gappers", "Offsuit Gappers",
    "Suited Non-Connectors", "Offsuit Non-Connectors",
    "Ace-X Suited", "Junk Hands"
]
selected_groups = st.multiselect("対象グループ", groups)

st.markdown("#### モンテカルロ試行回数を選択")
trials = st.selectbox("試行回数", [1000, 10000, 50000, 100000], index=1)

st.markdown("#### 相手レンジを選択")
range_option = st.radio("レンジ選択", ["すべて", "25%", "30%"])

range_25 = [
    "AA","KK","QQ","JJ","TT","99","88","77",
    "AKs","AQs","AJs","ATs","KQs","KJs","QJs","JTs",
    "AKo","AQo","AJo","KQo"
]
range_30 = range_25 + ["66", "A9s", "KTs", "QTs", "J9s", "T9s", "98s", "KJo", "QJo"]

if range_option == "25%":
    selected_range = range_25
elif range_option == "30%":
    selected_range = range_30
else:
    selected_range = None

st.markdown("#### 結果ファイル名を入力（例：results_hp_bw.csv）")
output_name = st.text_input("ファイル名", value="results_group.csv")

if st.button("分担計算スタート"):
    if not selected_groups:
        st.warning("最低1つのグループを選んでください。")
    else:
        with st.spinner("計算中...（数分〜十数分かかる場合があります）"):
            run_distributed_simulation(
                target_groups=selected_groups,
                flop_file="flop30.csv",
                output=output_name,
                trials=trials,
                range_list=selected_range
            )
        st.success(f"計算完了！保存ファイル：{output_name}")

# --- 出力エリア ---
st.header("② 結果確認・表示")

uploaded_file = st.file_uploader("計算済みのCSVをアップロード（results.csvなど）", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.markdown("#### 並べ替え対象")
    sort_column = st.selectbox("並べ替え列", ["ShiftFlop", "ShiftTurn", "ShiftRiver"])
    sort_order = st.radio("並べ替え順", ["降順", "昇順"])
    ascending = (sort_order == "昇順")

    st.markdown("#### 表示対象グループ（任意）")
    group_options = df["Group"].unique().tolist()
    selected_display_groups = st.multiselect("表示グループ", group_options, default=group_options)

    filtered_df = df[df["Group"].isin(selected_display_groups)].sort_values(by=sort_column, ascending=ascending)

    st.markdown("#### 勝率変動一覧（最大500行まで）")
    st.dataframe(filtered_df.head(500), use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("この結果をCSVでダウンロード", data=csv, file_name="filtered_results.csv", mime="text/csv")
else:
    st.info("上のエリアで計算するか、ここにCSVファイルをアップロードしてください。")
