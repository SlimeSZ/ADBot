import aiohttp

class DexTwo:
   def __init__(self):
       self.token_fdv = None
       self.m5_vol = None
       self.h1_vol = None
       self.h6_vol = None
       self.h24_vol = None
       self.token_5m_vol = None  
       self.token_1h_vol = None
       self.token_6h_vol = None
       self.token_24h_vol = None
       self.token_5m_buys = None
       self.token_5m_sells = None
       self.token_1h_buys = None
       self.token_1h_sells = None
       self.token_24h_buys = None
       self.token_24h_sells = None
       self.token_5m_price_change = None
       self.token_1h_price_change = None
       self.token_24h_price_change = None
       self.token_liquidity = None
       self.has_tg = False
       self.has_x = False
       self.x_link = None
       self.tg_link = None
       self.token_on_dex = False
       self.token_on_pump = False
       self.token_dex_url = None

   async def fetch_mc(self, session, ca):
       print(f"\n=== Fetching DexScreener Data for {ca[:8]}... ===")
       url = f"https://api.dexscreener.com/latest/dex/search?q={ca}"
       
       try:
           async with session.get(url) as response:
               if response.status != 200:
                   print(f"[ERROR] Dex Screener API Status: {response.status}")
                   return

               json_data = await response.json()
               if not json_data or 'pairs' not in json_data or not json_data['pairs']:
                   print(f"[INFO] No pairs found for {ca[:8]}... - Token might be on Pump")
                   self.token_on_pump = True
                   return

               self.token_on_dex = True
               print("[SUCCESS] Token found on DEX")

               for pair in json_data['pairs']:
                   # Market cap
                   self.token_fdv = float(pair.get('fdv', 0))
                   print(f"- Market Cap: ${self.token_fdv:,.2f}")

                   # Volume data
                   volume_data = pair.get('volume', {})
                   self.token_5m_vol = float(volume_data.get('m5', 0))
                   self.token_1h_vol = float(volume_data.get('h1', 0))
                   self.token_6h_vol = float(volume_data.get('h6', 0))
                   self.token_24h_vol = float(volume_data.get('h24', 0))
                   print(f"- 1h Volume: ${self.token_1h_vol:,.2f}")

                   # Transaction data
                   txns_data = pair.get('txns', {})
                   m5_txns = txns_data.get('m5', {})
                   self.token_5m_buys = int(m5_txns.get('buys', 0))
                   self.token_5m_sells = int(m5_txns.get('sells', 0))
                   h1_txns = txns_data.get('h1', {})
                   self.token_1h_buys = int(h1_txns.get('buys', 0))
                   self.token_1h_sells = int(h1_txns.get('sells', 0))
                   h24_txns = txns_data.get('h24', {})
                   self.token_24h_buys = int(h24_txns.get('buys', 0))
                   self.token_24h_sells = int(h24_txns.get('sells', 0))

                   # Price changes
                   price_data = pair.get('priceChange', {})
                   self.token_5m_price_change = price_data.get('m5', 0)
                   self.token_1h_price_change = price_data.get('h1', 0) 
                   self.token_24h_price_change = price_data.get('h24', 0)

                   # Liquidity
                   liquidity_data = pair.get('liquidity', {})
                   self.token_liquidity = float(liquidity_data.get('usd', 0))
                   print(f"- Liquidity: ${self.token_liquidity:,.2f}")

                   # Social links
                   info = pair.get('info', {})
                   socials = info.get('socials', [])
                   for social in socials:
                       if social['type'] == 'telegram':
                           self.has_tg = True
                           self.tg_link = social.get('url', 'No Telegram Link')
                       if social['type'] == 'twitter':
                           self.has_x = True
                           self.x_link = social.get('url', 'No Twitter Link')

                   self.token_dex_url = pair.get('url', '')
                   break

       except Exception as e:
           print(f"[ERROR] Error fetching data for {ca[:8]}: {str(e)}")