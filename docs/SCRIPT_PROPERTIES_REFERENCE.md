# Google App Script Properties Reference

## Required Script Properties

You need to set these properties in your Google App Script project for the checkout system to work.

### How to Set Script Properties

1. Open your Google App Script project
2. Click the **gear icon** (⚙️) in the left sidebar (Project Settings)
3. Scroll down to **"Script properties"**
4. Click **"Add script property"** for each property below
5. Enter the **Property** name and **Value**
6. Click **Save script properties**

---

## Required Properties

### 1. Stripe Test Mode Keys (for Development)

**Property Name:** `STRIPE_TEST_SECRET_KEY`  
**Value:** Your Stripe test secret key  
**Format:** `sk_test_...`  
**Where to get it:**
1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Toggle to **"Test mode"** (top right)
3. Go to **Developers** → **API keys**
4. Copy the **Secret key** (starts with `sk_test_`)

**Example:** Replace `YOUR_SECRET_KEY_HERE` with your actual Stripe test secret key (starts with `sk_test_`)

---

**Property Name:** `STRIPE_TEST_WEBHOOK_SECRET`  
**Value:** Your Stripe test webhook signing secret  
**Format:** `whsec_...`  
**Required:** ❌ **Not Required** (only needed if using webhooks instead of polling)  
**Where to get it:**
1. In Stripe Dashboard (Test mode)
2. Go to **Developers** → **Webhooks**
3. Click on your webhook endpoint (or create one)
4. Copy the **Signing secret** (starts with `whsec_`)

**Example:** Replace `YOUR_WEBHOOK_SECRET_HERE` with your actual webhook signing secret (starts with `whsec_`)

**Note:** We use **polling** instead of webhooks (simpler, no setup needed). This property is only needed if you want to use webhooks instead. See `docs/POLLING_VS_WEBHOOKS.md` for details.

---

### 2. Stripe Live Mode Keys (for Production)

**Property Name:** `STRIPE_LIVE_SECRET_KEY`  
**Value:** Your Stripe live secret key  
**Format:** `sk_live_...`  
**Where to get it:**
1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Toggle to **"Live mode"** (top right)
3. Go to **Developers** → **API keys**
4. Copy the **Secret key** (starts with `sk_live_`)

**Example:** Replace `YOUR_SECRET_KEY_HERE` with your actual Stripe live secret key (starts with `sk_live_`)

---

**Property Name:** `STRIPE_LIVE_WEBHOOK_SECRET`  
**Value:** Your Stripe live webhook signing secret  
**Format:** `whsec_...`  
**Required:** ❌ **Not Required** (only needed if using webhooks instead of polling)  
**Where to get it:**
1. In Stripe Dashboard (Live mode)
2. Go to **Developers** → **Webhooks**
3. Click on your webhook endpoint (or create one)
4. Copy the **Signing secret** (starts with `whsec_`)

**Example:** Replace `YOUR_WEBHOOK_SECRET_HERE` with your actual webhook signing secret (starts with `whsec_`)

**Note:** We use **polling** instead of webhooks (simpler, no setup needed). This property is only needed if you want to use webhooks instead. See `docs/POLLING_VS_WEBHOOKS.md` for details.

---

### 3. Google Sheet Configuration

**Property Name:** `GOOGLE_SHEET_ID`  
**Value:** Your Google Sheet ID  
**Format:** Long alphanumeric string  
**Where to get it:**
1. Open your Google Sheet
2. Look at the URL: `https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit`
3. Copy the `[SHEET_ID]` part (between `/d/` and `/edit`)

**Example:** `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`

---

**Property Name:** `GOOGLE_SHEET_NAME`  
**Value:** Name of the sheet tab to use  
**Format:** String (exact match, case-sensitive)  
**Default:** `Stripe Social Media Checkout ID` (if not set)  
**Where to get it:**
1. Open your Google Sheet
2. Look at the tab name at the bottom
3. Copy the exact name

**Example:** `Stripe Social Media Checkout ID`

**Note:** This should match the existing sheet tab name. The script will write to this tab using the existing column structure.

---

### 4. EasyPost Shipping Configuration (Optional - for Real Shipping Rates)

