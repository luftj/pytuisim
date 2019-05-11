FROM python:2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/CityScope/CSL_Hamburg_Noise.git
RUN pip install --no-cache-dir -r CSL_Hamburg_Noise/requirements.txt

COPY . .

CMD [ "python", "./main.py" ]