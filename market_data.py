import requests
from config import settings

GRAPHQL_URL = f"https://gateway.thegraph.com/api/{settings.UNISWAP_API_KEY}/subgraphs/id/GENunSHWLBXm59mBSgPzQ8metBEp9YDfdqwFr91Av1UM"

def get_market_data():

    query = """
{
  tokens(
    first: 30,
    orderBy: totalValueLockedUSD,
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
      first: 1,
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