import pandas as pd

def process_nationality_and_atp_code(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich the input DataFrame with country, flag, and picture URL based on nationality and atp_code.

    Parameters:
    ----------
    df : pd.DataFrame
        Input DataFrame containing columns 'nationality' and 'atp_code'.

    Returns:
    -------
    pd.DataFrame
        Enriched DataFrame with additional 'country', 'flag', and 'picture_url' columns.
    """
    nationality_to_country_flag = {
        "HUN": ("Hungary", "🇭🇺"),
        "ARG": ("Argentina", "🇦🇷"),
        "ESP": ("Spain", "🇪🇸"),
        "NED": ("Netherlands", "🇳🇱"),
        "ITA": ("Italy", "🇮🇹"),
        "RUS": ("Russia", "🇷🇺"),
        "CAN": ("Canada", "🇨🇦"),
        "GBR": ("United Kingdom", "🇬🇧"),
        "POL": ("Poland", "🇵🇱"),
        "AUS": ("Australia", "🇦🇺"),
        "GER": ("Germany", "🇩🇪"),
        "FRA": ("France", "🇫🇷"),
        "SVK": ("Slovakia", "🇸🇰"),
        "USA": ("United States", "🇺🇸"),
        "COL": ("Colombia", "🇨🇴"),
        "BRA": ("Brazil", "🇧🇷"),
        "JPN": ("Japan", "🇯🇵"),
        "MDA": ("Moldova", "🇲🇩"),
        "SUI": ("Switzerland", "🇨🇭"),
        "CZE": ("Czech Republic", "🇨🇿"),
        "AUT": ("Austria", "🇦🇹"),
        "IND": ("India", "🇮🇳"),
        "BIH": ("Bosnia and Herzegovina", "🇧🇦"),
        "CRO": ("Croatia", "🇭🇷"),
        "SRB": ("Serbia", "🇷🇸"),
        "SWE": ("Sweden", "🇸🇪"),
        "PER": ("Peru", "🇵🇪"),
        "LBN": ("Lebanon", "🇱🇧"),
        "JOR": ("Jordan", "🇯🇴"),
        "DOM": ("Dominican Republic", "🇩🇴"),
        None: ("Unknown", "🏳"),  # Handling None
        "CHI": ("Chile", "🇨🇱"),
        "MON": ("Monaco", "🇲🇨"),
        "KAZ": ("Kazakhstan", "🇰🇿"),
        "UKR": ("Ukraine", "🇺🇦"),
        "RSA": ("South Africa", "🇿🇦"),
        "MEX": ("Mexico", "🇲🇽"),
        "BLR": ("Belarus", "🇧🇾"),
        "TUN": ("Tunisia", "🇹🇳"),
        "POR": ("Portugal", "🇵🇹"),
        "MAR": ("Morocco", "🇲🇦"),
        "CHN": ("China", "🇨🇳"),
        "NZL": ("New Zealand", "🇳🇿"),
        "EST": ("Estonia", "🇪🇪"),
        "FIN": ("Finland", "🇫🇮"),
        "KOR": ("South Korea", "🇰🇷"),
        "TPE": ("Chinese Taipei", "🇹🇼"),
        "HKG": ("Hong Kong", "🇭🇰"),
        "BUL": ("Bulgaria", "🇧🇬"),
        "BOL": ("Bolivia", "🇧🇴"),
        "DEN": ("Denmark", "🇩🇰"),
        "NOR": ("Norway", "🇳🇴"),
        "GRE": ("Greece", "🇬🇷"),
        "BEL": ("Belgium", "🇧🇪"),
    }

    # Add country and flag columns
    df["country"] = df["nationality"].map(lambda x: nationality_to_country_flag.get(x, ("Unknown", "🏳"))[0])
    df["flag"] = df["nationality"].map(lambda x: nationality_to_country_flag.get(x, ("Unknown", "🏳"))[1])

    # Add picture_url column
    df["picture_url"] = df["atp_code"].map(
        lambda code: f"https://www.atptour.com/-/media/alias/player-gladiator-headshot/{code}" if code else None
    )

    return df
