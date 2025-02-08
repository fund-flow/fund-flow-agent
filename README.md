# Fund Flow Portfolio Reccomendation Agent

## Activate Virtual Env
python3 -m venv venv
source venv/bin/activate

## Install dependencies
pip install -r requirements.txt

## Create your .env file in root directory
Required keys are
- OPENAI_API_KEY
- UNISWAP_API_KEY

## Build Image
docker build -t fund-flow-agent .

## Run Image
docker run -d -p 8000:8000 --env-file .env --name fund-flow-agent fund-flow-agent

## Push to Dockerhub
docker tag fund-flow-agent:latest ongyimeng/fund-flow:latest
docker push ongyimeng/fund-flow:latest