FROM pypy:3
WORKDIR /usr/src/app
COPY . .
RUN ls
CMD ["pypy3", "/usr/src/app/run_match.py"]