**Property Name:** `EASYPOST_API_KEY`  
**Value:** Your EasyPost API key  
**Format:** `EZTK...` (test) or `EZAK...` (live)  
**Required:** ❌ **Optional** (if not set, falls back to fixed shipping rates)  
**Where to get it:**
1. Go to [EasyPost Dashboard](https://www.easypost.com/dashboard)
2. Go to **Settings** → **API Keys**
3. Copy your API key (use test key for development, live key for production)

**Example:** `EZTK_YOUR_EASYPOST_API_KEY_HERE` (replace with your actual EasyPost API key)

**Note:** If EasyPost API key is configured, the script will calculate real USPS shipping rates based on package weight and addresses. Otherwise, it falls back to fixed rates based on order total.

---

### 5. Origin Address (Required if using EasyPost)

**Property Name:** `ORIGIN_ADDRESS_LINE1`  
**Value:** Your warehouse/store street address  
**Example:** `123 Main Street`

---

**Property Name:** `ORIGIN_ADDRESS_CITY`  
**Value:** Your warehouse/store city  
**Example:** `San Francisco`

---

**Property Name:** `ORIGIN_ADDRESS_STATE`  
**Value:** Your warehouse/store state (2-letter code)  
**Example:** `CA`

---

**Property Name:** `ORIGIN_ADDRESS_POSTAL_CODE`  
**Value:** Your warehouse/store ZIP code  
**Example:** `94102`

---

**Property Name:** `ORIGIN_ADDRESS_COUNTRY`  
**Value:** Your warehouse/store country (2-letter code)  
**Default:** `US` (if not set)  
**Example:** `US`

---

### 6. Package Weight Configuration (Optional)

**Property Name:** `BASE_BOX_WEIGHT_OZ`  
**Value:** Base box weight in ounces (fixed, regardless of items)  
**Default:** `11.5` (if not set)  
**Example:** `11.5`

**Note:** This is the weight of the shipping box itself, padding, etc.

---

**Property Name:** `PER_ITEM_PACKAGING_OZ`  
**Value:** Per-item packaging weight in ounces (bubble wrap, padding per item)  
**Default:** `0.65` (if not set)  
**Example:** `0.65`

**Note:** This is additional packaging weight per item (bubble wrap, padding, etc.)

---

## Complete List (Quick Reference)

| Property Name | Required For | Required? | Format | Example |
|--------------|--------------|-----------|--------|---------|
| `STRIPE_TEST_SECRET_KEY` | Development | ✅ Yes | `sk_test_...` | `YOUR_KEY_HERE` |
| `STRIPE_TEST_WEBHOOK_SECRET` | Development | ❌ No | `whsec_...` | `YOUR_SECRET_HERE` |
| `STRIPE_LIVE_SECRET_KEY` | Production | ✅ Yes | `sk_live_...` | `YOUR_KEY_HERE` |
| `STRIPE_LIVE_WEBHOOK_SECRET` | Production | ❌ No | `whsec_...` | `YOUR_SECRET_HERE` |
| `GOOGLE_SHEET_ID` | Both | ✅ Yes | Alphanumeric | `1GE7PUq-UT6x...` |
| `GOOGLE_SHEET_NAME` | Both | ⚠️ Optional | String | `Stripe Social Media Checkout ID` |
| `EASYPOST_API_KEY` | Real Shipping Rates | ❌ No | `EZTK...` or `EZAK...` | `YOUR_KEY_HERE` |
| `ORIGIN_ADDRESS_LINE1` | EasyPost | ⚠️ If using EasyPost | String | `123 Main Street` |
| `ORIGIN_ADDRESS_CITY` | EasyPost | ⚠️ If using EasyPost | String | `San Francisco` |
| `ORIGIN_ADDRESS_STATE` | EasyPost | ⚠️ If using EasyPost | String (2-letter) | `CA` |
| `ORIGIN_ADDRESS_POSTAL_CODE` | EasyPost | ⚠️ If using EasyPost | String | `94102` |
| `ORIGIN_ADDRESS_COUNTRY` | EasyPost | ⚠️ If using EasyPost | String (2-letter) | `US` |
| `BASE_BOX_WEIGHT_OZ` | Package Weight | ❌ No | Number | `11.5` |
| `PER_ITEM_PACKAGING_OZ` | Package Weight | ❌ No | Number | `0.65` |

---

## Setup Checklist

**Required:**
- [ ] `STRIPE_TEST_SECRET_KEY` - Test mode secret key from Stripe
- [ ] `STRIPE_LIVE_SECRET_KEY` - Live mode secret key from Stripe
- [ ] `GOOGLE_SHEET_ID` - Your Google Sheet ID

**Optional:**
- [ ] `GOOGLE_SHEET_NAME` - Sheet tab name (defaults to "Stripe Social Media Checkout ID" if not set)
- [ ] `STRIPE_TEST_WEBHOOK_SECRET` - Only if using webhooks (we use polling instead)
- [ ] `STRIPE_LIVE_WEBHOOK_SECRET` - Only if using webhooks (we use polling instead)
- [ ] `EASYPOST_API_KEY` - For real USPS shipping rate calculation (falls back to fixed rates if not set)
- [ ] `ORIGIN_ADDRESS_*` - Warehouse/store address (required if using EasyPost)
- [ ] `BASE_BOX_WEIGHT_OZ` - Base box weight (default: 11.5 oz)
- [ ] `PER_ITEM_PACKAGING_OZ` - Per-item packaging weight (default: 0.65 oz)

---

## How It Works

The script automatically selects the correct keys based on the environment:

- **Development** (`localhost`, `127.0.0.1`): Uses `STRIPE_TEST_*` keys
- **Production** (`www.agroverse.shop`): Uses `STRIPE_LIVE_*` keys

This means you only need **one deployment** that works for both environments!

---

## Troubleshooting

### "Stripe development secret key not configured"
- Make sure you set `STRIPE_TEST_SECRET_KEY` (not `STRIPE_SECRET_KEY`)

### "Stripe production secret key not configured"
- Make sure you set `STRIPE_LIVE_SECRET_KEY` (not `STRIPE_SECRET_KEY`)

### "Google Sheet ID not configured"
- Make sure you set `GOOGLE_SHEET_ID` with the correct Sheet ID

### Wrong keys being used?
- Check that the property names match exactly (case-sensitive)
- Verify you're using the correct keys for test vs live mode

---

## Security Notes

⚠️ **Important:**
- Never commit these keys to version control
- Script Properties are encrypted by Google
- Only people with edit access to the script can see these properties
- Rotate keys if they're ever exposed

---

## Next Steps

After setting all properties:
1. Deploy the script as a Web App
2. Copy the Web App URL
3. Update `js/config.js` with the URL
4. Test with a test card: `4242 4242 4242 4242`

See `docs/SINGLE_DEPLOYMENT_SETUP.md` for complete setup instructions.

