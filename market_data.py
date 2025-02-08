import requests
from config import settings

GRAPHQL_URL = f"https://gateway.thegraph.com/api/{settings.UNISWAP_API_KEY}/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV"

def get_market_data():

    query = """
{
  tokens(
    first: 30,
    where: { 
      totalValueLockedUSD_gt: 5000000
    },
    orderBy: volumeUSD,
    orderDirection: desc
  ) {
    name
    symbol
    totalValueLockedUSD
    volumeUSD
    txCount
    totalSupply
    feesUSD
    poolCount
    tokenDayData(
      first: 7,
      orderBy: date,
      orderDirection: desc
    ) {
      date
      volumeUSD
      totalValueLockedUSD
      priceUSD
      feesUSD
      open
      high
      low
      close
    }
  }
}
    """

    headers = {"Content-Type": "application/json"}
    response = requests.post(GRAPHQL_URL, json={"query": query}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data