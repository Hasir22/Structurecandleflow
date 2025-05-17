def analyze_data(df):
    index = df["INDEX%"].iloc[0]
    range_ = df["RANGE%"].iloc[0]

    if index > 80 and range_ > 60:
        return "Market kemungkinan berada di zona ekstrem, potensi reversal tinggi."
    elif index < 30 and range_ < 40:
        return "Market tenang, kemungkinan lanjut trend atau akumulasi."
    else:
        return "Struktur netral, tunggu konfirmasi arah selanjutnya."
