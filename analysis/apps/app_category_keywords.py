# filename: app_category_keywords.py
# Description: Static keyword definitions for Android application categorization

# ============================================================
# CORE OS AND PLATFORM IDENTIFIERS
# ============================================================

GOOGLE_PACKAGES = [
    "com.google"  # All Google-branded services and applications
]

ANDROID_PACKAGES = [
    "com.google.android",  # Google Android base layer
    "com.android",         # AOSP platform components
    "android"              # Legacy or generic Android identifiers
]

# ============================================================
# SOCIAL MEDIA AND GLOBAL APP SUITES
# ============================================================

FACEBOOK_PACKAGES = [
    "com.facebook",         # Facebook main app, Messenger, Lite, etc.
    "com.facebook.katana",  # Facebook main app
    "com.facebook.orca",    # Messenger
    "com.facebook.mlite",   # Facebook Lite
    "com.facebook.services",
    "com.facebook.system",
    "com.facebook.appmanager"
]

TIKTOK_PACKAGES = [
    "com.zhiliaoapp",         # TikTok main identifier
    "com.ss.android.ugc.trill",  # TikTok regional variant
    "com.ss.android.ugc.aweme",  # Douyin (Chinese version of TikTok)
    "com.bytedance"              # Parent company packages
]

# ============================================================
# DEVICE MANUFACTURERS (OEMs)
# ============================================================

MANUFACTURER_KEYWORDS = [
    "motorola", "samsung", "google", "lenovo", "huawei", "xiaomi",
    "oneplus", "oppo", "vivo", "lg", "htc", "sony", "realme",
    "nokia", "asus", "zte", "infinix", "tecno", "alcatel"
]

# ============================================================
# HARDWARE COMPONENT AND SOC VENDORS
# ============================================================

HARDWARE_VENDOR_KEYWORDS = [
    "qualcomm", "mediatek", "broadcom", "nvidia", "intel",
    "amd", "qti", "arm", "hisilicon"
]

# ============================================================
# MOBILE CARRIERS / TELECOM OPERATORS
# ============================================================

CARRIER_KEYWORDS = [
    "att", "verizon", "tmobile", "cricket", "tracfone",
    "uscellular", "spectrum", "metropcs", "vodafone", "telstra",
    "orange", "jio", "telekom", "boost", "xfinitymobile",
    "rogers", "bell", "telenor", "aura", "dish", "mobily"
]

# ============================================================
# PROMOTION / ADWARE / PRELOAD ENGINES
# ============================================================

PROMOTION_FRAMEWORK_KEYWORDS = [
    "aura",                      # Common preload vendor
    "ironsrc",                   # Promotion & monetization SDK
    "inmobi",                    # Mobile ad network
    "glance.lockscreen",         # Lock screen ad/promotions
    "handmark.expressweather",   # Promotional weather app
    "appland",                   # Third-party preload channel
    "fyber"                      # Ad monetization provider
]

# ============================================================
# COMPOSITE: GENERAL VENDOR TAGGING
# Used in: vendor classification layer
# ============================================================

VENDOR_KEYWORDS = (
    MANUFACTURER_KEYWORDS +
    HARDWARE_VENDOR_KEYWORDS +
    CARRIER_KEYWORDS +
    PROMOTION_FRAMEWORK_KEYWORDS
)
