FROM alpine
RUN echo "foobar" > foobar.txt
ARG ep=ls
ENV ep=$ep
RUN echo $ep
ARG cm=-la
ENV cm=$cm
RUN echo $cm
#ENTRYPOINT $ep
CMD $ep $cm
