import locale

country_paper_sizes = {
    # North America (mostly letter)
    'US': 'letter',
    'CA': 'letter',
    'MX': 'letter',

    # Central America & Caribbean (mostly letter)
    'AG': 'letter', 'BS': 'letter', 'BB': 'letter', 'BZ': 'letter',
    'CR': 'letter', 'CU': 'letter', 'DM': 'letter', 'DO': 'letter',
    'GD': 'letter', 'GT': 'letter', 'HT': 'letter', 'HN': 'letter',
    'JM': 'letter', 'KN': 'letter', 'LC': 'letter', 'NI': 'letter',
    'PA': 'letter', 'PR': 'letter', 'SV': 'letter', 'TT': 'letter',
    'VC': 'letter',

    # South America (mostly a4)
    'AR': 'a4', 'BO': 'a4', 'BR': 'a4', 'CL': 'a4', 'CO': 'a4', 'EC': 'a4',
    'GY': 'a4', 'PY': 'a4', 'PE': 'a4', 'SR': 'a4', 'UY': 'a4', 'VE': 'a4',

    # Europe (almost all a4)
    'AL': 'a4', 'AD': 'a4', 'AT': 'a4', 'BY': 'a4', 'BE': 'a4', 'BA': 'a4',
    'BG': 'a4', 'HR': 'a4', 'CY': 'a4', 'CZ': 'a4', 'DK': 'a4', 'EE': 'a4',
    'FI': 'a4', 'FR': 'a4', 'DE': 'a4', 'GR': 'a4', 'HU': 'a4', 'IS': 'a4',
    'IE': 'a4', 'IT': 'a4', 'LV': 'a4', 'LI': 'a4', 'LT': 'a4', 'LU': 'a4',
    'MT': 'a4', 'MD': 'a4', 'MC': 'a4', 'ME': 'a4', 'NL': 'a4', 'MK': 'a4',
    'NO': 'a4', 'PL': 'a4', 'PT': 'a4', 'RO': 'a4', 'RU': 'a4', 'SM': 'a4',
    'RS': 'a4', 'SK': 'a4', 'SI': 'a4', 'ES': 'a4', 'SE': 'a4', 'CH': 'a4',
    'UA': 'a4', 'GB': 'a4', 'VA': 'a4',

    # Asia (mostly a4, except Japan and Philippines)
    'AF': 'a4', 'AM': 'a4', 'AZ': 'a4', 'BH': 'a4', 'BD': 'a4', 'BT': 'a4',
    'BN': 'a4', 'KH': 'a4', 'CN': 'a4', 'GE': 'a4', 'IN': 'a4', 'ID': 'a4',
    'IR': 'a4', 'IQ': 'a4', 'IL': 'a4', 'JO': 'a4', 'KZ': 'a4', 'KW': 'a4',
    'KG': 'a4', 'LA': 'a4', 'LB': 'a4', 'MY': 'a4', 'MV': 'a4', 'MN': 'a4',
    'MM': 'a4', 'NP': 'a4', 'OM': 'a4', 'PK': 'a4', 'QA': 'a4', 'SA': 'a4',
    'SG': 'a4', 'KR': 'a4', 'LK': 'a4', 'SY': 'a4', 'TW': 'a4', 'TJ': 'a4',
    'TH': 'a4', 'TR': 'a4', 'TM': 'a4', 'AE': 'a4', 'UZ': 'a4', 'VN': 'a4',
    # Exceptions:
    'JP': 'JIS B5',  # Japan uses JIS B5 (close to a4 but slightly different)
    'PH': 'letter',  # Philippines often uses letter

    # Africa (mostly a4)
    'DZ': 'a4', 'AO': 'a4', 'BJ': 'a4', 'BW': 'a4', 'BF': 'a4', 'BI': 'a4',
    'CM': 'a4', 'CV': 'a4', 'CF': 'a4', 'TD': 'a4', 'KM': 'a4', 'CG': 'a4',
    'CD': 'a4', 'DJ': 'a4', 'EG': 'a4', 'GQ': 'a4', 'ER': 'a4', 'SZ': 'a4',
    'ET': 'a4', 'GA': 'a4', 'GM': 'a4', 'GH': 'a4', 'GN': 'a4', 'GW': 'a4',
    'KE': 'a4', 'LS': 'a4', 'LR': 'a4', 'LY': 'a4', 'MG': 'a4', 'MW': 'a4',
    'ML': 'a4', 'MR': 'a4', 'MU': 'a4', 'MA': 'a4', 'MZ': 'a4', 'NA': 'a4',
    'NE': 'a4', 'NG': 'a4', 'RW': 'a4', 'ST': 'a4', 'SN': 'a4', 'SC': 'a4',
    'SL': 'a4', 'SO': 'a4', 'ZA': 'a4', 'SS': 'a4', 'SD': 'a4', 'TZ': 'a4',
    'TG': 'a4', 'TN': 'a4', 'UG': 'a4', 'ZM': 'a4', 'ZW': 'a4',

    # Oceania
    'AU': 'a4',
    'NZ': 'a4',
    'FJ': 'a4',
    'PG': 'a4',
    'SB': 'a4',
    'VU': 'a4',
    'WS': 'a4',
    'TO': 'a4',
    'KI': 'a4',
    'NR': 'a4',
    'TV': 'a4',

    # Others or unknown default to a4
}

def get_paper_size():
    """
    Get the default paper size for the system locale.
    Falls back to 'a4' if locale or country code cannot be determined.
    """
    loc = locale.getdefaultlocale()[0]  # e.g. 'en_US' or 'fr_FR'

    if not loc or '_' not in loc:
        return 'a4'

    country_code = loc.split('_')[-1].upper()
    return country_paper_sizes.get(country_code, 'a4')
